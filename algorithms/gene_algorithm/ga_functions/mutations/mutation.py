from abc import ABC, abstractmethod


# 抽象クラス
class Mutation(ABC):

    @abstractmethod
    def do_mutation(self, individual):
        pass
