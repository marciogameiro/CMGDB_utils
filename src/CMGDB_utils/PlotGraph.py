### PlotGraph.py
### MIT LICENSE 2025 Marcio Gameiro

import matplotlib
import graphviz

def PlotGraph(graph, cmap=None, clist=None, shape=None, margin=None):
    """Plot graph using cmap as the colormap or clist as a list of colors to make a colormap"""
    # Default colormap
    default_cmap = matplotlib.cm.tab20
    # Number of vertices
    num_verts = len(graph.vertices())
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
    # Normalization for color map
    cmap_norm = matplotlib.colors.Normalize(vmin=0, vmax=num_verts-1)
    # Get list of minimal nodes (nodes without children)
    minimal_nodes = [v for v in graph.vertices() if len(graph.adjacencies(v)) == 0]
    # Make graphviz string
    gv = 'digraph {\n'
    for v in graph.vertices():
        vertex_label = str(v) + ' : ' + graph.vertex_label(v)
        vertex_color = matplotlib.colors.to_hex(cmap(cmap_norm(v)), keep_alpha=True)
        gv += (str(v) + ' [label="' + vertex_label + '", shape=' + shape +
               ', style=filled, fillcolor="' + vertex_color + '", margin="' + margin + '"];\n')
    # Set rank for minimal nodes
    gv += '{rank=same; '
    for v in minimal_nodes:
        gv += str(v) + ' '
    gv += '}; \n'
    # Set the graph edges
    for u in graph.vertices():
        for v in graph.adjacencies(u):
            gv += str(u) + ' -> ' + str(v) + ';\n'
    gv += '}\n' # Close bracket
    # Return graphviz render
    return graphviz.Source(gv)
