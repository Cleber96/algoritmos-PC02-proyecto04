# wavl/rbt.py

from typing import Optional

RED = "RED"
BLACK = "BLACK"

class NodeRBT:
    """
    Nodo para Red_Black Tree:
    - key: la clave almacenada
    - left, right, parent: apuntadores a hijos y padre
    - color: RED o BLACK
    """
    def __init__(self, key, color=RED):
        self.key: int = key
        self.left: Optional[NodeRBT] = None
        self.right: Optional[NodeRBT] = None
        self.parent: Optional[NodeRBT] = None
        self.color: str = color

    def __repr__(self):
        left_k = self.left.key if self.left else None
        right_k = self.right.key if self.right else None
        return (f"NodeRBT(key={self.key}, color={self.color}, "
                f"left={left_k}, right={right_k})")


class RBTree:
    """
    Implementación de Red_Black Tree con:
    - search(key)
    - insert(key)
    - delete(key)
    - Instrumentación: rotation_count (rotaciones) y recolor_count (recolores)
    """

    def __init__(self):
        self.root: Optional[NodeRBT] = None
        self.rotation_count: int = 0
        self.recolor_count: int = 0

    # -------------------- UTILIDADES --------------------

    def _is_red(self, node: Optional[NodeRBT]) -> bool:
        return node is not None and node.color == RED

    def _is_black(self, node: Optional[NodeRBT]) -> bool:
        return node is None or node.color == BLACK

    def _set_color(self, node: Optional[NodeRBT], color: str):
        if node is not None:
            node.color = color
            self.recolor_count += 1

    def _replace_node(self, u: NodeRBT, v: Optional[NodeRBT]):
        """
        Reemplaza el subárbol en `u` por el subárbol en `v`.
        Actualiza parent pointers.
        """
        if u.parent is None:
            self.root = v
        else:
            if u == u.parent.left:
                u.parent.left = v
            else:
                u.parent.right = v
        if v:
            v.parent = u.parent

    def _minimum(self, node: NodeRBT) -> NodeRBT:
        """
        Retorna el nodo con clave mínima en el subárbol rooted at 'node'.
        """
        current = node
        while current.left:
            current = current.left
        return current

    # -------------------- ROTACIONES --------------------

    def _rotate_left(self, x: NodeRBT):
        """
        Rotación simple a la izquierda en x:
        Incrementa rotation_count y actualiza punteros.
        """
        self.rotation_count += 1
        y = x.right
        b = y.left

        # 1) Reestructurar
        y.left = x
        x.right = b

        # 2) Ajustar padres
        y.parent = x.parent
        x.parent = y
        if b:
            b.parent = x

        # 3) Reconectar con x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            else:
                y.parent.right = y

    def _rotate_right(self, x: NodeRBT):
        """
        Rotación simple a la derecha en x:
        Incrementa rotation_count y actualiza punteros.
        """
        self.rotation_count += 1
        y = x.left
        b = y.right

        # 1) Reestructurar
        y.right = x
        x.left = b

        # 2) Ajustar padres
        y.parent = x.parent
        x.parent = y
        if b:
            b.parent = x

        # 3) Reconectar con x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            else:
                y.parent.right = y

    # -------------------- SEARCH --------------------

    def search(self, key) -> Optional[NodeRBT]:
        """
        Busca un nodo con clave `key`. Retorna NodeRBT o None.
        """
        return self._search_rec(self.root, key)

    def _search_rec(self, node: Optional[NodeRBT], key) -> Optional[NodeRBT]:
        if node is None:
            return None
        if key == node.key:
            return node
        elif key < node.key:
            return self._search_rec(node.left, key)
        else:
            return self._search_rec(node.right, key)

    # -------------------- INSERT --------------------

    def insert(self, key):
        """
        Inserta un nuevo nodo con `key`:
        1) Inserción BST normal (nodo color RED).
        2) Llamar a _fix_insert para restaurar propiedades RBT.
        """
        new_node = NodeRBT(key, color=RED)
        self._bst_insert(new_node)
        self._fix_insert(new_node)

    def _bst_insert(self, node: NodeRBT):
        """
        Inserta `node` en el lugar correspondiente como en un BST normal.
        """
        parent = None
        curr = self.root
        while curr:
            parent = curr
            if node.key < curr.key:
                curr = curr.left
            else:
                curr = curr.right

        node.parent = parent
        if parent is None:
            self.root = node
        else:
            if node.key < parent.key:
                parent.left = node
            else:
                parent.right = node

    def _fix_insert(self, z: NodeRBT):
        """
        Restablece propiedades RBT tras insertar z (color RED):
        Mientras el padre de z es RED, ajusta con rotaciones y recolores:
          - Caso 1: Tío RED → recolorear padre, tío, abuelo, y subir aplicación.
          - Caso 2: Tío BLACK y z en "posición interna" → rotación para convertir a "exterior".
          - Caso 3: Tío BLACK y z en "posición exterior"→ rotación en abuelo, recolorear.
        Finalmente, color(root) = BLACK.
        """
        while z.parent and z.parent.color == RED:
            # z tiene padre y es RED
            parent = z.parent
            grandpa = parent.parent
            if grandpa is None:
                break

            # Determinar si padre es hijo izquierdo o derecho de grandpa
            if parent == grandpa.left:
                uncle = grandpa.right
                # Caso 1: tío existe y es RED
                if self._is_red(uncle):
                    self._set_color(parent, BLACK)
                    self._set_color(uncle, BLACK)
                    self._set_color(grandpa, RED)
                    z = grandpa
                    continue
                # Caso 2: tío BLACK y z es hijo derecho → rotación izquierda en parent
                if z == parent.right:
                    z = parent
                    self._rotate_left(z)
                    parent = z.parent
                    grandpa = parent.parent
                # Caso 3: tío BLACK y z es hijo izquierdo → rotación derecha en grandpa
                self._set_color(parent, BLACK)
                self._set_color(grandpa, RED)
                self._rotate_right(grandpa)
            else:
                # Simétrico: padre es hijo derecho de grandpa
                uncle = grandpa.left
                if self._is_red(uncle):
                    self._set_color(parent, BLACK)
                    self._set_color(uncle, BLACK)
                    self._set_color(grandpa, RED)
                    z = grandpa
                    continue
                if z == parent.left:
                    z = parent
                    self._rotate_right(z)
                    parent = z.parent
                    grandpa = parent.parent
                self._set_color(parent, BLACK)
                self._set_color(grandpa, RED)
                self._rotate_left(grandpa)

        # Asegurar raíz en BLACK
        if self.root:
            self._set_color(self.root, BLACK)

    # -------------------- DELETE --------------------

    def delete(self, key):
        """
        Elimina un nodo con clave `key`:
        1) Buscar nodo a eliminar z.
        2) Si no existe, return.
        3) Si z tiene dos hijos, intercambiar su clave con el sucesor.
        4) Luego borrar el nodo (que tiene a lo sumo un hijo).
        5) Si el nodo borrado era BLACK, llamar a _fix_delete en el hijo que lo reemplazó (o en None).
        """
        z = self.search(key)
        if z is None:
            return

        # Si z tiene dos hijos, intercambiar con sucesor
        if z.left and z.right:
            succ = self._minimum(z.right)
            z.key = succ.key
            z = succ

        # Ahora z tiene a lo sumo un hijo
        replacement = z.left if z.left else z.right

        # Guardar color original
        original_color = z.color

        # Reemplazar z con replacement (que puede ser None)
        if replacement:
            self._replace_node(z, replacement)
        else:
            # replacement = None → borrar z y ajustar parent pointers
            if z.parent is None:
                self.root = None
            else:
                if z == z.parent.left:
                    z.parent.left = None
                else:
                    z.parent.right = None
            replacement = None  # para claridad

        # Si el color del nodo eliminado era BLACK, se rompe propiedad de cantidad de negros
        if original_color == BLACK:
            self._fix_delete(replacement, z.parent)

    def _fix_delete(self, x: Optional[NodeRBT], parent: Optional[NodeRBT]):
        """
        Restaura las propiedades RBT tras eliminar un nodo negro:
        - x es el nodo que reemplazó al nodo eliminado (puede ser None).
        - parent es el padre de x (o None si x es new root).
        Aplica los 4 casos clásicos hasta restablecer propiedades.
        """
        while (x is None or x.color == BLACK) and x is not self.root:
            if x == (parent.left if parent else None):
                # x es hijo izquierdo
                w = parent.right  # hermano de x
                # Caso 1: w es RED
                if self._is_red(w):
                    self._set_color(w, BLACK)
                    self._set_color(parent, RED)
                    self._rotate_left(parent)
                    w = parent.right

                # Caso 2: w es BLACK y ambos hijos de w son BLACK
                if self._is_black(w.left) and self._is_black(w.right):
                    self._set_color(w, RED)
                    x = parent
                    parent = x.parent if x else None
                else:
                    # Caso 3: w es BLACK, w.left es RED, w.right es BLACK
                    if self._is_black(w.right):
                        self._set_color(w.left, BLACK)
                        self._set_color(w, RED)
                        self._rotate_right(w)
                        w = parent.right
                    # Caso 4: w es BLACK y w.right es RED
                    self._set_color(w, parent.color)
                    self._set_color(parent, BLACK)
                    self._set_color(w.right, BLACK)
                    self._rotate_left(parent)
                    x = self.root  # terminamos bucle
            else:
                # x es hijo derecho (simetría)
                w = parent.left
                if self._is_red(w):
                    self._set_color(w, BLACK)
                    self._set_color(parent, RED)
                    self._rotate_right(parent)
                    w = parent.left

                if self._is_black(w.left) and self._is_black(w.right):
                    self._set_color(w, RED)
                    x = parent
                    parent = x.parent if x else None
                else:
                    if self._is_black(w.left):
                        self._set_color(w.right, BLACK)
                        self._set_color(w, RED)
                        self._rotate_left(w)
                        w = parent.left
                    self._set_color(w, parent.color)
                    self._set_color(parent, BLACK)
                    self._set_color(w.left, BLACK)
                    self._rotate_right(parent)
                    x = self.root

        if x:
            self._set_color(x, BLACK)
