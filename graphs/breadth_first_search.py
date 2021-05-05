from typing import List, Dict

from base_graph import Graph
from base_vertice import Vertice

class Breadth_first_search(Graph):
	def __init__(self):
		super(Breadth_first_search, self).__init__()

	# return a dictionary of the distances between origin and other vertices
	def grau_separacao(self, valor_vertice_origem) -> Dict[Vertice,int]:
		distancia = {}
		visitou = {}
		vertice_inicial = self.obtem_vertice(valor_vertice_origem)

		if not vertice_inicial:
			return None
		for vertice in self.vertices.values():
			distancia[vertice] = float("inf")
			visitou[vertice] = False

		visitou[vertice_inicial] = True
		distancia[vertice_inicial] = 0

		queue = [vertice_inicial,]

		while len(queue) != 0:
			flash_vertice = queue.pop(0)
			#for quick_vertice in queue:
				#print(quick_vertice.valor)
			#print("flash:",flash_vertice.valor)
			if self.vertices[flash_vertice.obtem_valor()].adjacencias:
				for vertice in self.vertices[flash_vertice.obtem_valor()].adjacencias:
					#print("adj:",vertice.valor,"vis:",visitou[vertice],"dis:",distancia[vertice])
					if visitou[vertice] is False:
						#print("append:",vertice.valor)
						queue.append(vertice)
						distancia[vertice]=distancia[flash_vertice]+1#self.vertices[flash_vertice.obtem_valor()].adjacencias[vertice]
						visitou[vertice] = True
						#print("-->adj:",vertice.valor,"vis:",visitou[vertice],"dis:",distancia[vertice])

		return distancia  