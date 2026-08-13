"""Tests for the residual-density controls on the details page.

The structure viewer gets its atoms from the CIF block in memory, so the
density has to be told where model and reflections are.  Without usable
reflection data the button stays disabled and no file dialog is ever opened.
"""

from pathlib import Path

import gemmi
import pytest
from qtpy import QtWidgets

from finalcif.appwindow import AppWindow
from tests.helpers import AppWindowTestCase

CIF_WITH_HKL = Path('tests/examples/1979688.cif')
CIF_WITHOUT_HKL = Path('tests/examples/Esser_JW367_0m.cif')


class TestResidualDensitySources(AppWindowTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.app = AppWindow(file=CIF_WITH_HKL)

    def test_reflections_come_from_the_block_itself(self) -> None:
        self.assertIsInstance(self.app._reflection_source(), gemmi.cif.Block)

    def test_density_is_available(self) -> None:
        self.app.show_residuals()
        self.assertTrue(self.app.ui.render_widget.has_residual_density_data)
        self.assertTrue(self.app.density_controls.button.isEnabled())

    def test_model_source_is_the_current_block(self) -> None:
        self.app.show_residuals()
        self.assertIs(self.app.ui.render_widget.model_source, self.app.cif.block)


class TestWithoutReflections(AppWindowTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.app = AppWindow(file=CIF_WITHOUT_HKL)

    def test_no_reflection_source(self) -> None:
        self.assertIsNone(self.app._reflection_source())

    def test_button_stays_disabled(self) -> None:
        self.app.show_residuals()
        self.assertFalse(self.app.density_controls.button.isEnabled())

    def test_no_file_dialog_is_opened(self, ) -> None:
        """Switching density on without data must not ask for a file."""
        self.app.show_residuals()
        original = QtWidgets.QFileDialog.getOpenFileName
        QtWidgets.QFileDialog.getOpenFileName = lambda *a, **k: pytest.fail(
            'a file dialog was opened')
        try:
            self.app.density_controls.button.setChecked(True)
        finally:
            QtWidgets.QFileDialog.getOpenFileName = original
        self.assertFalse(self.app.density_controls.button.isChecked())
        self.assertIsNone(self.app.ui.render_widget.residual_density_map)
