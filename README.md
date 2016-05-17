# SolderSAB
Builds a server archive file from the recommended build in Solder

## Prerequisites
* Add a file named "client-only-mods.txt" to your pack (in the "configs" mod might be a good place)
* Add one line to the file for each mod which should be removed from the server
* It is assumed that listed files are in mods/ so only include paths for subfolders (i.e. 1.7.10/liteloader.jar)

## Instructions
* Check out this repo
* Copy the soldersab.ini-dist file to soldersab.ini and edit the contents to reflect your environment
* Create a template to use for your server. This is a generic "not modpack specific" archive containing only the files required to get the server up and running. Detailed instructions are in the template folder.
* Execute the script: python soldersab.py -t Server-Whatever -p packslugname [-b] [-c configfile]
** -t Server-Whatever : The template name to use. This is just the name of the archive in templates/ without the .zip extension
** -p packslugname    : The slug for the pack which should be processed
** -b                 : Whether or not to overwrite/clobber an existing server archive file in servers/ [Optional]
** -c configfile      : Full path to a config file if not in the current directory [Optional]
