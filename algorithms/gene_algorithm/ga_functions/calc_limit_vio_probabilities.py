import numpy as np


class CalcLimitVioProbabilities:

    def __init__(self, gene_length, gene_to_3d_shift, limitations_func_manager):
        self.gene_length = gene_length
        self.gene_to_3d_shift = gene_to_3d_shift
        self.limitation_function_manager = limitations_func_manager

    def initial_limit_vio_probabilities(self, ideal_selection_probability, calc_times=1000):
        """
        初期条件の違反率を先に計算しておく。
        :return それぞれの制約の違反率を返す
        :rtype list
        """
        shift_list = []
        for i in range(calc_times):
            p = ideal_selection_probability
            new_gene = np.random.choice([0, 1], size=self.gene_length, p=[1 - p, p])
            new_shift = self.gene_to_3d_shift(new_gene)
            shift_list.append(new_shift)
        vio_list = self.limitation_function_manager.calc_vio_probabilities(shift_list)
        return vio_list
