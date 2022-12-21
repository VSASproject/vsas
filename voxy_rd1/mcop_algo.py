#This code provides a solver module for MCOP algorithm
#It is based on the work
#Turgay Korkmaz and Marwan Krunz. 2001. Multi-constrained optimal path
#selection. In Proceedings IEEE INFOCOM 2001.
#Basically, it calls the shortest path algorithm multiple times
#and achieve a approximation on Multi-contrained Optimal Path problem.
#We here implement it with a adajacent matrix representation of graph,
#and reference the code of open-source Dijestra, so this software follows GPL Lisense.

class Graph():
	def __init__(self, vertices):
		self.V = vertices
		self.graph = [[0 for column in range(vertices)]
					for row in range(vertices)]
		self.c = [0 for column in range(vertices)]
		self.g = [0 for column in range(vertices)]
		self.r = [0 for column in range(vertices)]
		self.cs = [[0 for column in range(vertices)]
					for row in range(vertices)]
		self.G = [0 for column in range(vertices)]
		self.dist = [1e7] * self.V
		self.dist[0] = 0
		self.sptSet = [False] * self.V



	def printSolution(self, dist):
		print("Vertex \t Distance from Source")
		for node in range(self.V):
			print(node, "\t\t", dist[node])


	def minDistance(self, dist, sptSet):
		min = 1e7
		for v in range(self.V):
			if dist[v] < min and sptSet[v] == False:
				min = dist[v]
				min_index = v
		return min_index

	def tri(self):
		return 1

	def max_tri(self):
		K=5
		return K

	def l_a(self):
		return 0

	#The key step of the MCOP algoritm
	def look_ahead_dijkstra_relax(self,u,v):
		K=5
		tmp = 0
		self.c[tmp] = self.c[u] + self.cs(u,v)
		lamda = self.l_a()
		if lamda < 10000:
			g[tmp] = self.tri()
		if lamda == 10000:
			g[tmp] = self.max_tri()
		for k in range(K):
			g[tmp] = g[u] + self.graph[u][v]
			self.r[tmp] = self.r[v]
		if self.prefer_the_best(tmp,v) == tmp:
			self.c[v] = self.c[tmp]
			self.g[v] = self.g[tmp]
			for i in range(K):
				self.G[v] = self.G[tmp]


		return

	def reverse_dijkstra_relax(self,u,v):
		if (self.graph[u][v] > 0 and
				self.sptSet[v] == False and
				self.dist[v] > self.dist[u] + self.graph[u][v]):
			self.dist[v] = self.dist[u] + self.graph[u][v]
		return

	def prefer_the_best(self,a,b):
		for k in range(self.V):
			if self.c[a] < self.c[b] and self.g[a] + self.r[a] < self.cs[k]:
				return a
			if self.c[a] > self.c[b] and self.g[a] + self.r[a] < self.cs[k]:
				return b
		if g[a] < g[b]:
			return a
		return b

	def check_feasible(self,src):
		return True

	def reverse_dijkstra(self,K):
		return 0

	def look_ahead_dijkstra(self,K):
		return 0

	def h_mcop(self, src):
		K = 5
		dist = self.reverse_dijkstra(K)
		if dist[src] > K:
			return -1
		dist = self.look_ahead_dijkstra(0)
		if self.check_feasible(src):
			return dist
		return -1



if __name__=="__main__":
	g = Graph(9)
	g.graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
			[4, 0, 8, 0, 0, 0, 0, 11, 0],
			[0, 8, 0, 7, 0, 4, 0, 0, 2],
			[0, 0, 7, 0, 9, 14, 0, 0, 0],
			[0, 0, 0, 9, 0, 10, 0, 0, 0],
			[0, 0, 4, 14, 10, 0, 2, 0, 0],
			[0, 0, 0, 0, 0, 2, 0, 1, 6],
			[8, 11, 0, 0, 0, 0, 1, 0, 7],
			[0, 0, 2, 0, 0, 0, 6, 7, 0]
			]
	g.h_mcop(0)

