# できるだけシフトの人数に合わせる。

import numpy as np
from .request_condition_base import RequestConditionBase


class RequestCondition1(RequestConditionBase):

    def __init__(self, data_store, penalty_par, arg_dict):
        super().__init__(data_store)
        penalty_adjust_num = 0.5
        self.penalty_par = penalty_par * penalty_adjust_num

    # new_shiftは名前×日付×時間×ポジションのnumpy4次元配列で
    # 各要素はシフトが入っているか(1), 入っていないか(0)を1 or 0で表現している。
    def calc_penalty(self, new_shift):
        new_shift_num_sum = np.sum(new_shift, axis=0)
        difference_3d = self.data_store.store_request_3d_array_by_date_time_position - new_shift_num_sum
        difference_3d[difference_3d < 0] *= -5
        penalty_3d = np.abs(difference_3d)
        total_penalty = np.sum(penalty_3d)
        total_penalty *= self.penalty_par
        return total_penalty
