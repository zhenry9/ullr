Timing a ski race without a wire to the start
=============================================
This is the specific use case for which this software was originally designed. 
Ullr allows for FIS-legal timing of Level 3 races or lower anywhere there is an 
internet connection. We'll examine the setup for a homologated race step by 
step.

DIAGRAM

At the start
~~~~~~~~~~~~

DIAGRAM

The start block is connected by copper cable to two synchronized Time-of-Day 
timing devices, one for System A and one for System B. The System A timer is 
connected by serial cable to a computer running Ullr. This can be ANY computer 
capable of running Python applications and connecting to the internet. For 
example, the Raspberry Pi Zero W costs about $30 with a case and is around the 
size of a pocket knife. For the purposes of this tutorial we will assume that 
the start computer is a Raspberry Pi Zero W.

Next we need to configure Ullr on the Raspberry Pi. This is fairly simple, as 
we only have one device! 

There are several ways to configure Ullr, but the easiest is through the WebUI. 
The easiest way to access the Raspberry Pi web interface is from another 
computer on the same LAN. Typing "raspberrypi.local:5000/" into a browser 
window is typically sufficient. If this doesn't work, check your router's DHCP 
table to find the Raspberry Pi's IP address. 

First we need to make sure the MQTT broker is set up 
correctly. See :ref:`MQTT Broker Settings` for more info on how to do this. 
Next, we need to set Ullr to connect to our System A timing device. Since this 
device is plugged directly into the Pi with a serial cable, it is a local device. 
Click the "
