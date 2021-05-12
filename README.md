# ULLR
### Pronounced "OOH-ler"
A serial <-> MQTT interface for sports timing.

<img src="https://github.com/zhenry9/ullr/raw/main/ullr-signal-flow.png" height="300" align="middle">

Ullr allows for the two-way exchange of data between serial devices and computers over the internet, 
using MQTT as an intermediary. 
This is particularly useful for connecting to faraway devices that aren't on the same LAN. 
Ullr allows for connecting an arbitrary number of devices to an arbitrary number of computers.

Ullr works for connecting remotely to things like weather stations, sensors, or other devices that send 
simple data intermittently. It is not designed for high volume devices like modems or printers.

## Installation
### Python environment
  
`pip install ullr`
  
### Windows executable
If you don't have or don't wish to use a Python environment, a Windows executable version is available in the source
repository on GitHub.

### Get the source
The source code is always available at [https://github.com/zhenry9/Ullr](https://github.com/zhenry9/Ullr).

## Configuration
Modify `config.ini` to suit your needs, or configure interactively using the the software. The web interface is fully featured to alow for the configuration of device and MQTT broker settings.

## Usage

Ullr borrows terminology from the original RS232 protocol. 

### Default
`Ullr`

This starts Ullr with a web interface on `localhost:5000`.
If Ullr is run without command line options, it will attempt to load devices from the default config file. This
will be '~/.config/ullr/config.ini', or '/etc/ullr/config.ini' if run as superuser. 
If you are running Ullr for the first time or with an empty config file, no devices will be loaded. You can add
devices interactively using the web interface.

### CLI
`ullr --nowebui`

This will load Ullr with a command line interface only, whithout the web interface. 
Configuration can be done interactively from the command line.

### Empty
`ullr --empty`

This will ignore the default config file and start Ullr without any devices loaded. This is useful for fixing bad
config files, or creating new ones from scratch.

### From file
`ullr --file FILENAME`

This will attempt to start Ullr by loading the devices specified in an arbitrary config file at FILENAME.


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
