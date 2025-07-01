### Model.py
### MIT LICENSE 2025 Marcio Gameiro

class Model:
    def __init__(self, lower_bounds, upper_bounds, grid_size, F, periodic=None, map_type='BoxMap', padding=False):
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds
        self.grid_size = grid_size
        self.dim = len(self.grid_size)
        self.periodic = [False]*self.dim if periodic == None else periodic
        self.map_type = map_type
        self.padding = padding
        self.F = F
