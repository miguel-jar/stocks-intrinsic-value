from typing import Literal
import pandas as pd

from tools.get_b3_stocks_stats import get_b3_stocks_stats
from tools.get_index_current_comp import get_index_current_comp


def _calculate_iv(stocks_stats: pd.DataFrame) -> list[pd.DataFrame]:
    df = stocks_stats[
        ["companyname", "ticker", "price", "p_l", "p_vp", "vpa", "lpa", "valormercado"]
    ]
    df.columns = [
        "company",
        "ticker",
        "price",
        "p_e",
        "p_bv",
        "bvps",
        "eps",
        "market_cap",
    ]

    mask = "(bvps > 0 & eps > 0 & price > 0)"
    invalid_stocks = df.query(f"not {mask}").reset_index(drop=True)
    valid_stocks = df.query(mask).reset_index(drop=True)

    valid_stocks = valid_stocks.assign(
        iv=lambda x: ((x["bvps"] * x["eps"] * 22.5) ** (1 / 2)).round(2),
        p_iv=lambda x: (x["price"] / x["iv"]).round(2),
        ms=lambda x: (1 - x["p_iv"]).round(2),
        upside=lambda x: (1 / x["p_iv"] - 1).round(2),
    )
    
    return [valid_stocks, invalid_stocks]


def calculate_index_stocks_iv(
    index: Literal["IBOV", "SMLL", "IDIV"],
) -> list[pd.DataFrame]:
    index_stocks = get_index_current_comp(index)
    stocks_stats = get_b3_stocks_stats()
    index_stocks_stats = stocks_stats[
        stocks_stats["ticker"].isin(index_stocks["ticker"])
    ]

    return _calculate_iv(index_stocks_stats)


def calculate_b3_all_stocks_iv() -> list[pd.DataFrame]:
    return _calculate_iv(get_b3_stocks_stats())


if __name__ == "__main__":
    df1, df2 = calculate_index_stocks_iv("IBOV")
    print(df1)
    print(df2)
