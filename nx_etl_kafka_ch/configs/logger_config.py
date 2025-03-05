import logging


class CustomFormatter(logging.Formatter):
    green = '\033[92m'
    yellow = '\033[93m'
    bold_red = '\033[91m'
    format = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.INFO: green + format,
        logging.WARNING: yellow + format,
        logging.ERROR: bold_red + format
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.NOTSET)
ch.setFormatter(CustomFormatter())

logger.addHandler(ch)
