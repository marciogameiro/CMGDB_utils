### AdjacencyMatrix.py
### MIT LICENSE 2026 Marcio Gameiro

import CMGDB_utils
import DSGRN
import CMGDB

import matplotlib.pyplot as plt
import matplotlib
from collections import defaultdict
import numpy as np
import scipy

def point_counts(X, adjacencies, cubical_complex):
    """Count how many points of X in each cube"""
    # Default counting dictionary
    counts = defaultdict(int)
    # One point per box if X is empty
    if not X:
        tot_num_pts = len(adjacencies)
        return counts, tot_num_pts
    for x in X:
        # Find box containing x
        x_l_bounds = [xi for xi in x]
        x_u_bounds = [xi for xi in x]
        x_box = x_l_bounds + x_u_bounds
        # Get box containing x
        x_box_inds = cubical_complex.grid_cover(x_box)
        # Check to make sure this is true
        # assert len(x_box_inds) <= 1:
        for v in x_box_inds:
            if v in adjacencies:
                counts[v] += 1
    # Number of boxes with no points
    num_empty_boxes = len(adjacencies) - len(counts)
    # Number of points inside adjacencies boxes
    counts_sum = sum(counts.values())
    # Total number of points to compute weight
    # Count one point per empty box (if any)
    tot_num_pts = counts_sum + num_empty_boxes
    return counts, tot_num_pts

def weighted_adjacency_matrix(cubical_complex, model):
    """Compute digraph and weighted adjacency matrix"""
    # Define the digraph (multi-valued map)
    num_verts = cubical_complex.size()
    digraph = DSGRN.Digraph()
    digraph.resize(num_verts)
    # Compute the digraph and matrix
    W = {} # Adjacency matrix as a dict
    for u in range(num_verts):
        # Get min and max vertices of cube
        min_vert = cubical_complex.min_vertex(u)
        max_vert = cubical_complex.max_vertex(u)
        # Define rectangle and evaluate F
        box = min_vert + max_vert
        F_box, X = model.F(box)
        # Get list of adjacencies (cubes covering F_box)
        adjacencies = cubical_complex.grid_cover(F_box, padding=model.padding)
        # Count points in each adjacencies boxes
        counts, tot_num_pts = point_counts(X, adjacencies, cubical_complex)
        # Add edges to digraph and matrix
        for v in adjacencies:
            digraph.add_edge(u, v)
            # Number of points in v (or 1 if zero)
            n_pts = counts[v] if counts[v] else 1
            W[(u, v)] = n_pts / tot_num_pts
    return digraph, W

def morse_graph_adjacency_matrix(model, acyclic_check=True):
    """Compute Morse graph and weighted adjacency matrix"""
    # Construct the cubical complex
    cubical_complex = CMGDB_utils.CubicalGrid(model.lower_bounds, model.upper_bounds, model.grid_size)
    # Compute the multi-valued map and adjacency matrix
    digraph, W = weighted_adjacency_matrix(cubical_complex, model)
    # Compute Morse decomposition
    morse_decomp = DSGRN.MorseDecomposition(digraph)
    # Get number of Morse graph nodes
    num_nodes = morse_decomp.poset().size()
    # Create an indexing of the Morse graph vertices
    vertex_mapping = {v: num_nodes - 1 - v for v in range(num_nodes)}
    # Construct the Morse graph and add edges
    morse_graph = CMGDB_utils.DirectedAcyclicGraph()
    for v in range(num_nodes):
        # Get corresponding Morse node
        morse_node = vertex_mapping[v]
        morse_set = set(morse_decomp.morseset(v))
        # S subset F(S) for a Morse set. So X = F(S)
        # X_cells = set(morse_set)
        X_cells = set()
        for u in morse_set:
            X_cells.update(digraph.adjacencies(u))
        # Define multivalued map F restricted to X
        F = {u: [w for w in digraph.adjacencies(u) if w in X_cells] for u in X_cells}
        A = list(X_cells - morse_set)
        X = list(X_cells)
        conley_index = CMGDB.ComputeConleyIndex(X, A, model.grid_size, model.periodic, F, acyclic_check)
        conley_index_str = '(' + ', '.join(conley_index) + ')' if conley_index else 'Undefined'
        morse_graph.add_vertex(morse_node, label=conley_index_str)
    for u in range(num_nodes):
        for v in morse_decomp.poset().children(u):
            morse_graph.add_edge(vertex_mapping[u], vertex_mapping[v])
    morse_graph_data = (morse_graph, morse_decomp, vertex_mapping)
    return morse_graph_data, cubical_complex, W

