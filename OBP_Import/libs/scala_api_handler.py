#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
