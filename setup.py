from setuptools import setup, find_packages

setup(
    name="FiScanPro",
    version="1.0.0",
    description="Professional document scanning tool for Fujitsu Fi-6125",
    author="FiScanPro Team",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "PyQt6>=6.6.0",
        "Pillow>=10.0.0",
        "img2pdf>=0.5.1",
        "pikepdf>=8.0.0",
        "numpy>=1.24.0",
        "reportlab>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "fiscanpro=src.main:main",
        ],
    },
)
