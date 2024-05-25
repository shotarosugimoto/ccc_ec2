import numpy as np
from data_interfaces.data_store import DataStore


class GeneTo3dShiftConverter:

    def __init__(self, data_store: DataStore):
        exist_request_tuple = data_store.exist_request_tuple_inside_date_time_name_array
        self.zero_3d_array_by_date_time_name = data_store.zero_3d_array_by_date_time_name
        self.date_array = exist_request_tuple[0]
        self.time_array = exist_request_tuple[1]
        self.name_array = exist_request_tuple[2]

    def gene_to_3d_shift(self, gene_array):
        """
        :return: 遺伝子個体からシフト表の3次元numpy配列への変換器
        """
        index_array = np.where(gene_array == 1)[0]
        new_3d_array = self.zero_3d_array_by_date_time_name.copy()
        new_3d_array[
            self.date_array[index_array],
            self.time_array[index_array],
            self.name_array[index_array],
        ] = np.ones(len(index_array))
        return new_3d_array

