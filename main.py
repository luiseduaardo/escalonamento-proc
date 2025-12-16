from core import *
from schedulers import *

entradas = []

with open("EntradaProcessos.txt", "r") as arquivo:
    for linha in arquivo:
        entradas.append(linha.strip('\n').split(','))

# nProc,quantum,tTroca
nProc, quantum, tTroca = int(entradas[0][0]), int(entradas[0][1]), int(entradas[0][2])

lista_processos = []

# ID,Tch,Prio,Tcpu
for i in range(1, nProc+1):
    pid = int(entradas[i][0])
    creation_time = int(entradas[i][1])
    priority = int(entradas[i][2])
    cpu_time = int(entradas[i][3])

    lista_processos.append(Process(pid, priority, creation_time, cpu_time))

