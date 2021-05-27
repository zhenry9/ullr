Getting Started
===============
Ullr functions just like a really long serial cable, to connect software
to remote serial devices. Ullr needs to be installed and configured on both
sides of the connection: on the computer running the target software, and on
the remote computer connected to the serial device. The remote computer can be
a laptop, a Raspberry Pi, or any device capable of running Python applications. 
See :ref:`Installation` for installation info.


Navigating to the WebUI
~~~~~~~~~~~~~~~~~~~~~~~
Ullr hosts a web interface on port 5000 of the local machine by default. You 
can get there by typing :code:`localhost:5000` in a browser window. If you used 
a Windows installer, there will also be a shortcut in the start menu.

Configuring Ullr
~~~~~~~~~~~~~~~~
To get started, we need to get Ullr setup for our needs. The configuration 
settings can be accessed by clicking the "Configure" button on the top right of 
the screen.

PICTURE

A Note on Terminology
'''''''''''''''''''''
Ullr borrows terminology from the original RS-232 specification, specifically
the terms "DCE" and "DTE". "DCE" stands for Data Circuit-terminating Equipment. 
These are the serial devices, such as timers, sensors, and printers. "DTE" 
stands for Data Terminal Equipment. These are the computers and software 
instances. The RS-232 protocol connects DCE equipment to DTE equipment.

MQTT Broker settings
''''''''''''''''''''
The first step is to configure the MQTT broker. By default, these settings are
set to the free shared Ullr broker. 

PICTURE

However, Ullr can be configured to use any MQTT broker. Some free options are 
available at `Hive MQ <hivemq.com>` and .

Adding Local Devices
''''''''''''''''''''
A local device is a device that is plugged into the local machine with a 
serial cable, or a piece of software running on the local machine. Click on 
the "Add Local" button to open the add device dialog.

PICTURE

Give the device a descriptive name. It can be anything that makes sense to you, 
like "CP540", "Start Timer", or "Split Second Software". Next, we need to tell 
Ullr whether this is a DCE or DTE device. Generally, if it's a physical device
that's plugged into the computer is a DCE. If it's a piece of software it's a 
DTE.

The next step is to select the serial port and baudrate. This is the port the 
physical device is plugged into, or the port the software is listening on. Ullr 
automatically lists all available serial ports. If you don't see the port you're 
expecting, try refreshing the page or reconnecting your device. 

Finally, we have some choices to make reflected by the three checkboxes at the 
bottom. We can choose to Mute the device if we only want to send the device
messages and don't want or expect to receive messages from it. Checking this
box will reduce CPU usage for devices that don't send messages. By default this
box is unchecked.

Along these same lines, we can choose whether or not the device accepts incoming
messages. If we only expect the device to send messages, not receive them, this
box can be unchecked. This will also reduce CPU usage. By default the box is 
checked.

Finally, we can choose whether or not the device is published. If a device is 
published, any message it sends will also be sent to the MQTT broker (the 
"cloud"), where it can be read remotely.

Click the red "Add" button to add the device. It will then appear in the device
window under the appropriate tab: "Devices" if DCE, and "Computers" if DTE. 

PICTURE

Clicking the hamburger icon in the lower left will bring up some advanced 
options for the device, which will be covered elsewhere in this document. 
At the top of the window is the "Published Name". This is what is necessary to
connect to the device remotely.

PICTURE

Adding Remote Devices
'''''''''''''''''''''