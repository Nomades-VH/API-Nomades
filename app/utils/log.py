import inspect
import logging


# TODO: Implementar o sistema de log no sistema INTEIRO
class Log:
    def __init__(self, level: int = logging.DEBUG):
        logging.basicConfig(filename="app.log", level=level)
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        self.logger = logging.getLogger(mod.__name__)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def exception(self, message: str):
        self.logger.exception(message)

    def critical(self, message: str):
        self.logger.critical(message)

    def error(self, message: str):
        self.logger.error(message)
