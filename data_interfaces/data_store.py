from data_interfaces.data_converter import DataConverter


class DataStore:

    def __init__(self, data_converter: DataConverter):
        """
        コンバータからgetで全て呼び出す
        """

        # 名前-index辞書
        self.name_to_index_dict = data_converter.get_name_to_index_dict()
        # index-名前辞書
        self.index_to_name_dict = data_converter.get_index_to_name_dict()
        # 日付-index辞書
        self.date_to_index_dict = data_converter.get_date_to_index_dict()
        # index-日付辞書
        self.index_to_date_dict = data_converter.get_index_to_date_dict()
        # シフト時間-index辞書
        self.time_to_index_dict = data_converter.get_time_to_index_dict()
        # index-シフト時間辞書
        self.index_to_time_dict = data_converter.get_index_to_time_dict()
        # ポジション-index辞書
        self.position_to_index_dict = data_converter.get_position_to_index_dict()
        # index-ポジション辞書
        self.index_to_position_dict = data_converter.get_index_to_position_dict()
        # スキル-index辞書
        self.skill_to_index_dict = data_converter.get_skill_to_index_dict()
        # index-スキル辞書
        self.index_to_skill_dict = data_converter.get_index_to_skill_dict()

        # 名前index-時給辞書
        self.name_index_to_hourly_wage_dict = data_converter.get_name_index_to_hourly_wage_dict()
        # 名前indexによる時給のnumpy1次元配列
        self.hourly_wage_1d_array_by_name = data_converter.get_hourly_wage_1d_array_by_name()
        # 名前index-交通費辞書
        self.name_index_to_trans_fee_dict = data_converter.get_name_index_to_trans_fee_dict()
        # 日付index-曜日indexの辞書
        self.date_index_to_day_index_dict = data_converter.get_date_index_to_day_index_dict()
        # 曜日index-日付indexのnumpy1次元配列の辞書
        self.day_index_to_date_index_array_dict = data_converter.get_day_index_to_date_index_array_dict()

        # 週の数×曜日の二次元配列　各要素が日付
        self.week_2d_array = data_converter.get_week_2d_array()
        # 土日の数×曜日の二次元配列　各要素が日付index
        self.weekend_2d_array = data_converter.get_weekend_2d_array()
        # 名前×ポジションの二次元配列,各要素が評価値(bool)
        self.score_2d_array_by_name_position = data_converter.get_score_2d_array_by_name_position()
        # 名前×スキルのnumpy二次元配列,各要素が評価値(1~5)
        self.score_2d_array_by_name_skill = data_converter.get_score_2d_array_by_name_skill()
        # 日付数×時間×ポジションの三次元配列, 各要素がシフトに必要な人の数
        self.store_request_3d_array_by_date_time_position \
            = data_converter.get_store_request_3d_array_by_date_time_position()
        # 名前×日付×時間のnumpy3次元配列, 各要素が希望の有無(1 or 0)
        self.shift_request_3d_array_name_date_time = data_converter.get_shift_request_3d_array_name_date_time()

        # 要素の長さ
        self.date_len = data_converter.get_date_len()
        self.time_len = data_converter.get_time_len()
        self.name_len = data_converter.get_name_len()
        self.position_len = data_converter.get_position_len()
        self.skill_len = data_converter.get_skill_len()

        # 各店員のスキルスコアの平均。ただし各スキルでも平均を取っている。つまり1~5の範囲に収まる。
        self.average_skill_num = data_converter.get_average_skill_num()
        # 時給の下限, 上限
        self.min_hourly_wage = data_converter.get_min_hourly_wage()
        self.max_hourly_wage = data_converter.get_max_hourly_wage()
