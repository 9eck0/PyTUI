"""
How ShellGUI works:
'Canvas' is a class representing the GUI area drawn with ASCII method.
Each GUI element is a class inherited from 'Component' class. They need to be drawn onto a canvas.
X and Y positions are specified inside each GUI element's class;
Z position is specified inside Canvas class, within a dictionary.
"""

if __name__ == "__main__":
    # MAJOR +1 represents an added function.
    __MAJOR = 1
    # MINOR +1 represents a change in existing function(s) within the current MAJOR.
    __MINOR = 0 + 1

    __info = """This file contains the module 'ShellGUI_Core', used to create a shell-based rendering engine.
To use this module in another project, include this file inside the project's directory."""

    print("========================================================")
    print("ShellGUI_Core.py version ", __MAJOR, ".", __MINOR, sep='', end='\n\n')
    print(__info)
    print("========================================================\n")
    input("Press enter to continue...")



#========================Imports========================

# Used by: Canvas.draw()
import time

from lib.Utils import *
from lib.Color import Color

from lib.EventSystem.FocusLost import FocusLostEventListener
from lib.EventSystem.KeyPress import *
from lib.EventSystem.OnFocus import OnFocusEventListener



#========================Borders========================

class BorderTypes:
    """
    An 'enum' containing border types for drawing borders around components.
    """

    NoBorder = ("", "", "", "", "", "", "", "")
    
    BlankBorder = (" ", " ", " ", " ", " ", " ", " ", " ")

    ThinBorder = ("┌", "─", "┐", "│", "│", "└", "─", "┘")

    ThinHorizontalBorder = ("", "─", "", "", "", "", "─", "")

    ThinVerticalBorder = ("", "", "", "│", "│", "", "", "")

    ThinUnderline = ("", "", "", "", "", "", "─", "")

    ThinOverline = ("", "─", "", "", "", "", "", "")

    BlockBorder = ("█", "▀", "█", "█", "█", "▀", "▀", "▀")

    BlockHorizontalBorder = ("", "▀", "", "", "", "", "▀", "")

    BlockVerticalBorder = ("", "", "", "█", "█", "", "", "")

    BlockOverline = ("", "▀", "", "", "", "", "", "")

    BlockUnderline = ("", "", "", "", "", "", "▀", "")


def addborder(value: str, bordertype=BorderTypes.ThinBorder):
    """
    Adds a four-sided ASCII border around a component.

    Args:
        value: The string representation of the component's layout. Use <component>.value() to get.

    Returns:
        The component's value with a border, in string
    """

    # If the text is empty
    if value == "":
        value = " "
    buffer: list = str(value).splitlines(False)
    width: int = len(LongestFromList(buffer))

    # Insert side borders
    for lineindex in range(0, len(buffer)):
        linelength = len(buffer[lineindex])
        if linelength < width:
            # The line is not long enough. Add spaces after the line
            buffer[lineindex] = buffer[lineindex] + " "*(width-linelength)

        buffer[lineindex] = bordertype[3] + buffer[lineindex] + bordertype[4]

    # Insert top-and-bottom borders with corner pieces
    buffer = [bordertype[0] + bordertype[1] * width + bordertype[2]] + \
        buffer + \
        [bordertype[5] + bordertype[6] * width + bordertype[7]]

    # Delete empty horizontal borders
    if buffer[0] == "":
        del buffer[0]
    if buffer[-1] == "":
        del buffer[-1]


    return "\n".join(buffer)



#========================Color list========================

class SystemColors:

    Default = Color(255, 255, 255)
    WindowBorder = Color(96, 96, 96)

    Hyperlink = Color(6, 69, 173)
    VisitedHyperlink = Color(11, 0, 128)



#========================Canvas class========================

