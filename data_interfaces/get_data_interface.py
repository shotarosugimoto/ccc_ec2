from data_interfaces.data_interface_from_local import DataInterfaceFromLocal


def get_data_interface(data_file_place):
    if data_file_place == 'local':
        data_interface = DataInterfaceFromLocal()
        return data_interface


