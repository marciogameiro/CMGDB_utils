### PlotLatticeAttractors.py
### MIT LICENSE 2026 Marcio Gameiro

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import graphviz

def PlotLatticeAttractors(lattice_att, cmap=None, clist=None, shape=None, margin=None):
    """Plot lattice (of attractors) using cmap as the colormap or clist as a list of
       colors to make a colormap. Colors the minimal attractor (empty set) light gray."""
    # Default color list
    default_clist = ['#1f77b4', '#e6550d', '#31a354', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                     '#bcbd22', '#80b1d3', '#ffffb3', '#fccde5', '#b3de69', '#fdae6b', '#6a3d9a', '#c49c94',
                     '#fb8072', '#dbdb8d', '#bc80bd', '#ffed6f', '#637939', '#c5b0d5', '#636363', '#c7c7c7',
                     '#8dd3c7', '#b15928', '#e8cb32', '#9e9ac8', '#74c476', '#ff7f0e', '#9edae5', '#90d743',
                     '#e7969c', '#17becf', '#7b4173', '#8ca252', '#ad494a', '#8c6d31', '#a55194', '#00cc49']
    # # Default colormap
    # default_cmap = matplotlib.cm.tab20
    # Number of vertices
    num_verts = len(lattice_att.vertices())
    # Set defaults for unset values
    if shape == None:
        shape = 'ellipse'
    if margin == None:
        margin = '0.11, 0.055'
    margin = str(margin)
    # Set colormap for lattice
    if cmap == None and clist == None:
        clist = default_clist
    if cmap == None:
        cmap = matplotlib.colors.ListedColormap(clist[:num_verts])
    # Get number of colors in the colormap
    try:
        # Colormap is listed colors colormap
        num_colors = len(cmap.colors)
    except:
        num_colors = 0 # Colormap is "continuous"
    if (num_colors > 0) and (num_colors < num_verts):
        # Make colormap cyclic
        cmap_norm = lambda k: k % num_colors
    else:
        # Normalization for color map
        cmap_norm = matplotlib.colors.Normalize(vmin=0, vmax=num_verts-1)
    # Get list of minimal nodes (nodes without children)
    minimal_nodes = [v for v in lattice_att.vertices() if len(lattice_att.adjacencies(v)) == 0]

    def vertex_color(v):
        """Return vertex color"""
        # Light gray for minimal attractor
        if v == 0:
            return '#cdcdcd' # light gray
        # Shift v by 1 to match minimal Morse graph node colors
        clr = matplotlib.colors.to_hex(cmap(cmap_norm(v - 1)), keep_alpha=True)
        return str(clr)

    # Make graphviz string
    gv = 'digraph {\n'
    for v in lattice_att.vertices():
        vert_color = vertex_color(v)
        vert_label = str(v) + ' : ' + lattice_att.vertex_label(v)
        gv += (str(v) + ' [label="' + vert_label + '", shape=' + shape +
               ', style=filled, fillcolor="' + vert_color + '", margin="' + margin + '"];\n')
    # Set rank for minimal nodes
    gv += '{rank=same; '
    for v in minimal_nodes:
        gv += str(v) + ' '
    gv += '}; \n'
    # Set the graph edges
    for u in lattice_att.vertices():
        for v in lattice_att.adjacencies(u):
            gv += str(u) + ' -> ' + str(v) + ';\n'
    # Close bracket
    gv += '}\n'
    # Return graphviz render
    return graphviz.Source(gv)
