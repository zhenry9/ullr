===============
Ullr Quickstart
===============

.. rubric:: A serial <-> MQTT interface for sports timing.

.. figure:: /_static/ullr-signal-flow.png
    
    Ullr signal flow.

Ullr (pronounce "OOH-ler") allows for reading and writing data from remote serial devices. It was
designed with :ref:`ski racing <Wireless ski race timing>` in mind, but can be used to access any remote serial 
device with an available internet connection. It also acts as a hub, allowing 
for an arbitrary number of serial devices to be connected to an arbitrary 
number of software instances.

.. figure:: /_static/device-bus.png

    Multiple devices sharing a single serial connection.

Installation
~~~~~~~~~~~~
.. code-block::

    pip install ullr 

The simplest way to install Ullr is in a Python environment using pip. It is 
recommended, if possible, to install as superuser in Linux environments.

An installer for the latest Windows release can be found here: 
:xref:`windows_latest`.

The latest Debian(amd64) binary can be found here: 
:xref:`deb_64_latest`. 

An in-depth guide to installation on a Raspberry Pi can be found :ref:`here 
<Installing on a Raspberry Pi>`.

Configuring Ullr
~~~~~~~~~~~~~~~~
See the :ref:`Configuration` section for an in-depth guide to configuring Ullr.

Running
~~~~~~~
From a command line, type :code:`ullr`. Or navigate to the Windows start 
shortcut. By default, Ullr starts a web interface on localhost:5000. Navigate
to this page from a browser.

.. figure:: /_static/webui-empty.png

    The Ullr web interface.

See the :ref:`Usage` section for more information.

Get the Source
~~~~~~~~~~~~~~
Ullr is published under the GNU GPL 3 license.

The source is always available on the :xref:`github repo` and available for 
download :xref:`here <source>`.

.. toctree::
    :maxdepth: 2
    :includehidden:
    :caption: Getting Started

    self
    intro

.. toctree::
    :maxdepth: 2
    :includehidden:
    :caption: Installation In-Depth

    null-modems
    raspberry-pi

.. toctree::
    :maxdepth: 2
    :includehidden:
    :caption: Configuration and Use

    configuration
    use

.. toctree::
    :maxdepth: 2
    :includehidden:
    :caption: Example Use Cases
    :glob:

    use-cases/*

.. toctree::
    :maxdepth: 2
    :includehidden:
    :caption: Advanced

    cli
    config-file   

.. toctree::
    :maxdepth: 2
    :includehidden:
    :caption: Reference

    links
    contributing