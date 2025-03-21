# NonTrivialCMGraph.py
# Marcio Gameiro
# 2023-05-25
# MIT LICENSE

import pychomp
import pydot

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

def NonTrivialCMGraphPyChomP(morse_graph):
    # Make a pyChomP graph from morse_graph
    G = pychomp.DirectedAcyclicGraph()
    for v in morse_graph.vertices():
        G.add_vertex(v)
    for v in morse_graph.vertices():
        for w in morse_graph.adjacencies(v):
            G.add_edge(v, w)
    # Space dimension
    v = list(morse_graph.vertices())[0]
    label = morse_graph.vertex_label(v)
    D = len(label.split(','))
    # Check if a Morse node is trivial
    trivial = lambda v: morse_graph.vertex_label(v) == str((0,)*D)
    # Nontrivial Morse nodes
    non_trivial_nodes = [v for v in morse_graph.vertices() if not trivial(v)]
    # Construct nontrivial Conley Morse graph
    non_trivial_cmg = pychomp.DirectedAcyclicGraph()
    for v in non_trivial_nodes:
        label = morse_graph.vertex_label(v)
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

def graph_from_dotfile(dot_fname):
    # Read graphs from dot file
    dot_graphs = pydot.graph_from_dot_file(dot_fname)
    # Assuming there is only one graph
    dot_graph = dot_graphs[0]
    # Create a pyChomP graph from dot_graph
    G = pychomp.DirectedAcyclicGraph()
    for node in dot_graph.get_nodes():
        name = node.get_name()
        label = node.get_label()
        if label == None:
            continue
        label = label.split(':')[1][1:-1]
        G.add_vertex(int(name), label=label)
    for edge in dot_graph.get_edges():
        u = edge.get_source()
        v = edge.get_destination()
        G.add_edge(int(u), int(v))
    return G
