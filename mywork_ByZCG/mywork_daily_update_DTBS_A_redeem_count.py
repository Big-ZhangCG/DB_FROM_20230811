import requests
import pickle
import datetime

login_header = {
    "origin": "https://www.jisilu.cn",
    "Referer": "https://www.jisilu.cn/account/login/",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44"
}
login_url = 'https://www.jisilu.cn/webapi/account/login_process/'
login_info = {
   "return_url": "https://www.jisilu.cn/",
   "user_name": "d0cb8eb409b54ff8444593da78e20495",
   "password": "09e373cb61c6dc7d2f9ca59fdc996067",
   "aes": 1,
   "auto_login": 0
}


session = requests.session()

session.post(login_url, data = login_info, headers = login_header)
data_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44'
}

# 获取强赎信息
data_url = "https://www.jisilu.cn/data/cbnew/redeem_list/?___jsl=LST___t=1693531044474"

# retrieve data
# data_response =  session.get(data_url, headers = try_header)
data_response = session.get(data_url, headers=data_header)

data = data_response.json()

# 将原始信息存储到字典中
mapping = {}
for row in data['rows']:
    bond_code = row['id']
    cell = row['cell']
    mapping[bond_code] = cell
    print(row)


# 更换数据库地址
DTBS_path = '..\\database_storage\\DTBS.pkl'
DCBS_path = '..\\database_storage\\DCBS.pkl'

# re-open
with open(DCBS_path, 'rb') as f:
    DCBS = pickle.load(f)
# re-open
with open(DTBS_path, 'rb') as f:
    DTBS = pickle.load(f)


# 获取今天的日期
today = str(datetime.date.today())
print(today)

# 将强赎信息写入DTBS中
for bond_code, informations in DTBS['A'].items():
    print('\n', bond_code)
    if informations.get(today, False) and (informations[today]['ia'] == 1):
        print(DTBS['A'][bond_code][today])
        if mapping[bond_code[:6]].get('force_redeem', False):
            DTBS['A'][bond_code][today]['redeem_count'] = mapping[bond_code[:6]]['force_redeem']
        else:
            DTBS['A'][bond_code][today]['redeem_count'] = mapping[bond_code[:6]]['redeem_count'].replace("<br>", "，").\
                replace('<span title="未到转股期" style="color:gray;">', '未到转股期，').replace('</span>', '').\
                replace('<span style="color:blue;">!', '')
        print(DTBS['A'][bond_code][today])
    else:
        print('这只转债在本日不活跃')

# 保存上面的这些信息的更改
f_save = open(DTBS_path, 'wb')
pickle.dump(DTBS, f_save)
f_save.close()

print('强赎信息存储完毕')
