# <name>は毎週土日のどちらかのみ働かなければならない
# 未実装

from .must_condition_base import (MustConditionBase)
import numpy as np


class MustCondition9(MustConditionBase):

    def __init__(self, data_store, arg_dict):
        super().__init__(data_store)
        self.name = arg_dict["name"]

    def judgement(self, new_shift: np.ndarray):
        return True
