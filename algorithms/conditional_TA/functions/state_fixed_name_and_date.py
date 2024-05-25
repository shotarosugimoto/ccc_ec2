import numpy as np


class StateFixedNameAndDate:

    def __init__(self, min_hour, max_hour, request_array_by_time, score_array_by_position):
        time_len = len(request_array_by_time)
        position_len = len(score_array_by_position)
        self.state_num_len = 1
        self.possible_2d_array_by_time_position_state_list = [np.zeros((time_len, position_len), dtype=int)]
        self.now_state = np.zeros((time_len, position_len), dtype=int)
        self.make_possible_states(min_hour, max_hour, request_array_by_time, score_array_by_position)
        self.change_random_state()

    def make_possible_states(self, min_hour, max_hour, request_array_by_time, score_array_by_position):
        if np.sum(request_array_by_time) == 0:
            return
        else:
            time_len = len(request_array_by_time)
            position_len = len(score_array_by_position)
            # 働く時間を4時間から9時間まで変える
            for work_hour in range(min_hour, max_hour + 1):
                # スタート時間を変える
                for start_time_index in range(time_len - work_hour + 1):
                    # 働く時間連続勤務可能かチェック
                    possible_flag = True
                    for time_index in range(start_time_index, start_time_index + work_hour):
                        if request_array_by_time[time_index] == 0:
                            possible_flag = False
                            break
                    # 働く時間連続勤務可能の時stateを追加
                    if possible_flag:
                        for position_index in range(position_len):
                            # どのポジションが可能かチェック
                            if score_array_by_position[position_index]:
                                # その時間帯においてポジションごとにstate追加
                                new_state = np.zeros((time_len, position_len), dtype=int)
                                new_state[start_time_index:start_time_index + work_hour, position_index] = 1
                                self.possible_2d_array_by_time_position_state_list.append(new_state)
                                self.state_num_len += 1

    def change_random_state(self):
        random_integer = np.random.randint(0, self.state_num_len)
        self.now_state = self.possible_2d_array_by_time_position_state_list[random_integer]

    def change_state_by_index(self, index):
        self.now_state = self.possible_2d_array_by_time_position_state_list[index]

    def get_state_num_len(self):
        return self.state_num_len

    def get_now_state(self):
        return self.now_state
