# <name>は1週間に<min_hour>時間以上<max_hour>時間以下で働かなければならない
# 未実装

from .must_condition_base import (MustConditionBase)
import numpy as np


class MustCondition8(MustConditionBase):

    def __init__(self, data_store, arg_dict):
        super().__init__(data_store)
        self.name = arg_dict["name"]
        self.min_hour = arg_dict["min_hour"]
        self.max_hour = arg_dict["max_hour"]

    def judgement(self, new_shift: np.ndarray):
        return True
