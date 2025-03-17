"""
This module defines the Label view component.
"""

from Component import Component


class Label(Component):

    def __init__(self, location, text: str,
                 showborder: bool = False, bordertype=BorderTypes.ThinBorder,
                 length=-1, overflowindicator="…"):
        Component.__init__(self, location=location)

        self.Text = str(text)
        self.ShowBorder = bool(showborder)
        self.BorderType = bordertype
        self.Length = int(length)
        self.OverflowIndicator = str(overflowindicator)

    def value(self):
        # 'buffer' is the string representation of the 'Label' Component that is being processed.
        buffer = self.Text
        # If self.Length property is set to a positive integer, truncate.
        if self.OverflowIndicator and -1 < self.Length < len(buffer):
            buffer[self.Length - 2 :] = self.OverflowIndicator
        elif -1 < self.Length < len(buffer):
            buffer[self.Length - 1 :] = ""
        # Adds a hard-coded border around the text if property is set.
        if self.ShowBorder:
            buffer = addborder(buffer, self.BorderType)

        return buffer

    def render_content(self, width, height):
        pass
