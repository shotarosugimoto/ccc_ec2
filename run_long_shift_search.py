from data_interfaces.setting_data.get_long_search_setting_data import get_long_search_setting_data
from data_interfaces.setting_data.long_search_setting_data_store import LongSearchSettingDataStore

from data_interfaces.get_data_interface import get_data_interface
from data_interfaces.data_interface import DataInterface
from data_interfaces.data_converter import DataConverter
from data_interfaces.data_store import DataStore

from must_condition_local.must_condition_manager import MustConditionManager
from request_condition_local.request_condition_manager import RequestConditionManager

from algorithms.get_algorithm_instance import get_algorithm_instance


def run_long_shift_search():

    # 設定データの取得
    long_search_setting_data_store: LongSearchSettingDataStore = get_long_search_setting_data()

    # データの取得, 整形, 保存
    data_interface: DataInterface = get_data_interface(long_search_setting_data_store.data_file_place)
    data_converter = DataConverter(data_interface)
    data_store = DataStore(data_converter)

    if long_search_setting_data_store.condition_file_place == 'local':
        # 禁止条件管理クラスの作成
        must_condition_info_dict = data_interface.get_long_search_must_condition_info_dict()
        must_condition_manager = MustConditionManager(must_condition_info_dict, data_store)

        # 要求条件管理クラスの作成
        request_condition_info_dict = data_interface.get_long_search_request_condition_info_dict()
        request_condition_manager = RequestConditionManager(request_condition_info_dict, data_store)

    else:
        raise Exception("その条件ファイルの場所は実装されていません")

    # アルゴリズムのインスタンスの取得
    algorithm_instance = get_algorithm_instance(
        long_search_setting_data_store,
        data_interface,
        data_store,
        must_condition_manager,
        request_condition_manager
    )
    algorithm_instance.do_computation()





if __name__ == "__main__":
    run_long_shift_search()
