# 1シフトに<min_employee_num>以上入る必要がある
# 未実装

from .must_condition_base import (MustConditionBase)
import numpy as np


class MustCondition6(MustConditionBase):

    def __init__(self, data_store, arg_dict):
        super().__init__(data_store)
        self.min_employee_num = arg_dict["min_employee_num"]

    def judgement(self, new_shift: np.ndarray):
        return True

