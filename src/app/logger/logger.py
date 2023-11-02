import logging

from .handlers import RootHandler

# logging.getLogger('werkzeug').addHandler(WerkzeugHandler.StreamHandler())
# logging.getLogger('werkzeug').addHandler(WerkzeugHandler.RotatingFileHandler())

logger: logging.Logger = logging.getLogger("root")
logger.addHandler(RootHandler.StreamHandler())
logger.addHandler(RootHandler.RotatingFileHandler())
