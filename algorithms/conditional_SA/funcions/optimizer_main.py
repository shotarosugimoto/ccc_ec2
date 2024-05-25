from algorithms.algorithm_base import AlgorithmBase
from algorithms.gene_algorithm.gene_algorithm import GeneAlgorithm


class OptimizerMain:
    def __init__(self, data_store, data_interface, evaluation_func, limitations_func_manager, algo_name='ga'):
        self.algorithm: AlgorithmBase = self.algo_getter(
            algo_name,
            data_store,
            data_interface,
            evaluation_func,
            limitations_func_manager
        )

    @staticmethod
    def algo_getter(algo_name, data_store, data_interface, evaluation_func, limitations_func_manager):
        algo_name_list = ['ga']
        if algo_name not in algo_name_list:
            raise Exception("そのアルゴリズムは実装されていません")

        if algo_name == 'ga':
            ga_instance = GeneAlgorithm(
                data_store,
                data_interface,
                evaluation_func,
                limitations_func_manager,
            )
            return ga_instance

    def compute_optimization(self):
        self.algorithm.do_computation()

