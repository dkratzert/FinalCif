"""Tests for the CheckCIF log summary of added validation response forms."""

from pathlib import Path

from finalcif.appwindow import AppWindow
from tests.helpers import AppWindowTestCase


class TestVrfSummaryMessage(AppWindowTestCase):
    """The 'no alerts' branch is only reached for C/G-only CheckCIF reports."""

    def setUp(self) -> None:
        super().setUp()
        self.app = AppWindow(file=Path('tests/examples/work/cu_BruecknerJK_153F40_0m.cif').resolve())
        self.app.hide()

    def test_no_alerts_without_c_alerts_requested(self):
        self.app.ui.explainCAlertsCheckBox.setChecked(False)

        self.assertEqual('<br><b>No level A or B alerts require a response.</b>',
                         self.app._vrf_summary_message(0))

    def test_no_alerts_with_c_alerts_requested(self):
        self.app.ui.explainCAlertsCheckBox.setChecked(True)

        self.assertEqual('<br><b>No level A, B or C alerts require a response.</b>',
                         self.app._vrf_summary_message(0))

    def test_single_form_uses_singular_noun(self):
        self.assertEqual('<br><b>1 validation response form added to the main table.</b>',
                         self.app._vrf_summary_message(1))

    def test_multiple_forms_use_plural_noun(self):
        self.assertEqual('<br><b>3 validation response forms added to the main table.</b>',
                         self.app._vrf_summary_message(3))
