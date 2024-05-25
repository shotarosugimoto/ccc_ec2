from algorithms.conditional_SA.funcions.data_converter import DataConverter


class DataStore:

    def __init__(self, data_converter: DataConverter):
        """
        コンバータからgetで全て呼び出す
        """
        # 日付-index辞書
        self.date_to_index_dict = data_converter.get_date_to_index_dict()
        # index-日付辞書
        self.index_to_date_dict = data_converter.get_index_to_date_dict()
        # シフト時間-index辞書
        self.time_to_index_dict = data_converter.get_time_to_index_dict()
        # index-シフト時間辞書
        self.index_to_time_dict = data_converter.get_index_to_time_dict()
        # 名前-index辞書
        self.name_to_index_dict = data_converter.get_name_to_index_dict()
        # index-名前辞書
        self.index_to_name_dict = data_converter.get_index_to_name_dict()
        # スキル-index辞書
        self.skill_to_index_dict = data_converter.get_skill_to_index_dict()
        # index-スキル辞書
        self.index_to_skill_dict = data_converter.get_index_to_skill_dict()

        # 名前index-時給辞書
        self.name_index_to_hourly_wage_dict = data_converter.get_name_index_to_hourly_wage_dict()
        # 名前indexによる時給のnumpy1次元配列
        self.hourly_wage_1d_array_by_name = data_converter.get_hourly_wage_1d_array_by_name()
        # 名前index-交通費辞書
        self.name_index_to_expenses = data_converter.get_name_index_to_expenses_dict()
        # 日付index-曜日indexの辞書
        self.date_index_to_day_index_dict = data_converter.get_date_index_to_day_index_dict()
        # 曜日index-日付indexのnumpy1次元配列の辞書
        self.day_index_to_date_index_array_dict = data_converter.get_day_index_to_date_index_array_dict()
        # 名前index-パート属性indexの辞書
        self.name_index_to_attribute_index_dict = data_converter.get_name_index_to_attribute_index_dict()
        # パート属性index-名前indexのnumpy1次元配列の辞書
        self.attribute_index_to_name_index_array_dict = data_converter.get_attribute_index_to_name_index_array_dict()

        # 週の数×曜日の二次元配列　各要素が日付
        self.week_2d_array = data_converter.get_week_2d_array()
        # 土日の数×曜日の二次元配列　各要素が日付index
        self.weekend_2d_array = data_converter.get_weekend_2d_array()
        # 名前×スキルのnumpy二次元配列,各要素が評価値(1~5)
        self.score_2d_array_by_name_skill = data_converter.get_score_2d_array_by_name_skill()
        # 日付数×時間の二次元配列, 各要素がシフトに必要な人の数
        self.request_num_2d_array_by_date_time = data_converter.get_request_num_2d_array_by_date_time()
        # 日付数×シフト単位数×人数のnumpy3次元配列, 各要素が希望の有無(0-1)
        self.shift_request_3d_array_date_time_name = data_converter.get_shift_request_3d_array_date_time_name()

        # 要素の長さ
        self.date_len = data_converter.get_date_len()
        self.time_len = data_converter.get_time_len()
        self.name_len = data_converter.get_name_len()
        self.skill_len = data_converter.get_skill_len()

        # 各店員のスキルスコアの平均。ただし各スキルでも平均を取っている。つまり1~5の範囲に収まる。
        self.average_skill_num = data_converter.get_average_skill_num()
        # シフト単位においてどれほどのシフト人数が要求があるかの平均（店舗の要求）
        self.average_shift_demand_num = data_converter.get_average_shift_demand_num()
        # シフト単位においてどれほどのシフト人数が希望があるかの平均（バイトの要求の合計）
        self.average_shift_request_num = data_converter.get_average_shift_request_num()

        # 時給の下限, 上限
        self.min_hourly_wage = data_converter.get_min_hourly_wage()
        self.max_hourly_wage = data_converter.get_max_hourly_wage()

        # リクエストが存在する配列上の位置を日付indexのnumpy配列, 時間indexのnumpy配列, 人数indexのnumpy配列, の3つのtupleで表したもの
        self.exist_request_tuple_inside_date_time_name_array \
            = data_converter.get_exist_request_tuple_inside_date_time_name_array()
        # リクエスト数の総計
        self.total_request_num = data_converter.get_total_request_num()

        # 要素が全て0のシフト希望表と同じ長さの3次元numpy配列
        self.zero_3d_array_by_date_time_name = data_converter.get_zero_3d_array_by_date_time_name()
