import sys
from schedulers import RoundRobinScheduler, PriorityScheduler
from core import ProcessScheduler
from io_utils import read_file, save_file

def main():
    input_file, output_file = "test/inputs/"+sys.argv[1], "test/saida_obtida/"+sys.argv[2]

    quantum, ctx_switch_t, proc_list = read_file(input_file)

    round_robin = RoundRobinScheduler(ctx_switch_t, quantum, proc_list)
    round_robin.start()

    priority = PriorityScheduler(ctx_switch_t, proc_list)
    priority.start()

    with open(output_file, "w+") as file:
        save_file(file, "ROUND ROBIN", round_robin)
        file.write("\n\n")
        save_file(file, "PRIORITY", priority)

if __name__ == "__main__":
    main()