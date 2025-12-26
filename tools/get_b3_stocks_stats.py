import pandas as pd
import requests


def get_b3_stocks_stats(save_csv: bool = False) -> pd.DataFrame:
    _file_saving_path = "files/statistics_all_stocks_b3.csv"

    cookies = {
        "_adasys": "c043ca00-07e9-4df6-bbd2-03db2d984220",
        "suno_checkout_userid": "11ce0881-7f9e-478b-bfb2-728dca75c647",
        "wisepops": "%7B%22popups%22%3A%7B%7D%2C%22sub%22%3A0%2C%22ucrn%22%3A69%2C%22cid%22%3A%2252100%22%2C%22v%22%3A5%7D",
        "wisepops_visitor": "%7B%22TfwCNQSfMg%22%3A%22664b4d83-14d0-4ed9-a258-077b8a7e0ec4%22%7D",
        ".StatusAdThin": "1",
        "wisepops_visits": "%5B%222025-12-21T19%3A26%3A34.372Z%22%2C%222025-11-09T13%3A13%3A38.099Z%22%5D",
        "cf_clearance": "t8xXQgFIKYlBSSNccuUeCaivQemmeBGZxxNHZ9lqNaQ-1766349001-1.2.1.1-OgbeoS6T6JxCY0KFQjPPNmkt_gOTcHPfrIYtB_ms4h2_Dlv5z1qMcc0Mc8KfU82R9FJUTHdFlOERknttkvrBsTwYNH8HPxpKv6i8Wp.3NMYOCsSL7ji1cL9KLQWXwP4aDdSNCd_gPMN8zWndjD1rQBst0S0tpvNfr53dN_FV2HpDRgOkgaFWvCX9Fjrcq9Kt.G7gG9JyAt0jlRbCx6pdN5cTGHYBlvKVxeMMCQ6GRqI",
        "wisepops_session": "%7B%22mtime%22%3A1766349097301%2C%22pageviews%22%3A6%2C%22popups%22%3A%7B%7D%2C%22bars%22%3A%7B%7D%2C%22embeds%22%3A%7B%7D%2C%22sticky%22%3A%7B%7D%2C%22countdowns%22%3A%7B%7D%2C%22src%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22utm%22%3A%7B%7D%2C%22testIp%22%3Anull%2C%22debugToken%22%3Anull%2C%22closed%22%3A%5B%5D%7D",
        "g_state": '{"i_l":0,"i_ll":1766349097307,"i_b":"Qt0MKTPPVCDq/x0T5cinD7LK8wbS3y4IX7/3MccjOJo","i_e":{"enable_itp_optimization":0}}',
    }

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "pt-BR,pt;q=0.8",
        "priority": "u=1, i",
        "referer": "https://statusinvest.com.br/acoes/busca-avancada",
        "sec-ch-ua": '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    params = {
        "search": '{"Sector":"","SubSector":"","Segment":"","my_range":"-20;100","forecast":{"upsidedownside":{"Item1":null,"Item2":null},"estimatesnumber":{"Item1":null,"Item2":null},"revisedup":true,"reviseddown":true,"consensus":[]},"dy":{"Item1":null,"Item2":null},"p_l":{"Item1":null,"Item2":null},"peg_ratio":{"Item1":null,"Item2":null},"p_vp":{"Item1":null,"Item2":null},"p_ativo":{"Item1":null,"Item2":null},"margembruta":{"Item1":null,"Item2":null},"margemebit":{"Item1":null,"Item2":null},"margemliquida":{"Item1":null,"Item2":null},"p_ebit":{"Item1":null,"Item2":null},"ev_ebit":{"Item1":null,"Item2":null},"dividaliquidaebit":{"Item1":null,"Item2":null},"dividaliquidapatrimonioliquido":{"Item1":null,"Item2":null},"p_sr":{"Item1":null,"Item2":null},"p_capitalgiro":{"Item1":null,"Item2":null},"p_ativocirculante":{"Item1":null,"Item2":null},"roe":{"Item1":null,"Item2":null},"roic":{"Item1":null,"Item2":null},"roa":{"Item1":null,"Item2":null},"liquidezcorrente":{"Item1":null,"Item2":null},"pl_ativo":{"Item1":null,"Item2":null},"passivo_ativo":{"Item1":null,"Item2":null},"giroativos":{"Item1":null,"Item2":null},"receitas_cagr5":{"Item1":null,"Item2":null},"lucros_cagr5":{"Item1":null,"Item2":null},"liquidezmediadiaria":{"Item1":null,"Item2":null},"vpa":{"Item1":null,"Item2":null},"lpa":{"Item1":null,"Item2":null},"valormercado":{"Item1":null,"Item2":null}}',
        "orderColumn": "",
        "isAsc": "",
        "page": "0",
        "take": "1500",
        "CategoryType": "1",
    }

    # Always tries to get data from web to guaranty fresh data
    # Otherwise, uses saved data

    try:
        response = requests.get(
            "https://statusinvest.com.br/category/advancedsearchresultpaginated",
            params=params,
            cookies=cookies,
            headers=headers,
        )
        response.raise_for_status()

        df = pd.DataFrame(response.json()["list"])
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
    try:
        df = get_b3_stocks_stats(True)
    except Exception as e:
        print("\n" + str(e) + "\n")
