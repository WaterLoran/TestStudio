# -*- coding: utf-8 -*-

class BaseConfig:
    def __init__(self):
        self.para_order = ["层级", "特性", "用例ID", "用例名称", "前置条件", "用例过程", "期望结果", "用例级别", "责任人", "自动化", "组网类型", "备注","脚本路径"]
        self.para_order_en = ["level", "feature", "case_id", "case_name", "preconditions", "case_process", "desired_result", "case_level", "responsible", "automation", "network_type", "remark", "case_path"]