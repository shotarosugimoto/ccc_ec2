from abc import ABCMeta, abstractmethod
import numpy as np

from data_interfaces.data_store import DataStore


class RequestConditionBase(metaclass=ABCMeta):

    def __init__(self, data_store):
        self.data_store: DataStore = data_store

    @abstractmethod
    def calc_penalty(self, new_shift: np.ndarray):
        pass
