import numpy as np

from algorithms.algorithm_base import AlgorithmBase


class ConditionalSA(AlgorithmBase):

    def __init__(
            self,
            algo_detail,
            data_interface,
            data_store,
            must_condition_manager,
            request_condition_manager,
    ):
        super().__init__(algo_detail, data_interface, data_store, must_condition_manager, request_condition_manager)


    def do_computation(self):
        current_shift = self.data_store.initial_shift
        current_penalty = self.calc_penalty(current_shift)
        for i in range(self.iteration):
            new_shift = self.data_store.repair_shift(current_shift)
            new_penalty = self.calc_penalty(new_shift)
            if new_penalty < current_penalty:
                current_shift = new_shift
                current_penalty = new_penalty
            else:
                diff = new_penalty - current_penalty
                if np.random.rand() < np.exp(-diff / self.temperature):
                    current_shift = new_shift
                    current_penalty = new_penalty
            self.temperature *= self.alpha
        return current_shift, current_penalty

