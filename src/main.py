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

    # Import PyQt6 here to give a clear error if missing
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
    except ImportError:
        print(
            "ERROR: PyQt6 is required.\n"
            "Install with: pip install PyQt6"
        )
        sys.exit(1)

    # High DPI support for Windows 11
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

    app = QApplication(sys.argv)
    app.setApplicationName("FiScanPro")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("FiScanPro")

    # Set application-wide font
    from PyQt6.QtGui import QFont
    font = QFont("Segoe UI", 10)  # Windows 11 default font
    app.setFont(font)

    from src.ui.main_window import MainWindow
    window = MainWindow()
    window.show()

    logger.info("Application window shown")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
