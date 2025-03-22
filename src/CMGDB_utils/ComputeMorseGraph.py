### ComputeMorseGraph.py
### MIT LICENSE 2025 Marcio Gameiro

import DSGRN
import pychomp
import CMGDB_utils

def compute_multivalued_map(cubical_complex, model):
    """Compute the multi-valued map (digraph)"""
    # Define the digraph (multi-valued map)
    num_verts = cubical_complex.size()
    digraph = DSGRN.Digraph()
    digraph.resize(num_verts)
    # Just assign the edges if multi-valued map is given
    if model.map_type == 'GraphMap' or model.map_type == 'G':
        for u in range(num_verts):
            adjacencies = model.F(u)
            for v in adjacencies:
                digraph.add_edge(u, v)
        return digraph
    # Compute the digraph
    for u in range(num_verts):
        # Get min and max vertices of cube
        min_vert = cubical_complex.min_vertex(u)
        max_vert = cubical_complex.max_vertex(u)
        # Define rectangle and evaluate F
        box = min_vert + max_vert
        F_box = model.F(box)
        if model.map_type == 'BoxMap' or model.map_type == 'B':
            # Get list of adjacencies (cubes covering F_box)
            adjacencies = cubical_complex.grid_cover(F_box, padding=model.padding)
        if model.map_type == 'MultiBoxMap' or model.map_type == 'M':
            # Get list of cubes covering the list of boxes returned by F
            adjacencies = {v for F_b in F_box for v in cubical_complex.grid_cover(F_b, padding=model.padding)}
        # Add edges to digraph
        for v in adjacencies:
            digraph.add_edge(u, v)
    return digraph

def ComputeMorseGraph(model):
    """Compute cubical complex and Morse graph"""
    # Construct the cubical complex
    cubical_complex = CMGDB_utils.CubicalGrid(model.lower_bounds, model.upper_bounds, model.grid_size)
    # Compute the multi-valued map (digraph)
    digraph = compute_multivalued_map(cubical_complex, model)
    # Compute Morse decomposition
    morse_decomp = DSGRN.MorseDecomposition(digraph)
    # Get number of Morse graph nodes
    num_nodes = morse_decomp.poset().size()
    # Create an indexing of the Morse graph vertices
    vertex_mapping = {v: num_nodes - 1 - v for v in range(num_nodes)}
    # Construct the Morse graph and add edges
    morse_graph = pychomp.DirectedAcyclicGraph()
    for u in range(num_nodes):
        morse_graph.add_vertex(vertex_mapping[u])
        for v in morse_decomp.poset().children(u):
            morse_graph.add_edge(vertex_mapping[u], vertex_mapping[v])
    return morse_graph, morse_decomp, vertex_mapping, cubical_complex

