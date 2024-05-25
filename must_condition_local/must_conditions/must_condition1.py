# シフトに入る日は連続した時間で入る必要がある。
# 未実装
from .must_condition_base import (MustConditionBase)
import numpy as np


class MustCondition1(MustConditionBase):

    def __init__(self, data_store, arg_dict):
        super().__init__(data_store)

    def judgement(self, new_shift: np.ndarray):
        return True
