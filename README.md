# Colonia de Formigas
## Trabalho Algoritmo Bioinspirados

## Instalação
#### pip install -r requirements.txt
## Execução
#### python3 main.py -h (vizualizar parametros necessários)
#### python3 main.py -f <instancias/lau15_dist.txt> -t <ADJM> -s <valor_melhor_solucao (não é obrigatório)> (exemplo de execução)
#### python3 main.py -f <instancias/berlin52.tsp> -t <EUC2D> -s <valor_melhor_solucao (não é obrigatório)> (exemplo de execução)

## Execução dos testes fatoriais
#### python3 parallel_exec.py -h (vizualizar parametros necessários)
#### python3 parallel_exec.py -f instancias/lau15_dist.txt -t ADJM -s <valor_melhor_solucao (não é obrigatório)> (exemplo de execução)
#### python3 parallel_exec.py -f instancias/berlin52.tsp -t EUC2D -s <valor_melhor_solucao (não é obrigatório)> (exemplo de execução)

## Plot dos resultado do teste fatorial
#### python3 plot_charts.py -f resultados/results_lau15_dist.txt.pickle (exemplo de execução)