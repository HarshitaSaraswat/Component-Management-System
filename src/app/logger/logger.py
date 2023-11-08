import logging
from elasticsearch import logger as es_logger
from .handlers import BaseStreamHandler, BaseRotatingFileHandler

es_logger.addHandler(BaseStreamHandler())
es_logger.addHandler(BaseRotatingFileHandler())

logger: logging.Logger = logging.getLogger("root")
logger.addHandler(BaseStreamHandler())
logger.addHandler(BaseRotatingFileHandler())