class Canvas:

    def __init__(self, width: int, height: int, bordertype=BorderTypes.BlockBorder):

        # Dictionary to store all component
        self.__elem = {}

        # OPTIONS
        self.Width = int(width)
        self.Height = int(height)

        self.Border = bordertype


    def add(self, component, z_pos: int=-1):
        # We must first check if 'component' passes a subclass of class 'Component'
        if not issubclass(type(component), Component):
            raise TypeError("Argument 'component' is not an implementation of class 'Component'.")
        if z_pos == -1:
            self.__elem[len(self.__elem)] = component
        else:
            self.__elem[z_pos] = component


    def setzpos(self, z_pos, new_z_pos):
        if z_pos in self.__elem.keys():
            self.__elem[new_z_pos] = self.__elem[z_pos]
            del self.__elem[z_pos]


    def remove(self, z_pos: int):
        if z_pos in self.__elem.keys():
            del self.__elem[z_pos]


    def draw(self, delay: float=0, hideoverflown: bool=False, color: str='default'):
        """
        Draws/renders the current canvas with its components.

        Args:
            delay: A float indicating the delay, in seconds, before rendering starts.
            hideoverflown: Boolean indicating whether to omit rendering any component that is partially out of bounds.
            color: The color of the canvas. WILL OVERRIDE ANY CUSTOM COMPONENT COLOR (if not set to 'default')!

        """

        # draw elements inside __elem dictionary.
        # __elem dictionary has the following structure: ([z-pos], ([object to draw], [focus order]))

        # Delay parameter
        if delay > 0:
            time.sleep(delay)

        # This is the current ASCII frame to render.
        frame = (" "*self.Width + "\n")*(self.Height-1) + (" "*self.Width)
        # This buffer serves to write to individual lines
        framebuffer = frame.split(sep="\n")

        # Below for block writes individual component to 'framebuffer'
        # We need to write components from the smallest z-pos to the largest, hence the usage of range()
        for index in self.__elem.keys():
            comp: Component = self.__elem[index]
            # To write a component onto the frame, we need to separate each line and store the result in a list.
            compbuffer: list = comp.value().split(sep="\n")

            # Testing if the component overflows for optional parameter 'hideoverflown'
            if hideoverflown:
                if len(LongestFromList(compbuffer)) > (self.Width - comp.X):
                    # Object overflows in the x-axis, discard.
                    # Note: using Utils.py's LongestFromList() will rule out any inconsistent 'Component' class's value() implementation.
                    continue
                if len(compbuffer) > (self.Height - comp.Y):
                    # Object overflows in the y-axis, discard.
                    continue

            # Testing if the current component is outside of canvas area:
            if comp.X >= self.Width and comp.Y >= self.Height:
                # Object entirely outside of canvas, discard.
                continue

            # Drawing 'comp' inside 'framebuffer'
            for lineindex in range(0, len(compbuffer)):
                if comp.Y + lineindex >= len(framebuffer) or comp.Y + lineindex < 0:
                    # This line is out of bounds. Do not draw.
                    continue
                # Convert target 'framebuffer' line into a list of characters with list(str)
                linebuffer: list = list(framebuffer[comp.Y + lineindex])
                # Convert target 'compbuffer' line into a list of characters
                complinebuffer: list = list(compbuffer[lineindex])
                # This will replace the line with the current component's content without overflowing.
                #linebuffer[comp.X :] = complinebuffer[0 : len(linebuffer)-comp.X]      - produces undesirable result
                linebuffer[comp.X :] = complinebuffer
                # Update the target 'framebuffer' line with the new one
                framebuffer[comp.Y + lineindex]: str = "".join(linebuffer)

            for i in range(0, len(framebuffer)):
                # Adds space for lines that do not match canvas's width
                if len(framebuffer[i]) < self.Width:
                    framebuffer[i] += " " * (self.Width - len(framebuffer[i]))
                # Cuts overflown lines that do not match canvas's width
                if len(framebuffer[i]) > self.Width:
                    framebuffer[i] = framebuffer[i][0:self.Width]

        # Reassemble from from framebuffer
        frame = "\n".join(framebuffer)

        # Adding borders to current frame string
        frame = addborder(frame, self.Border)

        WriteShell(frame, end="\n", Color=color)

    def ColorPrinter(self, , delay: float=0, hideoverflown: bool=False, color: str='default'):




# ========================GUI class========================

