# -*- coding:utf-8 -*-

import json
import pandas as pd

with open('./录屏数据.json', 'r') as f:
    jd = json.load(f)

browser = []
country = []
size = []

for d in jd['recordings']:
    browser.append(d['browser'])
    country.append(d['country_code'])
    size.append(d['window_size'])

data = {
    'browser':browser,
    'country':country,
    'size':size
}

df = pd.DataFrame(data)
df.to_excel('1.xlsx', index=False)

print('over')
