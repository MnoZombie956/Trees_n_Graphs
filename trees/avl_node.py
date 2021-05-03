from base_node import Node

class Node_AVL(Node):
    def __init__(self, key, left:"Node_AVL"=None, right:"Node_AVL"=None):
    	super(Node_AVL,self).__init__(key,left,right)
    	self.height=1

    @property
    def left_subtree_height(self):
        if self.left is None:
            return 0
        return self.left.height

    @property
    def right_subtree_height(self):
        if self.right is None:
            return 0

        return self.right.height

    @property
    def balance(self):
        return self.left_subtree_height-self.right_subtree_height

    def height_update(self):
        self.height = 1 + max(self.left_subtree_height,self.right_subtree_height)
