from tree_wavl import WAVLTree
from utils_wavl import print_tree, rank_differences

tree = WAVLTree()
for key in [30, 20, 10]:
    tree.insert(key)
print("\nARBOL")
print_tree(tree.root)

print("\nbuscar nodo 20")
print(tree.search(20))

print("\neliminar nodo 20")
tree.delete(20)
print_tree(tree.root)