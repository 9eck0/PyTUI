"""
Internal functions and algorithms for TUI compositing and rendering.

This file exists to centralize internal rendering code, as well as alleviating code readability burden from class
definition files.

----------------------------------------------------------------

To render a frame of the TUI canvas, a rendering pipeline must be followed in a specific order, optimized for performance
and controlled by multiple rendering parameters.

Control parameters are (in no particular order):
    - Depth positioning (z-index), 0 is lowest.
    - Visibility
    - Background color (transparency)
    - 

----------------------------------------------------------------

The TUI general rendering pipeline is as follows:
    - Build z-stack: from z=0 and incrementing; sort by z-index, then by order of occurrence; z=None are topmost
      by order of occurrence.
    - Visibility tracing: determine visible components from their bounds and exclusivity mode.
    - Background buffer compositing: composes/caches background color buffer of each canvas, for transparency rendering.
    - Canvas compositing: using background color buffer, renders each visible component.
      Inner content rendering is controlled by each component separately.
    - Canvas post-processing (if available)
    - Screen compositing: layers all visible components to compose the final screen.
    - Screen post-processing (if available)
    - Final rendering: renders the TUI screen as a string.
Each step is cached if possible for better performance.

----------------------------------------------------------------

Some processes, such as video rendering, may employ an exclusive-mode rendering pipeline for expedited performance.
In exclusive mode, only the process window is visible, akin to traditional fullscreen mode.

The exclusive-mode pipeline is defined as follows:
    - Content rendering: controlled by custom process
    - Fullscreen canvas compositing: direct string manipulation render techniques.
      Used for e.g. adding a border around the content.
"""


import sys

from System import Terminal as term
from System.Rendering.FragmentCanvas import FragmentCanvas
from UI import Appearance
from UI.ABC.BaseComponent import BaseComponent
from Utils.ListHelper import longest_list_length


#region ================================ Utility functions ================================


def infill_bounds(comp: list[str]):
    width = longest_list_length(comp)
    height = len(comp)


def concat_UI(base_frame: list[str], top_elem: list[str], x: int, y: int):
    """
    Inserts an UI component on top of a larger base frame.
    This function will limit the resulting composition to within the bounds of the base frame, cutting off parts
    of top_elem exceeding these bounds.

    :param base_frame: The bottom frame render.
    :param top_elem: The component to insert onto the base frame.
    :param x: The horizontal coordinate for insertion, incremental from left to right.
    :param y: The vertical coordinate for insertion, incremental from top to bottom.
    :return: The resulting UI render, as a list of lines/str.
    :rtype: list[str]
    """

    # Convert to FragmentCanvas

    #


def concat_UI_strings(base_frame: str, top_elem: str, x: int, y: int):
    comp = base_frame.split('\n')
    insertion = top_elem.split('\n')
    return '\n'.join(concat_UI(comp, insertion, x, y))


#endregion


#region ================================ Layout Composition ================================
"""
Layout composition is the first step in the TUI rendering pipeline, and is responsible for the following tasks:
    - Build z-stack: from z=0 and incrementing; sort by z-index, then by order of occurrence; z=None are topmost
      by order of occurrence.
    - Visibility tracing: determine visible components from their bounds and exclusivity mode.
"""


foreground_mask : FragmentCanvas = FragmentCanvas.empty_canvas()


def is_out_of_bounds(component: BaseComponent) -> bool:
    """
    Checks whether the specified UI component is out of bounds of the TUI window.
    :param component: The UI component to check.
    :return: True if the component is out of bounds, False otherwise.
    """
    window_width, window_height = term.get_window_size()
    return component.location[0] < 0 or component.location[1] < 0 or \
        component.location[0] >= window_width or component.location[1] >= window_height


def is_hidden_by(this, other: BaseComponent) -> bool:
    """
    Checks whether this UI component is fully shadowed by another one
    :param this: The target component to check.
    :param other: Another component to check against.
    :return: True if the component is shadowed, False otherwise.
    """
    if this.z_index > other.z_index:
        return False
    # Top left X
    if this.location[0] < other.location[0]:
        return False
    # Top left Y
    if this.location[1] < other.location[1]:
        return False
    # Bottom right X
    if this.location[0] + this.width > other.location[0] + other.width:
        return False
    #Bottom right Y
    if this.location[1] + this.width > other.location[1] + other.width:
        return False
    return True


#endregion


#region ================================ Component Rendering ================================


