from enum import Enum

from pytui.Color import ColorHandler
from System.Rendering.FragmentCanvas import FragmentCanvas
from Utils.ListHelper import longest_list_length


#region ======================== Border Styles ========================

class BorderStyle:

    def __init__(self, top_left: str, top_center: str, top_right: str,
                 middle_left: str, middle_right: str,
                 bottom_left: str, bottom_center: str, bottom_right: str):
        self.top_left = top_left
        self.top_center = top_center
        self.top_right = top_right
        self.middle_left = middle_left
        self.middle_right = middle_right
        self.bottom_left = bottom_left
        self.bottom_center = bottom_center
        self.bottom_right = bottom_right

        # Horizontal border texts
        self._title_top_left = None
        self._title_top_center = None
        self._title_top_right = None
        self._title_bottom_left = None
        self._title_bottom_center = None
        self._title_bottom_right = None
    
    def __eq__(self, other):
        return self.top_left == other.top_left and \
               self.top_center == other.top_center and \
               self.top_right == other.top_right and \
               self.middle_left == other.middle_left and \
               self.middle_right == other.middle_right and \
               self.bottom_left == other.bottom_left and \
               self.bottom_center == other.bottom_center and \
               self.bottom_right == other.bottom_right
    
    def __iter__(self):
        return iter((self.top_left, self.top_center, self.top_right,
                     self.middle_left, self.middle_right,
                     self.bottom_left, self.bottom_center, self.bottom_right))

    def __index__(self, index):
        return self.__iter__()[index]

    @property
    def title_top_left(self):
        return self._title_top_left
    @title_top_left.setter
    def title_top_left(self, value: str):
        self._title_top_left = str(value)

    @property
    def title_top_center(self):
        return self._title_top_center
    @title_top_center.setter
    def title_top_center(self, value: str):
        self._title_top_center = str(value)

    @property
    def title_top_right(self):
        return self._title_top_right
    @title_top_right.setter
    def title_top_right(self, value: str):
        self._title_top_right = str(value)

    @property
    def title_bottom_left(self):
        return self._title_bottom_left
    @title_bottom_left.setter
    def title_bottom_left(self, value: str):
        self._title_bottom_left = str(value)

    @property
    def title_bottom_center(self):
        return self._title_bottom_center
    @title_bottom_center.setter
    def title_bottom_center(self, value: str):
        self._title_bottom_center = str(value)

    @property
    def title_bottom_right(self):
        return self._title_bottom_right
    @title_bottom_right.setter
    def title_bottom_right(self, value: str):
        self._title_bottom_right = str(value)


class BorderTypes(Enum):
    """
    An 'enum' containing border types for drawing borders around components.

    The order for border characters follows suit:
    1) top left,
    2) top center,
    3) top right,
    4) middle left,
    5) middle right,
    6) bottom left,
    7) bottom center,
    8) bottom right.
    """

    NoBorder = BorderStyle(None, None, None, None, None, None, None, None)
    """ This forces the renderer to ignore border drawing. """

    BlankBorder = BorderStyle(" ", " ", " ", " ", " ", " ", " ", " ")

    ThinBorder = BorderStyle("┌", "─", "┐", "│", "│", "└", "─", "┘")

    ThinHorizontalBorder = BorderStyle("", "─", "", "", "", "", "─", "")

    ThinVerticalBorder = BorderStyle("", "", "", "│", "│", "", "", "")

    ThinUnderline = BorderStyle("", "", "", "", "", "", "─", "")

    ThinOverline = BorderStyle("", "─", "", "", "", "", "", "")

    DoubleThinBorder = BorderStyle("╔", "═", "╗", "║", "║", "╚", "═", "╝")

    MediumBorder = BorderStyle("┏", "━", "┓", "┃", "┃", "┗", "━", "┛")

    BlockBorder = BorderStyle("█", "▀", "█", "█", "█", "▀", "▀", "▀")

    BlockHorizontalBorder = BorderStyle("", "▀", "", "", "", "", "▀", "")

    BlockVerticalBorder = BorderStyle("", "", "", "█", "█", "", "", "")

    BlockOverline = BorderStyle("", "▀", "", "", "", "", "", "")

    BlockUnderline = BorderStyle("", "", "", "", "", "", "▀", "")

    DottedInnerBorder = BorderStyle("⢀", "⣀", "⡀", "⢸", "⡇", "⠈", "⠉", "⠁")

    DottedOuterBorder = BorderStyle("⡤", "⠤", "⢤", "⡇", "⢸", "⠓", "⠒", "⠚")

    DoubleDottedBorder = BorderStyle("⣤", "⣤", "⣤", "⣿", "⣿", "⠛", "⠛", "⠛")

    DoubleDottedBeveledBorder = BorderStyle("⣠", "⣤", "⣄", "⣿", "⣿", "⠙", "⠛", "⠋")

