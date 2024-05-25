# 一回のシフトにおいてpositionが同じでなければならない
# 未実装

from .must_condition_base import (MustConditionBase)
import numpy as np


class MustCondition10(MustConditionBase):

    def __init__(self, data_store, arg_dict):
        super().__init__(data_store)

    def judgement(self, new_shift: np.ndarray):
        return True
