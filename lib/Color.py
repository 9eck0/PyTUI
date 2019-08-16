"""
Color definitions, color spaces
"""

if __name__ == "__main__":
    # MAJOR +1 represents an added function.
    __MAJOR = 1
    # MINOR +1 represents a change in existing function(s) within the current MAJOR.
    __MINOR = 0

    __info = """This file contains the module 'Color', used to integrate color systems into Python.
To use this module in another project, include this file inside the project's directory."""

    print("========================================================")
    print("Color.py version ", __MAJOR, ".", __MINOR, sep='', end='\n\n')
    print(__info)
    print("========================================================\n")
    input("Press enter to continue...")



#========================Imports========================

# No dependency



#========================Color========================

class Color:

    def __init__(self, r: int, g: int, b: int, a: int = 1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __eq__(self, other):
        return (self.r, self.g, self.b, self.a) == (other.r, other.g, other.b, other.a)

    def __repr__(self):
        return Color.tostring(self)

    def __str__(self):
        return ColorList.getName(self)

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        if value > 255:
            self._r = 255
        elif value < 0:
            self._r = 0
        else:
            self._r = int(value)

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, value: int):
        if value > 255:
            self._g = 255
        elif value < 0:
            self._g = 0
        else:
            self._g = int(value)

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        if value > 255:
            self._b = 255
        elif value < 0:
            self._b = 0
        else:
            self._b = int(value)

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        if value > 1.0:
            self._a = 1.0
        elif value < 0:
            self._a = 0
        else:
            self._a = int(value)

    def toHex(self):
        """
        Converts this color into a human-readable hexadecimal color code.

        Returns:
            a string representation of this color in hexadecimal format
        """

        return '#%02x%02x%02x' % (self.r, self.g, self.b)

    def toRgbaHex(self):
        """
        Converts this color into its corresponding hexadecimal color code with alpha channel included.

        Returns:
            a string representation of this color, including its alpha value, in hexadecimal format
        """

        return '#%02x%02x%02x%02x' % (self.r, self.g, self.b, self.a * 256)

    @staticmethod
    def tostring(color):
        return "Color(R=" + str(color.r) + ", G=" + str(color.g) + ", B=" + str(color.b) + ", A=" + str(color.a) + ")"



#========================ColorSpaces========================

class ColorList:
    """
    A class/enum containing a list of common colors.
    """

    Black = Color(0, 0, 0)
    DarkGray = Color(64, 64, 64)
    Gray = Color(128, 128, 128)
    LightGray = Color(192, 192, 192)
    White = Color(255, 255, 255)

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
    def getName(color: Color):
        colors = {key: value for key, value in ColorList.__dict__.items() if
                  type(value) is Color}

        closestColor = closestFromPalette(color, list(colors.values()))

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



#========================Module Functions========================

IdlePalette = {'stdout': Color(0, 0, 255),
               'SYNC': Color(0, 0, 0),
               'COMMENT': Color(221, 0, 0),
               'KEYWORD': Color(255, 119, 0),
               'STRING': Color(0, 170, 0),
               'DEFINITION': Color(0, 0, 255),
               'BUILTIN': Color(144, 0, 144),
               'console': Color(119, 0, 0),
               'stderr': Color(255, 0, 0)}


def closestFromPalette(color: Color, palette: list):
    workingPalette = palette.copy()
    closest = workingPalette.pop()
    threshold = 255*4
    for swatch in workingPalette:
        deltasum = abs((color.r - swatch.r) + (color.g - swatch.g) + (color.b - swatch.b) + (color.a * 255 - swatch.a * 255))
        if deltasum < threshold:
            closest = swatch
            threshold = deltasum
    return closest


def toIdle(color: Color):
    """
    Convert a color to the closest looking color in IDLE's color palette.

    Returns:
        a string for IDLE shell color printing
    """
    # Since color distribution in IDLE's palette is limited, there needs to be a bias towards less prevalent colors (e.g. green)
    biased = Color(int(color.r * 0.5), color.g, int(color.b * 0.75))
    reversePalette = {x: y for y, x in IdlePalette.items()}
    return reversePalette[closestFromPalette(biased, list(IdlePalette.values()))]



#========================Version History========================

# 1.0
"""
    Initial Release
    Event system for detecting when a ShellGUI component lost focus.

    Additions
    ---------
        -class KeyPressEventArgs implements EventArgs
            -__init__(self, key, **kwargs)
        -class _KeyPressEventListener implements EventListener
            -__init__(self, *subscribers)
            -notify(self, sender, key)
        -class KeyPressEventHandler implements EventHandler
            -__init__(self, *subscribers)
            -readkey(self)
            -class UnixKeyPress
                -__init__(self)
                -__call__(self)
            -class WindowsKeyPress
                -__init__(self)
                -__call__(self)
        -class KeyCodes
            -Defined constants (under this class) for all latin1 unicode characters
            -CombinationCharacters dictionary for special keyboard functions that cannot be represented as a single
             Unicode character
            -static tostring(key1: bytes, key2: bytes)
"""