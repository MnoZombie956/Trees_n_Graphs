import math
from b_plus_node import B_plus_node

class B_plus_tree:
    def __init__(self, order):
        self.root = B_plus_node(order)
        self.root.is_leaf = True

    def print_b_plus(self, tab="", start_node:"B_plus_node"=None, current_depth:int=0):
        if not start_node:
            start_node = self.root

        if start_node.is_leaf == False:
            print(f"{current_depth:3d}",tab,start_node.values,"n_children: ",len(start_node.keys))  
            for key in start_node.keys:
                self.print_b_plus(tab+"|    ",key, current_depth+1)
            return
        if start_node.values:
            print(f"{current_depth:3d}",tab,start_node.values)

    def get_node(self, value):
        current_node = self.root
        while(current_node.is_leaf == False):
            temp2 = current_node.values
            for i in range(len(temp2)):
                if (value == temp2[i]):
                    current_node = current_node.keys[i + 1]
                    break
                elif (value < temp2[i]):
                    current_node = current_node.keys[i]
                    break
                elif (i + 1 == len(current_node.values)):
                    current_node = current_node.keys[i + 1]
                    break
        return current_node

    def search(self, value, key):
        node = self.get_node(value)
        for i, item in enumerate(node.values):
            if item == value:
                if key in node.keys[i]:
                    return True
                else:
                    return False
        return False

    def insert(self, value, key):
        value = str(value)
        old_node = self.get_node(value)
        old_node.leaf_insert(old_node, value, key)

        if (len(old_node.values) == old_node.order):
            node1 = B_plus_node(old_node.order)
            node1.is_leaf = True
            node1.parent = old_node.parent
            mid = int(math.ceil(old_node.order / 2)) - 1
            node1.values = old_node.values[mid + 1:]
            node1.keys = old_node.keys[mid + 1:]
            node1.next_key = old_node.next_key
            old_node.values = old_node.values[:mid + 1]
            old_node.keys = old_node.keys[:mid + 1]
            old_node.next_key = node1
            self.insert_util(old_node, node1.values[0], node1)

    def insert_util(self, n, value, ndash):
        if (self.root == n):
            rootB_plus_node = B_plus_node(n.order)
            rootB_plus_node.values = [value]
            rootB_plus_node.keys = [n, ndash]
            self.root = rootB_plus_node
            n.parent = rootB_plus_node
            ndash.parent = rootB_plus_node
            return

        parentB_plus_node = n.parent
        flash3 = parentB_plus_node.keys
        for i in range(len(flash3)):
            if (flash3[i] == n):
                parentB_plus_node.values = parentB_plus_node.values[:i] + \
                    [value] + parentB_plus_node.values[i:]
                parentB_plus_node.keys = parentB_plus_node.keys[:i +
                                                  1] + [ndash] + parentB_plus_node.keys[i + 1:]
                if (len(parentB_plus_node.keys) > parentB_plus_node.order):
                    parentdash = B_plus_node(parentB_plus_node.order)
                    parentdash.parent = parentB_plus_node.parent
                    mid = int(math.ceil(parentB_plus_node.order / 2)) - 1
                    parentdash.values = parentB_plus_node.values[mid + 1:]
                    parentdash.keys = parentB_plus_node.keys[mid + 1:]
                    value_ = parentB_plus_node.values[mid]
                    if (mid == 0):
                        parentB_plus_node.values = parentB_plus_node.values[:mid + 1]
                    else:
                        parentB_plus_node.values = parentB_plus_node.values[:mid]
                    parentB_plus_node.keys = parentB_plus_node.keys[:mid + 1]
                    for j in parentB_plus_node.keys:
                        j.parent = parentB_plus_node
                    for j in parentdash.keys:
                        j.parent = parentdash
                    self.insert_util(parentB_plus_node, value_, parentdash)

    def delete(self, value, key):
        node_ = self.get_node(value)

        temp = 0
        for i, item in enumerate(node_.values):
            if item == value:
                temp = 1

                if key in node_.keys[i]:
                    if len(node_.keys[i]) > 1:
                        node_.keys[i].pop(node_.keys[i].index(key))
                    elif node_ == self.root:
                        node_.values.pop(i)
                        node_.keys.pop(i)
                    else:
                        node_.keys[i].pop(node_.keys[i].index(key))
                        del node_.keys[i]
                        node_.values.pop(node_.values.index(value))
                        self.delete_util(node_, value, key)
                else:
                    print("Value has no compatible key")
                    return
        if temp == 0:
            print("Tree with no such value")
            return

    def delete_util(self, node_, value, key):

        if not node_.is_leaf:
            for i, item in enumerate(node_.keys):
                if item == key:
                    node_.keys.pop(i)
                    break
            for i, item in enumerate(node_.values):
                if item == value:
                    node_.values.pop(i)
                    break

        if self.root == node_ and len(node_.keys) == 1:
            self.root = node_.keys[0]
            node_.keys[0].parent = None
            del node_
            return
        elif (len(node_.keys) < int(math.ceil(node_.order / 2)) and node_.is_leaf == False) or (len(node_.values) < int(math.ceil((node_.order - 1) / 2)) and node_.is_leaf == True):

            is_predecessor = 0
            parentB_plus_node = node_.parent
            PrevB_plus_node = -1
            NextB_plus_node = -1
            PrevK = -1
            PostK = -1
            for i, item in enumerate(parentB_plus_node.keys):

                if item == node_:
                    if i > 0:
                        PrevB_plus_node = parentB_plus_node.keys[i - 1]
                        PrevK = parentB_plus_node.values[i - 1]

                    if i < len(parentB_plus_node.keys) - 1:
                        NextB_plus_node = parentB_plus_node.keys[i + 1]
                        PostK = parentB_plus_node.values[i]

            if PrevB_plus_node == -1:
                ndash = NextB_plus_node
                value_ = PostK
            elif NextB_plus_node == -1:
                is_predecessor = 1
                ndash = PrevB_plus_node
                value_ = PrevK
            else:
                if len(node_.values) + len(NextB_plus_node.values) < node_.order:
                    ndash = NextB_plus_node
                    value_ = PostK
                else:
                    is_predecessor = 1
                    ndash = PrevB_plus_node
                    value_ = PrevK

            if len(node_.values) + len(ndash.values) < node_.order:
                if is_predecessor == 0:
                    node_, ndash = ndash, node_
                ndash.keys += node_.keys
                if not node_.is_leaf:
                    ndash.values.append(value_)
                else:
                    ndash.next_key = node_.next_key
                ndash.values += node_.values

                if not ndash.is_leaf:
                    for j in ndash.keys:
                        j.parent = ndash

                self.delete_util(node_.parent, value_, node_)
                del node_
            else:
                if is_predecessor == 1:
                    if not node_.is_leaf:
                        ndashpm = ndash.keys.pop(-1)
                        ndashkm_1 = ndash.values.pop(-1)
                        node_.keys = [ndashpm] + node_.keys
                        node_.values = [value_] + node_.values
                        parentB_plus_node = node_.parent
                        for i, item in enumerate(parentB_plus_node.values):
                            if item == value_:
                                p.values[i] = ndashkm_1
                                break
                    else:
                        ndashpm = ndash.keys.pop(-1)
                        ndashkm = ndash.values.pop(-1)
                        node_.keys = [ndashpm] + node_.keys
                        node_.values = [ndashkm] + node_.values
                        parentB_plus_node = node_.parent
                        for i, item in enumerate(p.values):
                            if item == value_:
                                parentB_plus_node.values[i] = ndashkm
                                break
                else:
                    if not node_.is_leaf:
                        ndashp0 = ndash.keys.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node_.keys = node_.keys + [ndashp0]
                        node_.values = node_.values + [value_]
                        parentB_plus_node = node_.parent
                        for i, item in enumerate(parentB_plus_node.values):
                            if item == value_:
                                parentB_plus_node.values[i] = ndashk0
                                break
                    else:
                        ndashp0 = ndash.keys.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node_.keys = node_.keys + [ndashp0]
                        node_.values = node_.values + [ndashk0]
                        parentB_plus_node = node_.parent
                        for i, item in enumerate(parentB_plus_node.values):
                            if item == value_:
                                parentB_plus_node.values[i] = ndash.values[0]
                                break

                if not ndash.is_leaf:
                    for j in ndash.keys:
                        j.parent = ndash
                if not node_.is_leaf:
                    for j in node_.keys:
                        j.parent = node_
                if not parentB_plus_node.is_leaf:
                    for j in parentB_plus_node.keys:
                        j.parent = parentB_plus_node
