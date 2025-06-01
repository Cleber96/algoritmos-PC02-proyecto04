# wavl/wavl_impl/tree_wavl.py

from typing import Optional
from node_wavl import NodeWAVL
from utils_wavl import get_rank, rank_differences

class WAVLTree:
    def __init__(self):
        self.root: Optional[NodeWAVL] = None
        # Contadores para benchmarking
        self.promote_count = 0
        self.demote_count = 0
        self.rotation_count = 0

    def search(self, key) -> Optional[NodeWAVL]:
        return self._search_rec(self.root, key)

    def _search_rec(self, node: Optional[NodeWAVL], key) -> Optional[NodeWAVL]:
        if node is None:
            return None
        if key == node.key:
            return node
        elif key < node.key:
            return self._search_rec(node.left, key)
        else:
            return self._search_rec(node.right, key)


    def insert(self, key):
        if self.root is None:
            self.root = NodeWAVL(key)
            return

        new_node = self._insert_rec(self.root, key)
        self._fix_insert(new_node)

    def _insert_rec(self, node: NodeWAVL, key) -> NodeWAVL:
        if key < node.key:
            if node.left is None:
                new_node = NodeWAVL(key)
                node.left = new_node
                new_node.parent = node
                return new_node
            else:
                return self._insert_rec(node.left, key)
        else:
            if node.right is None:
                new_node = NodeWAVL(key)
                node.right = new_node
                new_node.parent = node
                return new_node
            else:
                return self._insert_rec(node.right, key)

    def _fix_insert(self, node: NodeWAVL):
        current = node.parent

        while current is not None:
            rd_left, rd_right = rank_differences(current)

            # Si ambas diferencias >= 2 → no hubo violación → terminamos
            if rd_left >= 2 and rd_right >= 2:
                break

            # Si alguna diferencia < 1 → promovemos current
            if rd_left < 1 or rd_right < 1:
                self._promote(current)

                # Recalculamos tras la promoción
                new_rd_left, new_rd_right = rank_differences(current)
                # Si ambas diferencias < 1 tras promover → caso doble 0-0
                if new_rd_left < 1 and new_rd_right < 1:
                    left_child = current.left
                    right_child = current.right

                    # LL case: izquierda-izquierda
                    if left_child is not None and rank_differences(left_child)[0] < 1:
                        new_root = self._rotate_right(current)
                        new_root.rank += 1    # promoción adicional
                        current.rank -= 1     # democión

                    # LR case: izquierda-derecha
                    elif left_child is not None:
                        self._rotate_left(left_child)
                        new_root = self._rotate_right(current)
                        new_root.rank += 1
                        new_root.right.rank -= 1

                    # RR case: derecha-derecha
                    elif right_child is not None and rank_differences(right_child)[1] < 1:
                        new_root = self._rotate_left(current)
                        new_root.rank += 1
                        current.rank -= 1

                    # RL case: derecha-izquierda
                    elif right_child is not None:
                        self._rotate_right(right_child)
                        new_root = self._rotate_left(current)
                        new_root.rank += 1
                        new_root.left.rank -= 1

                    # Tras rotar, terminamos
                    return

                # Si no fue doble 0-0, subimos y seguimos
                current = current.parent
                continue

            # Si llegamos aquí, ambas diferencias estaban en {1,2} → no violación
            break

    # ----------------------- DELETE -----------------------

    def delete(self, key):
        target = self.search(key)
        if target is None:
            return

        parent = target.parent
        new_subroot = self._delete_rec(self.root, key)
        if new_subroot is not None and new_subroot.parent is None:
            self.root = new_subroot

        if parent is not None:
            self._fix_delete(parent)
        else:
            if self.root is not None:
                self._fix_delete(self.root)

    def _delete_rec(self, node: Optional[NodeWAVL], key) -> Optional[NodeWAVL]:

        if node is None:
            return None

        if key < node.key:
            node.left = self._delete_rec(node.left, key)
            if node.left:
                node.left.parent = node
        elif key > node.key:
            node.right = self._delete_rec(node.right, key)
            if node.right:
                node.right.parent = node
        else:
            # Encontramos el nodo a eliminar
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                replacement = node.right
                replacement.parent = node.parent
                return replacement
            elif node.right is None:
                replacement = node.left
                replacement.parent = node.parent
                return replacement
            else:
                # Intercambiar con sucesor in-order
                succ = node.right
                while succ.left:
                    succ = succ.left
                node.key = succ.key
                node.right = self._delete_rec(node.right, succ.key)
                if node.right:
                    node.right.parent = node

        return node

    def _fix_delete(self, node: NodeWAVL):
        current = node

        while current is not None:
            rd_left, rd_right = rank_differences(current)

            # 1) Si ambas diferencias en {1,2}, terminamos
            if 1 <= rd_left <= 2 and 1 <= rd_right <= 2:
                break

            # 2) Si alguna diferencia > 2 → demovemos current
            if rd_left > 2 or rd_right > 2:
                self._demote(current)
                new_rd_left, new_rd_right = rank_differences(current)

                # 2a) Si ahora ambas diferencias en {1,2} → subimos
                if 1 <= new_rd_left <= 2 and 1 <= new_rd_right <= 2:
                    current = current.parent
                    continue

                # 2b) Si alguna diferencia < 1 tras demover → rotación y terminamos
                left_child = current.left
                right_child = current.right

                # Caso “lado izquierdo demasiado bajo” (rd_left > 2 antes)
                if rd_left > 2:
                    if left_child is not None and rank_differences(left_child)[0] > 1:
                        # LL deletion case
                        new_root = self._rotate_right(current)
                        new_root.rank -= 1
                        current.rank -= 1
                    else:
                        # LR deletion case
                        self._rotate_left(left_child)
                        new_root = self._rotate_right(current)
                        new_root.rank -= 1
                        new_root.right.rank += 1
                    return

                # Caso “lado derecho demasiado bajo” (rd_right > 2 antes)
                if rd_right > 2:
                    if right_child is not None and rank_differences(right_child)[1] > 1:
                        # RR deletion case
                        new_root = self._rotate_left(current)
                        new_root.rank -= 1
                        current.rank -= 1
                    else:
                        # RL deletion case
                        self._rotate_right(right_child)
                        new_root = self._rotate_left(current)
                        new_root.rank -= 1
                        new_root.left.rank += 1
                    return

                # 2c) Si tras demover alguna diferencia sigue > 2 → subimos y continuamos
                current = current.parent
                continue

            # 3) Si alguna diferencia < 1 tras eliminación directa → demovemos y subimos
            if rd_left < 1 or rd_right < 1:
                self._demote(current)
                current = current.parent
                continue

            # 4) Si llegamos aquí, no hay más violaciones → terminamos
            break

    # ----------------------- PROMOTE / DEMOTE -----------------------

    def _promote(self, node: NodeWAVL):
        node.rank += 1
        self.promote_count += 1

    def _demote(self, node: NodeWAVL):
        node.rank -= 1
        self.demote_count += 1

    # ----------------------- ROTATIONS -----------------------

    def _rotate_right(self, z: NodeWAVL) -> NodeWAVL:
        self.rotation_count += 1

        y = z.left
        T2 = y.right

        # 1) Reasignar punteros
        y.right = z
        z.left = T2

        # 2) Ajustar parent
        parent_of_z = z.parent
        y.parent = parent_of_z
        z.parent = y
        if T2 is not None:
            T2.parent = z

        # 3) Conectar y en el lugar de z
        if parent_of_z is None:
            self.root = y
        else:
            if parent_of_z.left is z:
                parent_of_z.left = y
            else:
                parent_of_z.right = y

        return y

    def _rotate_left(self, z: NodeWAVL) -> NodeWAVL:
        self.rotation_count += 1

        y = z.right
        T2 = y.left

        # 1) Reasignar punteros
        y.left = z
        z.right = T2

        # 2) Ajustar parent
        parent_of_z = z.parent
        y.parent = parent_of_z
        z.parent = y
        if T2 is not None:
            T2.parent = z

        # 3) Conectar y en el lugar de z
        if parent_of_z is None:
            self.root = y
        else:
            if parent_of_z.left is z:
                parent_of_z.left = y
            else:
                parent_of_z.right = y

        return y

    # ----------------------- SPLIT -----------------------
    def split(self, key) -> tuple["WAVLTree", "WAVLTree"]:
        node = self.search(key)
        if node is None:
            self.insert(key)
            node = self.search(key)

        left_sub = node.left
        right_sub = node.right
        node.left = None
        node.right = None
        if left_sub:
            left_sub.parent = None
        if right_sub:
            right_sub.parent = None

        treeL = WAVLTree()
        treeR = WAVLTree()
        treeL.root = left_sub
        treeR.root = right_sub

        if treeL.root is not None:
            treeL._fix_delete(treeL.root)
        if treeR.root is not None:
            treeR._fix_delete(treeR.root)

        return treeL, treeR

    # ----------------------- JOIN -----------------------
    def join(self, other: "WAVLTree") -> "WAVLTree":
        if self.root is None:
            return other
        if other.root is None:
            return self

        min_node = other.root
        while min_node.left:
            min_node = min_node.left
        k = min_node.key
        other.delete(k)

        pivot = NodeWAVL(k)
        left_rank = get_rank(self.root)
        right_rank = get_rank(other.root)
        pivot.rank = max(left_rank, right_rank) + 1

        pivot.left = self.root
        self.root.parent = pivot

        pivot.right = other.root
        if other.root:
            other.root.parent = pivot

        joined = WAVLTree()
        joined.root = pivot
        joined._fix_delete(pivot)
        return joined

