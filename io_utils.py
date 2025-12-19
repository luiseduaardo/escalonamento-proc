from core import *

def read_file(filename: str):
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

def format_timeline(timeline: list[str]):
    if not timeline: return ""
    
    formatted = []
    current_str = timeline[0]
    label = "Escalonador" if current_str == "E" else (f"Processo {current_str}" if current_str != "." else "Ocioso")
    start = 0

    for i, s in enumerate(timeline):
        if s != current_str:
            formatted.append(f"[{start}-{i}] {label}")
            label = "Escalonador" if s == "E" else (f"Processo {s}" if s != "." else "Ocioso")
            current_str = s
            start = i
            
    label = "Escalonador" if current_str == "E" else (f"Processo {current_str}" if current_str != "." else "Ocioso")
    formatted.append(f"[{start}-{len(timeline)}] {label}")
    
    return "\n".join(formatted)

def save_file(file_obj: str, algo_name: str, scheduler: ProcessScheduler):
    file_obj.write(f"------------ {algo_name} ------------")
    file_obj.write("\nLINHA DO TEMPO DE OCUPAÇÃO DA CPU: ")
    for s in scheduler.timeline:
        file_obj.write(f"({s})")

    file_obj.write("\n")
    file_obj.write(format_timeline(scheduler.timeline))

    average = 0
    for n in scheduler.return_times:
        average += n
    average /= len(scheduler.return_times)

    file_obj.write(f"\n\nTempo médio de retorno: {average}")
    file_obj.write(f"\nTempo total de simulação: {scheduler.total_time}")
    file_obj.write(f"\nTempo executando processos: {scheduler.total_time - scheduler.overhead_time}")
    file_obj.write(f"\nTempo chaveando contexto: {scheduler.overhead_time}")
    file_obj.write(f"\nNúmero de chaveamentos: {scheduler.context_switch_counter}")
    file_obj.write(f"\nOverhead: {(scheduler.overhead_time / scheduler.total_time)*100:.2f}%")
