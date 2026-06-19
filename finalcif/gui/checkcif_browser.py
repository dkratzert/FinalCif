from __future__ import annotations

import re
from pathlib import Path

import requests
from qtpy.QtCore import QUrl
from qtpy.QtGui import QImage, QTextDocument
from qtpy.QtWidgets import QTextBrowser, QWidget

_IMG_SRC = re.compile(r'<img[^>]*\bsrc\s*=\s*["\']?([^"\'>\s]+)', re.IGNORECASE)


class CheckCifBrowser(QTextBrowser):
    """A QTextBrowser that renders the images embedded in CheckCIF HTML results.

    QTextBrowser only resolves resources lazily on paint and never fetches network
    resources, so the IUCr alert-level logos and the structure image stay blank.
    All ``<img>`` sources are therefore downloaded up front and registered as
    document resources before the HTML is set.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setOpenExternalLinks(True)
        self._image_cache: dict[str, QImage] = {}

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

