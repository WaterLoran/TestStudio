# -*- coding: utf-8 -*-
import paramiko
import logging
import os
import re
import time

class LinuxShell:
    def __init__(self, vm_ip="192.168.0.106"):
        self.vm_ip = vm_ip
        self.username = "root"
        # TODO 这里有密码,上传代码时候需要先处理
        self.password = "feng1996"
        self.ssh_port = 22
        pass

    def exec_cmd(self, cmd=""):
        if cmd == "":
            logging.error("The command to be executed needs to be passed in when calling the function")
            assert False
        logging.info("exec_cmd::cmd ==> {}".format(cmd))
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.vm_ip, self.ssh_port, self.username, self.password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        logs = stdout.readlines()  # Reading std is a necessary action to trigger the actual execution of the command
        logging.info("exec_cmd::logs ==> {}".format(logs))
        return logs

    def exec_cmd_use_nohup(self, cmd=""):
        if cmd == "":
            logging.error("The command to be executed needs to be passed in when calling the function")
            assert False
        cmd = "nohup {} &".format(cmd)
        logging.info("exec_cmd_use_nohup::cmd ==> {}".format(cmd))
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.vm_ip, self.ssh_port, self.username, self.password)
        stdin, stdout, stderr = ssh.exec_command(cmd)

    def exec_cmd_except_keyword(self, cmd="", keyword="", success_log="", fail_log=""):
        if cmd == "":
            logging.error("The command to be executed needs to be passed in when calling the function")
            assert False

        logging.info("exec_cmd_except_keyword::cmd ==> {}".format(cmd))
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.vm_ip, self.ssh_port, self.username, self.password)
        stdin, stdout, stderr = ssh.exec_command(cmd)

        stdout_list = stdout.readlines()
        stdout_all_content = "".join(stdout_list)
        if keyword != "":
            if bool(re.search(keyword, stdout_all_content)) == True:
                if success_log != "":
                    logging.info(success_log)
                ssh.close()
                return True
            else:
                if fail_log != "":
                    logging.error(fail_log)
                ssh.close()
                logging.info("exec_cmd_except_keyword::stdout_list ==> {}".format(stdout_list))
                logging.info("exec_cmd_except_keyword::keyword ==> {}".format(keyword))
                assert False
        return True

    def exec_cmd_by_invoke(self, cmd=""):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.vm_ip, self.ssh_port, self.username, self.password)
        chan = ssh.invoke_shell()
        chan.send(cmd)
        time.sleep(1)

