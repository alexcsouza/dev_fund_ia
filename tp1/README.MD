# TP1 — Problema da Ponte e da Tocha

Fundamentos de Inteligência Artificial — UFMG.

Resolve o quebra-cabeça da Ponte e da Tocha modelando-o como um problema de
busca em espaço de estados e resolvendo-o com quatro algoritmos: busca em
profundidade (DFS), busca em largura (BFS), busca de custo uniforme e A*.

## O problema

Quatro pessoas precisam atravessar uma ponte à noite. Regras:

- Só existe **uma tocha**, e toda travessia (ida ou volta) exige a tocha.
- No máximo **duas pessoas** atravessam por vez.
- Duas pessoas atravessando juntas andam na velocidade da **mais lenta**.

| Pessoa | Tempo |
|--------|-------|
| A | 1 min |
| B | 2 min |
| C | 5 min |
| D | 10 min |

Objetivo: levar todos para o outro lado no **menor tempo possível**.

## Tarefa 1 — Modelagem

Implementada em `lib/problema.py`.

- **Estado:** tripla `(origem, destino, tocha)`, onde `origem` e `destino` são
  os conjuntos de pessoas em cada lado e `tocha ∈ {origem, destino}` indica o
  lado da tocha. Guardar o lado da tocha é indispensável: sem ele, dois estados
  com a mesma divisão de pessoas seriam idênticos, mas apenas um permite
  avançar (o que tem a tocha do lado de quem vai atravessar).
- **Estado inicial:** todas as pessoas e a tocha na origem.
- **Estado objetivo:** origem vazia (todos no destino). A tocha estará no
  destino, pois o último movimento foi de ida.
- **Sucessora / ações / custos:** uma ação move uma ou duas pessoas do lado da
  tocha para o outro lado, levando a tocha junto. O custo é o tempo da pessoa
  mais lenta do grupo.

## Tarefas 2 e 3 — Algoritmos de busca

Implementados em `lib/agentes.py`. Todos usam **busca em grafo** (conjunto de
estados visitados) para não entrar em ciclo — dá para ir e voltar com a tocha
indefinidamente — e um **limite de nós expandidos** como salvaguarda contra
buscas longas (principalmente na DFS).

- **DFS** e **BFS** (não informadas) — Tarefa 2.
- **Custo Uniforme** (expande por `g(n)`, o tempo acumulado) e **A\*** (expande
  por `f(n) = g(n) + h(n)`) — Tarefa 3.

**Função de custo** `g(n)`: soma dos tempos das travessias do estado inicial
até `n`.

**Heurística** `h(n)` (em `lib/problema.py`): o maior tempo entre as pessoas
que ainda estão na origem. É **admissível** porque a pessoa mais lenta ainda na
origem terá, obrigatoriamente, de fazer ao menos uma travessia de ida, que já
custa pelo menos o tempo dela; como todos os demais custos são não negativos, o
tempo restante real nunca é menor que `h(n)`. Logo `h(n)` nunca superestima.

## Tarefa 4 — Comparação

Saída do programa (`python3 main.py`):

| Método | Custo (min) | Travessias | Nós expandidos | Ótimo? |
|--------|-------------|------------|----------------|--------|
| Profundidade (DFS) | 90 | 9 | 12 | não |
| Largura (BFS) | 19 | 5 | 25 | não |
| Custo Uniforme | 17 | 5 | 25 | sim |
| A* | 17 | 5 | 18 | sim |

(O tempo médio de processamento é medido em execução, sobre várias repetições.)

**Por que a BFS não garante o menor tempo?** A BFS expande os estados por
número de travessias, não por tempo acumulado. Ela devolve a solução com menos
movimentos, que não é necessariamente a de menor tempo — há soluções de 5
travessias com 17 e com 19 minutos, e a BFS pode retornar a de 19. Já o Custo
Uniforme e o A* expandem em ordem de `g(n)`; o primeiro estado objetivo retirado
da fronteira é, por construção, o de menor tempo, o que garante a otimalidade.
O A* expande menos nós que o Custo Uniforme porque a heurística orienta a busca
para os caminhos mais promissores, sem perder a garantia de otimalidade (a
heurística é admissível).

## Como executar

```bash
python3 main.py
```

Requer `pandas` (usado apenas para imprimir as tabelas).

## Estrutura

```
tp1/
├── main.py            # resolve com os 4 agentes e imprime a comparação
└── lib/
    ├── problema.py    # modelagem: estado, objetivo, sucessora, heurística
    ├── agentes.py     # DFS, BFS, custo uniforme e A*
    ├── search.py      # implementações genéricas de referência (não usadas)
    └── graphos.py     # utilitários de grafos de referência (não usados)
```
