from abc import ABC, abstractmethod

from data_interfaces.data_interface import DataInterface
from data_interfaces.data_store import DataStore
from must_condition_local.must_condition_manager import MustConditionManager
from request_condition_local.request_condition_manager import RequestConditionManager


# 抽象クラス
class AlgorithmBase(ABC):

    def __init__(
            self,
            algo_detail,
            data_interface,
            data_store,
            must_condition_manager,
            request_condition_manager,
    ):
        self.algo_detail = algo_detail
        self.data_interface: DataInterface = data_interface
        self.data_store: DataStore = data_store
        self.must_condition_manager: MustConditionManager = must_condition_manager
        self.request_condition_manager: RequestConditionManager = request_condition_manager

    @abstractmethod
    def do_computation(self):
        pass