def canvas_integrity_checks(canvas: FragmentCanvas, silent: bool = False):
    """
    Checks for rendering issues present within a FragmentCanvas instance.
    This check is necessary due to the support for custom UI renderers.

    :param canvas: The FragmentCanvas instance to check.
    :param silent: True to suppress any error messages and exceptions raised.
    :return: Whether an integrity violation has been detected during the checkup.
    """

    detection_result = False

    if not isinstance(canvas, FragmentCanvas):
        if not silent:
            err = TypeError("Rendering error: expected instance or subclass of FragmentCanvas; obtained '"
                  + str(type(canvas))
                  + "' instead.")
            err.add_note("This error is most likely caused by a custom UI renderer.")
            raise err
        return True

    return detection_result


def component_integrity_validation(component: BaseComponent, fix_errors: bool = False, silent: bool = False):
    """
    Checks for and fixes incorrect or corrupt internal fields and properties on an UI component, ensuring rendering
    pipeline consistency.

    :param component: The BaseComponent instance to validate.
    :param fix_errors: True to attempt to fix any detected issues, if possible.
    :param silent: True to suppress any error messages and non-critical exceptions raised.
    :return: Whether an integrity violation has been detected during the checkup.
    """

    detection_result = False

    # 1) Base checks

    if not isinstance(component, BaseComponent):
        # Critical error: not a supported UI component
        raise TypeError("Rendering error: expected instance or subclass of BaseComponent; obtained '"
                        + str(type(component))
                        + "' instead.")

    # 2) Property values validity checks

    if component.width < 0 or component.height < 0:
        detection_result = True
        if not silent:
            print("Invalid UI component size: component width and height must be positive integers.", file=sys.stderr)
        if fix_errors:
            component.width = max(0, component.width)
            component.height = max(0, component.height)

    # 2) Canvas is properly instanced

    """
    if type(component._base_canvas) is not FragmentCanvas:
        detection_result = True
        if not silent:
            print("Rendering error: expected instance or subclass of FragmentCanvas; obtained '"
                  + str(type(component._base_canvas))
                  + "' instead.", file=sys.stderr)
        if fix_errors:
            component._base_canvas = FragmentCanvas(component.width, component.height)
    """

    # 3) Properties: Border

    return detection_result


def render_border_internal(width: int, height: int, border: Appearance.BorderStyle):

    # 0) ======== Minimum size check ========

    if width < 2 or height < 2:
        return FragmentCanvas.empty(width, height)

    # 1) ======== Build border string ========
    # Note the use of strip() to exclude empty top/bottom borders

    border_str = border.top_left + border.top_center * (width-2) + border.top_right + "\n" + \
                 (border.middle_left + " " * (width-2) + border.middle_right + "\n") * (height-2) + \
                 border.bottom_left + border.bottom_center * (width-2) + border.bottom_right
    border_str = border_str.strip()

    # 2) ======== Convert to FragmentCanvas ========

    return FragmentCanvas.from_string(border_str)


def render_component_internal(component: BaseComponent) -> FragmentCanvas:

    # 0) ======== Integrity checks on internals ========

    if component is None:
        return FragmentCanvas.empty(0, 0)

    component_integrity_validation(component, fix_errors=True)

    # 1) ======== Preprocessing properties ========

    if not component.visible:
        # Component is invisible, returns an empty canvas with null size.
        # Note this design decision may affect the layout of auto-sizing parent containers.
        return FragmentCanvas.empty(0, 0)

    # 2) ======== Render UI content ========

    if component._state_indicators.content_changed:
        content_fragment = component.render_content()
        component._state_indicators.content_canvas_buffer = content_fragment                      # Update content canvas buffer
    else:
        content_fragment = component._state_indicators.content_canvas_buffer
    if canvas_integrity_checks(content_fragment):
        content_fragment = FragmentCanvas.empty(component.width, component.height)

    # Adaptive width and height handling
    content_width = content_fragment.width if component.adaptive_width else component.width
    content_height = content_fragment.height if component.adaptive_height else component.height

    # 3) ======== Render border ========
    # Surround border: paste content into border canvas
    # Inset border: paste border on top of content canvas

    if component._state_indicators.border_changed:
        if component.border is not None or component.border != Appearance.BorderTypes.NoBorder:
            border_fragment = render_border_internal(content_width, content_height, component.border)
            component._state_indicators.border_canvas_buffer = border_fragment
        else:
            component._state_indicators.border_canvas_buffer = None

    # 4) ======== Compose component ========

    render_canvas: FragmentCanvas = None
    if component._state_indicators.border_canvas_buffer is not None:
        render_canvas = component._state_indicators.border_canvas_buffer
        render_canvas.draw((1, 1), content_fragment)
    else:
        render_canvas = content_fragment

    return render_canvas

#endregion


def render_color(elem: BaseComponent):
    pass


