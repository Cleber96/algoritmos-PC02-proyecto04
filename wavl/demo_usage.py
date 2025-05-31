#!/usr/bin/env python3
"""
demo_usage.py

Script de demostración para la clase WAVLTree. Muestra inserciones, eliminaciones
y cuenta de operaciones de rebalanceo (promociones, demociones, rotaciones).
"""

from tree_wavl import WAVLTree
from utils_wavl import print_tree

def main():
    # Demostración de inserciones
    keys_to_insert = [50, 30, 20, 40, 70, 60, 80]
    tree = WAVLTree()
    print("Insertando la secuencia:", keys_to_insert)
    for k in keys_to_insert:
        tree.insert(k)
    print("\nÁrbol después de inserciones (in-order invertido):")
    print_tree(tree.root)
    print(f"Contadores tras inserciones: promociones={{tree.promote_count}}, demociones={{tree.demote_count}}, rotaciones={{tree.rotation_count}}")

    # Demostración de eliminación
    key_to_delete = 30
    print(f"\nEliminando la clave {key_to_delete}...")
    tree.delete(key_to_delete)
    print("Árbol después de la eliminación:")
    print_tree(tree.root)
    print(f"Contadores tras eliminación: promociones={{tree.promote_count}}, demociones={{tree.demote_count}}, rotaciones={{tree.rotation_count}}")

if __name__ == "__main__":
    main()
