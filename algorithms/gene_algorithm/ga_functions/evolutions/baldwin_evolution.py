from .evolution import Evolution


class BaldwinEvolution(Evolution):

    def evolve_for_main(
            self,
            individual_2d_array,
            ordered_index_array,
            probability_array,
            do_crossing,
            do_mutation
    ):
        pass

    def evolve_for_break_limit(self, individual_2d_array, ordered_index_array, probability_array, do_crossing, do_mutation):
        pass
