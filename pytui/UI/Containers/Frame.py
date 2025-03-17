"""
The Frame represents a fixed portion of the UI space for canvassing a standalone TUI window.
Frames can be used to create page navigation systems, taking the entire screen space, or as a tabbed format.

When receiving focus, a Frame will attempt to delegate focus to its child Components. Failing to do so (e.g. empty Frame),
the focus will be captured by the Frame itself.
When focus is lost, the Frame will remember its current focus cycling state and restore it when it regains focus.

PyTUI initializes with the root frame as the first layer of the drawing hierarchy. This root frame is initially blank
and has the same size as the configured TUI window.

"""

from pytui.System.Rendering.FragmentCanvas import FragmentCanvas
from pytui.UI.ABC.BaseContainer import BaseContainer
from pytui.UI.ABC.Focusable import Focusable
from pytui.UI.Components.Component import Component


class Frame(BaseContainer, Focusable):
    """
    Represents a top-level UI window/container for components.

    Properties of Frames include:

    - Frames can be nested within other Frames.
    - Focus: A Frame can be configured to capture focus within itself to be cycled over its child Components.
    - Frames can gain and lose focus independently of the specific component in focus.
    """

    def __init__(self, width: int, height: int, location: (int, int) = None):

        super().__init__(width=width, height=height, location=location)

        self.fullscreen = False

        # ======== Internal Properties ========

        self.components: list[Component] = []
        """ The list of components drawn within this Frame. """

    def render_content(self, width, height) -> FragmentCanvas:
        return super().render_content(width, height)

