# import logging
#
#
# class CustomFormatter(logging.Formatter):
#     """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""
#
#     grey = '\x1b[38;21m'
#     blue = '\x1b[38;5;39m'
#     yellow = '\x1b[38;5;226m'
#     red = '\x1b[38;5;196m'
#     bold_red = '\x1b[31;1m'
#     reset = '\x1b[0m'
#
#     def __init__(self, fmt):
#         super().__init__()
#         self.fmt = fmt
#         self.FORMATS = {
#             logging.DEBUG: self.grey + self.fmt + self.reset,
#             logging.INFO: self.blue + self.fmt + self.reset,
#             logging.WARNING: self.yellow + self.fmt + self.reset,
#             logging.ERROR: self.red + self.fmt + self.reset,
#             logging.CRITICAL: self.bold_red + self.fmt + self.reset
#         }
#
#     def format(self, record):
#         log_fmt = self.FORMATS.get(record.levelno)
#         formatter = logging.Formatter(log_fmt)
#         return formatter.format(record)
#
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
#
# fmt = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
# FORMAT = "[%(levelname)s]\t[%(filename)s:%(funcName)s():%(lineno)s]: %(message)s"
# # Create stdout handler for logging to the console (logs all five levels)
# stdout_handler = logging.StreamHandler()
# stdout_handler.setLevel(logging.DEBUG)
# stdout_handler.setFormatter(CustomFormatter(FORMAT))
#
# # Create file handler for logging to a file (logs all five levels)
# # today = date.today()
# # file_handler = logging.FileHandler('my_app_{}.log'.format(today.strftime('%Y_%m_%d')))
# # file_handler.setLevel(logging.DEBUG)
# # file_handler.setFormatter(logging.Formatter(fmt))
#
# # Add both handlers to the logger
# logger.addHandler(stdout_handler)
# # logger.addHandler(file_handler)
#
# # logger.basicConfig(format=FORMAT, level=logging.DEBUG)
import sys

from loguru import logger

log_format = (
    "<level>{level: <8}</level> | "
    "<cyan>[{file.name}]</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)
logger = logger.patch(lambda record: record.update(name=record["file"].name))

logger.remove()
logger.add(sys.stderr, colorize=True, format=log_format, level="DEBUG")

