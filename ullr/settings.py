
# Used to override the default config file location. If set to None the standard will be used,
# which is ~/.config/ullr/config.ini or /etc/ullr/config.ini if superuser
USER_SPECIFIED_DEFAULT_CONFIG_FILE = None

USER_SPECIFIED_LOG_FILE = None

CONFIG_COMMENTS = str("\n; The settings in the [DEFAULT] section reference the values set in 'settings.py' " +
                      "in the package directory." +
                      "\n; They should be here for config file stability." +
                      "\n; If you would like to change these default settings permanently, " +
                      "you should do so in settings.py, not here." +
                      "\n; Make sure you know what you're doing.\n\n")

# defaults when writing new configuration
CONFIG_DEFAULTS = {"type": "",
                   "location": "",
                   "mute": "False",
                   "accepts_incoming": "True",
                   "port": "",
                   "topic_name": "defualt_client/default_device",
                   "baud": "9600",
                   "published": "False",
                   "on_time_max": "0",
                   "translated": "False",
                   "translated_from": "None",
                   "translated_to": "None",
                   "channel_shift": "0",
                   "mqtt_broker_url": "57edaf7763054ccc91c1c8b6e646a155.s1.eu.hivemq.cloud",
                   "mqtt_broker_port": "8883",
                   "mqtt_broker_user": "PiTiming",
                   "mqtt_broker_pw": "Mammoth1"
                   }
