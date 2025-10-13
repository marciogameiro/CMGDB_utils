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
