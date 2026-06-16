# Trabalho 2 - Sistemas Operacionais

## Integrantes

- João Araujo
- Lucas Afonso
- Arthur Ferreira
- Matheus Corbellini
- Rafaela
- Vinicius

## Algoritmos Implementados

- **LRU (Least Recently Used)** — substitui a página que foi acessada há mais tempo.
- **OPT (Ótimo / Belady)** — substitui a página que será usada mais tarde no futuro (ou que não será mais usada).

## Descrição

### Introdução

Este trabalho tem como objetivo simular dois algoritmos clássicos de substituição de páginas em memória virtual: o **LRU** e o **OPT**. A partir de uma sequência de acessos a páginas, cada simulador mostra como a memória física (frames) se comporta, contabilizando _hits_ e _page faults_.

### Desenvolvimento

Os simuladores foram implementados em Python, usando classes para representar os `Frames`, a `TabelaPaginas` e o `Simulador`. A entrada é lida de um arquivo de texto, onde a primeira linha indica o número de frames disponíveis e as linhas seguintes representam a sequência de páginas acessadas. A cada passo, o programa imprime o estado atual da memória, indicando se houve _hit_ ou _page fault_ e qual frame foi alterado. Ao final, são exibidas estatísticas com o total de acessos, page faults e a taxa de faltas.

### Conclusão

A comparação entre os dois algoritmos evidencia o limite teórico do **OPT** (que serve como referência ótima, mas não é implementável na prática) e o desempenho realista do **LRU**, que é uma aproximação viável e amplamente usada em sistemas reais.

## Como Testar

1. Tenha o **Python 3** instalado.
2. Edite o arquivo `entrada.txt` com a configuração desejada:
   - Primeira linha: número de frames.
   - Demais linhas: sequência de páginas acessadas (uma por linha).
3. Execute um dos simuladores no terminal:

```bash
python simulador_lru.py
python simulador_opt.py
```
