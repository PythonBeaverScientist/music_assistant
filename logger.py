from logging import config, getLogger

from config import settings

config.dictConfig(settings.LOG_CONFIG)
logger = getLogger(__name__)
