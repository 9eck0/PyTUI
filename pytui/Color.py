"""
Color structure and color palettes.

The ColorHelper class is written with the goal of performance in mind, as coloring is an integral part of the rendering
pipeline, with thousands of operations per draw on a commonly mid-sized canvas, affecting performance and responsiveness
in a not insignificant manner.

As such, this class does not necessarily adhere to some fundamental principles of software engineering, such as
DRY (don't repeat yourself), where duplicate code is used to alleviate performance cost of function calls and object
instancing.

Color is stored inside ColorHelper as an int value, and operations performed directly modifies the integer, hence the
naming of this class. This is done partly to allude to the fact colors are stored in memory as int values (to optimize
the number of transient object instances kept in memory across a handful of canvases), and partly to respect the
ethos of performant code, as storing separate channel values possess a performance cost across the average of operations
(in the order of 10-20% for instancing methods).

Additional optimizations are possible, such as using a LUT for costly operations, which are to be considered only once
this project reaches a stable developmental level down the road.
"""


#========================Imports========================

# No dependency
from enum import Enum
from typing import Collection

from Utils.MathHelper import clamp, norm


#region ======================== ColorHandler ========================

class ColorHandler:
    """
    Handles color code conversions and operations.

    Color codes are in hexadecimal ARGB format, with alpha channel as the first byte.
    The 'value' property contains the resulting color code in int.
    """

    MAX_VALUE = 255

    # ================ Instantiation ================

    def __init__(self, color_code: int):
        """
        Initializes a ColorHandler instance with a color code in ARGB format.

        :param color_code: A color code in hexadecimal ARGB format.
        """
        self.value: int = int(color_code)
        """ The resulting color code, in ARGB format. """

    @staticmethod
    def from_ARGB(r: int, g: int, b: int, a: int = MAX_VALUE):
        """
        Instantiates a ColorHandler instance from ARGB components.

        :param r: The red channel of the color, from 0 to 255.
        :param g: The green channel of the color, from 0 to 255.
        :param b: The blue channel of the color, from 0 to 255.
        :param a: The alpha channel of the color, from 0 to 255.
        :return: A ColorHandler instance.
        """

        # Value range checks are inlined to avoid function call performance penalty
        if r < 0 or r > ColorHandler.MAX_VALUE:
            raise ValueError(f"Value for red channel must be between 0 and {ColorHandler.MAX_VALUE}.")
        if g < 0 or g > ColorHandler.MAX_VALUE:
            raise ValueError(f"Value for green channel must be between 0 and {ColorHandler.MAX_VALUE}.")
        if b < 0 or b > ColorHandler.MAX_VALUE:
            raise ValueError(f"Value for blue channel must be between 0 and {ColorHandler.MAX_VALUE}.")
        if a < 0 or a > ColorHandler.MAX_VALUE:
            raise ValueError(f"Value for alpha channel must be between 0 and {ColorHandler.MAX_VALUE}.")
        return ColorHandler((a << 24) | (r << 16) | (g << 8) | b)
    
    @staticmethod
    def from_html_code(hex_string: str):
        """
        Instantiates a ColorHandler instance from an HTML hexadecimal code.
        The format must either be #RGB, #RGBA, #RRGGBB or #RRGGBBAA

        :param hex_string: HTML hexadecimal color code, either in shorthand or longhand form, with optional alpha value.
        :return: A ColorHandler instance.
        """
        hex_string = hex_string.strip()

        if hex_string[0] == '#':
            hex_string = hex_string[1:]

        match len(hex_string):
            case 3:
                # Shorthand RBG format
                return ColorHandler.from_ARGB(
                    int(2*hex_string[1], 16),
                    int(2*hex_string[2], 16),
                    int(2*hex_string[3], 16))
            case 4:
                # Shorthand RBGA format
                return ColorHandler.from_ARGB(
                    int(2*hex_string[1], 16),
                    int(2*hex_string[2], 16),
                    int(2*hex_string[3], 16),
                    int(2*hex_string[4], 16))
            case 6:
                # Longhand RRGGBB format
                return ColorHandler.from_ARGB(
                    int(hex_string[1:3], 16),
                    int(hex_string[3:5], 16),
                    int(hex_string[5:7], 16))
            case 8:
                # Longhand RRGGBBAA format
                return ColorHandler.from_ARGB(
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

        The RGB values are returned within the sRGB color space.

        :param hue: An angular value between 0 and 360.
        :param saturation: Color richness, normalized between 0 (white) and 1.
        :param value: Color presence/brightness, normalized between 0 (black) and 1.
        :return:
        :rtype: Color
        """

        # Formula (alternative): https://en.wikipedia.org/wiki/HSL_and_HSV#To_RGB

        def f(n):
            k = (n + hue/60) % 6
            return value - value * saturation * max(0, min(k, 4-k, 1))

        return ColorHandler.from_ARGB(
            int(round(f(5) * ColorHandler.MAX_VALUE)),
            int(round(f(3) * ColorHandler.MAX_VALUE)),
            int(round(f(1) * ColorHandler.MAX_VALUE))
        )
    
    @staticmethod
    def empty():
        """ A ColorHandler instance with all channels set to 0. """
        return ColorHandler(0)

    # ================ Magic Methods ================
    
    def __eq__(self, other):
        return self.value == other.value

    def __add__(self, other):
        return ColorHandler.from_ARGB(
            max(0, min(ColorHandler.MAX_VALUE, self.r + other.r)),
            max(0, min(ColorHandler.MAX_VALUE, self.g + other.g)),
            max(0, min(ColorHandler.MAX_VALUE, self.b + other.b)),
            max(0, min(ColorHandler.MAX_VALUE, self.a + other.a))
        )
    
    def __iadd__(self, other):
        self.r = max(0, min(ColorHandler.MAX_VALUE, self.r + other.r))
        self.g = max(0, min(ColorHandler.MAX_VALUE, self.g + other.g))
        self.b = max(0, min(ColorHandler.MAX_VALUE, self.b + other.b))
        self.a = max(0, min(ColorHandler.MAX_VALUE, self.a + other.a))
        return self
        
    def __sub__(self, other):
        return ColorHandler.from_ARGB(
            max(0, min(ColorHandler.MAX_VALUE, self.r - other.r)),
            max(0, min(ColorHandler.MAX_VALUE, self.g - other.g)),
            max(0, min(ColorHandler.MAX_VALUE, self.b - other.b)),
            max(0, min(ColorHandler.MAX_VALUE, self.a - other.a))
        )
    
    def __isub__(self, other):
        self.r = max(0, min(ColorHandler.MAX_VALUE, self.r - other.r))
        self.g = max(0, min(ColorHandler.MAX_VALUE, self.g - other.g))
        self.b = max(0, min(ColorHandler.MAX_VALUE, self.b - other.b))
        self.a = max(0, min(ColorHandler.MAX_VALUE, self.a - other.a))
        return self
    
    def __and__(self, other):
        if isinstance(other, ColorHandler):
            return ColorHandler(self.value & other.value)
        else:
            return self.value & int(other)
    
    def __or__(self, other):
        if isinstance(other, ColorHandler):
            return ColorHandler(self.value | other.value)
        else:
            return self.value | int(other)
    
    def __xor__(self, other):
        if isinstance(other, ColorHandler):
            return ColorHandler(self.value ^ other.value)
        else:
            return self.value ^ int(other)
    
    def __hash__(self):
        return hash(self.value)
    
    def __int__(self):
        return self.value
    
    def __hex__(self):
        return hex(self.value)

    def __repr__(self):
        return hex(self.value)
    
    def __str__(self):
        return "ColorHandler(r={0}, g={1}, b={2}, a={3})".format(self.r, self.g, self.b, self.a)
    
    def __copy__(self):
        return ColorHandler(self.value)

    # ================ Properties ================

    @property
    def r(self):
        """ The red channel of the color, from 0 to 255. """
        return (self.value >> 16) & 0xFF

    @r.setter
    def r(self, value: int):
        """ The red channel of the color, from 0 to 255. """
        if value < 0 or value > ColorHandler.MAX_VALUE:
            raise ValueError("Value for red channel must be between 0 and 255.")
        self.value = (self.value & 0xFF00FFFF) | (value & 0xFF) << 16

    @property
    def g(self):
        """ The green channel of the color, from 0 to 255. """
        return (self.value >> 8) & 0xFF

    @g.setter
    def g(self, value: int):
        """ The green channel of the color, from 0 to 255. """
        if value < 0 or value > ColorHandler.MAX_VALUE:
            raise ValueError("Value for green channel must be between 0 and 255.")
        self.value = (self.value & 0xFFFF00FF) | (value & 0xFF) << 8

    @property
    def b(self):
        """ The blue channel of the color, from 0 to 255. """
        return self.value & 0xFF

    @b.setter
    def b(self, value: int):
        """ The blue channel of the color, from 0 to 255. """
        if value < 0 or value > ColorHandler.MAX_VALUE:
            raise ValueError("Value for blue channel must be between 0 and 255.")
        self.value = (self.value & 0xFFFFFF00) | (value & 0xFF)

    @property
    def a(self):
        """ The alpha channel of the color, from 0 to 255. """
        return (self.value >> 24) & 0xFF
    
    @a.setter
    def a(self, value: int):
        """ The alpha channel of the color, from 0 to 255. """
        if value < 0 or value > ColorHandler.MAX_VALUE:
            raise ValueError("Value for alpha channel must be between 0 and 255.")
        self.value = (self.value & 0x00FFFFFF) | (value & 0xFF) << 24

    # ================ Conversions ================

    def grayscale(self, method: str = "luminance") -> "ColorHandler":
        """
        Returns a new ColorHelper instance representing the grayscale transformation of this color.
        This conversion preserves the alpha channel's value.

        --------------------------------

        Different grayscale conversion methods (algorithms) are available to choose from, each with its own trade-offs.
        Below is a breakdown of each method, its string parameter value, and a brief explanation of their effects:

        - luma: Default option (also in case of invalid parameterization).
          Relatively performant (requiring 5 calculations) and yields good results.
          Follows the BT.601 luma curve without performing color space conversion.

        - luminance:
          Slowest, yields the best result.
          Follows the gamma expansion curve set by BT.701 of the CIE 1931 standard's sRGB color space. This restores
          the original linear luminance of an image before sRGB gamma compression, creating a grayscale which closely
          matches the image's relative luminance as perceived by the trichromatic human eyes.

        - average: Outputs the average of RGB channels as grayscale channel.
          Fast to process (4 calculations), but tends to misrepresent shades of gray correctly to the human vision.

        - green: Simplest conversion method - casts the green channel as the grayscale channel.
          Fastest method (1 operation), optimal for generating thumbnail previews of photographic images.
          In nature, the green channel dominates the visible spectrum output of the Sun, more closely correlating with
          a scene's true luminance value compared to the red and blue channels.
          Consequently, this method performs poorly on tinted or artificial images, and is not recommended for any
          serious rendering intent.
        """

        match method:
            case "average":
                gray = int((self.r + self.g + self.b) / 3.0)
                return ColorHandler.from_ARGB(gray, gray, gray, self.a)
            case "green":
                return ColorHandler.from_ARGB(self.g, self.g, self.g, self.a)
            case "luminance":
                # Algorithm: https://en.wikipedia.org/wiki/Grayscale#Colorimetric_(perceptual_luminance-preserving)_conversion_to_grayscale
                def linearize(value):
                    value = value / ColorHandler.MAX_VALUE
                    return value/12.92 if value <= 0.04045 else ((value+0.055)/1.055)**2.4
                gray = 0.2126 * linearize(self.r) + 0.7152 * linearize(self.g) + 0.0722 * linearize(self.b)
                gray = int(ColorHandler.MAX_VALUE * gray)
                return ColorHandler.from_ARGB(gray, gray, gray, self.a)
            case _:     # luma
                #Algorithm: https://en.wikipedia.org/wiki/Grayscale#Luma_coding_in_video_systems
                gray = int(0.3 * self.r + 0.59 * self.g + 0.11 * self.b)
                return ColorHandler.from_ARGB(gray, gray, gray, self.a)

    def to_html_code(self, include_alpha=False):
        """
        Converts this color into its corresponding HTML color code representation.

        :param include_alpha: Whether the alpha channel is included into the hexadecimal code.
        :return: a string containing the HTML color code
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

        unit_r = self.r / float(ColorHandler.MAX_VALUE)
        unit_g = self.g / float(ColorHandler.MAX_VALUE)
        unit_b = self.b / float(ColorHandler.MAX_VALUE)
        v_max = max(unit_r, unit_g, unit_b)     # a.k.a. Value
        v_min = min(unit_r, unit_g, unit_b)
        chroma = v_max - v_min

        if chroma == 0:
            hue = 0
        elif v_max == unit_r:
            hue = 60 * (unit_g - unit_b) / chroma
        elif v_max == unit_g:
            hue = 60 * (2 + (unit_b - unit_r) / chroma)
        else:   # v_max == unit_b
            hue = 60 * (4 + (unit_r - unit_g) / chroma)

        if v_max == 0:
            saturation = 0
        else:
            saturation = chroma / v_max
        
        return hue, saturation, v_max
    
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
            return "\033[48;2;" + str(self.r) + ";" + str(self.g) + ";" + str(self.b) + "m"
        else:
            return "\033[38;2;" + str(self.r) + ";" + str(self.g) + ";" + str(self.b) + "m"
    
    # ================ Manipulations ================
    
    def blend(self, other: "ColorHandler", ratio: float):
        """
        Blends the current color with another color by a given ratio.

        :param other: The other color to blend with.
        :param ratio: The ratio of the first color to the second color in the blend, between 0 and 1.
        :return: A new color that is the blend of the two given colors.
        :rtype: ColorHandler
        """
        return ColorHandler.blend_colors(self, other, ratio)

    def invert(self):
        """
        Performs in-place inversion of the current color.
        """
        self.r = ColorHandler.MAX_VALUE - self.r
        self.g = ColorHandler.MAX_VALUE - self.g
        self.b = ColorHandler.MAX_VALUE - self.b
        return self
    
    def scale_exposure(self, factor: float):
        """
        Uniformly scales the red, green, and blue channels by the given factor.
        This operation mostly affects the highlights of an image.

        Channel values are clamped between 0 and 255, resulting in white clipping when the scaling factor is high.

        NOTE: The scaling is in-place and non-reversible.

        :param factor: A positive or negative value that specifies the scaling factor.
        """
        # Inlined MathHelper.clamp() to reduce cost of method calls
        self.r = int(min(max(0.0, self.r * factor), ColorHandler.MAX_VALUE))
        self.g = int(min(max(0.0, self.g * factor), ColorHandler.MAX_VALUE))
        self.b = int(min(max(0.0, self.b * factor), ColorHandler.MAX_VALUE))
        return self
    
    def superpose(self, other: "ColorHandler"):
        """
        Superposes the current color on top of another color based on the alpha channel.

        :param other: The bottom color to blend the current color on top of.
        :return: A new color that is the superposition of the two given colors.
        :rtype: ColorHandler
        """
        return ColorHandler.blend_colors(self, other, ratio=self.a / float(ColorHandler.MAX_VALUE))
    
    # ================ Static Methods ================

    @staticmethod
    def get_color_from_argb(r: int, g: int, b: int, a: int = MAX_VALUE):
        """
        Obtains a color code from ARGB values.

        :param r: The red channel of the color, from 0 to 255.
        :param g: The green channel of the color, from 0 to 255.
        :param b: The blue channel of the color, from 0 to 255.
        :param a: The alpha channel of the color, from 0 to 255.
        :return: A color code in ARGB format.
        :rtype: int
        """

        # Value range checks are inlined to avoid function call performance penalty
        if r < 0 or r > ColorHandler.MAX_VALUE:
            raise ValueError("Value for red channel must be between 0 and 255.")
        if g < 0 or g > ColorHandler.MAX_VALUE:
            raise ValueError("Value for green channel must be between 0 and 255.")
        if b < 0 or b > ColorHandler.MAX_VALUE:
            raise ValueError("Value for blue channel must be between 0 and 255.")
        if a < 0 or a > ColorHandler.MAX_VALUE:
            raise ValueError("Value for alpha channel must be between 0 and 255.")
        return (a << 24) | (r << 16) | (g << 8) | b
    
    @staticmethod
    def blend_colors(color1: "ColorHandler", color2: "ColorHandler", ratio: float):
        """
        Blends two colors together by a given ratio.

        :param color1: The first color
        :param color2: The second color
        :param ratio: The ratio of the first color to the second color in the blend, between 0 and 1
        :return: A new color that is the blend of the two given colors
        :rtype: ColorHandler
        """

        scale1 = clamp(0.0, ratio, 1.0)
        scale2 = clamp(0.0, 1.0 - ratio, 1.0)
        return color1.scale_exposure(scale1) + color2.scale_exposure(scale2)

    @staticmethod
    def int_to_ansi24(color_code: int, is_background: bool = False):
        """
        Converts a hexadecimal color code into ANSI-ES terminal color code.

        :param is_background: False to output text character color, True to output text background color.
        :return: A properly formatted 24-bit ANSI-ES color code.
        :rtype: str
        """

        a, r, g, b = (color_code >> 24) & 0xFF, (color_code >> 16) & 0xFF, (color_code >> 8) & 0xFF, color_code & 0xFF
        if is_background:
            if a == 0:
                # Reset
                return "\033[39m"
            return "\033[48;2;" + str(r) + ";" + str(g) + ";" + str(b) + "m"
        else:
            return "\033[38;2;" + str(r) + ";" + str(g) + ";" + str(b) + "m"

#endregion Color


#region ======================== Color Spaces ========================

class NamedColorList(Enum):
    """
    A class/enum containing a list of common named colors.
    """
    
    Default     = None
    """ This value is used by PyTUI to reset color formatting to default terminal colors. """
    Transparent = 0x00000000    # Fully transparent

    # Grayscale colors
    Black       = 0xFF000000    # RGB(0, 0, 0)
    DarkGray    = 0xFF404040    # RGB(64, 64, 64)
    Gray        = 0xFF808080    # RGB(128, 128, 128)
    LightGray   = 0xFFC0C0C0    # RGB(192, 192, 192)
    White       = 0xFFFFFFFF    # RGB(255, 255, 255)

    # Spectral color ordering
    DarkRed     = 0xFF8B0000    # RGB(139, 0, 0)
    Brown       = 0xFFA52A2A    # RGB(165, 42, 42)
    Red         = 0xFFFF0000    # RGB(255, 0, 0)
    OrangeRed   = 0xFFFF4500    # RGB(255, 69, 0)
    Orange      = 0xFFFFA500    # RGB(255, 165, 0)
    Gold        = 0xFFFFD700    # RGB(255, 215, 0)
    Yellow      = 0xFFFFFF00    # RGB(255, 255, 0)
    YellowGreen = 0xFF9ACD32    # RGB(154, 205, 50)
    Green       = 0xFF00FF00    # RGB(0, 255, 0)
    DarkGreen   = 0xFF008000    # RGB(0, 128, 0)
    Cyan        = 0xFF00FFFF    # RGB(0, 255, 255)
    LightBlue   = 0xFFADD8E6    # RGB(173, 216, 230)
    Blue        = 0xFF0000FF    # RGB(0, 0, 255)
    DarkBlue    = 0xFF00008B    # RGB(0, 0, 139)
    Indigo      = 0xFF4B0082    # RGB(75, 0, 130)
    Purple      = 0xFF800080    # RGB(128, 0, 128)
    Magenta     = 0xFFFF00FF    # RGB(255, 0, 255)
    Pink        = 0xFFFFC0CB    # RGB(255, 192, 203)
    Beige       = 0xFFF5F5DC    # RGB(245, 245, 220)

    @staticmethod
    def get_name(color: int):
        """
        Obtains a readable color name based on similarity to the NamedColorList palette.
        :param color: The integer ARGB color value.
        :return: The name of the closest matching color in the NamedColorList palette.
            If the provided palette is empty, returns the string representation of its ARGB value.
        :rtype: str
        """
        colors = {key: value for key, value in NamedColorList.__dict__.items() if
                  isinstance(value, int) and not key.startswith('_')}

        closestColor = color.closest_from_palette(list(colors.values()))

        col_name = repr(closestColor)
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
        0xFF000000: 30,     # Black     (0, 0, 0)
        0xFFAA0000: 31,     # Red       (170, 0, 0)
        0xFF00AA00: 32,     # Green     (0, 170, 0)
        0xFFAA5500: 33,     # Yellow    (170, 85, 0)
        0xFF0000AA: 34,     # Blue      (0, 0, 170)
        0xFFAA00AA: 35,     # Magenta   (170, 0, 170)
        0xFF00AAAA: 36,     # Cyan      (0, 170, 170)
        0xFFC0C0C0: 37      # White     (192, 192, 192)
    }
    """ The 8 minimum colors supported by all ANSI-ES enabled terminals.
        This dictionary corresponds Colors with their respective ANSI foreground color number. """

    ANSI4Palette = {
        # ESC 30 to 37
        0xFF000000: 30,     # Standard black    (0, 0, 0)
        0xFFAA0000: 31,     # Standard red      (170, 0, 0)
        0xFF00AA00: 32,     # Standard green    (0, 170, 0)
        0xFFAA5500: 33,     # Standard yellow   (170, 85, 0)
        0xFF0000AA: 34,     # Standard blue     (0, 0, 170)
        0xFFAA00AA: 35,     # Standard magenta  (170, 0, 170)
        0xFF00AAAA: 36,     # Standard cyan     (0, 170, 170)
        0xFFC0C0C0: 37,     # Standard white    (192, 192, 192)
        # ESC 90 to 97
        0xFF808080: 90,     # Bright black (gray)   (128, 128, 128)
        0xFFFF0000: 91,     # Bright red        (255, 0, 0)
        0xFF00FF00: 92,     # Bright green      (0, 255, 0)
        0xFFFFFF00: 93,     # Bright yellow     (255, 255, 0)
        0xFF0000FF: 94,     # Bright blue       (0, 0, 255)
        0xFFFF00FF: 95,     # Bright magenta    (255, 0, 255)
        0xFF00FFFF: 96,     # Bright cyan       (0, 255, 255)
        0xFFFFFFFF: 97      # Bright white      (255, 255, 255)
    }
    """ 4 bit color palette present in the minimal ANSI-ES specification.\n
        30-37: Background colors.\n
        90-97: Foreground colors. """

    # To be generated at the end of module declaration using _generate_ansi256()
    ANSI256Palette = None
    """ The standard 8-bit 256-color palette supported by the majority of ANSI-ES enabled terminals.\n
        0-15: Standard 16 colors.\n
        16-231: Gradient colors in a 6x6x6 cube.\n
        232-255: Grayscale in 24 steps. """

    IdlePalette = {
        0xFF0000FF: 'stdout',       # Blue       (0, 0, 255)
        0xFF000000: 'SYNC',         # Black      (0, 0, 0)
        0xFFDD0000: 'COMMENT',      # Red        (221, 0, 0)
        0xFFFF7700: 'KEYWORD',      # Orange     (255, 119, 0)
        0xFF00AA00: 'STRING',       # Green      (0, 170, 0)
        0xFF0000FF: 'DEFINITION',   # Blue       (0, 0, 255)
        0xFF900090: 'BUILTIN',      # Purple     (144, 0, 144)
        0xFF770000: 'console',      # Brown      (119, 0, 0)
        0xFFFF0000: 'stderr'        # Red        (255, 0, 0)
    }
    """
    IdlePalette dictionary corresponds IDLE terminal's default color scheme
    to their RGB values.
    """

    @staticmethod
    def to_idle(color: ColorHandler):
        """
        Converts a color to the closest looking color code in IDLE's color palette.

        :param color: The Color instance to find an IDLE match for.
        :return: A string code for IDLE shell color printing.
        :rtype: str
        """
        # Since color distribution in IDLE's palette is limited,
        # there needs to be a bias towards less prevalent colors (e.g. green)
        colorBias = ColorHandler.from_ARGB(int(color.r * 0.5), color.g, int(color.b * 0.75))
        closestColor = _closest_from_palette(colorBias, ColorPalettes.IdlePalette.keys())
        return ColorPalettes.IdlePalette[closestColor]

    @staticmethod
    def to_ansi4_code(fg_color: int = None, bg_color: int = None):
        """
        Converts a color to the closest looking ANSI-ES 4-bit color code.

        If both foreground and background colors are set to None, this function outputs the default
        terminal coloring as an ANSI color reset code.

        :param fg_color: Foreground text color. Can be None to modify only the background.
        :param bg_color: Background color. Can be None to modify only the foreground.
        :return: A properly formatted ANSI-ES 4-bit color code.
        :rtype: str
        """

        if fg_color is None and bg_color is None:
            # Output color reset code (TODO may not work on some terminals, requires testing)
            return "\033[39;49"

        fg_closest = _closest_from_palette(fg_color, ColorPalettes.ANSI4Palette.keys())
        bg_closest = _closest_from_palette(bg_color, ColorPalettes.ANSI4Palette.keys())

        if fg_color is None:
            bg_code = ColorPalettes.ANSI4Palette[bg_closest] + 10
            return "\033[" + bg_code + "m"
        elif bg_color is None:
            fg_code = ColorPalettes.ANSI4Palette[fg_closest]
            return "\033[" + fg_code + "m"
        else:
            fg_code = ColorPalettes.ANSI4Palette[fg_closest]
            bg_code = ColorPalettes.ANSI4Palette[bg_closest] + 10
            return "\033[" + fg_code + ";" + bg_code + "m"

    @staticmethod
    def to_ansi256_code(color: int, is_background=False):
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
    def closest_from_palette(color: int, palette: Collection[int]):
        """
        Finds and returns the closest color in a given color palette. \n
        Note that this comparison does not take into account the alpha (transparency) channel.

        :param color: The color to match against.
        :param palette: The palette to choose output colors from.
        :return: The color in the given palette closest to the matching color, or None if palette is empty.
        :rtype: int
        """
        return _closest_from_palette(color, palette)

