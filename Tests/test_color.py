#region ============================ Imports =============================

import unittest
import sys
import os
import time

# Add the project root to PYTHONPATH for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from pytui.Color import ColorHandler


#endregion



class TestColorHandler(unittest.TestCase):
    def setUp(self):
        # Initialize with red=255, green=128, blue=64, alpha=32
        self.test_color = ColorHandler.from_ARGB(255, 128, 64, 32)

    def test_color_channels(self):
        """Test getting and setting individual color channels"""
        self.assertEqual(self.test_color.r, 255)
        self.assertEqual(self.test_color.g, 128)
        self.assertEqual(self.test_color.b, 64)
        self.assertEqual(self.test_color.a, 32)

    def test_channel_modification(self):
        """Test modifying individual color channels"""
        # Modify red channel
        self.test_color.r = 200
        self.assertEqual(self.test_color.r, 200)
        self.assertEqual(self.test_color.g, 128)  # Other channels unchanged
        self.assertEqual(self.test_color.b, 64)
        self.assertEqual(self.test_color.a, 32)

        # Modify green channel
        self.test_color.g = 100
        self.assertEqual(self.test_color.r, 200)
        self.assertEqual(self.test_color.g, 100)
        self.assertEqual(self.test_color.b, 64)
        self.assertEqual(self.test_color.a, 32)

        # Modify blue channel
        self.test_color.b = 50
        self.assertEqual(self.test_color.r, 200)
        self.assertEqual(self.test_color.g, 100)
        self.assertEqual(self.test_color.b, 50)
        self.assertEqual(self.test_color.a, 32)

        # Modify alpha channel
        self.test_color.a = 255
        self.assertEqual(self.test_color.r, 200)
        self.assertEqual(self.test_color.g, 100)
        self.assertEqual(self.test_color.b, 50)
        self.assertEqual(self.test_color.a, 255)

    def test_value_out_of_bounds(self):
        """Test illegal value overflow/underflow for color channels"""
        with self.assertRaises(ValueError):
            self.test_color.r = 300  # Value for red channel must be between 0 and 255
        with self.assertRaises(ValueError):
            self.test_color.g = -50  # Value for green channel must be between 0 and 255

    def test_equality(self):
        """Test equality comparison"""
        color1 = ColorHandler((255 << 24) | (128 << 16) | (64 << 8) | 32)
        color2 = ColorHandler((255 << 24) | (128 << 16) | (64 << 8) | 32)
        color3 = ColorHandler((200 << 24) | (128 << 16) | (64 << 8) | 32)

        self.assertEqual(color1, color2)
        self.assertNotEqual(color1, color3)

    def test_hash(self):
        """Test hash functionality"""
        color1 = ColorHandler((255 << 24) | (128 << 16) | (64 << 8) | 32)
        color2 = ColorHandler((255 << 24) | (128 << 16) | (64 << 8) | 32)

        self.assertEqual(hash(color1), hash(color2))
        self.assertEqual(hash(color1), hash(color1.value))

    def test_color_inversion(self):
        """Test color inversion functionality"""
        # Test with pure colors
        color = ColorHandler(0xFFFF0000)  # Red
        color.invert()
        self.assertEqual(color & 0x00FFFFFF, 0x0000FFFF)  # Should be cyan

        color = ColorHandler(0xFF00FF00)  # Green
        color.invert()
        self.assertEqual(color & 0x00FFFFFF, 0x00FF00FF)  # Should be magenta

        # Test with mixed colors
        color = ColorHandler(0xFF808080)  # Gray
        color.invert()
        self.assertEqual(color & 0x00FFFFFF, 0x007F7F7F)  # Should be inverse gray

        # Test alpha preservation
        color = ColorHandler(0x80FF0000)  # Semi-transparent red
        color.invert()
        self.assertEqual(color.a, 0x80)  # Alpha should remain unchanged

    def test_scale_exposure(self):
        """Test exposure scaling functionality"""
        color = ColorHandler(0xFF808080)  # Gray

        # Test brightening
        brightened = ColorHandler(color).scale_exposure(1.5)
        self.assertEqual(ColorHandler(brightened).r, min(255, int(0x80 * 1.5)))
        self.assertEqual(ColorHandler(brightened).g, min(255, int(0x80 * 1.5)))
        self.assertEqual(ColorHandler(brightened).b, min(255, int(0x80 * 1.5)))

        # Test darkening
        darkened = ColorHandler(color).scale_exposure(0.5)
        self.assertEqual(ColorHandler(darkened).r, int(0x80 * 0.5))
        self.assertEqual(ColorHandler(darkened).g, int(0x80 * 0.5))
        self.assertEqual(ColorHandler(darkened).b, int(0x80 * 0.5))

        # Test clamping
        over_bright = ColorHandler(color).scale_exposure(10.0)
        self.assertEqual(ColorHandler(over_bright).r, 255)
        self.assertEqual(ColorHandler(over_bright).g, 255)
        self.assertEqual(ColorHandler(over_bright).b, 255)

        over_dark = ColorHandler(color).scale_exposure(-0.5)
        self.assertEqual(ColorHandler(over_dark).r, 0)
        self.assertEqual(ColorHandler(over_dark).g, 0)
        self.assertEqual(ColorHandler(over_dark).b, 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
