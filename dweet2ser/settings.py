
# Used to override the default config file location. If set to None the standard will be used,
# which is ~/.config/dweet2ser/config.ini or /etc/dweet2ser/config.ini if superuser
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
                   "port": "",
                   "thing_name": "dweet2ser_default",
                   "key": "None",
                   "mute": "False",
                   "baud": "9600",
                   "ui": "webapp"
                   }



