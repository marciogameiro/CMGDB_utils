### SaveMorseSets.py
### MIT LICENSE 2026 Marcio Gameiro

import CMGDB_utils

import csv

def SaveMorseSets(morse_graph_data, cubical_complex, morse_sets_fname):
    # Get Morse graph data components
    morse_graph, morse_decomp, vertex_mapping = morse_graph_data
    # Number of Morse sets
    num_morse_sets = len(morse_graph.vertices())
    with open(morse_sets_fname, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for n in range(num_morse_sets):
            # Get corresponding Morse node
            morse_node = vertex_mapping[n]
            # Get cells in Morse decomposition node
            morse_set = morse_decomp.morseset(n)
            for index in morse_set:
                # Get min and max vertices of cube
                min_vert = cubical_complex.min_vertex(index)
                max_vert = cubical_complex.max_vertex(index)
                # Save Morse set box
                morse_rect = min_vert + max_vert + [morse_node]
                csv_writer.writerow(morse_rect)

def LoadMorseSetFile(morse_sets_fname):
    morse_sets = []
    with open(morse_sets_fname, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
        for row in csv_reader:
            morse_sets.append(row)
    return morse_sets
