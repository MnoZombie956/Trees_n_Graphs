import math

class B_plus_node:
    def __init__(self, order):
        self.order = order
        self.values = []
        self.keys = []
        self.next_key = None
        self.parent = None
        self.is_leaf = False
        self.min_keys = int(math.ceil(self.order / 2)) - 1

    def insert(self, leaf, value, key):
        if (self.values):
            temp1 = self.values
            for i in range(len(temp1)):
                if (value == temp1[i]):
                    self.keys[i].append(key)
                    break
                elif (value < temp1[i]):
                    self.values.insert(i,value)
                    self.keys.insert(i,[key])
                    break
                elif (i + 1 == len(temp1)):
                    self.values.append(value)
                    self.keys.append([key])
                    break
        else:
            self.values = [value]
            self.keys = [[key]]


# B plus tree
class B_plus_tree:
    def __init__(self, order):
        self.root = B_plus_node(order)
        self.root.is_leaf = True

    def print_b_plus(self, tab="", start_node:"B_plus_node"=None, current_depth:int=0):
        if not start_node:
            start_node = self.root

        if start_node.is_leaf == False:
            print(f"{current_depth:3d}",tab,start_node.values)
            for key in start_node.keys:
                self.print_b_plus(tab+"|    ",key, current_depth+1)
            return True
        if start_node.values:
            print(f"{current_depth:3d}",tab,start_node.values)
 
    # true if value and key exists in tree
    def exists(self, value:str, key:"B_plus_node"):
        node = self.search_node(value)
        for i, item in enumerate(node.values):
            if item == value:
                if key in node.keys[i]:
                    return True
                else:
                    return False
        return False

    # return node from value
    def search_node(self, value):
        actual = self.root
        while(actual.is_leaf == False):
            values = actual.values
            for i in range(len(values)):
                if (value == values[i]):
                    actual = actual.keys[i + 1]
                    break
                elif (value < values[i]):
                    actual = actual.keys[i]
                    break
                elif (i + 1 == len(actual.values)):
                    actual = actual.keys[i + 1]
                    break
        return actual

    def insert_util(self, node, value, node_at):
        if (self.root == node):
            self.root = B_plus_node(node.order)
            self.root.keys = [node, node_at]
            self.root.values = [value]

            node.parent = self.root
            node_at.parent = self.root
            return True
            
        node_parent = node.parent
        for i in range(len(node_parent.keys)):
            if (node_parent.keys[i] == node):
                node_parent.values.insert(i,value)
                node_parent.keys.insert(i+1,node_at)

                if (len(node_parent.keys) > node_parent.order):
                    flash_node_parent = B_plus_node(node_parent.order)
                    flash_node_parent.parent = node_parent.parent

                    mid = node_parent.min_keys

                    flash_node_parent.values = node_parent.values[mid + 1:]
                    flash_node_parent.keys = node_parent.keys[mid + 1:]

                    parent_mid_value = node_parent.values[mid]

                    if (mid == 0):
                        node_parent.values = node_parent.values[:mid + 1]
                    else:
                        node_parent.values = node_parent.values[:mid]

                    node_parent.keys = node_parent.keys[:mid + 1]

                    for key in node_parent.keys:
                        key.parent = node_parent
                    for k in flash_node_parent.keys:
                        k.parent = flash_node_parent
                    self.insert_util(node_parent, parent_mid_value, flash_node_parent)

    def insert(self, value, key):
        value = str(value)
        actual = self.search_node(value)
        actual.insert(actual, value, key)

        if (len(actual.values) == actual.order): # violation found, rearange
            node = B_plus_node(actual.order)
            
            node.is_leaf = True
            node.parent = actual.parent
            
            mid = actual.min_keys
            
            node.values = actual.values[mid + 1:]
            node.keys = actual.keys[mid + 1:]
            node.next_key = actual.next_key

            actual.values = actual.values[:mid + 1]
            actual.keys = actual.keys[:mid + 1]

            actual.next_key = node
            self.insert_util(actual, node.values[0], node) # rearange function

    def delete(self, value, key):
        node = self.search_node(value)
        found = False
        for i, item in enumerate(node.values):
            if item == value:
                found = True

                if key in node.keys[i]:
                    if len(node.keys[i]) > 1:
                        node.keys[i].pop(node.keys[i].index(key))
                    elif node == self.root:
                        node.values.pop(i)
                        node.keys.pop(i)
                    else:
                        node.keys[i].pop(node.keys[i].index(key))
                        del node.keys[i]
                        node.values.pop(node.values.index(value))
                        self.delete_util(node, value, key)
                else:
                    print("Non-existent value")
                    return False
        if found == False:
            print("Non-existent value")
            return False

    def delete_util(self, node, value, key):
        if not node.is_leaf:
            for i, key in enumerate(node.keys):
                if key == key:
                    node.keys.pop(i)
                    break
            for i, value2 in enumerate(node.values):
                if value2 == value:
                    node.values.pop(i)
                    break

        if self.root == node and len(node.keys) == 1:
            self.root = node.keys[0]
            node.keys[0].parent = None
            del node
            return True
        elif (len(node.keys) < node.min_keys + 1 and node.is_leaf == False) \
            or (len(node.values) < int(math.ceil((node.order - 1) / 2)) and node.is_leaf == True):

            is_predecessor = False
            node_parent = node.parent
            previous_node = -1
            next_node = -1
            pre_key = -1 
            pos_key = -1
            for i, key in enumerate(node_parent.keys):
                if key == node:
                    if i > 0:
                        previous_node = node_parent.keys[i - 1]
                        pre_key = node_parent.values[i - 1]
                    if i < len(node_parent.keys) - 1:
                        next_node = node_parent.keys[i + 1]
                        pos_key = node_parent.values[i]

            if previous_node == -1:
                actual_node = next_node
                actual_value = pos_key
            elif next_node == -1:
                is_predecessor = True
                actual_node = previous_node
                actual_value = pre_key
            else:
                if len(node.values) + len(next_node.values) < node.order:
                    actual_node = next_node
                    actual_value = pos_key
                else:
                    is_predecessor = True
                    actual_node = previous_node
                    actual_value = pre_key

            if len(node.values) + len(actual_node.values) < node.order:
                if is_predecessor == False:
                    node, actual_node = actual_node, node
                actual_node.keys += node.keys
                if not node.is_leaf:
                    actual_node.values.append(actual_value)
                else:
                    actual_node.next_key = node.next_key
                actual_node.values += node.values

                if not actual_node.is_leaf:
                    for key in actual_node.keys:
                        key.parent = actual_node

                self.delete_util(node.parent, actual_value, node)
                del node
            else:
                if is_predecessor == True:
                    if not node.is_leaf:
                        actual_node_lastK = actual_node.keys.pop(-1)
                        actual_node_lastV = actual_node.values.pop(-1)
                        node.keys = [actual_node_lastK] + node.keys
                        node.values = [actual_value] + node.values
                        node_parent = node.parent
                        for i, value in enumerate(node_parent.values):
                            if value == actual_value:
                                parent.values[i] = actual_node_lastV
                                break
                    else:
                        actual_node_lastK = actual_node.keys.pop(-1)
                        actual_node_lastV = actual_node.values.pop(-1)
                        node.keys = [actual_node_lastK] + node.keys
                        node.values = [actual_node_lastV] + node.values
                        node_parent = node.parent
                        for i, value in enumerate(parent.values):
                            if value == actual_value:
                                node_parent.values[i] = actual_node_lastV
                                break
                else:
                    if not node.is_leaf:
                        actual_node_lastK = actual_node.keys.pop(0)
                        actual_node_lastV = actual_node.values.pop(0)
                        node.keys = node.keys + [actual_node_lastK]
                        node.values = node.values + [actual_value]
                        node_parent = node.parent
                        for i, value in enumerate(node_parent.values):
                            if value == actual_value:
                                node_parent.values[i] = actual_node_lastV
                                break
                    else:
                        actual_node_lastK = actual_node.keys.pop(0)
                        actual_node_lastV = actual_node.values.pop(0)
                        node.keys = node.keys + [actual_node_lastK]
                        node.values = node.values + [actual_node_lastV]
                        node_parent = node.parent
                        for i, value in enumerate(node_parent.values):
                            if value == actual_value:
                                node_parent.values[i] = actual_node.values[0]
                                break

                if not actual_node.is_leaf:
                    for key in actual_node.keys:
                        key.parent = actual_node
                if not node.is_leaf:
                    for key in node.keys:
                        key.parent = node
                if not node_parent.is_leaf:
                    for key in node_parent.keys:
                        key.parent = node_parent


# Print the tree


order = int(3)
bpt = B_plus_tree(order)

bpt.insert(value='1', key='1')
bpt.insert('3', '3')
bpt.insert('5', '5')
bpt.insert('7', '7')
bpt.insert('9', '9')
bpt.insert('3', '3')
# bpt.insert('2', '17')
# bpt.insert('6', '18')
# bpt.insert('8', '19')

bpt.print_b_plus()

if(bpt.exists('10', '8')):
    print("Found")
else:
    print("Not found")
			




