from time import time
from datetime import timedelta


class Stopwatch:
    def __init__(self):
        """Constructor"""
        self.__start = None
        self.__end = None
        self.__round_start = None
        self.__rounds = None

    @property
    def elapsed(self):
        """Returns elapsed time"""
        if not self.__start or not self.__end:
            raise Exception("No start or end time assigned")
        return timedelta(0, (self.__end - self.__start))

    @property
    def elapsed_str(self):
        """Returns string of elapsed time"""
        return "Elapsed time: " + str(self.elapsed)

    @property
    def average(self):
        """Returns average time"""
        if len(self.__rounds) == 0:
            raise Exception("Rounds list is empty")
        total_time = timedelta(0, 0)
        for round_ in self.__rounds:
            total_time += round_
        return total_time / len(self.__rounds)

    @property
    def average_str(self):
        """Returns string of average time"""
        return "Average time for {0} rounds: {1}".format(len(self.__rounds), str(self.average))

    def start(self):
        """Starts stopwatch"""
        self.__start = time()
        self.__round_start = time()
        self.__rounds = []

    def stop(self):
        """Stops stopwatch"""
        self.__end = time()

    def round(self):
        """Saves time for one round"""
        if not self.__round_start:
            raise Exception("No round start time assigned")
        round_time = time() - self.__round_start
        self.__rounds.append(timedelta(0, round_time))
        self.__round_start = time()

    def reset(self):
        """Resets stopwatch"""
        self.__start = None
        self.__end = None
        self.__round_start = None
        self.__rounds = None
