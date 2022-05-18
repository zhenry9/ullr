
def _cp540(message: str, sequence: int):
    pre_seq = message[:8]
    seq = str(sequence).rjust(4)
    post_seq = message[12:]
    re_seq = f"{pre_seq}{seq}{post_seq}"
    return re_seq

def _timy(message: str, sequence: int):
    pre_seq = message[:1]
    seq = str(sequence).rjust(4)
    post_seq = message[5:]
    re_seq = f"{pre_seq}{seq}{post_seq}"
    return re_seq

def _s4(message: str, sequence: int):
    post_seq = message[4:]
    re_seq = f"{sequence:04x}{post_seq}"
    return re_seq

def _racetime2(message: str, sequence: int):
    post_seq = message[8:]
    re_seq = f"{sequence:04x}{sequence:04x}{post_seq}"
    return re_seq

RESEQUENCE = {
    "cp540": _cp540,
    "timy": _timy,
    "s4": _s4,
    "racetime2": _racetime2
}

def resequence(message, device, sequence):
    return RESEQUENCE[device](message, sequence)