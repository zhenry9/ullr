# ULLR
### Pronounced "OOH-ler"
A serial <-> MQTT interface for sports timing.

<img src="https://github.com/zhenry9/Ullr/raw/main/Ullr-signal-flow.png" height="300" align="middle">

Ullr allows for the two-way exchange of data between serial devices and computers over the internet, 
using MQTT as an intermediary. 
This is particularly useful for connecting to faraway devices that aren't on the same LAN. 
Ullr allows for connecting an arbitrary number of devices to an arbitrary number of computers.

Ullr works for connecting remotely to things like weather stations, sensors, or other devices that send 
simple data intermittently. It is not going to work for things like modems or printers, due to the limitations of 
dweet.io among other things.

## Installation
### Python environment
  
`pip install Ullr`
  
### Windows executable
If you don't have or don't wish to use a Python environment, a Windows executable version is available on the source
repository on GitHub.

### Get the source
The source code is always available at [https://github.com/zhenry9/Ullr](https://github.com/zhenry9/Ullr).

## Configuration
Modify `config.ini` to suit your needs, or configure interactively using the prompts in the software. Some example
configurations can be seen in the example-configs directory in the project repository.

## Usage

Ullr borrows terminology from the original RS232 protocol. "DCE" stands for Data Circuit-terminating Equipment. These 
are the serial devices themselves, such as sensors or synchronized timers. "DTE" stands for Data Terminal Equipment. 
These are the computers, or software instances that the DCE devices connect to. Ullr facilitates the connection of 
DCE devices to DTE devices using dweet.io and local serial ports. Every message received from a DCE device is written to 
every DTE device, and every message received from a DTE device is written to every DCE device. Ullr allows for 
connecting an arbitrary number of devices, either local or remote. In this way it is possible to connect one DCE device 
to many computers, or many DCE devices to one serial port. 

Ullr needs to be running and individually configured on all DTE and DCE devices that are part of the connection.

### Default
`Ullr`

This starts Ullr with a web interface on `localhost:5000`.
If Ullr is run without command line options, it will attempt to load devices from the default config file. This
will be '~/.config/Ullr/config.ini', or '/etc/Ullr/config.ini' if run as superuser. 
If you are running Ullr for the first time or with an empty config file, no devices will be loaded. You can add
devices interactively using the web interface.

### CLI
`Ullr --nowebui`

This will load Ullr with a command line interface only, whithout the web interface. 
Configuration can be done interactively from the command line.

### Empty
`Ullr --empty`

This will ignore the default config file and start Ullr without any devices loaded. This is useful for fixing bad
config files, or creating new ones from scratch.

### From file
`Ullr --file FILENAME`

This will attempt to start Ullr by loading the devices specified in an arbitrary config file at FILENAME.

### Override
`Ullr --override MODE PORT THING_NAME`

This allows Ullr to be configured for a simple connection directly from the command line. MODE is the type of device
connected to the local serial port PORT, either DCE or DTE. THING_NAME is the dweet.io name of the device on the other
side of the connection. For example, to set up a connection to a DCE device connected to a Raspberry Pi:

```Ullr --override DCE /dev/ttyUSB0 Ullr_default```

This starts Ullr listening for messages from a DCE device on Linux port '/dev/ttyUSB0'. Any messages it receives will
be sent to dweet.io using the thing name 'Ullr_default'. It will also listen for incoming messages from 
'Ullr_default', and write them to the serial port.

To set up the same connection on the DTE side:

```Ullr --override DTE COM20 Ullr_default```

This will listen for dweet.io messages from 'Ullr_default' and write them to the Windows port 'COM20'. It will also
 send any messages received from 'COM20' to dweet.io using the name 'Ullr_default'.

### Display help page

`Ullr --help`
  
This prints out the help page for command line options.


### Virtual COM ports
On the computer (DTE) side of the connection you'll need to set up a virtual null modem to allow Ullr to 
communicate with the target software. This is just a pair of com ports connected to each other. Ullr connects to 
one port, and your software application connects to the other. 

On Windows this can be accomplished with [com0com](https://sourceforge.net/projects/com0com/).

In the above example, we could use com0com to create a virtual null modem with ports COM20 and COM21. 
Ullr would connect to COM20, and the PC software to COM21.

## Licensing and Copyright
GNU GPL v3 License
Copyright (c) Zach Henry.
