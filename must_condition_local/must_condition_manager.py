import importlib
from .must_conditions.must_condition_base import MustConditionBase
from data_interfaces.data_store import DataStore


class MustConditionManager:
    def __init__(self, must_condition_info_dict: dict, data_store: DataStore):
        self.must_condition_instance_list, self.name_list \
            = self.get_must_condition_instance_and_name_list(must_condition_info_dict, data_store)

    @staticmethod
    def get_must_condition_instance_and_name_list(must_condition_info_dict, data_store):
        must_condition_instance_list = []
        name_list = []
        for name, must_condition_value in must_condition_info_dict.items():
            file_name = must_condition_value['file_name']
            class_name = must_condition_value['class_name']
            arg_dict = must_condition_value['arg_dict']
            static_name = 'must_condition_local.must_conditions.'
            module_name = static_name + file_name
            module = importlib.import_module(module_name)
            must_condition_class = getattr(module, class_name)
            must_condition_instance: MustConditionBase = must_condition_class(data_store, arg_dict)
            must_condition_instance_list.append(must_condition_instance)
            name_list.append(name)

        return must_condition_instance_list, name_list

    def all_judgement(self, new_shift):
        for must_condition_instance in self.must_condition_instance_list:
            if not must_condition_instance.judgement(new_shift):
                return False
        return True
