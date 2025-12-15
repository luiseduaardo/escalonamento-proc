entradas = []

with open("EntradaProcessos.txt", "r") as arquivo:
    for linha in arquivo:
        entradas.append(linha.strip('\n').split(','))

nProc, quantum, tTroca = int(entradas[0][0]), int(entradas[0][1]), int(entradas[0][2])


for i in range(nProc):
    #pega as infos e joga na classe
    pass

