Command Line Operation
======================
Ullr can take several useful command line arguments, which will be described 
below. Ullr can also be run interactively through the terminal, without the use 
of the web interface. This can be useful for reducing processing overhead, or 
for monitoring operation on headless installations.

Command Line Arguments
~~~~~~~~~~~~~~~~~~~~~~
Ullr accepts several useful command line arguments.

Ignore the config file
''''''''''''''''''''''
``ullr --empty``

This starts Ullr with a blank, default configuration regardless of any settings 
in the configuration file. This is useful for fixing broken config files or for 
starting fresh.

Use an arbitrary config file
''''''''''''''''''''''''''''
``ullr --file my-config.ini``

This loads devices from a user-specified config file in an arbitrary location 
rather than from the standard config file.

Specify WebUI port
''''''''''''''''''
``ullr --uiport 1234``

By default, Ullr serves the Web UI on port 5000 of the local machine. You can use 
the --uiport flag to specify a different port. This is useful if port 5000 is not 
available, or if multiple instances of Ullr are to be run on the same machine (be 
careful doing this!)

Open WebUI on run
'''''''''''''''''
``ullr --popup``

This opens a browser to the web interface when Ullr is run. This is the defualt 
for Windows .msi package installations.

Running on the Command Line
~~~~~~~~~~~~~~~~~~~~~~~~~~~
``ullr --nowebui``

This starts Ullr with a command line interface rather than the web interface. 
Configuration can be done interactively, though not all of the WebUI features 
are available, most notably the late message handling features.