import time
from datetime import timedelta


class Stopwatch:
    def __init__(self):
        """Constructor"""
        self.__round_start_time = None
        self.__round_end_time = None
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None
        self.round_list = None
        self.average_time = None

    def start(self):
        """Starts stopwatch"""
        self.start_time = time.time()
        self.__round_start_time = time.time()
        self.round_list = list()

    def stop(self):
        """Stops stopwatch"""
        if self.start_time is None:
            raise Exception("No start time assigned")

        self.end_time = time.time()
        self.elapsed_time = timedelta(0, (self.end_time - self.start_time))
        if len(self.round_list) > 0:
            total_time = timedelta(0, 0)
            for round_ in self.round_list:
                total_time += round_
            self.average_time = total_time / len(self.round_list)

    def round(self):
        """Saves time for one round"""
        if self.__round_start_time is None:
            raise Exception("No round start time")

        self.__round_end_time = time.time()
        round_time = self.__round_end_time - self.__round_start_time
        self.round_list.append(timedelta(0, round_time))
        self.__round_start_time = time.time()

    def print_elapsed_time(self, message="Elapsed time:"):
        """Returns elapsed time"""
        if self.elapsed_time is None:
            raise Exception("No elapsed time assigned")
        print(message, self.elapsed_time)

    def print_average_time(self, message="Average time for {0} rounds: {1}"):
        """Prints average time for rounds"""
        if self.round_list is None:
            raise Exception("No round list assigned")
        if self.average_time is None:
            raise Exception("No average round time assigned")
        if len(self.round_list) == 0:
            raise Exception("Length of round list is zero")

        rounds = len(self.round_list)
        print(message.format(rounds, self.average_time))

    def reset(self):
        """Resets stopwatch"""
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None
        self.__round_start_time = None
        self.__round_end_time = None
        self.round_list = None
        self.average_time = None
