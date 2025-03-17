"""
This module defines the Illustration view component.
"""

if __name__ == "__main__":
    # MAJOR +1 represents an added function.
    __MAJOR = 1
    # MINOR +1 represents a change in existing function(s) within the current MAJOR.
    __MINOR = 0

    __info = """This file contains the module 'Illustration', an integral view component to the ShellGUI system.
To use this module in another project, include this file inside the project's directory."""

    print("========================================================")
    print("Illustration.py version ", __MAJOR, ".", __MINOR, sep='', end='\n\n')
    print(__info)
    print("========================================================\n")
    input("Press enter to continue...")


#region ======================== Imports ========================

from ShellGUI_Core import BorderTypes, addborder
from Component import Component

#endregion Imports


# ======================== Common Functions ========================

# no function


#region ======================== Illustration ========================

class Illustration(Component):
    """
    A component that can draw colored images
    """

    def __init__(self, x, y, ascii, border=False):
        Component.__init__(self, x, y)

        self.ASCII = str(ascii)
        self.Border = bool(border)

#endregion Illustration


#region ======================== Version History ========================

# 1.0
"""
    Refactored Label class out of ShellGUI_Forms.py.

    Additions
    ---------
        -Illustration(Component) class
            -__init__(self, x, y, ascii, border=False)
            -A dud/foobar for later implementation of a drawing component
            -Will be used to convert external images into colored ASCII drawings
"""

#endregion Version History
