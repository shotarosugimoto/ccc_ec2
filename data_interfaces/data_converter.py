import datetime
import numpy as np
from data_interfaces.data_interface import DataInterface


class DataConverter:
    """
    このプログラムでは月曜日が0, 火曜日が1..., 日曜日が6の整数への対応を定義
    曜日のindexとは以上の定義に則っている。

    また学生を0, フリーターを1と整数への対応を定義
    パート属性のindexとは以上の定義に則っている。

    self.time_listの要素は1日あたりのシフト時間単位
    以下シフト時間単位を時間と簡潔に表記する

    辞書への変換が多いのは辞書の検索の計算量が1だからである

    n次元numpy配列が多いのはもちろん普通のn次元配列よりも計算がはるかに早いからである
    以下全てにおいてのことだが、indexが登場する時、それはn次元numpy配列のための識別子として機能させるために用意したと解釈してほしい
    """
    def __init__(self, data_interface: DataInterface):
        self.store_info_dict = data_interface.get_store_info_dict()
        self.store_shift_request_dict = data_interface.get_store_shift_request_dict()

        self.name_list, self.employee_list = self.initial_set_name_and_employee_list()
        self.date_list = self.initial_set_date_list()
        self.time_list, self.shift_unit_list = self.initial_set_time_and_shift_unit_list()
        self.position_list = self.initial_set_position_list()
        self.skill_list = self.initial_set_skill_list()

        self.name_to_index_dict = self.initial_set_name_to_index_dict()
        self.index_to_name_dict = self.initial_set_index_to_name_dict()
        self.date_to_index_dict = self.initial_set_date_to_index_dict()
        self.index_to_date_dict = self.initial_set_index_to_date_dict()
        self.time_to_index_dict = self.initial_set_time_to_index_dict()
        self.index_to_time_dict = self.initial_set_index_to_time_dict()
        self.position_to_index_dict = self.initial_set_position_to_index_dict()
        self.index_to_position_dict = self.initial_set_index_to_position_dict()
        self.skill_to_index_dict = self.initial_set_skill_to_index_dict()
        self.index_to_skill_dict = self.initial_set_index_to_skill_dict()

    def initial_set_name_and_employee_list(self):
        name_list = []
        employee_list = []
        employee_all_list = self.store_info_dict['employee_list']
        for employee in employee_all_list:
            name_list.append(employee['name'])
            employee_list.append(employee)
        return name_list, employee_list

    def initial_set_date_list(self):
        year = self.store_shift_request_dict['year']
        month = self.store_shift_request_dict['month']
        date_list = []
        if month == 6:
            for i in range(1, 31):
                date_list.append(datetime.date(year, month, i))

        return date_list

    def initial_set_time_and_shift_unit_list(self):
        time_list = []
        shift_unit_list = []
        store_shift_request_dict = self.store_shift_request_dict["store_shift_request_dict"]
        shift_unit_dict = store_shift_request_dict["date-1"]
        for _, value in shift_unit_dict.items():
            time_list.append(value['start_hour'])
            shift_unit_list.append({
                'start_hour': value['start_hour'],
                'end_hour': value['end_hour']
            })

        return time_list, shift_unit_list

    def initial_set_position_list(self):
        return self.store_info_dict['position_list']

    def initial_set_skill_list(self):
        return self.store_info_dict['skill_list']

    # 名前のリストを名前と番号(index)の辞書へ 逆のパターンも作成
    def initial_set_name_to_index_dict(self):
        name_to_index_dict = {}
        for i in range(len(self.name_list)):
            name_to_index_dict[self.name_list[i]] = i
        return name_to_index_dict

    def initial_set_index_to_name_dict(self):
        index_to_name_dict = {}
        for i in range(len(self.name_list)):
            index_to_name_dict[i] = self.name_list[i]
        return index_to_name_dict

    # 日付のリストを日付と番号(index)の辞書へ 逆のパターンも作成
    def initial_set_date_to_index_dict(self):
        date_to_index_dict = {}
        for i in range(len(self.date_list)):
            date_to_index_dict[self.date_list[i]] = i
        return date_to_index_dict

    def initial_set_index_to_date_dict(self):
        index_to_date_dict = {}
        for i in range(len(self.date_list)):
            index_to_date_dict[i] = self.date_list[i]
        return index_to_date_dict

    # 時間のリストを時間と番号(index)の辞書へ 逆のパターンも作成
    def initial_set_time_to_index_dict(self):
        time_to_index_dict = {}
        for i in range(len(self.time_list)):
            time_to_index_dict[self.time_list[i]] = i
        return time_to_index_dict

    def initial_set_index_to_time_dict(self):
        index_to_time_dict = {}
        for i in range(len(self.time_list)):
            index_to_time_dict[i] = self.time_list[i]
        return index_to_time_dict

    def initial_set_position_to_index_dict(self):
        position_to_index_dict = {}
        for i in range(len(self.position_list)):
            position_to_index_dict[self.position_list[i]] = i
        return position_to_index_dict

    def initial_set_index_to_position_dict(self):
        index_to_position_dict = {}
        for i in range(len(self.position_list)):
            index_to_position_dict[i] = self.position_list[i]
        return index_to_position_dict

    # スキルのリストをスキルと番号(index)の辞書へ 逆のパターンも作成
    def initial_set_skill_to_index_dict(self):
        skill_to_index_dict = {}
        for i in range(len(self.skill_list)):
            skill_to_index_dict[self.skill_list[i]] = i
        return skill_to_index_dict

    def initial_set_index_to_skill_dict(self):
        index_to_skill_dict = {}
        for i in range(len(self.skill_list)):
            index_to_skill_dict[i] = self.skill_list[i]
        return index_to_skill_dict

    # こっからがgetterのインターフェイス
    # 一貫性を持たせたいので初期値で設定したものにも取得用のget関数をそれぞれ作っておく
    def get_name_to_index_dict(self):
        """
        :return: 名前-index辞書
        :rtype: dict[str, int]
        """
        return self.name_to_index_dict

    def get_index_to_name_dict(self):
        """
        :return: index-名前辞書
        :rtype: dict[int, str]
        """
        return self.index_to_name_dict

    def get_date_to_index_dict(self):
        """
        :return: 日付-index辞書
        :rtype: dict[date_type, int]
        """
        return self.date_to_index_dict

    def get_index_to_date_dict(self):
        """
        :return: index-日付辞書
        :rtype: dict[int, date_type]
        """
        return self.index_to_date_dict

    def get_time_to_index_dict(self):
        """
        :return: 時間-index辞書
        :rtype: dict[str, int]
        """
        return self.time_to_index_dict

    def get_index_to_time_dict(self):
        """
        :return: index-時間辞書
        :rtype: dict[int, str]
        """
        return self.index_to_time_dict

    def get_position_to_index_dict(self):
        """
        :return: ポジション-index辞書
        :rtype: dict[str, int]
        """
        return self.position_to_index_dict

    def get_index_to_position_dict(self):
        """
        :return: index-ポジション辞書
        :rtype: dict[int, str]
        """
        return self.index_to_position_dict

    def get_skill_to_index_dict(self):
        """
        :return: スキル-index辞書
        :rtype: dict[str, int]
        """
        return self.skill_to_index_dict

    def get_index_to_skill_dict(self):
        """
        :return: index-スキル辞書
        :rtype: dict[int, str]
        """
        return self.index_to_skill_dict

    # 時給辞書
    def get_name_index_to_hourly_wage_dict(self):
        """
        :return: 名前index-時給辞書
        :rtype: dict[int, int]
        """
        name_index_to_hourly_wage_dict = {}
        for i in range(len(self.name_list)):
            name_index_to_hourly_wage_dict[i] = self.employee_list[i]['hourly_age']
        return name_index_to_hourly_wage_dict

    def get_hourly_wage_1d_array_by_name(self):
        """
        :return: 名前indexによる時給のnumpy1次元配列
        :rtype: np.ndarray
        """
        hourly_wage_1d_array_by_name = np.zeros(len(self.name_list), dtype=int)
        for i in range(len(self.name_list)):
            hourly_wage = self.employee_list[i]['hourly_age']
            hourly_wage_1d_array_by_name[i] = hourly_wage
        return hourly_wage_1d_array_by_name

    # 交通費辞書
    def get_name_index_to_trans_fee_dict(self):
        """
        :return: 名前index-交通費辞書
        :rtype: dict[int, int]
        """
        name_index_to_trans_fee_dict = {}
        for i in range(len(self.name_list)):
            name_index_to_trans_fee_dict[i] = self.employee_list[i]['trans_fee']
        return name_index_to_trans_fee_dict

    def get_date_index_to_day_index_dict(self):
        """
        曜日indexについては一番上を参照
        :return: 日付index-曜日indexの辞書
        :rtype: dict[int, int]
        """
        date_index_to_day_index_dict = {}
        for date in self.date_list:
            date_index = self.date_to_index_dict[date]
            day_index = date.weekday()
            date_index_to_day_index_dict[date_index] = day_index
        return date_index_to_day_index_dict

    def get_day_index_to_date_index_array_dict(self):
        """
        :return: 曜日index-日付indexのnumpy1次元配列の辞書
        :rtype: dict[int, np.ndarray]
        辞書のvalueをnumpy1次元配列にしたけど順番に意味はないのでもっといいデータ構造がある可能性もある。
        """
        day_index_to_date_index_array_dict = {}
        for date in self.date_list:
            day_index = date.weekday()
            date_index = self.date_to_index_dict[date]
            day_index_to_date_index_array_dict[day_index] \
                = day_index_to_date_index_array_dict.get(day_index, []) + [date_index]

        for key in day_index_to_date_index_array_dict:
            day_index_to_date_index_array_dict[key] = np.array(day_index_to_date_index_array_dict[key])
        return day_index_to_date_index_array_dict
    
    def get_week_2d_array(self):
        """
        :return: 週の数×曜日の二次元配列　各要素が日付index
        :rtype: np.ndarray
        """
        week_dates_list = []
        week_dates = []
        start_flag = False
        for date in self.date_list:
            if (date.weekday() != 0) and (not start_flag):
                continue
            else:
                start_flag = True
                week_dates.append(self.date_to_index_dict[date])
                if len(week_dates) == 7:
                    week_dates_list.append(week_dates)
                    week_dates = []
        return np.array(week_dates_list)

    def get_weekend_2d_array(self):
        """
        1要素目が土で2要素目が日と仮定する
        :return: 土日の数×曜日の二次元配列, 各要素が日付index
        :rtype: np.ndarray
        """
        weekends_list = []
        weekends = []
        for date in self.date_list:
            if date.weekday() == 5 or date.weekday() == 6:
                weekends.append(self.date_to_index_dict[date])
                if len(weekends) == 2:
                    weekends_list.append(weekends)
                    weekends = []
        return np.array(weekends_list)

    # 名前×ポジションの二次元配列,各要素が評価値(bool)
    def get_score_2d_array_by_name_position(self):
        """
        :return: 名前×ポジションのnumpy二次元配列,各要素が評価値(bool)
        :rtype: np.ndarray
        """
        name_len = len(self.name_list)
        position_len = len(self.position_list)
        score_2d_array_by_name_position = np.zeros((name_len, position_len), dtype=bool)
        for employee in self.employee_list:
            name = employee['name']
            position_assessment_dict = employee['position_assessment_dict']
            for position in self.position_list:
                position_assessment = position_assessment_dict[position]
                name_index = self.name_to_index_dict[name]
                position_index = self.position_to_index_dict[position]
                score_2d_array_by_name_position[name_index, position_index] = position_assessment
        return score_2d_array_by_name_position

    # 名前×スキルの二次元配列, 要素が評価値
    def get_score_2d_array_by_name_skill(self):
        """
        :return: 名前×スキルのnumpy二次元配列,各要素が評価値(1~5)
        :rtype: np.ndarray
        """
        name_len = len(self.name_list)
        skill_len = len(self.skill_list)
        score_2d_array_by_name_skill = np.zeros((name_len, skill_len), dtype=int)
        for employee in self.employee_list:
            name = employee['name']
            skill_assessment_dict = employee['skill_assessment_dict']
            for skill in self.skill_list:
                skill_assessment = skill_assessment_dict[skill]
                name_index = self.name_to_index_dict[name]
                skill_index = self.skill_to_index_dict[skill]
                score_2d_array_by_name_skill[name_index, skill_index] = skill_assessment
        return score_2d_array_by_name_skill

    # 日付数×時間×ポジションのnumpy三次元配列で店のシフト要請を表現
    def get_store_request_3d_array_by_date_time_position(self):
        """
        :return: 日付数×時間×ポジションの三次元配列, 各要素がシフトに必要な人の数
        :rtype: np.ndarray
        """
        date_len = len(self.date_list)
        time_len = len(self.time_list)
        position_len = len(self.position_list)
        store_shift_request_dict = self.store_shift_request_dict["store_shift_request_dict"]
        store_request_3d_array_by_date_time_position = np.zeros((date_len, time_len, position_len), dtype=int)
        for date_i in range(date_len):
            date = self.date_list[date_i]
            date_key = f"date-{date.day}"
            shift_request_dict_by_date = store_shift_request_dict[date_key]
            for time_i in range(time_len):
                time_key = f'shift-{time_i}'
                shift_request_dict_by_time = shift_request_dict_by_date[time_key]
                request_dict = shift_request_dict_by_time["request_dict"]
                for position_i in range(position_len):
                    position = self.index_to_position_dict[position_i]
                    request_num = request_dict[position]
                    store_request_3d_array_by_date_time_position[date_i, time_i, position_i] = request_num

        return store_request_3d_array_by_date_time_position

    # 名前×日付×時間のnumpy3次元配列でシフト希望表を表現
    def get_shift_request_3d_array_name_date_time(self):
        """
        :return: 名前×日付×時間のnumpy3次元配列, 各要素が希望の有無(1-0)
        :rtype: np.ndarray
        """
        name_len = len(self.name_list)
        date_len = len(self.date_list)
        time_len = len(self.time_list)
        shift_request_3d_array_name_date_time = np.zeros((name_len, date_len, time_len), dtype=int)
        for name_i in range(name_len):
            employee = self.employee_list[name_i]
            shift_request_dict = employee['shift_request_dict']
            for date_i in range(date_len):
                date = self.date_list[date_i]
                date_key = f"date-{date.day}"
                shift_request_dict_by_date = shift_request_dict[date_key]
                for time_i in range(time_len):
                    time_key = f'shift-{time_i}'
                    request_dict_by_time = shift_request_dict_by_date[time_key]
                    shift_request_3d_array_name_date_time[name_i, date_i, time_i] = int(request_dict_by_time['request'])

        return shift_request_3d_array_name_date_time

    # それぞれの配列の長さも欲しいところ
    def get_date_len(self):
        return len(self.date_list)

    def get_time_len(self):
        return len(self.time_list)

    def get_name_len(self):
        return len(self.name_list)

    def get_position_len(self):
        return len(self.position_list)

    def get_skill_len(self):
        return len(self.skill_list)

    def get_average_skill_num(self):
        """
        :return: 各店員のスキルスコアの平均。ただし各スキルでも平均を取っている。つまり1~5の範囲に収まる。
        :rtype: int
        """
        name_len = len(self.name_list)
        skill_len = len(self.skill_list)
        skill_sum = 0
        for name_i in range(name_len):
            employee = self.employee_list[name_i]
            skill_assessment_dict = employee['skill_assessment_dict']
            for skill in self.skill_list:
                skill_num = skill_assessment_dict[skill]
                skill_sum += skill_num
        average_skill_num = skill_sum/(name_len*skill_len)
        return average_skill_num

    # 各店員の最低, 最高時給
    def get_min_hourly_wage(self):
        min_hourly_wage = 100000
        for employee in self.employee_list:
            new_wage = employee['hourly_age']
            if new_wage < min_hourly_wage:
                min_hourly_wage = new_wage
        return min_hourly_wage

    def get_max_hourly_wage(self):
        max_hourly_wage = 0
        for employee in self.employee_list:
            new_wage = employee['hourly_age']
            if new_wage > max_hourly_wage:
                max_hourly_wage = new_wage
        return max_hourly_wage
