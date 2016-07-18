'''
    This is a function that times a function call and raises an error if the function execution time exceeds some threshold
    Original Source: http://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish

    Example Usage:
    import time
    with timeout(seconds=3):
        time.sleep(4)
'''

import signal


class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise StandardError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)
