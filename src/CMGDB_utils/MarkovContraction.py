from collections import defaultdict
import numpy as np

def average_rows_inplace(W, rows):
    rows_set = set(rows)
    target = rows[0]
    k = len(rows)

    col_sums = defaultdict(float)
    cols = set()
    to_delete = []

    # One pass: accumulate sums, and mark non-target entries for deletion
    for (i, j), v in W.items():
        if i in rows_set:
            col_sums[j] += v
            cols.add(j)
            if i != target:
                to_delete.append((i, j))

    # Delete only existing keys we know are present
    for key in to_delete:
        del W[key]

    inv_k = 1.0 / k
    for j in cols:
        avg = col_sums[j] * inv_k
        if avg != 0:
            W[(target, j)] = avg
        else:
            W.pop((target, j), None)


def add_cols_inplace(W, cols):
    cols_set = set(cols)
    target = cols[0]

    row_sums = defaultdict(float)
    rows = set()
    to_delete = []

    # One pass: accumulate sums, and mark non-target entries for deletion
    for (i, j), v in W.items():
        if j in cols_set:
            row_sums[i] += v
            rows.add(i)
            if j != target:
                to_delete.append((i, j))

    for key in to_delete:
        del W[key]

    for i in rows:
        s = row_sums[i]
        if s != 0:
            W[(i, target)] = s
        else:
            W.pop((i, target), None)



def contract_markov_matrix(W, indices):
    average_rows_inplace(W, indices)
    add_cols_inplace(W, indices)

def morse_set_self_weights(morse_decomp, W):
    W = W.copy()
    num_nodes = morse_decomp.poset().size()
    self_weights = np.zeros(num_nodes) # collect the diagonal elements/self weights of the contracted matrix
    for i in range(num_nodes):
        # contract
        morse_set_boxes = morse_decomp.morseset(i)
        contract_markov_matrix(W, morse_set_boxes)

        # get self edge
        index_box = morse_set_boxes[0]
        self_weights[i] = W[(index_box, np.int64(index_box))]
    return self_weights, W