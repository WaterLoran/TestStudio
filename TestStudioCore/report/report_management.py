# -*- coding: utf-8 -*-
from utils.linux_shell import LinuxShell

class ReportManagement:
    def __init__(self):
        self.shell = LinuxShell()
        pass

    def rm_rf_allure_result_report(self):
        cmd = "cd /usr/local/AutoTEST; rm -rf allure*;"
        logs = self.shell.exec_cmd(cmd=cmd)
        print("logs", logs)

    def start_report(self):
        cmd = "kill -9 $(ps -ef|grep allure|gawk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ')"
        logs = self.shell.exec_cmd(cmd=cmd)
        print("logs", logs)

        cmd = "nohup allure generate /usr/local/AutoTEST/allure-result -o /usr/local/AutoTEST/allure_report --clean &  \n"
        print("将要生成测试报告文件cmd", cmd)
        logs = self.shell.exec_cmd_by_invoke(cmd=cmd)
        print("logs", logs)

        cmd = 'nohup allure open -h 192.168.0.106 -p 8066 /usr/local/AutoTEST/allure_report & \n'
        print("使用nohup拉起报告cmd", cmd)
        self.shell.exec_cmd_by_invoke(cmd=cmd)


        pass
