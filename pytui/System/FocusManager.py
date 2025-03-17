"""
The FocusManager handles all requests to set focus and notifies observers centrally.

In PyTUI, focus is uniquely given to a single focusable UI component (implementing the UI.ABC.Focusable interface).
The cycling order between components is dictated by the following policies:

    - Only instances of classes implementing the Focusable interface can receive focus.

    - Focus scope

A component can request focus lock onto itself, which will prevent losing focus until the lock is cleared or the
component is invalidated (hidden, disabled, disposed from TUI).
"""


from collections import deque
from sys import stderr

from TUI import TUI
from UI.ABC.BaseComponent import BaseComponent
from UI.ABC.Focusable import Focusable
from Utils.Tree import Tree


_FOCUS_TREE_SORT_KEY = lambda node: node.value.focus_index


class FocusManager:

    def __init__(self, tui: TUI):
        self._tui_instance = tui

        self.current_focus: Tree = tui.layout_tree
        """
        The current component being focused.
        
        This node and its ancestors form the focus stack of the GUI.
        When focus is explicitly removed from the current component, it will traverse up the stack.
        """

        self._focus_lock: Tree | None = None

    def _focusable_onfocus_handler(self, sender: Focusable, args):
        if not isinstance(sender, Focusable):
            stderr.write("Warning: an unfocusable object instance has been registered with FocusManager")
            return
        # try focus
        self.try_focus(sender)
        pass

    def _focusable_onfocuslost_handler(self, sender: Focusable, args):
        if not isinstance(sender, Focusable):
            stderr.write("Warning: an unfocusable object instance has been registered with FocusManager")
            return
        if sender is self.current_focus.value:
            self.unfocus()
        pass


    def display_focus_feedback(self):
        """
        Executes a visual feedback to alert the user to the currently focus-locked UI component.
        """
        if not isinstance(self._focus_lock.value, Focusable):
            # Since this is a visual indicator function, an invalid instance encounter should be handled gracefully
            return

        mode = self._focus_lock.value.focus_feedback_mode
        pass

    def is_focus_locked(self):
        return isinstance(self._focus_lock, Tree)

    def register_focusable(self, focusable: Focusable):
        focusable.OnFocus.subscribe(self._focusable_onfocus_handler)
        focusable.OnFocusLost.subscribe(self._focusable_onfocuslost_handler)

    def try_focus(self, focusable: Focusable) -> bool:
        """
        Attempts to focus onto the specified focusable component.

        If this component is disabled, or another focusable component is in locked focus mode, and is not a hierarchical
        parent of the specified component, this action fails and returns False. Otherwise, returns True.
        Simultaneously, the currently focus-locked component's visual focus feedback mode activates.
        """

        #TODO focus lock stack logic
        if focusable is self.current_focus.value:
            return True
        if isinstance(focusable, BaseComponent) and not focusable.Enabled:
            return False
        if self._focus_lock is not None and not self.current_focus.is_descendant_of_value(focusable):
            # Policy: when focus is locked to another component, only if the target is a descendant can it receive focus
            self.display_focus_feedback()
            return False
        # Transfer focus
        node = focusable._tui_layout_node if isinstance(focusable, BaseComponent) else self._tui_instance.layout_tree.find(focusable)
        if node is None:
            return False
        self.current_focus = node
        return True

    def try_focus_parent(self):
        """
        Returns focus to the closest focusable ancestor.
        """

    def try_lock_focus(self, focusable: Focusable) -> bool:
        """
        Attempts to force lock focus onto the specified focusable component.

        If this component is disabled, or another focusable component is in focus lock mode, and is not a hierarchical
        parent of the specified focusable component, this action fails and returns False. Otherwise, returns True.
        """

        if self._focus_lock:
            if self.current_focus.is_ancestor_of(focusable):
                pass
        else:
            self._focus_lock = self.try_focus(focusable)
            return self._focus_lock
        return False

    def unlock_focus(self):
        pass

    def try_cycle_previous(self):
        prev_focus = self.current_focus.dfs_previous()
        while prev_focus is not self.current_focus:
            if isinstance(prev_focus.value, Focusable) and prev_focus.value.focusable:
                return self.try_focus(prev_focus)
            prev_focus = prev_focus.dfs_previous()
        # No component can currently receive focus
        return False

    def try_cycle_next(self):
        """
        Attempts to transfer current focus to next component, subject to focus policies.

        :return: True if successfully transferred focus to next component, False otherwise.
        """

        next_focus = self.current_focus.dfs_next()
        while next_focus is not self.current_focus:
            if isinstance(next_focus.value, Focusable) and next_focus.value.focusable:
                return self.try_focus(next_focus)
            next_focus = next_focus.dfs_next()
        # No component can currently receive focus
        return False

    def unfocus(self):
        """
        Removes focus from current component and returns it to its closest focusable ancestor.
        """

        # Assumption: focus lock is only valid for components implementing the Focusable interface
        # => this function should not skip a focus locked node when backtracking to root
        if self._focus_lock is self.current_focus:
            self._focus_lock = None
        while not self.current_focus.is_root():
            self.current_focus = self.current_focus.parent
            if isinstance(self.current_focus.value, Focusable) and self.current_focus.value.focusable:
                return
        if self.current_focus is None:
            # If no component is receiving focus, defaults to root Frame
            self.current_focus = self._tui_instance.layout_tree
