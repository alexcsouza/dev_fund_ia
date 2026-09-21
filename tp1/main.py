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

from lib.problema import PESSOAS, estado_inicial
from lib.agentes import (
    busca_profundidade,
    busca_largura,
    busca_custo_uniforme,
    busca_a_estrela,
)

REPETICOES = 200  # execucoes por algoritmo para o tempo medio de processamento


def descreve_acao(acao):
    grupo, direcao = acao
    seta = '-->' if direcao == 'ida' else '<--'
    return f'{seta} {" e ".join(grupo)}'


def mostra_solucao(resultado):
    print(f'\n{"-" * 60}')
    print(f'{resultado.nome}')
    print(f'{"-" * 60}')

    if not resultado.sucesso:
        print('Nenhuma solucao encontrada dentro do limite de expansoes.')
        return

    origem, destino, _ = estado_inicial()
    acumulado = 0
    for i, acao in enumerate(resultado.caminho, start=1):
        grupo, direcao = acao
        movidos = frozenset(grupo)
        custo = max(PESSOAS[p] for p in grupo)
        acumulado += custo
        if direcao == 'ida':
            origem, destino = origem - movidos, destino | movidos
        else:
            origem, destino = origem | movidos, destino - movidos
        print(f'  {i}. {descreve_acao(acao):<12} (+{custo:>2} min | acumulado {acumulado:>2} min)  '
              f'origem={sorted(origem)}  destino={sorted(destino)}')

    print(f'\n  Tempo total da travessia: {resultado.custo} min | '
          f'travessias: {len(resultado.caminho)} | nos expandidos: {resultado.nos_expandidos}')


def tempo_medio(funcao, repeticoes=REPETICOES):
    """Roda a busca varias vezes e devolve o tempo medio de processamento (ms)."""
    total = 0.0
    for _ in range(repeticoes):
        t0 = time.perf_counter()
        funcao()
        total += time.perf_counter() - t0
    return (total / repeticoes) * 1000


def main():
    print('=' * 60)
    print('PROBLEMA DA PONTE E DA TOCHA')
    print('=' * 60)
    print('Tempos: ' + ', '.join(f'{p}={t}min' for p, t in PESSOAS.items()))

    agentes = [busca_profundidade, busca_largura, busca_custo_uniforme, busca_a_estrela]
    resultados = [agente() for agente in agentes]

    for resultado in resultados:
        mostra_solucao(resultado)

    # Tarefa 4: comparacao dos quatro metodos.
    print(f'\n{"=" * 60}')
    print('COMPARACAO DOS METODOS')
    print('=' * 60)

    linhas = []
    for agente, resultado in zip(agentes, resultados):
        linhas.append({
            'Metodo': resultado.nome,
            'Custo (min)': resultado.custo if resultado.sucesso else '-',
            'Travessias': len(resultado.caminho) if resultado.sucesso else '-',
            'Nos expandidos': resultado.nos_expandidos,
            'Tempo medio (ms)': round(tempo_medio(agente), 4),
            'Otimo?': 'sim' if resultado.sucesso and resultado.custo == 17 else 'nao',
        })

    tabela = pd.DataFrame(linhas)
    print('\n' + tabela.to_string(index=False))

    print('\nObservacoes:')
    print('- Custo Uniforme e A* encontram o otimo (17 min) porque expandem os')
    print('  estados em ordem de custo acumulado g(n); o primeiro objetivo')
    print('  retirado da fronteira e, por construcao, o de menor tempo.')
    print('- A BFS expande por numero de travessias, nao por tempo. Ela devolve')
    print('  a solucao com menos movimentos, que nao e necessariamente a de menor')
    print('  tempo - existem solucoes de 5 travessias com 17 e com 19 minutos.')
    print('- A DFS apenas encontra alguma solucao valida, em geral pior em tempo.')
    print('- A* expande menos nos que o Custo Uniforme por usar a heuristica para')
    print('  priorizar caminhos promissores, mantendo a garantia de otimalidade')
    print('  por ser a heuristica admissivel.')


if __name__ == '__main__':
    main()
