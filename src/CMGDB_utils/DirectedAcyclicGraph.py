### DirectedAcyclicGraph.py
### MIT LICENSE 2025 Marcio Gameiro

import copy

class DirectedAcyclicGraph:
    """Represents a directed acyclic graph"""

    def __init__(self):
        """Initialize an empty graph object"""
        self.vertices_ = set()
        self.adjacency_lists_ = {}
        self.vertex_labels_ = {}
        self.edge_labels_ = {}

    def add_vertex(self, v, label=''):
        """Add the vertex v to the graph and associate a label if one is given"""
        if v in self.vertices_: return
        self.vertices_.add(v)
        self.adjacency_lists_[v] = set()
        self.vertex_labels_[v] = label
        self.edge_labels_[v] = {}

    def add_edge(self, u, v, label=''):
        """Add the edge u -> v to the graph and associate a label if one is given"""
        self.add_vertex(u)
        self.add_vertex(v)
        self.adjacency_lists_[u].add(v)
        self.edge_labels_[u][v] = label

    def remove_edge(self, u, v):
        """Remove the edge u -> v from the graph"""
        self.adjacency_lists_[u].discard(v)
        self.edge_labels_[u].pop(v, None)

    def vertex_label(self, v):
        """Return the label on the vertex v"""
        return self.vertex_labels_[v]

    def get_vertex_from_label(self, label):
        """Return the vertex v with label 'label'. Error if non-unique"""
        vertices = [v for v in self.vertices_ if self.vertex_label(v) == label]
        N = len(vertices)
        if N == 1:
            return vertices[0]
        elif N==0:
            return None
        elif N>1:
            raise ValueError("Non-unique vertex labels.")

    def edge_label(self, u, v):
        """Return the label on the edge u -> v"""
        return self.edge_labels_[u][v]

    def vertices(self):
        """Return the set of vertices in the graph"""
        return self.vertices_

    def edges(self):
        """Return a complete list of directed edges (u,v) in the graph"""
        return [(u,v) for u in self.vertices() for v in self.adjacencies(u)]

    def adjacencies(self, v):
        """Return the set of adjacencies of v, i.e. { u : v -> u }"""
        return self.adjacency_lists_[v]

    def clone(self):
        """Return a copy of this graph"""
        return copy.deepcopy(self)

    def transpose(self):
        """Return a new graph with edge direction reversed"""
        G = DirectedAcyclicGraph ()
        for v in self.vertices(): G.add_vertex(v,self.vertex_label(v))
        for (u,v) in self.edges(): G.add_edge(v,u,self.edge_label(u,v))
        return G

    def descendants(self, v):
        """Find vertices reachable from from v"""
        reachable = set([v])
        workstack = [v]
        while workstack:
            u = workstack.pop()
            for w in self.adjacencies(u):
                if w not in reachable:
                    workstack.append(w)
                    reachable.add(w)
        return reachable
