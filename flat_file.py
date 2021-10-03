"""
Subclass of the BaseCredContainer class used for reading secrets from a flat file.
While we all know it is not best practice, IRL to store sensitive things in flat files there may be some cases where it makes sense
(or at least is 'okay'):  Local Development.  Bearer Tokens.  Short-lived / Temporary Secrets.  Passphrases, corresponding with encryption keys, etc.

THINK TWICE BEFORE USING THIS TYPE OF CREDENTIAL CONTAINER IS PRODUCTION APPLICATIONS!
IF THERE IS A BETTER, MORE SUITABLE IMPLEMENTATION, PLEASE USE THAT
"""

import os
from base_cred_container import CredContainerBase

class FlatFileCredContainer(CredContainerBase):
    """
    A credential container for dealing with credentials stored in flat files
    """

    def __init__(self, file_path:str):
        """
        Init method for the FlatFileCredContainer

        Args:
            file_path (str): A fully qualified path the file which contains the secret
        """

        # Validate thet the file path is actually a flat file that exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Cannot instantiate {type(self)} container because file doesn't exist: {file_path}")

        self.file_path = file_path
    
    def get_cred(self, strip=True) -> str:
        """
        Reads a credential out of a credential file

        Args:
            strip (bool, optional): Causes the str.strip() method to be appled or not. Defaults to True.

        Returns:
            str: The contents of the file
        """
        
        with open(self.file_path, 'r') as f:
            s = f.read()

        if strip:
            s = s.strip()

        return s
    

    def set_cred(self):
        return super().set_cred()

    def delete_cred(self):
        return super().delete_cred()
