from data_interfaces.setting_data.long_search_setting_data_store import LongSearchSettingDataStore

from .gene_algorithm.gene_algorithm import GeneAlgorithm
from .conditional_SA.conditional_SA import ConditionalSA
from .conditional_TA.conditional_TA import ConditionalTA


def get_algorithm_instance(
        long_search_setting_data_store: LongSearchSettingDataStore,
        data_interface,
        data_store,
        must_condition_manager,
        request_condition_manager
):
    algo_name = long_search_setting_data_store.algo_name
    algo_detail = long_search_setting_data_store.algo_detail

    if algo_name == 'GA':
        algo_instance = GeneAlgorithm(
            algo_detail,
            data_interface,
            data_store,
            must_condition_manager,
            request_condition_manager
        )
    elif algo_name == 'Conditional_SA':
        algo_instance = ConditionalSA(
            algo_detail,
            data_interface,
            data_store,
            must_condition_manager,
            request_condition_manager
        )
    elif algo_name == 'Conditional_TA':
        algo_instance = ConditionalTA(
            algo_detail,
            data_interface,
            data_store,
            must_condition_manager,
            request_condition_manager
        )
    else:
        raise Exception("そのアルゴリズムは実装されていません")

    return algo_instance