#endregion Border Styles


#region ======================== Border Compositing ========================

def create_border(width: int, height: int,
                  border: BorderStyle = BorderTypes.ThinBorder,
                  color: int | ColorHandler = 0xffffff) -> FragmentCanvas:
    """
    Creates a border FragmentCanvas of the specified size and style.

    :param width: The width of the border.
    :param height: The height of the border.
    :param border: The border style to use. Defaults to BorderTypes.ThinBorder.
    :param color: The color of the border. Defaults to 0xffffff.
    :return: A FragmentCanvas containing the border.
    """

    if width <= 0 or height <= 0:
        return FragmentCanvas.empty(width, height)
    elif width == 1:
        return FragmentCanvas.from_string(f"{border.middle_left}\n" * (height-1) + border.middle_left, fg_color=color)
    elif height == 1:
        return FragmentCanvas.from_string(border.top_center * width, fg_color=color)
    else:
        return FragmentCanvas(border.top_left + border.top_center * (width-2) + border.top_right + "\n" + \
                               (border.middle_left + " " * (width-2) + border.middle_right + "\n") * (height-2) + \
                               border.bottom_left + border.bottom_center * (width-2) + border.bottom_right)


def add_border_text(canvas: FragmentCanvas, text: str,
                    text_top_left: str = None, text_top_center: str = None, text_top_right: str = None,
                    text_bottom_left: str = None, text_bottom_center: str = None, text_bottom_right: str = None,
                    text_color: int | ColorHandler = 0xffffff) -> FragmentCanvas:
    """
    Adds text to a border canvas.
    This operation will overwrite any existing charxel on the canvas.

    The text can only be added to the horizontal top and bottom borders.

    :param canvas: The FragmentCanvas instance to draw the text on.
    :param text: The text to draw on the border.
    :param text_top_left: The text to draw on the top-left corner. Defaults to None.
    :param text_top_center: The text to draw on the top-center. Defaults to None.
    :param text_top_right: The text to draw on the top-right corner. Defaults to None.
    :param text_bottom_left: The text to draw on the bottom-left corner. Defaults to None.
    :param text_bottom_center: The text to draw on the bottom-center. Defaults to None.
    :param text_bottom_right: The text to draw on the bottom-right corner. Defaults to None.
    :param text_color: The color of the text. Defaults to 0xffffff.
    :return: The original FragmentCanvas with the text drawn on the specified sides of its border.
    """

    raise NotImplementedError("add_border_text is not implemented yet.")


def add_border(canvas: FragmentCanvas, border: BorderStyle = BorderTypes.ThinBorder, outer=True):
    """
    Adds a four-sided border around an component's canvas.

    :param canvas: The FragmentCanvas instance to draw the border on.
    :param border: The border preset to draw. Defaults to BorderTypes.ThinBorder.
    :param outer: Whether to draw the border as an outer contour to the component. If False, the border will draw over
        the outermost ring in the existing component.
    :return: The component's value with a border, in string.
    """

    # If the text is empty
    if canvas == "":
        canvas = " "
    buffer: list = str(canvas).splitlines(False)
    width: int = longest_list_length(buffer)

    # Insert side borders
    for lineindex in range(0, len(buffer)):
        linelength = len(buffer[lineindex])
        if linelength < width:
            # The line is not long enough. Add spaces after the line
            buffer[lineindex] = buffer[lineindex] + " "*(width-linelength)

        buffer[lineindex] = border[3] + buffer[lineindex] + border[4]

    # Insert top-and-bottom borders with corner pieces
    buffer = [border[0] + border[1] * width + border[2]] + \
             buffer + \
             [border[5] + border[6] * width + border[7]]

    # Delete empty horizontal borders
    if buffer[0] == "":
        del buffer[0]
    if buffer[-1] == "":
        del buffer[-1]

    return "\n".join(buffer)

#endregion Border Compositing
