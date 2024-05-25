import json

from data_interfaces.data_interface import DataInterface


class DataInterfaceFromRemote(DataInterface):

    def __init__(self, data_dict):
        self.data_dict = data_dict

    def get_store_info_dict(self):
        return self.data_dict["store_info_dict"]

    def get_store_shift_request_dict(self):
        return self.data_dict["store_shift_request_dict"]

    def get_long_search_must_condition_info_dict(self):
        return self.data_dict["long_search_must_condition_info_dict"]

    def get_long_search_request_condition_info_dict(self):
        return self.data_dict["long_search_request_condition_info_dict"]

    def get_short_search_must_condition_info_dict(self, shift_id):
        return self.data_dict["short_search_must_condition_info_dict"]

    def get_short_search_request_condition_info_dict(self, shift_id):
        return self.data_dict["short_search_request_condition_info_dict"]

    def make_new_best_shift_file(self, shift_id, shift_dict):
        pass

    def make_new_shift_stock_file(self, shift_dict):
        pass

    def make_new_short_search_condition_files(self, shift_id, must_condition_info_dict, request_condition_info_dict):
        pass

    def change_short_search_conditions(self, shift_id, cmust_condition_info_dict, request_condition_info_dict):
        pass