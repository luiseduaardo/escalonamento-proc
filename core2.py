class Process:
    """
    Classe que representa um processo em execução.
    """

    def __init__(self, pid: int, priority: int, creation_time: int, cpu_time: int):
        self.pid = pid
        self.priority = priority
        self.creation_time = creation_time
        self.cpu_time = cpu_time
        
        self.start_time = -1
        self.finish_time = 0

    def clone(self):
        return Process(self.id, self.priority, self.creation_time, self.cpu_time)