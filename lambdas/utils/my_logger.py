import logging, os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

def get_logger(filename):
    logger = logging.getLogger(filename)
    logger.setLevel(logging.getLevelName(LOG_LEVEL))
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.getLevelName(LOG_LEVEL))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s() - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger