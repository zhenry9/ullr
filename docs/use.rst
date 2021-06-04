Usage
=====
Ullr facilitates the connection of DCE and DTE devices (see :ref:`RS-232 
Terminology`). Any message from a DCE device is sent to all DTE devices, and any 
message from a DTE device is sent to all DCE devices. See the diagram below:

.. figure:: /_static/device-bus.png

    Signal flow between devices in Ullr.

In this way it is possible to access a device such as a GPS receiver from 
multiple remote computers, as well as the computer the device is actually 
plugged into. It is also possible to connecte multiple devices to one piece of 
software as if they were a single device.

Once Ullr is configured and running (see :ref:`Configuration`) it is not 
necessary to use the web interface. It is sufficient to just run your target 
software, and Ullr will work in the background. However, the web interface 
provides some powerful features for monitoring operation and handling exceptions.

Monitoring Message Transmission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For this guide, we'll assume that you have added a few devices in :ref:`the 
previous step <Configuration>`. For example, you might have a remote DCE device, 
a local DCE device, and a local DTE software instance as in the example below.

.. figure:: /_static/usage/device-tab.png

    The "Devices" tab showing a remote device and a local device.

.. figure:: /_static/usage/computers-tab.png

    The "Computers" tab showing a single local software instance.

Using this configuration, any message from "My Local Device" or "My Remote 
Device" will be sent to "My Target Software". Similarly, any message from "My 
Target Software" will be sent to both "My Local Device" and "My Remote Device".

When a device receives a message, either from the :ref:`MQTT broker <MQTT 
Messaging Protocol>` (the "cloud") or from a physical serial port, it will appear 
in the white space above the device. You can think of this similar to a receipt 
printer, with the newest message at the bottom and the oldest message at the top. 
In the image below, you can see that "My Remote Device" has received three messages 
and "My Local Device" has received two.

.. figure:: /_static/usage/messages-received.png

    The device window with several messages received.

Using the Console
~~~~~~~~~~~~~~~~~
The console can be viewed by clicking the "Console" tab on the bottom middle of 
the screen. This provides a verbose output from the software. If you are having 
trouble, it is the first place to look for error feedback.

.. figure:: /_static/usage/console.png

    The console tab.

Using the Log File
~~~~~~~~~~~~~~~~~~
Sometimes it is necessary to debug with more detail than the console provides. 
Ullr keeps a log file with detailed operation information. By default this file 
is located in the user's home directory. For example, on Windows it might be in 
C:\\users\\zhenry\\.log\\ullr\\ullr.log. If run as superuser on Linux it will be 
located at /var/log/ullr/ullr.log.

The log file can also be downloaded directly through the web interface. Just 
open the "Configure" menu and click "Get Log File".

The Advanced Menu
~~~~~~~~~~~~~~~~~
Clicking the "hamburger" icon in the bottom left corner of a device will bring up 
the advanced menu for that device. There are subtle differences between the menu 
for local devices and the menu for remote devices, but the basic concepts are the 
same.

Message Transmission Settings
'''''''''''''''''''''''''''''

.. figure:: /_static/usage/transmission-settings.png

    The transmission settings section of the advanced menu.

The first section of the advanced menu deals with how messages are sent and 
received. Ticking the "Mute" checkbox will ignore any messages originating from 
the device. Ticking the "Accept Incoming" checkbox will allow messages to be sent 
to the device. And, if it's a local device, ticking the "Publish" checkbox will 
connect the device to the MQTT broker using the "Published name" field as the 
topic name.

Device Translation
''''''''''''''''''
The next section has to do with device translation settings. Device translation 
is currently only applicable to sports timing uses. 

"Translating" a device means converting its message format to that of a 
different device. For example, if a Tag Heuer CP545 receives a new impulse on its
first channel at 11:15:33.33261, it will send a message similar to the following:

.. code-block::

    TN       253  1 11:15:33.33261  7803       068E

If we were to translate the same information to Alge S4 format, it would look 
like this:

.. code-block::

    0253 SZ  11:15:33.332

There are a few important things to notice. While the first channel of a CP545 is 
1, the first channel of an S4 is SZ. Also, take a look at the Time-of-Day: an 
Alge S4 has a max precision of 1/1,000th of a second, while a CP545 is precise to 
the 1/100,000th of a second. When we translated we lost 2 digits of precision. 
For this reason it is important to always translate from lower precision devices 
to higher precision devices.

Why translate at all? Ullr supports the connection of multiple timing devices to 
a single serial port, but the target software will be expecting all messages to 
be in a uniform format. Translation allows the connection of multiple types of 
devices to the same target software.

For example, with translation it is possible to have a CP540 connected to the 
start wand, an Alge Timy to a split, and an S4 to the photocells at the finish. 
All three timers can then be connected to an application that only supports the 
connection of one timer, such as Split Second Ski Club.

To further support this feature, you can shift the channel numbers while 
translating. For example, the only ports accessible on an Alge Timy, without 
accessories, are c0 and c1, even though it is possible to map channels c0 through c7 in 
Split Second. Without channel shifting we would be unable to use more than two 
Timys wihout ending up with overlapping channel numbers. By shifting channels we 
can use both built-in ports on up to 4 Timys without conflict.

For more information on setting up device translation for skiing or other sports 
timing, see :ref:`Connecting multiple timers to Ski Club`.

.. figure:: /_static/usage/translation.png

    The translation settings in the advanced menu.

By default translation is off. To turn it on, select "True" from the dropdown 
menu. Next, set the source and destination settings according to your needs. The 
list of supported devices is growing, and :ref:`contributions <Contributing>` are always welcome! 
Finally, you can choose to shift the channels. This number can be either positive 
or negative as long as the resulting channel falls in the allowable range for the 
destination device. For example, 0-7 for an Alge Timy. It is possible to shift 
channels without translating to a different device format. Just select the same 
device for both source and destination.

Handling Late Messages
''''''''''''''''''''''
The late message feature is specific to remote devices only.

Ullr is designed to be used in portable, outdoor situations. If the quality of 
the internet connection is poor, messages can arrive later than expected. 
Depending on the use case, this can cause trouble on the receiving end. For 
example, Split Second software does not behave well when a competitor's start 
impulse arrives after their finish impulse, or when start impulses arrive out of 
order.

To prevent this, an on-time arrival window can be set. This is set when adding 
the device, and can also be edited in the advanced menu. The on-time arrival 
setting is the number of seconds a message can spend in transit and still be 
accepted by the software. 

If set to 0s, all messages will be accepted regardless of transit time. If set 
higher than 0, any message with a longer transit time will NOT be processed and 
sent to other devices. It will end up in the "Late Messages" section of the 
advanced menu, where it can then be manually sent, copied or discarded.

.. figure:: /_static/usage/late-messages.png

    The late messages window showing four late messages.

To accept and send these messages, select one or more and then hit the "Send 
Selected" button.

When a device has received late messages, a red badge will appear above the 
hamburger icon with the number of late messages.

.. figure:: /_static/usage/late-message-badge.png

    Remote device showing 4 late messages.
