class DictFormat(object):

    # 实例设置
    def __init__(self):
        return

    # 排除字典键
    def diff_key(self, data_dict, keys_tup):
        new_dict = dict()
        for key, value in data_dict.items():
            if key not in keys_tup:
                new_dict[key] = value
        return new_dict

    def is_set(self, data_dict, key):
        bool = False
        if key in data_dict.keys():
            bool = True
        return bool
