# スキルの合計値が大きくなるようにする。
import numpy as np
from .request_condition_base import RequestConditionBase


class RequestCondition3(RequestConditionBase):

    def __init__(self, data_store, penalty_par, arg_dict):
        super().__init__(data_store)
        penalty_adjust_num = 1
        self.penalty_par = penalty_par * penalty_adjust_num


    # new_shiftは名前×日付×時間×ポジションのnumpy4次元配列で
    # 各要素はシフトが入っているか(1), 入っていないか(0)を1 or 0で表現している。
    def calc_penalty(self, new_shift):
        shift_num_array_by_name = np.sum(new_shift, axis=(1, 2, 3))
        skill_sum_array = np.sum(self.data_store.score_2d_array_by_name_skill, axis=1)
        skill_average_array_by_name = skill_sum_array / self.data_store.skill_len
        average_skill_num = self.data_store.average_skill_num
        skill_diff_array_by_name = skill_average_array_by_name - average_skill_num
        skill_diff_array_by_name[skill_diff_array_by_name > 0] = 0
        skill_shortage_array_by_name = -skill_diff_array_by_name
        total_penalty = np.sum(shift_num_array_by_name @ skill_shortage_array_by_name) * self.penalty_par
        return total_penalty
