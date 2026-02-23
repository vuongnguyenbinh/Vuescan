"""Pages panel - thumbnail list of scanned pages on the right side."""

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QImage, QPixmap
from PyQt6.QtWidgets import (
    QAbstractItemView, QGroupBox, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget,
)

from PIL import Image

from src.i18n.translations import tr

THUMBNAIL_SIZE = 140


class PagesPanel(QWidget):
    """Panel showing thumbnails of all scanned pages."""

    page_selected = pyqtSignal(int)  # page index
    page_delete_requested = pyqtSignal(list)  # list of indices
    page_move_up = pyqtSignal(int)
    page_move_down = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pages: list[Image.Image] = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        # Header
        header_group = QGroupBox(tr.t("panel_pages"))
        header_layout = QVBoxLayout()

        self.count_label = QLabel(tr.t("pages_count", count=0))
        header_layout.addWidget(self.count_label)

        # Thumbnail list
        self.list_widget = QListWidget()
        self.list_widget.setIconSize(QSize(THUMBNAIL_SIZE, THUMBNAIL_SIZE))
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_widget.setFlow(QListWidget.Flow.TopToBottom)
        self.list_widget.setWrapping(False)
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.list_widget.setSpacing(6)
        self.list_widget.setMinimumWidth(THUMBNAIL_SIZE + 40)
        self.list_widget.currentRowChanged.connect(self._on_row_changed)
        header_layout.addWidget(self.list_widget)

        # Buttons
        btn_layout = QHBoxLayout()

        self.move_up_btn = QPushButton("↑")
        self.move_up_btn.setToolTip(tr.t("pages_move_up"))
        self.move_up_btn.setFixedWidth(36)
        self.move_up_btn.clicked.connect(self._on_move_up)
        btn_layout.addWidget(self.move_up_btn)

        self.move_down_btn = QPushButton("↓")
        self.move_down_btn.setToolTip(tr.t("pages_move_down"))
        self.move_down_btn.setFixedWidth(36)
        self.move_down_btn.clicked.connect(self._on_move_down)
        btn_layout.addWidget(self.move_down_btn)

        btn_layout.addStretch()

        self.delete_btn = QPushButton("✕")
        self.delete_btn.setToolTip(tr.t("pages_delete_selected"))
        self.delete_btn.setFixedWidth(36)
        self.delete_btn.clicked.connect(self._on_delete)
        btn_layout.addWidget(self.delete_btn)

        header_layout.addLayout(btn_layout)
        header_group.setLayout(header_layout)
        layout.addWidget(header_group)

    def _on_row_changed(self, row):
        if row >= 0:
            self.page_selected.emit(row)

    def _on_move_up(self):
        row = self.list_widget.currentRow()
        if row > 0:
            self.page_move_up.emit(row)

    def _on_move_down(self):
        row = self.list_widget.currentRow()
        if row >= 0 and row < self.list_widget.count() - 1:
            self.page_move_down.emit(row)

    def _on_delete(self):
        indices = [
            self.list_widget.row(item)
            for item in self.list_widget.selectedItems()
        ]
        if indices:
            self.page_delete_requested.emit(sorted(indices, reverse=True))

    def add_page(self, image: Image.Image):
        """Add a page thumbnail."""
        self._pages.append(image)
        self._add_thumbnail(image, len(self._pages))
        self._update_count()

    def _add_thumbnail(self, image: Image.Image, page_num: int):
        """Create and add a thumbnail item."""
        # Create thumbnail
        thumb = image.copy()
        thumb.thumbnail((THUMBNAIL_SIZE, THUMBNAIL_SIZE), Image.LANCZOS)

        # Convert to QPixmap
        if thumb.mode == "1":
            thumb = thumb.convert("L")
        if thumb.mode == "L":
            qimage = QImage(
                thumb.tobytes(), thumb.width, thumb.height,
                thumb.width, QImage.Format.Format_Grayscale8
            )
        elif thumb.mode == "RGBA":
            qimage = QImage(
                thumb.tobytes(), thumb.width, thumb.height,
                thumb.width * 4, QImage.Format.Format_RGBA8888
            )
        else:
            thumb = thumb.convert("RGB")
            qimage = QImage(
                thumb.tobytes(), thumb.width, thumb.height,
                thumb.width * 3, QImage.Format.Format_RGB888
            )

        pixmap = QPixmap.fromImage(qimage)
        icon = QIcon(pixmap)

        item = QListWidgetItem(icon, f"  {page_num}")
        item.setSizeHint(QSize(THUMBNAIL_SIZE + 20, THUMBNAIL_SIZE + 30))
        self.list_widget.addItem(item)

    def remove_pages(self, indices: list[int]):
        """Remove pages by indices (should be sorted descending)."""
        for idx in indices:
            if 0 <= idx < len(self._pages):
                self._pages.pop(idx)
                self.list_widget.takeItem(idx)
        self._renumber()
        self._update_count()

    def move_page(self, from_idx: int, to_idx: int):
        """Move a page from one position to another."""
        if (0 <= from_idx < len(self._pages) and
                0 <= to_idx < len(self._pages)):
            page = self._pages.pop(from_idx)
            self._pages.insert(to_idx, page)
            self._rebuild_list()
            self.list_widget.setCurrentRow(to_idx)

    def _rebuild_list(self):
        self.list_widget.clear()
        for i, page in enumerate(self._pages):
            self._add_thumbnail(page, i + 1)

    def _renumber(self):
        for i in range(self.list_widget.count()):
            self.list_widget.item(i).setText(f"  {i + 1}")

    def _update_count(self):
        self.count_label.setText(
            tr.t("pages_count", count=len(self._pages))
        )

    def clear(self):
        """Remove all pages."""
        self._pages.clear()
        self.list_widget.clear()
        self._update_count()

    @property
    def pages(self) -> list[Image.Image]:
        return self._pages

    @property
    def selected_indices(self) -> list[int]:
        return [
            self.list_widget.row(item)
            for item in self.list_widget.selectedItems()
        ]

    def retranslate(self):
        self.count_label.setText(
            tr.t("pages_count", count=len(self._pages))
        )
        self.move_up_btn.setToolTip(tr.t("pages_move_up"))
        self.move_down_btn.setToolTip(tr.t("pages_move_down"))
        self.delete_btn.setToolTip(tr.t("pages_delete_selected"))
