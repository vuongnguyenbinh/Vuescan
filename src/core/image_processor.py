"""
Image Processing Pipeline.

Provides image enhancement, correction, and transformation
operations for scanned documents.
"""

import logging
import math
from typing import Optional

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Image processing operations for scanned documents."""

    @staticmethod
    def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
        """
        Adjust image brightness.

        Args:
            image: Input PIL Image.
            factor: Brightness factor (0.0=black, 1.0=original, 2.0=max bright).
        """
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)

    @staticmethod
    def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
        """
        Adjust image contrast.

        Args:
            image: Input PIL Image.
            factor: Contrast factor (0.0=gray, 1.0=original, 2.0=max contrast).
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)

    @staticmethod
    def adjust_sharpness(image: Image.Image, factor: float) -> Image.Image:
        """
        Adjust image sharpness.

        Args:
            image: Input PIL Image.
            factor: Sharpness factor (0.0=blurred, 1.0=original, 2.0=sharp).
        """
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)

    @staticmethod
    def adjust_saturation(image: Image.Image, factor: float) -> Image.Image:
        """
        Adjust color saturation.

        Args:
            image: Input PIL Image.
            factor: Saturation factor (0.0=grayscale, 1.0=original).
        """
        if image.mode not in ("RGB", "RGBA"):
            return image
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)

    @staticmethod
    def auto_levels(image: Image.Image) -> Image.Image:
        """Auto-adjust levels (histogram stretch)."""
        if image.mode == "1":
            return image
        return ImageOps.autocontrast(image, cutoff=0.5)

    @staticmethod
    def convert_to_grayscale(image: Image.Image) -> Image.Image:
        """Convert image to grayscale."""
        return image.convert("L")

    @staticmethod
    def convert_to_bw(image: Image.Image, threshold: int = 128) -> Image.Image:
        """Convert image to black & white using threshold."""
        gray = image.convert("L")
        return gray.point(lambda x: 255 if x > threshold else 0, "1")

    @staticmethod
    def rotate(image: Image.Image, angle: float,
               expand: bool = True) -> Image.Image:
        """
        Rotate image by given angle (degrees, counter-clockwise).
        """
        return image.rotate(angle, expand=expand, resample=Image.BICUBIC,
                            fillcolor=(255, 255, 255) if image.mode == "RGB" else 255)

    @staticmethod
    def rotate_90_cw(image: Image.Image) -> Image.Image:
        """Rotate 90 degrees clockwise."""
        return image.transpose(Image.ROTATE_270)

    @staticmethod
    def rotate_90_ccw(image: Image.Image) -> Image.Image:
        """Rotate 90 degrees counter-clockwise."""
        return image.transpose(Image.ROTATE_90)

    @staticmethod
    def rotate_180(image: Image.Image) -> Image.Image:
        """Rotate 180 degrees."""
        return image.transpose(Image.ROTATE_180)

    @staticmethod
    def flip_horizontal(image: Image.Image) -> Image.Image:
        """Flip image horizontally."""
        return image.transpose(Image.FLIP_LEFT_RIGHT)

    @staticmethod
    def flip_vertical(image: Image.Image) -> Image.Image:
        """Flip image vertically."""
        return image.transpose(Image.FLIP_TOP_BOTTOM)

    @staticmethod
    def crop(image: Image.Image, left: int, top: int,
             right: int, bottom: int) -> Image.Image:
        """Crop image to specified rectangle."""
        return image.crop((left, top, right, bottom))

    @staticmethod
    def deskew(image: Image.Image) -> Image.Image:
        """
        Automatically detect and correct skew in scanned documents.
        Uses a simplified projection-profile method.
        """
        # Convert to grayscale for analysis
        if image.mode == "1":
            gray = image.convert("L")
        elif image.mode in ("RGB", "RGBA"):
            gray = image.convert("L")
        else:
            gray = image

        # Convert to numpy array
        img_array = np.array(gray)

        # Binarize
        threshold = np.mean(img_array)
        binary = (img_array < threshold).astype(np.uint8)

        # Try different angles and find the one with maximum variance
        # of horizontal projection profile (indicating straight text lines)
        best_angle = 0.0
        best_score = 0.0

        for angle_10x in range(-100, 101, 5):  # -10.0 to +10.0 degrees
            angle = angle_10x / 10.0
            if angle == 0:
                rotated = binary
            else:
                # Simple rotation using scipy-like approach with numpy
                rotated = _rotate_array(binary, angle)

            # Compute horizontal projection profile
            profile = np.sum(rotated, axis=1)

            # Score = variance of profile (higher = more aligned)
            score = np.var(profile)
            if score > best_score:
                best_score = score
                best_angle = angle

        # Refine around best angle
        for angle_100x in range(int(best_angle * 100) - 50,
                                 int(best_angle * 100) + 51, 1):
            angle = angle_100x / 100.0
            rotated = _rotate_array(binary, angle)
            profile = np.sum(rotated, axis=1)
            score = np.var(profile)
            if score > best_score:
                best_score = score
                best_angle = angle

        if abs(best_angle) < 0.01:
            return image

        logger.info(f"Deskew angle detected: {best_angle:.2f}°")

        # Apply rotation to original image
        return image.rotate(best_angle, expand=True,
                            resample=Image.BICUBIC,
                            fillcolor=(255, 255, 255) if image.mode == "RGB" else 255)

    @staticmethod
    def remove_blank_page(image: Image.Image,
                          threshold: float = 0.99) -> bool:
        """
        Check if a page is mostly blank.

        Returns True if the page should be removed (is blank).
        """
        gray = image.convert("L")
        arr = np.array(gray)
        white_ratio = np.sum(arr > 240) / arr.size
        return white_ratio > threshold

    @staticmethod
    def resize(image: Image.Image, width: Optional[int] = None,
               height: Optional[int] = None) -> Image.Image:
        """Resize image maintaining aspect ratio."""
        orig_w, orig_h = image.size

        if width and height:
            return image.resize((width, height), Image.LANCZOS)
        elif width:
            ratio = width / orig_w
            new_height = int(orig_h * ratio)
            return image.resize((width, new_height), Image.LANCZOS)
        elif height:
            ratio = height / orig_h
            new_width = int(orig_w * ratio)
            return image.resize((new_width, height), Image.LANCZOS)
        return image

    @staticmethod
    def auto_enhance(image: Image.Image) -> Image.Image:
        """Apply automatic enhancement for scanned documents."""
        # Auto contrast
        result = ImageOps.autocontrast(image, cutoff=1)
        # Slight sharpening
        result = ImageEnhance.Sharpness(result).enhance(1.3)
        return result


def _rotate_array(arr: np.ndarray, angle_degrees: float) -> np.ndarray:
    """Rotate a 2D numpy array by a small angle (for deskew analysis)."""
    angle_rad = math.radians(angle_degrees)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    h, w = arr.shape
    cy, cx = h / 2, w / 2

    # For small angles, we can use a simplified approach
    # Create output of same size
    result = np.zeros_like(arr)

    # Generate coordinate grids
    y_coords, x_coords = np.mgrid[0:h, 0:w]

    # Map to source coordinates
    src_x = cos_a * (x_coords - cx) + sin_a * (y_coords - cy) + cx
    src_y = -sin_a * (x_coords - cx) + cos_a * (y_coords - cy) + cy

    # Nearest-neighbor interpolation
    src_x = np.round(src_x).astype(int)
    src_y = np.round(src_y).astype(int)

    # Mask valid coordinates
    valid = (src_x >= 0) & (src_x < w) & (src_y >= 0) & (src_y < h)
    result[valid] = arr[src_y[valid], src_x[valid]]

    return result
