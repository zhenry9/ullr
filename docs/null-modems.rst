Virtual Null Modems
===================
A null modem, in the physical world, is just a serial cable used to connect two 
DTE devices. A virtual null modem is the software equivalent of the same thing. 
You can think of it as two com ports connected by a serial cable: what is sent 
to one com port is received by the other, and vice versa.

What do virtual null modems have to do with Ullr? A virtual null modem is what 
we need to connect Ullr to another piece of software. It is the pipe that carries 
serial data from Ullr to the target software. Ullr is connected to one end of the 
virtual null modem, and the target software to the other.

.. figure:: /_static/virtual-null-modem.png

    Diagram of virtual null modem functionality.

In practice, a virtual null modem just appears as two available serial ports on 
your machine. In the example above they would be ports COM50 and COM51. We'll go 
through setting it up on various operating systems below.

Windows
~~~~~~~
There are multiple virtual null modem products available for Windows, but we'll 
focus on `com0com <https://sourceforge.net/projects/com0com/>`_, as it is stable 
as well as free and open source. There is a signed Windows installer available 
from Alge at :xref:`com0com`. Using the signed installer avoids possible 
permission and security issues with Windows.

Once com0com is installed, it is necessary to open the configuration program 
from the start menu and add a linked pair of com ports (a virtual null modem). 
You can choose any names you want for these ports, as long as they aren't 
already in use. It is best practice, though not strictly necessary, to start the 
name with COM (for example, COM21 or COM50). This is because not all software 
will recognize com ports that don't follow this convention.

Running the com0com configuration tool will install drivers for the null modem 
on your machine. This null modem will persist until the drivers are removed, and 
there is no need to run this setup again.

Linux
~~~~~
On Linux (or other POSIX-like systems) a null modem can be setup much more simply 
by using socat. Make sure socat is installed on your system, then type:

.. code-block:: 

    sudo socat PTY,link=/dev/ttyS50 PTY,link=/dev/ttyS51

This example creates a virtual null modem by linking the ports /dev/ttyS50 and 
/dev/ttyS51. Note that you can choose any name you'd like for the ports, but 
starting the name with 'ttyS' will increase the chances of the ports being 
detected by Ullr and other software.

Unlike the Windows setup above, this virtual null modem will only persist as 
long as socat is running. If you'd like to run socat in the background, you can 
add an ampersand to the end of the command, like so:

.. code-block:: 

    sudo socat PTY,link=/dev/ttyS50 PTY,link=/dev/ttyS51 &

If you'd like socat to run on boot you could add the following line to your cron 
table:

.. code-block:: 

    @reboot socat PTY,link=/dev/ttyS50 PTY,link=/dev/ttyS51

See :ref:`Using cron` for more detail on editing the cron table.