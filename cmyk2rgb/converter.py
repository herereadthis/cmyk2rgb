"""
converter.py

Functions to convert CMYK to RGB using ICC profiles.

Requires:
- Pillow (PIL) for image and color management.
"""

from pathlib import Path
from PIL import ImageCms, Image

# Base directory for ICC profiles relative to this file
PROFILE_DIR = Path(__file__).parent / "profiles"

def cmyk_to_rgb(c: int, m: int, y: int, k: int, profile_filename: str) -> str:
    """
    Convert CMYK color to RGB hex string using a specified ICC profile.

    Args:
        c (int): Cyan percentage (0-100)
        m (int): Magenta percentage (0-100)
        y (int): Yellow percentage (0-100)
        k (int): Black percentage (0-100)
        profile_filename (str): ICC profile filename stored under profiles/

    Returns:
        str: RGB color in hex format, e.g. '#29bdad'
    """
    # Normalize CMYK to 0.0–1.0 floats for Pillow
    c_norm = c / 100
    m_norm = m / 100
    y_norm = y / 100
    k_norm = k / 100

    # Create a single-pixel CMYK image
    cmyk_pixel = (int(c_norm * 255), int(m_norm * 255), int(y_norm * 255), int(k_norm * 255))
    img_cmyk = Image.new("CMYK", (1, 1), cmyk_pixel)

    # Load the ICC profile from profiles/ directory
    profile_path = PROFILE_DIR / profile_filename
    if not profile_path.exists():
        raise FileNotFoundError(f"ICC profile not found: {profile_path}")

    cmyk_profile = ImageCms.getOpenProfile(str(profile_path))

    # Use sRGB profile for the output color space
    srgb_profile = ImageCms.createProfile("sRGB")

    # Build transform from CMYK to sRGB using specified profile
    transform = ImageCms.buildTransformFromOpenProfiles(
        cmyk_profile, srgb_profile, "CMYK", "RGB"
    )

    # Apply the color transform
    img_rgb = ImageCms.applyTransform(img_cmyk, transform)

    # Extract RGB pixel (tuple of 3 ints)
    r, g, b = img_rgb.getpixel((0, 0))

    # Format RGB as hex string, lowercase
    rgb_hex = f"#{r:02x}{g:02x}{b:02x}"
    return rgb_hex
