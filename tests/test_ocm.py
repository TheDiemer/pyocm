import unittest
import configparser
import json
import os

from pyocm import pyocm

# TEST DATA
DEBUG = os.getenv("DEBUG_TESTING", False)
INDENT = os.getenv("DEBUG_INDENT_NUMBER", 4)
ACCOUNT_NUMBER = os.getenv("DEBUG_ACCOUNT_NUMBER", "540155")
ORG_ID = os.getenv("DEBUG_ORG_ID", "1GXbLc45FSS70m9GxEULgCiwAxr")
CREATOR_ID = os.getenv("DEBUG_CREATOR_ID", "1Hm2PJLFvmHsmD6JsgdUW50miyR")
CLUSTER_ID = os.getenv("DEBUG_CLUSTER_ID", "dd25964a-0832-4d7c-be99-b11adab46b37")


class TestOCM(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config.read('tests/test_config.cfg')

        self.ocm = pyocm.ocm_api(token=config.get('ocm', 'token'))


    @unittest.skipUnless(DEBUG, "skipping manual debugging test")
    def test_org_by_account(self):
        r = self.ocm.get_org_by_account(ACCOUNT_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
        self.assertTrue(True)
   

    @unittest.skipUnless(DEBUG, "skipping manual debugging test")
    def test_account_by_org(self):
        r = self.ocm.get_account_by_org(ORG_ID)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
        self.assertTrue(True)
   

    @unittest.skipUnless(DEBUG, "skipping manual debugging test")
    def test_subs_by_creator(self):   # Subs is clusters
        r = self.ocm.get_subs_by_creator(CREATOR_ID)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
        self.assertTrue(True)
    

    @unittest.skipUnless(DEBUG, "skipping manual debugging test")
    def test_subs_by_cluster(self):   # Subs is clusters
        r = self.ocm.get_subs_by_cluster_id(CLUSTER_ID)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
        self.assertTrue(True)
   
    @unittest.skipUnless(DEBUG, "skipping manual debugging test")
    def test_user_account_info(self): 
        r = self.ocm.get_current_account()
        print(json.dumps(r,sort_keys=True, indent=INDENT))
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
