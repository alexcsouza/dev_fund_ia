"""
Modelagem do problema da Ponte e da Tocha como busca em espaco de estados.

Tarefa 1 do TP.

--------------------------------------------------------------------------
Representacao de estado
--------------------------------------------------------------------------
Um estado e a tripla (origem, destino, tocha), onde:

    origem  : frozenset com as pessoas que ainda estao no lado inicial;
    destino : frozenset com as pessoas que ja atravessaram;
    tocha   : lado onde a tocha se encontra ('origem' ou 'destino').

Guardar o lado da tocha e essencial: sem essa informacao dois estados com a
mesma divisao de pessoas seriam confundidos, mas so um deles permite avancar.

--------------------------------------------------------------------------
Estado inicial e objetivo
--------------------------------------------------------------------------
Inicial : todas as pessoas e a tocha no lado de origem.
Objetivo: nenhuma pessoa na origem (todas no destino). Nesse ponto a tocha
          necessariamente esta no destino, pois o ultimo movimento foi de ida.

--------------------------------------------------------------------------
Acoes, transicoes e custos
--------------------------------------------------------------------------
Uma acao move uma ou duas pessoas do lado onde a tocha esta para o outro lado,
levando a tocha junto. O custo da acao e o tempo da pessoa mais lenta do grupo
(duas pessoas andam na velocidade da mais lenta).
"""

import itertools

# Tempo de travessia de cada pessoa, em minutos.
PESSOAS = {
    'A': 1,
    'B': 2,
    'C': 5,
    'D': 10,
}


def estado_inicial():
    return (frozenset(PESSOAS), frozenset(), 'origem')


def eh_objetivo(estado):
    origem, _, _ = estado
    return len(origem) == 0


def sucessores(estado):
    """Gera os estados alcancaveis a partir de `estado`.

    Retorna tuplas (proximo_estado, acao, custo), onde `acao` e o par
    (grupo, direcao) e `custo` e o tempo da travessia.
    """
    origem, destino, tocha = estado
    lado_da_tocha = origem if tocha == 'origem' else destino

    # Movimentos possiveis: uma pessoa sozinha ou qualquer par de pessoas.
    pessoas_ordenadas = sorted(lado_da_tocha, key=lambda p: PESSOAS[p])
    grupos = [(p,) for p in pessoas_ordenadas]
    grupos += list(itertools.combinations(pessoas_ordenadas, 2))

    for grupo in grupos:
        custo = max(PESSOAS[p] for p in grupo)
        movidos = frozenset(grupo)
        if tocha == 'origem':
            proximo = (origem - movidos, destino | movidos, 'destino')
            direcao = 'ida'
        else:
            proximo = (origem | movidos, destino - movidos, 'origem')
            direcao = 'volta'
        yield proximo, (grupo, direcao), custo


def heuristica(estado):
    """Heuristica admissivel h(n) para a busca A*.

    Retorna o maior tempo entre as pessoas que ainda estao na origem (0 quando
    todas ja atravessaram).

    Por que e admissivel (nunca superestima):
    a pessoa mais lenta que ainda esta na origem tera, obrigatoriamente, de
    fazer pelo menos uma travessia de ida em algum momento. Essa travessia,
    sozinha, ja custa o tempo dela (se for acompanhada, o custo e o do par, que
    e ainda maior). Como todos os demais custos ate o objetivo sao nao
    negativos, o tempo restante real e sempre >= esse valor. Logo a heuristica
    nunca ultrapassa o custo real ate o objetivo.
    """
    origem, _, _ = estado
    if not origem:
        return 0
    return max(PESSOAS[p] for p in origem)
