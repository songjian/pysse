import pandas as pd
import requests
import time
import math
import random
import json
import re
import argparse

headers = {'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/56.0.2924.87 Safari/537.36',
           'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
           }

def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')

def common_query(**data):
    url = 'http://query.sse.com.cn/commonQuery.do'
    data['jsonCallBack'] = 'jsonpCallback' + \
        str(math.floor(1e5 * random.random()))
    data['_'] = str(int(round(time.time() * 1000)))
    data['isPagination'] = 'false'
    r = requests.get(url, params=data, headers=headers)
    return loads_jsonp(r.text)

def bond(BOND_TYPE, BOND_CODE=''):
    """
    BOND_TYPE='可转换公司债券',
    """
    r = common_query(
        sqlId='COMMON_SSE_CP_ZQ_KZZLB_L',
        BOND_CODE=BOND_CODE,
        BOND_TYPE=BOND_TYPE,
    )
    return r

def kzhgszq(BOND_CODE):
    """可转换公司债券
    """
    # print(bond('可转换公司债券', BOND_CODE)['result'][0])
    ret=bond('可转换公司债券', BOND_CODE)
    for r in ret['result']:
        print(r['BOND_CODE'], r['BOND_ABBR'], r['TERM_YEAR'], r['ISSUE_VALUE'], r['START_DATE'], r['END_DATE'])

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('code', help='债券代码', nargs='?', default='')
    args=parser.parse_args()
    kzhgszq(args.code)