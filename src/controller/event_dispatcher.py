from lib.weak_bound_method import WeakBoundMethod as Wbm


class EventDispatcher:
    """ Handles the sending of events 
        and their subscription
    """

    def __init__(self):
        # Contains event classes and the object method 
        # subscribed to said event.
        self.listeners = dict()


    def add(self, eventcls, listener):
        """ Suscribes a listener to an specific Event class.

            Recives:
                eventcls:<Event.__class__>
                listener:<BoundMethod>
        """

        listener = Wbm(listener)

        # If the event is not in the dictionary, 
        # it is added and subscribed to by the listener.
        self.listeners.setdefault(eventcls, list()).append(listener)

    
    def remove(self, eventcls, listener):
        key = eventcls.__name__
        self._listeners[key].remove(listener)


    def post(self, event):
        """ Sends an event instance to their suscribers.

                Recives:
                    event:<Event>
        """

        if self.listeners.get(event.get_class(), False):
            for listener in self.listeners[event.get_class()]:
                listener(event)