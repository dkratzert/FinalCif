from qtpy.QtCore import QSize
from qtpy.QtWidgets import QStackedWidget


class MyMainStackedWidget(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def minimumSizeHint(self) -> QSize:
        """Return zero so the stacked widget never forces the window to resize
        when switching pages. The window can still be freely resized by the user."""
        return QSize(0, 0)

    def sizeHint(self) -> QSize:
        """Return zero so content changes on any page never cause the window to
        spontaneously grow or shrink (e.g. on macOS when a page repopulates)."""
        return QSize(0, 0)

    def got_to_main_page(self):
        self.setCurrentIndex(0)

    def go_to_cif_text_page(self):
        self.setCurrentIndex(1)

    def go_to_info_page(self):
        self.setCurrentIndex(2)

    def go_to_data_sources_page(self):
        self.setCurrentIndex(3)

    def go_to_options_page(self):
        self.setCurrentIndex(4)

    def go_to_loops_page(self):
        self.setCurrentIndex(5)

    def on_loops_page(self):
        return self.currentIndex() == 5

    def go_to_checkcif_page(self):
        self.setCurrentIndex(6)

    def got_to_cod_page(self):
        self.setCurrentIndex(7)

    def go_to_text_template_page(self):
        self.setCurrentIndex(8)

    @property
    def current_page(self):
        return self.currentIndex()

    def on_checkcif_page(self):
        return self.current_page == 6

    def on_info_page(self):
        return self.current_page == 2