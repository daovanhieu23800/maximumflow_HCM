from collections import deque, defaultdict
from collections import defaultdict

class DinitzMaxFlow:
    def __init__(self, graph, source, sink):
        self.graph = graph
        self.source = source
        self.sink = sink
        self.flow = {}
        self.level = {}
        
    def bfs(self):
        """ Build level graph """
        self.level = {node: -1 for node in self.graph}
        queue = deque([self.source])
        self.level[self.source] = 0
        while queue:
            u = queue.popleft()
            for v, capacity in self.graph[u].items():
                if self.level[v] < 0 and self.flow.get((u, v), 0) < capacity['capacity']:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)
        return self.level[self.sink] >= 0

    def dfs(self, u, bottleneck=float('inf')):
        """ Find blocking flow in the layered graph """
        if u == self.sink:
            return bottleneck
        total_flow = 0
        for v, capacity in self.graph[u].items():
            residual_capacity = capacity['capacity'] - self.flow.get((u, v), 0)
            if self.level[v] == self.level[u] + 1 and residual_capacity > 0:
                min_cap = min(bottleneck, residual_capacity)
                pushed_flow = self.dfs(v, min_cap)
                if pushed_flow > 0:
                    self.flow[(u, v)] = self.flow.get((u, v), 0) + pushed_flow
                    self.flow[(v, u)] = self.flow.get((v, u), 0) - pushed_flow
                    total_flow += pushed_flow
                    bottleneck -= pushed_flow
                    if bottleneck == 0:
                        break
        return total_flow

    def max_flow(self):
        """ Calculate max flow using Dinitz's algorithm """
        max_flow_value = 0
        while self.bfs():
            flow = self.dfs(self.source)
            while flow:
                max_flow_value += flow
                flow = self.dfs(self.source)
        return max_flow_value
class FordFulkersonMaxFlow:
    def __init__(self, graph, source, sink):
        self.graph = graph
        self.source = source
        self.sink = sink
        self.flow = defaultdict(lambda: defaultdict(int))  # Dictionary to track flow on each edge

    def bfs(self):
        """BFS to find an augmenting path with available capacity."""
        parent = {self.source: None}  # Track the path with parent nodes
        queue = deque([self.source])
        
        while queue:
            u = queue.popleft()
            
            for v, capacity in self.graph[u].items():
                residual_capacity = capacity['capacity'] - self.flow[u][v]
                # Only proceed if there's residual capacity and v has not been visited
                if residual_capacity > 0 and v not in parent:
                    parent[v] = u
                    if v == self.sink:  # If we've reached the sink
                        return parent
                    queue.append(v)
        
        return None  # No augmenting path found

    def max_flow(self):
        """Calculate max flow using Ford-Fulkerson with BFS."""
        max_flow_value = 0
        
        while True:
            parent = self.bfs()
            if not parent:  # No more augmenting paths
                break
            
            # Find the maximum flow through the path found
            path_flow = float('Inf')
            s = self.sink
            while s != self.source:
                u = parent[s]
                path_flow = min(path_flow, self.graph[u][s]['capacity'] - self.flow[u][s])
                s = u
            
            # update residual capacities of the edges and reverse edges
            v = self.sink
            while v != self.source:
                u = parent[v]
                self.flow[u][v] += path_flow
                self.flow[v][u] -= path_flow
                v = u
            
            max_flow_value += path_flow  # Add path flow to overall flow
        
        return max_flow_value
        
class EdmondsKarpMaxFlow:
    def __init__(self, graph, source, sink):
        self.graph = graph
        self.source = source
        self.sink = sink
        self.flow = defaultdict(lambda: defaultdict(int))  # Dictionary to store flow along each edge

    def bfs(self, parent):
        """Find path with BFS to check for augmenting paths."""
        visited = {node: False for node in self.graph}
        queue = deque([self.source])
        visited[self.source] = True
        
        while queue:
            u = queue.popleft()
            for v, capacity in self.graph[u].items():
                residual_capacity = capacity['capacity'] - self.flow[u][v]
                if not visited[v] and residual_capacity > 0:  # Only proceed if there is residual capacity
                    parent[v] = u
                    if v == self.sink:
                        return True
                    queue.append(v)
                    visited[v] = True
        return False

    def max_flow(self):
        """Calculate the max flow using Edmonds-Karp."""
        parent = {}
        max_flow_value = 0

        while self.bfs(parent):
            # Find the maximum flow possible on the path found by BFS
            path_flow = float('inf')
            v = self.sink
            while v != self.source:
                u = parent[v]
                path_flow = min(path_flow, self.graph[u][v]['capacity'] - self.flow[u][v])
                v = u

            # Update residual capacities along the path
            v = self.sink
            while v != self.source:
                u = parent[v]
                self.flow[u][v] += path_flow
                self.flow[v][u] -= path_flow
                v = u

            max_flow_value += path_flow

        return max_flow_value
