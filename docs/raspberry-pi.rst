Running on a Raspberry Pi
=========================
Ullr was designed to be lightweight and useful in portable, outdoor 
applications. The Raspberry Pi is a great computer for these needs. This 
section will provide some in-depth info on installation, operation and 
configuration on a Raspberry Pi, specifically a Raspberry Pi Zero W.

Choosing an OS
~~~~~~~~~~~~~~
There are a number of Raspberry Pi operating systems to choose from. Virtually 
all of them are based on the Linux Kernel, and are tailored to suit different 
needs. Some offer a basic Graphical User Interface, while others are "headless", 
meaning they offer a Command Line Interface only. Either will work, but this 
guide recommends the use of Raspberry Pi OS Lite, a headless OS. This saves on 
processor and battery use and reduces complexity somewhat. The instructions in 
this section will be based on command line operation, but it is certainly 
possible to use a graphical interface as well.

Some Linux Basics
~~~~~~~~~~~~~~~~~
How to use Linux is mostly outside the scope of this guide. There are some 
excellent resources on the web at <resources here>. However, we'll go over a 
few essential concepts.

Superuser
'''''''''
Linux does not allow regular users to make system-wide changes by default. This 
is an important thing to keep in mind as we install and setup Ullr. The default 
user on a Raspberry Pi is "pi". This user does not have permission to install 
software or access serial ports. When we need to execute a command or run a 
program that does these things (like Ullr), we should put the "sudo" in front of 
the command. This will execute the command as as superuser with admin (root) 
priveleges. Keep in mind that whenver we use sudo we are acting as a different 
user, NOT the "pi" user. Changes we make will happen system wide.

Installation
~~~~~~~~~~~~

Installing Python
'''''''''''''''''
The first step on a fresh Raspberry Pi OS install is to install python. We'll 
use apt, the built in package manager. On a command line, type:

.. code-block::

    sudo apt install python3 python3-pip

This will install the latest available version on Python, as well as pip, the 
Python package manager. 

Installing Ullr
'''''''''''''''
The next step is to install Ullr using pip. Type:

.. code-block::

    sudo pip3 install ullr

Ullr should now be downloaded and installed! To run, just type:

.. code-block::

    sudo ullr

You should get the following message in the terminal:

.. code-block::

    Ullr running on port 5000

Ullr is now up and running! A web configuration interface is available on port 
5000 of the Raspberry Pi. If you're running a Raspberry Pi OS with a graphical 
interface, you can open a browser window to :code:`localhost:5000`. This isn't 
the best way to access the interface, however, due to the web rendering 
limitations of the Raspberry Pi. A better way is to access the interface 
remotely from a computer on the same LAN. From the remote PC navigate to 
:code:`raspberrypi.local:5000/`, or :code:`<pi-ip-address>:5000/`.

Why sudo? Ullr requires access to serial ports, which by default are not 
accessible by regular users. If you don't want to run as superuser, make sure 
you run as a user with serial port permissions.

Setting Ullr to run on boot
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Running Ullr from the command line is easy enough when we have a monitor and 
keyboard or remote access available, but that isn't always the case. We can make 
things easier by setting Ullr to start whenever the Raspberry Pi is powered on.

Using cron
''''''''''
The simplest way is to use cron, the Linux task scheduler. Before we start 
changing settings, we need to make sure the nano text editor is installed. Type: 

.. code-block::

    sudo apt install nano

Once we're sure nano is there, the next step is to edit the cron table to 
schedule Ullr to run at boot. Type:

.. code-block::

    sudo crontab -e

There may be a prompt asking you to select a text editor. Choose nano. Next you 
will see a screen with a rather lengthy comment explanation. Below these 
comments, add the following line:

.. code-block::

    @reboot sudo ullr

The file should look similar to this when you're done:

.. figure:: /_static/cron-settings.png
    
    Cron table with ullr task added.

Hit control-x, y for yes, then enter to confirm. That's it! Ullr will now run 
whenever the Raspberry Pi is powered on.

Adding a systemd service
''''''''''''''''''''''''
More info to come!