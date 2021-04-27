import bisect

class Node_B(object):
    def __init__(self, values=None, children=None):
        self.parent = None
        self.values = values or []
        self.children = children
        if self.children:
            for i in self.children:
                i.parent = self

    def __str__(self):
        return str(self.values)
        
    def print_b(self, tab=''):
        print('%s%s' % (tab, self))
        if self.children:
            for i in self.children:
                i.print_b(tab + '   |')

    def search(self, val):
        i = bisect.bisect_left(self.values, val)
        if (i != len(self.values) and not val < self.values[i]):
            return (True, self, i)            
        if self.children is not None:
            return self.children[i].search(val)
        else:
            return (False, self, i)

    def split_node(self, b_tree, val=None, slot=None, children=None):
        halve = [] if val is None else [ val ]
        if slot is None:
            slot = 0

        split = self.values[0:slot] + halve + self.values[slot:]
        mid_index = len(split) // 2
        
        lv = split[0:mid_index]
        medianVal = split[mid_index]
        rv = split[mid_index + 1:]
        
        child = self.children is not None

        if child:
            if children is not None:
                child_halve = (self.children[0:slot] + 
                                 list(children) + 
                                 self.children[slot + 1:])
            else:
                child_halve = self.children
            lc = child_halve[0:len(lv) + 1]
            rc = child_halve[len(lv) + 1:]
        else:
            lc = None
            rc = None

        leftNode = Node_B(lv, lc)
        rightNode = Node_B(rv, rc)

        if self.parent:
            self.parent.insert(b_tree,
                            medianVal,
                            None,
                            (leftNode, rightNode))
        else:
            newRoot = Node_B([ medianVal ], [leftNode, rightNode])
            leftNode.parent = newRoot
            rightNode.parent = newRoot
            b_tree.root = newRoot
            b_tree.height += 1
            b_tree.size += 1
    
    def insert(self, b_tree, val, slot=None, children=None):
        child = self.children is not None
        if slot is None:
            slot = bisect.bisect_left(self.values, val)

        if len(self.values) < b_tree.max_values:
            self.values.insert(slot, val)
            b_tree.size += 1
            if children:
                for i in children:
                    i.parent = self
                self.children[slot:slot + 1] = children
            return True
        
        self.split_node(b_tree, val, slot, children)
        return True

    def min_value(self, slot=0):
        if self.children:
            return self.children[slot].min_value()
        return self.values[0], self, 0

    def max_value(self, slot=None):
        if slot is None:
            slot = len(self.values) - 1
        if self.children:
            return self.children[slot + 1].max_value()
        return self.values[-1], self, len(self.values) - 1

    def delete(self, b_tree, val, slot=None):

        child = self.children is not None        
        if slot is None:
            slot = bisect.bisect_left(self.values, val)
        
        if not child:
            # perform deletion from a leaf
            del self.values[slot]
            b_tree.size -= 1
            if len(self.values) < b_tree.min_values:
                # underflow happened in the leaf node
                # rebalance b_tree starting with this node
                self.rebalance(b_tree)
        else:
            # find the minimum value in the right subb_tree
            # and use it as the separator value to replace val
            newSep, node, index = self.min_value(slot + 1)
            self.values[slot] = newSep
            del node.values[index]
            b_tree.size -= 1
            if len(node.values) < b_tree.min_values:
                node.rebalance(b_tree)

    def rebalance(self, b_tree):
        left_node, right_node, index = self.get_siblings()
        if self.parent is None:
            return

        child = self.children is not None

        if not child:
            if right_node and len(right_node.values) > b_tree.min_values:
                sepIdx = index
                sepVal = self.parent.values[sepIdx]
                self.parent.values[sepIdx] = right_node.values[0]
                del right_node.values[0]
                self.values.append(sepVal)
                return
            elif left_node and len(left_node.values) > b_tree.min_values:
                sepIdx = index - 1
                sepVal = self.parent.values[sepIdx]
                self.parent.values[sepIdx] = left_node.values[-1]
                del left_node.values[-1]
                self.values.insert(0, sepVal)
                return

        # we have to merge 2 nodes
        if left_node is not None:
            sepIdx = index - 1
            ln = left_node
            rn = self
        elif right_node is not None:
            sepIdx = index
            ln = self
            rn = right_node

        sepVal = self.parent.values[sepIdx]

        ln.values.append(sepVal)
        ln.values.extend(rn.values)
        del rn.values[:]
        del self.parent.values[sepIdx]
        del self.parent.children[sepIdx + 1]
        if rn.children:
            ln.children.extend(rn.children)
            for i in rn.children:
                i.parent = ln

        if len(ln.values) > b_tree.max_values:
            # we have to split the newly formed node
            # this situation can aris only when merging inner nodes
            ln.split_node(b_tree)

        if len(self.parent.values) < b_tree.min_values:
            # rebalance the parent
            self.parent.rebalance(b_tree)            

        if self.parent.parent is None and not self.parent.values:
            b_tree.root = ln
            b_tree.root.parent = None

    """     
    Return the tupple:
    (left sibiling node, right sibling node, separator index).
    """
    def get_siblings(self):
        if not self.parent:
            return (None, None, 0)
        left_node = None
        right_node = None
        index = 0
        for i, j in enumerate(self.parent.children):
            if j is self:
                if i != 0:
                    left_node = self.parent.children[i - 1]
                if (i + 1) < len(self.parent.children):
                    right_node = self.parent.children[i + 1]
                index = i  
                break

        return (left_node, right_node, index)
class B_tree(object):
    def __init__(self, order):
        if order <= 2:
            raise ValueError("B_tree order must be at least 3") # look it up
        self.root = Node_B()
        self.order = order
        self.max_values = order - 1
        self.min_values = self.max_values // 2
        self.height = 1
        self.size = 0

    def insert(self, val):
        # find the leaf node where the value should be inserted
        found, node, slot = self.root.search(val)
        if found:
            # the value already exists, can't insert it twice
            return False
        return node.insert(self, val, slot, None)

    def delete(self, val):
        # find the value and its
        found, node, slot = self.root.search(val)
        if not found:
            # the value doesn't exist, can't delete it
            return False
        return node.delete(self, val, slot)

    def search(self, val):
        return self.root.search(val)[0]

    def min(self):
        return self.root.min_value()[0]

    def max(self):
        return self.root.max_value()[0]
