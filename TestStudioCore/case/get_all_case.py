# -*- coding: utf-8 -*-
from utils.mysql import Mysql
from case.base_config import BaseConfig
import copy


class GetAllCase:
    def __init__(self):
        self.mysql = Mysql()
        self.case_tree = CaseTree()
        self.id_to_case_id_list = []

    def get_sql_data_to_item(self):
        sql_cmd = "select * from test_case;"
        sql_data = self.mysql.exec_sql_in_database(sql=sql_cmd)
        self.id_to_case_id_list = {}  #这里做一个映射,即编号id到case_id的映射,id即前端页面的标记id

        for case in sql_data:
            res = self.case_tree.insert_case(case)
            self.id_to_case_id_list.update(res)

class CaseTree:
    def __init__(self):
        self.config = BaseConfig()
        self.para_order = self.config.para_order
        self.para_order_en = self.config.para_order_en
        self.case_name_index = self.para_order_en.index("case_name")
        self.case_path_index = self.para_order_en.index("case_path")
        self.case_id_index = self.para_order_en.index("case_id")

        self.tree = self.Node("root", "root")
        self.count_id = 1
        pass

    class Node:
        def __init__(self, node_id, node_name):
            self.id = node_id
            self.name = node_name
            self.children = []

    def get_name_and_path_and_caseid(self, case):
        name = case[self.case_name_index + 1]
        path_str = case[self.case_path_index + 1]
        case_id = case[self.case_id_index + 1]
        path_list = path_str.split("==>")  # 这里的  ==> 符号是由上传用例处代码决定的,这里复制过来
        return name, path_list, case_id

    def insert_case(self, case):
        name, path_list, case_id = self.get_name_and_path_and_caseid(case)
        path_list.append(name)
        path = path_list
        # print("\n**********************************************")
        # print("path", path)
        last_id = 0

        q = self.tree
        for p in path:  # path是指要插入的用例的多个节点,p指其中一个节点
            in_flag = False
            if len(q.children) > 0:  # 即节点中的列表不为空的时候,进去依次遍历看看是否包含在内
                for child in q.children:
                    if p == child.name:
                        in_flag = True
                        break
            if in_flag:
                q = child
            else:
                node = self.Node(self.count_id, p)
                q.children.append(node)
                q = q.children[-1]
                last_id = self.count_id
                self.count_id += 1
        t_dict = {last_id: case_id}
        return t_dict

    def get_res_of_tree(self):
        def dg(root):
            if root:
                t_dict = {}
                t_dict["id"] = root.id
                t_dict["name"] = root.name
                # id_to_case_id[root.id] = root.name
                if root.children != []:
                    t_dict["children"] = []
                    for item in root.children:
                        t_dict["children"].append(dg(item))
                return t_dict

        items = dg(self.tree)

        items = items["children"].copy()
        return items

    def get_res_of_tree_interface(self, id_to_case_id):
        items = self.get_res_of_tree()
        data = {}
        data["items"] = items
        data["id_to_case_id"] = id_to_case_id
        return data

    def prepare_some(self):
        node1 = self.Node(2, "node_id_2")
        node2 = self.Node(3, "node_id_3")
        node4 = self.Node(4, "node_id_4")
        node5 = self.Node(5, "node_id_5")
        self.tree.children.append(node1)
        self.tree.children.append(node2)
        temp = self.tree.children[0]
        temp.children.append(node4)
        temp.children.append(node5)

if __name__ == "__main__":
    get_case = GetAllCase()
    get_case.get_sql_data_to_item()
    item = get_case.case_tree.get_res_of_tree_interface(get_case.id_to_case_id_list)

    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print(item)


