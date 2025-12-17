from schedulers import RoundRobinScheduler, PriorityScheduler
from core import ProcessScheduler

def read_file(filename):
    input = []

    with open(filename, "r") as file:
        for linha in file:
            input.append(linha.strip('\n').split(','))

    proc_count, quantum, ctx_switch_t = int(input[0][0]), int(input[0][1]), int(input[0][2])

    process_list = []

    # ID,Tch,Prio,Tcpu
    for i in range(1, proc_count+1):
        pid = int(input[i][0])
        creation_time = int(input[i][1])
        priority = int(input[i][2])
        cpu_time = int(input[i][3])

        process_list.append({
            "pid": pid,
            "priority": priority,
            "arrival_time": creation_time,
            "cpu_time": cpu_time
        })
    
    return quantum, ctx_switch_t, process_list

def print_info(scheduler: ProcessScheduler):
    print("----- TIMELINE -----")
    print(scheduler.timeline)

    average = 0
    for n in scheduler.return_times:
        average += n
    average /= len(scheduler.return_times)

    print(f"Tempo médio de retorno: {average}")
    print(f"Tempo total: {scheduler.total_time - scheduler.overhead_time}")
    print(f"Número de chaveamentos: {scheduler.context_switch_counter}")
    print(f"Overhead: {(scheduler.overhead_time / scheduler.total_time):.4f}")

def main():
    quantum, ctx_switch_t, proc_list = read_file("test/2.txt")

    round_robin = RoundRobinScheduler(ctx_switch_t, quantum, proc_list)
    priority = PriorityScheduler(ctx_switch_t, proc_list)

    round_robin.start()
    priority.start()

    print_info(round_robin)
    print("--------------------")
    print_info(priority)

if __name__ == "__main__":
    main()