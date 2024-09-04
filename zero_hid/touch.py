from time import sleep
from . import defaults
from .hid.touch import send_touch_event

class Touch:
    def __init__(self, dev=defaults.TOUCH_PATH) -> None:
        if not hasattr(dev, "write"):  # check if file like object
            self.dev = open(dev, "ab+")
        else:
            self.dev = dev

    def tap(self, x = 0, y = 0):
        x = round(x*100)
        y = round(y*100)
        send_touch_event(self.dev, x, y, 1)
        sleep(.1)
        send_touch_event(self.dev, x, y, 0)

    def __enter__(self):
        return self

    def _clean_resources(self):
        self.dev.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clean_resources()

    def close(self):
        self._clean_resources()