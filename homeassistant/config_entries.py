class ConfigEntry:
    def __init__(self):
        self.entry_id = "test_entry"
        self.options = {}


class ConfigEntryNotReady(Exception):
    pass
