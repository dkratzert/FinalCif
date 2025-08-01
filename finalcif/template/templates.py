from __future__ import annotations

from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING

from qtpy import compat
from qtpy.QtCore import Qt
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QFileDialog, QListWidgetItem

if TYPE_CHECKING:
    from finalcif.appwindow import AppWindow
    from finalcif.tools.settings import FinalCifSettings


class ReportTemplates:
    """
    Displays the list of report templates in the options menu.
    """

    def __init__(self, app: AppWindow, settings: FinalCifSettings):
        self.app = app
        self.settings = settings
        self.lw = self.app.ui.docxTemplatesListWidget
        self.load_templates_list()
        self.app.ui.AddNewTemplPushButton.clicked.connect(self.add_new_template)
        self.app.ui.RemoveTemplPushButton.clicked.connect(self.remove_current_template)
        self.app.ui.docxTemplatesListWidget.currentItemChanged.connect(self.template_changed)
        self.app.ui.docxTemplatesListWidget.itemChanged.connect(self.template_changed)
        self.app.ui.docxTemplatesListWidget.setCurrentItem(
            self.app.ui.docxTemplatesListWidget.item(self.app.options.current_template))

    def add_new_template(self, templ_path: str = '') -> None:
        if not templ_path:
            templ_path, _ = compat.getopenfilename(parent=self.app, filters="DOCX file (*.docx);; html file (*.html *.tmpl)",
                                                        selectedfilter="DOCX file (*.docx)",
                                                        caption='Open a Report Template File')
        itemslist = self.get_templates_list_from_widget()
        self.app.status_bar.show_message('')
        if templ_path in itemslist:
            self.app.status_bar.show_message('This templates is already in the list.', 10)
            print('This templates is already in the list.')
            return
        if (not Path(templ_path).exists() or not Path(templ_path).is_file()
                or Path(templ_path).suffix not in ('.docx', '.html', '.tmpl')):
            self.app.status_bar.show_message('This template does not exist or is unreadable.', 10)
            print('This template does not exist or is unreadable.', Path(templ_path).resolve())
            return
        item = QListWidgetItem(templ_path)
        item.setCheckState(Qt.CheckState.Unchecked)
        self.app.ui.docxTemplatesListWidget.addItem(item)
        self.settings.save_template_list('report_templates_list', self.get_templates_list_from_widget())

    def load_templates_list(self):
        templates = self.settings.load_value_of_key('report_templates_list')
        if not templates:
            return
        for text in templates:
            if text.startswith('Use'):
                continue
            with suppress(Exception):
                if not Path(text).exists():
                    item = QListWidgetItem(text)
                    item.setForeground(QColor(220, 12, 34))
                else:
                    item = QListWidgetItem(str(Path(text).resolve(strict=True)))
            self.app.ui.docxTemplatesListWidget.addItem(item)
            item.setCheckState(Qt.CheckState.Unchecked)

    def get_templates_list_from_widget(self) -> list:
        itemslist = []
        for num in range(self.lw.count()):
            itemtext = self.lw.item(num).text()
            if itemtext not in itemslist:
                itemslist.append(itemtext)
        return itemslist

    def remove_current_template(self) -> None:
        if self.lw.currentRow() == 0:
            return
        self.lw.takeItem(self.lw.row(self.lw.currentItem()))
        self.settings.save_template_list('report_templates_list', self.get_templates_list_from_widget())

    def template_changed(self, current_item: QListWidgetItem):
        # Blocking signal in order to avoid infinitive recursion:
        self.app.ui.docxTemplatesListWidget.blockSignals(True)
        options = self.settings.load_options()
        options.update({'current_report_template': self.lw.row(current_item)})
        self.uncheck_all_templates()
        if not current_item:
            self.app.ui.docxTemplatesListWidget.blockSignals(False)
            return
        current_item.setCheckState(Qt.CheckState.Checked)
        self.settings.save_options(options)
        self.app.ui.docxTemplatesListWidget.blockSignals(False)

    def uncheck_all_templates(self):
        for num in range(self.lw.count()):
            self.lw.item(num).setCheckState(Qt.CheckState.Unchecked)

    def report_from_default_template(self) -> bool:
        """Check whether the report is generated from a template or hard-coded"""
        return (self.lw.item(0).checkState() == Qt.CheckState.Checked
                or not self.lw.currentItem())
