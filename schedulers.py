from core import ProcessScheduler

class RoundRobinScheduler(ProcessScheduler):
    
    def __init__(self, context_switch_time: int, quantum: int, process_data: list[dict[str, int]]):
        super().__init__(context_switch_time, process_data)

        self.quantum = quantum
        self.quantum_timer = 0

    def on_tick(self) -> None:
        if self.current_process is None or self.context_switching:
            self.quantum_timer = 0
            return

        self.quantum_timer += 1

        if self.quantum_timer == self.quantum and self.current_process["execution_timer"] < self.current_process["cpu_time"]:
            self.quantum_timer = 0
            
            self.ready_processes.append(self.current_process)
            self.current_process = None
            self.context_switch_counter += 1
            self.context_switching = True

    def next_process(self) -> dict | None:
        if len(self.ready_processes) == 0:
            return self.current_process
        
        return self.ready_processes.pop(0)

class PriorityScheduler(ProcessScheduler):

    def on_tick(self) -> None:
        return

    def next_process(self) -> dict | None:
        return None


# testes

"""
ex = [
    {
        "pid": 1,
        "priority": 1,
        
        "arrival_time": 0,
        "cpu_time": 50
    },
    {
        "pid": 2,
        "priority": 0,
        
        "arrival_time": 1,
        "cpu_time": 15
    },
    {
        "pid": 3,
        "priority": 2,
        
        "arrival_time": 3,
        "cpu_time": 10
    },
    {
        "pid": 4,
        "priority": 0,
        
        "arrival_time": 5,
        "cpu_time": 100
    },
    {
        "pid": 5,
        "priority": 3,
        
        "arrival_time": 6,
        "cpu_time": 60
    }
]
"""

ex = [
    {
        "pid": 1,
        "priority": 5,
        
        "arrival_time": 2,
        "cpu_time": 5
    },
    {
        "pid": 2,
        "priority": 5,
        
        "arrival_time": 1,
        "cpu_time": 5
    },
        {
        "pid": 3,
        "priority": 5,
        
        "arrival_time": 3,
        "cpu_time": 5
    }
]

# a = RoundRobinScheduler(1, 20, ex)
# a = RoundRobinScheduler(2, 3, ex)

# a.start()

# print(f"TIMELINE: {a.timeline}")
# assert a.timeline == ".EE222EE111EE333EE22EE11EE33"