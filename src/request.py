import time
import requests
import hmac
from hashlib import sha256
import src.config as config

# 获取配置信息
conf=config.readConf("kuzoo")
api_key=conf.get("newdexBot",'api_key')
secret_key=conf.get("newdexBot",'secret_key').encode("utf-8")
url=conf.get("newdexBot",'url')
symbol=conf.get("newdexBot",'symbol')

def getNewdexReq(command,params={}):# params为key value

    # 请求时间
    params["timestamp"] = str(int(time.time()))
    params["api_key"] = api_key

    # 签名数据准备
    beforeSign=""
    for i in sorted (params) :
        beforeSign = beforeSign + "&" + i + "=" + params[i]

    # 签名 HmacSHA256
    signHmac=hmac.new(secret_key, beforeSign[1:].encode('utf-8'), digestmod=sha256)

    reqUrl = url+ command +"?"+beforeSign[1:] + "&sign=" + signHmac.hexdigest()
    headers = {"Content-Type":"application/json"}
    res = requests.get(reqUrl, headers=headers)
    return res

def symbols():# 获取所有交易对列表
    return getNewdexReq("/v1/common/symbols",{}).text

def ticker(symbol=symbol):# 获取单个交易对行情
    return getNewdexReq("/v1/ticker",{"symbol":symbol}).text

def tickers():# 获取所有交易对的行情
    return getNewdexReq("/v1/tickers",{}).text

def price(symbol=symbol):# 获取所有交易对的价格
    return getNewdexReq("/v1/price",{"symbol":symbol}).text

def depth(symbol=symbol):# 获取交易订单簿（交易深度）
    return getNewdexReq("/v1/depth",{"symbol":symbol}).text

def trades(symbol=symbol):# 获取交易对的成交记录
    return getNewdexReq("/v1/trades",{"symbol":symbol}).text

def candles(symbol=symbol):# 获取交易对的K线数据
    return getNewdexReq("/v1/candles",{"symbol":symbol}).text

# pending（挂单中,默认），filled（已成交），canceled（已撤单），history（包括filled以及canceled）
def orders(state='pending', symbol=symbol):# 获取订单数据
    return getNewdexReq("/v1/order/orders",{"state":state, "symbol":symbol}).text

def sendMessage(text):# 向telegram发送消息
    requests.get("https://api.telegram.org/bot" + conf.get('telBot','token')
                 + "/sendMessage?chat_id=" + conf.get('telBot','chat_id')
                 + "&text=" + text)
