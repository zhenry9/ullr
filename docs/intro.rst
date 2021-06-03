RS-232 Terminology
~~~~~~~~~~~~~~~~~~
Ullr borrows terminology from the original RS-232 specification, specifically
the terms "DCE" and "DTE". "DCE" stands for Data Circuit-terminating Equipment. 
These are the serial devices, such as timers, sensors, and printers. "DTE" 
stands for Data Terminal Equipment. These are the computers and software 
instances. The RS-232 protocol connects DCE equipment to DTE equipment.

MQTT Messaging Protocol
~~~~~~~~~~~~~~~~~~~~~~~
Ullr makes use of the MQTT messaging protocol to send and receive remote serial 
messages. This protocol was originally developed to monitor remote oil 
pipelines with satellite connections, and is particularly sturdy in situations 
with unreliable internet connections. It is also lightweight, and doesn't 
require much data or processing power.

MQTT is based on a publisher/subscriber model. Devices are NOT connected 
directly to each other, but to a central hub called a broker. When a device 
has information to send, it publishes it to the broker along with a topic name. 
The broker then sends this message to all devices that are subscribed to the 
topic. The protocol makes it possible to guarantee that all published messages 
get delivered to all subscribed clients at least once. For an excellent 
in-depth description of the MQTT protocol, see the `HiveMQ MQTT Essentials 
Guide <https://www.hivemq.com/mqtt-essentials/>`_.

Ullr makes use of this protocol by allowing local serial devices to be 
published. Ticking the "Published" checkbox on a local device will send all 
messages from the device to the MQTT broker. The topic the messages are 
published to will be the MAC address of the host client with the colons removed, 
followed by a forward slash and the device name with the spaces replaced by 
underscores. For example, for a device named "Thermometer" on a computer with a 
MAC address of 00:16:3e:2b:2f:28, messages will be published to the topic 
"00163e2b2f28/Thermometer". This topic name can be seen by clicking the 
hamburger icon in the bottom left corner of any device on the WebUI. If we want 
to connect to this device using Ullr on a remote PC, we can use the WebUI to add 
a remote device subscribed to "00163e2b2f28/Ullr".
