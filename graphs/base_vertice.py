class Vertice:
	def __init__(self, valor):
		self.valor = valor
		self.adjacencias = {}

	def insere(self, vizinho:"Vertice", peso:int):
		self.adjacencias[vizinho] = peso

	def obtem_valor(self):
		return self.valor

	def __str__(self):
		return f"{self.valor} len(adj)={len(self.adjacencias)}"

	def __repr__(self):
		return str(self)