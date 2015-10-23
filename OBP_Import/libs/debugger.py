# -*- coding: utf-8 -*-
__doc__ = """
This a esay debugger that call a pdb.
"""
__author__ = ['Jan Alexander Slabiak (alex@tesobe.com)']
__license__ = """
    Copyright (C) 2011-2015, TESOBE / Music Pictures Ltd

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Email: contact@tesobe.com
    TESOBE / Music Pictures Ltd
    Osloerstrasse 16/17
    Berlin 13359, Germany
"""


import os
import pdb
import logging


def debug():
    pdb.set_trace()


LOGGER_PATH = os.path.join(os.getcwd() + '/log/')
LOG_FILE_NAME = './var/log/file.log'

#print "Logging messages to %s" % LOG_FILE_NAME

DEFAULT_LOGGER = "ImporterLogger"
LOG_FILENAME = "./var/log/%s.log" % DEFAULT_LOGGER
LOG_LEVEL = "DEBUG"
LOG_MSG_FORMAT = "%(asctime)s %(levelname)s %(filename)s:%(funcName)s(%(lineno)d) : %(message)s"
LOG_MSG_TIME_FORMAT = '[%d %h %Y - %H:%M:%S]'

logger = logging.getLogger(DEFAULT_LOGGER)
logger.setLevel(LOG_LEVEL)
handler = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter(LOG_MSG_FORMAT, LOG_MSG_TIME_FORMAT)
handler.setFormatter(formatter)
logger.addHandler(handler)


obp_logger = logging.getLogger(DEFAULT_LOGGER)
obp_logger.setLevel(logging.DEBUG)


obp_logger.info("Initialization obp_logger")
obp_logger.debug("obp_logger settings:")
obp_logger.debug("obp_logger path: %s" % LOGGER_PATH)
obp_logger.debug("obp_logger file: %s" % LOG_FILE_NAME)
