from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

class ProcessState(Enum):
    """
    Enum simples dos estados possíveis para um processo.
    """

    NOT_READY = 0,
    READY = 1,
    EXECUTING = 2

@dataclass
class Process:
    """
    Classe que representa um processo em execução.
    """

    pid: int
    priority: int
    creation_time: int
    cpu_time: int
    state: ProcessState

class ProcessScheduler(ABC):
    """
    Classe base que representa a simulação abstrata de escalonador de processos.
    Tem o papel de escolher qual processo escalonar e supervisionar a sua execução ao longo do tempo (simulado).
    """

    def __init__(self, ctx_switch_time: int, processes: list[Process] = []):
        self.context_switch_time = ctx_switch_time
        self.processes = { proc.pid: proc for proc in processes }
        self.process_count = len(processes)

        self.current_process = None
        self.time = 0
    
    @abstractmethod
    def choose_process(self) -> Process:
        """
        Método chamado toda vez que o escalonador precisa escolher um novo processo.
        A metodologia de escolha de processo deve ser decidida por implementações concretas.
        """

        pass

    @abstractmethod
    def on_tick(self) -> None:
        """
        Método chamado toda vez que o tempo da simulação do escalonador avança.
        A implementação deve ser decidida pelo escalonador concreto.
        """

        pass

    def tick(self) -> None:
        """
        Avança o tempo da simulação.
        Aqui o escalonador deixa processos executarem e também 
        escalona um processo novo se não há nenhum ativo no começo do instante inicial
        ou quando for necessário de acordo com a estratégia do escalonador.
        """

        # se nenhum processo estiver ativo, escalone um processo
        if not self.current_process:
            self.current_process = self.choose_process()
        
        # deixando o processo executar
        ... # atualizar estado do processo

        # on tick?
        self.on_tick()
        self.time += 1

        # a ordem desses eventos tá meio esquisita

