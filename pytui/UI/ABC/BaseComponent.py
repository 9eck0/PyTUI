"""
BaseComponent is the base abstraction class for Component and Frame, containing shared code for static properties and
compositing.


"""
import warnings
from abc import abstractmethod
from typing import Sequence

from Color import ColorHandler, NamedColorList
from EventSystem.Event import Event
from System.Rendering.CanvasRenderState import CanvasRenderState
from System.Rendering.FragmentCanvas import FragmentCanvas
from TUI import TUI
from UI.ABC.BaseContainer import BaseContainer
from Utils.Tree import Tree

#region ================================ Rendering Set ================================


PIPELINE_TRANSPARENCY = NamedColorList.Transparent


#endregion


class BaseComponent:
    """
    Represents a generic UI component capable of being rendered by PyTUI.

    --------

    This is the base class for all components and containers, containing shared code for static properties and
    compositing.

    Extend this class to define visual extension functionalities for PyTUI.
    """

    #region ================================ Magic Functions ================================

    def __init__(self, width: int, height: int, location: (int, int) = None):

        # Hidden fields declared herein serve as property values. Use their getters and setters to enable side effects.

        # ======== Internal Properties ========

        self._tui_instance: TUI | None = None
        """ Dependency injection pattern for referencing the TUI system registration.
            A value of None means this is currently an unregistered UI component, unable to perform rendering. """

        self._tui_layout_node: Tree[BaseComponent] | None = None
        """ Reference to the node representing this component in the TUI's layout tree.
            Accessible after registration to a TUI instance. """

        #TODO to deprecate: self._base_canvas: FragmentCanvas = FragmentCanvas(width=width, height=height)
        """ The current component's base canvas. Does not include child components. """

        #TODO to deprecate: self._renderer = self.render_content
        """ The function used to render this UI component. Modify this property to implement custom skin renderers. """

        self._state_indicators: CanvasRenderState = CanvasRenderState()
        """
        Determines whether a call to redraw this Frame and all its contents is required.
        """

        #TODO to deprecate: self._lastRender: FragmentCanvas | None = None
        """ Stores the last render result value. Set to None to force re-rendering. """

        # ======== Layout Properties ========

        self._width: int = 1 if width < 1 else width
        """ This UI component's width, in character blocks. """

        self._height: int = 1 if height < 1 else height
        """ This UI component's height, in character blocks. """

        self._location: (int, int) = (0, 0) if location is None else location
        """ The default (x, y) location coordinates of this UI component's top left corner. \n
            Invalid location coordinates are accepted, although this will render as partially or fully clipped. """

        self._z_index: int | None = None

        self._visible: bool = True

        self._padding_top: int = 0
        """ Minimal blank space between this component's top border and its content, in character blocks. \n
            Setting padding values too large can result in content being clipped. """

        self._padding_bottom: int = 0
        """ Minimal blank space between this component's bottom border and its content, in character blocks. \n
            Setting padding values too large can result in content being clipped. """

        self._padding_left: int = 0
        """ Minimal blank space between this component's left border and its content, in character blocks. \n
            Setting padding values too large can result in content being clipped. """

        self._padding_right: int = 0
        """ Minimal blank space between this component's right border and its content, in character blocks. \n
            Setting padding values too large can result in content being clipped. """

        self._adaptive_width: bool = False
        """ Whether this component's width will adapt according to its content and padding. """

        self._adaptive_height: bool = False
        """ Whether this component's height will adapt according to its content and padding. """

        self._min_width: int = 0
        """ If adaptive_width is enabled, this setting will restrict dynamic width shrinking to no less than this value.
            Values greater than default width are ineffective. """

        self._min_height: int = 0
        """ If adaptive_height is enabled, this setting will restrict dynamic height shrinking to no less than this
            value. Values greater than default height are ineffective. """

        # ======== Appearance Properties ========

        self._fill: int | ColorHandler | None = None
        """ The infill color for this component. """

        self._border: list[str] | None = None
        """ The type of border drawn around this component. See Appearance.BorderTypes enum for a builtin selection.
            None for no border. """

        self._border_color: int | ColorHandler | None = None
        """ Custom color of the border. None for default terminal text color. """

        # ======== Behavior Properties ========

        self._enabled = True
        """ Whether this component is enabled for interactivity. """

        # ======== State Properties ========

        # ======== Base Events Registration ========

        self._on_dispose = Event()

    #endregion

    #region ==================== Event Listeners =====================

    @property
    def OnDispose(self):
        return self._on_dispose

    @OnDispose.setter
    def OnDispose(self, value):
        if value is not self._on_dispose:
            # Trying to set a new event listener object
            if not isinstance(value, Event):
                raise TypeError(
                    f"Attempting to set an incompatible object as an OnDispose event listener: {type(value)}")
            self._on_dispose = value
        # else: no need to perform setter operation on the same object, e.g. OnFocus += method

    #endregion

    #region ================================ Property Accessors ================================
    # Listed alphabetically within property groups

    @property
    def adaptive_width(self):
        return self._adaptive_width

    @adaptive_width.setter
    def adaptive_width(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("Specifying adaptive width requires a boolean. Obtained '"
                            + str(type(value))
                            + "' instead.")
        self._adaptive_width = value
    
    @property
    def adaptive_height(self):
        return self._adaptive_height

    @adaptive_height.setter
    def adaptive_height(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("Specifying adaptive height requires a boolean. Obtained '"
                            + str(type(value))
                            + "' instead.")
        self._adaptive_height = value

    @property
    def border(self):
        return self._border

    @border.setter
    def border(self, value: Sequence[str]):
        if not isinstance(value, Sequence) or len(value) < 8:
            raise TypeError("Invalid border value type: must be a sequence of 8 string characters.")
        self._border = value

    # Enabled
    @property
    def Enabled(self):
        return self._enabled
    @Enabled.setter
    def Enabled(self, value: bool):
        self._enabled = value

    # Location
    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value: (int, int)):
        if not isinstance(value, tuple) or len(value) < 2:
            raise TypeError("Invalid UI component location: must be a 2D coordinate in the form of tuple of two ints.")
        value = (int(value[0]), int(value[1]))
        if self._location != value:
            self._state_indicators.prev_location = self._location
            self._location = value
            self._state_indicators.location_changed = True

    @property
    def parent(self) -> BaseContainer | None:
        """
        The parent container to this component.

        If there is no parent, or the parent is not a proper container (corrupted layout tree), this property returns
        None.

        To add this component to a parent container, use the add_child() function of a valid container instance.

        :raise RuntimeWarning: Warns if the parent of this component is linked to an invalid object not implementing
            UI.ABC.BaseContainer class. This is not an error, as this check does not account for duck typing.
        """

        if self._tui_layout_node is not None and self._tui_layout_node.parent is not None:
            parent = self._tui_layout_node.parent.value
            if isinstance(parent, BaseContainer):
                # Proper parent container
                return parent
            elif isinstance(parent, BaseComponent):
                # improper parent
                warnings.warn("Component's linked parent is not a valid container object.", RuntimeWarning)
        return None

    # Width
    @property
    def width(self):
        """
        Specifies the width, in characters, of the UI.

        Note: setting this value manually will override adaptive width.

        Returns:
            an integer specifying the width of the UI
        """

        if not self._adaptive_width:
            return self._width
        else:
            return self.get_content_width()
    
    @width.setter
    def width(self, value: int):
        """
        Specifies the width, in characters, of the UI.

        Note: Setting this value manually will override adaptive width.

        Args:
            value: A positive integer specifying the width of the UI; its value must be at least 1.
        """

        value = int(value)
        if value < 1:
            raise ValueError("Invalid UI component width: must be at least 1.")
        if self._width != value:
            self._state_indicators.prev_width = self._width
            self._width = value
            self.adaptive_width = False
            self._state_indicators.size_changed = True

    # Height
    @property
    def height(self):
        """
        Specifies the height, in characters, of the UI.

        Note: Setting this value will override adaptive height.

        Returns:
            An integer specifying the height of the UI.
        """

        if not self._adaptive_height:
            return self._height
        else:
            return self.get_content_height()
    
    @height.setter
    def height(self, value: int):
        """
        Specifies the height, in characters, of the UI.

        Note: Setting this value will override adaptive height.

        Args:
            value: A positive integer specifying the height of the UI; its value must be at least 1.
        """

        value = int(value)
        if value < 1:
            raise ValueError("Invalid UI component height: must be at least 1.")
        if self._height != value:
            self._state_indicators.prev_height = self._height
            self._height = value
            self.adaptive_height = False
            self._state_indicators.size_changed = True

    # Z-index
    @property
    def z_index(self):
        return self._z_index

    @z_index.setter
    def z_index(self, value: int | None):
        value = int(value)
        if self._z_index != value:
            self._state_indicators.prev_z_index = self.z_index
            self._z_index = int(value)
            self._state_indicators.z_changed = True

    #endregion

    #region ================================ Interfacing Methods ================================

    def dispose(self):
        """

        :return:
        """

    #endregion

    #region ================================ Rendering Methods ================================

    @abstractmethod
    def get_content_width(self) -> int:
        """
        Returns the width of the current component's inner content.

        :return: The inner content's width, in character blocks.
        :rtype: int
        """
        if self._state_indicators is not None and self._state_indicators.content_canvas_buffer is not None:
            return self._state_indicators.content_canvas_buffer.width
        return self._width
    
    @abstractmethod
    def get_content_height(self) -> int:
        """
        Returns the height of the current component's inner content.

        :return: The inner content's height, in character blocks.
        :rtype: int
        """
        if self._state_indicators is not None and self._state_indicators.content_canvas_buffer is not None:
            return self._state_indicators.content_canvas_buffer.height
        return self._height

    @abstractmethod
    def render_content(self, width, height) -> FragmentCanvas:
        """
        Default renderer for the current component's content.

        :param width: The render width of the content.
        :param height: The render height of the content.
        :return: A rendered FragmentCanvas of the inner content.
        :rtype: FragmentCanvas
        """
        return None

