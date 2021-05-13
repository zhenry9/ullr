=====
Ullr
=====

A serial <-> MQTT interface for sports timing.
==============================================

Ullr allows for reading and writing data from remote serial devices. It was
designed with ski racing in mind, but can be used to access any remote serial 
device with an available internet connection.

Installation
~~~~~~~~~~~~
.. code-block::

    pip install ullr 

The simplest way to install Ullr is in a Python environment using pip. It is 
recommended, if possible, to install as superuser in Linux environments.

An .msi for the latest Windows release can be found here: 
:xref:`Latest Windows Release`.

Quick Start
~~~~~~~~~~~
From a command line, type :code:`ullr`. Or navigate to the Windows start 
shortcut. By default, Ullr starts a web interface on localhost:5000. navigate
to this page from a browser.

IMAGE HERE

.. toctree::
   :maxdepth: 2
   :includehidden:
   :hidden:
   :caption: Getting Started

   tutorial
   advanced
