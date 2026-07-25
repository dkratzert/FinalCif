from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

import requests
from qtpy.QtCore import QUrl
from qtpy.QtGui import QDesktopServices, QImage, QTextDocument
from qtpy.QtWidgets import QDialog, QTextBrowser, QVBoxLayout, QWidget

_IMG_SRC = re.compile(r'<img[^>]*\bsrc\s*=\s*["\']?([^"\'>\s]+)', re.IGNORECASE)
# Matches the checkCIF help popup links, e.g.: javascript:makeHelpWindow("PLAT042.html")
_HELP_WINDOW_LINK = re.compile(r'makeHelpWindow\(["\']?(PLAT\d+)\.html["\']?\)', re.IGNORECASE)
# The small alert-level logos, e.g. ".../iucr-top/logos/yellow.gif". IUCr's server is behind
# Cloudflare bot protection and refuses these requests, so a same-colored square is drawn locally.
_ALERT_LOGO = re.compile(r'/logos/(\w+)\.gif$', re.IGNORECASE)


class CheckCifBrowser(QTextBrowser):
    """A QTextBrowser that renders the images embedded in CheckCIF HTML results.

    QTextBrowser only resolves resources lazily on paint and never fetches network
    resources, so the IUCr alert-level logos and the structure image stay blank.
    All ``<img>`` sources are therefore downloaded up front and registered as
    document resources before the HTML is set.

    The CheckCIF HTML also contains ``javascript:makeHelpWindow(...)`` links that
    are meant to pop up a small help window explaining the PLATON alert. Since
    QTextBrowser cannot execute JavaScript, these links are intercepted and the
    matching help text (parsed from PLATON's ``check.def``) is shown in a
    dialog instead.
    """

    def __init__(self, parent: QWidget | None = None, checkdef: list[str] | None = None) -> None:
        super().__init__(parent)
        self.checkdef = checkdef or []
        self.setOpenLinks(False)
        self.anchorClicked.connect(self._on_anchor_clicked)
        self._image_cache: dict[str, QImage] = {}
        self._help_dialog: QDialog | None = None

    def set_checkcif_html(self, html: str, local_images: dict[str, Path] | None = None) -> None:
        """Register every embedded image, then display the HTML.

        Args:
            html: The CheckCIF result HTML.
            local_images: Optional mapping of image ``src`` URL → local file path to
                use instead of downloading (e.g. the locally saved structure image).
        """
        local_images = local_images or {}
        for src in dict.fromkeys(_IMG_SRC.findall(html)):
            image = self._load_image(src, local_images.get(src))
            if not image.isNull():
                self.document().addResource(QTextDocument.ResourceType.ImageResource, QUrl(src), image)
        self.setHtml(html)

    def _load_image(self, src: str, local_file: Path | None) -> QImage:
        if src in self._image_cache:
            return self._image_cache[src]
        image = QImage()
        if local_file and local_file.exists():
            image.load(str(local_file))
        if image.isNull() and src.startswith(('http://', 'https://')):
            try:
                image.loadFromData(requests.get(src, timeout=10).content)
            except requests.RequestException:
                pass
        self._image_cache[src] = image
        return image

    def _on_anchor_clicked(self, url: QUrl) -> None:
        """Handle link clicks: show a help dialog for PLATON alert links, open others externally."""
        match = _HELP_WINDOW_LINK.search(unquote(url.toString()))
        if match:
            self._show_help_window(match.group(1))
            return
        QDesktopServices.openUrl(url)

    def _show_help_window(self, alert: str) -> None:
        """Open a small dialog showing the PLATON alert explanation.

        Args:
            alert: The alert code, e.g. ``PLAT042``.
        """
        from finalcif.cif.checkcif.checkcif import AlertHelp
        helptext = AlertHelp(self.checkdef).get_help(alert) or f'No help text found for {alert}.'
        dialog = QDialog(self)
        dialog.setWindowTitle(f'checkCIF help: {alert}')
        dialog.resize(600, 350)
        layout = QVBoxLayout(dialog)
        browser = QTextBrowser(dialog)
        browser.setPlainText(helptext)
        layout.addWidget(browser)
        self._help_dialog = dialog
        dialog.show()

