# wavl/wavl_impl/node_wavl.py

from typing import Optional

class NodeWAVL:
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
