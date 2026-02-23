"""Application stylesheet - modern flat design for Windows 11."""

MAIN_STYLESHEET = """
QMainWindow {
    background-color: #f5f5f5;
}

/* Menu Bar */
QMenuBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e0e0e0;
    padding: 2px;
    font-size: 13px;
}
QMenuBar::item {
    padding: 6px 12px;
    border-radius: 4px;
}
QMenuBar::item:selected {
    background-color: #e8f0fe;
}
QMenu {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 8px;
    padding: 4px;
}
QMenu::item {
    padding: 8px 32px 8px 24px;
    border-radius: 4px;
}
QMenu::item:selected {
    background-color: #e8f0fe;
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
    padding: 4px;
    spacing: 4px;
}
QToolBar QToolButton {
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    border: none;
    background: transparent;
}
QToolBar QToolButton:hover {
    background-color: #e8f0fe;
}
QToolBar QToolButton:pressed {
    background-color: #d2e3fc;
}

/* Group Box */
QGroupBox {
    font-weight: bold;
    font-size: 12px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 16px;
    background-color: #ffffff;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #333333;
}

/* Buttons */
QPushButton {
    padding: 6px 16px;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    background-color: #ffffff;
    font-size: 12px;
    min-height: 20px;
}
QPushButton:hover {
    background-color: #f0f0f0;
    border-color: #b0b0b0;
}
QPushButton:pressed {
    background-color: #e0e0e0;
}
QPushButton:disabled {
    color: #aaaaaa;
    background-color: #f5f5f5;
}
QPushButton#primaryBtn {
    background-color: #1a73e8;
    color: white;
    border: none;
    font-weight: bold;
}
QPushButton#primaryBtn:hover {
    background-color: #1557b0;
}
QPushButton#primaryBtn:pressed {
    background-color: #104a96;
}

/* ComboBox */
QComboBox {
    padding: 5px 10px;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    background-color: #ffffff;
    font-size: 12px;
    min-height: 22px;
}
QComboBox:hover {
    border-color: #1a73e8;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox QAbstractItemView {
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    background-color: #ffffff;
    selection-background-color: #e8f0fe;
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
    background-color: #1a73e8;
    border-radius: 8px;
}
QSlider::handle:horizontal:hover {
    background-color: #1557b0;
}
QSlider::sub-page:horizontal {
    background-color: #1a73e8;
    border-radius: 3px;
}

/* SpinBox */
QSpinBox {
    padding: 4px 8px;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    background-color: #ffffff;
    font-size: 12px;
}

/* Line Edit */
QLineEdit {
    padding: 5px 10px;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    background-color: #ffffff;
    font-size: 12px;
}
QLineEdit:focus {
    border-color: #1a73e8;
}

/* List Widget (Page Thumbnails) */
QListWidget {
    background-color: #fafafa;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 4px;
}
QListWidget::item {
    border-radius: 6px;
    padding: 4px;
}
QListWidget::item:selected {
    background-color: #e8f0fe;
    border: 2px solid #1a73e8;
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
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
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
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
}

/* Status Bar */
QStatusBar {
    background-color: #ffffff;
    border-top: 1px solid #e0e0e0;
    font-size: 12px;
    color: #555555;
    padding: 2px 8px;
}

/* Splitter */
QSplitter::handle {
    background-color: #e0e0e0;
    width: 2px;
}
QSplitter::handle:hover {
    background-color: #1a73e8;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    background-color: #ffffff;
}
QTabBar::tab {
    padding: 8px 16px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-size: 12px;
}
QTabBar::tab:selected {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-bottom: none;
}
QTabBar::tab:!selected {
    background-color: #f0f0f0;
    margin-top: 2px;
}

/* CheckBox */
QCheckBox {
    font-size: 12px;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #d0d0d0;
    border-radius: 4px;
}
QCheckBox::indicator:checked {
    background-color: #1a73e8;
    border-color: #1a73e8;
}

/* Radio Button */
QRadioButton {
    font-size: 12px;
    spacing: 8px;
}
QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #d0d0d0;
    border-radius: 9px;
}
QRadioButton::indicator:checked {
    background-color: #1a73e8;
    border-color: #1a73e8;
}

/* Progress Bar */
QProgressBar {
    border: none;
    background-color: #e0e0e0;
    border-radius: 4px;
    height: 8px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #1a73e8;
    border-radius: 4px;
}
"""
