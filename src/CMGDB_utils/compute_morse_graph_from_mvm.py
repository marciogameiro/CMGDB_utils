### compute_morse_graph_from_mvm.py
### MIT LICENSE 2025 Marcio Gameiro

import CMGDB_utils
import collections

def morse_graph_from_edges(edges, grid_size):
    """Compute Morse graph from list of edges"""
    # Define multi-valued map from list of edges
    F = collections.defaultdict(list)
    for v1, v2 in edges:
        F[v1].append(v2)
    # Create normalized domain (just used for plotting)
    dim = len(grid_size)
    lower_bounds = [0.0]*dim
    upper_bounds = [1.0]*dim
    # Define model and compute Conley Morse graph
    model = CMGDB_utils.Model(lower_bounds, upper_bounds, grid_size, F, map_type='G')
    morse_graph_data, cubical_complex = CMGDB_utils.ComputeConleyMorseGraph(model, acyclic_check=True)
    morse_graph = morse_graph_data[0]
    return morse_graph, F

def morse_graph_from_mvm(edges, grid_size):
    """Compute Morse graph from list of edges (mvm)"""
    morse_graph, F = morse_graph_from_edges(edges, grid_size)
    mg_vertices = sorted(morse_graph.vertices())
    mg_labels = [morse_graph.vertex_label(v) for v in mg_vertices]
    mg_edges = morse_graph.edges()
    gv_graph = CMGDB_utils.PlotGraph(morse_graph)
    mg_gv_str = str(gv_graph)
    return mg_vertices, mg_edges, mg_labels, mg_gv_str

def lattice_attractors_from_mvm(edges, grid_size):
    """Compute lattice of attractors from list of edges (mvm)"""
    morse_graph, F = morse_graph_from_edges(edges, grid_size)
    # Compute lattice of attractors
    latt_attractors = CMGDB_utils.lattice_attractors(morse_graph)
    att_vertices = sorted(latt_attractors.vertices())
    att_labels = [latt_attractors.vertex_label(v) for v in att_vertices]
    att_edges = latt_attractors.edges()
    gv_graph = CMGDB_utils.PlotGraph(latt_attractors)
    att_gv_str = str(gv_graph)
    return att_vertices, att_edges, att_labels, att_gv_str

def lattice_repellers_from_mvm(edges, grid_size):
    """Compute lattice of repellers from list of edges (mvm)"""
    morse_graph, F = morse_graph_from_edges(edges, grid_size)
    # Compute lattice of attractors
    latt_repellers = CMGDB_utils.lattice_repellers(morse_graph)
    rep_vertices = sorted(latt_repellers.vertices())
    rep_labels = [latt_repellers.vertex_label(v) for v in rep_vertices]
    rep_edges = latt_repellers.edges()
    gv_graph = CMGDB_utils.PlotGraph(latt_repellers)
    rep_gv_str = str(gv_graph)
    return rep_vertices, rep_edges, rep_labels, rep_gv_str

def morse_graph_from_edges_new(edges, grid_size):
    """Compute Morse graph from list of edges"""
    # Define multi-valued map from list of edges
    F = collections.defaultdict(list)
    for v1, v2 in edges:
        F[v1].append(v2)
    # Create normalized domain (just used for plotting)
    dim = len(grid_size)
    lower_bounds = [0.0]*dim
    upper_bounds = [1.0]*dim
    # Define model and compute Conley Morse graph
    model = CMGDB_utils.Model(lower_bounds, upper_bounds, grid_size, F, map_type='G')
    morse_graph_data, cubical_complex = CMGDB_utils.ComputeConleyMorseGraph(model, acyclic_check=True)
    return morse_graph_data, cubical_complex

def get_attractor(morse_nodes, morse_sets, F):
    """Compute the attractor starting at the Morse nodes"""
    """This is a quick and dirty implementation. Needs to be optimized"""
    # Initialize attractor set as union of Morse sets
    attractor = set().union(*[morse_sets[n] for n in morse_nodes])
    # Create queue of elements to be processed
    process_queue = attractor.copy()
    # Create set of elements already processed
    processed = set()
    # Process the queue
    while process_queue:
        # Get cell from queue
        cell = process_queue.pop()
        if cell in processed:
            continue
        # Get adjacencies of cell
        adjacencies = F[cell]
        # Add to the attractor set
        attractor.update(adjacencies)
        # Add to the queue to process
        process_queue.update(adjacencies)
        # Add cell to set of processed
        processed.add(cell)
    return attractor

def directional_attractors_from_mvm(edges, grid_size, forward=True):
    """Compute list of directional attractors from list of edges (mvm).
       If forward == True compute attractors. If False compute repellers."""
    mg_data, cubical_complex = morse_graph_from_edges_new(edges, grid_size)
    # Get Morse graph data components
    morse_graph, morse_decomp, vertex_mapping = mg_data
    # Get Morse sets
    morse_sets = {}
    for n in range(len(morse_graph.vertices())):
        # Get corresponding Morse node
        node = vertex_mapping[n]
        # Get cells in Morse decomposition node
        morse_sets[node] = morse_decomp.morseset(n)
    # Compute lattice of attractors or repellers
    # Define multi-valued map from list of edges
    F = collections.defaultdict(list)
    if forward:
        # Compute lattice of forward attractors (attractors)
        latt_attractors = CMGDB_utils.lattice_attractors(morse_graph)
        # Compute the multi-valued map F
        for v1, v2 in edges:
            F[v1].append(v2)
    else:
        # Compute lattice of backward attractors (repellers)
        latt_attractors = CMGDB_utils.lattice_repellers(morse_graph)
        # Compute the transpose of the multi-valued map F
        for v1, v2 in edges:
            F[v2].append(v1)
    # Compute list of attractors
    attractors = []
    for v in latt_attractors.vertices():
        # Lattice of attractors vertex label
        label = latt_attractors.vertex_label(v)
        # Check for empty attractor
        if not label.strip('{} '):
            # Add empty attractor
            attractors.append([])
            continue
        # List of Morse nodes that belong to the attractor
        morse_nodes = [int(s.strip()) for s in label.strip('{}').split(',')]
        # Get the attractor and append to list
        attractor = get_attractor(morse_nodes, morse_sets, F)
        attractors.append(attractor)
    return attractors

def attractors_from_mvm(edges, grid_size):
    """Compute list of attractors from list of edges (mvm)"""
    attractors = directional_attractors_from_mvm(edges, grid_size)
    return attractors

def repellers_from_mvm(edges, grid_size):
    """Compute list of repellers from list of edges (mvm)"""
    repellers = directional_attractors_from_mvm(edges, grid_size, forward=False)
    return repellers

