import pandas as pd
import requests
import time
import math
import random
import io
import json
import re

headers = {'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/56.0.2924.87 Safari/537.36',
           'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
           }

STOCK_TYPES = {
    1: '主板A股',
    2: '主板B股',
    8: '科创板'
}

DIVIDEND_FIELDS = {
    'SECURITY_CODE_A': 'A股股票代码',
    'RECORD_DATE_A': 'A股股权登记日',
    'EX_DIVIDEND_DATE_A': '除息日',
    'DIVIDEND_PER_SHARE1_A': '税后每股红利',
    'DIVIDEND_PER_SHARE2_A': '税前每股红利',
    'EXCHANGE_RATE': '-',
    'COMPANY_CODE': '公司代码',
    'FULL_NAME': '公司名称',
    'DIVIDEND_DATE': '股息日',
    'SECURITY_ABBR_A': '股票简称'
}

BONU_FIELDS = {
    'ANNOUNCE_DATE': '公告刊登日',
    'ANNOUNCE_DESTINATION': '公告宣布地',
    'BONUS_RATE': '送股比例',
    'CHANGE_RATE': '变动比例',
    'COMPANY_CODE': '股票代码',
    'COMPANY_NAME': '公司名称',
    'EX_RIGHT_DATE_A': '除权基准日',
    'EX_RIGHT_DATE_B': '除权基准日B',
    'LAST_TRADE_DATE_B': '最后交易日B',
    'RECORD_DATE_A': 'A股股权登记日',
    'RECORD_DATE_B': 'B股股权登记日',
    'SECURITY_CODE_A': 'A股证券代码',
    'SECURITY_CODE_B': 'B股证券代码',
    'SECURITY_NAME_A': 'A股证券名称',
    'SECURITY_NAME_B': 'B股证券名称',
    'TRADE_DATE_A': '红股上市日',
    'TRADE_DATE_B': 'B股红股上市日',
}

ALLOTMENTS_FIELDS = {
    'COMPANY_CODE': '公司代码',
    'END_DATE_OF_REMITTANCE_A': '配股缴款截止日',
    'EX_RIGHTS_DATE_A': 'A股除权交易日',
    'LISTING_DATE_A': '配股上市日',
    'PRICE_OF_RIGHTS_ISSUE_A': 'A股配股价格',
    'RATIO_OF_RIGHTS_ISSUE_A': '配股比例(10：?)',
    'RECORD_DATE_A': 'A股股权登记日',
    'SECURITY_CODE_A': 'A股证券代码',
    'SECURITY_NAME_A': '证券名称',
    'START_DATE_OF_REMITTANCE_A': '配股缴款起始日',
    'TRUE_COLUME_A': '实际配股量(万股)',
}


def __regular_stocks(df):
    del(df['Unnamed: 5'])
    del(df['公司代码 '])
    del(df['公司简称 '])
    df['交易所'] = 0
    df['所属行业'] = ''
    df['代码'] = df['代码'].astype(str)
    return df


def call_download_stock_list_file(stock_type):
    headers = {'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/56.0.2924.87 Safari/537.36',
               'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
               }
    url = 'http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName='
    data = {
        'stockType': stock_type
    }
    r = requests.post(url, data=data, headers=headers)
    print(r.text)
    df = pd.read_table(io.StringIO(r.text))
    return pd.read_table(io.StringIO(r.text))

def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')

def common_query(**data):
    url='http://query.sse.com.cn/commonQuery.do'
    data['jsonCallBack'] = 'jsonpCallback' + \
        str(math.floor(1e5 * random.random()))
    data['_'] = str(int(round(time.time() * 1000)))
    r=requests.get(url, params=data, headers=headers)
    return loads_jsonp(r.text)

def security_list(**data):
    """返回证券列表

    Args:
        stockType (Any):  1: '主板A股', 2: '主板B股', 8: '科创板'

    >>> security_list(stockType=1)
    601949    中国出版        601949          中国出版        2017-08-21
    601952    苏垦农发        601952          苏垦农发        2017-05-15
    601956    东贝集团        601956          东贝集团        2020-12-25
    601958    金钼股份        601958          金钼股份        2008-04-17
    601963    重庆银行        601963          重庆银行        2021-02-05
    601965    中国汽研        601965          中国汽研        2012-06-11
    }
      
    """
    url='http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName='
    r=requests.get(url,params=data,headers=headers)
    return r.text

# 得到分红
def get_dividends(year):
    data = {
        'isPagination': 'false',
        'sqlId': 'COMMON_SSE_GP_SJTJ_FHSG_AGFH_L_NEW',
        'record_date_a': year,
        'security_code_a': '',
    }
    result = call_common_query(data)
    return result['result']
    # return pd.DataFrame(result['result'])

