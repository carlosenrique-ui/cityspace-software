import time

class TimeBase:
    def __init__(self):
        self.t0 = time.time()
        self.paused = False
        self.offset = 0.0

    def now(self):
        if self.paused:
            return self.offset
        return time.time() - self.t0

    def pause(self):
        self.offset = self.now()
        self.paused = True

    def resume(self):
        self.t0 = time.time() - self.offset
        self.paused = False
