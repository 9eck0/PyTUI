"""
This internal class handles the concrete printing of the TUI onto the terminal.

During a frame update, it must first erase the previous frame, then write the new frame on top.
"""


# TODO: for erasure: devise an algorithm to erase only to the earliest deviation from last frame (speed optimization)
