from typing import List, Dict
from functools import total_ordering

# just importing the Min_heap from the trees' folder
import sys
sys.path.insert(0, '../trees')
from minimun_heap import Min_heap

from base_graph import Graph
from base_vertice import Vertice

@total_ordering
class DistanciaVerticeOrigem:
	def __init__(self, vertice:Vertice, distancia:int):
		self.vertice = vertice 
		self.distancia = distancia
		
	def __eq__(self, outro:"DistanciaVerticeOrigem") ->bool:
		return self.vertice == outro.vertice
    
	def __lt__(self,  outro:"DistanciaVerticeOrigem") -> bool:
		return self.distancia < outro.distancia

	def __gt__(self, outro:"DistanciaVerticeOrigem") -> bool:
		return self.distancia > outro.distancia
    
	def __str__(self):
		return f"distance to {self.vertice.valor}: {self.distancia}"
	
	def __repr__(self):
		return str(self)

class Dijkstra_algorithm(Graph):
	def __init__(self):
		super(Dijkstra_algorithm, self).__init__()

	def dijkstra_relax(self, fila_min_heap:Min_heap,vertice_u: Vertice, vertice_v:Vertice, distancia:Dict[Vertice, DistanciaVerticeOrigem], pai:Dict[Vertice,Vertice]):
		if distancia[vertice_v].distancia > distancia[vertice_u].distancia + vertice_u.adjacencias[vertice_v]:
			distancia[vertice_v].distancia = distancia[vertice_u].distancia + vertice_u.adjacencias[vertice_v]
			pai[vertice_v] = vertice_u
			fila_min_heap.insere(distancia[vertice_v])
			
	def dijkstra(self, valor_vertice_origem) -> (Dict[Vertice,DistanciaVerticeOrigem], Dict[Vertice,Vertice]):
		distancia = {}
		pai = {}
		vertice_origem = self.obtem_vertice(valor_vertice_origem)
		if not vertice_origem:
			return None

		fila_min_heap = Min_heap()
		#inicialização 
		for vertice in self.vertices.values():
			dvo_ver = DistanciaVerticeOrigem(vertice,float("inf"))
			fila_min_heap.insere(dvo_ver)
			distancia[vertice] = dvo_ver
			pai[vertice] = None
		
		#print(f"HEAP: {fila_min_heap}")
		#print(f"Vertice Origem: {vertice_origem.valor}")

		distancia[vertice_origem].distancia=0#ou = DistanciaVerticeOrigem(vertice_origem,0)

		while fila_min_heap.pos_ultimo_item:
			u = fila_min_heap.retira_min()
			if self.vertices[u.vertice.valor].adjacencias.keys():
				for adj in self.vertices[u.vertice.valor].adjacencias.keys():
					self.dijkstra_relax(fila_min_heap,u.vertice,adj,distancia,pai)
					
		return distancia, pai