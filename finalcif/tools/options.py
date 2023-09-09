from contextlib import suppress

from finalcif.gui.finalcif_gui_ui import Ui_FinalCifWindow
from finalcif.tools.settings import FinalCifSettings


class Options:
    def __init__(self, ui: Ui_FinalCifWindow, settings: FinalCifSettings):
        self.ui = ui
        self.settings = settings
        # initial default, otherwise we have width=0.0 and no picture visible:
        if ui:
            self.ui.PictureWidthDoubleSpinBox.setValue(7.5)
            self._connect_signal_and_slots()
        self._options = {}

    def _connect_signal_and_slots(self):
        self.ui.HAtomsCheckBox.stateChanged.connect(self._state_changed)
        self.ui.ReportTextCheckBox.stateChanged.connect(self._state_changed)
        self.ui.PictureWidthDoubleSpinBox.valueChanged.connect(self._state_changed)
        self.ui.CheckCIFServerURLTextedit.textChanged.connect(self._state_changed)
        self.ui.CODURLTextedit.textChanged.connect(self._state_changed)
        self.ui.ADPTableCheckBox.stateChanged.connect(self._state_changed)
        self.ui.trackChangesCifCheckBox.stateChanged.connect(self._state_changed)

    def show_options(self):
        """
        This method is called in order to show the options page.
        It also sets the state of the options widgets.
        """
        self.ui.HAtomsCheckBox.setChecked(self.without_h)
        self.ui.ReportTextCheckBox.setChecked(not self.report_text)
        self.ui.PictureWidthDoubleSpinBox.setValue(self.picture_width)
        self.ui.CheckCIFServerURLTextedit.setText(self.checkcif_url)
        self.ui.CODURLTextedit.setText(self.cod_url)
        self.ui.ADPTableCheckBox.setChecked(self.report_adp)
        self.ui.trackChangesCifCheckBox.setChecked(self.track_changes)
        #
        self.ui.MainStackedWidget.go_to_options_page()

    def _state_changed(self):
        lw = self.ui.docxTemplatesListWidget
        self._options = {
            'report_text'            : not self.ui.ReportTextCheckBox.isChecked(),
            'report_adp'             : self.ui.ADPTableCheckBox.isChecked(),
            'without_h'              : self.ui.HAtomsCheckBox.isChecked(),
            'picture_width'          : self.ui.PictureWidthDoubleSpinBox.value(),
            'checkcif_url'           : self.ui.CheckCIFServerURLTextedit.text(),
            'atoms_table'            : True,
            'bonds_table'            : True,
            'hydrogen_bonds'         : True,
            'current_report_template': lw.row(lw.currentItem()),
            'cod_url'                : self.ui.CODURLTextedit.text(),
            'track_changes'          : self.ui.trackChangesCifCheckBox.isChecked(),
        }
        # print('saving:', self._options)
        self.settings.save_options(self._options)

    @property
    def values(self):
        return self.settings.load_options()

    def __getitem__(self, item):
        return self.settings.load_options()[item]

    def _get_setting(self, setting: str, default: object):
        with suppress(KeyError):
            return self.settings.load_options()[setting]
        return default

    @property
    def report_text(self) -> bool:
        return self._get_setting('report_text', True)

    @property
    def report_adp(self) -> bool:
        return self._get_setting('report_adp', True)

    @property
    def without_h(self) -> bool:
        return self._get_setting('without_h', False)

    @property
    def track_changes(self) -> bool:
        return self._get_setting('track_changes', False)

    @property
    def current_template(self) -> int:
        return self._get_setting('current_report_template', 0)

    @property
    def picture_width(self) -> float:
        width = self._get_setting('picture_width', 7.5)
        if width < 0.001:
            # preventing invisible picture
            return 7.5
        else:
            return width

    @property
    def checkcif_url(self) -> str:
        try:
            opt = self.settings.load_options()['checkcif_url']
            if opt:
                return opt
            else:
                return self.set_default_checkcif_url()
        except KeyError:
            return self.set_default_checkcif_url()

    def set_default_checkcif_url(self):
        url = 'https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl'
        self.ui.CheckCIFServerURLTextedit.setText(url)
        return url

    @property
    def cod_url(self) -> str:
        try:
            opt = self.settings.load_options()['cod_url']
            if opt:
                return opt
            else:
                return self.set_default_cod_url()
        except KeyError:
            return self.set_default_cod_url()

    def set_default_cod_url(self):
        url = 'https://www.crystallography.net/cod/cgi-bin/cif-deposit.pl'
        self.ui.CODURLTextedit.setText(url)
        return url
