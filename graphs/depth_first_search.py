from typing import List, Dict

from base_graph import Graph
from base_vertice import Vertice

class Depth_first_search(Graph):
	def __init__(self):
		super(Depth_first_search, self).__init__()

	def e_um_dag_dfs(self, vertice:Vertice, visitados:Dict[Vertice,int]) -> bool:
		"""
		vertice: vertice a ser explorado
		visitados: Dicionário que mapeia, cada vertice explorado. 
				Se visitados[vertice]==1: o vértice ainda sendo explorado ou foi encontrado um ciclo neste vertice explorado
				Se visitados[vertice]==2: o vértice já foi explorado totalmente e não foi encontrado ciclo durante a exploração
		"""
		visitados[vertice] = 1 
		for adj in vertice.adjacencias:
			if visitados[adj]>visitados[vertice]:
				return True
			if(visitados[adj]==0):
				self.e_um_dag_dfs(adj,visitados)
		visitados[vertice]=2
		return False

	# return True if it's a directed acyclical graph
	def e_um_dag(self) -> bool:
		visitados = {}

		for vertice in self.vertices.values():
			visitados[vertice] = 0

		for vertice in self.vertices.values():
			if visitados[vertice]==0:
				if self.e_um_dag_dfs(vertice, visitados):
					return True
		return False

	def depthSearch(self, u:Vertice, visited:List, topo_list:List):
		visited[u]=True
		for adj in u.adjacencias:
			if visited[adj] == False:
				self.depthSearch(adj,visited,topo_list)
		topo_list.insert(0,u)


	def ordenacao_topologica(self) -> List:
		visited = {}#Dict[Vertice,bool]
		topo_list_vertices = []
		topo_list_values = []
		for u in self.vertices.values():
			visited[u]=False;
		for u in self.vertices.values():
			if visited[u] == False:
				self.depthSearch(u,visited,topo_list_vertices)

		for ver in topo_list_vertices:
			topo_list_values.append(ver.valor)

		#print (topo_list_values,topo_list_vertices)

		return topo_list_values


