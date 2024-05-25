import time
import importlib
from .request_conditions.request_condition_base import RequestConditionBase
from data_interfaces.data_store import DataStore


class RequestConditionManager:

    def __init__(self, request_condition_info_dict: dict, data_store: DataStore):
        self.penalty_pal_list_by_level = [1, 5, 10, 20, 100]
        self.request_condition_instance_list, self.name_list \
            = self.get_request_condition_instance_and_name_list(request_condition_info_dict, data_store)

        # 多様性重みパラメーター
        self.higher_request_index = -1
        self.weight_for_diversity = 3

    def get_request_condition_instance_and_name_list(self, request_condition_info_dict, data_store):
        request_condition_instance_list = []
        name_list = []
        for name, request_condition_value in request_condition_info_dict.items():
            file_name = request_condition_value['file_name']
            class_name = request_condition_value['class_name']
            level = request_condition_value['level']
            penalty_par = self.penalty_pal_list_by_level[level-1]
            arg_dict = request_condition_value['arg_dict']
            static_name = 'request_condition_local.request_conditions.'
            module_name = static_name + file_name
            module = importlib.import_module(module_name)
            request_condition_class = getattr(module, class_name)
            request_condition_instance: RequestConditionBase = request_condition_class(data_store, penalty_par, arg_dict)
            request_condition_instance_list.append(request_condition_instance)
            name_list.append(name)

        return request_condition_instance_list, name_list

    def set_higher_request_index(self, index):
        self.higher_request_index = index

    def calc_total_request_penalty(self, new_shift):
        total_penalty = 0
        for i in range(len(self.request_condition_instance_list)):
            penalty = self.request_condition_instance_list[i].calc_penalty(new_shift)
            if i == self.higher_request_index:
                total_penalty += penalty * self.weight_for_diversity
            else:
                total_penalty += penalty

        return total_penalty

    def get_request_condition_num(self):
        return len(self.request_condition_instance_list)

    def measure_individual_request_time(self, shift_list):
        request_len = len(self.request_condition_instance_list)
        request_time_list = [0.0] * request_len
        for request_index in range(len(self.request_condition_instance_list)):
            calc_func = self.request_condition_instance_list[request_index].calc_penalty
            start_time = time.perf_counter()
            for shift in shift_list:
                calc_func(shift)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            request_time_list[request_index] = elapsed_time
        return request_time_list

    def measure_individual_request_average_penalty(self, shift_list):
        request_len = len(self.request_condition_instance_list)
        request_penalty_list = [0.0] * request_len
        for request_index in range(len(self.request_condition_instance_list)):
            calc_func = self.request_condition_instance_list[request_index].calc_penalty
            all_penalty = 0
            for shift in shift_list:
                all_penalty += calc_func(shift)
            request_penalty_list[request_index] = all_penalty/len(shift_list)
        return request_penalty_list
