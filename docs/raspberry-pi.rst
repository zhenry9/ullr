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
The first step on a fresh Raspberry Pi OS install is to install python.