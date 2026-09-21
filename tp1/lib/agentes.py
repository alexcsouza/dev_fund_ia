"""
Agentes de busca para o problema da Ponte e da Tocha.

Tarefa 2 (busca nao informada): profundidade e largura.
Tarefa 3 (busca informada e de custo): custo uniforme e A*.

Todas as buscas usam busca em grafo (mantem um conjunto de estados ja
visitados) para nao ficar presa nos ciclos do problema - e possivel ir e voltar
com a tocha indefinidamente. Como salvaguarda extra, ha um limite maximo de nos
expandidos: se ele for atingido a busca para sem solucao, o que evita execucoes
excessivamente longas (principalmente na busca em profundidade).

Cada busca devolve um `Resultado` com o caminho encontrado, o custo total
(tempo de travessia), o numero de nos expandidos e o tempo de processamento.
"""

import heapq
import itertools
import time
from collections import deque
from dataclasses import dataclass, field
from typing import List, Tuple

from lib.problema import estado_inicial, eh_objetivo, sucessores, heuristica

LIMITE_EXPANSOES = 100_000


@dataclass
class Resultado:
    nome: str
    caminho: List[Tuple] = field(default_factory=list)  # lista de acoes (grupo, direcao)
    custo: float = float('inf')
    nos_expandidos: int = 0
    tempo_s: float = 0.0
    sucesso: bool = False


def _custo_do_caminho(caminho):
    """Recalcula o tempo total de uma lista de acoes."""
    from lib.problema import PESSOAS
    return sum(max(PESSOAS[p] for p in grupo) for grupo, _ in caminho)


def busca_profundidade(limite=LIMITE_EXPANSOES):
    inicio = estado_inicial()
    pilha = [(inicio, [])]
    visitados = set()
    expandidos = 0
    t0 = time.perf_counter()

    while pilha:
        estado, caminho = pilha.pop()
        if eh_objetivo(estado):
            return Resultado('Profundidade (DFS)', caminho, _custo_do_caminho(caminho),
                             expandidos, time.perf_counter() - t0, True)
        if estado in visitados:
            continue
        visitados.add(estado)
        expandidos += 1
        if expandidos >= limite:
            break
        for proximo, acao, _ in sucessores(estado):
            if proximo not in visitados:
                pilha.append((proximo, caminho + [acao]))

    return Resultado('Profundidade (DFS)', [], float('inf'), expandidos,
                     time.perf_counter() - t0, False)


def busca_largura(limite=LIMITE_EXPANSOES):
    inicio = estado_inicial()
    fila = deque([(inicio, [])])
    visitados = {inicio}
    expandidos = 0
    t0 = time.perf_counter()

    while fila:
        estado, caminho = fila.popleft()
        if eh_objetivo(estado):
            return Resultado('Largura (BFS)', caminho, _custo_do_caminho(caminho),
                             expandidos, time.perf_counter() - t0, True)
        expandidos += 1
        if expandidos >= limite:
            break
        for proximo, acao, _ in sucessores(estado):
            if proximo not in visitados:
                visitados.add(proximo)
                fila.append((proximo, caminho + [acao]))

    return Resultado('Largura (BFS)', [], float('inf'), expandidos,
                     time.perf_counter() - t0, False)


def busca_custo_uniforme(limite=LIMITE_EXPANSOES):
    inicio = estado_inicial()
    contador = itertools.count()  # desempate estavel na fila de prioridade
    fronteira = [(0, next(contador), inicio, [])]
    melhor_g = {inicio: 0}
    expandidos = 0
    t0 = time.perf_counter()

    while fronteira:
        g, _, estado, caminho = heapq.heappop(fronteira)
        if eh_objetivo(estado):
            return Resultado('Custo Uniforme', caminho, g, expandidos,
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
                heapq.heappush(fronteira, (novo_g, next(contador), proximo, caminho + [acao]))

    return Resultado('Custo Uniforme', [], float('inf'), expandidos,
                     time.perf_counter() - t0, False)


def busca_a_estrela(limite=LIMITE_EXPANSOES):
    inicio = estado_inicial()
    contador = itertools.count()
    fronteira = [(heuristica(inicio), 0, next(contador), inicio, [])]
    melhor_g = {inicio: 0}
    expandidos = 0
    t0 = time.perf_counter()

    while fronteira:
        _, g, _, estado, caminho = heapq.heappop(fronteira)
        if eh_objetivo(estado):
            return Resultado('A*', caminho, g, expandidos,
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
                f = novo_g + heuristica(proximo)
                heapq.heappush(fronteira, (f, novo_g, next(contador), proximo, caminho + [acao]))

    return Resultado('A*', [], float('inf'), expandidos,
                     time.perf_counter() - t0, False)


AGENTES = {
    'dfs': busca_profundidade,
    'bfs': busca_largura,
    'ucs': busca_custo_uniforme,
    'a*': busca_a_estrela,
}
