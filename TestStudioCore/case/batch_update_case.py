# -*- coding: utf-8 -*-
import os
import sys
from utils.excel_parser import ReadExcel
from utils. mysql import Mysql
from case.base_config import BaseConfig

class BatchUpdateCase:
    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path
        self.case_list = []  # parse_excel_to_case函数解析生成的用例列表,将可直接用于写入Mysql数据库
        self.sql_cmd = ""  # prepare_case_to_sql函数的过程数据,即用来插入到数据库的sql命令

        self.excel = ReadExcel(self.excel_file_path)
        self.mysql = Mysql()
        self.config = BaseConfig()

        # self.para_order = ["层级", "特性", "用例ID", "用例名称", "前置条件", "用例过程", "期望结果", "用例级别", "责任人", "自动化", "组网类型", "备注", "脚本路径"]
        # self.para_order_en = ["level", "feature", "case_id", "case_name", "preconditions", "case_process", "desired_result", "case_level", "responsible", "automation", "network_type", "remark", "case_path"]
        self.para_order = self.config.para_order
        self.para_order_en = self.config.para_order_en


        pass

    def judge_case_or_feature(self, line):
        if line["特性"] is not None:
            return "feature"
        if line["用例ID"] is not None:
            return "case"

    def check_case_format_by_line(self, line):
        # 检查用例ID是否包含空格，如有则报错
        if " " in line["用例ID"]:
            print("发现用例ID中包含空格，用例ID是 ==> ", line["用例ID"])
            assert False
        # 其他需要检查的检查点
        pass

    def change_case_line_dict_to_list(self, case_dict):
        case_line = []
        para_order = self.para_order
        for item in para_order:
            case_line.append(case_dict[item])
        return case_line

    def parse_excel_to_case(self):
        case_data = self.excel.readExcel_to_dict()
        cur_depth = 0
        last_depth = 0
        path_stack = []
        for line in case_data:
            if self.judge_case_or_feature(line) == "feature":  # 表示这行是一个目录，需要做目录切换
                last_depth = cur_depth
                cur_depth = line["层级"].count(".")
                if cur_depth == last_depth:  # 表示是相同深度，需要取父目录再加上当前目录
                    path_stack.pop()
                    path_stack.append(line["特性"])
                elif cur_depth > last_depth:  # 表示是深度递进，需要在原先的基础上叠加新的目录
                    path_stack.append(line["特性"])
                elif cur_depth < last_depth:  # 表示是深度减少，需要将当前目录按数目退回到父目录，然后加上该行的目录
                    for _ in range(last_depth - cur_depth + 1):
                        path_stack.pop()
                    path_stack.append(line["特性"])
                else:
                    raise
            elif self.judge_case_or_feature(line) == "case":  # 表示这行是用例，需要做用例组装和写入本地
                self.check_case_format_by_line(line)
                path_node_label = "==>"
                case_path = path_node_label.join(path_stack)
                line["脚本路径"] = case_path  # 改变量为新增变量,用于表示一个用例的深度,将用于表示在属性结构的位置
                line["特性"] =  path_stack[-1]
                if line["备注"] is None:
                    line["备注"] = ""
                # print("line", line)
                new_line = self.change_case_line_dict_to_list(line)
                # print("new_line", new_line)
                self.case_list.append(new_line)
            else:
                raise

    def prepare_case_to_sql(self):
        # 根据用例列表信息转换出要写入数据库的sql命令,写入数据库的时候,可以考虑使用事务,多条数据一起插入,如果全部成功则OK,否则回退
        # print("self.case_list", self.case_list)
        sheet_name = "test_case"
        sql_cmd = ""
        sql_cmd += r"INSERT INTO {}".format(sheet_name)
        sql_cmd += "({}) ".format(",".join(self.para_order_en))
        sql_cmd += "VALUES "
        for j in range(len(self.case_list)):
            item = self.case_list[j]
            value_str = ""
            for i in range(len(item) - 1):
                value_str += '\"{}\", '.format(item[i])
            value_str += '\"{}\"'.format(item[-1])
            # 根据是否是最后一个来去除", \n"
            if j == len(self.case_list) - 1:
                sql_cmd += "({})".format(value_str)
            else:
                sql_cmd += "({}), ".format(value_str)
        sql_cmd += ";"
        self.sql_cmd = sql_cmd
        # print("sql_cmd", sql_cmd)
        pass

    def write_case_sql_to_mysql(self):
        # create table test_case(
        # 	id INT NOT NULL AUTO_INCREMENT,
        # 	level VARCHAR(10) NOT NULL,
        # 	feature VARCHAR(200) NOT NULL,
        # 	case_id VARCHAR(100) NOT NULL,
        # 	case_name VARCHAR(200) NOT NULL,
        # 	preconditions VARCHAR(2000) NOT NULL,
        # 	case_process VARCHAR(2000) NOT NULL,
        # 	desired_result VARCHAR(2000) NOT NULL,
        # 	case_level VARCHAR(20) NOT NULL,
        # 	responsible VARCHAR(20) NOT NULL,
        # 	automation VARCHAR(20) NOT NULL,
        # 	network_type VARCHAR(100) NOT NULL,
        # 	remark VARCHAR(1000) NOT NULL,
        # 	case_path VARCHAR(500) NOT NULL,
        # 	PRIMARY KEY (id, case_id) )
        # 	ENGINE=InnoDB DEFAULT CHARSET=utf8;
        print("self.sql_cmd", self.sql_cmd)
        self.mysql.exec_sql_in_database(sql=self.sql_cmd)

        pass

def batch_update_case_interface(abs_file_path):
    batch_case = BatchUpdateCase(abs_file_path)
    batch_case.parse_excel_to_case()
    batch_case.prepare_case_to_sql()
    batch_case.write_case_sql_to_mysql()
    pass



if __name__ == "__main__":
    excel_file_path = r"E:\development_space\TestStudioCore\files\show tag支持limit和offest和like查询用例.xlsx"
    batch_case = BatchUpdateCase(excel_file_path)
    batch_case.parse_excel_to_case()
    batch_case.prepare_case_to_sql()
    batch_case.write_case_sql_to_mysql()
    pass


