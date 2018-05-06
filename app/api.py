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
