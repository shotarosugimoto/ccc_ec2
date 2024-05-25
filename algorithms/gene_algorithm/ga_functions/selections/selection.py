from abc import ABC, abstractmethod


# 抽象クラス
class Selection(ABC):

    @abstractmethod
    def get_probability_array(self, score_array=None):
        pass
