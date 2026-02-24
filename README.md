# FiScan Pro - Fujitsu Fi-6125 Scanner Tool

A professional document scanning application for **Fujitsu Fi-6125** scanners on Windows 11.
Similar to VueScan 9 but with **free PDF export without watermark**.

## Features

- **Fujitsu Fi-6125 Support**: Full TWAIN/WIA driver integration
- **PDF Export**: Clean PDF output with no watermark
- **Multi-page Scanning**: Scan multiple pages into a single PDF
- **Bilingual UI**: English and Vietnamese (Tiếng Việt) interface
- **Image Processing**: Brightness, contrast, color correction, deskew, crop
- **Multiple Formats**: Export to PDF, TIFF, JPEG, PNG, BMP
- **ADF Support**: Automatic Document Feeder (duplex scanning)
- **Preview**: Real-time scan preview before saving
- **Batch Scanning**: Scan multiple documents in sequence

## Requirements

- Windows 11
- **Python 3.12 or 3.13** (recommended)
- Fujitsu Fi-6125 scanner with TWAIN driver installed

> **Note:** Python 3.14 is too new - PyQt6 does not have pre-built wheels yet.
> If you must use Python 3.14, install PySide6 instead (see below).

## Installation

### Option A: Python 3.12/3.13 (Recommended)
```bash
pip install -r requirements.txt
pip install PyQt6
python -m src.main
```

### Option B: Python 3.14+ (Use PySide6)
```bash
pip install -r requirements.txt
pip install PySide6
python -m src.main
```

### Build Executable
```bash
pip install pyinstaller
python scripts/build.py
```
The executable will be created in `dist/FiScanPro/`.

## Usage

1. Connect your Fujitsu Fi-6125 scanner
2. Install the Fujitsu TWAIN driver from [Fujitsu support](https://www.fujitsu.com/global/support/products/computing/peripheral/scanners/fi/software/fi-6125.html)
3. Launch FiScanPro
4. Select your scanner from the device list
5. Configure scan settings (resolution, color mode, paper size)
6. Click **Scan** to start scanning
7. Export to PDF or image format

## Language / Ngôn ngữ

Switch between English and Vietnamese from **Settings > Language**.

Chuyển đổi giữa Tiếng Anh và Tiếng Việt tại **Cài đặt > Ngôn ngữ**.

## License

MIT License - Free for personal and commercial use.
