import numpy as np

from must_condition_local.must_condition_manager import MustConditionManager
from data_interfaces.data_store import DataStore
from data_interfaces.data_interface import DataInterface

from algorithms.gene_algorithm.ga_functions.selections.selection_getter import selection_getter
from algorithms.gene_algorithm.ga_functions.selections.selection import Selection
from algorithms.gene_algorithm.ga_functions.crossings.crossing_getter import crossing_getter
from algorithms.gene_algorithm.ga_functions.crossings.crossing import Crossing
from algorithms.gene_algorithm.ga_functions.mutations.mutation_getter import mutation_getter
from algorithms.gene_algorithm.ga_functions.mutations.mutation import Mutation
from algorithms.gene_algorithm.ga_functions.evolutions.evolution_getter import evolution_getter
from algorithms.gene_algorithm.ga_functions.evolutions.evolution import Evolution


class FunctionToBreakLimits:

    def __init__(
        self,
        data_interface,
        data_store,
        limitation_function_manager,
        gene_to_3d_array,
        individual_number=10000,
        evolution_type='darwin',
        selection_type='ranking',
        crossing_type='uniform',
        mutation_type='uniform',
        recalc_interval=500,
    ):
        self.data_store: DataStore = data_store
        self.data_interface: DataInterface = data_interface
        self.limitation_function_manager = limitation_function_manager

        self.individual_number = individual_number
        self.gene_length = self.data_store.total_request_num

        # 次世代移行のパラメータ
        # 突然変異をかなり高かく設定
        self.crossing_probability = 0.8
        self.reproduction_probability = 0.1
        self.mutation_probability = 0.1

        # 進化, 選択, 交叉, 突然変異のインスタンス化
        self.evolution: Evolution = evolution_getter(
            evolution_type,
            self.crossing_probability,
            self.reproduction_probability,
            self.mutation_probability
        )
        self.selection: Selection = selection_getter(selection_type, individual_number, s_parameter_for_ranking=1.95)
        self.crossing: Crossing = crossing_getter(crossing_type, self.gene_length)
        self.mutation: Mutation = mutation_getter(mutation_type, self.gene_length)
        self.ideal_selection_probability \
            = self.data_store.average_shift_demand_num / self.data_store.average_shift_request_num

        self.gene_to_3d_array = gene_to_3d_array
        self.individual_2d_array = np.array([[]])
        self.penalty_array = np.array([])

        self.recalc_interval = recalc_interval

    def make_individuals_breaking_limits(self, need_individual_number, output=False, write_file=False):
        need_individual_2d_array = np.zeros((need_individual_number, self.gene_length), dtype=int)
        now_index = 0

        individual_2d_array = np.zeros((need_individual_number, self.gene_length), dtype=int)
        penalty_array = np.zeros(need_individual_number, dtype=int)
        self.make_new_random_individuals(individual_2d_array, penalty_array, np.arange(need_individual_number))

        flag = True
        loop_count = 0
        while flag:
            need_index_array = np.where(penalty_array == 0)[0]
            for index in need_index_array:
                if np.any(np.all(individual_2d_array[index] == need_individual_2d_array, axis=1)):
                    continue
                need_individual_2d_array[now_index] = individual_2d_array[index]
                now_index += 1
                if now_index == need_individual_number:
                    flag = False
                    if write_file:
                        self.data_interface.set_test_break_limit_individuals(need_individual_2d_array)
                        self.data_interface.set_test_new_individual_candidates(individual_2d_array)
                    break
            self.make_new_random_individuals(individual_2d_array, penalty_array, need_index_array)
            ordered_index_array = np.argsort(penalty_array)
            individual_2d_array = self.evolution.evolve_for_break_limit(
                individual_2d_array,
                ordered_index_array,
                self.selection.get_probability_array(),
                self.crossing.do_crossing,
                self.mutation.do_mutation
            )
            self.calc_penalty(individual_2d_array, penalty_array)
            if output:
                min_penalty = np.min(penalty_array)
                print(f'獲得個体: {now_index}', f'最小ペナルティ: {min_penalty}')

            if loop_count % self.recalc_interval == 0:
                vio_probabilities = self.limitation_function_manager.calc_vio_probabilities(
                    individual_2d_array,
                    self.gene_to_3d_array
                )
                print(vio_probabilities)
            loop_count += 1

        self.individual_2d_array = individual_2d_array
        self.penalty_array = penalty_array
        return need_individual_2d_array

    def supply_breaking_limits(self, need_individual_number):
        need_individual_2d_array = np.zeros((need_individual_number, self.gene_length), dtype=int)
        now_index = 0

        individual_2d_array = self.individual_2d_array
        penalty_array = self.penalty_array

        flag = True
        loop_count = 1
        while flag:
            need_index_array = np.where(penalty_array == 0)[0]
            for index in need_index_array:
                if np.any(np.all(individual_2d_array[index] == need_individual_2d_array, axis=1)):
                    continue
                need_individual_2d_array[now_index] = individual_2d_array[index]
                now_index += 1
                if now_index == need_individual_number:
                    flag = False
                    break
            self.make_new_random_individuals(individual_2d_array, penalty_array, need_index_array)
            ordered_index_array = np.argsort(penalty_array)
            individual_2d_array = self.evolution.evolve_for_break_limit(
                individual_2d_array,
                ordered_index_array,
                self.selection.get_probability_array(),
                self.crossing.do_crossing,
                self.mutation.do_mutation
            )
            self.calc_penalty(individual_2d_array, penalty_array)
            if loop_count % self.recalc_interval == 0:
                vio_probabilities = self.limitation_function_manager.calc_vio_probabilities(
                    individual_2d_array,
                    self.gene_to_3d_array
                )
                print(vio_probabilities)
            loop_count += 1
        self.individual_2d_array = individual_2d_array
        self.penalty_array = penalty_array
        return need_individual_2d_array

    def make_new_random_individuals(self, individual_2d_array, penalty_array, index_array):
        p = self.ideal_selection_probability
        for index in index_array:
            new_gene = np.random.choice([0, 1], size=self.gene_length, p=[1 - p, p])
            individual_2d_array[index] = new_gene
            new_shift = self.gene_to_3d_array(new_gene)
            penalty = self.limitation_function_manager.all_calc_evaluation(new_shift)
            penalty_array[index] = penalty

    def calc_penalty(self, individual_2d_array, penalty_array):
        num, _ = individual_2d_array.shape
        for i in range(num):
            new_gene = individual_2d_array[i]
            shift = self.gene_to_3d_array(new_gene)
            penalty = self.limitation_function_manager.all_calc_evaluation(shift)
            penalty_array[i] = penalty

    def calc_penalty_for_test(self):
        num, _ = self.individual_2d_array.shape
        self.penalty_array = np.zeros(num, dtype=int)
        for i in range(num):
            new_gene = self.individual_2d_array[i]
            shift = self.gene_to_3d_array(new_gene)
            penalty = self.limitation_function_manager.all_calc_evaluation(shift)
            self.penalty_array[i] = penalty
