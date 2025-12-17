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

    def __init__(self, context_switch_time: int, process_data: list[dict[str, int]]):
        super().__init__(context_switch_time, process_data)

        # função ordenando por prioridade. em caso de empate, o menor PID ganha
        self.ordering_function = lambda p : (p["priority"], p["pid"])

    def on_tick(self) -> None:
        if len(self.ready_processes) == 0:
            return

        max_proc = max(self.ready_processes, key=self.ordering_function)

        # se tiver algum processo com prioridade maior/PID menor que o processo atual, pegue um processo novo 
        if self.current_process and min(max_proc, self.current_process, key=self.ordering_function) == max_proc:
            self.ready_processes.append(self.current_process)
            self.current_process = None
            self.context_switch_counter += 1
            self.context_switching = True

    def next_process(self) -> dict | None:
        if len(self.ready_processes) == 0:
            return self.current_process
        
        self.ready_processes.sort(key=self.ordering_function)
        return self.ready_processes.pop(0)