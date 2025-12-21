import requests
import pandas as pd
import io
import base64

_saving_path = 'files/ibov_theoretical_composition.csv'

cookies = {
    'dtCookie': 'v_4_srv_27_sn_C7A6714027B3DC0EB295C4704ADA9C59_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0',
    'TS0171d45d': '011d592ce1549657fbc668b995b79413481f0c004bc5df32a64e19c12318fcd3f6c298bc8c4864ade9e838e5475e46f44727d8c2e5',
    '__cf_bm': 'fj.5Dhus9CpZp1OXqwv7n4gbrFaUGnRuiff2BCgUzeU-1766340959-1.0.1.1-bi8agLoYGXj.rZYjxnAJNs1Hyo2U3ylZbLzFERKPVVDAnJXHqh5StENXS6Tuf7aKw9eYmD7ysdx1BsvZBNi.yDqh3RmdBdHSrmgANaZwLl8',
    'rxVisitor': '17663409603805M80E5OO0DMS5ATCRDCHUA8KJP9KGSUU',
    'cf_clearance': 'PNNIhkewU7XWverUICMITvKXAsrh0b5PVFnJH02L8HE-1766340961-1.2.1.1-U8lWndK0DPK8EPbR3cHQPYKBj0C5AzhoenSICBBDrzmBxUbRUrvHeLwrq3qz5cOJNm72qetXw5nDwRZzbGaEMmYgo51iZ1r285Q1BdWS5v.KAfBZLCL4rAwhpSJezew3By7SHAJIq27C3WJeWYN23I_iBXENrswdA6BR4goKyil9poO3Jpr8V_VyQ8340fI2XERU_2_BkfSPyqw5gY4PDDWHjSsUMNppMnzWuNHxAYA',
    'dtSa': '-',
    'TS01f22489': '011d592ce1ce86d59bbd853f7a1857b88e2a89d8491d6f604fe540a2662b10740a28d96c477157c595305d6138845a449afb252d0c',
    'F051234a800': '!yfxXwHU3X0LACDObbgr6cBDzNKWo7rPJ1INkQZc6CVEpBHeNuLBSMQDg7cpdOsIX1KpOxW/7JRZ9z6Q=',
    'rxvt': '1766342777868|1766340960382',
    'dtPC': '27$540976035_168h-vUFUUGWWHKJMFJPQCACNKRNKNCKSKFMMJ-0e0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'pt-BR,pt;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://sistemaswebb3-listados.b3.com.br/',
    'sec-ch-ua': '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    # 'cookie': 'dtCookie=v_4_srv_27_sn_C7A6714027B3DC0EB295C4704ADA9C59_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0; TS0171d45d=011d592ce1549657fbc668b995b79413481f0c004bc5df32a64e19c12318fcd3f6c298bc8c4864ade9e838e5475e46f44727d8c2e5; __cf_bm=fj.5Dhus9CpZp1OXqwv7n4gbrFaUGnRuiff2BCgUzeU-1766340959-1.0.1.1-bi8agLoYGXj.rZYjxnAJNs1Hyo2U3ylZbLzFERKPVVDAnJXHqh5StENXS6Tuf7aKw9eYmD7ysdx1BsvZBNi.yDqh3RmdBdHSrmgANaZwLl8; rxVisitor=17663409603805M80E5OO0DMS5ATCRDCHUA8KJP9KGSUU; cf_clearance=PNNIhkewU7XWverUICMITvKXAsrh0b5PVFnJH02L8HE-1766340961-1.2.1.1-U8lWndK0DPK8EPbR3cHQPYKBj0C5AzhoenSICBBDrzmBxUbRUrvHeLwrq3qz5cOJNm72qetXw5nDwRZzbGaEMmYgo51iZ1r285Q1BdWS5v.KAfBZLCL4rAwhpSJezew3By7SHAJIq27C3WJeWYN23I_iBXENrswdA6BR4goKyil9poO3Jpr8V_VyQ8340fI2XERU_2_BkfSPyqw5gY4PDDWHjSsUMNppMnzWuNHxAYA; dtSa=-; TS01f22489=011d592ce1ce86d59bbd853f7a1857b88e2a89d8491d6f604fe540a2662b10740a28d96c477157c595305d6138845a449afb252d0c; F051234a800=!yfxXwHU3X0LACDObbgr6cBDzNKWo7rPJ1INkQZc6CVEpBHeNuLBSMQDg7cpdOsIX1KpOxW/7JRZ9z6Q=; rxvt=1766342777868|1766340960382; dtPC=27$540976035_168h-vUFUUGWWHKJMFJPQCACNKRNKNCKSKFMMJ-0e0',
}

response = requests.get(
    'https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetDownloadPortfolioDay/eyJpbmRleCI6IklCT1YiLCJsYW5ndWFnZSI6InB0LWJyIn0=',
    cookies=cookies,
    headers=headers,
)

if response.status_code == 200:
    data = base64.b64decode(response.content)
    df = pd.read_csv(io.BytesIO(data), sep=';', encoding='latin-1', skiprows=2, 
                     header=None, names=['ticker', 'company', 'stock_type', 'qty', 'percentage'], index_col=False)
    df.dropna(axis='index', how='any', inplace=True, ignore_index=False)  # Remove all rows that have Na or NaN values
    df['stock_type'] = df['stock_type'].str.replace(' ', '')
    df['percentage'] = df['percentage'].str.replace(',', '.').astype(float)  
    df.to_csv(_saving_path, index=False)
    
    print(f'\nFile saved in {_saving_path}\n')

else:
    # print(response.status_code)
    response.raise_for_status()