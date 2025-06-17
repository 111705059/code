import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random as ra
##導入需要資料並取出price
df=pd.read_csv('xxx.csv')
data=df.values
price=data[:,3]
from ast import Constant
##策略一:buy and hold
def strategy1(price):
  return (price[-1]-price[0])*200
##策略二:buy and hold+停損
def strategy2(price,sl_rate):##新增停損點stoploss->sl 
  cost=price[0]##成本
  slp=int(cost*(1-sl_rate))
  for i in range(285):
    final_price=price[i]
    if price[i]<=slp:
      break
  return (final_price-cost)*200
##策略三:buy and hold+停損停利
def strategy3(price,sl_rate,sp_rate):##新增停損點stop_profit->sp 
  cost=price[0]##成本
  slp=int(cost*(1-sl_rate))
  spp=int(cost*(1+sp_rate))
  for i in range(285):
    final_price=price[i]
    if price[i]<=slp:
      break
    elif price[i]>=spp:
      break
  return (final_price-cost)*200
##策略四:葛蘭碧交易法則
def strategy4(price):
  ma5=[0]*4
  cost=price[0]
  position=0#空手、平方、空倉
  r=0#reward
  for i in range(281):#前5筆不記
    ma5.append(np.mean(price[i:i+5]))##均線 price[0]～price[4]平均.....
  for i in range(6,285):#前5筆沒有均線
    #Buy
    if price[i-1]<=ma5[i-1] and price[i]>ma5[i] and ma5[i-2]>ma5[i-1] and ma5[i]>ma5[i-1]:##突破:前一時段均線>price 現時段price>均線 平均線轉漲:前兩時段平郡>前一時段平均且現時段平均>前一時段平均v型        
      if position==0:
        position=1
        cost=price[i]
      elif position==-1:
        position=0
        r += (cost-price[i])*200#先賣在成本價 在現在的價錢買入
    #sell
    if price[i-1]>=ma5[i-1] and price[i]<ma5[i] and ma5[i-2]<ma5[i-1] and ma5[i]<ma5[i-1]:##跌破:與突破相反 平均線轉跌:倒v型
      if position==0:
        position=-1
        cost=price[i]
      elif position==1:
        position=0
        r += (price[i]-cost)*200#先買在成本價 在現在價錢賣出
  if position==1: ##做完整天交易後多一口->收盤清倉
    r+=(price[-1]-cost)*200 ##每天最後一筆價錢時賣出-成本買入    
  elif position==-1:##做完整天交易後空方->收盤平倉
    r+=(cost-price[-1])*200##成本賣出-每天最後一筆價錢時買入
  return r
##策略五: random單日隨機時間買賣
def strategy5(price):
  buytime=ra.randint(0,284)
  selltime=ra.randint(0,284)
  if buytime>selltime:
    a=buytime
    buytime=selltime
    selltime=a
  r=price[selltime]-price[buytime]
  return r  
##結果與繪圖分析
# 初始化
strategy_funcs = [
    lambda p: strategy1(p),
    lambda p: strategy2(p, 0.01),
    lambda p: strategy3(p, 0.01, 0.04),
    lambda p: strategy4(p),
    lambda p: strategy5(p),
]

pnl_all = [[] for _ in range(5)]
acc_profits = [0] * 5
max_profits = [float('-inf')] * 5
max_losses = [float('inf')] * 5

# 模擬 245 天
for i in range(245):
    p = price[i * 285:(i + 1) * 285]
    for idx, func in enumerate(strategy_funcs):
        profit = func(p)
        pnl_all[idx].append(profit)
        acc_profits[idx] += profit
        max_profits[idx] = max(max_profits[idx], profit)
        max_losses[idx] = min(max_losses[idx], profit)

# 輸出
for i in range(5):
    print(f"策略{i+1} 累積獲利:{acc_profits[i]:.2f}, 最大獲利:{max_profits[i]:.2f}, 最大虧損:{max_losses[i]:.2f}")
# 策略函數清單（可擴充）
strategy_funcs = [
    lambda p: strategy1(p),
    lambda p: strategy2(p, 0.01),
    lambda p: strategy3(p, 0.01, 0.04),
    lambda p: strategy4(p),
    lambda p: strategy5(p),
]

# 累積獲利與時間序列初始化
acc_profits = [0] * 5
pnl_paths = [[] for _ in range(5)]

# 逐天模擬
for i in range(245):
    p = price[i * 285:(i + 1) * 285]
    for idx, func in enumerate(strategy_funcs):
        acc_profits[idx] += func(p)
        pnl_paths[idx].append(acc_profits[idx])

# 畫圖：策略1~4
for i in range(4):
    plt.plot(pnl_paths[i], label=f'strategy{i+1}')
plt.xlabel("days")
plt.title("total accumulated profit")
plt.legend()
plt.show()

# 畫圖：策略5單獨
plt.plot(pnl_paths[4], label='strategy5')
plt.xlabel("days")
plt.title("total accumulated profit")
plt.legend()
plt.show()
