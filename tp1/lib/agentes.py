"""
Soluções de busca para o desafio da Ponte e da Tocha.

Dividimos a abordagem em dois grupos principais:
- Tarefa 2: Algoritmos não informados (Profundidade e Largura).
- Tarefa 3: Algoritmos informados e baseados em custo (Custo Uniforme e A*).

Para evitar que a execução entre em um vai e vem infinito com a tocha, usamos
uma estratégia de busca em grafo para guardar o histórico dos estados já visitados.
Também definimos um limite para o total de nós expandidos — uma trava de segurança
essencial para impedir que a busca em profundidade rode indefinidamente.

Cada método gera um objeto `Resultado`, trazendo o caminho percorrido, o custo 
(tempo final de travessia), o total de nós visitados e o tempo de execução.
"""
import heapq
import itertools
import time
from collections import deque

from lib.problema import estado_inicial, eh_objetivo, sucessores
from lib.agentes import Resultado, _custo_do_caminho, LIMITE_EXPANSOES


LIMITE_PROFUNDIDADE = 15


def busca_largura_arvore(limite=LIMITE_EXPANSOES):
    inicio = estado_inicial()
    fila = deque([(inicio, [])])
    expandidos = 0
    t0 = time.perf_counter()

    while fila:
        estado, caminho = fila.popleft()
        if eh_objetivo(estado):
            return Resultado('Largura (BFS) - arvore', caminho, _custo_do_caminho(caminho),
                             expandidos, time.perf_counter() - t0, True)
        expandidos += 1
        if expandidos >= limite:
            break
        for proximo, acao, _ in sucessores(estado):
            fila.append((proximo, caminho + [acao]))

    return Resultado('Largura (BFS) - arvore', [], float('inf'), expandidos,
                     time.perf_counter() - t0, False)


def busca_profundidade_arvore(limite_profundidade=LIMITE_PROFUNDIDADE, limite=LIMITE_EXPANSOES):
    inicio = estado_inicial()
    pilha = [(inicio, [])]
    expandidos = 0
    t0 = time.perf_counter()

    while pilha:
        estado, caminho = pilha.pop()
        if eh_objetivo(estado):
            return Resultado('Profundidade (DFS) - arvore', caminho, _custo_do_caminho(caminho),
                             expandidos, time.perf_counter() - t0, True)
        if len(caminho) >= limite_profundidade:
            continue
        expandidos += 1
        if expandidos >= limite:
            break
        for proximo, acao, _ in sucessores(estado):
            pilha.append((proximo, caminho + [acao]))

    return Resultado('Profundidade (DFS) - arvore', [], float('inf'), expandidos,
                     time.perf_counter() - t0, False)


def busca_a_estrela(limite=LIMITE_EXPANSOES):
    inicio = estado_inicial()
    contador = itertools.count()
    fronteira = [(0, 0, next(contador), inicio, [])]
    melhor_g = {inicio: 0}
    expandidos = 0
    t0 = time.perf_counter()

    while fronteira:
        _, g, _, estado, caminho = heapq.heappop(fronteira)
        if eh_objetivo(estado):
            return Resultado('A* (h = 0)', caminho, g, expandidos,
                             time.perf_counter() - t0, True)
        if g > melhor_g.get(estado, float('inf')):
            continue
        expandidos += 1
        if expandidos >= limite:
            break
        for proximo, acao, custo in sucessores(estado):
            novo_g = g + custo
            if novo_g < melhor_g.get(proximo, float('inf')):
                melhor_g[proximo] = novo_g
                f = novo_g + 0  # heuristica nula
                heapq.heappush(fronteira, (f, novo_g, next(contador), proximo, caminho + [acao]))

    return Resultado('A* (h = 0)', [], float('inf'), expandidos,
                     time.perf_counter() - t0, False)
