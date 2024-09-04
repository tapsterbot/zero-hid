import numpy as np
from time import sleep
from . import defaults
from .hid.touch import send_touch_event

def points_between(x1, y1, x2, y2, num_points=10):
    """
    Returns an array of points between two endpoints (x1, y1) and (x2, y2).

    Parameters:
        x1, y1 : float : Coordinates of the first point.
        x2, y2 : float : Coordinates of the second point.
        num_points : int : The number of points to generate between the two endpoints, including the endpoints.

    Returns:
        points : list : A list of tuples representing the points between (x1, y1) and (x2, y2).
    """
    x_values = np.round(np.linspace(x1, x2, num_points), 2)
    y_values = np.round(np.linspace(y1, y2, num_points), 2)

    points = list(zip(x_values, y_values))

    return points

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

    def move(self, x1=0, y1=0, x2=0, y2=0, points=5, delay=0.1):
        points = points_between(x1, y1, x2, y2, num_points=points)
        for point in points:
            send_touch_event(self.dev, round(point[0] * 100), round(point[1] * 100), 1)
            sleep(delay)
        send_touch_event(self.dev, round(points[-1][0] * 100), round(points[-1][1] * 100), 0)

    def __enter__(self):
        return self

    def _clean_resources(self):
        self.dev.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clean_resources()

    def close(self):
        self._clean_resources()