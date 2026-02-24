"""Preview panel - central area for displaying scanned images."""

from src.ui.qt_compat import (
    QRectF, Qt, Signal, QImage, QPixmap, QWheelEvent,
    QFrame, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView,
    QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget,
)

from PIL import Image

from src.i18n.translations import tr


class ZoomableGraphicsView(QGraphicsView):
    """Graphics view with zoom support via mouse wheel."""

    zoom_changed = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._zoom_factor = 1.0
        self.setRenderHints(
            self.renderHints()
        )
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setFrameShape(QFrame.Shape.NoFrame)

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def zoom_in(self):
        if self._zoom_factor < 10.0:
            self._zoom_factor *= 1.15
            self.setTransform(
                self.transform().scale(1.15, 1.15)
            )
            self.zoom_changed.emit(self._zoom_factor)

    def zoom_out(self):
        if self._zoom_factor > 0.1:
            self._zoom_factor /= 1.15
            self.setTransform(
                self.transform().scale(1 / 1.15, 1 / 1.15)
            )
            self.zoom_changed.emit(self._zoom_factor)

    def fit_in_view(self):
        if self.scene() and self.scene().items():
            self.fitInView(
                self.scene().itemsBoundingRect(),
                Qt.AspectRatioMode.KeepAspectRatio
            )
            # Compute actual zoom
            transform = self.transform()
            self._zoom_factor = transform.m11()
            self.zoom_changed.emit(self._zoom_factor)

    def fit_width(self):
        if self.scene() and self.scene().items():
            rect = self.scene().itemsBoundingRect()
            view_width = self.viewport().width()
            scale = view_width / rect.width()
            self.resetTransform()
            self.scale(scale, scale)
            self._zoom_factor = scale
            self.zoom_changed.emit(self._zoom_factor)

    def actual_size(self):
        self.resetTransform()
        self._zoom_factor = 1.0
        self.zoom_changed.emit(self._zoom_factor)

    @property
    def zoom_factor(self) -> float:
        return self._zoom_factor


class PreviewPanel(QWidget):
    """Central preview panel for displaying scanned images."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_image = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(4, 4, 4, 4)

        self.zoom_in_btn = QPushButton("+")
        self.zoom_in_btn.setFixedSize(32, 28)
        self.zoom_in_btn.setToolTip(tr.t("preview_zoom_in"))
        self.zoom_in_btn.clicked.connect(lambda: self.view.zoom_in())
        toolbar.addWidget(self.zoom_in_btn)

        self.zoom_out_btn = QPushButton("−")
        self.zoom_out_btn.setFixedSize(32, 28)
        self.zoom_out_btn.setToolTip(tr.t("preview_zoom_out"))
        self.zoom_out_btn.clicked.connect(lambda: self.view.zoom_out())
        toolbar.addWidget(self.zoom_out_btn)

        self.fit_page_btn = QPushButton(tr.t("preview_fit_page"))
        self.fit_page_btn.clicked.connect(lambda: self.view.fit_in_view())
        toolbar.addWidget(self.fit_page_btn)

        self.fit_width_btn = QPushButton(tr.t("preview_fit_width"))
        self.fit_width_btn.clicked.connect(lambda: self.view.fit_width())
        toolbar.addWidget(self.fit_width_btn)

        self.actual_btn = QPushButton("100%")
        self.actual_btn.setToolTip(tr.t("preview_actual_size"))
        self.actual_btn.clicked.connect(lambda: self.view.actual_size())
        toolbar.addWidget(self.actual_btn)

        toolbar.addStretch()

        self.zoom_label = QLabel("100%")
        toolbar.addWidget(self.zoom_label)

        layout.addLayout(toolbar)

        # Graphics View
        self.scene = QGraphicsScene()
        self.view = ZoomableGraphicsView(self.scene)
        self.view.zoom_changed.connect(self._on_zoom_changed)
        self.view.setStyleSheet("background-color: #e0e0e0;")
        layout.addWidget(self.view)

        # Placeholder label
        self.placeholder_label = QLabel(tr.t("preview_no_image"))
        self.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder_label.setStyleSheet(
            "color: #888; font-size: 14px; padding: 40px;"
        )

        self._pixmap_item = None
        self._show_placeholder(True)

    def _on_zoom_changed(self, factor: float):
        self.zoom_label.setText(f"{int(factor * 100)}%")

    def _show_placeholder(self, show: bool):
        if show:
            self.view.hide()
            self.layout().addWidget(self.placeholder_label)
            self.placeholder_label.show()
        else:
            self.placeholder_label.hide()
            self.view.show()

    def display_image(self, image: Image.Image):
        """Display a PIL Image in the preview."""
        self._current_image = image
        self._show_placeholder(False)

        # Convert PIL Image to QPixmap
        if image.mode == "1":
            img = image.convert("L")
        elif image.mode == "RGBA":
            img = image
        elif image.mode == "L":
            img = image
        else:
            img = image.convert("RGB")

        if img.mode == "L":
            qimage = QImage(
                img.tobytes(), img.width, img.height,
                img.width, QImage.Format.Format_Grayscale8
            )
        elif img.mode == "RGBA":
            qimage = QImage(
                img.tobytes(), img.width, img.height,
                img.width * 4, QImage.Format.Format_RGBA8888
            )
        else:
            qimage = QImage(
                img.tobytes(), img.width, img.height,
                img.width * 3, QImage.Format.Format_RGB888
            )

        pixmap = QPixmap.fromImage(qimage)

        self.scene.clear()
        self._pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self._pixmap_item)
        self.scene.setSceneRect(QRectF(pixmap.rect()))

        self.view.fit_in_view()

    def clear(self):
        """Clear the preview."""
        self.scene.clear()
        self._pixmap_item = None
        self._current_image = None
        self._show_placeholder(True)

    @property
    def current_image(self) -> Image.Image:
        return self._current_image

    def retranslate(self):
        self.zoom_in_btn.setToolTip(tr.t("preview_zoom_in"))
        self.zoom_out_btn.setToolTip(tr.t("preview_zoom_out"))
        self.fit_page_btn.setText(tr.t("preview_fit_page"))
        self.fit_width_btn.setText(tr.t("preview_fit_width"))
        self.actual_btn.setToolTip(tr.t("preview_actual_size"))
        self.placeholder_label.setText(tr.t("preview_no_image"))
