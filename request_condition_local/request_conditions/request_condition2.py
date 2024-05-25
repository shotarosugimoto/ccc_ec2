# できるだけ時給を削減する。

import numpy as np
from .request_condition_base import RequestConditionBase


class RequestCondition2(RequestConditionBase):

    def __init__(self, data_store, penalty_par, arg_dict):
        super().__init__(data_store)
        penalty_adjust_num = 1
        self.penalty_par = penalty_par * penalty_adjust_num

    # new_shiftは名前×日付×時間×ポジションのnumpy4次元配列で
    # 各要素はシフトが入っているか(1), 入っていないか(0)を1 or 0で表現している。
    def calc_penalty(self, new_shift):
        shift_num_array = np.sum(new_shift, axis=(1, 2, 3))
        adjusted_costs = self.data_store.hourly_wage_1d_array_by_name - self.data_store.min_hourly_wage
        adjusted_costs = adjusted_costs / self.data_store.max_hourly_wage
        total_penalty = np.sum(shift_num_array @ adjusted_costs) * self.penalty_par
        return total_penalty
