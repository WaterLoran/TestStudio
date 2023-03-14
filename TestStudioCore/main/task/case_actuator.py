# -*- coding: utf-8 -*-
import platform
import time
from utils.linux_shell import LinuxShell
from utils.file_search_engine import FileSearchEngine
from report.report_management import ReportManagement
from main.task.task_manage import create_test_task_interface
from ..plugins.my_email import get_allure_screenshot_and_send_mail


class CaseActuator:
    def __init__(self):
        self.shell = LinuxShell()
        self.search = FileSearchEngine()
        pass

    def exec_case_by_file_path(self, file_path_list):
        cmd_list = ["cd /usr/local/AutoTEST;", "pytest -v"]
        # file_path_list = ["./func_1/test_1_1.py", "./func_1/test_1_2.py"]
        cmd_list += file_path_list
        # --alluredir=E:\development_space\AutoTEST\allure-result # TODO
        if platform.system() == "Windows":
            allure_part_cmd = [r"--alluredir=E:\development_space\AutoTEST\allure-result"]
        else:  # 如果不是Windows系统的话
            allure_part_cmd = [r"--alluredir=/usr/local/AutoTEST/allure-result"]
        cmd_list += allure_part_cmd

        # TODO 这里要去判断系统类型,然后指定路径
        cmd = " ".join(cmd_list)
        print("执行用例的命令是", cmd)
        logs = self.shell.exec_cmd(cmd=cmd)
        print("logs", logs)
        pass

    # files = self.search.get_all_py_file("/usr/local/AutoTEST")

    def exec_case_by_case_id(self, case_id_list):
        if platform.system() == "Windows":
            files = self.search.get_all_py_file("E:\development_space\AutoTEST")
        else:  # 如果不是Windows系统的话
            files = self.search.get_all_py_file("/usr/local/AutoTEST")
        # TODO 这里要去判断系统类型,然后指定路径

        exec_cases = []
        print("case_id_list", case_id_list)
        print("files", files)
        for case_id in case_id_list:
            files_to_remove = []
            for file in files:
                if case_id in file:
                    exec_cases.append(file)
                    files_to_remove.append(file)
                    break
            for file in files_to_remove:
                files.remove(file)

        print("exec_cases", exec_cases)
        self.exec_case_by_file_path(exec_cases)
        pass

    def exec_case_by_case_priority(self, case_priority):
        pass

    def find_case_path_by_case_id(self):
        pass

    def find_case_path_by_case_priority(self):
        pass

def execute_case_interface(case_id_list, test_task_id):

    print("================================================================================")
    print("case_id_list", case_id_list)

    # 创建测试任务,用于记录测试详情
    temp_test_task_id = create_test_task_interface(case_id_list, test_task_id)
    if test_task_id == "":
        test_task_id = temp_test_task_id
    print("test_task_id", test_task_id)

    report = ReportManagement()
    report.rm_rf_allure_result_report()

    # 执行脚本
    case = CaseActuator()
    case.exec_case_by_case_id(case_id_list)

    time.sleep(30)
    report.start_report()

    # # 调用发送邮件的接口去发送邮件
    get_allure_screenshot_and_send_mail()



if __name__ == "__main__":
    case_id_list = ["test_1_1", "test_1_2"]
    execute_case_interface(case_id_list, 19961996)





