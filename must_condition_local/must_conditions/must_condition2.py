# 全員１日<max_hour>時間以上働いてはいけない"
# 未実装

from .must_condition_base import (MustConditionBase)
import numpy as np


class MustCondition2(MustConditionBase):

    def __init__(self, data_store, arg_dict):
        super().__init__(data_store)
        self.max_hour = arg_dict["max_hour"]

    def judgement(self, new_shift: np.ndarray):
        return True



