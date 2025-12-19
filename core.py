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
        
        self.timeline = []

    def create_processes(self):
        """
        Verifica se algum processo novo chegou/foi criado e 
        adiciona ele ao final da lista de processos prontos.
        """

        initial_len = len(self.procs_to_create)
        for i in range(initial_len):
            data = self.procs_to_create[0]

            if data["arrival_time"] <= self.total_time:
                data["execution_timer"] = 0

                self.ready_processes.append(data)
                self.procs_to_create.remove(data)

    def start_context_switch(self) -> None:
        assert not self.context_switching

        self.context_switch_counter += 1
        self.context_switching = True

    def stop_context_switch(self) -> None:
        assert self.context_switching

        self.switch_timer = 0
        self.context_switching = False

    def queue_current_process(self) -> None:
        """
        Retorna o processo atual para a lista de processos prontos e começa o chaveamento de contexto.
        """

        self.ready_processes.append(self.current_process)

        self.current_process = None
        self.start_context_switch()

    def remove_current_process(self):
        """
        Remove o processo atual sem retorná-lo à lista de processos prontos e começa o chaveamento de contexto.

        Esse método só deve ser chamado quando o processo atual realizou seu trabalho.
        """

        assert self.current_process_finished()

        self.processes_finished += 1
        self.return_times.append(self.total_time - self.current_process["arrival_time"])

        self.current_process = None
        if len(self.ready_processes) > 0:
            self.start_context_switch()
            # se não houver processos prontos mais, não devemos chavear contexto

    def current_process_finished(self) -> bool:
        return self.current_process and self.current_process["execution_timer"] == self.current_process["cpu_time"]
    
    def simulation_finished(self) -> bool:
        return self.processes_finished == self.initial_proc_count

    @abstractmethod
    def on_tick(self) -> None:
        """
        Método chamado toda vez que o tempo da simulação do escalonador avança.
        
        Mais especificamente, é chamado logo após verificar se algum processo novo chegou,
        e antes de atualizar o processo atual ou chavear contexto.

        A implementação deve ser decidida pelo escalonador concreto.
        """

        pass

    @abstractmethod
    def next_process(self) -> dict | None:
        """
        Método chamado toda vez que o escalonador precisa escolher um novo processo.

        Deve retornar os dados do processo que foi escolhido, ou None somente se não há
        nenhum processo disponível.

        A metodologia de escolha de processo deve ser decidida por implementações concretas.
        """

        pass

    def start(self) -> None:
        """
        Inicia a simulação usando o escalonador.
        """

        while not self.simulation_finished():
            self.create_processes()
            self.on_tick()

            if self.current_process_finished():
                self.remove_current_process()

            if self.context_switching:
                if self.context_switch_time > 0:
                    self.switch_timer += 1
                    self.overhead_time += 1

                    self.end_tick()

                    if self.switch_timer == self.context_switch_time:
                        self.stop_context_switch()
                else:
                    self.stop_context_switch()

                continue

            if not self.current_process:
                self.current_process = self.next_process()

                # se ainda assim não tem nenhum processo disponível, só continue
                if not self.current_process:
                    self.end_tick()
                    continue

            # a partir daqui, tenho um processo de certeza.
            self.current_process["execution_timer"] += 1
            self.end_tick()
            
    def end_tick(self) -> None:
        if not self.simulation_finished():
            self.total_time += 1
            self.write_to_timeline()

    def write_to_timeline(self) -> None:
        if self.context_switching:
            self.timeline.append("E")
        elif self.current_process:
            self.timeline.append(str(self.current_process["pid"]))
        else:
            self.timeline.append(".")
