"""
Base class for all components which can contain other components as children.

This class has couplings to the TUI class, as a container needs to be layout-aware and interact with its
children components.
"""
from abc import abstractmethod

from BaseComponent import BaseComponent
from System.Rendering.FragmentCanvas import FragmentCanvas


class BaseContainer(BaseComponent):

    def __init__(self, width: int, height: int, location: (int, int) = None):
        super().__init__(width, height, location)

        self.children: list[BaseComponent] = []

    def add_child(self, child: BaseComponent):
        """
        Adds a component as child of the current container.

        This operation also registers the child component to the same TUI instance as this container if necessary.

        :param child: the child component to add to this UI container.
        """
        if not isinstance(child, BaseComponent):
            raise ValueError("Invalid addition to UI container: Object is not an instance of BaseComponent.")
        self.children.append(child)
        if self._tui_instance is not None and child._tui_instance is not self._tui_instance:
            self._tui_instance.register(child)

    @abstractmethod
    @property
    def width(self, child: BaseComponent = None):
        return super().width

    @abstractmethod
    def render_content(self, width, height) -> FragmentCanvas:
        pass
