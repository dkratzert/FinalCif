from unittest import TestCase

from cif.cod.deposit import COD_Deposit


class TestCOD_Deposit(TestCase):

    def setUp(self) -> None:
        self.cod = COD_Deposit('tests/examples/1979688.cif')

    def test__personal_was_toggled(self):
        self.cod._personal_was_toggled(True)
        # TODO make this a test:
        self.cod.ui.prepublicationDepositCheckBox.setChecked(False)
        self.cod.ui.publishedDepositionCheckBox.setChecked(False)

            self.cod.ui.depositionOptionsStackedWidget.setCurrentIndex(0)
            self.cod.deposition_type = 'personal'
            self.cod.reset_deposit_button_state_to_initial()
