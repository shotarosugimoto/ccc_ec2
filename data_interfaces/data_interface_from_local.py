import json

from data_interfaces.data_path_manager import DataPathManager
from data_interfaces.data_interface import DataInterface


class DataInterfaceFromLocal(DataInterface):

    def __init__(self):
        self.data_path_manager: DataPathManager = DataPathManager()

    def get_store_info_dict(self):
        store_info_path = self.data_path_manager.get_store_info_path()
        with open(store_info_path, 'r', encoding='utf-8') as file:
            store_info_dict = json.load(file)
        return store_info_dict

    def get_store_shift_request_dict(self):
        store_shift_request_path = self.data_path_manager.get_store_shift_request_path()
        with open(store_shift_request_path, 'r', encoding='utf-8') as file:
            store_shift_request_dict = json.load(file)
        return store_shift_request_dict

    def get_long_search_must_condition_info_dict(self):
        long_search_must_condition_path = self.data_path_manager.get_long_search_must_condition_path()
        with open(long_search_must_condition_path, 'r', encoding='utf-8') as file:
            long_search_must_condition_info_dict = json.load(file)
        return long_search_must_condition_info_dict

    def get_long_search_request_condition_info_dict(self):
        long_search_request_condition_path = self.data_path_manager.get_long_search_request_condition_path()
        with open(long_search_request_condition_path, 'r', encoding='utf-8') as file:
            long_search_request_condition_info_dict = json.load(file)
        return long_search_request_condition_info_dict

    def get_short_search_must_condition_info_dict(self, shift_id):
        short_search_must_condition_path = f'data_src/data_2024_6/shift{shift_id}/short_search_must_condition.json'
        with open(short_search_must_condition_path, 'r', encoding='utf-8') as file:
            short_search_must_condition_info_dict = json.load(file)
        return short_search_must_condition_info_dict

    def get_short_search_request_condition_info_dict(self, shift_id):
        short_search_request_condition_path \
            = f'data_src/data_2024_6/shift{shift_id}/short_search_request_condition.json'
        with open(short_search_request_condition_path, 'r', encoding='utf-8') as file:
            short_search_request_condition_info_dict = json.load(file)
        return short_search_request_condition_info_dict

    def make_new_best_shift_file(self, shift_id, shift_dict):
        data_path = f'data_dst/data_2024_6/shift{shift_id}/best_shift.json'
        with open(data_path, 'w', encoding='utf-8') as file:
            json.dump(shift_dict, file, ensure_ascii=False, indent=4)

    def make_new_shift_stock_file(self, shift_dict):
        pass

    def make_new_short_search_condition_files(self, shift_id, must_condition_info_dict, request_condition_info_dict):
        must_condition_path = f'data_src/data_2024_6/shift{shift_id}/short_search_must_condition.json'
        with open(must_condition_path, 'w', encoding='utf-8') as file:
            json.dump(must_condition_info_dict, file, ensure_ascii=False, indent=4)
        request_condition_path = f'data_src/data_2024_6/shift{shift_id}/short_search_request_condition.json'
        with open(request_condition_path, 'w', encoding='utf-8') as file:
            json.dump(request_condition_info_dict, file, ensure_ascii=False, indent=4)

    def change_short_search_conditions(self, shift_id, cmust_condition_info_dict, request_condition_info_dict):
        pass