def attractor_eigenvalues(W, morse_graph_data, latt_attractors, att_vert, num_evals=100):
    morse_graph, morse_decomp, vertex_mapping = morse_graph_data
    attractor_cells = {}
    att_vertices = sorted(latt_attractors.vertices())
    for v in att_vertices:
        att_str = latt_attractors.vertex_label(v)
        # Skip trivial attractor
        if att_str == '{ }':
            attractor_cells[v] = set()
            continue
        attractor = [int(v.strip()) for v in att_str[1:-1].split(',')]
        att_cells = set()
        for n in attractor:
            # Get corresponding Morse node
            morse_node = vertex_mapping[n]
            # Get cells in Morse decomposition node
            morse_set = morse_decomp.morseset(morse_node)
            att_cells.update(morse_set)
        attractor_cells[v] = att_cells
    # Get matrix corresponding to attractor
    att_cells = attractor_cells[att_vert]
    n_att_cells = len(att_cells)
    print('Number of cells in attractor:', n_att_cells)
    att_cell_index = {val: index for index, val in enumerate(att_cells)}
    M = np.zeros((n_att_cells, n_att_cells))
    for (u, v) in W:
        if (u in att_cells) and (v in att_cells):
            i = att_cell_index[u]
            j = att_cell_index[v]
            M[i, j] = W[(u, v)]
    if num_evals >= n_att_cells:
        # Compute all eigenvalues/eigenvecs
        eigen_vals, eigen_vecs = np.linalg.eig(M.T)
    else:
        # Compute only some eigenvalues/eigenvecs
        eigen_vals, eigen_vecs = scipy.sparse.linalg.eigs(M.T, k=num_evals)
    return eigen_vals, eigen_vecs, att_cell_index, M

def eigenvectos_min_attractor(eigen_vals, eigen_vecs, max_att, mg_data, latt_att, att_cell_index, tol=1e-12):
    """Return the minimal attractor containing support of eigenvectors"""
    # Get list of cells on each attractor
    morse_graph, morse_decomp, vertex_mapping = mg_data
    attractor_cells = {}
    # List of attractors below max_att (excluding 0)
    att_vertices = sorted(latt_att.descendants(max_att) - {0})
    # att_vertices = sorted(latt_att.vertices())
    for v in att_vertices:
        att_str = latt_att.vertex_label(v)
        # Skip trivial attractor
        if att_str == '{ }':
            attractor_cells[v] = set()
            continue
        attractor = [int(v.strip()) for v in att_str[1:-1].split(',')]
        att_cells = set()
        for n in attractor:
            # Get corresponding Morse node
            morse_node = vertex_mapping[n]
            # Get cells in Morse decomposition node
            morse_set = morse_decomp.morseset(morse_node)
            att_cells.update(morse_set)
        attractor_cells[v] = att_cells
    # Associate eigenvalues to minimal attractors
    eigen_vecs_att = {}
    for k in range(len(eigen_vals)):
        # Get the k-th eigenvector
        e_vec = eigen_vecs[:, k]
        # Get non-zero entries of the eigenvector
        e_vec_indices = set(np.where(abs(e_vec) > tol)[0])
        # Find minimum attractor containing support of eigenvector
        for v in att_vertices:
            # Get list of row/column indices corresponding to attractor cells
            att_indices = set([att_cell_index[c] for c in attractor_cells[v]])
            # Associate the first attractor found (should be min)
            if e_vec_indices.issubset(att_indices):
                eigen_vecs_att[k] = v
                break # Exit inner for loop
    return eigen_vecs_att

def plot_eigenvalues(e_vals, e_vecs, max_att, mg_data, latt_att, att_cell_index, cmap=None, clist=None, tol=1e-12):
    """Plot eigenvalues colored according to minimum attractor"""
    # List of markers for scatter plot
    markers = ['s', 'D', 'o', '*', 'P', 'v', '^', '<', '>', 'p', 'X', 'h', 'H', '1', '2', '3', '4']
    # Default color list
    default_clist = ['#1f77b4', '#e6550d', '#31a354', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                     '#bcbd22', '#80b1d3', '#ffffb3', '#fccde5', '#b3de69', '#fdae6b', '#6a3d9a', '#c49c94',
                     '#fb8072', '#dbdb8d', '#bc80bd', '#ffed6f', '#637939', '#c5b0d5', '#636363', '#c7c7c7',
                     '#8dd3c7', '#b15928', '#e8cb32', '#9e9ac8', '#74c476', '#ff7f0e', '#9edae5', '#90d743',
                     '#e7969c', '#17becf', '#7b4173', '#8ca252', '#ad494a', '#8c6d31', '#a55194', '#00cc49']
    # # Default colormap
    # default_cmap = matplotlib.cm.tab20
    # Number of vertices
    num_verts = len(latt_att.vertices())
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
    # Get minimum attractor associated to each eigenvector
    e_vecs_att = eigenvectos_min_attractor(e_vals, e_vecs, max_att, mg_data, latt_att, att_cell_index, tol=tol)
    vert_color = lambda v: matplotlib.colors.to_hex(cmap(cmap_norm(v)), keep_alpha=True)
    # colors = [vert_color(e_vecs_att[k]) for k in range(len(e_vals))]
    fig, ax = plt.subplots(figsize=(10, 6))
    # Create a circle patch with center (0, 0) and radius 1
    circle = plt.Circle((0, 0), radius=1, color='black', fill=False)
    # Add the circle to the plot
    ax.add_patch(circle)
    # Plot eigenvalues corresponding to each attractor
    for att in range(max_att + 1):
        clr = vert_color(att)
        m = markers[att]
        e_vals_att = [e_vals[k] for k in range(len(e_vals)) if e_vecs_att[k] == att]
        if e_vals_att:
            ax.scatter(np.real(e_vals_att), np.imag(e_vals_att), c=clr, marker=m, s=45, label=f'Attractor: {att}')
    ax.set_aspect('equal')
    ax.legend(loc='upper left', fontsize='small')
    plt.tight_layout()
    plt.show()
