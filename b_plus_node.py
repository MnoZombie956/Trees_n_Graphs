class B_plus_node:
    def __init__(self, order):
        self.order = order
        self.values = []
        self.keys = []
        self.next_key = None
        self.parent = None
        self.is_leaf = False

    # Insert at the leaf
    def leaf_insert(self, leaf, value, key):
        if (self.values):
            flash = self.values
            for i in range(len(flash)):
                if (value == flash[i]):
                    self.keys[i].append(key)
                    break
                elif (value < flash[i]):
                    self.values = self.values[:i] + [value] + self.values[i:]
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    break
                elif (i + 1 == len(flash)):
                    self.values.append(value)
                    self.keys.append([key])
                    break
        else:
            self.values = [value]
            self.keys = [[key]]
