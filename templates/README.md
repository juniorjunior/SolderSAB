# Templates
This folder is where server build template archives should be placed. Essentially, everything that is not mod specific (i.e. no mods, configs, etc.) should be zipped up into an archive file. The contents of this archive should not be in a subfolder so that when it is extracted into the build folder by the script the structure will mesh with the contents of the solder mods.

For example, one could create a ZIP archive named "Thermos-1.7.10-1614.56.zip" which contains start scripts, library folder, server JAR, etc. The file would then be referenced with -t or --template= on the command line with "-t Thermos-1.7.10-1614.56".
