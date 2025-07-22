# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                          Grok Image Generator                             ║
# ║  Minimal imghdr module replacement for Python 3.13 compatibility          ║
# ║  Features:                                                                ║
# ║  - Detects JPEG, PNG, GIF, WEBP, BMP, ICO, and TIFF formats              ║
# ║  - Supports file paths and file-like objects with 32-byte header check    ║
# ║  Author: [Your Name]                                                     ║
# ║  Creation Date: July 22, 2025                                            ║
# ║  Last Modified: July 22, 2025                                            ║
# ║  Notes: Place this file in the same directory as main.py                 ║
# ║         Future: Add support for additional formats or enhance detection  ║
# ╚════════════════════════════════════════════════════════════════════════════╝
"""
Minimal imghdr module replacement for Python 3.13 compatibility
Place this file in the same directory as your main.py
"""


def what(file, h=None):
    """
    Detect image format from file or file-like object
    Returns format string or None if not recognized
    """
    try:
        if hasattr(file, 'read'):
            # File-like object
            current_pos = file.tell() if hasattr(file, 'tell') else 0
            header = file.read(32)
            if hasattr(file, 'seek'):
                file.seek(current_pos)  # Reset file pointer
        else:
            # File path string
            with open(file, 'rb') as f:
                header = f.read(32)

        # Detect common image formats by magic bytes
        if header.startswith(b'\xff\xd8\xff'):
            return 'jpeg'
        elif header.startswith(b'\x89PNG\r\n\x1a\n'):
            return 'png'
        elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
            return 'gif'
        elif header.startswith(b'RIFF') and b'WEBP' in header[:12]:
            return 'webp'
        elif header.startswith(b'BM'):
            return 'bmp'
        elif header.startswith(b'\x00\x00\x01\x00') or header.startswith(b'\x00\x00\x02\x00'):
            return 'ico'
        elif header.startswith(b'II\x2a\x00') or header.startswith(b'MM\x00\x2a'):
            return 'tiff'

        return None

    except (IOError, OSError, AttributeError):
        return None


def test(file, h=None):
    """Test if file is a valid image (legacy compatibility)"""
    return what(file, h) is not None


# Additional legacy functions for compatibility
def test_jpeg(h, f):
    return h.startswith(b'\xff\xd8\xff')


def test_png(h, f):
    return h.startswith(b'\x89PNG\r\n\x1a\n')


def test_gif(h, f):
    return h.startswith(b'GIF87a') or h.startswith(b'GIF89a')


def test_webp(h, f):
    return h.startswith(b'RIFF') and b'WEBP' in h[:12]