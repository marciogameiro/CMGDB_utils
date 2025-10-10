### LatticeAttractors.py
### MIT LICENSE 2025 Marcio Gameiro

import pychomp
import functools

def transitive_closure(morse_graph):
    """Compute the transitive closure of Morse graph"""
    # First create a pychomp version of Morse graph
    morse_graph_new = pychomp.DirectedAcyclicGraph()
    for v in morse_graph.vertices():
        # # Handle the case of annotations not present
        # annotations = getattr(morse_graph, 'annotations', [])
        # v_label = str(tuple(annotations(v))) if annotations else morse_graph.vertex_label(v)
        # morse_graph_new.add_vertex(v, label=v_label)
        morse_graph_new.add_vertex(v)
    for v1, v2 in morse_graph.edges():
        morse_graph_new.add_edge(v1, v2)
    # Return the transitive closure of Morse graph
    return morse_graph_new.transitive_closure()

def morse_graph_attractors(morse_graph):
    """Compute all attractors from Morse graph"""
    # Compute the transitive closure of Morse graph
    mg_trans_closure = transitive_closure(morse_graph)
    # Store attractors as a set of frozensets
    attractors = {frozenset()}
    # Find elementary attractors (downsets of a node)
    for v in morse_graph.vertices():
        descendants = mg_trans_closure.adjacencies(v)
        # The down set of v is {v} union with its decendents
        attractors.add(frozenset({v} | descendants))
    # Compute all joins and meets to get all attractors
    found_new_attractor = True
    while found_new_attractor:
        found_new_attractor = False
        new_attractors = set()
        # Compute join and meet of pairs
        for A1 in attractors:
            for A2 in attractors:
                # Compute join (union)
                join = A1 | A2
                if join not in attractors:
                    new_attractors.add(join)
                    found_new_attractor = True
                # Compute meet (intersection)
                meet = A1 & A2
                if meet not in attractors:
                    new_attractors.add(meet)
                    found_new_attractor = True
        # Add new attractors found to the set
        attractors.update(new_attractors)
    return attractors

def lattice_attractors(morse_graph):
    """Compute lattice of attractors from Morse graph"""
    # Compute list of Morse graph attractors
    attractors = morse_graph_attractors(morse_graph)
    # Compute lattice of attractors as an acyclic graph
    lattice_att = pychomp.DirectedAcyclicGraph()
    # Get a sorted list of attractors
    sorted_attractors = sorted([set(A) for A in attractors])
    # Further sort attractor by lattice partial order
    partial_order = lambda A1, A2: 0 if A1 == A2 else (-1 if A1.issubset(A2) else 1)
    sorted_attractors.sort(key=functools.cmp_to_key(partial_order))
    # Create vertices (indexing of the set of attractors)
    vertices = range(len(sorted_attractors))
    for v in vertices:
        A = sorted_attractors[v]
        vertex_label = str(A) if A else '{ }'
        lattice_att.add_vertex(v, label=vertex_label)
    # Add edges corresponding to the partial order
    for v1 in vertices:
        A1 = sorted_attractors[v1]
        for v2 in vertices:
            A2 = sorted_attractors[v2]
            # Add edge if A1 < A2 (A1 subset A2)
            if A1.issubset(A2) and A1 != A2:
                lattice_att.add_edge(v2, v1)
    return lattice_att.transitive_reduction()
