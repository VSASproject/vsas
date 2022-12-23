#This code provides a solver module for MCOP algorithm
#It is based on the work
#Turgay Korkmaz and Marwan Krunz. 2001. Multi-constrained optimal path
#selection. In Proceedings IEEE INFOCOM 2001.
#Basically, it calls the shortest path algorithm multiple times
#and achieve a approximation on Multi-contrained Optimal Path problem.
#We here implement it with a adajacent matrix representation of graph,
#and reference the code of open-source Dijestra, so this software follows GPL Lisense.

import heapq

class Graph():
	def __init__(self, vertices):
		self.K = 1
		self.V = vertices
		self.graph = [[0 for column in range(vertices)]
					for row in range(vertices)]
		self.cost_graph = [[0 for column in range(vertices)]
					  for row in range(vertices)]
		self.bandwidth_limit = 0
		self.lambda_order = 2
		self.path = [0 for column in range(vertices)]
		self.r = [0 for column in range(vertices)]
		self.R = [0 for column in range(vertices)]
		self.pi_r = [0 for column in range(vertices)]
		self.pi_g = [0 for column in range(vertices)]
		self.g = [0 for column in range(vertices)]
		self.G = [0 for column in range(vertices)]
		self.c = [0 for column in range(vertices)]


	def h_mcop(self, src, dest):
		dist = self.reverse_dijkstra(dest)
		if self.r[src] > self.K:
			return -1
		self.look_ahead_dijkstra(src)
		if self.G[dest] <= self.bandwidth_limit:
			return self.path
		return -1


	def reverse_dijkstra(self,dest):
		unvisited_queue = [(self.graph[v][dest], v) for v in range(0, 9)]
		visited = [0 for column in range(self.V)]
		heapq.heapify(unvisited_queue)
		while len(unvisited_queue):
			uv = heapq.heappop(unvisited_queue)
			current = uv[1]
			# set visited
			for v in range(self.V):
				if visited[v] == 1:
					continue
				elif self.graph[v][current] > 0:
					self.reverse_dijkstra_relax(current, v)
		return 0


	def reverse_dijkstra_relax(self,u,v):
		limit = (self.R[v] + self.cost_graph[u][v])/self.bandwidth_limit
		if self.r[u] > limit:
			self.r[u] = limit
			self.R[u] = self.R[v] + self.cost_graph[u][v]
			self.pi_r[v] = u
		return


	def look_ahead_dijkstra(self,s):
		unvisited_queue = [(self.graph[s][v],v) for v in range(0,9)]
		visited = [0 for column in range(self.V)]
		heapq.heapify(unvisited_queue)
		while len(unvisited_queue):
			uv = heapq.heappop(unvisited_queue)
			current = uv[1]
			#set visited
			for v in range(self.V):
				if visited[v] == 1:
					continue
				elif self.graph[current][v] > 0:
					self.look_ahead_dijkstra_relax(current,v)
		return 0


	#The key step of the MCOP algoritm
	def look_ahead_dijkstra_relax(self,u,v):
		tmp = 0
		self.c[tmp] = self.c[u] + self.graph[u][v]
		self.g[tmp] = (self.G[u] + self.cost_graph[u][v] + self.R[v])/self.bandwidth_limit
		self.G[tmp] = self.G[u] + self.cost_graph[u][v]
		self.R[tmp] = self.R[v]
		if (self.prefer_the_best(tmp,v) == tmp):
			self.c[v] = self.c[tmp]
			self.g[v] = self.g[tmp]
			self.G[v] = self.G[tmp]
			self.pi_g[v] = u
		return


	def prefer_the_best(self, a, b):
		if self.c[a] < self.c[b] and self.G[a] + self.R[a] < self.bandwidth_limit:
			return a
		if self.c[a] > self.c[b] and self.G[a] + self.R[a] < self.bandwidth_limit:
			return b
		if self.g[a] < self.g[b]:
			return a
		return b










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
	g.cost_graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
			[4, 0, 8, 0, 0, 0, 0, 11, 0],
			[0, 8, 0, 7, 0, 4, 0, 0, 2],
			[0, 0, 7, 0, 9, 14, 0, 0, 0],
			[0, 0, 0, 9, 0, 10, 0, 0, 0],
			[0, 0, 4, 14, 10, 0, 2, 0, 0],
			[0, 0, 0, 0, 0, 2, 0, 1, 6],
			[8, 11, 0, 0, 0, 0, 1, 0, 7],
			[0, 0, 2, 0, 0, 0, 6, 7, 0]
			]
	g.bandwidth_limit = 10000
	g.h_mcop(0,5)

