import numpy as np
from .crossing import Crossing


class UniformCrossing(Crossing):

    def __init__(self, gene_length):
        self.gene_length = gene_length
        self.bool_array = np.array([True, False])

    def do_crossing(self, individual1, individual2):
        new_individual1 = individual1.copy()
        new_individual2 = individual2.copy()
        swap_mask = np.random.rand(self.gene_length) < 0.5
        temp_genes = np.copy(new_individual1[swap_mask])
        new_individual1[swap_mask] = new_individual2[swap_mask]
        new_individual2[swap_mask] = temp_genes
        return new_individual1, new_individual2
