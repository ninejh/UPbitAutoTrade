from numpy.lib.stride_tricks import as_strided
import pyupbit
import pandas as pd
import os
import time
import datetime
from pyupbit.exchange_api import Upbit
import msvcrt

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(access_key, secret_key,ticker):
    upbit = pyupbit.Upbit(access_key,secret_key) 
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def autotrade(access_key, secret_key):
    print("자동매매를 시작하겠습니다.")
    auto_coin=input("자동매매를 시작할 코인의 티커(ticker)를 입력하시오: ")
    print(auto_coin,"에 대한 자동매매를 시작합니다.(아무 키나 입력 시 종료합니다)")
    coin_service = "KRW-"+auto_coin 
    while True:
        
        try:
            now = datetime.datetime.now()
            start_time = get_start_time(coin_service)
            end_time = start_time + datetime.timedelta(days=1)

            if start_time < now < end_time - datetime.timedelta(seconds=10):
                target_price = get_target_price(coin_service, 0.5)
                ma15 = get_ma15(coin_service)
                current_price = pyupbit.get_current_price(coin_service)
                if target_price < current_price and ma15 < current_price:
                    krw = get_balance(access_key,secret_key,"KRW")
                    if krw > 5000:
                        auto_buy(access_key, secret_key, coin_service, krw)
            else:
                coin = get_balance(access_key,secret_key,auto_coin)
                if coin > 0.00008:
                    auto_sell(access_key,secret_key,coin_service,coin)
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)
        if msvcrt.kbhit():
            break
        

def get_ma15(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def account(access_key,secret_key):
    upbit = pyupbit.Upbit(access_key, secret_key)
    balance_df=pd.DataFrame(upbit.get_balances())
    print(balance_df)

def current_price():
    coin=input("\n조회하고 싶은 코인의 티커(ticker)를 입력하시오: ")
    value = "KRW-"+ coin
    price = pyupbit.get_current_price(value) 
    print(price)

def buy(access_key,secret_key):
    buy_coin=input("\n매수하고 싶은 코인의 티커(ticker)를 입력하시오(최소주문금액5000원이상): ")
    price=input("매수 호가를 입력하시오: ")
    size=input("매수량을 입력하시오: ")
    buy_coin = "KRW-"+ buy_coin
    upbit = pyupbit.Upbit(access_key,secret_key) 
    value=input("확인:1 취소:2  ")
    if (value=='1'):
        ret = upbit.buy_limit_order(buy_coin,price,size)
        print(ret)
    elif (value=='2'):
        return 0
    else:
        print("잘못입력하였습니다.")

def auto_buy(access_key,secret_key,coin_service,krw):
        upbit = pyupbit.Upbit(access_key,secret_key)
        upbit.buy_market_order(coin_service, krw*0.9995)
        print("매수하였습니다.") 
    
def sell(access_key,secret_key):
    sell_coin=input("\n매도하고 싶은 코인의 티커(ticker)를 입력하시오(최소주문금액5000원이상): ")
    price=input("매도 호가를 입력하시오: ")
    size=input("매도량을 입력하시오: ")
    sell_coin = "KRW-"+sell_coin
    upbit = pyupbit.Upbit(access_key,secret_key)
    value=input("확인:1 취소:2  ")
    if (value=='1'):
        ret = upbit.sell_limit_order(sell_coin,price,size) 
        print(ret)
    elif (value=='2'):
        return 0
    else:
        print("잘못입력하였습니다.")

def auto_sell(access_key,secret_key,coin_service,coin):
    upbit = pyupbit.Upbit(access_key,secret_key)
    upbit.sell_market_order(coin_service, coin*0.9995)
    print("매도하였습니다.")

def clean():
    user_clean=input("\n화면 지우기:1 \n화면 유지: 1을 제외한 아무키\n")
    if (user_clean=='1'):
        print("5초후에 화면이 지워집니다.")
        time.sleep(5)
        os.system('cls')
        
def cancel_order(access_key, secret_key):
    upbit = pyupbit.Upbit(access_key,secret_key)
    coin=input("주문 취소할 코인의 티커(ticker)를 입력하시오: ")
    cancel_coin="KRW-"+coin
    ret=upbit.get_order(cancel_coin)
    print(ret)
    print("\n[{'uuid' : 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', 에서 x부분이 취소 코드입니다.")
    code=input("주문을 취소하고 싶다면 코드를 그대로 입력해주세요(-)포함: ")
    upbit.cancel_order(code)    

def cherck_order(access_key, secret_key):
    check_coin=input(("\n 주문 내역을 확인하고 싶은 코인의 티커(ticker)를 입력하세요"))
    upbit = pyupbit.Upbit(access_key,secret_key)
    check_coin="krw-"+check_coin
    ret=upbit.get_order(check_coin)
    print("\n",check_coin,"의 주문 내역입니다.")
    print(ret)







print("====================UPbit거래 프로그램입니다====================")


print("\n업비트 access_key와 secret_key를 얻는 법")

upbit_user=input("알고 있다면 아무키나 모른다면 1을 입력하세요: ")
if(upbit_user=='1'):
    print("\n1.업비트 사이트에서 오른쪽 맨아래에 있는 open API를 클릭") 
    print("2.open API 사용하기 클릭")
    print("3.계정로그인")
    print("4.자산조회, 주문조회, 주문하기, 특정IP에서만 실행 클릭")
    print("5.자신의 IP주소를 입력하고 OPEN API Key 발급받기 클릭")
    print("6.발급된 자신의 key 이용하기")
    upbit_user=input("\n완료되었다면 아무키나 입력하세요")
    os.system('cls')

else:
    os.system('cls')





print("====================UPbit거래 프로그램 시작====================")
access_key=input("\n업비트 access_key를 입력하시오: ")

secret_key=input("업비트 secret_key를 입력하시오: ")







while(1):
    print("\n1. 잔고 조회 ")
    print("2. 원하는 코인 현재가 조회 ")
    print("3. 코인 매수하기 ")
    print("4. 코인 매도하기")
    print("5. 주문내역 조회하기")
    print("6. 주문 취소하기")
    print("7. 코인 자동매매하기")
    print("8. 프로그램 종료하기\n")
    value=(input("원하는 행동을 고르시오(숫자): "))

    if(value=='1'):
        account(access_key,secret_key)
        clean()  

    if(value=='2'):
        current_price()
        clean()

    if(value=='3'):
        buy(access_key,secret_key)
        clean()

    if(value=='4'):      
        sell(access_key,secret_key)
        clean()
    
    if(value=='5'):
        cherck_order(access_key, secret_key)

    if(value=='6'):
        cancel_order(access_key,secret_key)
        clean()

    if(value=='7'):
        autotrade(access_key,secret_key)
        clean()

    if(value=='8'):
        break





