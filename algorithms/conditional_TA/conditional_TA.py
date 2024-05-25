import numpy as np

from algorithms.algorithm_base import AlgorithmBase
from algorithms.shift_4d_to_shift_dict import shift_4d_to_shift_dict
from .functions.state_fixed_name_and_date import StateFixedNameAndDate
from .functions.tabu_list import TabuList
from .functions.score_stock_depq import ScoreStockDepq


class ConditionalTA(AlgorithmBase):

    def __init__(
            self,
            algo_detail,
            data_interface,
            data_store,
            must_condition_manager,
            request_condition_manager,
    ):
        super().__init__(algo_detail, data_interface, data_store, must_condition_manager, request_condition_manager)
        self.min_hour = algo_detail['min_hour']
        self.max_hour = algo_detail['max_hour']
        self.iteration_num = algo_detail['iteration_num']

        self.state_dict_list = []
        self.can_change_state_index_array = np.zeros(0, dtype=int)
        self.do_initial_setting()

        self.tabu_list = TabuList(algo_detail['tabu_list_size'])
        self.score_stock_depq = ScoreStockDepq()

        # 最初の一回
        random_index = np.random.choice(self.can_change_state_index_array)
        self.search_local_solution(random_index)
        self.now_state = random_index
        new_shift = self.state_list_to_shift_4d_array()
        self.best_shift = new_shift
        self.best_penalty = self.request_condition_manager.calc_total_request_penalty(new_shift)

        print(self.best_penalty)



    def do_initial_setting(self):
        can_change_state_index_list = []
        index = 0
        for name_index in range(self.data_store.name_len):
            for date_index in range(self.data_store.date_len):
                state = StateFixedNameAndDate(
                    self.min_hour,
                    self.max_hour,
                    self.data_store.shift_request_3d_array_name_date_time[name_index, date_index, :],
                    self.data_store.score_2d_array_by_name_position[name_index, :]
                )
                state_num_len = state.get_state_num_len()
                self.state_dict_list.append({
                    'name_index': name_index,
                    'date_index': date_index,
                    'state': state,
                    'state_num_len': state_num_len
                })

                if not state_num_len == 1:
                    can_change_state_index_list.append(index)
                index += 1
        self.can_change_state_index_array = np.array(can_change_state_index_list, dtype=int)

    def do_computation(self):
        for i in range(self.iteration_num):
            print(self.best_penalty, i)
            random_index = np.random.choice(self.can_change_state_index_array)
            if self.tabu_list.contains((self.now_state, random_index)):
                continue
            self.search_local_solution_half(random_index)
            new_shift = self.state_list_to_shift_4d_array()
            penalty = self.request_condition_manager.calc_total_request_penalty(new_shift)
            self.push_depq(new_shift, penalty)
            if penalty < self.best_penalty:
                self.best_penalty = penalty
                self.best_shift = new_shift
                self.tabu_list.add((self.now_state, random_index))
                self.now_state = random_index

        for state_dict_index in self.can_change_state_index_array:
            print(self.best_penalty)
            self.search_local_solution(state_dict_index)
            new_shift = self.state_list_to_shift_4d_array()
            penalty = self.request_condition_manager.calc_total_request_penalty(new_shift)
            self.push_depq(new_shift, penalty)
            if penalty < self.best_penalty:
                self.best_penalty = penalty
                self.best_shift = new_shift
        shift_list = []
        shift_list.append(new_shift)
        request_penalty_list = self.request_condition_manager.measure_individual_request_average_penalty(shift_list)
        print(request_penalty_list)



    def search_local_solution_half(self, state_dict_index):
        state_dict: dict = self.state_dict_list[state_dict_index]
        min_penalty = float('inf')
        best_index = 0
        for index in range(state_dict['state_num_len']):
            if np.random.rand() < 0.2:
                continue
            state_dict['state'].change_state_by_index(index)
            new_shift = self.state_list_to_shift_4d_array()
            penalty = self.request_condition_manager.calc_total_request_penalty(new_shift)
            if penalty < min_penalty:
                min_penalty = penalty
                best_index = index
        if min_penalty > 1000000:
            print('error')
            return
        state_dict['state'].change_state_by_index(best_index)

    def search_local_solution(self, state_dict_index):
        state_dict: dict = self.state_dict_list[state_dict_index]
        min_penalty = float('inf')
        best_index = 0
        for index in range(state_dict['state_num_len']):
            state_dict['state'].change_state_by_index(index)
            new_shift = self.state_list_to_shift_4d_array()
            penalty = self.request_condition_manager.calc_total_request_penalty(new_shift)
            if penalty < min_penalty:
                min_penalty = penalty
                best_index = index
        state_dict['state'].change_state_by_index(best_index)

    def state_list_to_shift_4d_array(self):
        shift_4d_array = np.zeros((self.data_store.name_len, self.data_store.date_len,
                                   self.data_store.time_len, self.data_store.position_len), dtype=int)
        for state_dict in self.state_dict_list:
            name_index = state_dict['name_index']
            date_index = state_dict['date_index']
            now_state = state_dict['state'].get_now_state()
            shift_4d_array[name_index, date_index, :, :] = now_state

        return shift_4d_array

    def penalty_average_check(self):
        shift_list = []
        for _ in range(1000):
            random_index = np.random.choice(self.can_change_state_index_array)
            state = self.state_dict_list[random_index]['state']
            state.change_random_state()
            shift_list.append(self.state_list_to_shift_4d_array())
        average_penalty = self.request_condition_manager.measure_individual_request_average_penalty(shift_list)
        print(average_penalty)

    def push_depq(self, new_shift, penalty):
        self.score_stock_depq.push(new_shift, penalty)
