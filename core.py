from abc import ABC, abstractmethod
from enum import Enum

class ProcessState(Enum):
    """
    Enum simples dos estados possíveis para um processo.
    """

    NOT_READY = 0,
    READY = 1,
    EXECUTING = 2,
    FINISHED = 3

class Process:
    """
    Classe que representa um processo em execução.
    """

    def __init__(self, pid: int, priority: int, creation_time: int, cpu_time: int):
        self.pid = pid
        self.priority = priority
        self.creation_time = creation_time
        self.cpu_time = cpu_time

        # estado interno
        self.__state: ProcessState = ProcessState.NOT_READY
        self.__time_spent_creating = 0
        self.__time_spent_executing = 0

    def start_executing(self) -> None:
        if self.is_ready():
            self.__state = ProcessState.EXECUTING

    def stop_executing(self) -> None:
        if self.__state == ProcessState.EXECUTING:
            self.__state = ProcessState.READY

    def is_ready(self) -> bool:
        return self.__state == ProcessState.READY
    
    def is_finished(self) -> bool:
        return self.__state == ProcessState.FINISHED

    def update(self, time_elapsed: int = 1) -> None:
        """
        Avança o tempo no contexto do processo.

        Aqui é onde o estado do processo é atualizado.
        """

        if self.__state == ProcessState.NOT_READY:
            self.__time_spent_creating += time_elapsed
            
            if self.__time_spent_creating >= self.creation_time:
                self.__state = ProcessState.READY
        elif self.__state == ProcessState.EXECUTING:
            self.__time_spent_executing += time_elapsed

            if self.__time_spent_executing >= self.cpu_time:
                self.__state = ProcessState.FINISHED
        # se o processo estiver READY ou FINISHED, não faça nada

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
        self.__current_switch_time: int = 0

        self.current_process: Process = None
        self.time: int = 0
    
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

        if self.current_process:
            self.current_process.start_executing()
        
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
        
        # deixa todos os processos atualizarem/executarem
        for proc in self.processes:
            proc.update()

        # tratando tempo de mudança de contexto
        if self.context_switching:
            self.__current_switch_time += 1

            if self.__current_switch_time == self.context_switch_time:
                self.context_switching = False
                self.__current_switch_time = 0

        # se o processo atual terminou, retire ele
        if self.current_process and self.current_process.is_finished():
            self.current_process = None
            self.context_switching = True
        
        self.on_tick()
        self.time += 1

