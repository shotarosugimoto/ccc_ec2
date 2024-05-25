import numpy as np
from .mutation import Mutation


class UniformMutation(Mutation):

    def __init__(self, gene_length, mutation_probability=0.01):
        self.gene_length = gene_length
        self.mutation_probability = mutation_probability

    def do_mutation(self, individual):
        random_values = np.random.rand(self.gene_length)
        mutation_indices = random_values < self.mutation_probability
        new_individual = individual.copy()
        new_individual[mutation_indices] = 1 - new_individual[mutation_indices]
        return new_individual


