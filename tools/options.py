from gui.finalcif_gui import Ui_FinalCifWindow
from tools.settings import FinalCifSettings


class Options:
    def __init__(self, ui: Ui_FinalCifWindow, settings: FinalCifSettings):
        self.ui = ui
        self.settings = settings
        # initial default, otherwise we have width=0.0 and no picture visible:
        self.ui.PictureWidthDoubleSpinBox.setValue(7.5)
        self._connect_signal_and_slots()
        self._options = {}

    def _connect_signal_and_slots(self):
        self.ui.HAtomsCheckBox.stateChanged.connect(self._state_changed)
        self.ui.ReportTextCheckBox.stateChanged.connect(self._state_changed)
        self.ui.PictureWidthDoubleSpinBox.valueChanged.connect(self._state_changed)
        self.ui.CheckCIFServerURLTextedit.textChanged.connect(self._state_changed)
        self.ui.AtomCoordsTableCheckbox.stateChanged.connect(self._state_changed)
        self.ui.BondsAnglesTableCheckbox.stateChanged.connect(self._state_changed)
        self.ui.TorsionTableCheckBox.stateChanged.connect(self._state_changed)
        self.ui.HydrogenBondTableCheckbox.stateChanged.connect(self._state_changed)

    def show_options(self):
        """
        This method and pnöy this is called in order to show the options page.
        It also sets the state of the options widgets.
        """
        self.ui.PictureWidthDoubleSpinBox.setValue(self.picture_width)
        self.ui.ReportTextCheckBox.setChecked(not self.report_text)
        self.ui.HAtomsCheckBox.setChecked(self.without_H)
        self.ui.AtomCoordsTableCheckbox.setChecked(not self.atom_coords_table)
        self.ui.BondsAnglesTableCheckbox.setChecked(not self.bonds_angles_table)
        self.ui.TorsionTableCheckBox.setChecked(not self.torsion_table)
        self.ui.HydrogenBondTableCheckbox.setChecked(not self.hydrogen_table)
        self.ui.CheckCIFServerURLTextedit.setText(self.checkcif_url)
        self.ui.MainStackedWidget.go_to_options_page()

    def _state_changed(self):
        self._options = {
            'report_text'       : not self.ui.ReportTextCheckBox.isChecked(),
            'without_H'         : self.ui.HAtomsCheckBox.isChecked(),
            'picture_width'     : self.ui.PictureWidthDoubleSpinBox.value(),
            'checkcif_url'      : self.ui.CheckCIFServerURLTextedit.text(),
            'atom_coords_table' : not self.ui.AtomCoordsTableCheckbox.isChecked(),
            'bonds_angles_table': not self.ui.BondsAnglesTableCheckbox.isChecked(),
            'torsion_table'     : not self.ui.TorsionTableCheckBox.isChecked(),
            'hydrogen_table'    : not self.ui.HydrogenBondTableCheckbox.isChecked(),
        }
        print('saving:', self._options)
        self.settings.save_options(self._options)

    @property
    def values(self):
        # print('loading:', self._options, self.settings.load_options())
        return self.settings.load_options()

    def __getitem__(self, item):
        return self.settings.load_options()[item]

    @property
    def report_text(self):
        return self.settings.load_options()['report_text']

    @property
    def without_H(self):
        return self.settings.load_options()['without_H']

    @property
    def atom_coords_table(self):
        try:
            return self.settings.load_options()['atom_coords_table']
        except KeyError:
            return True

    @property
    def bonds_angles_table(self):
        try:
            return self.settings.load_options()['bonds_angles_table']
        except KeyError:
            return True

    @property
    def torsion_table(self):
        try:
            return self.settings.load_options()['torsion_table']
        except KeyError:
            return True

    @property
    def hydrogen_table(self):
        try:
            return self.settings.load_options()['hydrogen_table']
        except KeyError:
            return True

    @property
    def picture_width(self):
        width = self.settings.load_options()['picture_width']
        if width < 0.001:
            # preventing invisible picture
            return 7.5
        else:
            return width

    @property
    def checkcif_url(self):
        return self.settings.load_options()['checkcif_url']
