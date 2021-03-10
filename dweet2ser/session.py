from . import _configure


class DweetSession(_configure.Dweet2serConfiguration):

    def __init__(self, ui="webapp"):
        super(DweetSession, self).__init__()
        self.ui = ui
