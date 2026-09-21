"""
TP1 - Problema da Ponte e da Tocha.

Quatro pessoas (A, B, C e D) precisam atravessar uma ponte a noite. A ponte so
suporta duas pessoas por vez e toda travessia exige a tocha, entao alguem
precisa voltar com ela. Duas pessoas atravessando juntas andam na velocidade da
mais lenta.

    A = 1 min    B = 2 min    C = 5 min    D = 10 min

O objetivo e levar todos para o outro lado no menor tempo possivel. O programa
resolve o quebra-cabeca com quatro algoritmos de busca (profundidade, largura,
custo uniforme e A*) e compara os resultados.
"""

import time

import pandas as pd

from lib.agentes import busca_largura, busca_profundidade, busca_a_estrela
from lib.agentes import (
    busca_largura_arvore,
    busca_profundidade_arvore,
    busca_a_estrela,
)

REPETICOES = 50


def tempo_medio(funcao, repeticoes=REPETICOES):
    total = 0.0
    for _ in range(repeticoes):
        t0 = time.perf_counter()
        funcao()
        total += time.perf_counter() - t0
    return (total / repeticoes) * 1000


def main():
    pares = [
        ('BFS', busca_largura, busca_largura_arvore),
        ('DFS', busca_profundidade, busca_profundidade_arvore),
        ('A*', busca_a_estrela, busca_a_estrela),
    ]



    linhas = []
    for rotulo, eficiente in pares:
        r_ef = eficiente()
        linhas.append({
            'Estrategia': rotulo,
            'Nos (eficiente)': r_ef.nos_expandidos,
            'ms (eficiente)': round(tempo_medio(eficiente), 4),
        })

    tabela = pd.DataFrame(linhas)
    print('\n' + tabela.to_string(index=False))


if __name__ == '__main__':
    main()
