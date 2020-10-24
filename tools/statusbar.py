from typing import Union

from gui.finalcif_gui import Ui_FinalCifWindow


class StatusBar():
    """
    An abstraction class to display messages either on the status bar
    or the console if statusbar is unavailable.
    """

    def __init__(self, ui: Union[Ui_FinalCifWindow, None] = None):
        self.ui = ui
        self._message = ''
        if ui:
            self.graphics = True
        else:
            self.graphics = False

    @property
    def current_message(self) -> str:
        if self.graphics:
            return self.ui.statusBar.currentMessage()
        else:
            return self._message

    def set_message(self, message: Union[str, list]):
        self._message = self.message_to_string(message)
        if self.graphics:
            self.ui.statusBar.showMessage(self._message)
        else:
            print(self._message)

    def message_to_string(self, message: Union[str, list]) -> str:
        if isinstance(message, list):
            return ' '.join(message)
        return message

    def show_message(self, message: str) -> None:
        self.set_message(message)
