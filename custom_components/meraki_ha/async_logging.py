import logging
import threading


class QueueHandler(logging.Handler):
    """A logging handler that puts records into a queue."""

    def __init__(self, q):
        """Initialize the handler."""
        super().__init__()
        self.queue = q

    def emit(self, record):
        """Emit a record."""
        self.queue.put(record)


class QueueListener(threading.Thread):
    """A thread that listens for records on a queue and sends them to a handler."""

    def __init__(self, q, handler):
        """Initialize the listener."""
        super().__init__()
        self.queue = q
        self.handler = handler
        self.daemon = True

    def run(self):
        """Run the listener."""
        while True:
            try:
                record = self.queue.get()
                if record is None:
                    break
                self.handler.handle(record)
            except Exception as e:
                _LOGGER.error(f"Error handling log record: {e}")
