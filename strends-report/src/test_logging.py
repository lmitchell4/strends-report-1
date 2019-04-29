# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 10:34:52 2019
put in __init__.py

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


@author: jsaracen
"""

import logging
#import logging.handlers
from logging.config import fileConfig


def setup_logger(logconfig='logging_config.ini'):
    #logfile="strends.log",
    fileConfig(logconfig)
    logger = logging.getLogger()
    logger.debug('Test message: %s', 'I am logging...')
    return

setup_logger()
