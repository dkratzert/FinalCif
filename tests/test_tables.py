import os
import sys
import unittest
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from appwindow import AppWindow

app = QApplication(sys.argv)


class TablesTestCase(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.testcif = Path('tests/examples/1979688.cif').absolute()
        self.myapp = AppWindow(self.testcif)
        self.myapp.hide()  # For full screen view
        self.myapp.ui.LoopsPushButton.click()
        self.reportdoc = Path('report_' + self.testcif.stem + '-finalcif.docx')
        self.report_zip = Path(self.testcif.stem + '-finalcif.zip')

    def tearDown(self) -> None:
        self.myapp.final_cif_file_name.unlink(missing_ok=True)
        self.reportdoc.unlink(missing_ok=True)
        self.report_zip.unlink(missing_ok=True)

    def test_picture(self):
        self.myapp.set_report_picture(Path('../../icon/finalcif.png'))
        self.myapp.ui.SaveFullReportButton.click()
        self.assertEqual(True, self.reportdoc.exists())


if __name__ == '__main__':
    unittest.main()
