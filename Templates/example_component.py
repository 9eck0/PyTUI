"""
This is a PyTUI template for custom component implementation.

--------------------------------

In order to render custom

To implement a custom skin, you need to overwrite the _renderer internal pointer to the rendering function
"""


from UI.Components.Component import Component


class ExampleComponent(Component):

    def __init__(self, width, height):
        super().__init__(width=width, height=height)

    def get_content_width(self) -> int:
        pass

    def get_content_height(self) -> int:
        pass

    def render_content(self, width, height):
        pass
