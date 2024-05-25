from data_interfaces.data_interface import DataInterface
import pandas as pd
import re
import numpy as np
from datetime import date as date_type


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

        # 今の所インターファイスから読み込めるもの
        self.date_list = data_interface.get_date_info()
        self.name_list = data_interface.get_part_name()
        self.part_info_df: pd.DataFrame = data_interface.get_part_info()
        self.shift_num_df: pd.DataFrame = data_interface.get_shift_num_info()
        self.shift_request_form_df = data_interface.get_shift_request_form()

        # 以下は初期値として必要だがインターフェイスから直接読み込めない
        # よって関数を実装して初期セットしておく
        self.time_list = self.initial_set_time_list()
        self.skill_list = self.initial_set_skill_list()
        # 日付-index辞書
        self.date_to_index_dict = self.initial_set_date_to_index_dict()
        self.index_to_date_dict = self.initial_set_index_to_date_dict()
        # 時間-index辞書
        self.time_to_index_dict = self.initial_set_time_to_index_dict()
        self.index_to_time_dict = self.initial_set_index_to_time_dict()
        # 名前-index辞書
        self.name_to_index_dict = self.initial_set_name_to_index_dict()
        self.index_to_name_dict = self.initial_set_index_to_name_dict()
        # skill-index辞書
        self.skill_to_index_dict = self.initial_set_skill_to_index_dict()
        self.index_to_skill_dict = self.initial_set_index_to_skill_dict()

    def initial_set_time_list(self):
        date_shift_time_list = []
        column_names = self.shift_num_df.columns.tolist()
        for column in column_names:
            shift_time = re.findall(r"\[.*?]", column)[0]
            if shift_time not in date_shift_time_list:
                date_shift_time_list.append(shift_time)
        return date_shift_time_list

    def initial_set_skill_list(self):
        skill_list = []
        column_names = self.part_info_df.columns.tolist()
        for column in column_names:
            if column != '時給' and column != '交通費' and column != 'パート属性' and column != '希望曜日':
                skill_list.append(column)
        return skill_list

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

    # シフト単位（日付あたりの)のリストをシフト単位と番号(index)の辞書へ 逆のパターンも作成
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
        hourly_wage_data = self.part_info_df['時給']
        name_index_to_hourly_wage_dict = {}
        for name, hourly_wage in hourly_wage_data.items():
            name_index = self.name_to_index_dict[name]
            name_index_to_hourly_wage_dict[name_index] = hourly_wage
        return name_index_to_hourly_wage_dict

    def get_hourly_wage_1d_array_by_name(self):
        """
        :return: 名前indexによる時給のnumpy1次元配列
        :rtype: np.ndarray
        """
        hourly_wage_1d_array_by_name = np.zeros(len(self.name_list), dtype=int)
        for i in range(len(self.name_list)):
            hourly_wage = self.part_info_df.at[self.name_list[i], '時給']
            hourly_wage_1d_array_by_name[i] = hourly_wage
        return hourly_wage_1d_array_by_name

    # 交通費辞書
    def get_name_index_to_expenses_dict(self):
        """
        :return: 名前index-交通費辞書
        :rtype: dict[int, int]
        """
        expenses_data = self.part_info_df['交通費']
        name_index_to_expenses_dict = {}
        for name, expenses in expenses_data.items():
            name_index = self.name_to_index_dict[name]
            name_index_to_expenses_dict[name_index] = expenses
        return name_index_to_expenses_dict

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

    def get_name_index_to_attribute_index_dict(self):
        """
        パート属性indexについては一番上を参照
        :return: 名前index-パート属性indexの辞書
        :rtype: dict[int, int]
        """
        attribute_data = self.part_info_df['パート属性']
        name_index_to_attribute_index_dict = {}
        for name, attribute in attribute_data.items():
            name_index = self.name_to_index_dict[name]
            attribute_index = 0 if attribute == '学生' else 1
            name_index_to_attribute_index_dict[name_index] = attribute_index
        return name_index_to_attribute_index_dict

    # パート属性(index)-名前（index)のnumpy配列の辞書
    def get_attribute_index_to_name_index_array_dict(self):
        """
        :return: パート属性index-名前indexのnumpy1次元配列の辞書
        :rtype: dict[int, np.ndarray]
        これも同様に順番に意味はないのでvalueにはもっといいデータ構造がある可能性がある。
        """
        attribute_data = self.part_info_df['パート属性']
        attribute_index_to_name_index_array_dict = {
            0: [],
            1: [],
        }
        for name, attribute in attribute_data.items():
            attribute_index = 0 if attribute == '学生' else 1
            name_index = self.name_to_index_dict[name]
            attribute_index_to_name_index_array_dict[attribute_index].append(name_index)
        for key in attribute_index_to_name_index_array_dict:
            attribute_index_to_name_index_array_dict[key] = np.array(attribute_index_to_name_index_array_dict[key])
        return attribute_index_to_name_index_array_dict

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
        １要素目が土で2要素目が日と仮定する
        :return: 土日の数×曜日の二次元配列　各要素が日付index
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

    # 名前×スキルの二次元配列, 要素が評価値
    def get_score_2d_array_by_name_skill(self):
        """
        :return: 名前×スキルのnumpy二次元配列,各要素が評価値(1~5)
        :rtype: np.ndarray
        """
        name_len = len(self.name_list)
        skill_len = len(self.skill_list)
        score_2d_array_by_name_skill = np.zeros((name_len, skill_len), dtype=int)
        for name in self.name_list:
            for skill in self.skill_list:
                skill_num = self.part_info_df.at[name, skill]
                name_index = self.name_to_index_dict[name]
                skill_index = self.skill_to_index_dict[skill]
                score_2d_array_by_name_skill[name_index, skill_index] = skill_num
        return score_2d_array_by_name_skill

    def get_request_num_2d_array_by_date_time(self):
        """
        :return: 日付数×時間の二次元配列, 各要素がシフトに必要な人の数
        :rtype: np.ndarray
        """
        date_len = len(self.date_list)
        shift_time_len = len(self.time_list)
        request_num_2d_array_by_date_time = np.zeros((date_len, shift_time_len), dtype=int)
        for date in self.date_list:
            date_string = date.strftime("%Y/%-m/%-d")
            for shift_time in self.time_list:
                column_key = f'{date_string} {shift_time}'
                request_num = self.shift_num_df.at['シフト人数', column_key]
                date_index = self.date_to_index_dict[date]
                shift_time_index = self.time_to_index_dict[shift_time]
                request_num_2d_array_by_date_time[date_index, shift_time_index] = request_num
        return request_num_2d_array_by_date_time

    # 日付数×シフト単位数×人数のnumpy3次元配列でシフト希望表を表現
    def get_shift_request_3d_array_date_time_name(self):
        """
        :return: 日付数×シフト単位数×人数のnumpy3次元配列, 各要素が希望の有無(0-1)
        :rtype: np.ndarray
        """
        date_len = len(self.date_list)
        shift_time_len = len(self.time_list)
        name_len = len(self.name_list)
        shift_request_3d_array_date_time_name = np.zeros((date_len, shift_time_len, name_len), dtype=int)
        for date in self.date_list:
            date_index = self.date_to_index_dict[date]
            date_string = date.strftime("%Y/%-m/%-d")
            for shift_time in self.time_list:
                shift_time_index = self.time_to_index_dict[shift_time]
                column_key = f'{date_string} {shift_time}'
                for name in self.name_list:
                    name_index = self.name_to_index_dict[name]
                    request = self.shift_request_form_df.at[name, column_key]
                    shift_request_3d_array_date_time_name[date_index, shift_time_index, name_index] = request
        return shift_request_3d_array_date_time_name

    # それぞれの配列の長さも欲しいところ
    def get_date_len(self):
        return len(self.date_list)

    def get_time_len(self):
        return len(self.time_list)

    def get_name_len(self):
        return len(self.name_list)

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
        for name in self.name_list:
            for skill in self.skill_list:
                skill_num = self.part_info_df.at[name, skill]
                skill_sum += skill_num
        average_skill = skill_sum/(name_len*skill_len)
        return average_skill

    def get_average_shift_demand_num(self):
        """
        :return: シフト単位においてどれほどのシフト人数が要求があるか（店舗の要求）
        :rtype: int
        """
        total_shift_num = self.shift_num_df.sum().sum()
        average_shift_demand = total_shift_num/(len(self.date_list) * len(self.time_list))
        return average_shift_demand

    def get_average_shift_request_num(self):
        """
        :return: シフト単位においてどれほどのシフト人数が希望があるか（バイトの要求の合計）
        :rtype: int
        """
        total_shift_num = self.shift_request_form_df.sum().sum()
        average_shift_request = total_shift_num / (len(self.date_list) * len(self.time_list))
        return average_shift_request

    # 各店員の最低, 最高時給
    def get_min_hourly_wage(self):
        min_wage = 0
        for name in self.name_list:
            new_wage = self.part_info_df.at[name, '時給']
            if new_wage < min_wage:
                min_wage = new_wage
        return min_wage

    def get_max_hourly_wage(self):
        max_wage = 0
        for name in self.name_list:
            new_wage = self.part_info_df.at[name, '時給']
            if new_wage > max_wage:
                max_wage = new_wage
        return max_wage

    def get_exist_request_tuple_inside_date_time_name_array(self):
        """
        :return: リクエストが存在する配列上の位置を日付indexのnumpy配列, 時間indexのnumpy配列, 人数indexのnumpy配列, の3つのtupleで表したもの
        :rtype: tuple
        """
        date_len = len(self.date_list)
        shift_time_len = len(self.time_list)
        name_len = len(self.name_list)
        shift_request_3d_array_date_time_name = np.zeros((date_len, shift_time_len, name_len), dtype=int)
        for date in self.date_list:
            date_index = self.date_to_index_dict[date]
            date_string = date.strftime("%Y/%-m/%-d")
            for shift_time in self.time_list:
                shift_time_index = self.time_to_index_dict[shift_time]
                column_key = f'{date_string} {shift_time}'
                for name in self.name_list:
                    name_index = self.name_to_index_dict[name]
                    request = self.shift_request_form_df.at[name, column_key]
                    shift_request_3d_array_date_time_name[date_index, shift_time_index, name_index] = request

        exist_request_tuples_inside_date_time_name_array = np.where(shift_request_3d_array_date_time_name == 1)
        return exist_request_tuples_inside_date_time_name_array

    def get_zero_3d_array_by_date_time_name(self):
        """
        使い勝手が良さそうなので作っておく
        :return: 要素が全て0のシフト希望表と同じ長さの3次元numpy配列
        :rtype: np.ndarray
        """
        zero_3d_array_by_date_time_name \
            = np.zeros((len(self.date_list), len(self.time_list), len(self.name_list)), dtype=int)
        return zero_3d_array_by_date_time_name

    def get_total_request_num(self):
        """
        :return: リクエスト数の総計
        :rtype: int
        """
        date_len = len(self.date_list)
        shift_time_len = len(self.time_list)
        name_len = len(self.name_list)
        shift_request_3d_array_date_time_name = np.zeros((date_len, shift_time_len, name_len), dtype=int)
        for date in self.date_list:
            date_index = self.date_to_index_dict[date]
            date_string = date.strftime("%Y/%-m/%-d")
            for shift_time in self.time_list:
                shift_time_index = self.time_to_index_dict[shift_time]
                column_key = f'{date_string} {shift_time}'
                for name in self.name_list:
                    name_index = self.name_to_index_dict[name]
                    request = self.shift_request_form_df.at[name, column_key]
                    shift_request_3d_array_date_time_name[date_index, shift_time_index, name_index] = request

        exist_request_tuples_inside_date_time_name_array = np.where(shift_request_3d_array_date_time_name == 1)
        total_request_num = len(exist_request_tuples_inside_date_time_name_array[0])
        return total_request_num
