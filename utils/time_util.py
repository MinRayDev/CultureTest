import time
from decimal import Decimal


def has_elapsed(start_time: float, interval_duration: float | Decimal) -> bool:
    """Returns True if the time 'start_time' added to the interval duration elapsed.

        :param start_time: The start time of the interval.
        :type start_time: float.

        :param interval_duration: The duration of the interval in seconds.
        :type interval_duration: float.

        :return: True if elapsed.
        :rtype: bool.

    """
    if isinstance(interval_duration, Decimal):
        interval_duration = float(interval_duration)
    return time.time() > start_time + interval_duration
