# queues.py

from collections import deque
from heapq import heappop, heappush
from itertools import count


# ...

class PriorityQueue:
    def __init__(self):
        self.size = 0
        self._elements = []
        self._counter = count()

    def enqueue_with_priority(self, priority, value):
        self.size += 1
        element = (-priority, next(self._counter), value)
        heappush(self._elements, element)

    def dequeue(self):
        self.size -= 1
        return heappop(self._elements)[-1]
