# <max_date>日以上連続で働かないようにする。
import numpy as np
from .request_condition_base import RequestConditionBase


class RequestCondition4(RequestConditionBase):

    def __init__(self, data_store, penalty_par, arg_dict):
        super().__init__(data_store)
        penalty_adjust_num = 5
        self.penalty_par = penalty_par * penalty_adjust_num
        self.max_date = arg_dict['max_date']

    # new_shiftは名前×日付×時間×ポジションのnumpy4次元配列で
    # 各要素はシフトが入っているか(1), 入っていないか(0)を1 or 0で表現している。
    def calc_penalty(self, new_shift):
        total_penalty = 0
        shift_sum_2d_by_name_date = np.sum(new_shift, axis=(2, 3))

        for name_index in range(self.data_store.name_len):
            shift_sum_array_by_date = shift_sum_2d_by_name_date[name_index, :]
            shift_sum_array_by_date[shift_sum_array_by_date > 0] = 1
            shift_array_by_date = shift_sum_array_by_date

            consecutive = np.diff(np.concatenate(([0], shift_array_by_date, [0])))
            start_idx = np.where(consecutive == 1)[0]
            end_idx = np.where(consecutive == -1)[0]
            consecutive_lengths = end_idx - start_idx
            over_lengths = np.where(consecutive_lengths >= self.max_date)[0]
            total_penalty += self.penalty_par * len(over_lengths)
        return total_penalty

