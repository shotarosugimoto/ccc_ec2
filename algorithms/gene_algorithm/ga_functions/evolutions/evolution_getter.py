from .darwin_evolution import DarwinEvolution


def evolution_getter(
        evolution_type, crossing_probability=0.9,
        reproduction_probability=0.08,
        mutation_probability=0.02
):
    evolution_type_list = ['darwin']
    if evolution_type not in evolution_type_list:
        raise Exception("そのアルゴリズムは実装されていません")

    if evolution_type == 'darwin':
        return DarwinEvolution(crossing_probability, reproduction_probability, mutation_probability)


