from abc import ABC, abstractmethod


# 抽象クラス
class Crossing(ABC):

    @abstractmethod
    def do_crossing(self, individual1, individual2):
        pass
