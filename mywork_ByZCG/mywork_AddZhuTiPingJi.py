import pandas as pd
import numpy as np
import pickle
import time
import os
from datetime import datetime
from operator import itemgetter
from WindPy import w

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

# 更新主体评级的日期（按季度） 2023-03
time = '2023-03'
date = '2023-03-01'

w.start()

# 将DTBS的F区的键取出，即取出所有的正股代码，并将其都存到一个列表stock_codes
stock_codes = list(DTBS['F'].keys())
print(stock_codes)

# 调用wind接口，获取正股对应的主体评级，传入一个列表stock_codes，传出数据格式为：[[主体评级1,主体评级2,...]]
Wind_ZhuTiPingJi = w.wsd(stock_codes, "latestissurercreditrating", date, date, "").Data
print(Wind_ZhuTiPingJi)

# 对DTBS的F区增加主体评级
for i in range(len(stock_codes)):
    DTBS['F'][stock_codes[i]][time]['ztpj'] = Wind_ZhuTiPingJi[0][i]


# 保存到数据库DTBS中
f_save = open(DTBS_path, 'wb')
pickle.dump(DTBS, f_save)
f_save.close()


