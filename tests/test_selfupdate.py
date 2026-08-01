import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
import requests

from finalcif.tools import selfupdate
from finalcif.tools.selfupdate import UpdateCancelled, UpdateError

SETUP_CONTENT = b'x' * 3000


class FakeResponse:
    def __init__(self, content: bytes = b'', status_code: int = 200, headers: dict | None = None) -> None:
        self.content = content
        self.status_code = status_code
        self.headers = headers if headers is not None else {'content-length': str(len(content))}

    def iter_content(self, block_size: int):
        for start in range(0, len(self.content), block_size):
            yield self.content[start:start + block_size]

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False


@pytest.fixture()
def fake_server(monkeypatch):
    """Serve the installer and its checksum from memory."""
    from finalcif.tools.misc import sha512_checksum_of_file

    checksum = {'value': None}

    def fake_get(url, **_kwargs):
        if url.endswith('.sha'):
            return FakeResponse(content=(checksum['value'] or '').encode('ascii'))
        return FakeResponse(content=SETUP_CONTENT)

    monkeypatch.setattr(requests, 'get', fake_get)
    # The checksum the server announces is calculated from the same bytes the server sends:
    tmp = Path(tempfile.mkdtemp()) / 'setup.exe'
    tmp.write_bytes(SETUP_CONTENT)
    checksum['value'] = sha512_checksum_of_file(str(tmp))
    tmp.unlink()
    return checksum


def test_installation_directory_is_the_package_parent():
    assert selfupdate.installation_directory() == Path(__file__).resolve().parent.parent


def test_download_installer_writes_outside_the_installation_directory(fake_server):
    setup_file = selfupdate.download_installer('169')
    try:
        assert setup_file.read_bytes() == SETUP_CONTENT
        assert setup_file.name == 'FinalCif-setup-x64-v169.exe'
        assert selfupdate.installation_directory() not in setup_file.parents
        assert Path(tempfile.gettempdir()).resolve() in setup_file.resolve().parents
    finally:
        setup_file.unlink(missing_ok=True)


def test_download_installer_rejects_a_wrong_checksum(fake_server):
    fake_server['value'] = 'deadbeef'
    with pytest.raises(UpdateError, match='checksum'):
        selfupdate.download_installer('169')


def test_download_installer_removes_the_temporary_directory_on_failure(fake_server, monkeypatch):
    created = []
    original_mkdtemp = tempfile.mkdtemp

    def remember(*args, **kwargs):
        directory = original_mkdtemp(*args, **kwargs)
        created.append(Path(directory))
        return directory

    monkeypatch.setattr(tempfile, 'mkdtemp', remember)
    fake_server['value'] = 'deadbeef'
    with pytest.raises(UpdateError):
        selfupdate.download_installer('169')
    assert created and not created[0].exists()


def test_download_installer_can_be_cancelled(fake_server):
    with pytest.raises(UpdateCancelled):
        selfupdate.download_installer('169', should_cancel=lambda: True)


def test_download_installer_reports_a_missing_installer(monkeypatch):
    monkeypatch.setattr(requests, 'get', lambda url, **kwargs: FakeResponse(status_code=404))
    with pytest.raises(UpdateError, match='404'):
        selfupdate.download_installer('169')


def test_download_installer_reports_a_connection_error(monkeypatch):
    def failing_get(url, **kwargs):
        raise requests.ConnectionError('no network')

    monkeypatch.setattr(requests, 'get', failing_get)
    with pytest.raises(UpdateError, match='no network'):
        selfupdate.download_installer('169')


def test_progress_is_reported(fake_server):
    seen = []
    setup_file = selfupdate.download_installer('169', progress=lambda done, total: seen.append((done, total)))
    setup_file.unlink(missing_ok=True)
    assert seen[-1] == (len(SETUP_CONTENT), len(SETUP_CONTENT))


def test_installer_keeps_the_current_installation_directory():
    parameters = selfupdate.installer_parameters()
    assert parameters[0] == '/CURRENTUSER'
    assert parameters[1] == f'/DIR={selfupdate.installation_directory()}'


def test_leave_installation_directory_changes_away_from_the_installation(monkeypatch, tmp_path):
    changed_to = []
    installation = str(selfupdate.installation_directory())
    monkeypatch.setattr(selfupdate, 'installation_directory', lambda: Path(installation))
    monkeypatch.setattr(os, 'getcwd', lambda: installation)
    monkeypatch.setattr(os, 'chdir', lambda path: changed_to.append(Path(path)))
    selfupdate._leave_installation_directory()
    assert changed_to == [Path(tempfile.gettempdir())]


def test_leave_installation_directory_keeps_an_unrelated_working_directory(monkeypatch, tmp_path):
    changed_to = []
    installation = selfupdate.installation_directory()
    unrelated = str(tmp_path.resolve())
    monkeypatch.setattr(selfupdate, 'installation_directory', lambda: installation)
    monkeypatch.setattr(os, 'getcwd', lambda: unrelated)
    monkeypatch.setattr(os, 'chdir', lambda path: changed_to.append(Path(path)))
    selfupdate._leave_installation_directory()
    assert changed_to == []


def test_start_installer_runs_detached_from_the_installation_directory(monkeypatch, tmp_path):
    calls = {}

    def fake_popen(command, **kwargs):
        calls['command'] = command
        calls.update(kwargs)

    monkeypatch.setattr(subprocess, 'Popen', fake_popen)
    monkeypatch.setattr(os, 'chdir', lambda path: None)
    setup_file = tmp_path / 'FinalCif-setup-x64-v169.exe'
    setup_file.touch()
    selfupdate.start_installer(setup_file)
    assert calls['command'][0] == str(setup_file)
    assert calls['cwd'] == str(tmp_path)
    assert calls['close_fds'] is True
    assert calls['stdin'] == subprocess.DEVNULL
    if sys.platform.startswith('win'):
        assert calls['creationflags'] & subprocess.DETACHED_PROCESS


@pytest.mark.skipif(not sys.platform.startswith('win'), reason='The mutex is a Windows feature')
def test_running_mutex_is_created_and_released():
    selfupdate.release_running_mutex()
    selfupdate.create_running_mutex()
    assert selfupdate._running_mutex is not None
    selfupdate.release_running_mutex()
    assert selfupdate._running_mutex is None


def test_exit_watchdog_is_a_daemon_and_can_be_cancelled():
    watchdog = selfupdate.start_exit_watchdog(timeout=600)
    try:
        assert watchdog.daemon
        assert watchdog.is_alive()
    finally:
        watchdog.cancel()
