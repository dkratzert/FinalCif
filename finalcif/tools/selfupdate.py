#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
"""Self update of a FinalCif installation on Windows.

FinalCif downloads the installer of the new version itself and starts it afterward.  An
installation made with ``FinalCif-setup-x64-vNNN.exe /CURRENTUSER`` lives in
``%LocalAppData%\\Programs\\FinalCif`` and is replaced by an ordinary process, a machine wide
installation in ``C:\\Program Files`` needs an elevated installer, which is requested with
``ShellExecuteW('runas', ...)``.

FinalCif cannot end itself before the installer starts, but every loaded ``.exe``/``.pyd``/
``.dll`` keeps a lock in the installation directory.  Therefore the installer is not started
directly but by a small ``.cmd`` launcher that ends all FinalCif processes with ``taskkill``
first and starts the installer afterwards, exactly like the standalone updater did before.

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
import time
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
# A virus scanner can hold the freshly downloaded installer for a moment:
LOCKED_FILE_ATTEMPTS = 5
LOCKED_FILE_DELAY = 1.0
# Downloads of this age belong to a previous update and not to a second running FinalCif:
LEFTOVER_DOWNLOAD_AGE = 3600.0
# Seconds granted for a regular Qt shutdown before the process is ended the hard way:
EXIT_TIMEOUT = 10.0
# The launcher ends every process with this name before it starts the installer:
PROCESS_NAME = 'finalcif.exe'
LAUNCHER_SCRIPT_NAME = 'update-finalcif.cmd'
# Rounds of taskkill the launcher performs before it starts the installer anyway:
KILL_ATTEMPTS = 5
# nShowCmd values of ShellExecuteW:
SW_HIDE = 0
SW_SHOWNORMAL = 1

_running_mutex: int | None = None


class UpdateError(Exception):
    """The update could not be performed."""


class UpdateCancelled(UpdateError):
    """The user cancelled the download."""


class ElevationRefused(UpdateError):
    """The installer of a machine wide installation did not get administrator rights."""


def installation_directory() -> Path:
    """Directory that contains finalcif.exe and the finalcif package."""
    return Path(__file__).resolve().parent.parent.parent


def is_windows() -> bool:
    return sys.platform.startswith('win')


def can_self_update() -> bool:
    """Only the Windows version is shipped with an installer."""
    return is_windows()


def is_installed() -> bool:
    """False when FinalCif runs from a source checkout instead of from an installation.

    An installation ships its own python.exe next to the finalcif package, a checkout runs
    with the python.exe of a virtual environment somewhere else.
    """
    return Path(sys.executable).resolve().parent == installation_directory()


def is_user_installation() -> bool:
    """True if the installation belongs to the current user and needs no elevation.

    Being able to write into the installation directory is not sufficient, because an
    elevated FinalCif may write into ``C:\\Program Files`` as well, while its installer
    still has to run as administrator.
    """
    if not is_windows():
        return False
    local_app_data = os.environ.get('LOCALAPPDATA')
    if not local_app_data:
        return False
    installation = installation_directory()
    user_directory = Path(local_app_data).resolve()
    return user_directory == installation or user_directory in installation.parents


def user_installation_directory() -> Path:
    """The place a per-user installation goes to (see ``/CURRENTUSER`` in the Inno script)."""
    local_app_data = os.environ.get('LOCALAPPDATA')
    base = Path(local_app_data) if local_app_data else Path.home() / 'AppData' / 'Local'
    return base / 'Programs' / 'FinalCif'


def is_elevated() -> bool:
    """True if FinalCif itself runs with administrator rights."""
    if not is_windows():
        return False
    with suppress(OSError, AttributeError):
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    return False


def _headers() -> dict[str, str]:
    return {'User-Agent': f'FinalCif v{VERSION} ({sys.platform})'}


def download_installer(version: str,
                       progress: Callable[[int, int], None] | None = None,
                       should_cancel: Callable[[], bool] | None = None) -> Path:
    """Download the installer of `version` into a fresh temporary directory.

    The installer is never written into the installation directory, because the running
    setup would not be able to remove it there.  The returned file is checksum verified.
    """
    _remove_leftover_downloads()
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


def _remove_leftover_downloads() -> None:
    """An installer of a previous update is a few hundred megabytes of garbage.

    Only old directories are touched; a young one may belong to a second FinalCif that is
    downloading right now or has just started its installer.
    """
    too_old = time.time() - LEFTOVER_DOWNLOAD_AGE
    for directory in Path(tempfile.gettempdir()).glob('finalcif-update-*'):
        with suppress(OSError):
            if directory.is_dir() and directory.stat().st_mtime < too_old:
                shutil.rmtree(directory, ignore_errors=True)


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
        try:
            # The context manager guarantees that no handle to the setup file survives:
            with target.open('wb') as setup:
                for chunk in response.iter_content(BLOCK_SIZE):
                    if should_cancel is not None and should_cancel():
                        raise UpdateCancelled('The update was cancelled.')
                    setup.write(chunk)
                    received += len(chunk)
                    if progress is not None:
                        progress(received, total)
        except (requests.RequestException, OSError) as err:
            raise UpdateError(f'The download of the installer failed:\n{err}') from err
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
        content = response.content.decode('ascii', errors='ignore')
    # A checksum file may hold the file name behind the hash ('<hash> *installer.exe'):
    words = content.split()
    expected = words[0].lower() if words else ''
    if not expected:
        raise UpdateError('The checksum file of this version is empty.')
    if _checksum_of_downloaded_file(setup_file).lower() != expected:
        raise UpdateError('The checksum of the downloaded installer is wrong.\n'
                          'The file was not installed.')


def _checksum_of_downloaded_file(setup_file: Path, attempts: int = LOCKED_FILE_ATTEMPTS) -> str:
    """A virus scanner may still hold the freshly written installer, so this waits a bit."""
    for attempt in range(attempts):
        try:
            return sha512_checksum_of_file(str(setup_file))
        except OSError as err:
            if attempt == attempts - 1:
                raise UpdateError(f'The downloaded installer could not be read:\n{err}') from err
            time.sleep(LOCKED_FILE_DELAY)
    raise UpdateError('The downloaded installer could not be read.')


def start_installer(setup_file: Path) -> None:
    """Hand the downloaded installer over to the launcher script.

    The launcher ends every running FinalCif before the installer replaces the files, so this
    process may (and should) quit immediately afterwards (see `finalcif.gui.dialogs`).  A
    machine wide installation is only replaceable by an elevated installer, so the user is
    asked for administrator rights.  Without them, :class:`ElevationRefused` offers the caller
    the per-user installation as a way out.
    """
    release_running_mutex()
    _leave_installation_directory()
    if not is_installed():
        # A source checkout must not be overwritten by the installer:
        _start_update(setup_file, user_installer_parameters(), elevated=False)
    elif is_user_installation():
        _start_update(setup_file, installer_parameters(), elevated=False)
    else:
        _start_update(setup_file, installer_parameters(), elevated=True)


def start_user_installer(setup_file: Path) -> None:
    """Install into the user directory, which needs no administrator rights at all.

    This is the fallback for restricted accounts that cannot update the machine wide
    installation in ``C:\\Program Files``.
    """
    release_running_mutex()
    _leave_installation_directory()
    _start_update(setup_file, user_installer_parameters(), elevated=False)


def _start_update(setup_file: Path, parameters: list[str], elevated: bool) -> None:
    """Start the launcher script that kills FinalCif and installs the new version.

    A launcher that cannot be written or started is no reason to give up the update; the
    installer is started directly then and complains itself about files in use.
    """
    script = _write_launcher_script(setup_file, parameters)
    if script is None:
        _start_installer_directly(setup_file, parameters, elevated)
        return
    try:
        if elevated:
            _start_launcher_elevated(script)
        else:
            _start_launcher(script)
    except ElevationRefused:
        raise
    except UpdateError:
        _start_installer_directly(setup_file, parameters, elevated)


def _start_installer_directly(setup_file: Path, parameters: list[str], elevated: bool) -> None:
    if elevated:
        _start_elevated(setup_file, parameters)
    else:
        _start_detached(setup_file, parameters)


def _write_launcher_script(setup_file: Path, parameters: list[str]) -> Path | None:
    """Write the script that ends FinalCif and starts the installer next to the installer."""
    script = setup_file.parent / LAUNCHER_SCRIPT_NAME
    try:
        script.write_text(_launcher_script_text(setup_file, parameters), encoding='ascii')
    except (OSError, UnicodeEncodeError):
        return None
    return script


def _launcher_script_text(setup_file: Path, parameters: list[str]) -> str:
    """The batch equivalent of the former standalone updater.

    ``taskkill`` reports a non-zero exit code once no FinalCif is left, which ends the wait
    loop.  Neither pipes nor ``start`` nor ``timeout`` are used, because the launcher runs
    without a console; ``ping`` is the sleep of a console-less script.
    """
    installer = subprocess.list2cmdline([str(setup_file), *parameters])
    return ('@echo off\r\n'
            f'for /l %%A in (1,1,{KILL_ATTEMPTS}) do (\r\n'
            f'    taskkill /f /im "{PROCESS_NAME}" >nul 2>&1 || goto install\r\n'
            '    ping -n 3 127.0.0.1 >nul\r\n'
            ')\r\n'
            ':install\r\n'
            f'{installer}\r\n')


def _start_launcher(script: Path) -> None:
    """Run the launcher hidden and detached, so it survives the end of FinalCif."""
    command = [_command_processor(), '/c', str(script)]
    for attempt in range(LOCKED_FILE_ATTEMPTS):
        try:
            subprocess.Popen(command,
                             cwd=str(script.parent),
                             close_fds=True,
                             creationflags=_detached_flags(),
                             stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
            return
        except OSError as err:
            if attempt == LOCKED_FILE_ATTEMPTS - 1:
                raise UpdateError(f'The installer could not be started:\n{err}') from err
            time.sleep(LOCKED_FILE_DELAY)


def _start_launcher_elevated(script: Path) -> None:
    """Ask for administrator rights and run the launcher with them.

    The UAC prompt is answered before FinalCif quits, so a refusal can still be reported.
    """
    if is_elevated():
        # A child of an elevated FinalCif is elevated as well, no UAC prompt needed:
        _start_launcher(script)
        return
    parameters = subprocess.list2cmdline(['/c', str(script)])
    result = _shell_execute(_command_processor(), parameters, str(script.parent), show=SW_HIDE)
    # ShellExecuteW returns a value greater than 32 on success:
    if result <= 32:
        raise ElevationRefused(f'{installation_directory()}\n'
                               'can only be updated with administrator rights, which were not granted.')


def _command_processor() -> str:
    """cmd.exe of the system directory, which no FinalCif installation can ever lock."""
    system_root = os.environ.get('SystemRoot')
    if system_root:
        cmd = Path(system_root) / 'System32' / 'cmd.exe'
        if cmd.is_file():
            return str(cmd)
    return os.environ.get('COMSPEC') or 'cmd.exe'


def _start_detached(setup_file: Path, parameters: list[str]) -> None:
    command = [str(setup_file), *parameters]
    for attempt in range(LOCKED_FILE_ATTEMPTS):
        try:
            subprocess.Popen(command,
                             cwd=str(setup_file.parent),
                             close_fds=True,
                             creationflags=_detached_flags(),
                             stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
            return
        except OSError as err:
            if attempt == LOCKED_FILE_ATTEMPTS - 1:
                raise UpdateError(f'The installer could not be started:\n{err}') from err
            time.sleep(LOCKED_FILE_DELAY)


def _start_elevated(setup_file: Path, parameters: list[str]) -> None:
    """Ask for administrator rights and start the installer with them."""
    if is_elevated():
        # A child of an elevated FinalCif is elevated as well, no UAC prompt needed:
        _start_detached(setup_file, parameters)
        return
    result = _shell_execute(str(setup_file), subprocess.list2cmdline(parameters), str(setup_file.parent))
    # ShellExecuteW returns a value greater than 32 on success:
    if result <= 32:
        raise ElevationRefused(f'{installation_directory()}\n'
                               'can only be updated with administrator rights, which were not granted.')


def _shell_execute(file: str, parameters: str, directory: str, show: int = SW_SHOWNORMAL) -> int:
    """Run `file` with the 'runas' verb, which triggers the UAC prompt."""
    return ctypes.windll.shell32.ShellExecuteW(None, 'runas', file, parameters, directory, show)


def installer_parameters() -> list[str]:
    """Keep the installation in the same place and with the same privileges as before."""
    scope = '/CURRENTUSER' if is_user_installation() else '/ALLUSERS'
    return [scope, f'/DIR={installation_directory()}']


def user_installer_parameters() -> list[str]:
    return ['/CURRENTUSER', f'/DIR={user_installation_directory()}']


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
