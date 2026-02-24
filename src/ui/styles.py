"""Application stylesheet - Windows 11 compatible, works with PySide6/PyQt6."""

MAIN_STYLESHEET = """
/* === Global text color === */
* {
    color: #1a1a1a;
    font-family: "Segoe UI", sans-serif;
}

QMainWindow {
    background-color: #f3f3f3;
}

/* Menu Bar */
QMenuBar {
    background-color: #ffffff;
    color: #1a1a1a;
    border-bottom: 1px solid #e0e0e0;
    padding: 2px 4px;
    font-size: 13px;
}
QMenuBar::item {
    color: #1a1a1a;
    padding: 6px 12px;
    background: transparent;
}
QMenuBar::item:selected {
    background-color: #e8f0fe;
    border-radius: 4px;
}
QMenu {
    background-color: #ffffff;
    color: #1a1a1a;
    border: 1px solid #d0d0d0;
    padding: 4px;
}
QMenu::item {
    color: #1a1a1a;
    padding: 8px 32px 8px 24px;
}
QMenu::item:selected {
    background-color: #e8f0fe;
}
QMenu::item:disabled {
    color: #999999;
}
QMenu::separator {
    height: 1px;
    background-color: #e0e0e0;
    margin: 4px 8px;
}

/* Toolbar */
QToolBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e0e0e0;
    padding: 4px 8px;
    spacing: 2px;
}
QToolBar QToolButton {
    color: #1a1a1a;
    padding: 6px 14px;
    border-radius: 6px;
    border: 1px solid transparent;
    background: transparent;
    font-size: 12px;
    font-weight: 500;
    min-width: 50px;
}
QToolBar QToolButton:hover {
    background-color: #e8f0fe;
    border: 1px solid #c8d8f0;
}
QToolBar QToolButton:pressed {
    background-color: #d2e3fc;
}
QToolBar QToolButton:disabled {
    color: #aaaaaa;
}
QToolBar::separator {
    width: 1px;
    background-color: #e0e0e0;
    margin: 4px 6px;
}

/* Group Box */
QGroupBox {
    color: #0060c0;
    font-weight: bold;
    font-size: 12px;
    border: 1px solid #d8d8d8;
    border-radius: 6px;
    margin-top: 14px;
    padding: 18px 8px 8px 8px;
    background-color: #ffffff;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 6px;
    color: #0060c0;
    background-color: #ffffff;
}

/* Label */
QLabel {
    color: #1a1a1a;
    font-size: 12px;
    background: transparent;
}

/* Buttons */
QPushButton {
    color: #1a1a1a;
    padding: 6px 16px;
    border: 1px solid #cccccc;
    border-radius: 4px;
    background-color: #fbfbfb;
    font-size: 12px;
    min-height: 22px;
}
QPushButton:hover {
    background-color: #e8f0fe;
    border-color: #0060c0;
}
QPushButton:pressed {
    background-color: #d2e3fc;
}
QPushButton:disabled {
    color: #aaaaaa;
    background-color: #f5f5f5;
    border-color: #e0e0e0;
}

/* ComboBox */
QComboBox {
    color: #1a1a1a;
    padding: 5px 28px 5px 10px;
    border: 1px solid #cccccc;
    border-radius: 4px;
    background-color: #ffffff;
    font-size: 12px;
    min-height: 22px;
}
QComboBox:hover {
    border-color: #0060c0;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 24px;
    border-left: 1px solid #e0e0e0;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}
QComboBox::down-arrow {
    width: 10px;
    height: 10px;
}
QComboBox QAbstractItemView {
    color: #1a1a1a;
    background-color: #ffffff;
    border: 1px solid #cccccc;
    selection-background-color: #e8f0fe;
    selection-color: #1a1a1a;
    outline: none;
}
QComboBox QAbstractItemView::item {
    color: #1a1a1a;
    padding: 4px 8px;
    min-height: 24px;
}
QComboBox QAbstractItemView::item:selected {
    background-color: #e8f0fe;
    color: #1a1a1a;
}

/* Slider */
QSlider::groove:horizontal {
    height: 6px;
    background-color: #e0e0e0;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    width: 16px;
    height: 16px;
    margin: -5px 0;
    background-color: #0060c0;
    border-radius: 8px;
}
QSlider::handle:horizontal:hover {
    background-color: #004fa0;
}
QSlider::sub-page:horizontal {
    background-color: #0060c0;
    border-radius: 3px;
}

/* SpinBox */
QSpinBox {
    color: #1a1a1a;
    padding: 4px 8px;
    border: 1px solid #cccccc;
    border-radius: 4px;
    background-color: #ffffff;
    font-size: 12px;
}

/* Line Edit */
QLineEdit {
    color: #1a1a1a;
    padding: 5px 10px;
    border: 1px solid #cccccc;
    border-radius: 4px;
    background-color: #ffffff;
    font-size: 12px;
}
QLineEdit:focus {
    border-color: #0060c0;
    border-width: 2px;
}

/* List Widget (Page Thumbnails) */
QListWidget {
    color: #1a1a1a;
    background-color: #fafafa;
    border: 1px solid #d8d8d8;
    border-radius: 4px;
    padding: 4px;
}
QListWidget::item {
    color: #1a1a1a;
    border-radius: 4px;
    padding: 4px;
}
QListWidget::item:selected {
    background-color: #e8f0fe;
    border: 2px solid #0060c0;
    color: #1a1a1a;
}
QListWidget::item:hover {
    background-color: #f0f4ff;
}

/* Scroll Bars */
QScrollBar:vertical {
    width: 10px;
    background: transparent;
    margin: 0;
}
QScrollBar::handle:vertical {
    background-color: #c0c0c0;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #a0a0a0;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
}
QScrollBar:horizontal {
    height: 10px;
    background: transparent;
}
QScrollBar::handle:horizontal {
    background-color: #c0c0c0;
    border-radius: 5px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #a0a0a0;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: transparent;
}

/* Status Bar */
QStatusBar {
    background-color: #ffffff;
    color: #444444;
    border-top: 1px solid #e0e0e0;
    font-size: 12px;
    padding: 2px 8px;
}
QStatusBar QLabel {
    color: #444444;
}

/* Splitter */
QSplitter::handle {
    background-color: #e0e0e0;
    width: 2px;
}
QSplitter::handle:hover {
    background-color: #0060c0;
}

/* CheckBox */
QCheckBox {
    color: #1a1a1a;
    font-size: 12px;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #999999;
    border-radius: 3px;
    background-color: #ffffff;
}
QCheckBox::indicator:checked {
    background-color: #0060c0;
    border-color: #0060c0;
}

/* Radio Button */
QRadioButton {
    color: #1a1a1a;
    font-size: 12px;
    spacing: 8px;
}
QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #999999;
    border-radius: 9px;
    background-color: #ffffff;
}
QRadioButton::indicator:checked {
    background-color: #0060c0;
    border-color: #0060c0;
}

/* Progress Bar */
QProgressBar {
    color: #1a1a1a;
    border: none;
    background-color: #e0e0e0;
    border-radius: 4px;
    height: 8px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #0060c0;
    border-radius: 4px;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #d8d8d8;
    background-color: #ffffff;
}
QTabBar::tab {
    color: #1a1a1a;
    padding: 8px 16px;
    font-size: 12px;
    background-color: #f0f0f0;
}
QTabBar::tab:selected {
    background-color: #ffffff;
    border-bottom: 2px solid #0060c0;
}
"""
