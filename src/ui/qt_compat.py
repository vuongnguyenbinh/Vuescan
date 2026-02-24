"""
Qt Compatibility Layer.

Allows the application to work with either PyQt6 or PySide6.
Import all Qt classes from this module instead of directly from PyQt6/PySide6.
"""

import sys

# Try PyQt6 first, then PySide6
try:
    from PyQt6 import QtCore, QtGui, QtWidgets
    from PyQt6.QtCore import (
        QRectF, QSettings, QSize, Qt, QThread, pyqtSignal as Signal,
    )
    from PyQt6.QtGui import (
        QAction, QFont, QIcon, QImage, QKeySequence, QPixmap, QWheelEvent,
    )
    from PyQt6.QtWidgets import (
        QAbstractItemView, QApplication, QCheckBox, QComboBox, QDialog,
        QDialogButtonBox, QFileDialog, QFormLayout, QFrame, QGraphicsPixmapItem,
        QGraphicsScene, QGraphicsView, QGroupBox, QHBoxLayout, QLabel,
        QLineEdit, QListWidget, QListWidgetItem, QMainWindow, QMessageBox,
        QProgressBar, QPushButton, QRadioButton, QSlider, QSpinBox, QSplitter,
        QStatusBar, QToolBar, QVBoxLayout, QWidget,
    )
    QT_BACKEND = "PyQt6"

except ImportError:
    from PySide6 import QtCore, QtGui, QtWidgets
    from PySide6.QtCore import (
        QRectF, QSettings, QSize, Qt, QThread, Signal,
    )
    from PySide6.QtGui import (
        QAction, QFont, QIcon, QImage, QKeySequence, QPixmap, QWheelEvent,
    )
    from PySide6.QtWidgets import (
        QAbstractItemView, QApplication, QCheckBox, QComboBox, QDialog,
        QDialogButtonBox, QFileDialog, QFormLayout, QFrame, QGraphicsPixmapItem,
        QGraphicsScene, QGraphicsView, QGroupBox, QHBoxLayout, QLabel,
        QLineEdit, QListWidget, QListWidgetItem, QMainWindow, QMessageBox,
        QProgressBar, QPushButton, QRadioButton, QSlider, QSpinBox, QSplitter,
        QStatusBar, QToolBar, QVBoxLayout, QWidget,
    )
    QT_BACKEND = "PySide6"
