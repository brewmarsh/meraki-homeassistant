class CoordinatorEntity:
    def __init__(self, coordinator=None):
        self.coordinator = coordinator

    @property
    def available(self):
        return True
