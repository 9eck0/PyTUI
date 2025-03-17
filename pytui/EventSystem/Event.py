"""
All base classes for event system implementation are found herein.

The event system is designed around the observer pattern to register and link event providers and consumers together.


EventArgs:
    A container for passing data across event handlers during trigger.

Event:
    Implementing the observer pattern, it acts as the main
"""

from inspect import signature
from typing import Callable, Any


#region ======================== Template class: EventArgs ========================

class EventArgs:
    """
    Container for passing event-related data to event handlers.
    """

    def __init__(self, **kwargs):
        """
        Initialize a generic EventArgs container with custom parameters
        in the form of named key-value pairs.

        :param kwargs: any keyed value(s) to store in this container.
        """
        self.__dict__.update(kwargs)

#endregion Template class: EventArgs


#region ======================== Template class: EventListener ========================

class Event:
    """
    Manages event subscriptions and invocation.

    This is the base class for implementing new event listeners with custom EventArgs subclasses.
    """

    def __init__(self, *subscribers: Callable[[Any, EventArgs], None]):
        # Subscribers (function delegates) to this event listener are stored here.
        self.subscribers = set()

        for method in subscribers:
            self.subscribe(method)

    def __iadd__(self, subscriber: Callable[[Any, EventArgs], None]):
        # Calling += on this class will call the __iadd__ magic method.
        self.subscribe(subscriber)
        return self

    def __isub__(self, subscriber: Callable[[Any, EventArgs], None]):
        self.unsubscribe(subscriber)
        return self

    def __len__(self):
        return len(self.subscribers)

    def __repr__(self):
        return f"{str(type(self))}{self.subscribers}"

    def subscribe(self, handler: Callable[[Any, EventArgs], None]):
        """
        Subscribe an event handler to this event.

        An event handler is a callable method which will be invoked once an event it is subscribed to is triggered.
        The event handler's method signature must receive two pieces of information:
          - a sender object, which is a reference to the publisher object
          - an EventArgs container, which passes along event-specific data to the event handler

        Example event handler signature:
          def my_event_handler(self, sender, args: EventArgs)

        :param handler: a callable reference to the event handler method
        """

        if not isinstance(handler, Callable):
            raise TypeError("{!r} is not a callable method".format(handler))
        nb_params = len(signature(handler).parameters)
        if nb_params < 2:
            raise TypeError("A valid event handler method must possess at least 2 function parameters."
                            "{0!r} possesses {1}".format(handler.__name__, nb_params))

        if handler not in self.subscribers:
            self.subscribers.add(handler)

    def unsubscribe(self, handler: Callable[[Any, EventArgs], None]):
        if handler in self.subscribers:
            self.subscribers.remove(handler)

    def invoke(self, sender, args: EventArgs):
        """
        Invokes the current event and notifies all its subscribers.

        :param sender: an object reference to the original publisher of the event
        :param args: an EventArgs data container
        """
        if args is None:
            args = EventArgs()
        for subscriber in self.subscribers:
            subscriber(sender, args)

#endregion Template class: EventListener
