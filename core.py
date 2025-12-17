from abc import ABC, abstractmethod

process_data_example = {
    "pid": int,
    "priority": int,
    
    "arrival_time": int,
    "cpu_time": int
}

class ProcessScheduler(ABC):
    """
    Classe base que representa a simulação abstrata de escalonador de processos.
    Tem o papel de escolher qual processo escalonar e supervisionar a sua execução ao longo do tempo (simulado).
    """

    def __init__(self, context_switch_time: int, process_data: list[dict[str, int]]):
        self.procs_to_create = sorted(process_data, key = lambda p : p["pid"])
        self.ready_processes = []
        self.current_process = None

        self.return_times = []
        self.processes_finished = 0
        self.initial_proc_count = len(process_data)

        self.context_switch_time = context_switch_time
        self.context_switch_counter = 0
        self.context_switching = False
        self.switch_timer = 0 # contador pra quando estiver chaveando contexto

        self.total_time = 0
        self.overhead_time = 0
        
        self.timeline = ""

    def create_processes(self):
        for data in self.procs_to_create:
            if self.total_time >= data["arrival_time"]:
                new_proc = data
                new_proc["execution_timer"] = 0

                self.ready_processes.append(new_proc)
                self.procs_to_create.remove(data)

    @abstractmethod
    def on_tick(self) -> None:
        pass

    @abstractmethod
    def next_process(self) -> dict | None:
        pass

    def start(self) -> None:
        while self.processes_finished < self.initial_proc_count:
            self.create_processes()
            self.on_tick()

            if self.current_process and self.current_process["execution_timer"] == self.current_process["cpu_time"]:
                self.processes_finished += 1
                self.return_times.append(self.total_time - self.current_process["arrival_time"])

                self.current_process = None

                if self.processes_finished == self.initial_proc_count:
                    break

                self.context_switch_counter += 1
                self.context_switching = True

            if self.context_switching:
                if self.context_switch_time > 0:
                    self.switch_timer += 1
                    self.overhead_time += 1

                    self.end_tick()

                    if self.switch_timer == self.context_switch_time:
                        self.switch_timer = 0
                        self.context_switching = False
                else:
                    self.switch_timer = 0
                    self.context_switching = False

                continue

            if not self.current_process:
                self.current_process = self.next_process()

                # se ainda assim não tem nenhum processo disponível, só continue
                if not self.current_process:
                    self.end_tick()
                    continue

            # a partir daqui, tenho um processo de certeza.
            if not self.context_switching:
                self.current_process["execution_timer"] += 1
                self.end_tick()

    def end_tick(self):
        self.total_time += 1

        # linha do tempo
        if self.context_switching:
            self.timeline += "E"
        elif self.current_process:
            self.timeline += str(self.current_process["pid"])
        else:
            self.timeline += "."