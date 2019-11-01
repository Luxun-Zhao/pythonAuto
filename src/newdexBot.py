import src.request as request
import json
import src.config as config

def getBestPrice():
    depthData = json.loads(request.depth())['data']
    bids = depthData['bids'][0]
    asks = depthData['asks'][-1]
    return {"bids":bids[0], "asks":asks[0]}

def getLastFilledOrder():
    ordersData = json.loads(request.orders(state="filled"))['data']
    last = ordersData[0]
    return last

if __name__ == '__main__':
    oldPrice = {'bids':0,'asks':0}#getBestPrice()
    oldOrder = getLastFilledOrder()
    while(1):
        newPrice = getBestPrice()
        if oldPrice['bids'] != newPrice['bids']:
            request.sendMessage("买一价格：" + str(newPrice['bids']))
            oldPrice['bids'] = newPrice['bids']
        if oldPrice['asks'] != newPrice['asks']:
            request.sendMessage("卖一价格：" + str(newPrice['asks']))
            oldPrice['asks'] = newPrice['asks']

        newOrder = getLastFilledOrder()
        if oldOrder['id'] != newOrder['id']:
            request.sendMessage("新单成交")
            oldOrder = newOrder
