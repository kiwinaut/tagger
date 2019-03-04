import logging
from config import CONFIG

LOGFILE = CONFIG['logger.path']

logger = logging.getLogger('indexer')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)s:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.FileHandler(LOGFILE)
fh.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)s|%(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)