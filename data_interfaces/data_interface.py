from abc import ABC, abstractmethod


# 抽象クラス
class DataInterface(ABC):

    @abstractmethod
    def get_store_info_dict(self):
        pass

    @abstractmethod
    def get_store_shift_request_dict(self):
        pass

    @abstractmethod
    def get_long_search_must_condition_info_dict(self):
        pass

    @abstractmethod
    def get_long_search_request_condition_info_dict(self):
        pass

    @abstractmethod
    def get_short_search_must_condition_info_dict(self, shift_id):
        pass

    @abstractmethod
    def get_short_search_request_condition_info_dict(self, shift_id):
        pass

    @abstractmethod
    def make_new_best_shift_file(self, shift_id, shift_dict):
        pass

    @abstractmethod
    def make_new_shift_stock_file(self, shift_dict):
        pass

    @abstractmethod
    def make_new_short_search_condition_files(self, shift_id, must_condition_info_dict, request_condition_info_dict):
        pass

    @abstractmethod
    def change_short_search_conditions(self, shift_id, must_condition_info_dict, request_condition_info_dict):
        pass
