### AdjacencyMatrix.py
### MIT LICENSE 2026 Marcio Gameiro

import CMGDB_utils
import DSGRN
import CMGDB

import matplotlib.pyplot as plt
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
        X_cells = set()
        for u in morse_set:
            X_cells.update(digraph.adjacencies(u))
        F = {u: digraph.adjacencies(u) for u in X_cells}
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
    return eigen_vals, eigen_vecs, M

def plot_eigenvalues(eigs_complex, clr='b'):
    fig, ax = plt.subplots()
    # Create a circle patch with center (0, 0) and radius 1
    circle = plt.Circle((0, 0), radius=1, color='black', fill=False)
    # Add the circle to the plot
    ax.add_patch(circle)
    ax.plot(np.real(eigs_complex), np.imag(eigs_complex), 'o', color=clr)
    ax.set_aspect('equal', adjustable='datalim')
    plt.show()
