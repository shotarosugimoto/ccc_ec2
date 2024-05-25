from .uniform_mutation import UniformMutation
from .block_mutation import BlockMutation


def mutation_getter(mutation_type, gene_length, m_probability_for_uniform=0.01):
    mutation_type_list = ['uniform', 'block']
    if mutation_type not in mutation_type_list:
        raise Exception("そのアルゴリズムは実装されていません")
    if mutation_type == 'uniform':
        return UniformMutation(gene_length, m_probability_for_uniform)
    if mutation_type == 'block':
        return BlockMutation(gene_length)
