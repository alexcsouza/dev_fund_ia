"""
Modelagem do problema da Ponte e da Tocha.

Estrutura do estado: (origem, destino, tocha)
- origem/destino: frozenset com as pessoas de cada lado.
- tocha: 'origem' ou 'destino'.

A tocha no estado é essencial: dois estados com a mesma divisão de pessoas 
são bem diferentes dependendo de quem está com a luz.

Objetivo: esvaziar a origem (a tocha termina do outro lado naturalmente).
Ações: mover 1 ou 2 pessoas pro lado oposto. O tempo do passo é o da pessoa mais lenta.
"""
import itertools

# Tempo de travessia (em minutos)
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
    """Gera os próximos estados válidos, a ação tomada e o tempo gasto."""
    origem, destino, tocha = estado
    lado_da_tocha = origem if tocha == 'origem' else destino

    # Pode ir/voltar 1 pessoa sozinha ou em dupla
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
    """Retorna o tempo da pessoa mais lenta na origem (0 se todos cruzaram).

    É admissível porque essa pessoa obrigatoriamente fará pelo menos mais 
    uma travessia, então o custo real nunca será menor que o tempo dela.
    """
    origem, _, _ = estado
    if not origem:
        return 0
    return max(PESSOAS[p] for p in origem)