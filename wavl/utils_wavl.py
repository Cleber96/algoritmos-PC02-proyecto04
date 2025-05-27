# wavl/wavl_impl/utils_wavl.py

from typing import Optional
from node_wavl import NodeWAVL

def get_rank(node: Optional[NodeWAVL]) -> int:
    """
    Devuelve el rank de un nodo WAVL.
    Si node es None (hoja externa), retornamos -1.
    """
    if node is None:
        return -1
    return node.rank

def rank_differences(node: Optional[NodeWAVL]) -> tuple[int, int]:
    """
    Retorna la tupla de diferencias de rango de 'node' con sus hijos:
      (r(node) - r(node.left),  r(node) - r(node.right))
    Si node es None, retornamos (0,0).
    """
    if node is None:
        return (0, 0)
    left_rank = get_rank(node.left)
    right_rank = get_rank(node.right)
    return (node.rank - left_rank, node.rank - right_rank)

def print_tree(root: Optional[NodeWAVL], level: int = 0):
    """
    Imprime el árbol en in-order invertido (derecha → nodo → izquierda),
    mostrando (key, rank) con indentación según el nivel.
    Útil para visualizar la estructura: 
        (clave, r) 
        subárbol derecho
    """
    if root is not None:
        print_tree(root.right, level + 1)
        print('    ' * level + f"({root.key}, r={root.rank})")
        print_tree(root.left, level + 1)
