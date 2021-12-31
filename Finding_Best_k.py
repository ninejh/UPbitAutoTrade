import pyupbit
import numpy as np


coin = input("K값을 구하고 싶은 코인의 티커(ticker)를 입력하시오: ")
coin = "KRW-" + coin
def get_ror(k=0.5):
    df = pyupbit.get_ohlcv(coin,count=7)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror


for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k)
    print("%.1f %f" % (k, ror))