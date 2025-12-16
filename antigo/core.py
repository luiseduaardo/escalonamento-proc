from abc import ABC, abstractmethod

class Process:
    """
    Classe que representa um processo em execução.
    """

    def __init__(self, pid: int, priority: int, creation_time: int, cpu_time: int):
        self.pid = pid
        self.priority = priority
        self.creation_time = creation_time
        self.cpu_time = cpu_time
        
        self.executing = False
        self.time_spent_creating = 0
        self.time_spent_executing = 0

    def is_created(self) -> bool:
        return self.time_spent_creating == self.creation_time

    def is_finished(self) -> bool:
        return self.time_spent_executing == self.creation_time

    def tick_create(self) -> None:
        assert not self.is_created()

        self.time_spent_creating += 1

    def tick_execute(self) -> None:
        assert self.executing and not self.is_finished()

        self.time_spent_executing += 1
        

class ProcessScheduler(ABC):
    """
    Classe base que representa a simulação abstrata de escalonador de processos.
    Tem o papel de escolher qual processo escalonar e supervisionar a sua execução ao longo do tempo (simulado).
    """

    def __init__(self, ctx_switch_time: int, processes: list[Process] = []):
        self.processes: dict[int, Process] = { proc.pid: proc for proc in processes }
        self.process_count: int = len(processes)

        self.context_switch_time: int = ctx_switch_time
        self.context_switching: bool = False
        self.current_switch_time: int = 0

        self.current_process: Process = None
        self.time: int = 0

    def add_process(self, process: Process) -> None:
        """
        Adiciona um processo novo ao escalonador.
        
        Cria um AssertionError em caso do processo não estar em condições para ser escalonado (não está pronto).
        """

        assert process.is_created()

        self.processes.update(process.pid, process)
    
    @abstractmethod
    def choose_process(self) -> Process | None:
        """
        Método chamado toda vez que o escalonador precisa escolher um novo processo.
        Deve retornar o processo escolhido ou None somente se não há processos disponíveis.

        A metodologia de escolha de processo deve ser decidida por implementações concretas.
        """

        pass

    @abstractmethod
    def on_tick(self) -> None:
        """
        Método chamado toda vez que o tempo da simulação do escalonador avança, APÓS todos os processos atualizarem.

        A implementação deve ser decidida pelo escalonador concreto.
        """

        pass

    def get_new_process(self) -> None:
        """
        Atualiza o processo atual escolhido pelo escalonador e atualiza o seu estado.
        """

        self.current_process = self.choose_process()
        ...
        
    def tick(self) -> None:
        """
        Avança o tempo da simulação.

        Aqui o escalonador deixa processos executarem e também 
        escalona um processo novo se não há nenhum ativo no começo do instante inicial
        ou quando for necessário de acordo com a estratégia do escalonador.
        """

        # se nenhum processo estiver ativo, escalone um processo
        if not self.current_process and not self.context_switching:
            self.get_new_process()
        
        if self.current_process:
            self.current_process.tick_execute()

        # tratando tempo de mudança de contexto
        if self.context_switching:
            self.__current_switch_time += 1

            if self.current_switch_time == self.context_switch_time:
                self.context_switching = False
                self.current_switch_time = 0

        # se o processo atual terminou, retire ele
        if self.current_process and self.current_process.is_finished():
            self.processes.pop(self.current_process.pid)
            self.current_process = None
            
            self.context_switching = True
        
        self.on_tick()
        self.time += 1

