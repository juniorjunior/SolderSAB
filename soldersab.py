import ConfigParser
import os
import sys
import getopt
import shutil
import urllib2
import urllib
import json
import zipfile

templatename = ""
packslug = ""

# Unless a full path is specified on the command line, the .ini file
# will be read from the folder in which the script is executed.
configfile = "soldersab.ini"

try:
   opts, args = getopt.getopt(sys.argv[1:], "hc:t:p:", ["config=", "template=", "packslug="])
except getopt.GetoptError:
   print "Usage: srvbuilder.py -t <templatename> -p <packslug>"
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print "Usage: srvbuilder.py -t <templatename> -p <packslug>"
      sys.exit(2)
   elif opt in ("-t", "--template"):
      templatename = arg
   elif opt in ("-p", "--packslug"):
      packslug = arg
   elif opt in ("-c", "--config"):
      configfile = arg

if ( not os.path.isfile(configfile) ):
   print "Could not find config file \"%s\"" % configfile
   sys.exit(4)

# Read in the config file and set some local values
Config = ConfigParser.ConfigParser()
Config.read(configfile)

SolderAPIURL = Config.get("Solder", "SolderAPIURL")
ModsBaseURL = Config.get("Solder", "ModsBaseURL")
WorkingFolder = Config.get("Builder", "WorkingFolder")
ClientOnlyMatch = Config.get("Builder", "ClientOnlyMatch").replace(" ","").split(",")

if ( not os.path.isdir(WorkingFolder) ):
   print "Working folder \"%s\" does not exist!" % BuildFolder
   sys.exit(1)

# Shouldn't have to change these
CacheFolder = WorkingFolder + "cache/"
BuildFolder = WorkingFolder + "build/"
OutputFolder = WorkingFolder + "servers/"
TemplateFile = WorkingFolder + "templates/" + templatename + ".zip"

if ( not os.path.isfile(TemplateFile) ):
   print "Template file \"%s\" does not exist!" % TemplateFile
   sys.exit(3)

# Clean out the Cache and Build folders
if ( os.path.isdir(CacheFolder) ):
   shutil.rmtree(CacheFolder)
if ( os.path.isdir(BuildFolder) ):
   shutil.rmtree(BuildFolder)
os.makedirs(CacheFolder)
os.makedirs(BuildFolder)

# Extract the specified template into the Build folder
zf = zipfile.ZipFile(TemplateFile)
zf.extractall(BuildFolder)

if ( not os.path.isdir(OutputFolder) ):
   os.makedirs(OutputFolder)

# Query Solder for pack metadata and the mod list.
# Extract all the mods into the Build folder.
PackURL = SolderAPIURL + "modpack/" + packslug
packData = json.loads(urllib2.urlopen(PackURL).read())
packContents = json.loads(urllib2.urlopen(PackURL + "/" + packData["recommended"]).read())
print "Pack Name: %s" % packData["display_name"]
print "Number of mods: %d" % len(packContents["mods"])
print ""
for mod in packContents["mods"]:
   modFile =  mod["name"] + "-" + mod["version"] + ".zip"
   modURL = ModsBaseURL + mod["name"] + "/" + modFile
   print "Retrieving mod: %s" % modFile
   urllib.urlretrieve(modURL, CacheFolder + modFile)
   zf = zipfile.ZipFile(CacheFolder + modFile)
   zf.extractall(BuildFolder)

# If a client-only-mods.txt file exists, parse its contents and remove any listed files
if ( os.path.isfile(BuildFolder + "client-only-mods.txt") ):
   fh = open(BuildFolder + "client-only-mods.txt")
   for line in fh:
      if ( os.path.isfile(BuildFolder + "mods/" + line.strip()) ):
         os.remove(BuildFolder + "mods/" +line.strip())
   fh.close

# Remove mod names matching ClientOnlyMatch
for path, dirs, files in os.walk(BuildFolder + "mods/"):
   for filename in files:
      for match in ClientOnlyMatch:
         if ( match in filename ):
            os.remove(os.path.join(path, filename))

# Get rid of the bin/ folder
if ( os.path.isdir(BuildFolder + "bin/") ):
   shutil.rmtree(BuildFolder + "bin/")

# Set the ZIP compression type if available
try:
   import zlib
   compression = zipfile.ZIP_DEFLATED
except:
   compression = zipfile.ZIP_STORED

# Create the server archive
serverArchiveFile = OutputFolder + packslug + "-" + packData["recommended"] + "-server.zip"
print ""
print "Creating server archive: %s" % serverArchiveFile
zf = zipfile.ZipFile(serverArchiveFile, mode='w')
for path, dirs, files in os.walk(BuildFolder):
   for filename in files:
      zf.write(os.path.join(path, filename), arcname=os.path.join(path[len(BuildFolder):], filename), compress_type=compression)
zf.close()
