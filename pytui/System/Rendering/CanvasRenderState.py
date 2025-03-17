"""
Belonging to the rendering pipeline, this utility class serves to store temporary render states and indicators.
  - Render state: A
  - Rendering indicator: Tracks whether a visual property has been modified in order to require a redraw.

These properties are stored in a separate class file from FragmentCanvas.py for readability purposes.
"""


from System.Rendering.FragmentCanvas import FragmentCanvas


class CanvasRenderState:

    def __init__(self):

        # -------- Render states --------

        self.final_canvas_buffer: FragmentCanvas | None = None
        """
        A FragmentCanvas containing the final render of the entire component, including its border and any applied
        post-processing steps.
        
        To reset this rendering step, set the value of this variable to None.
        """

        self.border_canvas_buffer: FragmentCanvas | None = None
        """
        A FragmentCanvas containing pre-rendered border. None for no border.
        
        To perform border redrawing, set the value of this variable to None.
        """

        self.content_canvas_buffer: FragmentCanvas | None = None
        """
        A FragmentCanvas containing last rendered content, prior to any post-processing steps.
        
        To perform content redrawing, set the value of this variable to None.
        """

        # -------- Rendering indicators --------

        self._visible_changed = True
        """ Visibility determines whether the UI component is rendered or not. """

        self._content_changed = True
        """ Whether an inner content change requires redraw of the component or child components. """

        self._padding_changed = True
        """ A padding change can clip content, also affecting adaptive size and border size, requiring a redraw. """
        self.prev_paddings = (0, 0, 0, 0)

        self._size_changed = True
        """ Size change directly affects border and padding, as well as affecting the inner content through side effects.
            Note that adaptive size is categorized as a content change, not a size change. """
        self.prev_width = 0
        self.prev_height = 0

        self._border_changed = True
        """ Borders should be redrawn when their character set is redefined, when size changes, or when border
            properties change (e.g. border color). """

        self._location_changed = True
        """ When the location is changed,  """
        self.prev_location = (0, 0)

        self._z_changed = True
        """ When the Z-order is changed, a visibility recalculation must be performed by the TUI system. """
        self.prev_z_index = None

    @property
    def visible_changed(self):
        return self._visible_changed

    @visible_changed.setter
    def visible_changed(self, value):
        self._visible_changed = value

    @property
    def content_changed(self):
        return self.content_canvas_buffer is None or self._content_changed

    @content_changed.setter
    def content_changed(self, value):
        self._content_changed = value

    @property
    def padding_changed(self):
        return self._padding_changed

    @padding_changed.setter
    def padding_changed(self, value):
        self._padding_changed = value

    @property
    def size_changed(self):
        return self._size_changed    

    @size_changed.setter    
    def size_changed(self, value):
        self._size_changed = value

    @property
    def border_changed(self):
        return self.border_canvas_buffer is None or self._border_changed

    @border_changed.setter
    def border_changed(self, value):
        self._border_changed = value

    @property
    def location_changed(self):
        return self._location_changed

    @location_changed.setter
    def location_changed(self, value):
        self._location_changed = value

    @property
    def z_changed(self):
        return self._z_changed

    @z_changed.setter
    def z_changed(self, value):
        self._z_changed = value
