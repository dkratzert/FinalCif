from pathlib import Path

import os

import pytest

from finalcif.cif.checkcif.checkcif import (CheckCifFormParser, find_matching_fcf_file,
                                            needs_structure_factor_upload)

FCF_REQUEST_HTML = Path('tests/fixtures/checkcif_fcf_request.html').read_text()


@pytest.fixture
def parser() -> CheckCifFormParser:
    return CheckCifFormParser(FCF_REQUEST_HTML)


def test_needs_structure_factor_upload():
    assert needs_structure_factor_upload(FCF_REQUEST_HTML)


def test_regular_report_needs_no_upload():
    assert not needs_structure_factor_upload('<html><body>No alerts found</body></html>')


def test_both_forms_are_found(parser: CheckCifFormParser):
    assert len(parser.forms) == 2


def test_fcf_upload_form(parser: CheckCifFormParser):
    form = parser.fcf_upload_form
    assert form.file_input_name == 'filehkl'
    assert form.hidden_data['Qcifid'] == 'sNB9cLi6MS'
    assert form.hidden_data['Qdatablock'] == 'zubju66_a_sq'
    assert 'Upload structure factor file' in form.submit_data


def test_form_url_from_protocol_relative_action(parser: CheckCifFormParser):
    url = parser.fcf_upload_form.url('https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl')
    assert url == 'https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl'


def test_form_without_action_falls_back_to_base_url(parser: CheckCifFormParser):
    form = parser.fcf_upload_form
    form.action = ''
    assert form.url('https://foo.bar/baz.pl') == 'https://foo.bar/baz.pl'


def test_no_structure_factors_form(parser: CheckCifFormParser):
    form = parser.no_structure_factors_form
    assert form.file_input_name == ''
    assert 'Qsubmitnow' in form.submit_data
    assert 'Qdatablock' not in form.hidden_data


def test_payload_contains_hidden_and_submit_fields(parser: CheckCifFormParser):
    payload = parser.no_structure_factors_form.payload
    assert payload['referer'] == 'checkcif_server'
    assert payload['Qsubmitnow'] == 'Submit for checking (without remaining structure factors)'


def _make_files(directory: Path, fcf_name: str, time_difference: float = 0.0) -> Path:
    source_cif = directory / 'foo.cif'
    source_cif.write_text('data_foo')
    finalcif_file = directory / 'foo-finalcif.cif'
    finalcif_file.write_text('data_foo')
    fcf_file = directory / fcf_name
    fcf_file.write_text('data_foo_fcf')
    reference_time = source_cif.stat().st_mtime
    os_time = reference_time + time_difference
    os.utime(fcf_file, (os_time, os_time))
    return finalcif_file


def test_fcf_without_finalcif_suffix_is_found(tmp_path: Path):
    finalcif_file = _make_files(tmp_path, 'foo.fcf')
    assert find_matching_fcf_file(finalcif_file) == tmp_path / 'foo.fcf'


def test_fcf_with_finalcif_suffix_is_found(tmp_path: Path):
    finalcif_file = _make_files(tmp_path, 'foo-finalcif.fcf')
    assert find_matching_fcf_file(finalcif_file) == tmp_path / 'foo-finalcif.fcf'


def test_too_old_fcf_is_rejected(tmp_path: Path):
    finalcif_file = _make_files(tmp_path, 'foo.fcf', time_difference=-7200)
    assert find_matching_fcf_file(finalcif_file) is None


def test_too_new_fcf_is_rejected(tmp_path: Path):
    finalcif_file = _make_files(tmp_path, 'foo.fcf', time_difference=7200)
    assert find_matching_fcf_file(finalcif_file) is None


def test_closest_fcf_in_time_is_taken(tmp_path: Path):
    finalcif_file = _make_files(tmp_path, 'foo.fcf', time_difference=-1000)
    other = tmp_path / 'foo-finalcif.fcf'
    other.write_text('data_foo_fcf')
    reference_time = (tmp_path / 'foo.cif').stat().st_mtime - 100
    os.utime(other, (reference_time, reference_time))
    assert find_matching_fcf_file(finalcif_file) == other


def test_no_fcf_file_at_all(tmp_path: Path):
    finalcif_file = tmp_path / 'foo-finalcif.cif'
    finalcif_file.write_text('data_foo')
    assert find_matching_fcf_file(finalcif_file) is None
