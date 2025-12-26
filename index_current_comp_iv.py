from typing import Literal
import pandas as pd

from tools.get_b3_stocks_stats import get_b3_stocks_stats
from tools.get_index_current_comp import get_index_current_comp


def index_current_comp_iv(index: Literal["IBOV", "SMLL", "IDIV"]) -> list[pd.DataFrame]:
    index_stocks = get_index_current_comp(index)
    stocks_stats = get_b3_stocks_stats()
    index_stocks_stats = stocks_stats[
        stocks_stats["ticker"].isin(index_stocks["ticker"])
    ]

    df = index_stocks_stats[
        ["companyname", "ticker", "price", "p_l", "p_vp", "vpa", "lpa"]
    ].copy()
    df.columns = ["company", "ticker", "price", "p_e", "p_bv", "bvps", "eps"]

    valid_stocks = df.query("bvps > 0 & eps > 0").reset_index(drop=True)
    final_df = valid_stocks.assign(
        iv=lambda x: ((x["bvps"] * x["eps"] * 22.5) ** (1 / 2)).round(2),
        p_iv=lambda x: (x["price"] / x["iv"]).round(2),
        ms=lambda x: (1 - x["p_iv"]).round(2),
        upside=lambda x: (1 / x["p_iv"] - 1).round(2),
    )

    invalid_stocks = df.query("bvps <= 0 or eps <= 0").reset_index(drop=True)

    return [final_df, invalid_stocks]


if __name__ == "__main__":
    dfs = index_current_comp_iv("IBOV")
    print(dfs)
