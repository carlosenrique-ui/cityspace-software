# runner/path.py

from typing import List, Tuple


def zigzag_scan(rows: int, cols: int) -> List[Tuple[int, int]]:
    """
    Gera uma ordem de varredura zig-zag (boustrophedon).

    Retorna uma lista de (row, col).

    Linha 0: esquerda -> direita
    Linha 1: direita -> esquerda
    Linha 2: esquerda -> direita
    ...
    """

    order: List[Tuple[int, int]] = []

    for row in range(rows):
        if row % 2 == 0:
            cols_iter = range(cols)
        else:
            cols_iter = reversed(range(cols))

        for col in cols_iter:
            order.append((row, col))

    return order
