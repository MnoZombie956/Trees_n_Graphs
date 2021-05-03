# english is pretty close to pt-br so you'll get it

from typing import List, Dict
from functools import total_ordering

# just importing the Min_heap from the trees' folder
import sys
sys.path.insert(0, '../trees')
from minimun_heap import Min_heap

from base_graph import Graph
from base_vertice import Vertice

@total_ordering
class PesoVertice(): # weighted vertice
	def __init__(self, vertice_destino:Vertice, peso:int):
		self.vertice_destino = vertice_destino 
		self.peso = peso

	def __eq__(self, outro:"PesoVertice") ->bool:
		return self.vertice_destino.valor == outro.vertice_destino.valor and self.peso == outro.peso
	
	def __lt__(self,  outro:"PesoVertice") -> bool:
		return self.peso < outro.peso

	def __str__(self):
		return f"Peso até {self.vertice_destino.valor}: {self.peso}"
	
	def __repr__(self):
		return str(self)

	def __str__(self):
		return f"pv_peso:{self.peso} v_des: {self.vertice_destino}"


class Minimun_spanning_tree(Graph):
	def __init__(self):
		super(Minimun_spanning_tree, self).__init__()

	def cria_arv_geradora_minima(self, valor_vertice_inicial) -> Dict[Vertice,Vertice]:
		pai = {}
		set_ja_explorado = set()
		peso = {}
		vertice_inicial = self.obtem_vertice(valor_vertice_inicial)
		if not vertice_inicial:
			return None

		fila_min_heap = Min_heap()
		for vertice in self.vertices.values():
			pai[vertice] = None
			peso[vertice] = PesoVertice(vertice, float("inf"))
			

		#print(f"Origin Vertice: {vertice_inicial.valor}")
		peso[vertice_inicial].peso = 0
		fila_min_heap.insere(peso[vertice_inicial])

		while fila_min_heap.pos_ultimo_item:
			#print(f"min HEAP: {fila_min_heap}")
			u = fila_min_heap.retira_min()
			#print(f"Removed from heap: {u}")
			set_ja_explorado.add(u.vertice_destino)
			#print(f"Explored: {set_ja_explorado}")
			#print(f"for v in self.vertices[u.vertice_destino.valor] adj keys:")
			for v in self.vertices[u.vertice_destino.valor].adjacencias.keys():
				#print(f"\t{v}")
				if (not v in set_ja_explorado) and (u.vertice_destino.adjacencias[v]<peso[v].peso):
					pai[v] = u.vertice_destino
					peso[v].peso=u.vertice_destino.adjacencias[v]
					fila_min_heap.insere(peso[v])
				#print(f"updated")
		return pai