### PlotGraph.py
### MIT LICENSE 2025 Marcio Gameiro

import graphviz

def PlotGraph(graph):
    """Plot graph using graphviz"""
    # Set default values for graphviz
    shape = 'ellipse'
    margin = '0.0, 0.04'
    # Make graphviz string
    gv = 'digraph {\n'
    for v in graph.vertices():
        vertex_label = str(v) + ' : ' + graph.vertex_label(v)
        gv += str(v) + ' [label="' + vertex_label + '"' + (
            ', shape=' + shape + ', style=filled, fillcolor="white", margin="' + margin + '"];\n')
    # Set the graph edges
    for u in graph.vertices():
        for v in graph.adjacencies(u):
            gv += str(u) + ' -> ' + str(v) + ';\n'
    gv += '}\n' # Close bracket
    # Return graphviz render
    return graphviz.Source(gv)
