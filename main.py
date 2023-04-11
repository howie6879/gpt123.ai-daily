"""
    Created by howie.hu at 2021-10-30.
    Description: 周刊初始化脚本
    Changelog: all notable changes to this file will be documented
"""
import os

import yaml


def read_mkdocs_config(path=""):
    """读取mkdocs配置

    Args:
        path (str): 可选，mkdocs配置路径
    """
    config_path = path or os.path.join(os.path.dirname(__file__), "mkdocs.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        result = f.read()
        return yaml.load(result, Loader=yaml.FullLoader)


def write_mkdocs_config(data: dict, path=""):
    """写入mkdocs配置

    Args:
        data (dict): 配置数据
        path (str): 可选，mkdocs配置路径
    """
    config_path = path or os.path.join(os.path.dirname(__file__), "mkdocs.yml")
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)


def gen_daily_title(years: int):
    """生成周刊标题

    Args:
        years (int): 年份
    """
    root_path = os.path.dirname(__file__)
    target_path = os.path.join(root_path, f"docs/{years}")
    res_dict = {}
    for file_name in os.listdir(target_path):
        if str(file_name).endswith(".md"):
            # 目标文件
            title = str(file_name).split(".md", maxsplit=1)[0]
            res_dict[title] = {
                "file_name": file_name,
                "title": title,
            }

    res_list = []
    for i in sorted(res_dict):
        file_data_dict: dict() = res_dict[i]
        print(f"- {file_data_dict['title']}: ./{years}/{file_data_dict['file_name']}")
        res_list.append(
            {
                f"{file_data_dict['title']} 日报": f"./{years}/{file_data_dict['file_name']}"
            }
        )

    # 获取yaml配置
    mkdocs_config = read_mkdocs_config()
    # 赋值
    for each in mkdocs_config["nav"]:
        for key, _ in each.items():
            if str(years) in key:
                # 倒序
                each[key] = res_list[::-1]
    # 写入新配置
    write_mkdocs_config(mkdocs_config)


if __name__ == "__main__":
    # 生成最新日报
    gen_daily_title(2023)
