#!/bin/python

import requests
from concurrent.futures import ThreadPoolExecutor

class ocm_api:
    """."""
    def __init__(self, api="https://api.openshift.com/api/",
            ca_path="/etc/pki/tls/certs/ca-bundle.crt",
            username=None,
            password=None):
        if (username is None) or (password is None):
            raise Exception("Username or Password were not supplied.")

        self.base_api_uri = api
        self.username = username
        self.password = password
        self.ca_certificate_path = ca_path

        if ca_path == False:
            requests.packages.urllib3.disable_warnings()

        self.thread_pool = ThreadPoolExecutor(4)

    def __del__(self):
        self.thread_pool.shutdown(wait=True)

    def __call_api(self, endpoint, parameters=None):
        authentication = (self.username, self.password)

        r = requests.get("{0}/{1}".format(self.base_api_uri, endpoints),
                params=parameters,
                auth=authentication,
                verify=self.ca_certificate_path)
        if r.status_code == 204:
            return []
        if r.status_code != 200:
            # do errors
        return r.json()
