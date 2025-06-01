# wavl/rbt.py

from typing import Optional

RED = "RED"
BLACK = "BLACK"

class NodeRBT:
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
        current = node
        while current.left:
            current = current.left
        return current

    # -------------------- ROTACIONES --------------------

    def _rotate_left(self, x: NodeRBT):
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
        new_node = NodeRBT(key, color=RED)
        self._bst_insert(new_node)
        self._fix_insert(new_node)

    def _bst_insert(self, node: NodeRBT):
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
        while z.parent and z.parent.color == RED:
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
        z = self.search(key)
        if z is None:
            return
        if z.left and z.right:
            succ = self._minimum(z.right)
            z.key = succ.key
            z = succ

        replacement = z.left if z.left else z.right
        original_color = z.color


        if replacement:
            self._replace_node(z, replacement)
        else:
            if z.parent is None:
                self.root = None
            else:
                if z == z.parent.left:
                    z.parent.left = None
                else:
                    z.parent.right = None
            replacement = None
        
        if original_color == BLACK:
            self._fix_delete(replacement, z.parent)

    def _fix_delete(self, x: Optional[NodeRBT], parent: Optional[NodeRBT]):

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
