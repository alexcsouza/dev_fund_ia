"""
Comparacao de eficiencia: versoes eficientes x versoes ingenuas.

Mostra, para o mesmo problema da Ponte e da Tocha, quanto as otimizacoes das
buscas de `lib/agentes.py` reduzem o numero de nos expandidos e o tempo de
processamento em relacao as variantes menos eficientes de
`lib/agentes_ingenuos.py`.

O par comparado em cada linha resolve o problema com a MESMA estrategia; a
unica diferenca e a otimizacao:
- BFS/DFS: busca em grafo (com visitados) x busca em arvore (sem visitados);
- A*: com heuristica admissivel x com heuristica nula (h = 0).
"""

import time

import pandas as pd

from lib.agentes import busca_largura, busca_profundidade, busca_a_estrela
from lib.agentes_ingenuos import (
    busca_largura_arvore,
    busca_profundidade_arvore,
    busca_a_estrela_sem_heuristica,
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
        ('A*', busca_a_estrela, busca_a_estrela_sem_heuristica),
    ]

    print('=' * 72)
    print('COMPARACAO DE EFICIENCIA: versao eficiente x versao ingenua')
    print('=' * 72)

    linhas = []
    for rotulo, eficiente, ingenua in pares:
        r_ef = eficiente()
        r_in = ingenua()
        fator = (r_in.nos_expandidos / r_ef.nos_expandidos) if r_ef.nos_expandidos else float('inf')
        linhas.append({
            'Estrategia': rotulo,
            'Nos (eficiente)': r_ef.nos_expandidos,
            'Nos (ingenua)': r_in.nos_expandidos,
            'Fator': round(fator, 1),
            'ms (eficiente)': round(tempo_medio(eficiente), 4),
            'ms (ingenua)': round(tempo_medio(ingenua), 4),
        })

    tabela = pd.DataFrame(linhas)
    print('\n' + tabela.to_string(index=False))

    print('\nObservacoes:')
    print('- BFS e DFS: sem o conjunto de visitados a busca vira busca em arvore e')
    print('  reexpande os mesmos estados varias vezes, disparando o numero de nos.')
    print('- A*: com heuristica nula (h = 0) ela degenera em custo uniforme e perde')
    print('  a orientacao, expandindo mais nos que a versao com heuristica admissivel.')
    print('- Todas as variantes ainda encontram uma solucao valida: a diferenca esta')
    print('  no custo computacional, nao na corretude.')


if __name__ == '__main__':
    main()
