from abc import ABCMeta, abstractmethod
import numpy as np
from data_interfaces.data_store import DataStore


# 抽象クラス
class MustConditionBase(metaclass=ABCMeta):

    def __init__(self, data_store):
        self.data_store: DataStore = data_store

    @abstractmethod
    def judgement(self, new_shift: np.ndarray):
        pass

    def calc_evaluation(self, new_shift: np.ndarray):
        pass


