本文基于docker-compose进行python项目的docker实践。

## 一、实践环境&版本：

#### 1. Docker: 18.03.0-ce  
https://www.docker.com

#### 2. Docker Compose: 1.20.1  
https://docs.docker.com/compose/

#### 3. Python Image: 3.7.0b4  
https://hub.docker.com/r/library/python/

## 二、应具备知识：

#### 1. Python基础
https://www.w3cschool.cn/python/

#### 2. Docker基础
https://www.w3cschool.cn/docker/

#### 3. Docker Compose知识
http://wiki.jikexueyuan.com/project/docker-technology-and-combat/commands.html

#### 4. SHELL脚本基础
https://www.w3cschool.cn/shellbook/

三、目录结构

![image.png](https://upload-images.jianshu.io/upload_images/10858371-e8f5ecb0989e8dda.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/400)

目录结构截图

```
/app  # python应用目录
  api.py  # API入口脚本
/docker  # docker运行目录
  docker-compose.yml  # docker compose脚本 
  requirements.txt  # python组件清单
  run.sh  # 容器启动执行脚本
```

## 四、API入口文件样例：

### 1. api.py
```python
from flask import Flask, request

# 创建一个服务，赋值给APP
app = Flask(__name__)


# 指定接口访问的路径，支持什么请求方式get，post
@app.route('/HelloWorld', methods=['post', 'get'])
# 请求后直接拼接入参方式
def get_ss():
    # 使用request.args.get方式获取拼接的入参数据
    name = request.args.get('name')

    # 输出结果
    return 'Hello World! ' + name


app.run(host='0.0.0.0', port=8880, debug=True)
# 这个host：windows就一个网卡，可以不写，而liux有多个网卡，写成'0.0.0.0'可以接受任意网卡信息
```

## 五、Docker相关文件说明

### 1. docker-compose.yml
```yml
version: "3"  # docker-compose版本
services:
  docker-python-demo:  # docker-compose编排名称，一般同微服务名称，注意不要与其他服务重名
    image: "python:3.7.0b4"  # docker镜像名及版本
    hostname: docker-python-demo  # docker容器主机名
    container_name: docker-python-demo  # docker容器名
    volumes:  # 挂载目录
      - ../app:/app  # 项目相关
      - ../docker:/docker  # docker相关
    ports:  # 端口映射
      - "8880:8880"
    environment:  # 配置环境变量
      - TZ=Asia/Shanghai  # 设置时区
    command: bash /docker/run.sh  # 设置启动命令
    network_mode: bridge  # 网络模式：host、bridge、none等，我们使用bridge
    restart: unless-stopped  # 自动启动：unless-stopped、always等，unless-stopped为非正常停止则自动启动
#    external_links: # 外链其他服务,此处名称为docker-compose编排名
#      - mongodb
```

#### 2. requirements.txt 
一行一个
```
flask
requests
```

#### 3. run.sh
```shell
#!/bin/bash

# 使用阿里云源安装必须组件
pip install -i https://mirrors.aliyun.com/pypi/simple/ -r /docker/requirements.txt

# 运行API入口脚本
python /app/api.py
```

## 六、开始运行
在docker目录执行命名，如需后台运行，加参数 `` -d``
> docker-compose up

运行日志结果：
```log
Creating docker-python-demo ... done
Attaching to docker-python-demo
docker-python-demo    | Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
docker-python-demo    | Collecting flask (from -r /docker/requirements.txt (line 1))
docker-python-demo    |   Downloading https://mirrors.aliyun.com/pypi/packages/7f/e7/08578774ed4536d3242b14dacb4696386634607af824ea997202cd0edb4b/Flask-1.0.2-py2.py3-none-any.whl (91kB)
docker-python-demo    | Collecting requests (from -r /docker/requirements.txt (line 2))
docker-python-demo    |   Downloading https://mirrors.aliyun.com/pypi/packages/49/df/50aa1999ab9bde74656c2919d9c0c085fd2b3775fd3eca826012bef76d8c/requests-2.18.4-py2.py3-none-any.whl (88kB)
docker-python-demo    | Collecting Werkzeug>=0.14 (from flask->-r /docker/requirements.txt (line 1))
docker-python-demo    |   Downloading https://mirrors.aliyun.com/pypi/packages/20/c4/12e3e56473e52375aa29c4764e70d1b8f3efa6682bef8d0aae04fe335243/Werkzeug-0.14.1-py2.py3-none-any.whl (322kB)
docker-python-demo    | Collecting click>=5.1 (from flask->-r /docker/requirements.txt (line 1))
docker-python-demo    |   Downloading https://mirrors.aliyun.com/pypi/packages/34/c1/8806f99713ddb993c5366c362b2f908f18269f8d792aff1abfd700775a77/click-6.7-py2.py3-none-any.whl (71kB)
docker-python-demo    | Collecting itsdangerous>=0.24 (from flask->-r /docker/requirements.txt (line 1))
docker-python-demo    |   Downloading https://mirrors.aliyun.com/pypi/packages/dc/b4/a60bcdba945c00f6d608d8975131ab3f25b22f2bcfe1dab221165194b2d4/itsdangerous-0.24.tar.gz (46kB)
docker-python-demo    | Collecting Jinja2>=2.10 (from flask->-r /docker/requirements.txt (line 1))
docker-python-demo    |   Downloading https://mirrors.aliyun.com/pypi/packages/7f/ff/ae64bacdfc95f27a016a7bed8e8686763ba4d277a78ca76f32659220a731/Jinja2-2.10-py2.py3-none-any.whl (126kB)
docker-python-demo    | Collecting idna<2.7,>=2.5 (from requests->-r /docker/requirements.txt (line 2))
docker-python-demo    |   Downloading https://mirrors.aliyun.com/pypi/packages/27/cc/6dd9a3869f15c2edfab863b992838277279ce92663d334df9ecf5106f5c6/idna-2.6-py2.py3-none-any.whl (56kB)
docker-python-demo    | Collecting chardet<3.1.0,>=3.0.2 (from requests->-r /docker/requirements.txt (line 2))
docker-python-demo    |   Downloading https://mirrors.aliyun.com/pypi/packages/bc/a9/01ffebfb562e4274b6487b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl (133kB)
docker-python-demo    | Collecting urllib3<1.23,>=1.21.1 (from requests->-r /docker/requirements.txt (line 2))
docker-python-demo    |   Downloading https://mirrors.aliyun.com/pypi/packages/63/cb/6965947c13a94236f6d4b8223e21beb4d576dc72e8130bd7880f600839b8/urllib3-1.22-py2.py3-none-any.whl (132kB)
docker-python-demo    | Collecting certifi>=2017.4.17 (from requests->-r /docker/requirements.txt (line 2))
docker-python-demo    |   Downloading https://mirrors.aliyun.com/pypi/packages/7c/e6/92ad559b7192d846975fc916b65f667c7b8c3a32bea7372340bfe9a15fa5/certifi-2018.4.16-py2.py3-none-any.whl (150kB)
docker-python-demo    | Collecting MarkupSafe>=0.23 (from Jinja2>=2.10->flask->-r /docker/requirements.txt (line 1))
docker-python-demo    |   Downloading https://mirrors.aliyun.com/pypi/packages/4d/de/32d741db316d8fdb7680822dd37001ef7a448255de9699ab4bfcbdf4172b/MarkupSafe-1.0.tar.gz
docker-python-demo    | Building wheels for collected packages: itsdangerous, MarkupSafe
docker-python-demo    |   Running setup.py bdist_wheel for itsdangerous: started
docker-python-demo    |   Running setup.py bdist_wheel for itsdangerous: finished with status 'done'
docker-python-demo    |   Stored in directory: /root/.cache/pip/wheels/53/d7/48/a1f187b9001bf967a6e4eaf925b96b1a928b9136f0df691c6d
docker-python-demo    |   Running setup.py bdist_wheel for MarkupSafe: started
docker-python-demo    |   Running setup.py bdist_wheel for MarkupSafe: finished with status 'done'
docker-python-demo    |   Stored in directory: /root/.cache/pip/wheels/e8/91/a5/449fc7a22f10717491d290617cd827aaacb3b72555e7c394f8
docker-python-demo    | Successfully built itsdangerous MarkupSafe
docker-python-demo    | Installing collected packages: Werkzeug, click, itsdangerous, MarkupSafe, Jinja2, flask, idna, chardet, urllib3, certifi, requests
docker-python-demo    | Successfully installed Jinja2-2.10 MarkupSafe-1.0 Werkzeug-0.14.1 certifi-2018.4.16 chardet-3.0.4 click-6.7 flask-1.0.2 idna-2.6 itsdangerous-0.24 requests-2.18.4 urllib3-1.22
docker-python-demo    |  * Serving Flask app "api" (lazy loading)
docker-python-demo    |  * Environment: production
docker-python-demo    |    WARNING: Do not use the development server in a production environment.
docker-python-demo    |    Use a production WSGI server instead.
docker-python-demo    |  * Debug mode: on
docker-python-demo    |  * Running on http://0.0.0.0:8880/ (Press CTRL+C to quit)
docker-python-demo    |  * Restarting with stat
docker-python-demo    |  * Debugger is active!
docker-python-demo    |  * Debugger PIN: 211-677-763
```

## 七、结果验证
在浏览器中访问：
> http://127.0.0.1:8880/HelloWorld?name=2018

返回结果：
> Hello World! 2018

大功告成！！！

## 八、demo文件

> https://github.com/jason-sun/docker-python-demo