import time
import signal

class TimeoutException(Exception):
    pass

def alarm_handler(signum, frame):
    raise TimeoutException()