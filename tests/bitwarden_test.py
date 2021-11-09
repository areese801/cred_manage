"""
Unit tests for bitwarden.py
See:  https://code.visualstudio.com/docs/python/testing
"""

import unittest
from cred_manage.bitwarden import BitwardenCredContainer
from cred_manage.bitwarden import make_bitwarden_container
from cred_manage.bitwarden import API_KEY_FLAT_FILE

TEST_GUID = "755bb142-1d9d-44cf-8f74-ac600149633c"

class Test_BitwardenCredContainer(unittest.TestCase):
    

    def test_get_vault_item_by_guid(self):
        bw_cc = make_bitwarden_container()

        # Ensure we get a string back when passing in a valid GUID to read.  
        some_guid = bw_cc.vault_contents[0]['id']

        bw_item = bw_cc.get_vault_item_by_guid(guid=some_guid)
        self.assertIsInstance(bw_item, dict)

    def test_get_vault_item_by_guid_w_bad_guid(self):
        bw_cc = make_bitwarden_container()

        # Ensure we get a an exception when we seek a non-existent guid.  Note the way we pass args into assertRaises
        # There may be a way to pass in named arguments but this will suffice for now
        rubbish_guid = "This is not a real guid.  it's fake rubbish"
        self.assertRaises(ValueError, bw_cc.get_vault_item_by_guid, rubbish_guid)
        

    # def test_get_credentials_by_guid(self):
    #     raise NotImplementedError
    
    
    #TODO:  Implement this test
    def test_get_username_by_guid(self):
        # Make a container and get the password for the test GUID
        obj = make_bitwarden_container()
        pw = obj.get_username_by_guid(guid=TEST_GUID)

        self.assertIsInstance(pw, str)
    
    def test_get_password_by_guid(self):
        # Make a container and get the password for the test GUID
        obj = make_bitwarden_container()
        pw = obj.get_password_by_guid(guid=TEST_GUID)

        self.assertIsInstance(pw, str)
        self.assertNotEqual(pw, '<password removed>')

    def test_all_passwords_redacted(self):
        """
        Ensure that all of the passwords in the vault that is pinned to self have been redacted
        """
        vault_contents = make_bitwarden_container().vault_contents
        for i in vault_contents:
            creds = i['login']
            pw = creds['password']

            self.assertEqual(pw, '<password removed>')

    def test_get_cred(self):
        #  Note that this is just a wrapper around get_password_by_guid, but it is defined in the superclass and 
        #  Intended to be overridden
        
        # Make a container and get the credentials object
        obj = make_bitwarden_container()
        creds = obj.get_cred(guid=TEST_GUID)

        # Assert that credentials is a dict, with 'username' and 'password' keys and that the PW is NOT redacted
        self.assertIsInstance(creds, dict)
        self.assertIn('username', creds)
        self.assertIn('password', creds)
        self.assertNotEqual(creds['password'], '<password removed>')
    