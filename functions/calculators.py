import heapq
from math import sqrt

class MeanCalculator:
    def __init__(self, instrument, date_filter=None):
        self.instrument = instrument
        self.date_filter = date_filter
        self.total = 0.0
        self.count = 0

    def process(self, row):
        if row.instrument == self.instrument and (self.date_filter is None or self.date_filter(row.date)):
            self.total += row.value
            self.count += 1

    def mean_result(self):
        return self.total / self.count if self.count > 0 else 0.0


class LatestSumCalculator:
    def __init__(self, exclude_instruments, top_n):
        self.exclude_instruments = set(exclude_instruments)
        self.top_n = top_n
        self.heap = []

    def process(self, row):
        if row.instrument not in self.exclude_instruments:
            heapq.heappush(self.heap, (row.date.timestamp(), row.value))
            if len(self.heap) > self.top_n:
                heapq.heappop(self.heap)

    def sum_result(self):
        return sum(value for _, value in self.heap)

class MeanStdDevCalculator:
    def __init__(self, instrument):
        self.instrument = instrument
        self.count = 0
        self.mean = 0.0
        self.M2 = 0.0

    def process(self, row):
        if row.instrument == self.instrument:
            self.count += 1
            delta = row.value - self.mean
            self.mean += delta / self.count
            delta2 = row.value - self.mean
            self.M2 += delta * delta2


    def mean_result(self):
        return self.mean if self.count > 0 else 0.0

    def stddev_result(self):
        if self.count < 2:
            return 0.0
        return sqrt(self.M2 / (self.count - 1))