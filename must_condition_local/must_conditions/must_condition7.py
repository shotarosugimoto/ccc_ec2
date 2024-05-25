# 全員1週間に<min_date_num>日以上<max_date_num>日以下働かなければならない
# 未実装

from .must_condition_base import (MustConditionBase)
import numpy as np


class MustCondition7(MustConditionBase):

    def __init__(self, data_store, arg_dict):
        super().__init__(data_store)
        self.min_date_num = arg_dict["min_date_num"]
        self.max_date_num = arg_dict["max_date_num"]

    def judgement(self, new_shift: np.ndarray):
        return True
