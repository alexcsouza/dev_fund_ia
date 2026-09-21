"""
Versoes propositalmente MENOS EFICIENTES dos agentes de busca.

Estas variantes existem apenas para comparacao didatica com as versoes de
`lib/agentes.py`. Cada uma resolve o mesmo problema e chega a uma solucao
valida, mas abre mao de uma otimizacao:

- as buscas nao informadas fazem busca em ARVORE (sem conjunto de visitados),
  entao revisitam estados e expandem muito mais nos;
- a A* aqui usa heuristica nula (h = 0), o que a faz degenerar em custo
  uniforme e perder a orientacao da heuristica.

Nao devem ser usadas como solucao final - servem so para evidenciar, no numero
de nos expandidos e no tempo, o impacto das otimizacoes das versoes eficientes.
"""

import heapq
import itertools
import time
from collections import deque

from lib.problema import estado_inicial, eh_objetivo, sucessores
from lib.agentes import Resultado, _custo_do_caminho, LIMITE_EXPANSOES

# Sem conjunto de visitados, a DFS em arvore poderia descer para sempre indo e
# voltando com a tocha; limitamos a profundidade para garantir o termino.
LIMITE_PROFUNDIDADE = 15


def busca_largura_arvore(limite=LIMITE_EXPANSOES):
    """BFS sem conjunto de visitados (busca em arvore)."""
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
    """DFS sem conjunto de visitados (busca em arvore) e com limite de profundidade."""
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


def busca_a_estrela_sem_heuristica(limite=LIMITE_EXPANSOES):
    """A* com heuristica nula (h = 0), que a reduz ao custo uniforme."""
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
