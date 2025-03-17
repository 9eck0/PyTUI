"""
FragmentCanvas is the final abstraction layer of the rendering pipeline, representing the matrix of "character pixels,"
or "charxels" of a particular UI component, effectively analogous to the traditional rendering pipeline's fragment
processing step.

A charxel is composed of three pieces of data:
  - Character glyph of the charxel
  - Foreground color of the character glyph (32-bit ARGB integer)
  - Background color (32-bit ARGB integer)

If both the foreground and background colors are set to None, the charxel is reset to default terminal colors.

--------------------------------

All codes within this file must be written with performance optimization in mind, as this is part of the core UI
compositing process of PyTUI.
"""


from collections.abc import Sequence

from pytui.Color import ColorHandler, NamedColorList
from pytui.Utils.ListHelper import longest_list_length

empty_charxel = (' ', None, None)
""" The default charxel value, representing an empty glyph (space character) without custom color. """


class FragmentCanvas:

    # ================================ Instantiation ================================

    def __init__(self, width, height):
        self._width: int = 0
        """ When directly modifying the canvas, always update the internal _width and _height values. """
        self._height: int = 0
        """ When directly modifying the canvas, always update the internal _width and _height values. """
        self.canvas: list[list[tuple[str, int|None, int|None]]] = [[empty_charxel]]

        # Build empty canvas
        self.reinitialize(width, height)

    @staticmethod
    def from_string(string: str, fg_color: None | int = None, bg_color: None | int = None, sep: str = '\n'):
        """
        Creates a new FragmentCanvas from a string with empty color values.

        The width of the resulting canvas is determined by the length of the longest line in the string.
        All lines are left-justified with spaces to match the width of the longest line.

        :param string: The string to convert
        :param fg_color: An uniformly-filled foreground color to use for the resulting canvas
        :param bg_color: An uniformly-filled background color to use for the resulting canvas
        :param sep: The separator to use when splitting the string into lines
        :return: A new FragmentCanvas instance
        """
        fc = FragmentCanvas(0, 0)
        fc.canvas = FragmentCanvas._str_to_canvas(string, fg_color, bg_color, sep)
        fc._width = len(fc.canvas[0])
        fc._height = len(fc.canvas)
        return fc

    @staticmethod
    def empty(width: int, height: int):
        """ An empty FragmentCanvas without any additional properties. """
        return FragmentCanvas(width, height)

    # ================================ Magic Functions ================================

    def __iter__(self):
        return self.canvas.__iter__()
    
    # ================================ Internal Functions ================================

    @staticmethod
    def _str_to_charxels(string: str,
                         fg_color: None | int = None,
                         bg_color: None | int = None):
        return [(char, fg_color, bg_color) for char in string]

    @staticmethod
    def _str_to_canvas(string: str,
                       fg_color: None | int = None,
                       bg_color: None | int = None,
                       sep: str = '\n'):
        lines = string.split(sep)
        width = longest_list_length(lines)
        return [FragmentCanvas._str_to_charxels(line.ljust(width), fg_color, bg_color) for line in lines]

    # ================================ Methods ================================

    def draw(self, coords: tuple[int, int],
             content: "str | Sequence[Sequence[tuple[str, int, int]]] | FragmentCanvas",
             fg_color: None | int = None,
             bg_color: None | int = None,
             blend=False):
        """
        Draws over the current canvas, replacing a rectangular area with the content of another canvas.

        This function crops any region outside the borders of the current canvas.

        :param coords: The top-left corner of the new content's drawing area.
        :param content: The new content to draw.
        :param fg_color: Overrides the foreground color of the new content.
        :param bg_color: Overrides the background color of the new content.
        :param blend: Enables transparency passthrough, preserving existing charxel's foreground/background colors.
        """

        def is_empty_color(color):
            return color is None or color == NamedColorList.Transparent

        def blend_charxels(base, new):
            """
            Blending mode:
            Transparent
            """
            if new == empty_charxel:
                return base
            new_char = new[0][0]
            new_fg = new[1]
            new_bg = new[2]
            new_fg = base[1] if is_empty_color(new_fg) else new_fg
            new_bg = base[2] if is_empty_color(new_bg) else new_bg
            return new_char, new_fg, new_bg

        if isinstance(content, FragmentCanvas):
            content = content.canvas
        elif isinstance(content, str):
            content = FragmentCanvas._str_to_canvas(content, fg_color, bg_color)

        if content is None or len(content) == 0 or len(content[0]) == 0:
            return

        # Width (x) and height (y) ranges for cropping out-of-bounds drawing
        # Restrict content redrawing to the bounding box formed by below variables
        x0_min = max(0, coords[0])
        x0_max = min(self.width, coords[0] + len(content[0]))
        y0_min = max(0, coords[1])
        y0_max = min(self.height, coords[1] + len(content))
        # print(f"X0: {x0_min} - {x0_max}")
        # print(f"Y0: {y0_min} - {y0_max}")

        # Draw new content to current canvas
        for y0 in range(y0_min, y0_max):
            y1 = y0 - coords[1]     # y1 and x1 are the indices of the new content matrix
            for x0 in range(x0_min, x0_max):
                x1 = x0 - coords[0]
                to_draw = content[y1][x1]
                if to_draw[0] == "" or to_draw[0] is None:
                    # Since this is a textual UI, empty characters are prohibited.
                    to_draw = empty_charxel
                if blend:
                    to_draw = blend_charxels(self.canvas[y0][x0], to_draw)
                self.canvas[y0][x0] = to_draw

    def reinitialize(self, width, height):
        self._width = max(0, width)
        self._height = max(0, height)
        # Build empty canvas
        self.canvas = [[empty_charxel] * self._width] * self._height
    
    def to_string(self, sep: str = '\n'):
        return sep.join([''.join([charxel[0] for charxel in row]) for row in self.canvas])

    # ================================ Properties ================================

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        delta = value - self._height
        if delta > 0:
            # Append empty charxels to width
            for i_row in self.canvas:
                i_row += [empty_charxel] * delta
        elif delta < 0:
            # Truncate canvas width
            for j in range(len(self.canvas)):
                i_row = self.canvas[j]
                i_truncate_to = max(0, len(i_row)+delta)
                self.canvas[j] = i_row[0:i_truncate_to]
        self._width = value

    @property
    def height(self):
        return self._width

    @height.setter
    def height(self, value):
        delta = value - self._height
        if delta > 0:
            # Append empty charxel rows to height
            for _ in range(delta):
                self.canvas.append([empty_charxel]*self._width)
        elif delta < 0:
            # Shorten canvas height/rows
            i_truncate_to = max(0, len(self.canvas) + delta)
            self.canvas = self.canvas[0:i_truncate_to]
        self._height = value

    # ================================ Static Functions ================================

