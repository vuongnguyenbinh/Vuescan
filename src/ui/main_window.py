"""
Main Window - Primary application window for FiScanPro.

Integrates scanner panel, preview, pages panel, and all menus/toolbars.
"""

import logging
import os

from src.ui.qt_compat import (
    QSettings, QSize, Qt, QThread, Signal,
    QAction, QKeySequence,
    QApplication, QFileDialog, QHBoxLayout, QMainWindow,
    QMessageBox, QProgressBar, QSplitter, QStatusBar,
    QToolBar, QVBoxLayout, QWidget,
)

from PIL import Image

from src.core.image_processor import ImageProcessor
from src.core.pdf_exporter import PDFExporter, PDFExportSettings
from src.core.scanner_engine import ScannerEngine
from src.i18n.translations import tr
from src.ui.dialogs import (
    BatchScanDialog, PDFExportDialog, ScannerSelectDialog, SettingsDialog,
)
from src.ui.pages_panel import PagesPanel
from src.ui.preview_panel import PreviewPanel
from src.ui.scanner_panel import ScannerPanel
from src.ui.styles import MAIN_STYLESHEET

logger = logging.getLogger(__name__)


class ScanWorker(QThread):
    """Background thread for scanning operations."""

    page_scanned = Signal(object)  # PIL Image
    scan_finished = Signal(int)    # total pages
    scan_error = Signal(str)

    def __init__(self, engine: ScannerEngine, batch: bool = False,
                 max_pages: int = 0):
        super().__init__()
        self._engine = engine
        self._batch = batch
        self._max_pages = max_pages

    def run(self):
        try:
            if self._batch:
                pages = self._engine.scan_batch(
                    max_pages=self._max_pages,
                    callback=lambda n, img: self.page_scanned.emit(img)
                )
                self.scan_finished.emit(len(pages))
            else:
                image = self._engine.scan_page()
                if image:
                    self.page_scanned.emit(image)
                    self.scan_finished.emit(1)
                else:
                    self.scan_error.emit("No image received from scanner")
        except Exception as e:
            self.scan_error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self._engine = ScannerEngine()
        self._exporter = PDFExporter()
        self._processor = ImageProcessor()
        self._scan_worker = None
        self._default_folder = os.path.expanduser("~/Documents")

        self._load_settings()
        self._setup_ui()
        self._create_menus()
        self._create_toolbar()
        self._create_statusbar()
        self._connect_signals()
        self._refresh_scanners()

    def _load_settings(self):
        """Load saved application settings."""
        settings = QSettings("FiScanPro", "FiScanPro")
        lang = settings.value("language", "en")
        tr.language = lang
        self._default_folder = settings.value(
            "default_folder",
            os.path.expanduser("~/Documents")
        )
        self._geometry = settings.value("geometry")
        self._state = settings.value("state")

    def _save_settings(self):
        """Save application settings."""
        settings = QSettings("FiScanPro", "FiScanPro")
        settings.setValue("language", tr.language)
        settings.setValue("default_folder", self._default_folder)
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())

    def _setup_ui(self):
        """Set up the main UI layout."""
        self.setWindowTitle(tr.t("app_title"))
        self.setMinimumSize(1024, 700)
        self.resize(1280, 800)

        if self._geometry:
            self.restoreGeometry(self._geometry)
        if self._state:
            self.restoreState(self._state)

        self.setStyleSheet(MAIN_STYLESHEET)

        # Central widget with splitter layout
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left: Scanner settings panel
        self.scanner_panel = ScannerPanel()
        self.scanner_panel.setFixedWidth(280)
        self.splitter.addWidget(self.scanner_panel)

        # Center: Preview
        self.preview_panel = PreviewPanel()
        self.splitter.addWidget(self.preview_panel)

        # Right: Pages thumbnails
        self.pages_panel = PagesPanel()
        self.pages_panel.setFixedWidth(200)
        self.splitter.addWidget(self.pages_panel)

        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setStretchFactor(2, 0)

        main_layout.addWidget(self.splitter)

    def _create_menus(self):
        """Create application menus."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu(tr.t("menu_file"))

        self.action_new = file_menu.addAction(tr.t("action_new"))
        self.action_new.setShortcut(QKeySequence("Ctrl+N"))
        self.action_new.triggered.connect(self._new_session)

        self.action_open = file_menu.addAction(tr.t("action_open"))
        self.action_open.setShortcut(QKeySequence("Ctrl+O"))
        self.action_open.triggered.connect(self._open_image)

        file_menu.addSeparator()

        self.action_save_pdf = file_menu.addAction(tr.t("action_export_pdf"))
        self.action_save_pdf.setShortcut(QKeySequence("Ctrl+S"))
        self.action_save_pdf.triggered.connect(self._export_pdf)

        self.action_save_tiff = file_menu.addAction(tr.t("action_export_tiff"))
        self.action_save_tiff.triggered.connect(lambda: self._export_image("TIFF"))

        self.action_save_jpeg = file_menu.addAction(tr.t("action_export_jpeg"))
        self.action_save_jpeg.triggered.connect(lambda: self._export_image("JPEG"))

        self.action_save_png = file_menu.addAction(tr.t("action_export_png"))
        self.action_save_png.triggered.connect(lambda: self._export_image("PNG"))

        file_menu.addSeparator()

        self.action_exit = file_menu.addAction(tr.t("action_exit"))
        self.action_exit.setShortcut(QKeySequence("Alt+F4"))
        self.action_exit.triggered.connect(self.close)

        # Scan menu
        scan_menu = menubar.addMenu(tr.t("menu_scan"))

        self.action_scan = scan_menu.addAction(tr.t("action_scan"))
        self.action_scan.setShortcut(QKeySequence("F5"))
        self.action_scan.triggered.connect(self._start_scan)

        self.action_preview_scan = scan_menu.addAction(tr.t("action_scan_preview"))
        self.action_preview_scan.setShortcut(QKeySequence("F6"))
        self.action_preview_scan.triggered.connect(self._preview_scan)

        self.action_batch_scan = scan_menu.addAction(tr.t("action_scan_batch"))
        self.action_batch_scan.setShortcut(QKeySequence("F7"))
        self.action_batch_scan.triggered.connect(self._batch_scan)

        self.action_stop_scan = scan_menu.addAction(tr.t("action_scan_stop"))
        self.action_stop_scan.setShortcut(QKeySequence("Escape"))
        self.action_stop_scan.triggered.connect(self._stop_scan)
        self.action_stop_scan.setEnabled(False)

        scan_menu.addSeparator()

        self.action_select_scanner = scan_menu.addAction(
            tr.t("action_select_scanner")
        )
        self.action_select_scanner.triggered.connect(self._select_scanner_dialog)

        # Edit menu
        edit_menu = menubar.addMenu(tr.t("menu_edit"))

        self.action_rotate_left = edit_menu.addAction(tr.t("action_rotate_left"))
        self.action_rotate_left.setShortcut(QKeySequence("Ctrl+Left"))
        self.action_rotate_left.triggered.connect(self._rotate_left)

        self.action_rotate_right = edit_menu.addAction(tr.t("action_rotate_right"))
        self.action_rotate_right.setShortcut(QKeySequence("Ctrl+Right"))
        self.action_rotate_right.triggered.connect(self._rotate_right)

        self.action_rotate_180 = edit_menu.addAction(tr.t("action_rotate_180"))
        self.action_rotate_180.triggered.connect(self._rotate_180)

        edit_menu.addSeparator()

        self.action_flip_h = edit_menu.addAction(tr.t("action_flip_h"))
        self.action_flip_h.triggered.connect(self._flip_horizontal)

        self.action_flip_v = edit_menu.addAction(tr.t("action_flip_v"))
        self.action_flip_v.triggered.connect(self._flip_vertical)

        edit_menu.addSeparator()

        self.action_deskew = edit_menu.addAction(tr.t("action_deskew"))
        self.action_deskew.setShortcut(QKeySequence("Ctrl+D"))
        self.action_deskew.triggered.connect(self._deskew)

        self.action_auto_enhance = edit_menu.addAction(tr.t("action_auto_enhance"))
        self.action_auto_enhance.setShortcut(QKeySequence("Ctrl+E"))
        self.action_auto_enhance.triggered.connect(self._auto_enhance)

        edit_menu.addSeparator()

        self.action_delete_page = edit_menu.addAction(tr.t("action_delete_page"))
        self.action_delete_page.setShortcut(QKeySequence("Delete"))
        self.action_delete_page.triggered.connect(self._delete_current_page)

        # Settings menu
        settings_menu = menubar.addMenu(tr.t("menu_settings"))

        self.action_settings = settings_menu.addAction(tr.t("settings_general"))
        self.action_settings.setShortcut(QKeySequence("Ctrl+,"))
        self.action_settings.triggered.connect(self._open_settings)

        # Help menu
        help_menu = menubar.addMenu(tr.t("menu_help"))

        self.action_about = help_menu.addAction(tr.t("help_about"))
        self.action_about.triggered.connect(self._show_about)

    def _create_toolbar(self):
        """Create main toolbar with visible text buttons."""
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextOnly
        )
        self.toolbar.setStyleSheet(
            "QToolBar { spacing: 4px; padding: 4px 8px; "
            "background-color: #ffffff; border-bottom: 1px solid #e0e0e0; }"
            "QToolBar QToolButton { color: #1a1a1a; padding: 6px 14px; "
            "border-radius: 4px; border: 1px solid #d0d0d0; "
            "background-color: #f8f8f8; font-size: 12px; min-width: 60px; }"
            "QToolBar QToolButton:hover { background-color: #e8f0fe; "
            "border-color: #0060c0; }"
            "QToolBar QToolButton:pressed { background-color: #d2e3fc; }"
            "QToolBar QToolButton:disabled { color: #aaaaaa; "
            "border-color: #e0e0e0; background-color: #f0f0f0; }"
            "QToolBar::separator { width: 1px; background: #e0e0e0; "
            "margin: 4px 4px; }"
        )
        self.addToolBar(self.toolbar)

        # Scan buttons - styled as primary actions
        self.tb_scan = self.toolbar.addAction(tr.t("toolbar_scan"))
        self.tb_scan.triggered.connect(self._start_scan)

        self.tb_preview = self.toolbar.addAction(tr.t("toolbar_preview"))
        self.tb_preview.triggered.connect(self._preview_scan)

        self.tb_stop = self.toolbar.addAction(tr.t("toolbar_stop"))
        self.tb_stop.triggered.connect(self._stop_scan)
        self.tb_stop.setEnabled(False)

        self.toolbar.addSeparator()

        self.tb_save_pdf = self.toolbar.addAction(tr.t("toolbar_save_pdf"))
        self.tb_save_pdf.triggered.connect(self._export_pdf)

        self.toolbar.addSeparator()

        self.tb_rotate_l = self.toolbar.addAction(tr.t("toolbar_rotate_l"))
        self.tb_rotate_l.triggered.connect(self._rotate_left)

        self.tb_rotate_r = self.toolbar.addAction(tr.t("toolbar_rotate_r"))
        self.tb_rotate_r.triggered.connect(self._rotate_right)

        self.tb_deskew = self.toolbar.addAction(tr.t("toolbar_deskew"))
        self.tb_deskew.triggered.connect(self._deskew)

        self.toolbar.addSeparator()

        self.tb_settings = self.toolbar.addAction(tr.t("toolbar_settings"))
        self.tb_settings.triggered.connect(self._open_settings)

        # Style the Scan button as primary (blue)
        scan_btn = self.toolbar.widgetForAction(self.tb_scan)
        if scan_btn:
            scan_btn.setStyleSheet(
                "QToolButton { background-color: #0060c0; color: white; "
                "border: none; font-weight: bold; border-radius: 4px; "
                "padding: 6px 18px; }"
                "QToolButton:hover { background-color: #004fa0; }"
                "QToolButton:pressed { background-color: #003d80; }"
                "QToolButton:disabled { background-color: #a0a0a0; color: #d0d0d0; }"
            )

    def _create_statusbar(self):
        """Create status bar."""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setVisible(False)
        self.statusbar.addPermanentWidget(self.progress_bar)

        self.statusbar.showMessage(tr.t("status_ready"))

    def _connect_signals(self):
        """Connect panel signals."""
        self.scanner_panel.refresh_requested.connect(self._refresh_scanners)
        self.scanner_panel.scanner_selected.connect(self._on_scanner_selected)

        self.pages_panel.page_selected.connect(self._on_page_selected)
        self.pages_panel.page_delete_requested.connect(self._delete_pages)
        self.pages_panel.page_move_up.connect(
            lambda idx: self.pages_panel.move_page(idx, idx - 1)
        )
        self.pages_panel.page_move_down.connect(
            lambda idx: self.pages_panel.move_page(idx, idx + 1)
        )

    # --- Scanner Operations ---

    def _refresh_scanners(self):
        """Discover and list available scanners."""
        self.statusbar.showMessage(tr.t("status_processing"))
        scanners = self._engine.discover_scanners()
        self.scanner_panel.set_scanners(scanners)

        if scanners:
            self._engine.select_scanner(scanners[0].device_id)
            self.statusbar.showMessage(
                tr.t("status_scanner_connected", name=scanners[0].name)
            )
        else:
            self.statusbar.showMessage(tr.t("status_no_scanner"))

    def _on_scanner_selected(self, device_id: str):
        """Handle scanner selection from panel."""
        self._engine.select_scanner(device_id)
        scanner = self._engine.selected_scanner
        if scanner:
            self.statusbar.showMessage(
                tr.t("status_scanner_connected", name=scanner.name)
            )

    def _select_scanner_dialog(self):
        """Show scanner selection dialog."""
        scanners = self._engine.discover_scanners()
        dialog = ScannerSelectDialog(scanners, self)
        if dialog.exec():
            device_id = dialog.selected_device_id
            if device_id:
                self._engine.select_scanner(device_id)
                self.scanner_panel.set_scanners(scanners)

    def _start_scan(self):
        """Start a single-page scan."""
        if not self._engine.selected_scanner:
            QMessageBox.warning(
                self, tr.t("dialog_warning_title"),
                tr.t("error_no_scanner")
            )
            return

        self._engine.settings = self.scanner_panel.get_settings()
        self._set_scanning_state(True)
        self.statusbar.showMessage(tr.t("status_scanning"))

        self._scan_worker = ScanWorker(self._engine)
        self._scan_worker.page_scanned.connect(self._on_page_scanned)
        self._scan_worker.scan_finished.connect(self._on_scan_finished)
        self._scan_worker.scan_error.connect(self._on_scan_error)
        self._scan_worker.start()

    def _preview_scan(self):
        """Do a low-res preview scan."""
        if not self._engine.selected_scanner:
            QMessageBox.warning(
                self, tr.t("dialog_warning_title"),
                tr.t("error_no_scanner")
            )
            return

        settings = self.scanner_panel.get_settings()
        settings.resolution = 75  # Low res for preview
        self._engine.settings = settings
        self._set_scanning_state(True)
        self.statusbar.showMessage(tr.t("status_scanning"))

        self._scan_worker = ScanWorker(self._engine)
        self._scan_worker.page_scanned.connect(
            lambda img: self.preview_panel.display_image(img)
        )
        self._scan_worker.scan_finished.connect(self._on_scan_finished)
        self._scan_worker.scan_error.connect(self._on_scan_error)
        self._scan_worker.start()

    def _batch_scan(self):
        """Start batch scanning."""
        if not self._engine.selected_scanner:
            QMessageBox.warning(
                self, tr.t("dialog_warning_title"),
                tr.t("error_no_scanner")
            )
            return

        dialog = BatchScanDialog(self)
        if dialog.exec():
            self._engine.settings = self.scanner_panel.get_settings()
            self._set_scanning_state(True)
            self.statusbar.showMessage(tr.t("status_scanning"))
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, dialog.max_pages or 0)

            self._scan_worker = ScanWorker(
                self._engine, batch=True,
                max_pages=dialog.max_pages
            )
            self._scan_worker.page_scanned.connect(self._on_page_scanned)
            self._scan_worker.scan_finished.connect(self._on_scan_finished)
            self._scan_worker.scan_error.connect(self._on_scan_error)
            self._scan_worker.start()

    def _stop_scan(self):
        """Cancel running scan."""
        self._engine.cancel_scan()
        if self._scan_worker and self._scan_worker.isRunning():
            self._scan_worker.quit()
            self._scan_worker.wait(3000)
        self._set_scanning_state(False)
        self.statusbar.showMessage(tr.t("status_ready"))

    def _on_page_scanned(self, image):
        """Handle a newly scanned page."""
        self.pages_panel.add_page(image)
        self.preview_panel.display_image(image)
        page_count = len(self.pages_panel.pages)
        self.progress_bar.setValue(page_count)

    def _on_scan_finished(self, count):
        """Handle scan completion."""
        self._set_scanning_state(False)
        self.progress_bar.setVisible(False)
        self.statusbar.showMessage(
            tr.t("status_scan_complete", count=count)
        )

    def _on_scan_error(self, message):
        """Handle scan error."""
        self._set_scanning_state(False)
        self.progress_bar.setVisible(False)
        self.statusbar.showMessage(tr.t("status_error", message=message))
        QMessageBox.critical(
            self, tr.t("dialog_error_title"),
            tr.t("error_scan_failed", message=message)
        )

    def _set_scanning_state(self, scanning: bool):
        """Enable/disable UI during scanning."""
        self.action_scan.setEnabled(not scanning)
        self.action_preview_scan.setEnabled(not scanning)
        self.action_batch_scan.setEnabled(not scanning)
        self.action_stop_scan.setEnabled(scanning)
        self.tb_scan.setEnabled(not scanning)
        self.tb_preview.setEnabled(not scanning)
        self.tb_stop.setEnabled(scanning)

    # --- Page Operations ---

    def _on_page_selected(self, index: int):
        """Display selected page in preview."""
        pages = self.pages_panel.pages
        if 0 <= index < len(pages):
            self.preview_panel.display_image(pages[index])

    def _delete_pages(self, indices: list[int]):
        """Delete pages after confirmation."""
        result = QMessageBox.question(
            self, tr.t("dialog_confirm_title"),
            tr.t("dialog_confirm_delete", count=len(indices)),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if result == QMessageBox.StandardButton.Yes:
            self.pages_panel.remove_pages(indices)
            if self.pages_panel.pages:
                self.preview_panel.display_image(self.pages_panel.pages[0])
            else:
                self.preview_panel.clear()

    def _delete_current_page(self):
        """Delete the currently selected page."""
        indices = self.pages_panel.selected_indices
        if indices:
            self._delete_pages(indices)

    # --- Image Processing ---

    def _apply_to_current_page(self, operation):
        """Apply an image operation to the currently viewed page."""
        idx = self.pages_panel.selected_indices
        if not idx:
            return
        page_idx = idx[0]
        pages = self.pages_panel.pages
        if 0 <= page_idx < len(pages):
            result = operation(pages[page_idx])
            pages[page_idx] = result
            self.preview_panel.display_image(result)
            self.pages_panel._rebuild_list()
            self.pages_panel.list_widget.setCurrentRow(page_idx)

    def _rotate_left(self):
        self._apply_to_current_page(self._processor.rotate_90_ccw)

    def _rotate_right(self):
        self._apply_to_current_page(self._processor.rotate_90_cw)

    def _rotate_180(self):
        self._apply_to_current_page(self._processor.rotate_180)

    def _flip_horizontal(self):
        self._apply_to_current_page(self._processor.flip_horizontal)

    def _flip_vertical(self):
        self._apply_to_current_page(self._processor.flip_vertical)

    def _deskew(self):
        self.statusbar.showMessage(tr.t("status_processing"))
        self._apply_to_current_page(self._processor.deskew)
        self.statusbar.showMessage(tr.t("status_ready"))

    def _auto_enhance(self):
        self._apply_to_current_page(self._processor.auto_enhance)

    # --- File Operations ---

    def _new_session(self):
        """Start a new scanning session."""
        if self.pages_panel.pages:
            result = QMessageBox.question(
                self, tr.t("dialog_confirm_title"),
                tr.t("dialog_confirm_exit"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if result != QMessageBox.StandardButton.Yes:
                return

        self.pages_panel.clear()
        self.preview_panel.clear()
        self.statusbar.showMessage(tr.t("status_ready"))

    def _open_image(self):
        """Open an image file."""
        path, _ = QFileDialog.getOpenFileName(
            self, tr.t("dialog_open_title"),
            self._default_folder,
            "Image Files (*.jpg *.jpeg *.png *.tiff *.tif *.bmp *.pdf)"
        )
        if path:
            try:
                image = Image.open(path)
                image.load()  # Force load
                self.pages_panel.add_page(image)
                self.preview_panel.display_image(image)
                self.statusbar.showMessage(
                    tr.t("status_saved", path=path)
                )
            except Exception as e:
                QMessageBox.critical(
                    self, tr.t("dialog_error_title"),
                    tr.t("error_open_failed", message=str(e))
                )

    def _export_pdf(self):
        """Export pages to PDF."""
        pages = self.pages_panel.pages
        if not pages:
            QMessageBox.warning(
                self, tr.t("dialog_warning_title"),
                tr.t("error_no_pages")
            )
            return

        dialog = PDFExportDialog(len(pages), self)
        dialog.path_input.setText(
            os.path.join(self._default_folder, "scan.pdf")
        )

        if dialog.exec():
            indices = dialog.get_page_indices()
            selected_pages = [pages[i] for i in indices]

            settings = PDFExportSettings(
                output_path=dialog.output_path,
                title=dialog.title,
                author=dialog.author,
                subject=dialog.subject,
                compress_images=dialog.compress_images,
                jpeg_quality=dialog.jpeg_quality,
            )

            self.statusbar.showMessage(tr.t("status_saving"))
            try:
                path = self._exporter.export_pages(selected_pages, settings)
                self.statusbar.showMessage(
                    tr.t("status_saved", path=path)
                )
                QMessageBox.information(
                    self, tr.t("dialog_info_title"),
                    tr.t("status_saved", path=path)
                )
            except Exception as e:
                QMessageBox.critical(
                    self, tr.t("dialog_error_title"),
                    tr.t("error_save_failed", message=str(e))
                )
                self.statusbar.showMessage(
                    tr.t("status_error", message=str(e))
                )

    def _export_image(self, format_type: str):
        """Export pages to image format."""
        pages = self.pages_panel.pages
        if not pages:
            QMessageBox.warning(
                self, tr.t("dialog_warning_title"),
                tr.t("error_no_pages")
            )
            return

        ext_map = {"JPEG": "*.jpg", "PNG": "*.png", "TIFF": "*.tiff", "BMP": "*.bmp"}
        ext_filter = f"{format_type} Files ({ext_map.get(format_type, '*.*')})"

        path, _ = QFileDialog.getSaveFileName(
            self, tr.t("dialog_save_title"),
            self._default_folder,
            ext_filter
        )
        if path:
            self.statusbar.showMessage(tr.t("status_saving"))
            try:
                saved = self._exporter.export_images_to_format(
                    pages, path, format_type
                )
                self.statusbar.showMessage(
                    tr.t("status_saved", path=saved[0])
                )
            except Exception as e:
                QMessageBox.critical(
                    self, tr.t("dialog_error_title"),
                    tr.t("error_save_failed", message=str(e))
                )

    # --- Settings ---

    def _open_settings(self):
        """Open settings dialog."""
        dialog = SettingsDialog(tr.language, self._default_folder, self)
        if dialog.exec():
            new_lang = dialog.selected_language
            self._default_folder = dialog.default_folder

            if new_lang != tr.language:
                tr.language = new_lang
                self._retranslate_ui()

            self._save_settings()

    def _retranslate_ui(self):
        """Update all UI text after language change."""
        self.setWindowTitle(tr.t("app_title"))

        # Recreate menus and toolbar with new language
        self.menuBar().clear()
        self._create_menus()

        self.removeToolBar(self.toolbar)
        self._create_toolbar()

        self.statusbar.showMessage(tr.t("status_ready"))

        # Update panels
        self.scanner_panel.retranslate()
        self.preview_panel.retranslate()
        self.pages_panel.retranslate()

    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self, tr.t("help_about"),
            tr.t("app_about")
        )

    # --- Window Events ---

    def closeEvent(self, event):
        """Handle window close."""
        if self.pages_panel.pages:
            result = QMessageBox.question(
                self, tr.t("dialog_confirm_title"),
                tr.t("dialog_confirm_exit"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if result != QMessageBox.StandardButton.Yes:
                event.ignore()
                return

        self._save_settings()
        self._engine.close()
        event.accept()
