"""
Subclass of the BaseCredContainer used for reading secrets from bitwarden password manager
"""

from flat_file import FlatFileCredContainer
from base_cred_container import CredContainerBase
import json
import requests
import hashlib
import base64
import getpass

API_CONF_FLAT_FILE='/.credentials/bw_api.json'
API_BASE_URL='https://api.bitwarden.com'
API_AUTH_ENDPOINT='https://identity.bitwarden.com/connect/token'

def make_bitwarden_container_using_flat_file(api_conf_flat_file:str = None):
    """
    Factory function to return a BitwardeCredContainer object, instantiated using data
    read from a flat file.  In this case, we expect the contents of the flat file to be
    JSON with these keys: [client_id, client_secret, scope, grant_type]
    See 'View API Key' button at https://vault.bitwarden.com/#/settings/account

    Args:
        api_key_flat_file (str, optional): The flat file that contains the API details. If not provided, defaults to API_KEY_FLAT_FILE

    Returns:
        BitwardenCredContainer
    """

    # Read the contents of the flat file
    if api_conf_flat_file is None:
        api_conf_flat_file = API_CONF_FLAT_FILE
    
    file_cred_obj = FlatFileCredContainer(file_path=api_conf_flat_file)
    file_contents = file_cred_obj.read()
    j = json.loads(file_contents)

    # Handle the password, it needs to be hashed (as would be the case with the hash_password function).  User can omit this from config or set falsy to be prompted interactively
    if not j.get('password'):
        j['password'] = prompt_for_credentials(email=j['username']) # Causes user to be prompted and puts the hashed value into the j dictionary

    o = BitwardenCredContainer(**j)
    return o

def hash_password(email:str, password: str) -> str:
    """
    Function to return the 'password' argument to pass into the API.
    As it turns out, the API documentation covers getting a bearer token only for the Enterprise version.
    I had to do some hacking (read:  Googling / Inspecting Crome Network traffic) to understand that the 
    POST data payload into the API to get a token really ought to look like this:
        grant_type=password
        username=<EMAIL>
        password=<PASSWORD_HASH>  (As constructed by this function)
        scope=api
        client_id=web

    Basically:  I've copied/collapsed the 'makeKey' and 'hashedPassword' functions from here and made the pythonic:  https://github.com/birlorg/bitwarden-cli/blob/trunk/python/bitwarden/crypto.py
    
    Example here explains how the hashing works (Not sure how they know, but they know.  
        Consider:  Login with example creds and inspect network): https://github.com/jcs/rubywarden/blob/master/API.md
    
    This calculator more or less proves the same:  https://bitwarden.com/help/crypto.html
    Using these arguments, we expect a "Master Password" of "r5CFRR+n9NQI8a525FY+0BPR0HGOjVJX0cR1KEMnIOo="
    If you were to inspect network traffic and attempt to log into bitwarden with these (imaginary) credentials, you'd see this same value
        user = nobody@example.com
        password = p4ssw0rd
        iterations = 5000
        

    Args:
        password (str): The password to hash.  Corresponds with bitwarden Master password
        email_address_salt (str): The email address to use as salt

    Returns:
        str: The password hash
    """

    iterations = 5000  # Don't know how somebody figured out that this it the number, but it is the number (See Docstring)

    password = password.encode('utf-8')
    email = email.lower().encode('utf-8')

    hash_key = hashlib.pbkdf2_hmac(hash_name='sha256', password=password, salt=email, iterations=5000, dklen=32)
    ret_val = base64.b64encode(hashlib.pbkdf2_hmac(hash_name='sha256', password=hash_key, salt=password, iterations=1, dklen=32)).decode('utf-8')
    return ret_val

def prompt_for_credentials(email:str = None, password: str = None) -> str:
    """
    A wrapper function around hash_password that will interactively prompt the use for the (non-hashed) password in order to come up with the right digest.
    This behavior allows a user to not specify the hashed password in the config flat file and be prompted for it instead
    Args:
        email (string, optional): The email address. If not passed, the user will be prompted
        password (string, optional): The password. If not passed (intended behavior for this function), the user will be prompted

    Returns:
        string: The hashed password 
    """

    if not email:
        email = input("Bitwarden account email address: ")

    if not password:
        password = getpass.getpass(f"{email} account password: ")

    ret_val = hash_password(email=email, password=password)

    return ret_val

class BitwardenCredContainer(CredContainerBase):
    """
    A credential container for interacting with bitwarden

    Args:
        CredContainerBase ([type]): [description]
    """

    def __init__(self, username, password, **kwargs) -> None:
        """
        Init method for the BitwardenCredContainer

        Note:  The password needs to be hashed.  See docstring under hash_password function for more specifics

        Args:
            username ([type]): Username (email address)
            password ([type]): Password (Hashed, as would be treutnred by the has_password function)
            grant_type (str, optional): [description]. Defaults to "password".  This is an argument required by the API.  It might as well be hard-coded
            scope (str, optional): [description]. Defaults to "api".  This is an argument required by the API.  It might as well be hard-coded
            client_id (str, optional): [description]. Defaults to "web".  This is an argument required by the API.  It might as well be hard-coded
        """

        self.username = username
        self._password = password
        self.grant_type = kwargs.get('grant_type') or 'password'
        self.scope = kwargs.get('scope') or 'api'
        self.client_id = kwargs.get('client_id') or 'web'

        print(f"Instantiated {type(self)} for username (email address) {self.username}")
        

        #self._get_bearer_token()

    # def _get_bearer_token(self):
    #     """
    #     Gets a bearer token from the API to use for subsequent requests
    #     """
    #     # TODO:  I dont think we need this method.  Drop it

    #     url = API_AUTH_ENDPOINT
        
    #     headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
    #     data = dict(grant_type="client_credentials", 
    #                 scope="api", 
    #                 client_id=self._client_id, 
    #                 client_secret=self._client_secret)
        

    #     res = requests.post(url=url, headers=headers, data=json.dumps(data))
    #     print(res.json())

    #     print("!")



    def get_cred(self):
        return super().get_cred()

    def set_cred(self):
        return super().set_cred()
    
    def delete_cred(self):
        return super().delete_cred()

if __name__ == '__main__':
    o = make_bitwarden_container_using_flat_file()
    print("!")

    # test = hash_password(password="p4ssw0rd", email="nobody@example.com")
    # print(test)

    # print(prompt_for_credentials())