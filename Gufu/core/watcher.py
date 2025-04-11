import functools

from telethon import events
from . import client

class Watcher:
    def __init__(self):
        self.watchers = {}

    def new(self):
        def decorator(func):
            self.watchers["new"] = func

            @functools.wraps(func)
            async def wrapper(event):
                await func(event)

            client.add_event_handler(wrapper, events.NewMessage())
            return wrapper

        return decorator

    def edited(self):
        def decorator(func):
            self.watchers["edited"] = func

            @functools.wraps(func)
            async def wrapper(event):
                await func(event)

            client.add_event_handler(wrapper, events.MessageEdited())
            return wrapper

        return decorator

watcher = Watcher()
