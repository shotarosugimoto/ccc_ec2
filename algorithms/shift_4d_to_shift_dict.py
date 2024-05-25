from data_interfaces.data_store import DataStore


# shift_4d_arrayは名前×日付×時間×ポジションのnumpy4次元配列で
# 各要素はシフトが入っているか(1), 入っていないか(0)を1 or 0で表現している。
def shift_4d_to_shift_dict(shift_4d_array, data_store: DataStore):
    shift_result_dict = {}
    for date_index in range(data_store.date_len):
        date_key = f"date-{date_index + 1}"
        date_value_dict = {}
        for time_index in range(data_store.time_len):
            time_key = f"shift-{time_index + 1}"
            time_value_dict = {
                "start_hour": data_store.index_to_time_dict[time_index],
                "end_hour": data_store.index_to_time_dict[time_index] + 1
            }
            result_duct = {}
            for position_index in range(data_store.position_len):
                position_name = data_store.index_to_position_dict[position_index]
                name_list = []
                array_1d_by_name = shift_4d_array[:, date_index, time_index, position_index]
                for name_index in range(data_store.name_len):
                    if array_1d_by_name[name_index] == 1:
                        name_list.append(data_store.index_to_name_dict[name_index])
                result_duct[position_name] = name_list
            time_value_dict["result_dict"] = result_duct
            date_value_dict[time_key] = time_value_dict
        shift_result_dict[date_key] = date_value_dict
    shift_dict = {
        "shift_result_dict": shift_result_dict
    }
    return shift_dict