from typing import List

class Node_trie:
	def __init__(self, letter="", word_ending:bool=False):
		self.children = dict()
		self.word_ending = word_ending
		self.letter = letter

	def insert(self, letter:str, word_ending:bool):
		self.children[letter] = Node_trie(letter, word_ending)

	def is_children(self, letter:str) -> bool:
		return letter in self.children

	def get_child(self,letter:str) -> "Node_trie":
		return self.children[letter]

	def children_keys(self) -> List[str]:
		return self.children.keys()
