import unittest

from appwindow import AppWindow
from report.templated_report import TemplatedReport


@unittest.skip('foo')
class TemplateReportTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.myapp = AppWindow()
        self.myapp.running_inside_unit_test = True
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(0.0)
        self.myapp.hide()
        self.t = TemplatedReport()
        self.t.make_templated_report(options=self.myapp.options, file_obj=self.myapp.final_cif_file_name,
                                     output_filename=report_filename, picfile=picfile,
                                     template_path=Path(self.ui.TemplatesListWidget.currentItem().text()))

    def test_context_space_group(self):
        pass


if __name__ == '__main__':
    unittest.main()
