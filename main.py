from schedulers import RoundRobinScheduler, PriorityScheduler

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

def main():
    quantum, ctx_switch_t, proc_list = read_file("test/1.txt")

    round_robin = RoundRobinScheduler(ctx_switch_t, quantum, proc_list)
    priority = PriorityScheduler(ctx_switch_t, proc_list)

    round_robin.start()
    priority.start()

    print(round_robin.timeline)
    average = 0
    for n in round_robin.return_times:
        average += n
    average /= len(round_robin.return_times)
    print(f"Tempo médio de retorno: {average}")
    print(f"Tempo total: {round_robin.total_time - round_robin.overhead_time}")
    print(f"Número de chaveamentos: {round_robin.context_switch_counter}")
    print(f"Overhead: {(round_robin.overhead_time / round_robin.total_time):.4f}")

    print("--------------------")
    print(priority.timeline)
    average = 0
    for n in priority.return_times:
        average += n
    average /= len(priority.return_times)
    print(f"Tempo médio de retorno: {average}")
    print(f"Tempo total: {priority.total_time - priority.overhead_time}")
    print(f"Número de chaveamentos: {priority.context_switch_counter}")
    print(f"Overhead: {(priority.overhead_time / priority.total_time):.4f}")

if __name__ == "__main__":
    main()