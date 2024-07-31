import time


class Timer:
    def __init__(self, timeLeft=0):
        self.endTimeReference = time.time() + timeLeft

    def getTimeLeft(self):
        seconds = round(self.endTimeReference - time.time())
        if seconds <= 0:
            self.endTimeReference = time.time()
            return 0

        return round(self.endTimeReference - time.time())

    def addSeconds(self, seconds):
        if self.getTimeLeft() == 0:
            self.endTimeReference = time.time()

        self.endTimeReference += seconds