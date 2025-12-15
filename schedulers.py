from core import Process, ProcessScheduler

class RoundRobinScheduler(ProcessScheduler):

    def __init__(self, ctx_switch_time: int, quantum: int, processes: list[Process] = []):
        super().__init__(ctx_switch_time, processes)
        self.quantum = quantum

    def choose_process(self) -> Process | None:
        ...

    def on_tick(self) -> None:
        ...

class PriorityScheduler(ProcessScheduler):

    def choose_process(self) -> Process | None:
        ...

    def on_tick(self) -> None:
        ...