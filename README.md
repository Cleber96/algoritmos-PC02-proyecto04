# algoritmos-PC02-proyecto04
# Implementación de WAVL Trees

## Descripción del proyecto
Este proyecto implementa un **Weak AVL Tree (WAVL)** en Python, junto con análisis empírico comparativo frente a árboles AVL y Árboles Rojo-Negro (RBT). Un WAVL tree es una variante de árbol binario de búsqueda auto-balanceable que utiliza **rangos** en lugar de alturas estrictas (AVL) o colores (RBT). Las invariantes de rango garantizan una altura O(log n) y suelen requerir menos ajustes en promedio que otras variantes.

## Motivación
Los WAVL trees ofrecen una implementación conceptualmente más sencilla de las reglas de rebalanceo que los RBT tradicionales, manteniendo propiedades de eficiencia. Este proyecto permite:
- Comprender en detalle las invariantes de rango y sus reglas de promoción/democión.
- Comparar empíricamente el número de rotaciones/promociones frente a alternativas.
- Proveer una base modular para extender con operaciones avanzadas (join/split).

---

## Estructura de directorios
```text
├── wavl/                            # Código fuente principal
│   ├── node_wavl.py                 # Definición de NodeWAVL (clave, rango, punteros)
│   ├── utils_wavl.py                # Funciones auxiliares: print_tree, rank_differences
│   ├── tree_wavl.py                 # Clase WAVLTree con métodos insert, delete, search
│   ├── pruebando.py                 # Script de prueba rápida de funciones principales
│   ├── avl.py                       # Implementación de árbol AVL para comparación
│   ├── rbt.py                       # Implementación de Árbol Rojo-Negro para comparación
│   ├── benchmarks/                  # Scripts y resultados de benchmarks
│   │   ├── scripts/                 
│   │   │   ├── bench_wavl_vs_avl_rbt.py
│   │   │   └── plot_benchmarks.py
│   │   ├── data/                    # Archivos CSV con resultados de benchmarks
│   │   └── plots/                   # Gráficos generados (PNG)
│   └── __init__.py
├── tests/                           # Pruebas unitarias (pytest/unittest)
│   ├── test_insert.py
│   ├── test_delete.py
│   └── test_search.py
├── demo_usage.py                    # Script de demostración de uso del WAVL tree
├── informe_tecnico.pdf              # Informe técnico en PDF (3–5 páginas)
└── README.md                        # Este archivo
```

---

## Requisitos de software
- Python 3.10 o superior.
- [Opcional] `pytest` (si se quieren ejecutar pruebas con pytest).

_Ninguna dependencia externa adicional es necesaria
---

## Instalación y ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

2. **Configuración de entorno (opcional):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias (solo ReportLab si se modifica el informe):**
   ```bash
   pip install reportlab pytest
   ```

4. **Ejecutar la demostración de uso:**
   ```bash
   python3 demo_usage.py
   ```

5. **Ejecutar pruebas unitarias (opcional):**
   - Con `pytest`:
     ```bash
     pytest tests/
     ```
   - Con `unittest`:
     ```bash
     python3 -m unittest discover tests
     ```

6. **Generar benchmarks y gráficos:**
   ```bash
   # Ejecutar benchmarks y guardar resultados en CSV
   python3 wavl/benchmarks/scripts/bench_wavl_vs_avl_rbt.py --output wavl/benchmarks/data/bench_wavl_avl_rbt.csv

   # Generar gráficos a partir del CSV
   python3 wavl/benchmarks/scripts/plot_benchmarks.py --input wavl/benchmarks/data/bench_wavl_avl_rbt.csv --output wavl/benchmarks/plots/
   ```

---

## Uso de la API
La clase principal es `WAVLTree`, ubicada en `wavl/tree_wavl.py`.

```python
from wavl.tree_wavl import WAVLTree
from wavl.utils_wavl import print_tree

# Crear árbol WAVL
tree = WAVLTree()

# Insertar claves
for key in [50, 30, 20, 40, 70]:
    tree.insert(key)

# Imprimir árbol en consola (in-order invertido)
print_tree(tree.root)

# Buscar nodo
node = tree.search(30)
if node:
    print(f"Nodo encontrado: key={node.key}, rank={node.rank}")
else:
    print("Nodo no encontrado")

# Eliminar clave
tree.delete(30)

# Acceder a contadores internos de benchmarking
print(f"Promociones: {tree.promote_count}")
print(f"Demociones: {tree.demote_count}")
print(f"Rotaciones: {tree.rotation_count}")
```

### Métodos principales de `WAVLTree`
- `insert(key: int) -> None`: Inserta una clave en el árbol, ajustando rangos y rotaciones.
- `delete(key: int) -> None`: Elimina una clave si existe, rebalanceando el árbol.
- `search(key: int) -> Optional[NodeWAVL]`: Busca una clave y devuelve el nodo o `None`.
- Atributos:
  - `promote_count`: Número total de promociones de rango realizadas.
  - `demote_count`: Número total de demociones de rango realizadas.
  - `rotation_count`: Número total de rotaciones ejecutadas.

---

## Pruebas unitarias
Las pruebas se encuentran en la carpeta `tests/`. Para ejecutarlas:
```bash
pytest tests/
# o
python3 -m unittest discover tests
```

Los archivos de prueba incluyen:
- `test_insert.py`: Verifica inserciones y casos de rotación/promoción.
- `test_delete.py`: Verifica eliminaciones y casos de democión/rotación.
- `test_search.py`: Verifica búsquedas de claves existentes y no existentes.

---

## Benchmarks
Para comparar empíricamente WAVL con AVL y RBT:

1. **Generar datos de benchmarking**  
   ```bash
   python3 wavl/benchmarks/scripts/bench_wavl_vs_avl_rbt.py --output wavl/benchmarks/data/bench_wavl_avl_rbt.csv
   ```

2. **Generar gráficos**  
   ```bash
   python3 wavl/benchmarks/scripts/plot_benchmarks.py --input wavl/benchmarks/data/bench_wavl_avl_rbt.csv --output wavl/benchmarks/plots/
   ```

Los gráficos resultantes se guardan en `wavl/benchmarks/plots/` y permiten visualizar:
- Comparación de promociones (WAVL) vs recoloraciones (RBT) en inserciones aleatorias y secuenciales.
- Altura promedio de cada estructura.
- Tiempo de inserción/eliminación.

---
