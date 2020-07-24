#!/bin/python

import time
import requests
from concurrent.futures import ThreadPoolExecutor

class ocm_api:
    """."""
    def __init__(self, api="https://api.openshift.com/api/",
            ca_path="/etc/pki/tls/certs/ca-bundle.crt", token=None):

        if token is None:
            raise Exception("Token was not supplied.")

        # Provide a method of automatically refreshing the auth bearer token, if a long-running
        # function happens to exist. This will occur every 5 minutes.
        self.offline_token = token
        self.last_token_refresh_time = 0.00

        self.thread_pool = ThreadPoolExecutor(4)
        self.base_api_uri = api
        self.auth_token = self.__confirm_auth(token)

        self.ca_certificate_path = ca_path
        if ca_path == False: # Used to Disable SSL warning (from each api call)
            requests.packages.urllib3.disable_warnings()


    def __del__(self):
        if self.thread_pool:
            self.thread_pool.shutdown(wait=True)


    def __confirm_auth(self, token):
        endpoint = 'https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token'
        r = requests.post(endpoint,
                data={'grant_type': 'refresh_token',
                    'client_id':'cloud-services',
                    'refresh_token': token})

        if r.status_code != 200:
            if r.status_code == 400:
                if r.json().get('error_description') == 'Offline user session not found':
                    raise Exception("""OFFLINE Token Expired! Please update your config with a new token from: {}\n"
                        Error Code: {}""".format('https://cloud.redhat.com/openshift/token', r.status_code))
            else:
                raise Exception("""looking up infomation from: {}\n"
                        Error Code: {}""".format(endpoint, r.status_code))

        self.last_token_refresh_time = time.time()
        return r.json()['access_token']


    def __call_api(self, endpoint, parameters=None):
        # Conditionally refresh the auth token
        timediff = time.time() - self.last_token_refresh_time
        if  timediff > 300:
            print('Refreshing auth token')
            self.auth_token = self.__confirm_auth(self.offline_token)

        r = requests.get("{}/{}".format(self.base_api_uri, endpoint),
                params=parameters, verify=self.ca_certificate_path,
                headers={'Accept': 'application/json',
                    'Authorization': 'Bearer {}'.format(self.auth_token),
                    'User-Agent': 'pythonCall'})

        if r.status_code == 204:
            return []
        if r.status_code != 200:
            raise Exception('''looking up infomation from: {}\n
                    Error Code: {}\n {}'''.format(endpoint, r.status_code, r.url))

        return r.json()

    def get_current_account(self):
        return self.__call_api('accounts_mgmt/v1/current_account')


    def get_org_by_id(self, organization_id):
        return self.__call_api('accounts_mgmt/v1/organizations/{}'.format(organization_id))


    def get_org_by_account(self, account_number):
        return self.__call_api('accounts_mgmt/v1/organizations',
                parameters={'search': 'ebs_account_id=\'{}\''.format(account_number)})


    def get_account_by_org(self, organization_id):
        return self.__call_api('accounts_mgmt/v1/accounts',
                parameters={'search': 'organization_id=\'{}\''.format(organization_id)})


    def get_account_by_creator(self, creator_id):
        return self.__call_api('accounts_mgmt/v1/accounts/{}'.format(creator_id))


    # Subscriptions (subs) will give you clusters!
    def get_subs_by_creator(self, creator_id):
        return self.__call_api('accounts_mgmt/v1/subscriptions',
                parameters={'search': 'creator_id=\'{}\''.format(creator_id)})


    def get_subs_by_cluster_id(self, cluster_id):
        return self.__call_api('accounts_mgmt/v1/subscriptions',
                parameters={'search': 'external_cluster_id=\'{}\''.format(cluster_id)})


    def get_subscriptions(self, params=None):
        """Provides a paged function for retrieving subscriptions.
            For full API definition, see 'accounts_mgmt/v1/subscriptions' on
            https://api.openshift.com/?urls.primaryName=Accounts%20management%20service
            'params' is a dictionary with the following possible elements.
                size: Maximum number of records to return. Default is 100.
                page: Page number of record list when record list exceeds specified page size.
                      Default is 1.
                search: A SQL-like where clause to filter results.
            Note: More options than this are available. See the service definition mentioned above.
        """
        # Set default page and size parameters, if not specified.
        if not params:
            params = {
                'page': 1,
                'size': 100
            }

        if 'page' not in params.keys():
            params['page'] = 1
        if 'size' not in params.keys():
            params['size'] = 100

        return self.__call_api('accounts_mgmt/v1/subscriptions', parameters=params)
