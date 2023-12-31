# By 张程功
# 2023-07-06
# 主要功能:每日更新下修可转债的基本信息
# 手动模式

import pandas as pd
import numpy as np
import pickle
import time
import os
from datetime import datetime
from operator import itemgetter

data_folder_path = '../'
raw_data_path = "../raw_data"
storage_path = "../database_storage"
daily_path = "../daily"
DTBS_path = os.path.join(storage_path, "DTBS.pkl")
DCBS_path = os.path.join(storage_path, "DCBS.pkl")
# re-open
with open(DCBS_path, 'rb') as f:
    DCBS = pickle.load(f)
# re-open
with open(DTBS_path, 'rb') as f:
    DTBS = pickle.load(f)

# 通过转债代码查询相对应的正股代码、正股名称，根据需要修改需要查询的可转债代码、日期、季度 bond_code、query_date、query_quarter
bond_code = '113644.SH'
query_date = '2023-09-12'
query_quarter = '2023-03'

stock_code = DTBS['B'][bond_code]['sc']
cn = DTBS['B'][bond_code]['cn']

# 以下查询并输出货币资金、债券余额、到期期限、大股东名称及是否为国企等信息
# hb 货币资金
if DTBS['F'].get(stock_code, 'F区未存储对应正股信息') == 'F区未存储对应正股信息':
    hb = 'F区未存储对应正股的货币资金信息'
    print('F区未存储对应正股的货币资金信息')
else:
    hb = DTBS['F'][stock_code][query_quarter]['hb']
    print(DTBS['F'][stock_code][query_quarter])

# bl 债券余额, yl 到期期限
bl = DTBS['A'][bond_code][query_date]['bl']
yl = DTBS['A'][bond_code][query_date]['yl']
print(DTBS['A'][bond_code][query_date])

# dgd 大股东名称
if DTBS['G'].get(stock_code, 'G区未存储对应正股信息') == 'G区未存储对应正股信息':
    dgd = 'G区未存储对应正股的大股东信息'
    print('G区未存储对应正股的大股东信息')
else:
    dgd = DTBS['G'][stock_code]['dgd']
    print(DTBS['G'][stock_code])

# gq 是否为国企（1 代表是，0 代表否）
gq = DTBS['B'][bond_code].get('gq', 'B区未存储正股是否为国企的信息')
company_nature = DTBS['B'][bond_code].get('company_nature', 'B区未存储正股的公司属性')
print(DTBS['B'][bond_code])

# 打印信息，大股东是否持有需要根据wind手动判断一下
if gq == 0:
    print(cn, bond_code, '：现金', round(hb, 3), '亿，债券余额', bl, '亿，到期期限', yl, '年，', '大股东', dgd, ', 是',
          company_nature, '，不是国企')
else:
    print(cn, bond_code, '：现金', round(hb, 3), '亿，债券余额', bl, '亿，到期期限', yl, '年，', '大股东', dgd, ', 是',
          company_nature, '，是国企')
