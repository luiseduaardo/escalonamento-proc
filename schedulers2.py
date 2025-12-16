from core2 import *
from collections import deque

class RoundRobin:
    def __init__(self, processes: list[Process], quantum: int, ctx_switch_time: int):
        self.process_list = processes
        self.quantum = quantum
        self.ctx_switch_time = ctx_switch_time
        self.queue = deque()
        self.time_now = 0

    def execute(self):
        pass

class Priority:
    def __init__(self, processes: list[Process], ctx_switch_time: int):
        self.process_list = processes
        self.ctx_switch_time = ctx_switch_time
        self.time_now = 0

    def execute(self):
        pass