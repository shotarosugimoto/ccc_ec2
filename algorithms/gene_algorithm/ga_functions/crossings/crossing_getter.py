from .two_point_crossing import TwoPointCrossing
from .uniform_crossing import UniformCrossing


def crossing_getter(crossing_type, gene_length):
    crossing_type_list = ['2point', 'uniform']
    if crossing_type not in crossing_type_list:
        raise Exception("そのアルゴリズムは実装されていません")

    if crossing_type == '2point':
        return TwoPointCrossing(gene_length)
    elif crossing_type == 'uniform':
        return UniformCrossing(gene_length)


