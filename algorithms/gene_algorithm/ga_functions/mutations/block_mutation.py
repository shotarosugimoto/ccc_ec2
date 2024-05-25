import numpy as np
from .mutation import Mutation


class BlockMutation(Mutation):

    def __init__(self, gene_length, mutation_size=10):
        self.gene_length = gene_length
        self.gene_index_array = np.arange(gene_length)
        self.mutation_size = mutation_size

    def do_mutation(self, individual):
        new_individual = individual.copy()
        start_index = np.random.choice(self.gene_index_array, size=1)[0]
        if start_index + self.mutation_size >= self.gene_length:
            start_index = self.gene_length - self.mutation_size
        bit = np.random.choice([0, 1])
        for index in range(start_index, start_index + self.mutation_size):
            new_individual[index] = bit
        return new_individual


