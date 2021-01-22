import os
from configparser import ConfigParser, NoSectionError


class DweetConfiguration(object):

    def __init__(self):
        self.parser = ConfigParser()
        self.home_path = os.path.expanduser('~')
        self.file_name = "config.ini"
        self.default_config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.file_name)
        self.user_config_file = ''
        self._verify_defaults()
        self._update_parser()

    def setup(self):
        self._verify_defaults()
        self._verify_user_file()
        return

    def _update_parser(self):
        self.parser.read(self.default_config_file)
        self.user_config_file = self.parser.get("DEFAULT", "user_config_file")
        self.parser.read(self.user_config_file)
        return

    def _verify_defaults(self):
        if not os.path.exists(self.default_config_file):
            print(f"\nDefault file not found. Creating at {self.default_config_file}")
            self._write_defaults()
        else:
            print(f"\nDefault config file found at {self.default_config_file}")
        return

    def _write_defaults(self):
        # reset parser
        self.parser = ConfigParser()
        self.parser['DEFAULT'] = {"DCE_port": "/dev/ttyUSB0",
                                  "DTE_port": "COM50",
                                  "pc_keyword": "from_PC",
                                  "device_keyword": "from_device",
                                  "thing_id": "dweet2ser_default",
                                  "key": "None",
                                  "user_config_file": ''
                                  }
        self.parser.add_section("User")
        with open(self.default_config_file, 'w') as configfile:
            self.parser.write(configfile)
        return self._update_parser()

    def _write_user_file_path(self, path):
        self.parser["DEFAULT"]["user_config_file"] = path
        with open(self.default_config_file, 'w') as configfile:
            return self.parser.write(configfile)

    def _verify_user_file(self):
        if os.path.exists(self.user_config_file):
            print(f"User config file found at {self.user_config_file}")
            resp = input("  Overwrite? (y/n):")
            if resp == "n":
                return
            else:
                return self._create_user_file(self.user_config_file)
        else:
            print("User config file does not exist.")
            filepath = os.path.join(self.home_path, '.config', 'dweet2ser', self.file_name)
            return self._create_user_file(filepath)

    def _create_user_file(self, path):

        print(f"Writing user config file to: {path}\n"
              f"\nHit enter to accept defaults.")
        keys = ["thing_id",
                "key",
                "DCE_port",
                "DTE_port",
                "pc_keyword",
                "device_keyword",
                ]
        defaults = {}
        for i in range(0, len(keys)):
            defaults[keys[i]] = self.parser.get("DEFAULT", keys[i])

        currents = {}
        for i in range(0, len(keys)):
            try:
                currents[keys[i]] = self.parser.get("User", keys[i])
            except NoSectionError:
                currents[keys[i]] = ''

        inputs = {
            'thing_id': input(f"  Enter thing name (default:{defaults['thing_id']}, current:{currents['thing_id']}):  "),
            'key': input(f"  Enter thing key if locked (default:{defaults['key']}, current:{currents['key']}):  "),
            'DCE_port': input(
                f"  Enter default DCE serial port (default:{defaults['DCE_port']}, current:{currents['DCE_port']}):  "),
            'DTE_port': input(
                f"  Enter default DTE serial port (default:{defaults['DTE_port']}, current:{currents['DTE_port']}):  "),
            'pc_keyword': input(
                f"  Enter PC keyword (default:{defaults['pc_keyword']}, current:{currents['pc_keyword']}):  "),
            'device_keyword': input(
                f"  Enter device keyword (default:{defaults['device_keyword']}, current:{currents['device_keyword']})  :")}

        self._write_user_file_path(path)
        self.parser = ConfigParser()
        self.parser.add_section("User")

        for key in keys:
            if inputs[key] != '':
                self.parser["User"][key] = inputs[key]

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as configfile:
            self.parser.write(configfile)

        print(f"\nUser config file successfully written to: {path}")
        return self._update_parser()