class GUI:
    """
    Class responsible for the creation and maintenance of a canvas and its components.
    """

    #====================Magic methods====================

    def __init__(self, width: int = 100, height = 25, bordertype = BorderTypes.NoBorder):
        self.width = width
        self.height = height
        self.bordertype = bordertype

        self.Focus = 0 # focuses on first component

        # UX interactions
        self._inputkey = KeyCodes.Null
        self._inputkeystr = KeyCodes.tostring(KeyCodes.Null)
        self._userinput = KeyPressEventHandler(self._keypressdetector)

    #====================Properties====================

    @property
    def active(self):
        """
        Returns the index of the child component currently receiving focus.

        Returns:
            the index of the component to focus in integer
        """
        return self._active
    @active.setter
    def active(self, value: bool):
        """
        Focuses on a child component by its index.

        Args:
            value: the index of the component to focus in integer
        """
        self._active = bool(value)
        if bool(value):
            self._run()

    @property
    def focus(self):
        """
        Returns the index of the child component curently receiving focus.

        Returns:
            the index of the component to focus in integer
        """
        return self._focusindex
    @focus.setter
    def focus(self, value: int):
        """
        Focuses on a child component by its index.

        Args:
            value: the index of the component to focus in integer
        """
        if int(value) != self._focusindex:

            self._focusindex = int(value)

    @property
    def height(self):
        """
        Returns the width, in characters, of the GUI.

        Returns:
            an integer representing the height of the GUI
        """
        return self._height
    @height.setter
    def height(self, value: int):
        """
        Specifies the height, in characters, of the GUI.

        Args:
            value: an integer specifying the height of the GUI
        """
        self._height = value

    @property
    def width(self):
        """
        Returns the width, in characters, of the GUI.

        Returns:
            an integer representing the width of the GUI
        """
        return self._width
    @width.setter
    def width(self, value: int):
        """
        Specifies the width, in characters, of the GUI.

        Args:
            value: an integer specifying the width of the GUI
        """
        self._width = value

    #====================UX====================

    def _keypressdetector(self, args: KeyPressEventArgs):
        """
        Function delegate used to detect user key press input

        Args:
            sender:
            args:
        """
        self._inputkey = args.Key
        self._inputkeystr = KeyCodes.tostring(args.Key, args.Key2)

    def _run(self):
        """
        Begins execution of the GUI thread.
        Controlled internally by the GUI class.
        """



#========================Component class========================

class Component:

    #====================Magic methods====================

    def __init__(self, location, width: int = 0, height: int = 0):
        self.width = width
        self.height = height
        self.location = location

        self._focused = False


        self.handledinput = False       # This variable determines whether the GUI should transmit input to the component

        self.FocusLost = FocusLostEventListener()
        self.KeyPress = KeyPressEventListener()
        self.OnFocus = OnFocusEventListener()

    def __eq__(self, other):
        return str(self) == str(other)

    def __repr__(self):
        return self.value()

    #====================Methods====================

    def value(self):
        """
        Each component should be a string which, when printed, yields a rectangular footprint.

        Returns:
            A string representing the component.
        """
        return ""

    #====================Properties====================

    @property
    def focused(self):
        """
        Whether the component is receiving focus.
        """
        return self._focused
    @focused.setter
    def focused(self, value: bool):
        """
        Notifies this component's OnFocus event listener when it receives focus.
        Notifies this component's FocusLost event listener when focus is lost.
        """
        if value:
            self._focused = True
            self.OnFocus.notify(sender=self)
        else:
            self._focused = False
            self.FocusLost.notify(sender=self)

    @property
    def height(self):
        """
        Returns the width, in characters, of the UI.

        Returns:
            an integer representing the height of the UI
        """
        return self._height
    @height.setter
    def height(self, value: int):
        """
        Specifies the height, in characters, of the UI.

        Args:
            value: an integer specifying the height of the UI
        """
        self._height = int(value)

    @property
    def location(self):
        """
        The location of the component inside the UI.

        Returns:
            a tuple specifying the component's (x, y) location inside the UI
        """
        return self._location
    @location.setter
    def location(self, value):
        """
        Sets the location of the component inside the UI.

        Args:
            value: a tuple specifying the component's (x, y) location inside the UI
        """
        self._location = (value[0], value[1])

    @property
    def width(self):
        """
        Returns the width, in characters, of the UI.

        Returns:
            an integer representing the width of the UI
        """
        return self._width
    @width.setter
    def width(self, value: int):
        """
        Specifies the width, in characters, of the UI.
        Set to 0 for

        Args:
            value: an integer specifying the width of the UI
        """
        self._width = int(value)



