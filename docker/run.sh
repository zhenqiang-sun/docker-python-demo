#!/bin/bash

# 使用阿里云源安装必须组件
pip install -i https://mirrors.aliyun.com/pypi/simple/ -r /docker/requirements.txt

# 运行API入口脚本
python /app/api.py