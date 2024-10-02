"""
Color structure and color palettes.
"""


#========================Imports========================

# No dependency
from collections import Collection
from enum import Enum


#region ======================== Color ========================

class Color:

    def __init__(self, r: int, g: int, b: int, a: int = 255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __eq__(self, other):
        return (self.r, self.g, self.b, self.a) == (other.r, other.g, other.b, other.a)

    def __repr__(self):
        return Color.tostring(self)

    def __str__(self):
        return NamedColorList.get_name(self)

    @property
    def r(self):
        """ The red channel of the color, from 0 to 255. """
        return self._r

    @r.setter
    def r(self, value: int):
        """ The red channel of the color, from 0 to 255. """
        self._r = min(max(0, int(value)), 255)

    @property
    def g(self):
        """ The green channel of the color, from 0 to 255. """
        return self._g

    @g.setter
    def g(self, value: int):
        """ The green channel of the color, from 0 to 255. """
        self._g = min(max(0, int(value)), 255)

    @property
    def b(self):
        """ The blue channel of the color, from 0 to 255. """
        return self._b

    @b.setter
    def b(self, value: int):
        """ The blue channel of the color, from 0 to 255. """
        self._b = min(max(0, int(value)), 255)

    @property
    def a(self):
        """ The alpha channel (transparency) of the color, from 0 to 255.
            Used for dithering effect. """
        return self._a

    @a.setter
    def a(self, value: int):
        """ The alpha channel (transparency) of the color, from 0 to 255.
            Used for dithering effect. """
        self._a = min(max(0, int(value)), 255)

    def closest_from_palette(self, palette: Collection['Color']):
        """
        Searches for the closest color to the current one in a given palette. \n
        Note that this comparison does not take into account the alpha (transparency) channel.

        :param palette: A collection of Color instances.
        :return: The Color instance closest from the current color within the palette, or None if palette is empty.
        """
        return _closest_from_palette(self, palette)

    @staticmethod
    def from_html_hex(hex_string: str):
        """
        Instantiates a Color object from an HTML hexadecimal code.
        The format must either be #RGB, #RGBA, #RRGGBB or #RRGGBBAA

        :param hex_string: HTML hexadecimal color code, either in shorthand or longhand form, with optional alpha value.
        :return: A color instance with the same values as the hexadecimal code.
        """
        hex_string = hex_string.strip()

        if hex_string[0] != '#':
            raise ValueError("Not a valid hexadecimal color code: " + hex_string)

        match len(hex_string[1:]):
            case 3:
                # Shorthand RBG format
                return Color(
                    int(2*hex_string[1], 16),
                    int(2*hex_string[2], 16),
                    int(2*hex_string[3], 16))
            case 4:
                # Shorthand RBGA format
                return Color(
                    int(2*hex_string[1], 16),
                    int(2*hex_string[2], 16),
                    int(2*hex_string[3], 16),
                    int(2*hex_string[4], 16))
            case 6:
                # Longhand RRGGBB format
                return Color(
                    int(hex_string[1:3], 16),
                    int(hex_string[3:5], 16),
                    int(hex_string[5:7], 16))
            case 8:
                # Longhand RRGGBBAA format
                return Color(
                    int(hex_string[1:3], 16),
                    int(hex_string[3:5], 16),
                    int(hex_string[5:7], 16),
                    int(hex_string[7:9], 16))
            case _:
                raise ValueError("Not a valid hexadecimal color code: " + hex_string)

    @staticmethod
    def from_hsv(hue: float, saturation: float, value: float):
        """
        Instantiates a Color object from HSV values.

        The RGB values are treated as within the sRGB color space.

        :param hue:
        :param saturation:
        :param value:
        :return:
        :rtype: Color
        """
        #TODO convert HSV to Color
        pass

    def to_html(self, include_alpha=False):
        """
        Converts this color into a fully-qualified HTML hexadecimal color code.

        :param include_alpha: Whether the alpha channel is included into the hexadecimal code.
        :return: A string representation of this color in hexadecimal HTML color format.
        :rtype: str
        """
        if include_alpha:
            return '#%02x%02x%02x%02x' % (self.r, self.g, self.b, self.a)
        else:
            return '#%02x%02x%02x' % (self.r, self.g, self.b)

    def to_hsv(self):
        """
        Converts this color into its corresponding HSV representation.

        The RGB values are treated as within the sRGB color space.

        :return: a tuple containing three floats in this order: (hue, saturation, value)
        :rtype: (float, float, float)
        """
        # Formula: https://en.wikipedia.org/wiki/HSL_and_HSV#From_RGB

        unit_r = self.r / 255.0
        unit_g = self.g / 255.0
        unit_b = self.b / 255.0
        x_max = max(unit_r, unit_g, unit_b)     # a.k.a. Value
        x_min = min(unit_r, unit_g, unit_b)
        v_range = x_max - x_min

        if v_range == 0:
            hue = 0
        elif x_max == unit_r:
            hue = 60 * (unit_g - unit_b) / v_range
        elif x_max == unit_g:
            hue = 60 * (2 + (unit_b - unit_r) / v_range)
        else:   # x_max == unit_b
            hue = 60 * (4 + (unit_r - unit_g) / v_range)

        if x_max == 0:
            saturation = 0
        else:
            saturation = v_range / x_max
        
        return hue, saturation, x_max

    def to_ansi24_code(self, is_background=False):
        """
        Converts the current color into ANSI-ES terminal color code.

        :param is_background: False to output text character color, True to output text background color.
        :return: A properly formatted 24-bit ANSI-ES color code.
        :rtype: str
        """
        if is_background:
            if self.a == 0:
                # Reset
                return "\033[39m"
            return "\033[48;2;" + str(self.r) + ";" + str(self.g) + ";" + str(self.b) + " m"
        else:
            return "\033[38;2;" + str(self.r) + ";" + str(self.g) + ";" + str(self.b) + " m"

    @staticmethod
    def tostring(color):
        return "Color(R=" + str(color.r) + ", G=" + str(color.g) + ", B=" + str(color.b) + ", A=" + str(color.a) + ")"

#endregion Color


#region ======================== Color Spaces ========================

class NamedColorList(Enum):
    """
    A class/enum containing a list of common named colors.
    """

    Default = Color(0, 0, 0, -1)
    Transparent = Color(0, 0, 0, 0)
    """ The transparent color serves to reset """

    # Grayscale colors
    Black = Color(0, 0, 0)
    DarkGray = Color(64, 64, 64)
    Gray = Color(128, 128, 128)
    LightGray = Color(192, 192, 192)
    White = Color(255, 255, 255)

    # Spectral color ordering
    DarkRed = Color(139, 0, 0)
    Brown = Color(165, 42, 42)
    Red = Color(255, 0, 0)
    OrangeRed = Color(255, 69, 0)
    Orange = Color(255, 165, 0)
    Gold = Color(255, 215, 0)
    Yellow = Color(255, 255, 0)
    YellowGreen = Color(154, 205, 50)
    Green = Color(0, 255, 0)
    DarkGreen = Color(0, 128, 0)
    Cyan = Color(0, 255, 255)
    LightBlue = Color(173, 216, 230)
    Blue = Color(0, 0, 255)
    DarkBlue = Color(0, 0, 139)
    Indigo = Color(75, 0, 130)
    Purple = Color(128, 0, 128)
    Magenta = Color(255, 0, 255)
    Pink = Color(255, 192, 203)
    Beige = Color(245, 245, 220)

    @staticmethod
    def get_name(color: Color):
        colors = {key: value for key, value in NamedColorList.__dict__.items() if
                  type(value) is Color}

        closestColor = _closest_from_palette(color, list(colors.values()))

        col_name = Color.tostring(closestColor)
        for name, col in colors.items():
            if col == closestColor:
                col_name_list = list(name)
                col_name = col_name_list.pop(0).lower()
                while col_name_list:
                    letter = col_name_list.pop(0)
                    if letter.isupper():
                        col_name += " " + letter.lower()
                    else:
                        col_name += letter

        if closestColor == color:
            return col_name
        else:
            return col_name + "-ish"


class ColorPalettes:
    """
    A class containing standard color palettes and conversion functions.
    """

    ANSI3Palette = {
        NamedColorList.Black: 30,           # Black
        Color(170, 0, 0): 31,       # Red
        Color(0, 170, 0): 32,       # Green
        Color(170, 85, 0): 33,      # Yellow
        Color(0, 0, 170): 34,       # Blue
        Color(170, 0, 170): 35,     # Magenta
        Color(0, 170, 170): 36,     # Cyan
        NamedColorList.LightGray: 37        # White
    }
    """ The 8 minimum colors supported by all ANSI-ES enabled terminals.
        This dictionary corresponds Colors with their respective ANSI foreground color number. """

    ANSI4Palette = {
        # ESC 30 to 37
        NamedColorList.Black: 30,           # Standard black
        Color(170, 0, 0): 31,       # Standard red
        Color(0, 170, 0): 32,       # Standard green
        Color(170, 85, 0): 33,      # Standard yellow
        Color(0, 0, 170): 34,       # Standard blue
        Color(170, 0, 170): 35,     # Standard magenta
        Color(0, 170, 170): 36,     # Standard cyan
        NamedColorList.LightGray: 37,       # Standard white
        # ESC 90 to 97
        NamedColorList.Gray: 90,            # Bright black (gray)
        NamedColorList.Red: 91,             # Bright red
        NamedColorList.Green: 92,           # Bright
        NamedColorList.Yellow: 93,          # Bright
        NamedColorList.Blue: 94,            # Bright
        NamedColorList.Magenta: 95,         # Bright
        NamedColorList.Cyan: 96,            # Bright
        NamedColorList.White: 97            # Bright
    }

    ANSI256Palette = {
        # ESC 30 to 37
        NamedColorList.Black: 0,        # Standard black
        Color(128, 0, 0): 1,    # Standard red
        Color(0, 128, 0): 2,    # Standard green
        Color(128, 128, 0): 3,  # Standard yellow
        Color(0, 0, 128): 4,    # Standard blue
        Color(128, 0, 128): 5,  # Standard magenta
        Color(0, 128, 128): 6,  # Standard cyan
        NamedColorList.LightGray: 7,    # Standard white
        # ESC 90 to 97
        NamedColorList.Gray: 8,         # Bright black
        NamedColorList.Red: 9,          # Bright red
        NamedColorList.Green: 10,       # Bright green
        NamedColorList.Yellow: 11,      # Bright yellow
        NamedColorList.Blue: 12,        # Bright blue
        NamedColorList.Magenta: 13,     # Bright magenta
        NamedColorList.Cyan: 14,        # Bright cyan
        NamedColorList.White: 15,       # Bright white
    }
    """ The standard 256-color palette supported by the majority of ANSI-ES enabled terminals. """
    with 16 as i, (0, 95, 135, 175, 215, 255) as vals:
        # 6*6*6 cube gradient: 16 + 36 × r + 6 × g + b (0 ≤ r, g, b ≤ 5)
        for r in vals:
            for g in vals:
                for b in vals:
                    ANSI256Palette[Color(r, g, b)] = i
                    i += 1
        # Grayscale in 24 steps (excluding pure black and white)
        for v in range(8, 239, 10):
            ANSI256Palette[Color(v, v, v)] = i
            i += 1

    IdlePalette = {
        Color(0, 0, 255): 'stdout',
        Color(0, 0, 0): 'SYNC',
        Color(221, 0, 0): 'COMMENT',
        Color(255, 119, 0): 'KEYWORD',
        Color(0, 170, 0): 'STRING',
        Color(0, 0, 255): 'DEFINITION',
        Color(144, 0, 144): 'BUILTIN',
        Color(119, 0, 0): 'console',
        Color(255, 0, 0): 'stderr'
    }
    """
    IdlePalette dictionary corresponds IDLE terminal output color schemes
    to their default RGB values.
    """

    @staticmethod
    def to_idle(color: Color):
        """
        Converts a color to the closest looking color code in IDLE's color palette.

        :param color: The Color instance to find an IDLE match for.
        :return: A string code for IDLE shell color printing.
        :rtype: str
        """
        # Since color distribution in IDLE's palette is limited,
        # there needs to be a bias towards less prevalent colors (e.g. green)
        colorBias = Color(int(color.r * 0.5), color.g, int(color.b * 0.75))
        closestColor = _closest_from_palette(colorBias, ColorPalettes.IdlePalette.keys())
        return ColorPalettes.IdlePalette[closestColor]

    @staticmethod
    def to_ansi4_code(fg_color: Color, bg_color: Color = None, is_background=False):
        """
        Converts a color to the closest looking ANSI-ES 4-bit color code.

        :param fg_color: The Color instance to match.
        :param bg_color:
        :param is_background: False to output text character color, True to output text background color.
        :return: A properly formatted ANSI-ES 4-bit color code.
        :rtype: str
        """
        fg_closest = _closest_from_palette(fg_color, ColorPalettes.ANSI4Palette.keys())
        fg_code = ColorPalettes.ANSI4Palette[fg_closest]
        if is_background:
            return "\033[" + fg_code + "m"
        else:
            return "\033[" + (fg_code + 10) + "m"

    @staticmethod
    def to_ansi256_code(color: Color, is_background=False):
        """
        Converts a color to the closest looking ANSI-ES 8-bit color code.

        :param color: The Color instance to match.
        :param is_background: False to output text character color, True to output text background color.
        :return: A properly formatted ANSI-ES 8-bit color code.
        :rtype: str
        """
        closest = _closest_from_palette(color, ColorPalettes.ANSI256Palette.keys())
        code = ColorPalettes.ANSI256Palette[closest]
        if is_background:
            return "\033[48;5;" + code + "m"
        else:
            return "\033[38;5;" + code + "m"

    @staticmethod
    def closest_from_palette(color: Color, palette: Collection[Color]):
        """
        Finds and returns the closest color in a given color palette. \n
        Note that this comparison does not take into account the alpha (transparency) channel.

        :param color: The color to match against.
        :param palette: The palette to choose output colors from.
        :return: The color in the given palette closest to the matching color, or None if palette is empty.
        """
        _closest_from_palette(color, palette)

#endregion Color Spaces


#region ======================== Module Functions ========================

def _closest_from_palette(color: Color, palette: Collection[Color]):
    """
    Finds and returns the closest color in a given color palette.

    Note that this comparison does not take into account the alpha (transparency) channel.

    :param color: The color to match against.
    :param palette: The palette to choose output colors from.
    :return: The color in the given palette closest to the matching color, or None if palette is empty.
    """

    def norm(*comp):
        return sum([x**2 for x in comp]) ** 0.5

    closest = None
    threshold = 255*3       # Maximum initial threshold
    for swatch in palette:
        # Computes the nearest neighbor to the target color within the provided palette using vector length.
        # 'deviation' is the vector length between the target color and all colors in the palette.
        deviation = norm(
            abs(color.r - swatch.r),
            abs(color.g - swatch.g),
            abs(color.b - swatch.b)
        )
        if deviation < threshold:
            closest = swatch
            threshold = deviation
    return closest

#endregion Module Functions
