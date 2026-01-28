from functools import wraps


class HomeAssistant:
    def __init__(self):
        self.data = {}
        self.config_entries = type("CE", (), {"async_reload": lambda *a, **k: None})()
        self.config = type("C", (), {"entries": None})()


def callback(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
