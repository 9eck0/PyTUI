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

    __info = """This file contains the module 'ShellGUI_Forms', used  by ShellGUI_Core to create a shell-based rendering engine.
To use this module in another project, include this file inside the project's directory."""

    print("========================================================")
    print("ShellGUI_Forms.py version ", __MAJOR, ".", __MINOR, sep='', end='\n\n')
    print(__info)
    print("========================================================\n")
    input("Press enter to continue...")


#========================Imports========================

from ShellGUI_Core import *
from EventSystem import *
from Utils import *


#========================Label class========================




#========================Label class========================




#========================Illustration class========================




#========================Version History========================

# 1.0
"""
    Initial Release
    See version 2.0 of ShellGUI_Core.py for details.

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
