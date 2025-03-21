### CubicalGrid.py
### MIT LICENSE 2025 Marcio Gameiro

import numpy as np
import itertools
import math

class CubicalGrid:
    def __init__(self, lower_bounds, upper_bounds, grid_size):
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds
        self.grid_size = grid_size
        self.dim = len(self.lower_bounds)
        self.num_cubes = np.prod(self.grid_size)
        self.cube_sizes = [(self.upper_bounds[k] - self.lower_bounds[k]) / self.grid_size[k] for k in range(self.dim)]

    def dimension(self):
        """Return the space dimesnion"""
        return self.dim

    def size(self):
        """Return the number of cubes"""
        return self.num_cubes

    def get_lower_bounds(self):
        """Return the grid lower bounds"""
        return self.lower_bounds

    def get_upper_bounds(self):
        """Return the grid upper bounds"""
        return self.upper_bounds

    def get_grid_size(self):
        """Return the grid size"""
        return self.grid_size

    def get_cube_sizes(self):
        """Return the cube sizes"""
        return self.cube_sizes

    def coordinates(self, index):
        """Return integer coordinates from index"""
        return np.unravel_index(index, self.grid_size, order='F')

    def index(self, coords):
        """Return index from integer coordinates"""
        return np.ravel_multi_index(coords, self.grid_size, order='F')

    def min_vertex(self, index):
        """Return real coordinates of minimum vertex"""
        coords = self.coordinates(index)
        min_vert = [self.lower_bounds[k] + coords[k] * self.cube_sizes[k] for k in range(self.dim)]
        return min_vert

    def max_vertex(self, index):
        """Return real coordinates of maximum vertex"""
        coords = self.coordinates(index)
        max_vert = [self.lower_bounds[k] + (coords[k] + 1) * self.cube_sizes[k] for k in range(self.dim)]
        return max_vert

    def grid_cover(self, box, padding=False):
        """Return"""
        # Get box lower and upper bounds
        box_lower_bounds = box[:self.dim]
        box_upper_bounds = box[self.dim:]
        # Check if box is outside the domain
        if any(box_upper_bounds[k] < self.lower_bounds[k] for k in range(self.dim)):
            return {}
        if any(box_lower_bounds[k] > self.upper_bounds[k] for k in range(self.dim)):
            return {}
        # Get min and max coordinate for each dimension. The math.ceil gives the right
        # coordinate of the left most cube in the cover so we subtract 1 to get the left
        # coordinate. We do it this way to get the correct result in the case of a box
        # with left boundary on top of a boundary of a grid element. The math.floor gives
        # the left coordinate of the right most cube in the cover, which is what we want.
        min_coord = lambda k: math.ceil((box_lower_bounds[k] - self.lower_bounds[k]) / self.cube_sizes[k]) - 1
        max_coord = lambda k: math.floor((box_upper_bounds[k] - self.lower_bounds[k]) / self.cube_sizes[k])
        # Pad by one layer of cubes if requested and make sure coordinates are in [0, grid_size)
        min_coords = [max(min_coord(k) - (1 if padding else 0), 0) for k in range(self.dim)]
        max_coords = [min(max_coord(k) + (1 if padding else 0), self.grid_size[k] - 1) for k in range(self.dim)]
        # Get ranges of coordinates for each dimension
        coord_ranges = [range(min_c, max_c + 1) for min_c, max_c in zip(min_coords, max_coords)]
        # Get set of indices of cubes covering the box
        cover_indices = {self.index(coords) for coords in itertools.product(*coord_ranges)}
        return cover_indices
