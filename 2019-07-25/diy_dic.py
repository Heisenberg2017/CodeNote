class StrKeyDict0(dict):

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def get(self, key, default=None):
        try:
            # 这里使用[]的隐式调用了__getitem__宣布失败之前会先调用__missing__
            return self[key]
        except KeyError:
            return default

    def __contains__(self, item):
        # 使用key in self会导致递归调用
        return item in self.keys() or str(item) in self.keys()


if __name__ == '__main__':
    str_dic = StrKeyDict0()
    str_dic.get(4, 5)