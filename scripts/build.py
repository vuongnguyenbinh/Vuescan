"""
Build script - Create standalone Windows executable using PyInstaller.

Usage:
    python scripts/build.py

Output:
    dist/FiScanPro/FiScanPro.exe
"""

import os
import subprocess
import sys


def build():
    """Build FiScanPro as a standalone Windows executable."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)

    print("=" * 60)
    print("  FiScanPro Build Script")
    print("  Building standalone Windows executable...")
    print("=" * 60)

    # Ensure PyInstaller is available
    try:
        import PyInstaller
        print(f"  PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("  Installing PyInstaller...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "pyinstaller"
        ])

    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=FiScanPro",
        "--windowed",           # No console window
        "--onedir",             # Create directory bundle
        "--noconfirm",          # Overwrite without asking
        "--clean",              # Clean build cache

        # Hidden imports needed at runtime
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageEnhance",
        "--hidden-import=PIL.ImageFilter",
        "--hidden-import=PIL.ImageOps",
        "--hidden-import=PIL.ImageDraw",
        "--hidden-import=numpy",
        "--hidden-import=img2pdf",
        "--hidden-import=pikepdf",
        "--hidden-import=reportlab",
        "--hidden-import=reportlab.pdfgen.canvas",
        "--hidden-import=reportlab.lib.pagesizes",

        # Collect all submodules
        "--collect-submodules=PIL",
        "--collect-submodules=reportlab",

        # Add source data
        f"--add-data=src/i18n{os.pathsep}src/i18n",
        f"--add-data=src/resources{os.pathsep}src/resources",

        # Entry point
        "src/main.py",
    ]

    # Add icon if it exists
    icon_path = os.path.join("src", "resources", "icons", "app.ico")
    if os.path.exists(icon_path):
        cmd.insert(-1, f"--icon={icon_path}")

    print(f"\n  Running PyInstaller...")
    print(f"  Command: {' '.join(cmd[:5])}...")

    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        exe_path = os.path.join("dist", "FiScanPro", "FiScanPro.exe")
        print("\n" + "=" * 60)
        print("  BUILD SUCCESSFUL!")
        print(f"  Output: {os.path.abspath(exe_path)}")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("  BUILD FAILED!")
        print(f"  Exit code: {result.returncode}")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    build()