# 得到送股
def get_bonus(year):
    data = {
        'isPagination': 'false',
        'sqlId': '',
        'year1': year,
        'year2': year,
    }
    result = call_common_query(data)
    return pd.DataFrame(result['result'])

# 得到配股
def get_allotments(year):
    data = {
        'isPagination': 'false',
        'sqlId': 'COMMON_SSE_GP_SJTJ_MJZJ_PG_AGPG_L',
        'searchyear': year,
    }
    result = call_common_query(data)
    return pd.DataFrame(result['result'])

def overview(SEARCH_DATE='', PRODUCT_CODE='01,02,03,11,17'):
    r"""返回沪市成交概况

    >>> overview('20220323')
    '01 20220323 1663 420949.77 379170.91 3687.92 341.21 15.06 0.8761 0.9726
02 20220323 46 791.31 668.08 0.98 0.23 13.07 0.1235 0.1463
03 20220323 402 49116.16 19574.31 377.0 9.03 59.27 0.7676 1.926
11 20220323 0 0.0 0.0 2.49 0.24 - 0.0 0.0
17 20220323 2111 470857.23 399413.3 4065.9 350.47 16.23 0.8635 1.018'
    """
    r=common_query(
        sqlId='COMMON_SSE_SJ_GPSJ_CJGK_MRGK_C',
        isPagination='false',
        PRODUCT_CODE=PRODUCT_CODE,
        type='inParams',
        SEARCH_DATE=SEARCH_DATE
        )
    for i in r['result']:
        print(i['PRODUCT_CODE'], i['TRADE_DATE'], i['LIST_NUM'], i['TOTAL_VALUE'], \
            i['NEGO_VALUE'], i['TRADE_AMT'], i['TRADE_VOL'], i['AVG_PE_RATE'], \
                i['TOTAL_TO_RATE'], i['NEGO_TO_RATE'])

def profile(code):
    """返回股票基础资料

    >>> profile('605500')
    {'STATE_CODE_B_DESC': '-', 'COMPANY_ABBR': '森林包装', 'SCU_TYPE': '-', 'AREA_NAME_DESC': '浙江', 'OPERATION_SEQ': 'bc5b6660ff5cb1322604304888bcbcff', 'COMPANY_ADDRESS': '浙江省温岭市大溪镇大洋城工业区', 'LEGAL_REPRESENTATIVE': '林启军                        ', 'ISHLT': '-', 'SECURITY_CODE_A_SZ': '-', 'SECURITY_CODE_A': '605500', 'ENGLISH_ABBR': 'Forest', 'SECURITY_CODE_B': '-', 'IF_VOTE_DIFFERENCE': '-', 'STATE_CODE_A_DESC': '上市', 'SMALL_CLASS_NAME': '-', 'STATUS': 'D  F  N', 'IF_PROFIT': '-', 'OTHER_CODE': '-', 'SSE_CODE_DESC': '工业', 'COMPANY_CODE': '605500', 'OFFICE_ZIP': '317525', 'QIANYI_DATE': '2021-01-05 17:48:00', 'SECURITY_30_DESC': '-', 'FULLNAME': '森林包装集团股份有限公司', 'E_MAIL_ADDRESS': 'forestpackaging@126.com', 'TYPE': '0', 'CSRC_GREAT_CODE_DESC': '造纸和纸制品业', 'FOREIGN_LISTING_ADDRESS': '-', 'FOREIGN_LISTING_DESC': '-', 'CHANGEABLE_BOND_CODE': '-', 'OTHER_ABBR': '-', 'FULL_NAME_IN_ENGLISH': 'Forest Packaging Group Co., Ltd.', 'CSRC_MIDDLE_CODE_DESC': '-', 'SEC_NAME_FULL': '森林包装', 'WWW_ADDRESS': 'www.forestpacking.com ', 'SECURITY_ABBR_A': '森林包装', 'CSRC_CODE_DESC': '制造业', 'CHANGEABLE_BOND_ABBR': '-', 'OFFICE_ADDRESS': '浙江省温岭市大溪镇大洋城工业区', 'REPR_PHONE': '-'}
    """
    r=common_query(
        sqlId='COMMON_SSE_ZQPZ_GP_GPLB_C',
        isPagination='false',
        productid=str(code)
    )
    for i,k in r['result'][0].items():
        print(i, k)

    # 得到分红
    # print(common_query(sqlId='COMMON_SSE_GP_SJTJ_FHSG_AGFH_L_NEW', record_date_a=2021, security_code_a='', isPagination='false'))
    # 得到送股
    # print(common_query(sqlId='COMMON_SSE_GP_SJTJ_FHSG_SG_L_NEW', isPagination='false', year1=2021, year2=2021))
    # overview(sys.argv[1], sys.argv[2])
    # call_download_stock_list_file(1)
    # print(security_list(stockType=1))
    # profile('605500')