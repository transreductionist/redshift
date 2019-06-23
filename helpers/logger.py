import logging

logging.basicConfig(level=logging.DEBUG)

def log(message):
    logging.debug('*****')
    logging.debug('***** {}'.format(message))
    logging.debug('*****')
