import numpy as np
from .crossing import Crossing


class TwoPointCrossing(Crossing):

    def __init__(self, gene_length):
        self.gene_index_array = np.arange(gene_length)

    def do_crossing(self, individual1, individual2):
        new_individual1 = individual1.copy()
        new_individual2 = individual2.copy()
        selected_numbers = np.random.choice(self.gene_index_array, size=2, replace=False)
        sorted_numbers = np.sort(selected_numbers)
        point1, point2 = sorted_numbers[0], sorted_numbers[1]
        middle_gene_for_individual1 = new_individual2[point1:point2]
        middle_gene_for_individual2 = new_individual1[point1:point2]
        new_individual1[point1:point2] = middle_gene_for_individual1
        new_individual2[point1:point2] = middle_gene_for_individual2
        return new_individual1, new_individual2
