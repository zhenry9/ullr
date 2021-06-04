Using the Config File
=====================
Ullr can be configured using the :ref:`interactive web interface <Configuration>`. 
However, configuration can be achieved by simply modifying the config file.

The Ullr config file follows `INI format <https://en.wikipedia.org/wiki/INI_file>`_. 
Each section represents a device, with the exception of the DEFAULT and $mqtt 
sections.

Finding the config file
~~~~~~~~~~~~~~~~~~~~~~~
A default config file is created the first time Ullr is run. Before that, the 
config file will not exist.

The location of the config file depends on your operating system, and whether you 
are running as :ref:`superuser (root) <Superuser>` or as a regular user.

On Windows, the config file will be located in the .config subfolder of your home 
directory. For example, C:\\users\\zhenry\\.config\\ullr\\config.ini.

The same applies for Linux if run as a regular user. For example, 
/home/zhenry/.config/ullr/config.ini.

If run on Linux as superuser the config file will be located at 
/etc/ullr.config.ini.

Default config settings
~~~~~~~~~~~~~~~~~~~~~~~
Let's take a look at the 'DEFAULT' section of the config file. These are the device 
settings that Ullr falls back to if you don't specify anything different.

.. code-block:: toml

    [DEFAULT]
    type = 
    location = 
    mute = False
    accepts_incoming = True
    port = 
    topic_name = defualt_client/default_device
    baud = 9600
    published = False
    on_time_max = 0
    translated = False
    translated_from = None
    translated_to = None
    channel_shift = 0
    mqtt_broker_url = 57edaf7763054ccc91c1c8b6e646a155.s1.eu.hivemq.cloud
    mqtt_broker_port = 8883
    mqtt_broker_user = PiTiming
    mqtt_broker_pw = Mammoth1

Type and location have no default. Type can be either DCE or DTE, and localtion 
can be either remote or local. The rest of the default settings are fairly 
self-explanatory.

MQTT broker settings
~~~~~~~~~~~~~~~~~~~~
The :ref:`MQTT broker <MQTT Messaging Protocol>` settings are under a special 
section named '$mqtt'. We'll stick with the default settings for this example, 
but you can use any broker setings you'd like. Using a private broker provides 
added security.

.. code-block:: toml

    [$mqtt]
    mqtt_broker_url = 57edaf7763054ccc91c1c8b6e646a155.s1.eu.hivemq.cloud
    mqtt_broker_port = 8883
    mqtt_broker_user = PiTiming
    mqtt_broker_pw = Mammoth1

Adding a device
~~~~~~~~~~~~~~~
To add and configure a device, all we have to do is add a section with the 
device name. For example, say we want to add a local DCE device called "Finish 
Timer". Let's say it's 9600 baud and plugged into COM3. We'd add the following 
section:

.. code-block:: toml

    [Finish Timer]
    type = DCE
    location = local
    port = COM3
    baud = 9600

That's it! Note that any key value we didn't specify will fall back to the 
default: this device won't be muted, it will accept incoming messages, and it 
won't be translated or published. To change any of these settings, we just have 
to add the appropriate key value to the section.