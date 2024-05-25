import json

from .long_search_setting_data_store import LongSearchSettingDataStore


def get_long_search_setting_data():
    with open('data_src/long_search_setting_data.json', 'r', encoding='utf-8') as file:
        long_search_setting_data = json.load(file)
    with open('data_src/algo_details.json', 'r', encoding='utf-8') as file:
        algo_details = json.load(file)

    algo_name = long_search_setting_data['algo_name']
    algo_detail = algo_details[algo_name]
    long_search_setting_data_store = LongSearchSettingDataStore(
        run_type=long_search_setting_data['run_type'],
        algo_name=algo_name,
        algo_detail=algo_detail,
        data_file_place=long_search_setting_data['data_file_place'],
        condition_file_place=long_search_setting_data['condition_file_place'],
    )
    return long_search_setting_data_store
