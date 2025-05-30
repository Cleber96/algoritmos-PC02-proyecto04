# wavl/avl.py

from typing import Optional

class NodeAVL:
    """
    Nodo para AVL Tree:
    - key: la clave almacenada
    - left, right: hijos (NodeAVL o None)
    - parent: nodo padre (NodeAVL o None)
    - height: altura del subárbol en este nodo
    """
    def __init__(self, key):
        self.key: int = key
        self.left: Optional[NodeAVL] = None
        self.right: Optional[NodeAVL] = None
        self.parent: Optional[NodeAVL] = None
        self.height: int = 0  # Altura de hoja = 0

    def __repr__(self):
        left_k = self.left.key if self.left else None
        right_k = self.right.key if self.right else None
        return (f"NodeAVL(key={self.key}, height={self.height}, "
                f"left={left_k}, right={right_k})")


class AVLTree:
    """
    Implementación de un Árbol AVL con:
    - search(key)
    - insert(key)
    - delete(key)
    - Instrumentación: rotation_count (conteo de rotaciones)
    """

    def __init__(self):
        self.root: Optional[NodeAVL] = None
        self.rotation_count: int = 0

    # -------------------- UTILIDADES --------------------

    def _update_height(self, node: NodeAVL):
        """
        Recalcula la altura de `node` a partir de sus hijos.
        """
        left_h = node.left.height if node.left else -1
        right_h = node.right.height if node.right else -1
        node.height = 1 + max(left_h, right_h)

    def _get_balance(self, node: Optional[NodeAVL]) -> int:
        """
        Retorna el balance factor: altura(izq) - altura(der).
        Por convención, altura(None) = -1.
        """
        if node is None:
            return 0
        left_h = node.left.height if node.left else -1
        right_h = node.right.height if node.right else -1
        return left_h - right_h

    # -------------------- ROTACIONES --------------------

    def _rotate_left(self, z: NodeAVL) -> NodeAVL:
        """
        Rotación simple a la izquierda en z:
        Incrementa rotation_count y actualiza parents/heights.
        Retorna `y` como nueva raíz de este subárbol.
        """
        self.rotation_count += 1
        y = z.right
        T2 = y.left

        # 1) Reestructurar hijos
        y.left = z
        z.right = T2

        # 2) Ajustar parents
        parent_of_z = z.parent
        y.parent = parent_of_z
        z.parent = y
        if T2:
            T2.parent = z

        # 3) Reconectar y con parent_of_z
        if parent_of_z is None:
            self.root = y
        else:
            if parent_of_z.left is z:
                parent_of_z.left = y
            else:
                parent_of_z.right = y

        # 4) Actualizar alturas
        self._update_height(z)
        self._update_height(y)
        return y

    def _rotate_right(self, z: NodeAVL) -> NodeAVL:
        """
        Rotación simple a la derecha en z:
        Incrementa rotation_count y actualiza parents/heights.
        Retorna `y` como nueva raíz de este subárbol.
        """
        self.rotation_count += 1
        y = z.left
        T2 = y.right

        # 1) Reestructurar hijos
        y.right = z
        z.left = T2

        # 2) Ajustar parents
        parent_of_z = z.parent
        y.parent = parent_of_z
        z.parent = y
        if T2:
            T2.parent = z

        # 3) Reconectar y con parent_of_z
        if parent_of_z is None:
            self.root = y
        else:
            if parent_of_z.left is z:
                parent_of_z.left = y
            else:
                parent_of_z.right = y

        # 4) Actualizar alturas
        self._update_height(z)
        self._update_height(y)
        return y

    # -------------------- SEARCH --------------------

    def search(self, key) -> Optional[NodeAVL]:
        """
        Busca recursivamente la clave `key` y retorna el nodo, o None si no existe.
        """
        return self._search_rec(self.root, key)

    def _search_rec(self, node: Optional[NodeAVL], key) -> Optional[NodeAVL]:
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
        Inserta `key` en el AVL:
        1) Si root es None, crea nuevo nodo como raíz.
        2) Sino, inserta recursivamente como BST.
        3) Al volver, actualiza alturas y hace rotaciones según balance factor.
        """
        if self.root is None:
            self.root = NodeAVL(key)
            return

        self.root = self._insert_rec(self.root, key)

    def _insert_rec(self, node: NodeAVL, key) -> NodeAVL:
        # 1) Inserción BST normal
        if key < node.key:
            if node.left is None:
                new_node = NodeAVL(key)
                node.left = new_node
                new_node.parent = node
            else:
                node.left = self._insert_rec(node.left, key)
                node.left.parent = node
        else:
            if node.right is None:
                new_node = NodeAVL(key)
                node.right = new_node
                new_node.parent = node
            else:
                node.right = self._insert_rec(node.right, key)
                node.right.parent = node

        # 2) Actualizar altura de este nodo
        self._update_height(node)

        # 3) Chequear balance
        balance = self._get_balance(node)

        # 4) Rotaciones según el caso

        # LL case (inserción en subárbol izquierdo de hijo izquierdo)
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)

        # RR case (inserción en subárbol derecho de hijo derecho)
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)

        # LR case (inserción en subárbol derecho de hijo izquierdo)
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            node.left.parent = node
            return self._rotate_right(node)

        # RL case (inserción en subárbol izquierdo de hijo derecho)
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            node.right.parent = node
            return self._rotate_left(node)

        # Si no necesitó rotar, retorna este nodo
        return node

    # -------------------- DELETE --------------------

    def delete(self, key):
        """
        Elimina `key` del AVL:
        1) Si no existe, retorna.
        2) Llama a _delete_rec para obtener nueva subraíz.
        3) Actualiza heights/rotaciones hacia arriba.
        """
        self.root = self._delete_rec(self.root, key)
        if self.root:
            self.root.parent = None

    def _delete_rec(self, node: Optional[NodeAVL], key) -> Optional[NodeAVL]:
        if node is None:
            return None

        # 1) BST delete
        if key < node.key:
            node.left = self._delete_rec(node.left, key)
            if node.left:
                node.left.parent = node
        elif key > node.key:
            node.right = self._delete_rec(node.right, key)
            if node.right:
                node.right.parent = node
        else:
            # Encontramos el nodo a borrar
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                temp = node.right
                temp.parent = node.parent
                return temp
            elif node.right is None:
                temp = node.left
                temp.parent = node.parent
                return temp
            else:
                # Dos hijos: encontrar sucesor in-order (mínimo en subárbol derecho)
                succ = node.right
                while succ.left:
                    succ = succ.left
                node.key = succ.key
                node.right = self._delete_rec(node.right, succ.key)
                if node.right:
                    node.right.parent = node

        # 2) Si la rama quedó vacía, retornamos
        if node is None:
            return None

        # 3) Actualizar altura
        self._update_height(node)

        # 4) Chequear balance
        balance = self._get_balance(node)

        # 5) Rotaciones según casos

        # LL case
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # LR case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            node.left.parent = node
            return self._rotate_right(node)

        # RR case
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # RL case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            node.right.parent = node
            return self._rotate_left(node)

        return node
