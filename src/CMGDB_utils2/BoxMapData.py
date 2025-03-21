### BoxMapData.py
### MIT LICENSE 2025 Marcio Gameiro

# TODO: 1) Use a KD-Tree or a grid to make it more efficient to find the points inside a rectangle
#       2) Unify the names rect and box (rename everything as box)

import numpy as np

class BoxMapData:
    """Define a box map from datasets X and Y, where the points in Y are the images of
       the points in X. Given an input rectangle rect, compute a (list of) rectangle(s)
       f_rect containing the points in Y which are image of the points in X inside of
       rect. If there are no X points in rect the result depends on the flag map_empty:
       If map_empty is 'outside' return a rectangle outiside the domain, if map_empty
       is 'terminate' raise an exception, and if map_empty is 'interp' use a form of
       interpolation to compute the image."""

    def __init__(self, X, Y, map_empty='interp', multi_box=False, box_size=None, box_size_factor=1.0,
                 lower_bounds=None, upper_bounds=None, domain_padding=False, padding=False):
        if map_empty not in ['interp', 'outside', 'terminate']:
            raise ValueError("Invalid value for map_empty. Allowed values are: 'interp', 'outside', or 'terminate'")
        if map_empty == 'outside' and (lower_bounds is None or upper_bounds is None):
            raise ValueError("The bounds lower_bounds and upper_bounds must be provided if map_empty is 'outside'")
        self.X = np.array(X)
        self.Y = np.array(Y)
        self.map_empty = map_empty
        self.multi_box = multi_box
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds
        self.domain_padding = domain_padding
        self.padding = padding
        # num_pts, dim = self.X.shape
        self.dim = self.X.shape[1]
        # Set box_size for MultiBox map
        self.box_size = box_size
        if not (box_size == None or isinstance(box_size, list)):
            # Transform into a list
            self.box_size = [box_size] * self.dim
        # Factor for default box_size
        self.box_size_factor = box_size_factor

    def __call__(self, rect):
        return self.compute(rect)

    def map_points(self, rect):
        """Return the points in Y which are image of the points in X inside of rect."""
        l_bounds = rect[:self.dim]
        u_bounds = rect[self.dim:]
        # Get index mask for the points in X inside rect
        index_mask = np.all((self.X >= l_bounds) & (self.X <= u_bounds), axis=1)
        # Get the corresponding points in Y
        Y_rect = self.Y[index_mask]
        return Y_rect

    def interpolate(self, rect):
        """Compute the image of the empty rectangle rect using interpolation.
           Double the size of the rectangle until there are X points inside
           and return a rectangle with the corresponding points in Y."""
        Y_rect = self.map_points(rect)
        if Y_rect.size > 0:
            return Y_rect
        l_bounds = rect[:self.dim]
        u_bounds = rect[self.dim:]
        # Double rectangle size until nonempty
        while Y_rect.size == 0:
            l_bounds_new = [l_b - (u_b - l_b) / 2 for l_b, u_b in zip(l_bounds, u_bounds)]
            u_bounds_new = [u_b + (u_b - l_b) / 2 for l_b, u_b in zip(l_bounds, u_bounds)]
            l_bounds, u_bounds = l_bounds_new, u_bounds_new
            rect_new = l_bounds_new + u_bounds_new
            Y_rect = self.map_points(rect_new)
        return Y_rect

    def compute(self, rect):
        """Compute a rectangle containing the images of the points inside rect."""
        # Compute points in the image
        Y_rect = self.map_points(rect)
        # Raise an exception if empty image and map_empty is terminate
        if Y_rect.size == 0 and self.map_empty == 'terminate':
            raise ValueError(f'Rectangle {rect} has empty image')
        # Map to a box outside if empty image and map_empty is outside
        if Y_rect.size == 0 and self.map_empty == 'outside':
            # Make a box outside the domain
            f_l_bounds = [b + 1 for b in self.upper_bounds]
            f_u_bounds = [b + 2 for b in self.upper_bounds]
            f_rect = f_l_bounds + f_u_bounds
            return f_rect
        # Pad domain rectangle if flag is set
        if self.domain_padding:
            l_bounds = [l_b - (u_b - l_b) for l_b, u_b in zip(rect[:self.dim], rect[self.dim:])]
            u_bounds = [u_b + (u_b - l_b) for l_b, u_b in zip(rect[:self.dim], rect[self.dim:])]
            rect_new = l_bounds + u_bounds
            Y_rect = self.map_points(rect_new)
        # Interpolate if empty image and map_empty is interp
        if Y_rect.size == 0 and self.map_empty == 'interp':
            Y_rect = self.interpolate(rect)
        if not self.multi_box:
            # Return a single rectangle f_rect
            # Get lower and upper bounds of Y_rect
            Y_l_bounds = list(np.min(Y_rect, axis=0))
            Y_u_bounds = list(np.max(Y_rect, axis=0))
            # Add padding if padding is True
            f_l_bounds = [Y_l_bounds[k] - (rect[k + self.dim] - rect[k] if self.padding else 0) for k in range(self.dim)]
            f_u_bounds = [Y_u_bounds[k] + (rect[k + self.dim] - rect[k] if self.padding else 0) for k in range(self.dim)]
            f_rect = f_l_bounds + f_u_bounds
            return f_rect
        # Return a list of rectangles
        # Make box_size proportional to size of input box if None
        box_size = self.box_size
        if self.box_size == None:
            box_size = [self.box_size_factor * (rect[d + self.dim] - rect[d]) for d in range(self.dim)]
        # Get image boxes lower and upper bounds
        Y_l_bounds = [[y[d] - 0.5 * box_size[d] for d in range(self.dim)] for y in Y_rect]
        Y_u_bounds = [[y[d] + 0.5 * box_size[d] for d in range(self.dim)] for y in Y_rect]
        # Get list of boxes containing image points
        f_box = [Y_lb + Y_up for Y_lb, Y_up in zip(Y_l_bounds, Y_u_bounds)]
        return f_box
