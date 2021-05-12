from . import _configure


class Session(_configure.UllrConfiguration):

    def __init__(self, ui="webapp"):
        super(Session, self).__init__()
        self.ui = ui
