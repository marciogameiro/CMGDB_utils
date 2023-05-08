# NonTrivialCMGraph.py
# Marcio Gameiro
# 2023-05-08
# MIT LICENSE

import CMGDB
import pychomp2 as pychomp

def NonTrivialCMGraph(morse_graph):
    # Make a pyChomP graph from morse_graph
    G = pychomp.DirectedAcyclicGraph()
    for v in morse_graph.vertices():
        G.add_vertex(v)
    for v in morse_graph.vertices():
        for w in morse_graph.adjacencies(v):
            G.add_edge(v, w)
    # Space dimension
    D = len(morse_graph.annotations(0))
    # Check if a Morse node is trivial
    trivial = lambda v: morse_graph.annotations(v) == ['0']*D
    # Nontrivial Morse nodes
    non_trivial_nodes = [v for v in morse_graph.vertices() if not trivial(v)]
    # Construct nontrivial Conley Morse graph
    non_trivial_cmg = pychomp.DirectedAcyclicGraph()
    for v in non_trivial_nodes:
        label = '(' + ', '.join(morse_graph.annotations(v)) + ')'
        # label = str(v) + ' : (' + ', '.join(morse_graph.annotations(v)) + ')'
        non_trivial_cmg.add_vertex(v, label=label)
    for v in non_trivial_nodes:
        for w in G.descendants(v):
            if (w in non_trivial_nodes) and (w != v):
                non_trivial_cmg.add_edge(v, w)
    # The labels are not preserved in the transitively reduced
    # graph. So need to remove edges from original graph.
    # Get transitively reduced graph and its edges
    G_reduced = non_trivial_cmg.transitive_reduction()
    edges_reduced = G_reduced.edges()
    # Remove transitive reducible edges
    for (v, w) in non_trivial_cmg.edges():
        if (v, w) not in edges_reduced:
            non_trivial_cmg.remove_edge(v, w)
    return non_trivial_cmg
