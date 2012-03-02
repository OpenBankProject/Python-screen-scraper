#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

__doc__ = """
This will contain a handler to insert JSON over a Scala Lift API to a database back-end.
Using liburl2 for Human, requests:
# LINK: http://kennethreitz.com/requests-python-http-module.html
"""


import requests
from debugger import obp_logger
from urllib2 import HTTPError


def check_scala_host_reachable(scala_api_host, scala_api_port):
    """
    Check for a reachable System of the Scala API Host.
    """

    obp_logger.debug("try to connect to api host")
    # Try to call the web root of the  scala_api_host
    try:
        obp_logger.debug("requested http://%s:%s/" % (scala_api_host, scala_api_port))
        result = requests.get('http://' + scala_api_host + ':' + scala_api_port + '/', timeout=5)
        obp_logger.debug("request result is: %s" % result)
        return result
    except:
        obp_logger.critical("ERROR! -  Can't connect to Scala API")
        obp_logger.critical("Check the API Host!")
        print "ERROR! -  Can't connect to Scala API!"
        print "Check the API Host!"
        raise


def insert_into_scala(scala_api_host, scala_api_port, JSON_to_insert):
    """
    Inserting JSON via HTTP POST into the API.
    """

    obp_logger.info("Insert JSON to Scala API")
    obp_logger.debug("test connection to Scala API Host")
    check_scala_host_reachable(scala_api_host, scala_api_port)

    # Set content-type to JSON in the HTTP Header
    headers = {'content-type': 'application/json'}
    obp_logger.debug("Set HTTP headers to: %s" % headers)
    post_request = requests.post("http://" + scala_api_host + ":" + scala_api_port + "/api/transactions",
                        data=JSON_to_insert, headers=headers)
    # Return the http status code.
    obp_logger.debug("Inserted to SCALA API")
    return post_request
