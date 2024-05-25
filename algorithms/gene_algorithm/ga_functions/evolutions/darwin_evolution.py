import numpy as np
from .evolution import Evolution


class DarwinEvolution(Evolution):

    def __init__(self, crossing_probability=0.9, reproduction_probability=0.05, mutation_probability=0.05):
        self.crossing_probability = crossing_probability
        self.reproduction_probability = reproduction_probability
        self.mutation_probability = mutation_probability

    def evolve_for_main(
            self,
            individual_2d_array,
            ordered_index_array,
            probability_array,
            do_crossing,
            do_mutation,
    ):
        individual_number, gene_length = individual_2d_array.shape
        new_individual_2d_array = np.zeros((individual_number, gene_length), dtype=int)
        now_index = 0

        while not now_index == individual_number:
            random_probability = np.random.rand()
            if self.crossing_probability > random_probability:
                selected_index = np.random.choice(ordered_index_array, size=2, p=probability_array, replace=False)
                index1, index2 = selected_index[0], selected_index[1]
                individual1, individual2 = do_crossing(individual_2d_array[index1], individual_2d_array[index2])
                new_individual_2d_array[now_index] = individual1
                now_index += 1
                if now_index == individual_number:
                    break
                new_individual_2d_array[now_index] = individual2
                now_index += 1
            elif random_probability - self.crossing_probability > self.reproduction_probability:
                selected_index = np.random.choice(ordered_index_array, size=1, p=probability_array)
                index1 = selected_index[0]
                new_individual_2d_array[now_index] = individual_2d_array[index1]
                now_index += 1
            else:
                selected_index = np.random.choice(ordered_index_array, size=1, p=probability_array)
                index1 = selected_index[0]
                individual = do_mutation(individual_2d_array[index1])
                new_individual_2d_array[now_index] = individual
                now_index += 1
        return new_individual_2d_array

    def evolve_for_main2(
            self,
            individual_2d_array,
            ordered_index_array,
            probability_array,
            do_crossing,
            do_mutation,
            les_check_func,
            gene_to_3d
    ):
        individual_number, gene_length = individual_2d_array.shape
        new_individual_2d_array = np.zeros((individual_number, gene_length), dtype=int)
        now_index = 0
        loop_num = 0
        while not now_index == individual_number:

            random_probability = np.random.rand()
            if self.crossing_probability > random_probability:
                selected_index = np.random.choice(ordered_index_array, size=2, p=probability_array, replace=False)
                index1, index2 = selected_index[0], selected_index[1]
                individual1, individual2 = do_crossing(individual_2d_array[index1], individual_2d_array[index2])
                if les_check_func(gene_to_3d(individual1)):
                    new_individual_2d_array[now_index] = individual1
                    now_index += 1
                    if now_index == individual_number:
                        break
                if les_check_func(gene_to_3d(individual2)):
                    new_individual_2d_array[now_index] = individual2
                    now_index += 1
            elif random_probability - self.crossing_probability > self.reproduction_probability:
                selected_index = np.random.choice(ordered_index_array, size=1, p=probability_array)
                index1 = selected_index[0]
                if les_check_func(gene_to_3d(individual_2d_array[index1])):
                    new_individual_2d_array[now_index] = individual_2d_array[index1]
                    now_index += 1
            else:
                index = np.random.choice(ordered_index_array)
                individual = do_mutation(individual_2d_array[index])
                if les_check_func(gene_to_3d(individual)):
                    new_individual_2d_array[now_index] = individual
                    now_index += 1
            loop_num += 1

        return new_individual_2d_array, loop_num

    def evolve_for_break_limit(
            self,
            individual_2d_array,
            ordered_index_array,
            probability_array,
            do_crossing,
            do_mutation,
            must_number=15,
        ):
        individual_number, gene_length = individual_2d_array.shape
        new_individual_2d_array = np.zeros((individual_number, gene_length), dtype=int)
        now_index = 0

        for _ in range(must_number):
            new_individual_2d_array[now_index] = individual_2d_array[ordered_index_array[now_index]]
            now_index += 1

        while not now_index == individual_number:
            random_probability = np.random.rand()
            if self.crossing_probability > random_probability:
                selected_index = np.random.choice(ordered_index_array, size=2, p=probability_array, replace=False)
                index1, index2 = selected_index[0], selected_index[1]
                individual1, individual2 = do_crossing(individual_2d_array[index1], individual_2d_array[index2])
                new_individual_2d_array[now_index] = individual1
                now_index += 1
                if now_index == individual_number:
                    break
                new_individual_2d_array[now_index] = individual2
                now_index += 1
            elif random_probability - self.crossing_probability > self.reproduction_probability:
                selected_index = np.random.choice(ordered_index_array, size=1, p=probability_array)
                index1 = selected_index[0]
                new_individual_2d_array[now_index] = individual_2d_array[index1]
                now_index += 1
            else:
                index = np.random.choice(ordered_index_array)
                individual = do_mutation(individual_2d_array[index])
                new_individual_2d_array[now_index] = individual
                now_index += 1
        return new_individual_2d_array
