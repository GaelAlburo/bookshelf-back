import logging as log


class Logger:
    def __init__(self, log_file="bookshelf_api.log", level=log.INFO):
        log.basicConfig(
            level=level,
            format="%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s",
            datefmt="%I:%M:%S %p",
            handlers=[
                log.FileHandler(log_file),  # Logs to bookshelf_api.log file
                log.StreamHandler(),  # Logs to console
            ],
        )
        self.logger = log.getLogger()

    def debug(self, message):
        self.logger.debug(
            message, stacklevel=2
        )  # stack_level=2 to get the correct line number

    def info(self, message):
        self.logger.info(message, stacklevel=2)

    def warning(self, message):
        self.logger.warning(message, stacklevel=2)

    def error(self, message):
        self.logger.error(message, stacklevel=2)

    def critical(self, message):
        self.logger.critical(message, stacklevel=2)


if __name__ == "__main__":
    logger = Logger()
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
