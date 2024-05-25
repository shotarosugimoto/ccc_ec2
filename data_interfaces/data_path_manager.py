class DataPathManager:

    store_info_path = 'data_src/data_2024_6/store_info.json'
    store_shift_request_path = 'data_src/data_2024_6/store_shift_request.json'
    long_search_must_condition_path = 'data_src/data_2024_6/long_search_must_condition.json'
    long_search_request_condition_path = 'data_src/data_2024_6/long_search_request_condition.json'
    must_conditions_path = 'data_src/all_must_conditions.json'
    request_conditions_path = 'data_src/all_request_conditions.json'

    def __init__(self):
        pass

    @classmethod
    def get_store_info_path(cls):
        return cls.store_info_path

    @classmethod
    def get_store_shift_request_path(cls):
        return cls.store_shift_request_path

    @classmethod
    def get_long_search_must_condition_path(cls):
        return cls.long_search_must_condition_path

    @classmethod
    def get_long_search_request_condition_path(cls):
        return cls.long_search_request_condition_path

    @classmethod
    def get_must_condition_path(cls):
        return cls.must_conditions_path

    @classmethod
    def get_request_condition_path(cls):
        return cls.request_conditions_path
