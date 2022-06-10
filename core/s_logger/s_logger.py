import logging


class ScraperLogger:
    def __init__(self, logger, train_id=None):
        self.logger = logger
        self._train_id = train_id

        self.logger.info("initializing data collection")

    @property
    def train_id(self):
        return self._train_id

    @train_id.setter
    def train_id(self, value: int):
        self._train_id = value

    def processing_train(self):
        self.logger.debug("[" + str(self._train_id) + "] " + "processing train")

    def loading_error(self, exception):
        self.logger.error("[" + str(self._train_id) + "] " + str(exception))
        # self.logger.error("[" + str(self._train_id) + "] couldn't load train")

    def unexpected_error(self, exception):
        self.logger.error("[" + str(self._train_id) + "] UNEXPECTED ERROR")
        self.loading_error(exception)

    def connection_established(self):
        self.logger.debug("[" + str(self._train_id) + "] connection established")

    def parsing_successful(self):
        self.logger.debug("[" + str(self._train_id) + "] parsing successful")

    def log_delay(self, delay):
        self.logger.info("[" + str(self._train_id) + "] " + str(delay))

    def new_delay(self):
        self.logger.debug("[" + str(self._train_id) + "] new delay saved")

    def old_delay(self):
        self.logger.debug("[" + str(self._train_id) + "] delay has already been recorded")

    def finalise(self, amount, missing):
        if missing:
            self.logger.warning(f"all delay data saved ({amount}), some are missing")
        else:
            self.logger.info(f"all delay data successfully saved ({amount})")