#========================Version History========================

# 1.0
"""
    Initial Release

    Additions
    ---------
        -BordeeTypes class
        -addborder(value: str, bordertype=BorderTypes.ThinBorder, vertical=True, horizontal=True)
        -Canvas class
            -__init__(self, width: int, height: int, horizontal_borders=True, vertical_borders=False, bordertype=BorderTypes.BlockBorder)
            -add(self, component, z_pos: int=-1)
            -setzpos(self, z_pos, new_z_pos)
            -remove(self, z_pos: int)
            -draw(self, delay: float=0, hideoverflown: bool=False, color: str='default')
                -Currently the option to color the canvas is limited: can only color the whole canvas+components altogether, instead of simply the canvas's background
            -Canvas is the drawing board on which Components are added
        -Component class
            -__init__(self, x, y)
            -value(self)
        -Label(Component) class
            -__init__(self, x, y, text, showborder=False, bordertype=BorderTypes.ThinBorder, length=-1, overflowindicator="…")
            -value(self)
            -Can act not only as a label for simple lines or paragraphs, but also as a textbox, a checkbox, or a button
        -Illustration(Component) class
            -__init__(self, x, y, ascii, border=False)
            -A dud/foobar for later implementation of a drawing component
            -Will be used to convert external images into colored ASCII drawings
    To-Do
    -----
        -Add a function to superpose two different strings into one, with option to specify coloring for each string component.
        -Implement a GUI system to automatically control canvas drawing and offer additional components that are tied with the event system.
            -Most likely needs to be inside a separate Python file, as this system would require dependencies of EventSystem.py.
                -Will need to rename this file as ShellGUIbase.py, and migrate Label and Illustration classes to the new ShellGUI_Core.py file.
"""

# 1.1
"""
    Additions and changes related to borders

    Additions
    ---------
        -Added Version History at the end of ShellGUI_Core.py
        -Added more border types as tuple constants in BorderTypes class (under the new border format)
            -NoBorder, ThinHorizontalBorder, ThinVerticalBorder, ThinUnderline, ThinOverline, BlockHorizontalBorder, BlockVerticalBorder, BlockOverline, BlockUnderline
    
    Changes
    -------
        -Changed border structure
            -Previously the structure is specified as ([horizontal piece], [vertical piece], [upper left corner], [upper right corner], [lower left corner], [lower right corner])
            -Changed to ([ul corner], [upper horizontal piece], [ur corner], [left vertical piece], [right vertical piece], [ll corner], [lower horizontal piece], [lr corner])
            -This change allows larger diversity in the stylistical types of borders 
        -Changed addborder() mechanism
            -To comply with the new border structure
            -Will now also omit blank horizontal border lines (e.g. for ThinUnderline border type)
        -Signatures for these functions/methods are changed to comply with the new border structure
            -addborder(value: str, bordertype=BorderTypes.ThinBorder, vertical=True, horizontal=True) changed to addborder(value: str, bordertype=BorderTypes.ThinBorder)
            -Canvas.__init__(self, width: int, height: int, horizontal_borders=True, vertical_borders=False, bordertype=BorderTypes.BlockBorder)
                ->Changed to Canvas.__init__(self, width: int, height: int, bordertype=BorderTypes.BlockBorder)
    Bug Fixes
    ---------
        -
"""

# 2.0
"""
    Refactored ShellGUI.py into two separate modules: ShellGUI_Core.py and ShellGUI_Forms.py
    This separation permits better modular forms support without encumbering the core ASCII rendering engine.
    
    Additions
    ---------
        -
    
    Changes
    -------
        -Removed class 
    
    Bug Fixes
    ---------
        -
"""
