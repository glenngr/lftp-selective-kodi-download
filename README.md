# lftp-selective-kodi-sync
Fetches movies you don't have in your Kodi SQL Library from a remote server via LFTP

## Setup
Edit the configuration section in lftp_selective_sync.py to get started.
You need to have lftp installed for the tool to work. In debian or ubuntu, you can install it with the command sudo apt-get install lftp.
#### Setup details
Set up the SQL connection details in the variables **mysqlLogin**, **mysqlPassword**, **mysqlDtabase** and **mysqlHost**.
Set the remote login details in the variables **remoteUser**, **remotePass**, **remoteHost**.
You can also set up rsa keys on the remote host to allow automatic login, if the remote host is SSH/SFTP. If you do this, just set a dummy password in the configuration section.

The **remotepath** and **localpath** variables are the full path to the directories you want to download from and save to.

The **lftp_parallell** variable is how many parallell connections you want while downloading.

The **debug** variable can be set to True if you want extra logging.

The **requireMinimumImdbRating** can be set to True if you only want to download directories with certain imdb ratings.
If you set this to true, set up the minimum and maximum rating in the variables **mimimumImdbRating** and **lowerImdbRating**.
