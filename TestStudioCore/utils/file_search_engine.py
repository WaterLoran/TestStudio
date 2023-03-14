# -*- coding: utf-8 -*-
import os


class FileSearchEngine:
    def __init__(self):
        pass

    @classmethod
    def get_all_py_file(self, rootdir):
        import os
        _files = []
        # 列出文件夹下所有的目录与文件
        list_file = os.listdir(rootdir)
        for i in range(0, len(list_file)):
            # 构造路径
            path = os.path.join(rootdir, list_file[i])
            # 判断路径是否是一个文件目录或者文件
            # 如果是文件目录，继续递归
            if os.path.isdir(path):
                _files.extend(self.get_all_py_file(path))
            if os.path.isfile(path):
                # print("path", path)
                if path.endswith("py"):
                    _files.append(path)
        return _files

