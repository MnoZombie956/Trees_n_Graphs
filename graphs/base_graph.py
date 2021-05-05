from base_vertice import Vertice

class Graph:
	def __init__(self):
		self.vertices = {}

	def adiciona_vertice(self, valor_vertice) -> Vertice:
		#importante pois podem haver vertices que não tem arestas
		novo_vertice = Vertice(valor_vertice)
		self.vertices[valor_vertice] = novo_vertice
		return novo_vertice

	def adiciona_aresta(self, valor_origem, valor_destino, peso:int=1, bidirecional = False):
		vertice_origem = self.obtem_vertice(valor_origem)
		vertice_destino = self.obtem_vertice(valor_destino)
		if not vertice_origem is None and not vertice_destino is None:
			vertice_origem.insere(vertice_destino, peso)
			if bidirecional:
				vertice_destino.insere(vertice_origem,peso)	
	def obtem_vertice(self, valor_vertice) -> Vertice:
		if valor_vertice in self.vertices:
			return self.vertices[valor_vertice]
		else:
			return None
			
	def print(self, start_vertice=None, tab="", visited=[], parent = None):
		for value in self.vertices:
			if start_vertice:
				value = start_vertice.valor
			weight = 0
			if parent:
				weight = parent.adjacencias[start_vertice]

			vertice = self.obtem_vertice(value)
			print(tab,f"-{weight}-",vertice.valor)
			for adj in vertice.adjacencias:
				if adj not in visited: # in case there is cycles
					visited.append(adj)
					self.print(adj, tab+"|    ", visited, vertice)
				else:
					print(tab,f"-{vertice.adjacencias[adj]}-",vertice.valor,"->",adj.valor)

			if start_vertice:
				return