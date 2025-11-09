import sys
import zipfile
from pathlib import Path

from finalcif.gui.custom_classes import light_red
from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtCore import Qt


class VZSImageViewer(QtWidgets.QWidget):
    zip_path: None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.zipfile: zipfile.ZipFile
        self.image_names: list[Path] | None = None
        self.index = 0
        self.pixmap = None
        # self.setMinimumSize(300, 300)
        self.zoom_rect = None
        self.zoomed = False
        self.zoom_start = None
        self.zoom_end = None
        self.rotation: float = 0.0

    def load_file(self, file_path: Path) -> None:
        if not file_path or not file_path.is_file():
            return
        if file_path.suffix.lower() == '.vzs':
            self._load_zip(file_path)
        elif file_path.suffix.lower() == '.jpg':
            self.load_jpegs(file_path)

    def load_jpegs(self, file_path: Path):
        self.zipfile = None
        globber = f'{file_path.stem.rstrip("1234567890")}*.jpg'
        self.image_names = list(file_path.parent.glob(globber))
        self.image_names.sort()
        self._load_current_image()

    def _load_zip(self, zip_path: Path) -> None:
        self.zipfile = zipfile.ZipFile(zip_path, mode="r")
        if self.zipfile.namelist():
            self.image_names = [name for name in self.zipfile.namelist()
                                if name.lower().endswith(".jpg")]
            self.image_names.sort()
            self._load_orientation()
            self._load_current_image()

    def _load_orientation(self) -> None:
        parameters = 'params.txt'
        if parameters in self.zipfile.namelist():
            for line in self.zipfile.open(parameters):
                if line.startswith(b'Microscope Rotation'):
                    splitline = line.decode('latin1').rstrip().split('=')
                    if len(splitline) > 1:
                        _, rotation = splitline
                        try:
                            self.rotation = float(rotation)
                        except ValueError:
                            print(f'Rotation value invalid: {rotation}')
                            self.rotation = 0.0
                        return None

    def reset(self) -> None:
        self.pixmap = None
        self.update()

    def _load_current_image(self) -> None:
        if not self.image_names:
            self.pixmap = None
            return
        data = self._read_data()
        image = QtGui.QImage()
        image.loadFromData(data)
        t = QtGui.QTransform().rotate(self.rotation)
        rotated = image.transformed(t, QtCore.Qt.TransformationMode.SmoothTransformation)
        self.pixmap = QtGui.QPixmap().fromImage(rotated)
        self.update()

    def save_image(self, file_path: Path) -> None:
        size = self.pixmap.size()
        cropped = self.pixmap.copy(self.zoom_rect)
        scaled = cropped.scaled(size, Qt.AspectRatioMode.KeepAspectRatio,
                                Qt.TransformationMode.SmoothTransformation)
        self.pixmap = scaled
        self.pixmap.save(str(file_path))

    def _read_data(self) -> bytes:
        if self.zipfile:
            with self.zipfile.open(self.image_names[self.index]) as f:
                data = f.read()
        else:
            with open(self.image_names[self.index], 'rb') as f:
                data = f.read()
        return data

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if not self.pixmap:
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter,
                             "No images found.\nSelect a crystal video file.")
            return
        if self.zoomed and self.zoom_rect:
            cropped = self.pixmap.copy(self.zoom_rect)
            scaled = cropped.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                    Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(self.rect().center() - scaled.rect().center(), scaled)
        else:
            scaled = self.pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(self.rect().center() - scaled.rect().center(), scaled)
        if self.zoom_start and self.zoom_end:
            pen = painter.pen()
            pen.setColor(light_red)
            pen.setWidth(1)
            painter.setPen(pen)
            rect = QtCore.QRectF(self.zoom_start, self.zoom_end)
            painter.drawRect(rect)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if not self.image_names:
            return
        if event.angleDelta().y() > 0:
            self.next()
        else:
            self.previous()

    def previous(self) -> None:
        self.index = (self.index + 1) % len(self.image_names)
        self._load_current_image()

    def next(self) -> None:
        self.index = (self.index - 1) % len(self.image_names)
        self._load_current_image()

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self.pixmap:
            self.zoom_start = event.position().toPoint()
            self.zoom_end = None

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if self.zoom_start:
            self.zoom_end = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        if self.zoom_start and self.pixmap:
            self.zoom_end = event.position().toPoint()
            rect = QtCore.QRectF(self.zoom_start, self.zoom_end).normalized()
            scaled = self.pixmap.scaled(self.size(),
                                        Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            offset = self.rect().center() - scaled.rect().center()
            x_ratio = self.pixmap.width() / scaled.width()
            y_ratio = self.pixmap.height() / scaled.height()
            img_rect = scaled.rect().translated(offset)
            intersected = rect.intersected(img_rect)
            if intersected.isValid():
                x1 = (intersected.left() - offset.x()) * x_ratio
                y1 = (intersected.top() - offset.y()) * y_ratio
                x2 = (intersected.right() - offset.x()) * x_ratio
                y2 = (intersected.bottom() - offset.y()) * y_ratio
                self.zoom_rect = QtCore.QRectF(x1, y1, x2 - x1, y2 - y1).toRect().intersected(self.pixmap.rect())
                if self.zoom_rect.width() > 10 and self.zoom_rect.height() > 10:
                    self.zoomed = True
            self.zoom_start = None
            self.zoom_end = None
            self.update()
        elif event.button() == Qt.MouseButton.RightButton:
            self.zoomed = False
            self.zoom_rect = None
            self.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = VZSImageViewer()
    widget.load_file(Path("test-data/BB_GS3.vzs"))
    widget.setWindowTitle("VZS Viewer")
    widget.show()
    sys.exit(app.exec())
