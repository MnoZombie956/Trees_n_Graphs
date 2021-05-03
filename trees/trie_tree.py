from trie_node import Node_trie
from typing import List

class Trie_tree:
	def __init__(self, root=None):
		if not root:
			root = Node_trie()
		self.root = root
	def print_trie(self, start_node=None, tab=""):
		if not start_node: 
			start_node = self.root

		for child_key in start_node.children_keys():
			temp_child = start_node.children[child_key]
			print(tab,temp_child.letter)
			self.print_trie(temp_child, tab+"|    ")

	def insert(self, words:str):
		current_node = self.root

		for i,letter in enumerate(words):
			if not current_node.is_children(letter):
				current_node.insert(letter, i == len(words)-1)

			current_node = current_node.get_child(letter)
		current_node.word_ending = True

	def search(self, words:str) -> bool:
		child = self.root
		for i,letter in enumerate(words):
			if (child.is_children(letter) and i<len(words)):
				child = child.get_child(letter)
				if(i+1==len(words) and child.word_ending==1):
					return True
			else:
				return False

	def predictor(self, words_prefix:str) -> List[str]:		
		#obtem a ultima letter do prefixo
		if self.root.is_children(words_prefix[0]):
			last_letter_prefix_node = self.root.get_child(words_prefix[0])
			#print("childs inicias:",last_letter_prefix_node.get_children())
		else:
			print("non-existent inicial prefix '",words_prefix[0],"' ")
			return []

		for i in range(1,len(words_prefix)):
			letter=words_prefix[i]
			#print("letter test:",letter)
			if last_letter_prefix_node.is_children(letter):
			#	print("a letter existe e os childs:")
				last_letter_prefix_node = last_letter_prefix_node.get_child(letter)
			#	print(last_letter_prefix_node)
			else:
			#	print("prefixo inexiste")
				return []
		#por meio da ultima letter do prefixo, faz a predição das possiveis wordss
		#Para isso, você poderá precisar de fazer um método recursivo
		predictions = [] #wordss finais

		posfixed_letters = []#letters filhas do ultimo no

		new_posfixes = []#posfix formados das letters filhas do ultimo noh caso este n sejam terminais, atualizado recursivamente

		# print("no_ult childs:",last_letter_prefix_node.get_children())

		for letter in last_letter_prefix_node.children_keys():
		# print("nC:",letter)
			if(last_letter_prefix_node.get_child(letter).word_ending):
			#	print("final!")
				predictions.append(words_prefix+letter)
			else:
				posfixed_letters.append(letter)

		#print("prontas:",predictions,"posfixed_letters:",posfixed_letters)

		for letter2 in posfixed_letters:
			new_posfixes.extend(self.predictor(words_prefix+letter2))

		for posfix in new_posfixes:
			predictions.append(posfix)

		return predictions

