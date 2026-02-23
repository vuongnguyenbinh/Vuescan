"""
Scanner Engine - TWAIN and WIA interface for Fujitsu Fi-6125.

Provides a unified API for communicating with document scanners
through Windows TWAIN and WIA (Windows Image Acquisition) drivers.
"""

import logging
import os
import platform
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from PIL import Image

logger = logging.getLogger(__name__)


class ScanSource(Enum):
    FLATBED = "flatbed"
    ADF_FRONT = "adf_front"
    ADF_BACK = "adf_back"
    ADF_DUPLEX = "adf_duplex"


class ColorMode(Enum):
    COLOR = "color"
    GRAYSCALE = "grayscale"
    BW = "bw"


class PaperSize(Enum):
    AUTO = "auto"
    A3 = "a3"
    A4 = "a4"
    A5 = "a5"
    A6 = "a6"
    LETTER = "letter"
    LEGAL = "legal"
    CUSTOM = "custom"


# Paper dimensions in inches (width, height)
PAPER_DIMENSIONS = {
    PaperSize.A3: (11.69, 16.54),
    PaperSize.A4: (8.27, 11.69),
    PaperSize.A5: (5.83, 8.27),
    PaperSize.A6: (4.13, 5.83),
    PaperSize.LETTER: (8.5, 11.0),
    PaperSize.LEGAL: (8.5, 14.0),
}


@dataclass
class ScanSettings:
    """Configuration for a scan operation."""
    source: ScanSource = ScanSource.ADF_FRONT
    color_mode: ColorMode = ColorMode.COLOR
    resolution: int = 300
    paper_size: PaperSize = PaperSize.A4
    brightness: int = 0       # -100 to 100
    contrast: int = 0         # -100 to 100
    threshold: int = 128      # 0-255, for B&W mode
    custom_width: float = 8.27   # inches
    custom_height: float = 11.69  # inches
    duplex: bool = False
    auto_deskew: bool = True
    blank_page_removal: bool = False


@dataclass
class ScannerInfo:
    """Information about a detected scanner."""
    name: str
    device_id: str
    manufacturer: str = ""
    model: str = ""
    driver_type: str = "twain"  # "twain" or "wia"
    has_adf: bool = False
    has_duplex: bool = False
    has_flatbed: bool = False
    max_resolution: int = 600
    supported_modes: list = field(default_factory=lambda: [
        ColorMode.COLOR, ColorMode.GRAYSCALE, ColorMode.BW
    ])


