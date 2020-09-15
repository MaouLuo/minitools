import pandas as pd
import requests
import json
import time 
import tools
import numpy as np

data = pd.read_excel('./最近半年船名.xlsx', index=False)
ship_name = [n for n in data['vessel']]
amount = len(ship_name)
num = 1
res_list = []
dd = tools.Dingding()
frame = pd.DataFrame(columns=('Vessel','num','ShipID', 'MatchType', 'mmsi', 'shiptype', 'name', 'callsign', 'imo', 'lasttime'))


def query_ship(sn):
    global frame
    url = 'http://api.shipdt.com/DataApiServer/apicall/QueryShip'
    params={
        'k': 'd3122724f649428cb362fe030d2b9fb4',
        'kw': sn,
        'max':50
    }
    try:
        resp = requests.get(url, params=params)
    except Exception as e:
        print('api err:{}'.format(e))
        dd.send_text('api err:{}'.format(e))
    jd = json.loads(resp.text)    

    if jd['status'] == 0:
        #res_list.append({'vessel':sn, 'num':len(jd['data'])})
        for r in jd['data']:
            if 70 <= r['shiptype'] <= 79:        
                ship = pd.DataFrame([[sn,len(jd['data']),r['ShipID'], r['MatchType'], r['mmsi'], r['shiptype'], r['name'], r['callsign'], r['imo'], r['lasttime']]], columns=('Vessel','num','ShipID', 'MatchType', 'mmsi', 'shiptype', 'name', 'callsign', 'imo', 'lasttime'))
                frame = frame.append(ship, ignore_index=False)
        #print('{} has {} data'.format(ship_name, len(jd['data'])))        
    else:
        ship = pd.DataFrame([[sn, 0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]], columns=('Vessel', 'num', 'ShipID', 'MatchType', 'mmsi', 'shiptype', 'name', 'callsign', 'imo', 'lasttime'))
        frame = frame.append(ship, ignore_index=False)
        #res_list.append({'vessel':sn, 'num':0})
        #print('{} data error'.format(ship_name))
    time.sleep(0.1)
    #return frame

    

def main():
    global num
    global frame

    s = time.time()
    try:
        for n in ship_name:
            query_ship(n)
            tools.bar(amount, num)
            num += 1
    except Exception as e:
        print('ergodic err:{}'.format(e))
        dd.send_text('ergodic err:{}'.format(e))
            
    #df = pd.DataFrame(res_list)
    #print(len(res_list))

    try:
        frame.to_excel('./船只查询结果.xlsx',index=False)
    except Exception as e:
        print('save excel  err:{}'.format(e))        
        dd.send_text('save excel err:{}'.format(e))

    e = time.time()
    print('\ntime:{}'.format(e-s))
    #dd.send_text('check ship name, total {}, check {}, use time {}'.format(len(ship_name) ,len(res_list), e-s))
    dd.send_text('check ship name, total {}, get {}, use time {}'.format(len(ship_name) , frame.shape[0], e-s))


if __name__ == '__main__':
    main()