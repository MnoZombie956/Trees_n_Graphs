from typing import List

class Node_BST():
    def __init__(self, key, left:"Node_BST"=None, right:"Node_BST"=None):
        self.key = key
        self.left = left
        self.right = right
        self.size = 0
        
    def print_bst(self, tab=""):
        print(tab,self.key)
        if self.left:
            self.left.print_bst(tab+"|    ")
        else:
            print(tab+"    None")
        if self.right:
            self.right.print_bst(tab+"|    ")
        else:
            print(tab+"    None")

    def insert(self, key) -> bool:
        """
        Insere um nodo na árvore que a chave "key"
        """
        self.size = self.size + 1
        if key < self.key:
            if self.left:
                return self.left.insert(key)
            else:
                self.left = Node_BST(key)
                return True
        elif key > self.key:
            if self.right:
                return self.right.insert(key)
            else:
                self.right = Node_BST(key)
                return True
        else:
            return False
        
    def search(self, key) -> bool: # recursive, stack backtracking
        """
        Retorna verdadeiro caso a chave `key` exista na árvore
        """
        if key < self.key:
            if self.left:
                return self.left.search(key)
        elif key > self.key:
            if self.right:
                return self.right.search(key)
        else:
            return True
        return False

    def to_sorted_array(self, arr_result:List =None) -> List:
        """
        Retorna um vetor das chaves ordenadas.
        arr_result: Parametro com os itens já adicionados.
        """
        if(arr_result == None):
            arr_result = []

        if self.left:
            self.left.to_sorted_array(arr_result)

        arr_result.append(self.key)

        if self.right:
            self.right.to_sorted_array(arr_result)
        return arr_result
    
    def max_depth(self,current_max_depth:int=0) -> int:
        """
        Calcula a maior distancia entre o nodo raiz e a folha
        current_max_depth: Valor representando a maior distancia até então
                           ao chamar pela primeira vez, não é necessário usa-lo
        """
        current_max_depth = current_max_depth +1
        val_left,val_right = current_max_depth,current_max_depth

        if self.left:
            val_left = self.left.max_depth(current_max_depth)
        if self.right:
            val_right = self.right.max_depth(current_max_depth)

        if(val_left>val_right):
            return val_left
        else:
            return val_right
        
    def is_balanced(self):
        l_tree_max_depth,r_tree_max_depth=0,0
        l_tree_is_balanced,r_tree_is_balanced=None,None
        if self.key is None:
            return 1
        if self.left:
        	l_tree_is_balanced=self.left.is_balanced()
        	l_tree_max_depth=self.left.max_depth()
        if l_tree_is_balanced == 0:
            return 0
        if self.right:
        	r_tree_is_balanced=self.right.is_balanced()
        	r_tree_max_depth=self.right.max_depth()
        if r_tree_is_balanced == 0:
            return 0

        if abs(l_tree_max_depth - r_tree_max_depth) > 1:#se l % r nao sao
            return 0

        return 1

    def sorted_array_to_balanced_tree(self, array:List, start:int, end:int) -> "Node_BST":
        if (start > end):
            return None

        pos_raiz_sub_arvore = start
        raiz_sub_arvore = Node_BST(array[pos_raiz_sub_arvore])

        raiz_sub_arvore.left = Node_BST(array[pos_raiz_sub_arvore+1]) if len(array)>pos_raiz_sub_arvore+1 else None
        raiz_sub_arvore.right = Node_BST(array[pos_raiz_sub_arvore+2]) if len(array)>pos_raiz_sub_arvore+2 else None

        return raiz_sub_arvore

    def to_balanced_tree(self):
        array = self.to_sorted_array()
        return self.sorted_array_to_balanced_tree(array, 0, len(array)-1)
    
    def delete_node(self, root, key) -> "Node_BST":
        if root is None:
            return root
        if key < root.key:
            root.left = self.delete_node(root.left, key)
        elif(key > root.key):
            root.right = self.delete_node(root.right, key)
        elif(key == root.key): # "you have arrived in your destination"
            # If the node is with only one child or no child
            self.size = self.size - 1
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            # If the node has two children,
            # place the inorder successor in position of the node to be deleted
            temp = self.min_value_node(root.right)
            root.key = temp.key
            # Delete the inorder successor
            root.right = self.delete_node(root.right, temp.key)
        else:
            print("Deletion of a non-existent key")
            return None
        return root
    
    def min_value_node(self,node):
        current = node
        # Find the leftmost leaf, nice and simple
        while(current.left is not None):
            current = current.left
        return current
    
    def max_value_node(self,node):
        current = node
        # Find the rightmost leaf
        while(current.right is not None):
            current = current.right
        return current
