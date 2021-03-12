from threading import Lock

from termcolor import colored
from colorama import init as colorama_init, Fore, Style

colorama_init()
s_print_lock = Lock()


def s_print(*a, **b):
    """Thread safe print function"""
    with s_print_lock:
        print(*a, **b)


def s_input(*a):
    """Thread safe input function"""
    with s_print_lock:
        print(*a, end='')
    return input('')


def get_devices_table(session):
    """
    Returns a list of devices in table form.
    """
    def get_table(dev_list):
        cols = ["#".ljust(3),
                "Name".ljust(16),
                "Type".ljust(10),
                "Port".ljust(15),
                "ThingName".ljust(20),
                "Locked".ljust(10),
                "Muted".ljust(10)
                ]
        buf = ''
        header = ''
        for col in cols:
            header = header + f"{col}  "
        buf += (f"\t{Fore.LIGHTWHITE_EX}{header}{Style.RESET_ALL}\n")

        for i in range(0, len(dev_list)):
            num = str(i + 1)
            d = dev_list[i]
            if type(d).__name__ == "LocalDevice":
                buf += (f"\t"
                        f"{num.ljust(3)}  "
                        f"{d.name.ljust(16)}  "
                        f"{colored(d.type.ljust(10), d.type_color)}  "
                        f"{d.port_name.ljust(15)}  "
                        f"{''.ljust(20)}  "
                        f"{''.ljust(10)}  "
                        f"{str(d.mute).ljust(10)}  "
                        )
            if type(d).__name__ == "RemoteDevice":
                buf += (f"\t"
                        f"{num.ljust(3)}  "
                        f"{d.name.ljust(16)}  "
                        f"{colored(d.type.ljust(10), d.type_color)}  "
                        f"{''.ljust(15)}  "
                        f"{d.thing_id.ljust(20)}  "
                        f"{str(d.locked).ljust(10)}  "
                        f"{str(d.mute).ljust(10)}  "
                        )
        buf += "\n"
        return buf
    buffer = ''
    buffer += "\nDCE Devices\n"
    buffer += get_table(session.bus.dce_devices)
    buffer += "\nDTE Devices\n"
    buffer += get_table(session.bus.dte_devices)
    return buffer
