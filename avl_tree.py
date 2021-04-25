from avl_node import Node_AVL
from base_tree import Tree
class AVL_tree(Tree):
    def __init__(self,root):
        super(AVL_tree,self).__init__(root)

    def print_avl(self, tab="", start:"Node_AVL"=None):
        if start == None:
            start = self.root

        print(tab,start.key)

        if start.left:
            self.print_avl(tab+"    ", start.left)
        else:
            print(tab+"    None")
        if start.right:
            self.print_avl(tab+"    ", start.right)
        else:
            print(tab+"    None")

    def left_rotation(self, raiz_sub_arvore):
        nova_raiz_sub_arvore = raiz_sub_arvore.right

        temp = nova_raiz_sub_arvore.left
        nova_raiz_sub_arvore.left = raiz_sub_arvore
        raiz_sub_arvore.right = temp

        raiz_sub_arvore.height_update()
        nova_raiz_sub_arvore.height_update()

        return nova_raiz_sub_arvore

    def right_rotation(self, raiz_sub_arvore):
        nova_raiz_sub_arvore = raiz_sub_arvore.left

        temp = nova_raiz_sub_arvore.right
        nova_raiz_sub_arvore.right = raiz_sub_arvore
        raiz_sub_arvore.left = temp

        raiz_sub_arvore.height_update()
        nova_raiz_sub_arvore.height_update()

        return nova_raiz_sub_arvore

    def double_right_rotation(self, raiz_sub_arvore):
        raiz_sub_arvore.left = self.left_rotation(raiz_sub_arvore.left)
        return self.right_rotation(raiz_sub_arvore)

    def double_left_rotation(self,raiz_sub_arvore): # LR
        raiz_sub_arvore.right = self.right_rotation(raiz_sub_arvore.right)
        return self.left_rotation(raiz_sub_arvore)

    def restructurate(self, raiz_sub_arvore, key):
        #Rebalanceia a árvore de tal forma que o balance sempre fique entre -1 e 1
        # Caso 1
        if raiz_sub_arvore.balance > 1 and key < raiz_sub_arvore.left.key:
            return self.right_rotation(raiz_sub_arvore)
        # Caso 2
        if raiz_sub_arvore.balance < -1 and key > raiz_sub_arvore.right.key:
            return self.left_rotation(raiz_sub_arvore)
        # Caso 3
        if raiz_sub_arvore.balance > 1 and key > raiz_sub_arvore.left.key:
            return self.double_right_rotation(raiz_sub_arvore)
        # Caso 4
        if raiz_sub_arvore.balance < -1 and key < raiz_sub_arvore.right.key:
            return self.double_left_rotation(raiz_sub_arvore)

        #caso já esteja equilibrado, a raiz subarvore não é modificada
        return raiz_sub_arvore

    def insert(self,key):
        self.root = self.insert_util(key, self.root)

    def insert_util(self, key, raiz_sub_arvore):
        #Inserção - alterando subarvores se necessario
        if not raiz_sub_arvore:
            return Node_AVL(key)
        elif key < raiz_sub_arvore.key:
            raiz_sub_arvore.left = self.insert_util(key,raiz_sub_arvore.left)
        elif key > raiz_sub_arvore.key:
            raiz_sub_arvore.right = self.insert_util(key,raiz_sub_arvore.right)
        else:
            #raiz desta subarvore não é modificada quando a key é a mesma - e não realiza inserção
            return raiz_sub_arvore
        # altura atualizada
        raiz_sub_arvore.height_update()

        return self.restructurate(raiz_sub_arvore,key)
       
    def delete_util(self, key, raiz_sub_arvore):

        # Find the node to be deleted and remove it
        if not raiz_sub_arvore:
            return Node_AVL(key)
        elif key < raiz_sub_arvore.key:
            raiz_sub_arvore.left = self.delete_util(key, raiz_sub_arvore.left)
        elif key > raiz_sub_arvore.key:
            raiz_sub_arvore.right = self.delete_util(key, raiz_sub_arvore.right)
        else:
            if raiz_sub_arvore.left is None:
                temp = raiz_sub_arvore.right
                raiz_sub_arvore = None
                return temp
            elif raiz_sub_arvore.right is None:
                temp = raiz_sub_arvore.left
                raiz_sub_arvore = None
                return temp
            temp = self.get_min_node(raiz_sub_arvore.right)
            raiz_sub_arvore.key = temp.key
            raiz_sub_arvore.right = self.delete_util(temp.key, raiz_sub_arvore.right)
        if raiz_sub_arvore is None:
            return raiz_sub_arvore

        raiz_sub_arvore.height_update()

        # restructurate a bit diferent
        if raiz_sub_arvore.balance > 1:
            if raiz_sub_arvore.left.balance >= 0:
                return self.right_rotation(raiz_sub_arvore)
            else:
                return self.double_right_rotation(raiz_sub_arvore)
        if raiz_sub_arvore.balance < -1:
            if raiz_sub_arvore.right.balance <= 0:
                return self.left_rotation(raiz_sub_arvore)
            else:
                return self.double_left_rotation(raiz_sub_arvore)

        return raiz_sub_arvore

    def delete(self,key):
        self.root = self.delete_util(key, self.root)

    def get_min_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_node(root.left)

    def preOrder(self, root):
        if not root:
            return
        print("{0} ".format(root.key), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)

    def getHeight(self, root):
        if not root:
            return 0
        return root.height