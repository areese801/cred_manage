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

        # itm = bw.get_vault_item_by_guid(guid=some_guid)
        # self.assertIsInstance(itm, dict)


        # # Ensure that we get an exception if we try to find an item with a bad GUID (one that doesn't exist)
        # self.assertRaises(ValueError, bw.get_vault_item_by_guid(guid='this_is_not_a_valid_GUID'))


    #TODO:  Implement this test
    # def test_get_credentials_by_guid(self):
    #     raise NotImplementedError
    #TODO:  Implement this test
    # def test_get_username_by_guid(self):
    #     raise NotImplementedError
    #TODO:  Implement this test
    # def test_get_password_by_guid(self):
    #     raise NotImplementedError

    def test_all_passwords_redacted(self):
        """
        Ensure that all of the passwords in the vault that is pinned to self have been redacted
        """
        vault_contents = make_bitwarden_container().vault_contents
        for i in vault_contents:
            creds = i['login']
            pw = creds['password']

            self.assertEqual(pw, '<password removed>')

    # TODO:  Implement this test
    def test_get_cred(self):
        
        # Make a container and get the credentials object
        obj = make_bitwarden_container()
        creds = obj.get_cred(guid=TEST_GUID)

        # Assert that credentials is a dict, with 'username' and 'password' keys and that the PW is NOT redacted
        self.assertIsInstance(creds, dict)
        self.assertIn('username', creds)
        self.assertIn('password', creds)
        self.assertNotEqual(creds['password'], '<password removed>')
    
    
    def test_set_cred(self):
        self.assertRaises(NotImplementedError)  # At this time (2021-11-08), we're not bothering to implement this method 

    #TODO:  Implement this test
    # def test_delete_cred(self):
    #     raise NotImplementedError

        