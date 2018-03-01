import time
import datetime


class Stopwatch:
    """
    Stopwatch class.
    """
    def __init__(self):
        """
        Constructor.

        :return: new instance
        """
        self._start = None
        self._end = None
        self._round_start = None
        self._rounds = None

    @property
    def elapsed(self):
        """
        Returns elapsed time.

        :return: timedelta
        """
        if not self._start or not self._end:
            raise Exception("No start or end time assigned")
        return datetime.timedelta(0, (self._end - self._start))

    @property
    def elapsed_str(self):
        """
        Returns string of elapsed time.

        :return: str
        """
        return "Elapsed time: {}".format(str(self.elapsed))

    @property
    def average(self):
        """
        Returns average time.

        :return: timedelta
        """
        if len(self._rounds) == 0:
            raise Exception("Rounds list is empty")
        total_time = datetime.timedelta(0, 0)
        for round_ in self._rounds:
            total_time += round_
        return total_time / len(self._rounds)

    @property
    def average_str(self):
        """
        Returns string of average time.

        :return: str
        """
        return "Average time for {} rounds: {}".format(len(self._rounds), str(self.average))

    def start(self):
        """
        Starts stopwatch.

        :return: None
        """
        self._start = time.time()
        self._round_start = time.time()
        self._rounds = []

    def stop(self):
        """
        Stops stopwatch.

        :return: None
        """
        self._end = time.time()

    def round(self):
        """
        Saves time for one round.

        :return: None
        """
        if not self._round_start:
            raise Exception("No round start time assigned")
        round_time = time.time() - self._round_start
        self._rounds.append(datetime.timedelta(0, round_time))
        self._round_start = time.time()

    def reset(self):
        """
        Resets stopwatch.

        :return: None
        """
        self._start = None
        self._end = None
        self._round_start = None
        self._rounds = None
