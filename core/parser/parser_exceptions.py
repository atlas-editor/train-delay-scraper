class ElementNotFoundError(Exception):

    def __init__(self, element, message):
        self.element = element
        self.message = message

    def __str__(self):
        return f"{self.message} (element={self.element})"


class TrainNotInTerminalError(Exception):

    def __init__(self, last_station, message):
        self.last_station = last_station
        self.message = message

    def __str__(self):
        return f"{self.message} (last station={self.last_station})"


class ArrivalDataLoadingError(Exception):

    def __init__(self, message):
        self.message = message
