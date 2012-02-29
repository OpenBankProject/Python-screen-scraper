# -*- coding: utf-8 -*-
__doc__ = """
This a esay debugger that call a pdb.
"""
__author__ = ['Jan Alexander Slabiak (alex@tesobe.com)']
__license__ = """
  Copyright 2011/2012 Music Pictures Ltd / TESOBE

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


import os
import pdb
import logging

def debug():
    pdb.set_trace()


LOGGER_PATH = os.path.join(os.getcwd() + '/log/')
print LOGGER_PATH
LOG_FILE_NAME = './var/log/file.log'

logging.basicConfig(
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s:%(funcName)s(%(lineno)d) : %(message)s',
                    filename=LOG_FILE_NAME,
                    filemode='a',
                    datefmt='[%d %h %Y - %H:%M:%S]')

#print "Logging messages to %s" % LOG_FILE_NAME


class NoParsingFilter(logging.Filter):
    def filter(self, record):
        #debug()
        return not record.getMessage().startswith('POST')


logger = logging.getLogger(LOGGER_PATH)
logger.setLevel(logging.DEBUG)
logger.addFilter(NoParsingFilter())

logger.info("Initialization logger")
logger.debug("logger settings:")
logger.debug("logger path: %s" % LOGGER_PATH)
logger.debug("logger file: %s" % LOG_FILE_NAME)


