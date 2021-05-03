class Vertice:
	def __init__(self, valor):
		self.valor = valor
		self.adjacencias = {}

	def insere(self, vizinho:"Vertice", peso:int):
		self.adjacencias[vizinho] = peso

	def obtem_valor(self):
		return self.valor

	def __str__(self):
		return f"v_value:{self.valor} len_adj: {len(self.adjacencias)}"