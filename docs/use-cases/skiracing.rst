Wireless ski race timing
========================
This is the specific use case for which this software was originally designed. 
Ullr allows for FIS-legal timing of Level 3 races or lower anywhere there is an 
internet connection. We'll examine the setup for a homologated race step by 
step.

.. figure:: /_static/pi-timer.png

    Wiring and signal flow for homologated ski timing.

At the start
~~~~~~~~~~~~

Wiring
''''''

.. figure:: /_static/start-wiring.png

    Wiring at the start.

The start block is connected by copper cable to two synchronized Time-of-Day 
timing devices, one for System A and one for System B. The System A timer is 
connected by serial cable to a computer running Ullr. This can be ANY computer 
capable of running Python applications and connecting to the internet. For 
example, the Raspberry Pi Zero W costs about $30 with a case and is around the 
size of a pocket knife. For the purposes of this tutorial we will assume that 
the start computer is a Raspberry Pi Zero W.

Ullr Configuration on the Raspberry Pi
''''''''''''''''''''''''''''''''''''''
Next we need to configure Ullr on the Raspberry Pi. This is fairly simple, as 
we only have one device! Navigate to the Raspberry Pi web interface, either 
from the Pi itself or from another computer on the same LAN. See 
:ref:`Running on a Raspberry Pi` for more information on how to do this.

First we need to make sure the MQTT broker is set up 
correctly. See :ref:`MQTT Broker Settings` for more info on how to do this. 
Next, we need to set Ullr to connect to our System A timing device. Since this 
device is plugged directly into the Pi with a serial cable, it is a local device. 
Click the "Add Local Device" button in the "Configure" menu to pull up the add 
device dialog.

Give the device a descriptive name. For this example we'll use a TAG CP540 as 
our timing device, so let's name the device "CP540". The next step is to select 
the port. We're using a USB-serial converter cable in this example, so our port 
will be "/dev/ttyUSB0". If you are using a serial connection directly to the 
Raspberry Pi your port name may be different. The CP540 runs at 9600 baud, so 
we'll select that from the dropdown menu.

We'll leave the mute checkbox unticked, since we are expecting to receive 
messages from this device. We'll untick the "Accept Incoming" checkbox, 
since we don't expect the timer to receive any messages (in fact, this is against 
FIS rules). This also reduces some of the processing overhead. We'll leave the 
"Publish?" checkbox ticked as we are planning to access this device remotely.

When you're finished, the settings should look like this: 

.. figure:: 
