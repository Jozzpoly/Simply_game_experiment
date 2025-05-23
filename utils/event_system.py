"""
Event system for game events
"""

class EventSystem:
    """Simple event system for game events"""
    
    def __init__(self):
        """Initialize the event system"""
        self.listeners = {}
        
    def add_listener(self, event_type, callback):
        """
        Add a listener for an event type
        
        Args:
            event_type (str): The type of event to listen for
            callback (function): The function to call when the event is dispatched
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
        
    def remove_listener(self, event_type, callback):
        """
        Remove a listener
        
        Args:
            event_type (str): The type of event to remove the listener from
            callback (function): The function to remove
        """
        if event_type in self.listeners and callback in self.listeners[event_type]:
            self.listeners[event_type].remove(callback)
            
    def dispatch(self, event_type, **kwargs):
        """
        Dispatch an event to all listeners
        
        Args:
            event_type (str): The type of event to dispatch
            **kwargs: Additional data to pass to the listeners
        """
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(**kwargs)
