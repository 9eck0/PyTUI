"""
This file contains the TUI system implementation.
"""


from typing import Sequence

import System.Terminal.Terminal as Terminal

from EventSystem.KeyCodes import KeyCodes, KeyCombo
from System.FocusManager import FocusManager
from UI.ABC.BaseContainer import BaseContainer
from UI.ABC.Focusable import Focusable
from UI.Components.Component import Component
from UI.Containers.Frame import Frame
from UI.ABC.BaseComponent import BaseComponent
from Utils.Tree import Tree


class TUI:
    """
    The textual interface implementation class.
    The TUI controller's task is to coordinate between UI data, rendering and the event system.

    To use PyTUI, initialize this class with
    """

    def __init__(self):

        self.root_frame = Frame(**Terminal.get_terminal_size(), location=(0, 0))
        """
        The base frame of the TUI, shown as the root layer of the drawing hierarchy.
        
        This special frame can always receive focus and cannot be removed.
        """

        self.layout_tree = Tree(self.root_frame)
        """
        Hierarchical data structure representing the TUI's component layout.
        
        The root node of this layout tree is the topmost Frame encapsulating the entire TUI's content.
        """

        self.z_stack = []

        self.focus_manager = FocusManager(self)

        # ================ TUI Configuration ================

        self.key_navigation_next: KeyCombo = KeyCombo(KeyCodes.ArrowLeft)

        self.key_navigation_previous: KeyCombo = KeyCombo(KeyCodes.ArrowRight)

    def register(self, component: BaseComponent, parent: BaseContainer | None = None) -> Tree[BaseComponent]:
        if parent is None:
            # Adds the component as a base
            parent = self.root_frame
        if not isinstance(parent, BaseContainer):
            raise ReferenceError("Invalid component registration: the given parent is not a valid container")
        if not isinstance(parent._tui_layout_node, Tree):
            raise ReferenceError("Invalid component registration: the given parent has corrupted registration")
        if parent._tui_layout_node.get_root() is not self.layout_tree:
            raise ReferenceError("Invalid component registration: the given parent container is not registered to the"
                                 "current TUI instance")

        reg_node = Tree(component)
        parent._tui_layout_node.add_child(reg_node)

        component._tui_layout_node = reg_node
        component._tui_instance = self

        if isinstance(component, Focusable):
            self.focus_manager.register_focusable(component)

        return reg_node


    #region ================ Layout Management ================
    """
    PyTUI possesses a layout hierarchy composed of Frames > [Frames | Panels] (optional) > Components.
    
    A Frame is the top-level container for a TUI, and contains all other UI components in the
    hierarchy, including other Frames.
    
    A panel is an optional sub-container of a Frame, allowing for nested layout management.
    They handle component ordering and layout, available in multiple layout configurations
    such as single panel, columnar, tabular, etc.
    
    A component is an interactive UI element that can be drawn directly on a Frame.
    They are the leaf nodes of the UI hierarchy, receiving input and rendering.
    """


    #endregion


# region ================ PyTUI initialization ================

# Check terminal capabilities

#endregion
