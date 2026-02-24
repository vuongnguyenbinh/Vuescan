"""Scanner settings panel - left sidebar for scanner configuration."""

from src.ui.qt_compat import (
    Qt, Signal, QComboBox, QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QSlider, QSpinBox, QVBoxLayout, QWidget,
)

from src.core.scanner_engine import ColorMode, PaperSize, ScanSettings, ScanSource
from src.i18n.translations import tr


class ScannerPanel(QWidget):
    """Panel for configuring scanner settings."""

    settings_changed = Signal()
    refresh_requested = Signal()
    scanner_selected = Signal(str)  # device_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        # Device selection
        device_group = QGroupBox(tr.t("panel_scanner"))
        device_layout = QVBoxLayout()

        device_layout.addWidget(QLabel(tr.t("scanner_device")))
        self.device_combo = QComboBox()
        self.device_combo.currentIndexChanged.connect(self._on_device_changed)
        device_layout.addWidget(self.device_combo)

        self.refresh_btn = QPushButton(tr.t("scanner_refresh"))
        self.refresh_btn.clicked.connect(self.refresh_requested.emit)
        device_layout.addWidget(self.refresh_btn)

        device_group.setLayout(device_layout)
        layout.addWidget(device_group)

        # Source selection
        source_group = QGroupBox(tr.t("scanner_source"))
        source_layout = QVBoxLayout()

        self.source_combo = QComboBox()
        self._populate_sources()
        self.source_combo.currentIndexChanged.connect(
            lambda: self.settings_changed.emit()
        )
        source_layout.addWidget(self.source_combo)

        source_group.setLayout(source_layout)
        layout.addWidget(source_group)

        # Color mode
        mode_group = QGroupBox(tr.t("scanner_mode"))
        mode_layout = QVBoxLayout()

        self.mode_combo = QComboBox()
        self._populate_modes()
        self.mode_combo.currentIndexChanged.connect(
            lambda: self.settings_changed.emit()
        )
        mode_layout.addWidget(self.mode_combo)

        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # Resolution
        res_group = QGroupBox(tr.t("scanner_resolution"))
        res_layout = QVBoxLayout()

        self.resolution_combo = QComboBox()
        for dpi in [75, 100, 150, 200, 300, 400, 600]:
            self.resolution_combo.addItem(f"{dpi} DPI", dpi)
        self.resolution_combo.setCurrentIndex(4)  # 300 DPI default
        self.resolution_combo.currentIndexChanged.connect(
            lambda: self.settings_changed.emit()
        )
        res_layout.addWidget(self.resolution_combo)

        res_group.setLayout(res_layout)
        layout.addWidget(res_group)

        # Paper size
        paper_group = QGroupBox(tr.t("scanner_paper_size"))
        paper_layout = QVBoxLayout()

        self.paper_combo = QComboBox()
        self._populate_paper_sizes()
        self.paper_combo.currentIndexChanged.connect(
            lambda: self.settings_changed.emit()
        )
        paper_layout.addWidget(self.paper_combo)

        paper_group.setLayout(paper_layout)
        layout.addWidget(paper_group)

        # Brightness
        brightness_group = QGroupBox(tr.t("scanner_brightness"))
        brightness_layout = QHBoxLayout()

        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.setValue(0)
        self.brightness_label = QLabel("0")
        self.brightness_slider.valueChanged.connect(
            lambda v: self.brightness_label.setText(str(v))
        )
        self.brightness_slider.valueChanged.connect(
            lambda: self.settings_changed.emit()
        )
        brightness_layout.addWidget(self.brightness_slider)
        brightness_layout.addWidget(self.brightness_label)

        brightness_group.setLayout(brightness_layout)
        layout.addWidget(brightness_group)

        # Contrast
        contrast_group = QGroupBox(tr.t("scanner_contrast"))
        contrast_layout = QHBoxLayout()

        self.contrast_slider = QSlider(Qt.Orientation.Horizontal)
        self.contrast_slider.setRange(-100, 100)
        self.contrast_slider.setValue(0)
        self.contrast_label = QLabel("0")
        self.contrast_slider.valueChanged.connect(
            lambda v: self.contrast_label.setText(str(v))
        )
        self.contrast_slider.valueChanged.connect(
            lambda: self.settings_changed.emit()
        )
        contrast_layout.addWidget(self.contrast_slider)
        contrast_layout.addWidget(self.contrast_label)

        contrast_group.setLayout(contrast_layout)
        layout.addWidget(contrast_group)

        layout.addStretch()

    def _populate_sources(self):
        self.source_combo.clear()
        sources = [
            (tr.t("scanner_source_flatbed"), ScanSource.FLATBED),
            (tr.t("scanner_source_adf_front"), ScanSource.ADF_FRONT),
            (tr.t("scanner_source_adf_back"), ScanSource.ADF_BACK),
            (tr.t("scanner_source_adf_duplex"), ScanSource.ADF_DUPLEX),
        ]
        for label, source in sources:
            self.source_combo.addItem(label, source)
        self.source_combo.setCurrentIndex(1)  # ADF Front default

    def _populate_modes(self):
        self.mode_combo.clear()
        modes = [
            (tr.t("scanner_mode_color"), ColorMode.COLOR),
            (tr.t("scanner_mode_gray"), ColorMode.GRAYSCALE),
            (tr.t("scanner_mode_bw"), ColorMode.BW),
        ]
        for label, mode in modes:
            self.mode_combo.addItem(label, mode)

    def _populate_paper_sizes(self):
        self.paper_combo.clear()
        sizes = [
            (tr.t("paper_auto"), PaperSize.AUTO),
            (tr.t("paper_a4"), PaperSize.A4),
            (tr.t("paper_a3"), PaperSize.A3),
            (tr.t("paper_a5"), PaperSize.A5),
            (tr.t("paper_a6"), PaperSize.A6),
            (tr.t("paper_letter"), PaperSize.LETTER),
            (tr.t("paper_legal"), PaperSize.LEGAL),
        ]
        for label, size in sizes:
            self.paper_combo.addItem(label, size)
        self.paper_combo.setCurrentIndex(1)  # A4 default

    def _on_device_changed(self, index):
        if index >= 0:
            device_id = self.device_combo.itemData(index)
            if device_id:
                self.scanner_selected.emit(device_id)

    def set_scanners(self, scanners):
        """Update the scanner device list."""
        self.device_combo.clear()
        if not scanners:
            self.device_combo.addItem(tr.t("scanner_no_device"), None)
        else:
            for scanner in scanners:
                self.device_combo.addItem(scanner.name, scanner.device_id)

    def get_settings(self) -> ScanSettings:
        """Get current scan settings from the panel."""
        return ScanSettings(
            source=self.source_combo.currentData() or ScanSource.ADF_FRONT,
            color_mode=self.mode_combo.currentData() or ColorMode.COLOR,
            resolution=self.resolution_combo.currentData() or 300,
            paper_size=self.paper_combo.currentData() or PaperSize.A4,
            brightness=self.brightness_slider.value(),
            contrast=self.contrast_slider.value(),
            duplex=(self.source_combo.currentData() == ScanSource.ADF_DUPLEX),
        )

    def retranslate(self):
        """Update all text when language changes."""
        self._populate_sources()
        self._populate_modes()
        self._populate_paper_sizes()
        self.refresh_btn.setText(tr.t("scanner_refresh"))
