"""
Unit tests for flat_file.py
See:  https://code.visualstudio.com/docs/python/testing
"""


import unittest
from cred_manage.flat_file import FlatFileCredContainer
import os

FLAT_FILE_THAT_EXISTS='/tmp/file_that_exist.txt'
FLAT_FILE_THAT_DOES_NOT_EXIST='/tmp/file_that_not_exists.txt'

def setUpModule():
    """
    Boilerplate to ensure the conditions are right for these tests
    """

    # See that there is a flat file that actually exists
    with open(FLAT_FILE_THAT_EXISTS, 'w') as f:
        f.write("There is content in this file.\n")


    # Ensure that there is no such file on disk with the name in FLAT_FILE_THAT_DOES_NOT_EXIST
    if os.path.exists(FLAT_FILE_THAT_DOES_NOT_EXIST):
        os.remove(FLAT_FILE_THAT_DOES_NOT_EXIST)

def tearDownModule():
    """
    Post-testing cleanup 
    """

    # Clean up the flat file we generated as part of setUpModule

    if os.path.exists(FLAT_FILE_THAT_EXISTS):
        os.remove(FLAT_FILE_THAT_EXISTS) # It exists no longer


class Test_FlatFileCredContainer(unittest.TestCase):

    def test_init_with_bad_file_name(self):
        """
        Assert that a FileNotFoundError is raised when we try to init FlatFileCredContainer with a bad file name
        """

        self.assertRaises(FileNotFoundError, FlatFileCredContainer, file_path=FLAT_FILE_THAT_DOES_NOT_EXIST)

    def test_init_with_valid_file_name(self):
        """
        Assert that no Exceptions are raised by __ini__ for FlatFileCredContainer when instantiating with a valid file name 
        """

        # Armed with a file that exists, init the object.  We expect no exceptions to be raised
        try:
            o = FlatFileCredContainer(file_path=FLAT_FILE_THAT_EXISTS, allow_broad_permissions=True)
        except Exception as ex:
            self.fail(f"An unexpected exception occurred when instantiating the FlatFileCredContainer during the test:  {str(type(ex))}")

    def test_get_cred_method_implemented(self):
        """
        Asserts that the get_cred method has been implemented.  
        The superclass will raise a NotImplementedError otherwise
        """

        o = FlatFileCredContainer(file_path=FLAT_FILE_THAT_EXISTS, allow_broad_permissions=True)
        try:
            c = o.get_cred(self)
        except NotImplementedError as ex:
            self.fail(f"The get_cred() method has not been implemented in the subclass: {type(o)}")




    #TODO:  Add a test to see that set cred is implemented

    #TODO:  Add a test to see that delete cred is implemented