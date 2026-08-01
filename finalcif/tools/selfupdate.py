#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
"""Self update of a per-user installation of FinalCif.

A machine wide installation lives in ``C:\\Program Files`` and can only be replaced by an
elevated process, therefore it still uses ``update.exe``.  An installation made with
``FinalCif-setup-x64-vNNN.exe /CURRENTUSER`` lives in ``%LocalAppData%\\Programs\\FinalCif``
and is writable by the user, so FinalCif downloads and starts the installer itself.

Everything in here is deliberately free of Qt imports so that it can be tested without a
running QApplication.  The GUI part lives in :mod:`finalcif.gui.dialogs`.
"""
from __future__ import annotations

import ctypes
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from collections.abc import Callable
from contextlib import suppress
from pathlib import Path

import requests

from finalcif import VERSION
from finalcif.tools.misc import sha512_checksum_of_file

SETUP_URL = 'https://dkratzert.de/files/finalcif/FinalCif-setup-x64-v{version}.exe'
CHECKSUM_URL = 'https://dkratzert.de/files/finalcif/FinalCif-setup-x64-v{version}-sha512.sha'
# Inno Setup checks this mutex (AppMutex in finalcif-install_win64.iss) and refuses to
# overwrite the files of a still running FinalCif:
RUNNING_MUTEX_NAME = 'FinalCifSetupMutex'
DOWNLOAD_TIMEOUT = 30
BLOCK_SIZE = 65536
# Seconds granted for a regular Qt shutdown before the process is ended the hard way:
EXIT_TIMEOUT = 10.0

_running_mutex: int | None = None


class UpdateError(Exception):
    """The update could not be performed."""


class UpdateCancelled(UpdateError):
    """The user cancelled the download."""


def installation_directory() -> Path:
    """Directory that contains finalcif.exe, update.exe and the finalcif package."""
    return Path(__file__).resolve().parent.parent.parent


def is_windows() -> bool:
    return sys.platform.startswith('win')


def is_user_installation() -> bool:
    """True if the installation can be replaced without administrator rights."""
    return is_windows() and _is_writable(installation_directory())


def _is_writable(directory: Path) -> bool:
    probe = directory / f'.finalcif-write-test-{os.getpid()}'
    try:
        probe.touch()
    except OSError:
        return False
    finally:
        with suppress(OSError):
            probe.unlink()
    return True


def _headers() -> dict[str, str]:
    return {'User-Agent': f'FinalCif v{VERSION} ({sys.platform})'}


def download_installer(version: str,
                       progress: Callable[[int, int], None] | None = None,
                       should_cancel: Callable[[], bool] | None = None) -> Path:
    """Download the installer of `version` into a fresh temporary directory.

    The installer is never written into the installation directory, because the running
    setup would not be able to remove it there.  The returned file is checksum verified.
    """
    target_dir = Path(tempfile.mkdtemp(prefix='finalcif-update-'))
    url = SETUP_URL.format(version=version)
    setup_file = target_dir / url.rsplit('/', 1)[-1]
    try:
        _download_to_file(url, setup_file, progress, should_cancel)
        _verify_checksum(setup_file, CHECKSUM_URL.format(version=version))
    except BaseException:
        shutil.rmtree(target_dir, ignore_errors=True)
        raise
    return setup_file


def _download_to_file(url: str, target: Path,
                      progress: Callable[[int, int], None] | None,
                      should_cancel: Callable[[], bool] | None) -> None:
    try:
        response = requests.get(url, stream=True, headers=_headers(), timeout=DOWNLOAD_TIMEOUT)
    except requests.RequestException as err:
        raise UpdateError(f'Could not download the installer:\n{err}') from err
    with response:
        if response.status_code != 200:
            raise UpdateError(f'The installer is not available at\n{url}\n(HTTP {response.status_code}).')
        total = int(response.headers.get('content-length', 0))
        received = 0
        # The context manager guarantees that no handle to the setup file survives:
        with target.open('wb') as setup:
            for chunk in response.iter_content(BLOCK_SIZE):
                if should_cancel is not None and should_cancel():
                    raise UpdateCancelled('The update was cancelled.')
                setup.write(chunk)
                received += len(chunk)
                if progress is not None:
                    progress(received, total)
    if total and received != total:
        raise UpdateError('The download of the installer is incomplete.')


def _verify_checksum(setup_file: Path, checksum_url: str) -> None:
    try:
        response = requests.get(checksum_url, headers=_headers(), timeout=DOWNLOAD_TIMEOUT)
    except requests.RequestException as err:
        raise UpdateError(f'Could not download the checksum:\n{err}') from err
    with response:
        if response.status_code != 200:
            raise UpdateError('No checksum file was found for this version.')
        expected = response.content.decode('ascii', errors='ignore').strip()
    if not expected:
        raise UpdateError('The checksum file of this version is empty.')
    if sha512_checksum_of_file(str(setup_file)) != expected:
        raise UpdateError('The checksum of the downloaded installer is wrong.\n'
                          'The file was not installed.')


def start_installer(setup_file: Path) -> None:
    """Start the downloaded installer as a detached process.

    Every handle FinalCif might hold in the installation directory is released before, the
    process itself has to end immediately afterwards (see `finalcif.gui.dialogs`).
    """
    release_running_mutex()
    _leave_installation_directory()
    command = [str(setup_file), *installer_parameters()]
    subprocess.Popen(command,
                     cwd=str(setup_file.parent),
                     close_fds=True,
                     creationflags=_detached_flags(),
                     stdin=subprocess.DEVNULL,
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)


def installer_parameters() -> list[str]:
    """Keep the installation in the same place and with the same privileges as before."""
    return ['/CURRENTUSER', f'/DIR={installation_directory()}']


def _detached_flags() -> int:
    if not is_windows():
        return 0
    return subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP


def _leave_installation_directory() -> None:
    """A process keeps its working directory locked, and the start menu entry uses {app}."""
    with suppress(OSError):
        current = Path(os.getcwd()).resolve()
        installation = installation_directory()
        if current == installation or installation in current.parents:
            os.chdir(tempfile.gettempdir())


def create_running_mutex() -> None:
    """Announce the running FinalCif to Inno Setup (AppMutex)."""
    global _running_mutex
    if not is_windows() or _running_mutex is not None:
        return
    with suppress(OSError, AttributeError):
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel32.CreateMutexW.restype = ctypes.c_void_p
        kernel32.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_bool, ctypes.c_wchar_p]
        _running_mutex = kernel32.CreateMutexW(None, False, RUNNING_MUTEX_NAME) or None


def release_running_mutex() -> None:
    """Let the installer proceed even though this process is not gone yet."""
    global _running_mutex
    if _running_mutex is None:
        return
    with suppress(OSError, AttributeError):
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
        kernel32.CloseHandle(_running_mutex)
    _running_mutex = None


def start_exit_watchdog(timeout: float = EXIT_TIMEOUT) -> threading.Timer:
    """End the process even if the Qt shutdown hangs.

    Every loaded .pyd and .dll keeps a lock in the installation directory, so the installer
    can only replace them once this process is really gone.  The timer is a daemon and dies
    silently with a regular shutdown.
    """
    watchdog = threading.Timer(timeout, os._exit, (0,))
    watchdog.daemon = True
    watchdog.start()
    return watchdog


def start_elevated_updater(version: str) -> None:
    """Machine wide installations need update.exe running with administrator rights."""
    updater_exe = str(installation_directory() / 'update.exe')
    ctypes.windll.shell32.ShellExecuteW(None, 'runas', updater_exe, f'-v {version} -p finalcif', None, 1)
