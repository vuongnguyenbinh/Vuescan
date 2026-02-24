"""Dialog windows - PDF export, batch scan, settings, scanner selection."""

import os

from src.ui.qt_compat import (
    Qt, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFileDialog,
    QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QMessageBox, QPushButton, QRadioButton,
    QSlider, QSpinBox, QVBoxLayout, QWidget,
)

from src.i18n.translations import tr


class PDFExportDialog(QDialog):
    """Dialog for configuring PDF export settings."""

    def __init__(self, page_count: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr.t("pdf_title"))
        self.setMinimumWidth(450)
        self._page_count = page_count
        self._output_path = ""
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Page selection
        page_group = QGroupBox(tr.t("pdf_pages"))
        page_layout = QVBoxLayout()

        self.all_pages_radio = QRadioButton(
            tr.t("pdf_all_pages") + f" (1-{self._page_count})"
        )
        self.all_pages_radio.setChecked(True)
        page_layout.addWidget(self.all_pages_radio)

        range_layout = QHBoxLayout()
        self.range_radio = QRadioButton(tr.t("pdf_page_range"))
        range_layout.addWidget(self.range_radio)
        self.range_input = QLineEdit()
        self.range_input.setPlaceholderText("1-5, 8, 10-12")
        self.range_input.setEnabled(False)
        self.range_radio.toggled.connect(self.range_input.setEnabled)
        range_layout.addWidget(self.range_input)
        page_layout.addLayout(range_layout)

        page_group.setLayout(page_layout)
        layout.addWidget(page_group)

        # Metadata
        meta_group = QGroupBox("Metadata")
        meta_layout = QFormLayout()

        self.title_input = QLineEdit("Scanned Document")
        meta_layout.addRow(QLabel("Title:"), self.title_input)

        self.author_input = QLineEdit()
        meta_layout.addRow(QLabel(tr.t("pdf_author")), self.author_input)

        self.subject_input = QLineEdit()
        meta_layout.addRow(QLabel(tr.t("pdf_subject")), self.subject_input)

        meta_group.setLayout(meta_layout)
        layout.addWidget(meta_group)

        # Compression
        compress_group = QGroupBox(tr.t("output_compression"))
        compress_layout = QVBoxLayout()

        self.compress_check = QCheckBox(tr.t("pdf_compress"))
        self.compress_check.setChecked(True)
        compress_layout.addWidget(self.compress_check)

        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel(tr.t("pdf_quality_label")))
        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setRange(10, 100)
        self.quality_slider.setValue(85)
        self.quality_label = QLabel("85%")
        self.quality_slider.valueChanged.connect(
            lambda v: self.quality_label.setText(f"{v}%")
        )
        quality_layout.addWidget(self.quality_slider)
        quality_layout.addWidget(self.quality_label)
        compress_layout.addLayout(quality_layout)

        compress_group.setLayout(compress_layout)
        layout.addWidget(compress_group)

        # Output path
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel(tr.t("output_folder")))
        self.path_input = QLineEdit()
        path_layout.addWidget(self.path_input)
        browse_btn = QPushButton(tr.t("output_browse"))
        browse_btn.clicked.connect(self._browse_output)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText(
            tr.t("pdf_export")
        )
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(
            tr.t("dialog_cancel")
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _browse_output(self):
        path, _ = QFileDialog.getSaveFileName(
            self, tr.t("dialog_save_title"),
            os.path.expanduser("~/Documents/scan.pdf"),
            "PDF Files (*.pdf)"
        )
        if path:
            self.path_input.setText(path)

    def _on_accept(self):
        if not self.path_input.text().strip():
            QMessageBox.warning(
                self, tr.t("dialog_warning_title"),
                "Please specify an output file path."
            )
            return
        self._output_path = self.path_input.text().strip()
        if not self._output_path.lower().endswith(".pdf"):
            self._output_path += ".pdf"
        self.accept()

    @property
    def output_path(self) -> str:
        return self._output_path

    @property
    def compress_images(self) -> bool:
        return self.compress_check.isChecked()

    @property
    def jpeg_quality(self) -> int:
        return self.quality_slider.value()

    @property
    def title(self) -> str:
        return self.title_input.text()

    @property
    def author(self) -> str:
        return self.author_input.text()

    @property
    def subject(self) -> str:
        return self.subject_input.text()

    def get_page_indices(self) -> list[int]:
        """Return list of 0-based page indices to export."""
        if self.all_pages_radio.isChecked():
            return list(range(self._page_count))

        text = self.range_input.text().strip()
        if not text:
            return list(range(self._page_count))

        indices = set()
        for part in text.split(","):
            part = part.strip()
            if "-" in part:
                try:
                    start, end = part.split("-", 1)
                    start = int(start.strip()) - 1
                    end = int(end.strip()) - 1
                    for i in range(start, end + 1):
                        if 0 <= i < self._page_count:
                            indices.add(i)
                except ValueError:
                    pass
            else:
                try:
                    idx = int(part) - 1
                    if 0 <= idx < self._page_count:
                        indices.add(idx)
                except ValueError:
                    pass

        return sorted(indices)


class BatchScanDialog(QDialog):
    """Dialog for batch scanning configuration."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr.t("batch_title"))
        self.setMinimumWidth(350)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.unlimited_check = QCheckBox(tr.t("batch_unlimited"))
        self.unlimited_check.setChecked(True)
        self.unlimited_check.toggled.connect(
            lambda checked: self.count_spin.setEnabled(not checked)
        )
        layout.addWidget(self.unlimited_check)

        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 999)
        self.count_spin.setValue(10)
        self.count_spin.setEnabled(False)
        form.addRow(QLabel(tr.t("batch_count")), self.count_spin)

        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(0, 30)
        self.delay_spin.setValue(0)
        form.addRow(QLabel(tr.t("batch_delay")), self.delay_spin)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText(
            tr.t("batch_start")
        )
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(
            tr.t("dialog_cancel")
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    @property
    def max_pages(self) -> int:
        return 0 if self.unlimited_check.isChecked() else self.count_spin.value()

    @property
    def delay_seconds(self) -> int:
        return self.delay_spin.value()


class ScannerSelectDialog(QDialog):
    """Dialog for selecting a scanner device."""

    def __init__(self, scanners: list, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr.t("select_scanner_title"))
        self.setMinimumWidth(400)
        self._scanners = scanners
        self._selected_id = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(tr.t("select_scanner_label")))

        self.scanner_list = QListWidget()
        if not self._scanners:
            self.scanner_list.addItem(tr.t("select_scanner_none"))
            self.scanner_list.setEnabled(False)
        else:
            for scanner in self._scanners:
                label = f"{scanner.name}"
                if scanner.manufacturer:
                    label += f" ({scanner.manufacturer})"
                self.scanner_list.addItem(label)
            self.scanner_list.setCurrentRow(0)

        layout.addWidget(self.scanner_list)

        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton(tr.t("select_scanner_refresh"))
        refresh_btn.clicked.connect(self.reject)  # Parent will refresh
        btn_layout.addWidget(refresh_btn)

        btn_layout.addStretch()

        select_btn = QPushButton(tr.t("select_scanner_select"))
        select_btn.setDefault(True)
        select_btn.clicked.connect(self._on_select)
        select_btn.setEnabled(bool(self._scanners))
        btn_layout.addWidget(select_btn)

        cancel_btn = QPushButton(tr.t("dialog_cancel"))
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

    def _on_select(self):
        row = self.scanner_list.currentRow()
        if 0 <= row < len(self._scanners):
            self._selected_id = self._scanners[row].device_id
            self.accept()

    @property
    def selected_device_id(self) -> str:
        return self._selected_id


class SettingsDialog(QDialog):
    """Application settings dialog."""

    def __init__(self, current_language: str, default_folder: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr.t("settings_general"))
        self.setMinimumWidth(450)
        self._current_language = current_language
        self._default_folder = default_folder
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Language
        lang_group = QGroupBox(tr.t("settings_language"))
        lang_layout = QHBoxLayout()

        self.lang_combo = QComboBox()
        for code, name in tr.available_languages().items():
            self.lang_combo.addItem(name, code)
            if code == self._current_language:
                self.lang_combo.setCurrentIndex(self.lang_combo.count() - 1)

        lang_layout.addWidget(self.lang_combo)
        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)

        # Default folder
        folder_group = QGroupBox(tr.t("settings_default_folder"))
        folder_layout = QHBoxLayout()

        self.folder_input = QLineEdit(self._default_folder)
        folder_layout.addWidget(self.folder_input)

        browse_btn = QPushButton(tr.t("settings_browse"))
        browse_btn.clicked.connect(self._browse_folder)
        folder_layout.addWidget(browse_btn)

        folder_group.setLayout(folder_layout)
        layout.addWidget(folder_group)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, tr.t("dialog_folder_title"),
            self.folder_input.text()
        )
        if folder:
            self.folder_input.setText(folder)

    @property
    def selected_language(self) -> str:
        return self.lang_combo.currentData()

    @property
    def default_folder(self) -> str:
        return self.folder_input.text()
