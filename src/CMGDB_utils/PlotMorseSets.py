### PlotMorseSets.py
### MIT LICENSE 2025 Marcio Gameiro

import CMGDB_utils

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def PlotMorseSets(morse_graph_data, cubical_complex=None, morse_nodes=None, proj_dims=None,
                  cmap=None, clist=None, fig_w=8, fig_h=8, xlim=None, ylim=None, axis_labels=True,
                  xlabel='$x$', ylabel='$y$', fontsize=15, fig_fname=None, dpi=300):
    # Default color list
    default_clist = ['#1f77b4', '#e6550d', '#31a354', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                     '#bcbd22', '#80b1d3', '#ffffb3', '#fccde5', '#b3de69', '#fdae6b', '#6a3d9a', '#c49c94',
                     '#fb8072', '#dbdb8d', '#bc80bd', '#ffed6f', '#637939', '#c5b0d5', '#636363', '#c7c7c7',
                     '#8dd3c7', '#b15928', '#e8cb32', '#9e9ac8', '#74c476', '#ff7f0e', '#9edae5', '#90d743',
                     '#e7969c', '#17becf', '#7b4173', '#8ca252', '#ad494a', '#8c6d31', '#a55194', '#00cc49']
    # Get list of Morse sets boxes
    if isinstance(morse_graph_data, str): # String giving file name
        morse_fname = morse_graph_data
        morse_sets = CMGDB_utils.LoadMorseSetFile(morse_fname)
        # Number of Morse sets
        num_morse_sets = max([int(rect[-1]) for rect in morse_sets]) + 1
    else:
        # Get Morse graph data components
        morse_graph, morse_decomp, vertex_mapping = morse_graph_data
        # Number of Morse sets
        num_morse_sets = len(morse_graph.vertices())
        # Get list of Morse sets boxes
        morse_sets = []
        for n in range(num_morse_sets):
            # Get corresponding Morse node
            morse_node = vertex_mapping[n]
            # Get cells in Morse decomposition node
            morse_set = morse_decomp.morseset(n)
            for index in morse_set:
                # Get min and max vertices of cube
                min_vert = cubical_complex.min_vertex(index)
                max_vert = cubical_complex.max_vertex(index)
                # Add Morse set box to list of Morse sets
                morse_sets.append(min_vert + max_vert + [morse_node])
    # Set colormap for Morse sets
    if cmap == None and clist == None:
        clist = default_clist
    if cmap == None:
        cmap = matplotlib.colors.ListedColormap(clist[:num_morse_sets])
    # Get number of colors in the colormap
    try:
        # Colormap is listed colors colormap
        num_colors = len(cmap.colors)
    except:
        num_colors = 0 # Colormap is "continuous"
    if (num_colors > 0) and (num_colors < num_morse_sets):
        # Make colormap cyclic
        cmap_norm = lambda k: k % num_colors
    else:
        # Normalization for color map
        cmap_norm = matplotlib.colors.Normalize(vmin=0, vmax=num_morse_sets-1)
    # # Default colormap
    # default_cmap = matplotlib.cm.tab20
    rect = morse_sets[0]
    assert len(rect) % 2 == 1, "Wrong dimension in Morse sets data"
    dim = int((len(rect) - 1) / 2)
    if dim == 1:
        # Add extra fake dimension to plot
        x0_min, x0_max, node = morse_sets[0]
        x1_min = 0
        x1_max = x0_max - x0_min
        morse_sets = [[x0_min, x1_min, x0_max, x1_max, node] for x0_min, x0_max, node in morse_sets]
        dim = 2
    if morse_nodes == None:
        morse_nodes = range(num_morse_sets)
    if proj_dims == None:
        d1 = 0
        d2 = 1
    else:
        d1 = proj_dims[0]
        d2 = proj_dims[1]
    assert max(d1, d2) < dim, "Wrong projection dimensions"
    # Get min and max x and y values
    if xlim == None:
        x_min = min([rect[d1] for rect in morse_sets if int(rect[-1]) in morse_nodes])
        x_max = max([rect[dim + d1] for rect in morse_sets if int(rect[-1]) in morse_nodes])
        if x_max - x_min < 0.1:
            x_min -= 0.05
            x_max += 0.05
    else:
        x_min = xlim[0]
        x_max = xlim[1]
    if ylim == None:
        y_min = min([rect[d2] for rect in morse_sets if int(rect[-1]) in morse_nodes])
        y_max = max([rect[dim + d2] for rect in morse_sets if int(rect[-1]) in morse_nodes])
        if y_max - y_min < 0.1:
            y_min -= 0.05
            y_max += 0.05
    else:
        y_min = ylim[0]
        y_max = ylim[1]
    x_axis_width = x_max - x_min
    y_axis_height = y_max - y_min
    # Next plot Morse sets
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=100)
    # Set axis limits
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    # The scatter plot in Matplotlib uses a marker size in points**2 units.
    # The relationship between points and pixels is 1 point = dpi/72 pixels,
    # hence multiplying by 72 / fig.dpi gives the number of pixels in the plot.
    # For example using size s=10**2 in a scatter plot will plot the markers
    # with a size of 100 points^2, which changes size according to the dpi.
    # On the other hand using size s=(10*72.0/fig.dpi)**2 will plot markers
    # of size 100 pixels^2, which will be the same size regardless of the dpi.
    # First we get unit size in data units, that is, the size in pixels that
    # correspond to one unit of data (one unit in each axis). The value needs
    # to be squared later for the scatter plot.
    s0_x = (ax.get_window_extent().width / x_axis_width) * (72.0 / fig.dpi)
    s0_y = (ax.get_window_extent().height / y_axis_height) * (72.0 / fig.dpi)
    # Alternative way to set marker size in data units
    # M = ax.transData.get_matrix()
    # x_scale = M[0,0]
    # y_scale = M[1,1]
    for morse_node in morse_nodes:
        morse_set = [rect for rect in morse_sets if int(rect[-1]) == morse_node]
        # Use morse_node as color index for consistency if not plotting all
        clr = matplotlib.colors.to_hex(cmap(cmap_norm(morse_node)), keep_alpha=True)
        X = []; Y = []; S = []
        for rect in morse_set:
            p1 = [rect[d1], rect[d2]]                   # Lower point
            p2 = [rect[dim + d1], rect[dim + d2]]       # Upper point
            p = list((np.array(p1) + np.array(p2)) / 2) # Center point
            s = list((np.array(p2) - np.array(p1)))     # Rect size
            s_x = (s0_x * s[0]) ** 2 # Scatter x-axis size
            s_y = (s0_y * s[1]) ** 2 # Scatter y-axis size
            # Alternative way to set marker size in data units
            # s_x = (x_scale * s[0]) ** 2 # Scatter x-axis size
            # s_y = (y_scale * s[1]) ** 2 # Scatter y-axis size
            X.append(p[0])
            Y.append(p[1])
            # Use max of both sizes
            S.append(max(s_x, s_y))
        ax.scatter(X, Y, s=S, marker='s', c=clr)
        # ax.scatter(X, Y, s=S, marker='s', c=clr, edgecolors=None)
        # ax.scatter(X, Y, s=S, marker='s', c=clr, alpha=0.5)
    # Add axis labels
    if axis_labels:
        ax.set_xlabel(xlabel, fontsize=fontsize)
        ax.set_ylabel(ylabel, fontsize=fontsize)
    # Set tick labels size
    ax.tick_params(labelsize=fontsize)
    # ax.set_aspect('equal')
    # plt.grid(True)
    if fig_fname:
        fig.savefig(fig_fname, dpi=dpi, bbox_inches='tight')
    plt.show()
