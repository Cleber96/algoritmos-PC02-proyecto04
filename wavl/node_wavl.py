# wavl/wavl_impl/node_wavl.py

from typing import Optional

class NodeWAVL:
    """
    Nodo para Weak AVL Tree (WAVL).
    Atributos:
        key    : clave o valor almacenado en el nodo.
        left   : referencia al hijo izquierdo (NodeWAVL o None).
        right  : referencia al hijo derecho (NodeWAVL o None).
        parent : referencia al padre (NodeWAVL o None).
        rank   : entero ≥ 0 que indica el “rank” de este nodo.
    """
    def __init__(self, key):
        self.key: int = key
        self.left: Optional[NodeWAVL] = None
        self.right: Optional[NodeWAVL] = None
        self.parent: Optional[NodeWAVL] = None
        self.rank: int = 0  # Al crear el nodo, asumimos rank = 0

    def __repr__(self):
        left_k = self.left.key if self.left else None
        right_k = self.right.key if self.right else None
        return (f"NodeWAVL(key={self.key}, rank={self.rank}, "
                f"left={left_k}, right={right_k})")
