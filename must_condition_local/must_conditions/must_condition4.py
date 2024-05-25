# 全員1週間<max_hour>時間以上働いてはいけない
# 未実装

from .must_condition_base import (MustConditionBase)
import numpy as np


class MustCondition4(MustConditionBase):

    def __init__(self, data_store, arg_dict):
        super().__init__(data_store)
        self.min_hour = arg_dict["min_hour"]

    def judgement(self, new_shift: np.ndarray):
        return True