class ScannerEngine:
    """
    Unified scanner interface supporting TWAIN and WIA on Windows.

    On non-Windows systems, provides a simulation mode for development.
    """

    def __init__(self):
        self._scanners: list[ScannerInfo] = []
        self._selected_scanner: Optional[ScannerInfo] = None
        self._settings = ScanSettings()
        self._is_scanning = False
        self._cancel_requested = False
        self._twain_manager = None
        self._twain_source = None
        self._lock = threading.Lock()

        self._is_windows = platform.system() == "Windows"

        if self._is_windows:
            self._init_twain()

    def _init_twain(self):
        """Initialize TWAIN Data Source Manager on Windows."""
        try:
            import twain
            self._twain_manager = twain.SourceManager(0)
            logger.info("TWAIN DSM initialized successfully")
        except ImportError:
            logger.warning(
                "pytwain not installed. Install with: pip install pytwain"
            )
        except Exception as e:
            logger.warning(f"Failed to initialize TWAIN: {e}")

    def discover_scanners(self) -> list[ScannerInfo]:
        """Detect all available scanners on the system."""
        self._scanners.clear()

        if self._is_windows:
            self._discover_twain_scanners()
            self._discover_wia_scanners()
        else:
            self._add_simulation_scanner()

        logger.info(f"Discovered {len(self._scanners)} scanner(s)")
        return self._scanners

    def _discover_twain_scanners(self):
        """Discover scanners via TWAIN driver."""
        if not self._twain_manager:
            return
        try:
            import twain
            sources = self._twain_manager.GetSourceList()
            for source_name in sources:
                is_fi6125 = "fi-6125" in source_name.lower() or "6125" in source_name
                scanner = ScannerInfo(
                    name=source_name,
                    device_id=f"twain:{source_name}",
                    manufacturer="Fujitsu" if "fujitsu" in source_name.lower() else "",
                    model="fi-6125" if is_fi6125 else source_name,
                    driver_type="twain",
                    has_adf=True,
                    has_duplex=is_fi6125,
                    has_flatbed=True,
                    max_resolution=600,
                )
                self._scanners.append(scanner)
        except Exception as e:
            logger.error(f"TWAIN discovery failed: {e}")

    def _discover_wia_scanners(self):
        """Discover scanners via WIA (Windows Image Acquisition)."""
        try:
            import comtypes.client
            wia_manager = comtypes.client.CreateObject("WIA.DeviceManager")
            for i in range(1, wia_manager.DeviceInfos.Count + 1):
                device_info = wia_manager.DeviceInfos.Item(i)
                if device_info.Type == 1:  # Scanner device
                    name = device_info.Properties("Name").Value
                    device_id = device_info.DeviceID
                    already_found = any(
                        s.name.lower() == name.lower() for s in self._scanners
                    )
                    if not already_found:
                        is_fi6125 = "fi-6125" in name.lower() or "6125" in name
                        scanner = ScannerInfo(
                            name=name,
                            device_id=f"wia:{device_id}",
                            manufacturer="Fujitsu" if "fujitsu" in name.lower() else "",
                            model="fi-6125" if is_fi6125 else name,
                            driver_type="wia",
                            has_adf=True,
                            has_duplex=is_fi6125,
                            has_flatbed=True,
                            max_resolution=600,
                        )
                        self._scanners.append(scanner)
        except ImportError:
            logger.debug("comtypes not available for WIA")
        except Exception as e:
            logger.debug(f"WIA discovery failed: {e}")

    def _add_simulation_scanner(self):
        """Add simulated scanner for development/testing on non-Windows."""
        sim_scanner = ScannerInfo(
            name="Fujitsu fi-6125 (Simulated)",
            device_id="sim:fi-6125",
            manufacturer="Fujitsu",
            model="fi-6125",
            driver_type="simulation",
            has_adf=True,
            has_duplex=True,
            has_flatbed=True,
            max_resolution=600,
        )
        self._scanners.append(sim_scanner)

    @property
    def scanners(self) -> list[ScannerInfo]:
        return self._scanners

    @property
    def selected_scanner(self) -> Optional[ScannerInfo]:
        return self._selected_scanner

    @property
    def settings(self) -> ScanSettings:
        return self._settings

    @settings.setter
    def settings(self, value: ScanSettings):
        self._settings = value

    @property
    def is_scanning(self) -> bool:
        return self._is_scanning

    def select_scanner(self, device_id: str) -> bool:
        """Select a scanner by its device ID."""
        for scanner in self._scanners:
            if scanner.device_id == device_id:
                self._selected_scanner = scanner
                logger.info(f"Selected scanner: {scanner.name}")
                return True
        logger.warning(f"Scanner not found: {device_id}")
        return False

    def scan_page(self) -> Optional[Image.Image]:
        """Scan a single page and return as PIL Image."""
        if not self._selected_scanner:
            raise RuntimeError("No scanner selected")

        if self._is_scanning:
            raise RuntimeError("Scanner is busy")

        with self._lock:
            self._is_scanning = True
            self._cancel_requested = False

        try:
            driver_type = self._selected_scanner.driver_type
            if driver_type == "twain":
                return self._scan_twain()
            elif driver_type == "wia":
                return self._scan_wia()
            else:
                return self._scan_simulation()
        finally:
            with self._lock:
                self._is_scanning = False

    def _scan_twain(self) -> Optional[Image.Image]:
        """Perform scan via TWAIN driver."""
        try:
            import twain

            source_name = self._selected_scanner.name
            source = self._twain_manager.OpenSource(source_name)

            # Configure source settings
            self._configure_twain_source(source)

            # Acquire image
            source.RequestAcquire(0, 0)  # ShowUI=False, Modal=False
            rv = source.XferImageNatively()
            if rv:
                handle, count = rv
                bmp_data = twain.DIBToBMFile(handle)
                import io
                image = Image.open(io.BytesIO(bmp_data))
                source.close()
                return image.copy()
            source.close()
            return None
        except Exception as e:
            logger.error(f"TWAIN scan error: {e}")
            raise RuntimeError(f"TWAIN scan failed: {e}")

    def _configure_twain_source(self, source):
        """Apply scan settings to TWAIN source."""
        import twain

        s = self._settings

        # Color mode
        pixel_type_map = {
            ColorMode.COLOR: twain.TWPT_RGB,
            ColorMode.GRAYSCALE: twain.TWPT_GRAY,
            ColorMode.BW: twain.TWPT_BW,
        }
        try:
            source.SetCapability(
                twain.ICAP_PIXELTYPE, twain.TWTY_UINT16,
                pixel_type_map.get(s.color_mode, twain.TWPT_RGB)
            )
        except Exception:
            pass

        # Resolution
        try:
            source.SetCapability(
                twain.ICAP_XRESOLUTION, twain.TWTY_FIX32, float(s.resolution)
            )
            source.SetCapability(
                twain.ICAP_YRESOLUTION, twain.TWTY_FIX32, float(s.resolution)
            )
        except Exception:
            pass

        # Brightness
        if s.brightness != 0:
            try:
                source.SetCapability(
                    twain.ICAP_BRIGHTNESS, twain.TWTY_FIX32,
                    float(s.brightness)
                )
            except Exception:
                pass

        # Contrast
        if s.contrast != 0:
            try:
                source.SetCapability(
                    twain.ICAP_CONTRAST, twain.TWTY_FIX32,
                    float(s.contrast)
                )
            except Exception:
                pass

        # Paper size / scan area
        if s.paper_size != PaperSize.AUTO:
            dims = PAPER_DIMENSIONS.get(s.paper_size)
            if dims is None and s.paper_size == PaperSize.CUSTOM:
                dims = (s.custom_width, s.custom_height)
            if dims:
                try:
                    source.SetImageLayout((0, 0, dims[0], dims[1]), 1, 1, 1)
                except Exception:
                    pass

        # ADF / Feeder
        if s.source in (ScanSource.ADF_FRONT, ScanSource.ADF_BACK,
                        ScanSource.ADF_DUPLEX):
            try:
                source.SetCapability(
                    twain.CAP_FEEDERENABLED, twain.TWTY_BOOL, True
                )
            except Exception:
                pass

        # Duplex
        if s.source == ScanSource.ADF_DUPLEX or s.duplex:
            try:
                source.SetCapability(
                    twain.CAP_DUPLEXENABLED, twain.TWTY_BOOL, True
                )
            except Exception:
                pass

        # B&W threshold
        if s.color_mode == ColorMode.BW:
            try:
                source.SetCapability(
                    twain.ICAP_THRESHOLD, twain.TWTY_FIX32,
                    float(s.threshold)
                )
            except Exception:
                pass

    def _scan_wia(self) -> Optional[Image.Image]:
        """Perform scan via WIA driver."""
        try:
            import comtypes.client

            device_id = self._selected_scanner.device_id.replace("wia:", "")
            wia_manager = comtypes.client.CreateObject("WIA.DeviceManager")

            device = None
            for i in range(1, wia_manager.DeviceInfos.Count + 1):
                info = wia_manager.DeviceInfos.Item(i)
                if info.DeviceID == device_id:
                    device = info.Connect()
                    break

            if not device:
                raise RuntimeError("Could not connect to WIA device")

            item = device.Items[1]
            s = self._settings

            # Set properties
            props = item.Properties
            color_map = {
                ColorMode.COLOR: 1,
                ColorMode.GRAYSCALE: 2,
                ColorMode.BW: 4,
            }
            try:
                props("6146").Value = color_map.get(s.color_mode, 1)
                props("6147").Value = s.resolution  # Horizontal DPI
                props("6148").Value = s.resolution  # Vertical DPI
            except Exception:
                pass

            if s.brightness != 0:
                try:
                    props("6154").Value = s.brightness * 10
                except Exception:
                    pass

            if s.contrast != 0:
                try:
                    props("6155").Value = s.contrast * 10
                except Exception:
                    pass

            # Scan area
            if s.paper_size != PaperSize.AUTO:
                dims = PAPER_DIMENSIONS.get(s.paper_size)
                if dims is None and s.paper_size == PaperSize.CUSTOM:
                    dims = (s.custom_width, s.custom_height)
                if dims:
                    try:
                        props("6151").Value = int(dims[0] * s.resolution)
                        props("6152").Value = int(dims[1] * s.resolution)
                    except Exception:
                        pass

            # Transfer image
            img_file = item.Transfer("{B96B3CAE-0728-11D3-9D7B-0000F81EF32E}")
            import tempfile
            tmp = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
            tmp_path = tmp.name
            tmp.close()
            img_file.SaveFile(tmp_path)
            image = Image.open(tmp_path).copy()
            os.unlink(tmp_path)
            return image

        except Exception as e:
            logger.error(f"WIA scan error: {e}")
            raise RuntimeError(f"WIA scan failed: {e}")

    def _scan_simulation(self) -> Optional[Image.Image]:
        """Generate a simulated scan image for development."""
        s = self._settings
        dims = PAPER_DIMENSIONS.get(s.paper_size, PAPER_DIMENSIONS[PaperSize.A4])
        width = int(dims[0] * s.resolution)
        height = int(dims[1] * s.resolution)

        if s.color_mode == ColorMode.COLOR:
            image = Image.new("RGB", (width, height), (255, 255, 255))
        elif s.color_mode == ColorMode.GRAYSCALE:
            image = Image.new("L", (width, height), 255)
        else:
            image = Image.new("1", (width, height), 1)

        # Draw a border and text to indicate it's a simulated scan
        try:
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(image)
            border_color = (200, 200, 200) if s.color_mode == ColorMode.COLOR else 200
            text_color = (100, 100, 100) if s.color_mode == ColorMode.COLOR else 100
            if s.color_mode == ColorMode.BW:
                border_color = 0
                text_color = 0

            # Draw border
            draw.rectangle(
                [20, 20, width - 20, height - 20],
                outline=border_color, width=3
            )
            # Draw header lines to simulate a document
            y = 80
            for i in range(15):
                line_width = width - 160 if i > 0 else width // 2
                draw.rectangle(
                    [80, y, 80 + line_width, y + 8],
                    fill=text_color
                )
                y += 30
                if y > height - 100:
                    break

            # Label
            draw.text(
                (width // 2 - 100, height - 60),
                "SIMULATED SCAN",
                fill=text_color,
            )
        except Exception:
            pass

        return image

    def scan_batch(self, max_pages: int = 0, callback=None) -> list[Image.Image]:
        """
        Scan multiple pages from ADF.

        Args:
            max_pages: Maximum pages to scan (0 = until feeder empty).
            callback: Called with (page_number, image) after each page.

        Returns:
            List of scanned PIL Images.
        """
        pages = []
        page_num = 0

        while not self._cancel_requested:
            if max_pages > 0 and page_num >= max_pages:
                break

            try:
                image = self.scan_page()
                if image is None:
                    break
                pages.append(image)
                page_num += 1
                if callback:
                    callback(page_num, image)
            except RuntimeError as e:
                error_msg = str(e).lower()
                if "empty" in error_msg or "no paper" in error_msg:
                    break
                raise

        return pages

    def cancel_scan(self):
        """Request cancellation of the current scan operation."""
        self._cancel_requested = True
        logger.info("Scan cancellation requested")

    def close(self):
        """Release scanner resources."""
        if self._twain_source:
            try:
                self._twain_source.close()
            except Exception:
                pass
            self._twain_source = None

        if self._twain_manager:
            try:
                self._twain_manager.close()
            except Exception:
                pass
            self._twain_manager = None

        logger.info("Scanner engine closed")
