import logging
import sys


# logger = logging.getLogger('app')
# formatter = logging.Formatter(
#     # fmt='%(asctime)s - %(levelname)s - %(message)s'
#     fmt="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)3d %(levelname)-8s - %(message)s"
# )
# stream_handler = logging.StreamHandler(sys.stdout)
# # file_handler = logging.FileHandler('app.log')
# stream_handler.setFormatter(formatter)
# # file_handler.setFormatter(formatter)
# logger.handlers = [stream_handler]
# logger.setLevel(logging.DEBUG)


class ColorFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""
    # Microsoft ColorTool
    # grey = '\x1b[38;21m'
    green = "\x1b[1;32m"
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    format = "[%(asctime)s.%(msecs)03d] — %(levelname)-5s — %(module)10s:%(lineno)3d — %(message)s"

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: red + format + reset
    }

    def format(self, record):
        record.levelname = 'WARN' if record.levelname == 'WARNING' else record.levelname
        record.levelname = 'ERROR' if record.levelname == 'CRITICAL' else record.levelname
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(
            log_fmt,
            datefmt='%Y-%m-%d %H:%M:%S',
            # datefmt='%H:%M:%S',
        )
        return formatter.format(record)


logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(ColorFormatter())
logger.addHandler(stream_handler)
