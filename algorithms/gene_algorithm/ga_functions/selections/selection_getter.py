from .ranking_selection import RankingSelection


def selection_getter(selection_type, number, s_parameter_for_ranking=1.5):
    selection_type_list = ['ranking']
    if selection_type not in selection_type_list:
        raise Exception("そのアルゴリズムは実装されていません")
    if selection_type == 'ranking':
        return RankingSelection(number, s_parameter_for_ranking)
