# 1シフトに<min_employee_num>人以上入れたい
# 未実装
import numpy as np
from .request_condition_base import RequestConditionBase


class RequestCondition14(RequestConditionBase):

    def __init__(self, data_store, penalty_par, arg_dict):
        super().__init__(data_store)
        penalty_adjust_num = 1
        self.penalty_par = penalty_par * penalty_adjust_num
        self.min_employee_num = arg_dict['min_employee_num']

    # new_shiftは名前×日付×時間×ポジションのnumpy4次元配列で
    # 各要素はシフトが入っているか(1), 入っていないか(0)を1 or 0で表現している。
    def calc_penalty(self, new_shift):
        total_penalty = 0
        return total_penalty
