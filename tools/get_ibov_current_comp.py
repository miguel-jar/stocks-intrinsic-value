import requests
import pandas as pd
import io
import base64

_saving_path = 'files/ibov_current_composition.csv'

cookies = {
    'dtCookie': 'v_4_srv_27_sn_C7A6714027B3DC0EB295C4704ADA9C59_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0',
    'rxVisitor': '17663409603805M80E5OO0DMS5ATCRDCHUA8KJP9KGSUU',
    'TS0171d45d': '011d592ce109d858cd64412235c0e12ffaa2b0bb1a71b013b325fc0d4cc78d1b75ee6a69aacfa57022c68357b3c6a282ce517d25d5',
    '__cf_bm': 'pS70rb2833IbLSiEs9R3b2j1Bx0ThhaMN5Mbev1YvlI-1766345470-1.0.1.1-wYjYqnBn4KpsW9e_steQkZjOZgyWYr9pk94xkjg5cZDvxoL8xGinb39zRh8zn7G_1dy_vdVRKr2i5Qnd64ia6nZjRH.UZQOWeGCQvMhCTPM',
    'TS01f22489': '011d592ce119f72eb456be5bfeaf0fce79e05c7ddd62512257b8ddf91bf1c606318e79e9a16c31c17e89e2424657f215340cab7f5f',
    'cf_clearance': 'Boz0IzVXB6fvoTnUxO8XzJppPBCJRdHoGyduX6cnq9Y-1766345582-1.2.1.1-FDz7oHlkNV.qXQf18Ghx5RZb4YjxqB.W27GFyQaz1yz1nPk.xSHjvrAKE4gGhDb00Drna49xhHnwiLBOO39Aoc0ny5BTGsSnUBMqsm0pUPC58Pk17KVQf9tkU.WFO7khEQbyYnvili7PKKK_NThNp21Izot2G_u7ReUfnhHWsRNO5cdEjHcU6S3NjIB.uio_YrOhhSKhrnTF_PIgNLmMDqDIiezlq8jQdZAV6f2QX1A',
    'dtSa': '-',
    'TS01871345': '016e3b076f683bfecfbfe3aeb58963e3e58b4586e72ff763ccde139e930c8f0ba4249deb41001c8fb941e009550475679b74ba3fef',
    'rxvt': '1766347385821|1766344579169',
    'dtPC': '27$545584529_5h-vHDFCUFURROVQFOJNQRPTMPTCCFVKLREA-0e0',
    'F051234a800': '!hIplbDSQ0BSBS8RnsRGjgvQcm9MkMG3U8laO2AKc8Z9Sp/iKcrxo8TCQ5+T+tY1MtgJCu1KISrLiaXc=',
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
    # 'cookie': 'dtCookie=v_4_srv_27_sn_C7A6714027B3DC0EB295C4704ADA9C59_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0; rxVisitor=17663409603805M80E5OO0DMS5ATCRDCHUA8KJP9KGSUU; TS0171d45d=011d592ce109d858cd64412235c0e12ffaa2b0bb1a71b013b325fc0d4cc78d1b75ee6a69aacfa57022c68357b3c6a282ce517d25d5; __cf_bm=pS70rb2833IbLSiEs9R3b2j1Bx0ThhaMN5Mbev1YvlI-1766345470-1.0.1.1-wYjYqnBn4KpsW9e_steQkZjOZgyWYr9pk94xkjg5cZDvxoL8xGinb39zRh8zn7G_1dy_vdVRKr2i5Qnd64ia6nZjRH.UZQOWeGCQvMhCTPM; TS01f22489=011d592ce119f72eb456be5bfeaf0fce79e05c7ddd62512257b8ddf91bf1c606318e79e9a16c31c17e89e2424657f215340cab7f5f; cf_clearance=Boz0IzVXB6fvoTnUxO8XzJppPBCJRdHoGyduX6cnq9Y-1766345582-1.2.1.1-FDz7oHlkNV.qXQf18Ghx5RZb4YjxqB.W27GFyQaz1yz1nPk.xSHjvrAKE4gGhDb00Drna49xhHnwiLBOO39Aoc0ny5BTGsSnUBMqsm0pUPC58Pk17KVQf9tkU.WFO7khEQbyYnvili7PKKK_NThNp21Izot2G_u7ReUfnhHWsRNO5cdEjHcU6S3NjIB.uio_YrOhhSKhrnTF_PIgNLmMDqDIiezlq8jQdZAV6f2QX1A; dtSa=-; TS01871345=016e3b076f683bfecfbfe3aeb58963e3e58b4586e72ff763ccde139e930c8f0ba4249deb41001c8fb941e009550475679b74ba3fef; rxvt=1766347385821|1766344579169; dtPC=27$545584529_5h-vHDFCUFURROVQFOJNQRPTMPTCCFVKLREA-0e0; F051234a800=!hIplbDSQ0BSBS8RnsRGjgvQcm9MkMG3U8laO2AKc8Z9Sp/iKcrxo8TCQ5+T+tY1MtgJCu1KISrLiaXc=',
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