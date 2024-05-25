import numpy as np
from .selection import Selection


class RankingSelection(Selection):

    def __init__(self, number, s_parameter=1.5):
        self.number = number
        self.ranking_selection_probability_array = self.make_ranking_selection_probability_array(s_parameter)

    def get_probability_array(self, score_array=None):
        return self.ranking_selection_probability_array

    def make_ranking_selection_probability_array(self, s_parameter):
        s = s_parameter
        ranking_probability = np.zeros(self.number)
        for i in range(self.number):
            p = (2 - s) / self.number + (2 * (s - 1)) * (self.number - i - 1) / (self.number * (self.number - 1))
            ranking_probability[i] = p
        return ranking_probability
