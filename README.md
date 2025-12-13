# escalonamento-proc

O programa principal desse projeto deve:
- Ler um arquivo de entrada contendo as informações dos processos e parâmetros do sistema
- Executar os algoritmos de escalonamento, simulando a ocupação de CPU, troca de contexto e registrando os eventos.
- Gerar um arquivo de saída com os resultados utilizando cada um dos algoritmos de escalonamento:
    - o Tempo médio de retorno
    - o Linha do tempo de ocupação da CPU, indicando o processo que está ocupando a CPU em cada momento.
    - o Número de chaveamento de processos
    - o Overhead de chaveamento de processos (fração entre o tempo total gasto com os chaveamentos e o tempo total da simulação).
    - o Tempo total para executar todos os processos

A simulação deve considerar os dois algoritmos de escalonamento preemptivos a seguir:
- Round Robin com quantum fixo (fatia de tempo indicada no arquivo de entrada)
- Baseado em Prioridade

Observações sobre os algoritmos:
- Considere no algoritmo baseado em prioridade: quando menor o valor numérico da prioridade, maior é a prioridade do processo.
- Caso dois ou mais processos com mesma prioridade sejam criados ao mesmo tempo, a ordem de escalonamento deve seguir o ID do processo. Processo com menor ID é escalonado primeiro que o de maior ID.
- Similarmente, no Round Robin caso dois ou mais processos sejam criados no mesmo instante, a ordem de escalonamento deve ser a do ID do processo. Processo com menor ID é escalonado primeiro que o de maior ID.
- No Round Robin, caso um processo finalize antes de expirar a sua fatia de tempo (quantum), a troca de contexto deve acontecer logo.
- Na criação da linha do tempo de ocupação da CPU, indicar “Escalonador” quando se estiver realizando a troca de contexto.

O arquivo de entrada (em formato .txt) do programa conterá as seguintes informações.
- Na primeira linha, os valores dos parâmetros nProc, quantum e tTroca, separados por vírgula, onde:
    - nProc: é o número de processos a escalonar;
    - quantum representa o valor da fatia de tempo a ser adotada no algortimo de escalonamento Round Robin;
    - tTroca denota o tempo de chaveamento de contexto, isto é, o tempo necessário para a troca de processos na CPU.
- Em cada linha, a partir da segunda linha até a linha número nProc+1, têm-se, separados por vígula e nesta ordem:
    - o identificador do processo (ID);
    - o Tempo de chegada/criação do processo (Tch)
    - a Prioridade do processo (Prio);
    - Tempo total de CPU (Tcpu) que o processo necessita.
- As linhas subseqüentes do arquivo podem apresentar apenas as legendas dos itens descritos anteriormente.

O arquivo de saída (em formato .txt) do programa deve conter para cada algoritmo de escalonamento, pelo menos, as seguintes informações,
- Tempo de retorno
- Número de chaveamento de processos
- Overhead de chaveamento de processos (fração entre o tempo total gasto com os chaveamentos e o tempo total da simulação).
- Tempo total para executar todos os processos
- Linha do tempo de ocupação da CPU, indicando o processo que está ocupando a CPU em cada momento, do inicio ao fim da simulação.