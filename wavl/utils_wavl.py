# wavl/wavl_impl/utils_wavl.py

from typing import Optional
from node_wavl import NodeWAVL

def get_rank(node: Optional[NodeWAVL]) -> int:
    if node is None:
        return -1
    return node.rank

def rank_differences(node: Optional[NodeWAVL]) -> tuple[int, int]:

    if node is None:
        return (0, 0)
    left_rank = get_rank(node.left)
    right_rank = get_rank(node.right)
    return (node.rank - left_rank, node.rank - right_rank)

def print_tree(root: Optional[NodeWAVL], level: int = 0):

    if root is not None:
        print_tree(root.right, level + 1)
        print('    ' * level + f"({root.key}, r={root.rank})")
        print_tree(root.left, level + 1)
