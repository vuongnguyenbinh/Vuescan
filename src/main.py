"""
FiScanPro - Main Entry Point.

Professional document scanning application for Fujitsu Fi-6125.
"""

import logging
import os
import sys


def setup_logging():
    """Configure application logging."""
    log_dir = os.path.join(os.path.expanduser("~"), ".fiscanpro")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "fiscanpro.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main():
    """Launch FiScanPro application."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting FiScanPro v1.0.0")

    # Check Python version
    py_ver = sys.version_info
    if py_ver >= (3, 14):
        logger.warning(
            f"Python {py_ver.major}.{py_ver.minor} detected. "
            "PyQt6 may not have pre-built wheels for this version. "
            "Recommended: Python 3.12 or 3.13."
        )

    # Import Qt - try PyQt6 first, fallback to PySide6
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QFont
    except ImportError:
        try:
            from PySide6.QtWidgets import QApplication
            from PySide6.QtGui import QFont
            logger.info("Using PySide6 as UI backend (PyQt6 not available)")
        except ImportError:
            print(
                "ERROR: No Qt UI library found.\n\n"
                "Please install one of the following:\n"
                "  pip install PyQt6          (recommended for Python 3.12/3.13)\n"
                "  pip install PySide6        (alternative, wider Python support)\n\n"
                "NOTE: If you are using Python 3.14+, PyQt6 may not be available yet.\n"
                "      Try: pip install PySide6\n"
                "      Or use Python 3.12/3.13 instead."
            )
            sys.exit(1)

    # High DPI support for Windows 11
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

    app = QApplication(sys.argv)
    app.setApplicationName("FiScanPro")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("FiScanPro")

    # Set application-wide font
    font = QFont("Segoe UI", 10)  # Windows 11 default font
    app.setFont(font)

    from src.ui.main_window import MainWindow
    window = MainWindow()
    window.show()

    logger.info("Application window shown")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
