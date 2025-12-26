import base64
import io
import json
from typing import Literal

import pandas as pd
import requests


def get_index_current_comp(index: Literal["IBOV", "SMLL", "IDIV", "IFIX"]) -> pd.DataFrame:
    _file_saving_path = f"files/{index.lower()}_current_composition.csv"

    payload = {"index": index, "language": "pt-br"}
    encoded_payload = base64.b64encode(json.dumps(payload).encode()).decode()
    url = f"https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetDownloadPortfolioDay/{encoded_payload}"

    cookies = {
        "dtCookie": "v_4_srv_34_sn_88EED4A58FB0D551CAB6CBB6F3E8CE70_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_0_rcs-3Acss_0",
        "cf_clearance": "fb1W204FHidkoxMY_5s8RhiqfnAE9_nt_nH113uXKHE-1766365076-1.2.1.1-npBD5an.yaJzcBWlrDfG2tXrnzM_Knl8u.TPlcbgfnV0TJasom3hS89N_kLtELIXSksldhnJ.BdWD2q2fWE0FK92iCp44CsHuHtwYTExM.oVSBUBA31fbLw3.wd5seGzKKl7tekU8fgvhJW0gpVNRWRJOesqvYdbq7R0v5zVljtblaGP0eWAndRnvPyYZ3YFFgKZjpQu0RaYRE0T2gbeM6dgZGqtDffUu6ZFFLuax.U",
        "F051234a800": "!jv+j08zF+QYepmJnsRGjgvQcm9MkMOv26jCpVx197DCo6zq2LAGzQqRGI/3uOXgxVg2HogEEge2AbgA=",
        "TS0171d45d": "011d592ce1d4477aa4e045f7a340066c54219f61fd7a9cddbd77e03712faf9903617b56ded15bc58ae1bdf04e06a9ffe77264df5d6",
        "TS01871345": "016e3b076f6cc2e735d393440a32af2e805e4457503c24d4615c4d4eb08119d8185bf9eb3ac85682b7f22012cfb4df33b92c6fc147",
        "__cf_bm": "ddnWblR7HC4hF43fQaVulo0BYTf7oW0I94gcH7oq7so-1766366608-1.0.1.1-i_LBB3cwmxmWRZ7A8x0uRyPp3B1cT_6_fDY8d3AXDJoG9nue7ZqKH3R.ntKVUgyPGmt8kmn3pCU7kZ_NJXYnB4wFHw3.d1qpq9sn_0Bj5iw",
        "TS01f22489": "011d592ce1c0d3d815d633a247b2595ccb8bfafa25054e540b7922a1605843426e7af3e7c98ed5cd5fb794f710c8aacb5252564658",
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "pt-BR,pt;q=0.7",
        "priority": "u=1, i",
        "referer": "https://sistemaswebb3-listados.b3.com.br/",
        "sec-ch-ua": '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    }

    # Always tries to get data from web to guaranty fresh data
    # Otherwise, uses saved data

    try:
        response = requests.get(url, cookies=cookies, headers=headers, timeout=15)
        response.raise_for_status()

        data = base64.b64decode(response.content)
        df = pd.read_csv(
            io.BytesIO(data),
            sep=";",
            encoding="latin-1",
            decimal=",",
            thousands=".",
            skipfooter=2,
            skiprows=2,
            header=None,
            names=["ticker", "company", "stock_type", "qty", "percentage"],
            index_col=False,
            engine="python",
        )
        df["stock_type"] = df["stock_type"].str.replace(" ", "")
        df.to_csv(_file_saving_path, index=False)
        print(f"\nFile saved in {_file_saving_path}")

    except Exception as e:
        print(e)
        print("\nCouldn't get data from web. Checking for stored files ...\n")

        try:
            df = pd.read_csv(_file_saving_path)
        except FileNotFoundError:
            print("No stored file found. Exiting program ....")
            exit(1)

    return df


if __name__ == "__main__":
    index = "IFIX"
    df = get_index_current_comp(index)
