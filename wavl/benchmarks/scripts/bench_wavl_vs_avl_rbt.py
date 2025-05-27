# benchmarks/scripts/bench_wavl_vs_avl_rbt.py

import random
import time
import csv
import os
from tree_wavl import WAVLTree
from wavl.avl import AVLTree
from wavl.rbt import RBTree  # Supongamos que tienes tu propia implementación de RBT

def measure_height(root):
    """
    Calcula la altura máxima (profundidad) de un árbol recursivamente.
    Definimos altura de nodo None = -1; nodo interno = 1 + max(altura(hijos)).
    """
    if root is None:
        return -1
    return 1 + max(measure_height(root.left), measure_height(root.right))


def benchmark_structures(n, mode="random"):
    """
    Ejecuta un único experimento para tamaño n y modo dado ("random" o "sequential").
    Devuelve un diccionario con métricas para WAVL, AVL y RBT.
    """
    # 1) Generar lista de claves según el modo
    if mode == "random":
        keys = random.sample(range(1, n * 10 + 1), n)
    else:  # "sequential"
        keys = list(range(1, n + 1))

    # --- WAVL ---
    wavl = WAVLTree()
    # Reiniciar contadores
    wavl.promote_count = 0
    wavl.demote_count = 0
    wavl.rotation_count = 0

    start = time.time()
    for key in keys:
        wavl.insert(key)
    insert_time_wavl = time.time() - start

    # Altura final WAVL
    height_wavl = measure_height(wavl.root)
    w_prom = wavl.promote_count
    w_dem = wavl.demote_count
    w_rot = wavl.rotation_count

    # --- AVL ---
    avl = AVLTree()
    avl.rotation_count = 0

    start = time.time()
    for key in keys:
        avl.insert(key)
    insert_time_avl = time.time() - start

    height_avl = measure_height(avl.root)
    a_rot = avl.rotation_count

    # --- RBT ---
    rbt = RBTree()  # Implementación propia de RBT
    rbt.rotation_count = 0
    rbt.recolor_count = 0

    start = time.time()
    for key in keys:
        rbt.insert(key)
    insert_time_rbt = time.time() - start

    height_rbt = measure_height(rbt.root)
    r_rot = rbt.rotation_count
    r_col = rbt.recolor_count

    return {
        "n": n,
        "mode": mode,
        # WAVL métricas
        "wavl_promotions": w_prom,
        "wavl_demotions": w_dem,
        "wavl_rotations": w_rot,
        "wavl_height": height_wavl,
        "wavl_time": insert_time_wavl,
        # AVL métricas
        "avl_rotations": a_rot,
        "avl_height": height_avl,
        "avl_time": insert_time_avl,
        # RBT métricas
        "rbt_rotations": r_rot,
        "rbt_recolors": r_col,
        "rbt_height": height_rbt,
        "rbt_time": insert_time_rbt
    }


def run_benchmarks(sizes, modes, output_csv):
    """
    Para cada tamaño en 'sizes' y cada modo en 'modes':
      - Ejecuta benchmark_structures(n, mode)
      - Acumula resultados y los escribe en 'output_csv'
    """
    results = []

    for mode in modes:
        for n in sizes:
            print(f"Corriendo n={n}, mode={mode}...")
            data = benchmark_structures(n, mode)
            results.append(data)

    # Guardar en CSV
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, mode='w', newline='') as f:
        fieldnames = list(results[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Resultados guardados en {output_csv}")


if __name__ == "__main__":
    # Definir tamaños de prueba
    sizes = [1000, 5000, 10000, 20000]
    # Modos: "random" y "sequential"
    modes = ["random", "sequential"]
    output_file = "../data/bench_wavl_avl_rbt.csv"
    run_benchmarks(sizes, modes, output_file)
