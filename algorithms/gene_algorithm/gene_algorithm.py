import numpy as np
# import pandas as pd


from algorithms.algorithm_base import AlgorithmBase

from .ga_functions.selections.selection_getter import selection_getter
from .ga_functions.selections.selection import Selection
from .ga_functions.crossings.crossing_getter import crossing_getter
from .ga_functions.crossings.crossing import Crossing
from .ga_functions.mutations.mutation_getter import mutation_getter
from .ga_functions.mutations.mutation import Mutation
from .ga_functions.evolutions.evolution_getter import evolution_getter
from .ga_functions.evolutions.evolution import Evolution

from .ga_functions.gene_to_3d_shift_converter import GeneTo3dShiftConverter
from .ga_functions.function_to_break_limits import FunctionToBreakLimits
from algorithms.conditional_TA.functions.score_stock_depq import ScoreStockDepq


class GeneAlgorithm(AlgorithmBase):

    def __init__(
            self,
            algo_detail,
            data_interface,
            data_store,
            must_condition_manager,
            request_condition_manager,
            check_penalty=True,
            restoration_gen=1,
            action_type='normal',
            recalc_interval=200
    ):
        super().__init__(algo_detail, data_interface, data_store, must_condition_manager, request_condition_manager)

        # gaの基本設定
        self.individual_number = self.algo_detail['individual_number']
        self.generation_number = self.algo_detail['generation_number']
        self.gene_length = self.data_store.total_request_num

        # 今回のgaの特別設定
        self.check_penalty = check_penalty
        self.restoration_gen = restoration_gen

        # 次世代移行のパラメータ
        # 突然変異を少し高かく設定
        self.crossing_probability = 0.85
        self.reproduction_probability = 0.09
        self.mutation_probability = 0.06

        # 進化, 選択, 交叉, 突然変異のインスタンス化
        self.evolution: Evolution = evolution_getter(
            algo_detail['evolution_type'],
            self.crossing_probability,
            self.reproduction_probability,
            self.mutation_probability
        )
        self.selection: Selection = selection_getter(algo_detail['selection_type'], self.individual_number)
        self.crossing: Crossing = crossing_getter(algo_detail['crossing_type'], self.gene_length)
        self.mutation: Mutation = mutation_getter(algo_detail['mutation_type'], self.gene_length,
                                                  m_probability_for_uniform=0.005)

        # その他の初期設定
        gene_to_3d_shift_converter = GeneTo3dShiftConverter(self.data_store)
        self.gene_to_3d_shift_func = gene_to_3d_shift_converter.gene_to_3d_shift
        self.individual_2d_array = np.zeros((self.individual_number, self.gene_length), dtype=int)
        self.recalc_interval = recalc_interval
        # gaにより制約を突破し初期個体群の生成
        self.ga_to_break_limit = FunctionToBreakLimits(
            self.data_interface,
            self.data_store,
            self.limitation_function_manager,
            self.gene_to_3d_shift_func
        )
        if action_type == 'test':
            self.individual_2d_array = self.data_interface.get_test_break_limit_individuals()
            self.ga_to_break_limit.individual_2d_array = self.data_interface.get_test_new_individual_candidates()
            self.ga_to_break_limit.calc_penalty_for_test()
        else:
            self.individual_2d_array = self.ga_to_break_limit.make_individuals_breaking_limits(
                self.individual_number,
                output=True,
                write_file=True,
            )

        self.res_penalty_array = np.zeros(self.individual_number, dtype=int)
        # 制限を守っている個体を判別するための配列
        self.save_limit_bool_array_for_index = np.ones(self.individual_number, dtype=bool)
        # 上位n個の個体を保持しておくための。データ構造
        self.score_stock_depq = ScoreStockDepq(self.gene_length)

        self.index_array = np.arange(self.individual_number)

    def do_computation(self, output=False, write_file=False):
        res_time_list = self.restrictions_func_manager.measure_restrictions_time(
            self.individual_2d_array,
            self.gene_to_3d_shift_func
        )
        print(res_time_list)
        for gen_index in range(self.generation_number):
            if gen_index % self.restoration_gen == 0:
                self.restoration_individuals()
            self.calc_res_penalty_and_stock_data()
            ordered_index_array = np.argsort(self.res_penalty_array)
            self.individual_2d_array = self.evolution.evolve_for_main(
                self.individual_2d_array,
                ordered_index_array,
                self.selection.get_probability_array(),
                self.crossing.do_crossing,
                self.mutation.do_mutation,
            )
            self.change_save_limit_bool_array()
            if output:
                min_penalty = np.min(self.res_penalty_array)
                no_vio_num = np.sum(self.save_limit_bool_array_for_index)
                print(f'世代: {gen_index+1}, 最小ペナルティ: {min_penalty}, 生き残り, {no_vio_num}')

            if gen_index + 1 % self.recalc_interval == 0:
                res_average_penalty_list = self.restrictions_func_manager.measure_restrictions_average_penalty(
                    self.individual_2d_array,
                    self.gene_to_3d_shift_func
                )
                print(res_average_penalty_list)

        if write_file:
            self.shift_save_func()

    def do_computation2(self, output=False, write_file=False):
        res_time_list = self.restrictions_func_manager.measure_restrictions_time(
            self.individual_2d_array,
            self.gene_to_3d_shift_func
        )
        print(res_time_list)
        for gen_index in range(self.generation_number):
            self.calc_res_penalty2()
            if (gen_index + 1) % self.recalc_interval == 0:
                res_average_penalty_list = self.restrictions_func_manager.measure_restrictions_average_penalty(
                    self.individual_2d_array,
                    self.gene_to_3d_shift_func
                )
                self.stock_data2()
                print(res_average_penalty_list)

            ordered_index_array = np.argsort(self.res_penalty_array)
            self.individual_2d_array, loop_num = self.evolution.evolve_for_main2(
                self.individual_2d_array,
                ordered_index_array,
                self.selection.get_probability_array(),
                self.crossing.do_crossing,
                self.mutation.do_mutation,
                self.limitation_function_manager.all_judgement,
                self.gene_to_3d_shift_func,
            )
            if output:
                min_penalty = np.min(self.res_penalty_array)
                print(f'世代: {gen_index+1}, ループ回数{loop_num}, 最小ペナルティ: {min_penalty}')

        if write_file:
            self.shift_save_func()

    def change_save_limit_bool_array(self):
        no_vio_index = np.where(self.save_limit_bool_array_for_index)[0]
        for index in no_vio_index:
            new_gene = self.individual_2d_array[index]
            shift = self.gene_to_3d_shift_func(new_gene)
            judgement = self.limitation_function_manager.all_judgement(shift)
            if not judgement:
                self.save_limit_bool_array_for_index[index] = False

    def restoration_individuals(self):
        no_vio_num = np.sum(self.save_limit_bool_array_for_index)
        if no_vio_num < self.individual_number:
            new_2d_array = self.ga_to_break_limit.supply_breaking_limits(self.individual_number - no_vio_num)
            no_vio_index = np.where(self.save_limit_bool_array_for_index)[0]
            self.individual_2d_array = np.vstack((self.individual_2d_array[no_vio_index, :], new_2d_array))
            self.res_penalty_array = np.zeros(self.individual_number, dtype=int)
            self.save_limit_bool_array_for_index = np.ones(self.individual_number, dtype=bool)

    def calc_res_penalty_and_stock_data(self):
        no_vio_index = np.where(self.save_limit_bool_array_for_index)[0]
        for index in no_vio_index:
            new_gene = self.individual_2d_array[index]
            shift = self.gene_to_3d_shift_func(new_gene)
            penalty = self.restrictions_func_manager.calc_res_penalty(shift)
            self.res_penalty_array[index] = penalty
            self.score_stock_depq.push(new_gene, penalty)

    def calc_res_penalty2(self):
        for index in self.index_array:
            new_gene = self.individual_2d_array[index]
            shift = self.gene_to_3d_shift_func(new_gene)
            penalty = self.restrictions_func_manager.calc_res_penalty(shift)
            self.res_penalty_array[index] = penalty

    def stock_data2(self):
        for index in self.index_array:
            new_gene = self.individual_2d_array[index]
            penalty = self.res_penalty_array[index]
            self.score_stock_depq.push(new_gene, penalty)

    def shift_save_func(self):
        column_dict = {}
        column_list = []
        for date_i in range(self.data_store.date_len):
            date = self.data_store.index_to_date_dict[date_i]
            for time_i in range(self.data_store.time_len):
                times = self.data_store.index_to_time_dict[time_i]
                column_list.append(f'{str(date)} [{str(times)}')
                column_dict[(date_i, time_i)] = f'{str(date)} [{str(times)}'

        name_dict = {}
        name_list = []
        for name_i in range(self.data_store.name_len):
            name = self.data_store.index_to_name_dict[name_i]
            name_list.append(name)
            name_dict[name_i] = name
        # df = pd.DataFrame(index=name_list, columns=column_list)
        df = None
        df.index.name = '名前'

        now_index = 0
        while len(self.score_stock_depq) != 0:
            top_gene = self.score_stock_depq.pop()[0]
            top_shift = self.gene_to_3d_shift_func(top_gene)
            for date_i in range(self.data_store.date_len):
                for time_i in range(self.data_store.time_len):
                    for name_i in range(self.data_store.name_len):
                        name = name_dict[name_i]
                        column = column_dict[(date_i, time_i)]
                        df.at[name, column] = top_shift[date_i, time_i, name_i]
            self.data_interface.set_top_score_individuals(df, now_index)
            now_index += 1