#endregion Color Spaces


#region ======================== Module Functions ========================

def _closest_from_palette(color: int, palette: Collection[int]):
    """
    [Internal function]
    Please use the equivalent function within the ColorPalettes class.

    Finds and returns the closest color in a given color palette.

    Note that this comparison does not take into account the alpha (transparency) channel.

    :param color: The color to match against.
    :param palette: The palette to choose output colors from.
    :return: The color in the given palette closest to the matching color, or None if palette is empty.
    :rtype: int
    """

    if color is None:
        return None

    target = ColorHandler(color)
    match = None
    threshold = 255*3       # Maximum initial threshold
    for color_code in palette:
        # Computes the nearest neighbor to the target color within the provided palette using vector length.
        # 'deviation' is the vector length between the target color and all colors in the palette.
        swatch = ColorHandler(color_code)
        deviation = norm(
            abs(target.r - swatch.r),
            abs(target.g - swatch.g),
            abs(target.b - swatch.b)
        )
        if deviation < threshold:
            match = swatch
            threshold = deviation
    return match.value


def _generate_ansi256():
    """
    [Internal function]
    Generates the ANSI256Palette dictionary with 256 colors.
    """

    # 0-15 are same as ANSI 4-bit palette
    palette = ColorPalettes.ANSI4Palette.copy() 

    i = 16
    vals = (0, 95, 135, 175, 215, 255)

    # 6*6*6 cube gradient: 16 + 36 × r + 6 × g + b (0 ≤ r, g, b ≤ 5)
    for r in vals:
        for g in vals:
            for b in vals:
                palette[ColorHandler.get_color_from_argb(r, g, b)] = i
                i += 1
    
    # Grayscale in 24 steps (excluding pure black and white)
    for v in range(8, 239, 10):
        palette[ColorHandler.get_color_from_argb(v, v, v)] = i
        i += 1
    
    return palette

ColorPalettes.ANSI256Palette = _generate_ansi256()

#endregion Module Functions
