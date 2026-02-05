### BoxMap.py
### MIT LICENSE 2025 Marcio Gameiro

import numpy as np
import itertools

def CornerPoints(box):
    """Return corner points of a rectangle"""
    dim = int(len(box) / 2)
    # Get list of intervals
    list_intvals = [[box[d], box[d + dim]] for d in range(dim)]
    # Get points in the cartesian product of intervals
    X = [list(u) for u in itertools.product(*list_intvals)]
    return X

def CenterPoint(box):
    """Return center point of a rectangle"""
    dim = int(len(box) / 2)
    x_center = [(box[d] + box[dim + d]) / 2 for d in range(dim)]
    return [x_center]

def SamplePoints(lower_bounds, upper_bounds, num_pts):
    """Return sample points in rectangle"""
    # Sample num_pts in dimension dim, where each
    # component of the sampled points are in the
    # ranges given by lower_bounds and upper_bounds
    dim = len(lower_bounds)
    X = np.random.uniform(lower_bounds, upper_bounds, size=(num_pts, dim))
    return list(X)

def BoxMap(f, box, mode='corners', num_pts=10):
    """Return a rectangle containing the image of the input rectangle"""
    f_box, X = BoxMapSample(f, box, mode=mode, num_pts=num_pts)
    return f_box

def BoxMapSample(f, box, mode='random', num_pts=100):
    """Return a rectangle containing the image of the input rectangle"""
    dim = int(len(box) / 2)
    if mode == 'corners': # Compute at corner points
        X = CornerPoints(box)
    elif mode == 'center': # Compute at center point
        # Return a degenerate rectangle with a single point
        X = CenterPoint(box)
    elif mode == 'random': # Compute at random points
        # Get lower and upper bounds
        lower_bounds = box[:dim]
        upper_bounds = box[dim:]
        X = SamplePoints(lower_bounds, upper_bounds, num_pts)
    else: # Unknown mode
        return [], []
    # Evaluate f at points in X
    Y = [f(x) for x in X]
    # Get lower and upper bounds of Y
    Y_l_bounds = [min([y[d] for y in Y]) for d in range(dim)]
    Y_u_bounds = [max([y[d] for y in Y]) for d in range(dim)]
    f_box = Y_l_bounds + Y_u_bounds
    # Return X if mode = 'random'
    if mode == 'random':
        return f_box, X
    return f_box, []

def MultiBoxMap(f, box, box_size=None, mode='corners', num_pts=10):
    """Return a list of rectangles containing the images of points in the input rectangle"""
    dim = int(len(box) / 2)
    if box_size == None:
        # Box size factor for image boxes
        factor = 1.0 if mode == 'center' else 0.5
        # Make box_size proportional to size of input box
        box_size = [factor * (box[d + dim] - box[d]) for d in range(dim)]
    if not isinstance(box_size, list):
        # Transform into a list
        box_size = [box_size] * dim
    if mode == 'corners': # Compute at corner points
        X = CornerPoints(box)
    elif mode == 'center': # Compute at center point
        # Return a degenerate rectangle with a single point
        X = CenterPoint(box)
    elif mode == 'random': # Compute at random points
        # Get lower and upper bounds
        lower_bounds = box[:dim]
        upper_bounds = box[dim:]
        X = SamplePoints(lower_bounds, upper_bounds, num_pts)
    else: # Unknown mode
        return []
    # Evaluate f at points in X
    Y = [f(x) for x in X]
    # Get image boxes lower and upper bounds
    Y_l_bounds = [[y[d] - 0.5 * box_size[d] for d in range(dim)] for y in Y]
    Y_u_bounds = [[y[d] + 0.5 * box_size[d] for d in range(dim)] for y in Y]
    # Get list of boxes containing image points
    f_box = [Y_lb + Y_up for Y_lb, Y_up in zip(Y_l_bounds, Y_u_bounds)]
    return f_box
