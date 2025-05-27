# benchmarks/scripts/plot_benchmarks.py

import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_metric(df, mode, metric_wavl, metric_avl, metric_rbt,
                ylabel, title, output_png):
    """
    Dibuja en un mismo gráfico WAVL vs AVL vs RBT para el 'mode' dado,
    usando las columnas metric_wavl, metric_avl, metric_rbt.
    Guarda el PNG en output_png.
    """
    sub = df[df["mode"] == mode]
    xs = sub["n"].tolist()

    plt.figure(figsize=(8, 5))
    plt.plot(xs, sub[metric_wavl], marker='o', label='WAVL')
    plt.plot(xs, sub[metric_avl], marker='s', label='AVL')
    plt.plot(xs, sub[metric_rbt], marker='^', label='RBT')
    plt.xlabel('n (número de inserciones)')
    plt.ylabel(ylabel)
    plt.title(f"{title} ({mode})")
    plt.legend()
    plt.grid(True)
    os.makedirs(os.path.dirname(output_png), exist_ok=True)
    plt.savefig(output_png)
    plt.close()

if __name__ == "__main__":
    data_file = "../data/bench_wavl_avl_rbt.csv"
    df = pd.read_csv(data_file)

    # 1) Comparar número de rotaciones (WAVL vs AVL vs RBT)
    plot_metric(
        df, mode="random",
        metric_wavl="wavl_rotations",
        metric_avl="avl_rotations",
        metric_rbt="rbt_rotations",
        ylabel="Número de rotaciones",
        title="Rotaciones comparadas",
        output_png="../plots/rotations_random.png"
    )
    plot_metric(
        df, mode="sequential",
        metric_wavl="wavl_rotations",
        metric_avl="avl_rotations",
        metric_rbt="rbt_rotations",
        ylabel="Número de rotaciones",
        title="Rotaciones comparadas",
        output_png="../plots/rotations_sequential.png"
    )

    # 2) Comparar promociones (WAVL) vs recolors (RBT)
    for mode in ["random", "sequential"]:
        sub = df[df["mode"] == mode]
        xs = sub["n"].tolist()
        plt.figure(figsize=(8, 5))
        plt.plot(xs, sub["wavl_promotions"], marker='o', label='WAVL promotions')
        plt.plot(xs, sub["rbt_recolors"], marker='^', label='RBT recolors')
        plt.xlabel('n')
        plt.ylabel('Conteo de promociones/recolors')
        plt.title(f"Promotions (WAVL) vs Recolors (RBT) ({mode})")
        plt.legend()
        plt.grid(True)
        filename = f"../plots/promote_vs_recolor_{mode}.png"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        plt.savefig(filename)
        plt.close()

    # 3) Comparar altura final de cada estructura
    plot_metric(
        df, mode="random",
        metric_wavl="wavl_height",
        metric_avl="avl_height",
        metric_rbt="rbt_height",
        ylabel="Altura del árbol",
        title="Altura comparada",
        output_png="../plots/height_random.png"
    )
    plot_metric(
        df, mode="sequential",
        metric_wavl="wavl_height",
        metric_avl="avl_height",
        metric_rbt="rbt_height",
        ylabel="Altura del árbol",
        title="Altura comparada",
        output_png="../plots/height_sequential.png"
    )

    # 4) Comparar tiempo de inserción
    plot_metric(
        df, mode="random",
        metric_wavl="wavl_time",
        metric_avl="avl_time",
        metric_rbt="rbt_time",
        ylabel="Tiempo (segundos)",
        title="Tiempo de inserción",
        output_png="../plots/time_random.png"
    )
    plot_metric(
        df, mode="sequential",
        metric_wavl="wavl_time",
        metric_avl="avl_time",
        metric_rbt="rbt_time",
        ylabel="Tiempo (segundos)",
        title="Tiempo de inserción",
        output_png="../plots/time_sequential.png"
    )

    print("Gráficos generados en benchmarks/plots/")
