### LatticeAttractors.py
### MIT LICENSE 2025 Marcio Gameiro

import pychomp
import functools
import itertools

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

def morse_graph_attractors_slow(morse_graph):
    """Compute all attractors from Morse graph. This is a slow (direct)
       implementation used to test the faster implementation below."""
    # Compute the transitive closure of Morse graph
    mg_trans_closure = transitive_closure(morse_graph)
    # Store attractors as a set of frozensets
    elementary_attractors = {frozenset()}
    # Find elementary attractors (downsets of a node)
    for v in morse_graph.vertices():
        descendants = mg_trans_closure.adjacencies(v)
        # The down set of v is {v} union with its decendents
        elementary_attractors.add(frozenset({v} | descendants))
    # Generate the full lattice of attractors
    attractors = elementary_attractors.copy()
    # # Compute all joins to get all attractors
    # # Computing the meets is not necessary
    # found_new_attractor = True
    # while found_new_attractor:
    #     found_new_attractor = False
    #     new_attractors = set()
    #     # Compute joins and meets of pairs
    #     for A1 in attractors:
    #         for A2 in attractors:
    #             # Compute join (union)
    #             join = A1 | A2
    #             if join not in attractors:
    #                 new_attractors.add(join)
    #                 found_new_attractor = True
    #             # # Compute meet (intersection)
    #             # meet = A1 & A2
    #             # if meet not in attractors:
    #             #     new_attractors.add(meet)
    #             #     found_new_attractor = True
    #     # Add new attractors found to the set
    #     attractors.update(new_attractors)
    # return attractors
    for k in range(1, len(elementary_attractors)):
        for combo in itertools.combinations(elementary_attractors, k + 1):
            union_of_combo = frozenset().union(*combo)
            attractors.add(union_of_combo)
    return attractors

def comparable(A1, A2):
    """Check if two attractors are comparable"""
    if A1 == A2 or A1.issubset(A2) or A2.issubset(A1):
        return True
    return False

def cmp_func(A1, A2):
    """Compare function for sorting"""
    if len(A1) == len(A2):
        # Compare by lexicographical order
        return 0 if A1 == A2 else (-1 if sorted(A1) < sorted(A2) else 1)
    # Compare by length (includes order relation)
    return -1 if len(A1) < len(A2) else 1

def morse_graph_attractors(morse_graph):
    """Compute all attractors from Morse graph"""
    # Compute the transitive closure of Morse graph
    mg_trans_closure = transitive_closure(morse_graph)
    # Store attractors as a set of frozensets
    elementary_attractors = {frozenset()}
    # Find elementary attractors (downsets of a node)
    for v in morse_graph.vertices():
        descendants = mg_trans_closure.adjacencies(v)
        # The down set of v is {v} union with its decendents
        elementary_attractors.add(frozenset({v} | descendants))
    # Compute all joins to get all attractors
    attractors = elementary_attractors.copy()
    attractors_list = list(elementary_attractors)
    for k1 in range(len(attractors_list)):
        combos = set()
        A1 = attractors_list[k1]
        for k2 in range(k1 + 1, len(attractors_list)):
            A2 = attractors_list[k2]
            if comparable(A1, A2):
                continue
            # New combo if A1 and A2 not comparable
            new_combos = {frozenset({A1, A2})}
            for combo in combos:
                # Add A2 to combo if not comparable with its elements
                if not any(comparable(A2, A3) for A3 in combo):
                    new_combos.add(frozenset({A2} | combo))
            # Update set of combos
            combos.update(new_combos)
        # Add union of each combo obtained from A1 = attractors_list[k1]
        attractors.update({frozenset.union(*combo) for combo in combos})
    return attractors

def lattice_attractors(morse_graph):
    """Compute lattice of attractors from Morse graph"""
    # Compute list of Morse graph attractors
    attractors = morse_graph_attractors(morse_graph)
    # Compute lattice of attractors as an acyclic graph
    lattice_att = pychomp.DirectedAcyclicGraph()
    # Get a sorted list of attractors
    sorted_attractors = sorted(map(set, attractors), key=functools.cmp_to_key(cmp_func))
    # sorted_attractors = sorted([set(A) for A in attractors], key=functools.cmp_to_key(cmp_func))
    # Create vertices (indexing of the set of attractors)
    vertices = range(len(sorted_attractors))
    for v in vertices:
        A = sorted_attractors[v]
        vertex_label = '{' + (str(sorted(A))[1:-1] if A else ' ') + '}'
        # vertex_label = str(set(sorted(A))) if A else '{ }'
        # vertex_label = str(A) if A else '{ }'
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

def lattice_repellers(morse_graph):
    """Compute lattice of repellers from Morse graph"""
    # Get the transpose of the Morse graph
    morse_graph_transpose = pychomp.DirectedAcyclicGraph()
    for v in morse_graph.vertices():
        morse_graph_transpose.add_vertex(v)
    for v1, v2 in morse_graph.edges():
        morse_graph_transpose.add_edge(v2, v1)
    # Compute list attractors for transposed morse graph
    repellers = morse_graph_attractors(morse_graph_transpose)
    # Compute lattice of repellers as an acyclic graph
    lattice_rep = pychomp.DirectedAcyclicGraph()
    # Get a sorted list of repellers
    sorted_repellers = sorted(map(set, repellers), key=functools.cmp_to_key(cmp_func), reverse=True)
    # sorted_repellers = sorted([set(R) for R in repellers], key=functools.cmp_to_key(cmp_func), reverse=True)
    # Create vertices (indexing of the set of repellers)
    vertices = range(len(sorted_repellers))
    for v in vertices:
        R = sorted_repellers[v]
        vertex_label = '{' + (str(sorted(R))[1:-1] if R else ' ') + '}'
        # vertex_label = str(set(sorted(R))) if R else '{ }'
        # vertex_label = str(R) if R else '{ }'
        lattice_rep.add_vertex(v, label=vertex_label)
    # Add edges corresponding to the partial order
    for v1 in vertices:
        R1 = sorted_repellers[v1]
        for v2 in vertices:
            R2 = sorted_repellers[v2]
            # Add edge if R1 < R2 (R2 subset R1)
            if R2.issubset(R1) and R1 != R2:
                lattice_rep.add_edge(v2, v1)
    return lattice_rep.transitive_reduction()
