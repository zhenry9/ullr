# dweet2ser
A serial <-> dweet.io interface

<img src="https://github.com/zhenry9/dweet2ser/blob/main/dweet2ser-signal-flow.png" height="300" align="middle">

dweet2ser allows for the two-way exchange of data between a serial device and a PC over the internet, using the free [dweet.io](https://dweet.io) API as an intermediary. This is particularly useful for connecting to faraway devices that aren't on the same LAN.

dweet2ser works for connecting remotely to things like weather stations, sensors, or other devices that send simple data intermittently. It is not going to work for things like modems, due to the limitations of dweet.io among other things.

## Installation
### Python environment
This package is not yet published on PyPI, but you can use pip to install the github repository:
  
`pip install git+https://github.com/zhenry9/dweet2ser.git#egg=dweet2ser`
  
### Windows executable
If you don't have a Python environment on your computer, you can download the files in the `windows` folder.

### Get the source
The source code is always available at [https://github.com/zhenry9/dweet2ser](https://github.com/zhenry9/dweet2ser).

## Configuration
Modify config.txt to suit your needs. Locked dweet.io things are supported.

## Usage

### Display help page

`dweet2ser -h`
  
This prints out the help page for command line options.

### On the device side of the connection:
  
`dweet2ser DCE -p /dev/tty0`
 
This opens an instance of dweet2ser in DCE mode on the linux port /dev/tty0. If you don't specify a port, the default from config.txt will be used. DCE mode means we are on the device side, sending data to the PC (DTE) side.

### On the PC side of the connection:
  
`dweet2ser DTE -p COM50`

This opens an instance of dweet2ser in DTE mode on windows port COM50. If you don't specify a port, the default from config.txt will be used. DTE mode means we are on the PC side, listening to data from the device (DCE) side.

### Virtual COM ports
On the PC (DTE) side you'll need to set up a virtual null modem to allow dweet2ser to communicate with the target software. This is just a pair of com ports connected to each other. dweet2ser connects to one port, and your software application connects to the other. 

On Windows this can be accomplished with [com0com](http://com0com.sourceforge.net/).

In the above example, we could use com0com to create a virtual null modem with ports COM50 and COM51. dweet2ser would connect to COM50, and the PC software to COM51.

## Licensing and Copyright
MIT License
Copyright (c) Zach Henry.
