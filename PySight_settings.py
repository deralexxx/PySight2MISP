import configparser
import logging


# Initialize the config parser
config = configparser.ConfigParser()

# Read the config file and set config values
config.read('config.cfg')

# Fall back to log level "WARNING" if not specified.
LOG_LEVEL = config['general'].get('log_level', 'WARNING')

THREADING = config['general'].getboolean('use_threading', fallback=False)
# If threading is requested, set the number of threads according to the configuration.
# Otherwise only use one thread.
if THREADING:
    NUMBER_THREADS = config['general'].getint('number_threads', fallback=1)
else:
    NUMBER_THREADS = 1

ISIGHT_URL = config['isight'].get('isight_url')
ISIGHT_KEY = config['isight'].get('isight_pub_key')
ISIGHT_SECRET = config['isight'].get('isight_priv_key')
ISIGHT_ORG = config['isight'].get('isight_organization', '')
ISIGHT_VERIFYCERT = config['isight'].getboolean('isight_verifycert')
HOURS = config['isight'].getint('last_hours')

MISP_URL = config['MISP'].get('misp_url')
MISP_KEY = config['MISP'].get('misp_key')
MISP_VERIFYCERT = config['MISP'].getboolean('misp_verifycert', fallback=True)
misp_eventtags = config['MISP'].get('misp_eventtags')
if misp_eventtags == '' or misp_eventtags is None:
    MISP_EVENTTAGS = False
else:
    MISP_EVENTTAGS = misp_eventtags.split(',')

ISIGHT_PROXY = config['proxy'].getboolean('use_isight_proxy', fallback=False)
MISP_PROXY = config['proxy'].getboolean('use_misp_proxy', fallback=False)
if ISIGHT_PROXY or MISP_PROXY:
    PROXY_URL = config['proxy'].get('full', '')
    if PROXY_URL == '':
        print('Proxy usage requested but no proxy specified. Please check "config.cfg".')
        PROXIES = {}
    else:
        PROXIES = {
            "http": PROXY_URL,
            "https": PROXY_URL
        }
else:
    PROXIES = {}

DEBUG_MODE = False

# Create a logger.
logger = logging.getLogger('PySight')
# Set the loglevel, also for imported modules.
if LOG_LEVEL.upper() == 'DEBUG':
    logger.setLevel(logging.DEBUG)
    # Pymisp DEBUG logging would include the authorization key which we want to avoid
    logging.getLogger('pymisp').setLevel(logging.INFO)
    logging.getLogger('urllib3').setLevel(logging.DEBUG)
    DEBUG_MODE = True
elif LOG_LEVEL.upper() == 'INFO':
    logger.setLevel(logging.INFO)
    logging.getLogger('pymisp').setLevel(logging.INFO)
    logging.getLogger('urllib3').setLevel(logging.INFO)
elif LOG_LEVEL.upper() == 'WARNING':
    logger.setLevel(logging.WARNING)
    logging.getLogger('pymisp').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
elif LOG_LEVEL.upper() == 'ERROR':
    logger.setLevel(logging.ERROR)
    logging.getLogger('pymisp').setLevel(logging.ERROR)
    logging.getLogger('urllib3').setLevel(logging.ERROR)
elif LOG_LEVEL.upper() == 'CRITICAL':
    logger.setLevel(logging.CRITICAL)
    logging.getLogger('pymisp').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
else:
    print('Invalid logging level "%s". Using default level WARNING.' % LOG_LEVEL)
    logger.setLevel(logging.WARNING)
    logging.getLogger('pymisp').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

# Create a file handler and log there, too, in addition to the console.
log_file = logging.FileHandler('output.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_file.setFormatter(formatter)
logger.addHandler(log_file)
