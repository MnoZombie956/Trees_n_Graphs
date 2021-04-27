from trie_tree import Trie_tree
from trie_node import Node_trie

class Patricia_tree(Trie_tree):
	# Overwriting Trie_tree insert method	
	def insert(self, words:str, current_node=None):
		if not current_node:
			current_node = self.root
		
		if not current_node.children.keys(): # if is an empty node, just create a child
			current_node.children[words] = Node_trie(words, True)
			self.root = current_node
			return True

		common  = ""
		for child_key in current_node.children.keys():
			if child_key[0] != words[0]:
				continue
			for i in range(0,len(child_key)):
				if (child_key == words[:i+1]):
					self.insert(words[i+1:],current_node.children[child_key])
					self.root = current_node
					return True

				if child_key[i] != words[i]:
					save_children = current_node.children[child_key].children
					del current_node.children[child_key]
					current_node.children[common] = Node_trie(common, False)
					self.insert(words[i:],current_node.children[common])

					self.insert(child_key[i:],current_node.children[common])
					current_node.children[common].children[child_key[i:]].children = save_children
					
					self.root = current_node
					return True
				common += words[i] # could be also child_key[i]
		current_node.children[words] = Node_trie(words, True)
		self.root = current_node
		return True
	# Just a rename, bad code
	def print_patricia(self):
		self.print_trie()