
# cred_manage is for managing credentials.

The `cred_manage` package contains classes for managing credentials or secrets.

The Abstract Base Class `CredContainerBase` is defined in `base_cred_container.py`.

Subclasses of `CredContainerBase` are called "Credential Containers"

There are 3 methods which are intended to be overridden by subclasses.  If not implemented, a `NotImplementedError` will be raised.  Sometimes this might be perfectly appropriate, and you should catch these exceptions as applicable.  

These are:

- `get_cred()` - Used to get a credential out of a credential container.
- `set_cred()` - If implemented, used to set a credential within a credential container.
- `delete_cred()` - If implemented, used to delete a credential within a credential container.

A Credential container can really be anything that is reasonably responsible to keep credentials, keys, or other secret things inside of.  For example: 

- A Password Manager like Bitwarden or Lastpass
- A Flat File (Containing an API Key, for example) **
- A Keychain, like that in MacOS

Currently, the `cred_manage` package has these Credential Containers implemented (Contributions are welcome!):
- `FlatFileCredContainer` - Used to interact with flat files containing passwords or other secret things.  **Please read the warnings below and take them to heart.
- `BitwardenCredContainer` - Used to interact with [Bitwarden Password Manager](https://bitwarden.com/).

A common pattern might be to use a `FlatFileCredContainer` to manage the context necessary to subsequently log into and interact with a Password Manager tool, like Bitwarden (`BitwardenCredContainer`) or Lastpass, or a Keychain, which are surely better places to keep sensitive information than flat files.  

# FlatFileCredContainer

First things first:  

**Never, never, never, EVER** commit passwords or other secrets into version control.  

Never.  **DO NOT DO IT!**  

Instead:
- Write your code such that it references and reads sensitive information from outside of the repository (e.g. A config file containing a path to another file outside of version control).
- Avoid keeping sensitive information in flat files in the first place.  If you find yourself with more than just a few secrets in flat files, you should probably rethink your design.
- For cases where you do decide to keep secrets in flat files, be very sure that the machine on which they reside is sufficiently locked down (beyond the scope of this README.md other than to say:  Not exposed to the internet, no superfluous open ports, and login passwords required for all users.)


With that warning behind us...

`FlatFileCredContainer` isn't complex at all.  It doesn't do much more than the standard Python library can do to read from and write to a file with a file handle.  One feature that it does implement is that by default, it will be stubborn (this can be overridden) about interacting with files for which the permission bits are too broad, in which case an exception will be raised.

`FlatFileCredContainer` might be a good place to keep API keys, bearer tokens, or anything else that is needed to bootstrap some process or otherwise allow for automation without human interaction.

# BitwardenCredContainer
BitwardenCredContainer is a wrapper around the [Bitwarden CLI](https://bitwarden.com/help/article/cli/).  It is **NOT** a wrapper around the [Bitwarden API](https://bitwarden.com/help/article/public-api/), which as far as this author can tell is only available to Enterprise Organization plans.  If you're a user of an Enterprise Organization plan, you'll probably want to interact with he API directly, using the Python `requests` library, rather than this package.

**Thus, a prerequisite is that you'll have installed the [Bitwarden CLI](https://bitwarden.com/help/article/cli/#download-and-install) ahead of time.**

`BitwardenCredContainer` can be instantiated directly but for convenience, a factory function, `make_bitwarden_container()` is provided. `make_bitwarden_container()` accepts just a single argument, which is a path to a flat JSON file with the proper context to instantiate the class via the `__init__` method.  The contents of the file should look like this:

```
{
    "client_id": "<YOUR CLIENT ID HERE>",
    "client_secret": "<YOUR CLIENT SECRET HERE>",
    "scope": "api",
    "grant_type": "client_credentials",
    "email_address": "<you@yourdomain.com HERE, OPTIONALLY.>"
}
```
Note that the `email_address` key is optional, to suppress a subsequent prompt for your email address.

### About Vault Items and GUIDs
`BitwardenCredContainer` is a container around your entire Bitwarden vault.  The vault is initially loaded in it's entirety, but all passwords are redacted and replaced with the string `<password removed>`, in the spirit of paranoia.  Subsequent calls to methods that would return an actual password, make a secondary call to the CLI to retrieve just that password and return the actual value.  Such methods are listed below and do what you think they might based on their names (more context in Docstrings, if needed):
- `get_cred()`
- `get_vault_item_by_guid()`
- `get_credentials_by_guid()`
- `get_username_by_guid()`
- `get_password_by_guid()`

Each of these methods accepts a GUID, which serves as the 'primary key' for the vault item in question.  If you need to find the GUID for a given item, you can instantiate a `BitwardenCredContainer` object and invoke the `print_items()` method (This will not print passwords).  Alternatively, you can directly invoke the [Bitwarden CLI](https://bitwarden.com/help/article/cli/) using the `bw list items` command (Consider piping into [jq](https://stedolan.github.io/jq/) for readability) to find the GUID (under the `id` key) for any given vault item.

### About the `BW_SESSION` environment variable.
When logging into [Bitwarden via the CLI, a Session Key is returned](https://bitwarden.com/help/article/cli/#using-a-session-key), which can be exported to the environment variable `BW_SESSION` to suppress subsequent prompts for the master password.  When instantiating `BitwardenCredContainer`, a check is performed to see if the `BW_SESSION` is set.  If it is set (and valid), YOU WILL NOT be prompted for the master password, interactively.  If it is not set, YOU WILL be prompted for the master password for each instantiation.  Depending on your use case, exploit this functionality (or not) as appropriate.  Hint:  Consider the ways in which you might be able to temporarily store this value in a `FlatFileCredContainer` object, only to destroy it when you're done.


# Example Usage.

In this example we use a `FlatFileCredContainer` object to read the necessary context to instantiate a `BitwardenCredContainer` object out of a flat file.  Then, we print the GUIDs and corresponding names of the items from the Bitwarden Vault

```
from cred_manage.flat_file import FlatFileCredContainer
from cred_manage.bitwarden import BitwardenCredContainer
import json

# Instantiate Flat File Credential Container
ff_obj = FlatFileCredContainer(file_path='/.credentials/bw_api.json', allow_broad_permissions=False)

# Read the JSON contents out of the Flat file Credential Container
j = json.loads(ff_obj.read())

# Use those JSON contents to instantiate a Bitwarden Credential Container
bw = BitwardenCredContainer(**j)  #  <-- If environment variable BW_SESSION is set, then no interactive password prompt here.

# Print the GUIDs and corresponding names of vault items
bw.print_items()
```


