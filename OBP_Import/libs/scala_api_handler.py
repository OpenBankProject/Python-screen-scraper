#!/usr/bin/env python
__author__ = ['Jan Alexander Slabiak (alex@tesobe.com)']
__license__ = """
  Copyright 2011 Music Pictures Ltd / TESOBE

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
This will contain a handler to insert JSON over a Scala Lift API to a database backend.
"""


import requests
from urllib2 import HTTPError



def check_scala_host_reachable(scala_api_host,scala_api_port):
    try:
        requests.get('http://'+scala_api_host+':'+scala_api_port+'/',timeout=5)
    except HTTPError:
        return None
    except:
        print "Can't connecte to Scala API! Check for Host, and Info!"
        raise
    

def insert_into_scala(scala_api_host,scala_api_port,JSON_to_insert):
    # This wil
    check_scala_host_reachable(scala_api_host,scala_api_port)
    headers = {'content-type': 'application/json'}
    post_request = requests.post("http://"+scala_api_host+":"+scala_api_port+"/api/transactions", 
                        data=JSON_to_insert,headers=headers)
    return post_request


def main():
    pass



if __name__ == '__main__':
    main()
