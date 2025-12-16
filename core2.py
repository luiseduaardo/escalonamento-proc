class Process:
    """
    Classe que representa um processo em execução.
    """

    def __init__(self, pid: int, priority: int, creation_time: int, cpu_time: int):
        self.pid = pid
        self.priority = priority
        self.creation_time = creation_time
        self.cpu_time = cpu_time
        
        self.execution_time = 0
        self.finish_time = 0