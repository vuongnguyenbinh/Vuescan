"""
PDF Exporter - Clean PDF export without watermark.

Exports scanned images to PDF format with no watermarks,
supporting multi-page documents, compression, and metadata.
"""

import io
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from PIL import Image

logger = logging.getLogger(__name__)


@dataclass
class PDFExportSettings:
    """Settings for PDF export."""
    output_path: str = ""
    title: str = ""
    author: str = ""
    subject: str = ""
    compress_images: bool = True
    jpeg_quality: int = 85
    page_size: Optional[tuple[float, float]] = None  # (width_pt, height_pt)
    dpi: int = 300


class PDFExporter:
    """
    Exports scanned images to clean PDF without any watermark.

    Uses img2pdf for lossless image-to-PDF conversion, and pikepdf
    for metadata and post-processing.
    """

    def export_single_page(self, image: Image.Image, settings: PDFExportSettings) -> str:
        """Export a single image to PDF."""
        return self.export_pages([image], settings)

    def export_pages(self, images: list[Image.Image],
                     settings: PDFExportSettings) -> str:
        """
        Export multiple images to a single multi-page PDF.

        Args:
            images: List of PIL Images to include.
            settings: PDF export configuration.

        Returns:
            Path to the saved PDF file.
        """
        if not images:
            raise ValueError("No images to export")

        if not settings.output_path:
            raise ValueError("Output path is required")

        # Ensure output directory exists
        output_dir = os.path.dirname(settings.output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        try:
            return self._export_with_img2pdf(images, settings)
        except ImportError:
            logger.info("img2pdf not available, using reportlab fallback")
            return self._export_with_reportlab(images, settings)

    def _export_with_img2pdf(self, images: list[Image.Image],
                              settings: PDFExportSettings) -> str:
        """Export using img2pdf (lossless, fast)."""
        import img2pdf
        import pikepdf

        image_bytes_list = []

        for image in images:
            buf = io.BytesIO()

            # Convert to RGB if necessary (img2pdf doesn't support all modes)
            if image.mode == "1":
                # B&W: convert to grayscale for better PDF compression
                export_img = image.convert("L")
            elif image.mode == "RGBA":
                export_img = image.convert("RGB")
            elif image.mode not in ("RGB", "L"):
                export_img = image.convert("RGB")
            else:
                export_img = image

            if settings.compress_images:
                export_img.save(buf, format="JPEG",
                                quality=settings.jpeg_quality)
            else:
                export_img.save(buf, format="TIFF")

            image_bytes_list.append(buf.getvalue())

        # Create PDF with img2pdf
        pdf_bytes = img2pdf.convert(
            image_bytes_list,
            rotation=img2pdf.Rotation.ifvalid,
        )

        # Write initial PDF
        temp_path = settings.output_path + ".tmp"
        with open(temp_path, "wb") as f:
            f.write(pdf_bytes)

        # Add metadata with pikepdf
        with pikepdf.open(temp_path) as pdf:
            with pdf.open_metadata() as meta:
                meta["dc:title"] = settings.title or "Scanned Document"
                meta["dc:creator"] = [settings.author or "FiScanPro"]
                meta["dc:description"] = settings.subject or ""
                meta["xmp:CreatorTool"] = "FiScanPro 1.0.0"
                meta["xmp:CreateDate"] = datetime.now().isoformat()

            pdf.save(settings.output_path)

        # Clean up temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

        logger.info(
            f"PDF exported: {settings.output_path} "
            f"({len(images)} pages)"
        )
        return settings.output_path

    def _export_with_reportlab(self, images: list[Image.Image],
                                settings: PDFExportSettings) -> str:
        """Fallback export using reportlab (pure Python)."""
        from reportlab.lib.pagesizes import A4, letter
        from reportlab.lib.utils import ImageReader
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(settings.output_path)

        # Set metadata
        c.setTitle(settings.title or "Scanned Document")
        c.setAuthor(settings.author or "FiScanPro")
        c.setSubject(settings.subject or "")
        c.setCreator("FiScanPro 1.0.0")

        for image in images:
            # Convert to RGB
            if image.mode not in ("RGB", "L"):
                export_img = image.convert("RGB")
            else:
                export_img = image

            # Calculate page size from image dimensions
            img_width_px, img_height_px = export_img.size
            dpi = settings.dpi or 300
            img_width_pt = img_width_px * 72.0 / dpi
            img_height_pt = img_height_px * 72.0 / dpi

            if settings.page_size:
                page_width, page_height = settings.page_size
            else:
                page_width, page_height = img_width_pt, img_height_pt

            c.setPageSize((page_width, page_height))

            # Scale image to fit page while maintaining aspect ratio
            scale_x = page_width / img_width_pt
            scale_y = page_height / img_height_pt
            scale = min(scale_x, scale_y)

            draw_width = img_width_pt * scale
            draw_height = img_height_pt * scale
            x_offset = (page_width - draw_width) / 2
            y_offset = (page_height - draw_height) / 2

            # Save image to buffer
            buf = io.BytesIO()
            if settings.compress_images:
                export_img.save(buf, format="JPEG",
                                quality=settings.jpeg_quality)
            else:
                export_img.save(buf, format="PNG")
            buf.seek(0)

            img_reader = ImageReader(buf)
            c.drawImage(img_reader, x_offset, y_offset,
                        draw_width, draw_height)
            c.showPage()

        c.save()

        logger.info(
            f"PDF exported (reportlab): {settings.output_path} "
            f"({len(images)} pages)"
        )
        return settings.output_path

    def export_images_to_format(self, images: list[Image.Image],
                                output_path: str,
                                format_type: str = "JPEG",
                                quality: int = 95) -> list[str]:
        """
        Export images to individual image files.

        Args:
            images: List of PIL Images.
            output_path: Base output path (page number will be appended).
            format_type: "JPEG", "PNG", "TIFF", or "BMP".
            quality: JPEG quality (1-100).

        Returns:
            List of saved file paths.
        """
        saved_paths = []
        base, ext = os.path.splitext(output_path)

        ext_map = {
            "JPEG": ".jpg",
            "PNG": ".png",
            "TIFF": ".tiff",
            "BMP": ".bmp",
        }
        file_ext = ext_map.get(format_type, ext or ".jpg")

        for i, image in enumerate(images):
            if len(images) == 1:
                file_path = f"{base}{file_ext}"
            else:
                file_path = f"{base}_{i + 1:04d}{file_ext}"

            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)

            save_kwargs = {}
            if format_type == "JPEG":
                if image.mode not in ("RGB", "L"):
                    image = image.convert("RGB")
                save_kwargs["quality"] = quality
                save_kwargs["optimize"] = True
            elif format_type == "TIFF":
                save_kwargs["compression"] = "tiff_lzw"
            elif format_type == "PNG":
                save_kwargs["optimize"] = True

            image.save(file_path, format=format_type, **save_kwargs)
            saved_paths.append(file_path)

        logger.info(f"Exported {len(saved_paths)} image(s) as {format_type}")
        return saved_paths
