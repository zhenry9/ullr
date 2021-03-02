# All encode functions take a channel and tod (time of day) argument. The channel argument is a list.
# The first item on the list is an integer representing the actual channel number. The channel number should
# be normalized, so the first channel is 0, whether or not the timer itself starts its channel counts at 0.
# The second item in the channel list argument is a boolean value indicating whether or not the impulse was 
# manual, eg. from a pushbutton on the timer. So, a channel argument of [0, True] would compute to "c0M" on 
# an Alge Timy, because Timy channels start at 0. It would compute to "M1" on a Tag CP540 because CP540 
# channels start at 1, and "SZ " on an s4 because s4s are weird. The same logic applies to decoding.

class TranslationError(Exception):
    pass

def _decode_cp540(message):
    chan = message[13:15]
    tod = message[16:29]
    channel = ['', False]
    if chan[0].upper() == "M":
        channel[1] = True
    channel[0] = int(chan[1]) - 1  # First channel of CP540 is 1. This normalizes to first channel of 0
    return channel, tod

def _encode_cp540(channel, tod):
    channel[0] += 1  # First channel of CP540 is 1, not 0.
    if channel[0] > 8:
        raise TranslationError(f"Channel {channel[0]} out of range for CP540.")
    if channel[1]:
        chan = f"M{channel[0]}"
    else:
        chan = f" {channel[0]}"
    msg = f"TN           {chan} {tod}      "
    cs16 = f'{int(sum(bytearray(msg.encode("ascii"))) % 65536):04x}'.upper() #calculate checksum
    msg += f"\t{cs16}\r\n"
    return msg

def _decode_timy(message):
    chan = message[6:10]
    tod = message[10:23]
    channel = ["", False]
    if chan[2].upper() == "M":
        channel[1] = True
    channel[0] = int(chan[1])
    return channel, tod

def _encode_timy(channel, tod):
    if channel[0] > 7:
        raise TranslationError(f"Channel {channel[0]} out of range for Timy.")
    if channel[1]:
        chan = f"c{channel[0]}M"
    else:
        chan = f"c{channel[0]} "
    msg = f"      {chan} {tod}       \r"
    return msg 

def _decode_s4(message):
    chan = message[5:8]
    tod = message[9:21] + "0"  # add zero to normalize TOD to 1/10,000 format
    channel = ["", False]
    if chan.upper()[:2] == "SZ":
        channel[0] = 0
    else:
        channel[0] = int(chan[1:])
    return channel, tod

def _encode_s4(channel, tod):
    if channel[0] > 17:
        raise TranslationError(f"Channel {channel[0]} out of range for S4.")
    if channel[0] == 0:
        chan = "SZ "
    else:
        chan = f"K{channel[0]:02d}"
    tod = str(tod)[:12]  # remove last digit as S4 only goes to 1/1,000s
    msg = f"0000 {chan} {tod}\r"
    return msg


ENCODE = {
    "cp540": _encode_cp540,
    "timy": _encode_timy,
    "s4": _encode_s4
}

DECODE = {
    "cp540": _decode_cp540,
    "timy": _decode_timy,
    "s4": _decode_s4
}

def translate(message, source, destination, shift=0):
    channel, tod = DECODE[source](message)
    channel[0] += shift
    translation = ENCODE[destination](channel, tod)
    return translation