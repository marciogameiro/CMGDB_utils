### PlotMorseGraph.py
### MIT LICENSE 2025 Marcio Gameiro

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import graphviz

def PlotMorseGraph(mg_data, cmap=None, clist=None, shape=None, margin=None):
    """Plot Morse graph using cmap as the colormap or clist as a list of colors to make a colormap."""
    # Default colormap
    default_cmap = matplotlib.cm.tab20
    # Get the Morse graph from mg_data, which can be a tuple
    # (morse_graph, morse_decomp, vertex_mapping) or just morse_graph
    morse_graph = mg_data[0] if isinstance(mg_data, tuple) else mg_data
    # Number of vertices
    num_verts = len(morse_graph.vertices())
    # Set defaults for unset values
    if clist and cmap == None:
        cmap = matplotlib.colors.ListedColormap(clist[:num_verts], name='clr_list')
    if cmap == None:
        cmap = default_cmap
    if shape == None:
        shape = 'ellipse'
    if margin == None:
        margin = '0.11, 0.055'
    margin = str(margin)

    def vertex_color(v):
        """Return vertex color"""
        clr = matplotlib.colors.to_hex(cmap(cmap_norm(v)), keep_alpha=True)
        return str(clr)

    def vertex_label(v):
        """Return vertex label"""
        graph_v_label = morse_graph.vertex_label(v)
        v_label = str(v) + (' : ' if graph_v_label else '') + graph_v_label
        return v_label

    # Normalization for color map
    cmap_norm = matplotlib.colors.Normalize(vmin=0, vmax=num_verts-1)
    # Get list of attractors (nodes without children)
    attractors = [v for v in morse_graph.vertices() if len(morse_graph.adjacencies(v)) == 0]
    # Make graphviz string
    gv = 'digraph {\n'
    for v in morse_graph.vertices():
        gv += str(v) + ' [label="' + vertex_label(v) + '", shape=' + shape + ', style=filled, fillcolor="' + (
              vertex_color(v) + '", margin="' + margin + '"];\n')
    # Set rank for attractors
    gv += '{rank=same; '
    for v in attractors:
        gv += str(v) + ' '
    gv += '}; \n'
    # Set the graph edges
    for u in morse_graph.vertices():
        for v in morse_graph.adjacencies(u):
            gv += str(u) + ' -> ' + str(v) + ';\n'
    # Close bracket
    gv += '}\n'
    # Return graphviz render
    return graphviz.Source(gv)
