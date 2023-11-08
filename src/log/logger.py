import logging

import urllib3
from elasticsearch import logger as es_logger

from .handlers import BaseRotatingFileHandler, BaseStreamHandler

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

es_logger.addHandler(BaseStreamHandler())
es_logger.addHandler(BaseRotatingFileHandler())

logger: logging.Logger = logging.getLogger("root")
logger.addHandler(BaseStreamHandler())
logger.addHandler(BaseRotatingFileHandler())
