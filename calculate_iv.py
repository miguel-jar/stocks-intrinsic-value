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
    valid_stocks = df.query(mask).reset_index(drop=True)
    invalid_stocks = df.query(f"not {mask}").copy().reset_index(drop=True)
    # Copy in invalid_stocks to avoid new columns

    valid_stocks = valid_stocks.assign(
        intrinsic_value=lambda x: ((x["bvps"] * x["eps"] * 22.5) ** (1 / 2)).round(2),
        p_iv=lambda x: (x["price"] / x["intrinsic_value"]).round(2),
        margin_of_security=lambda x: (1 - x["p_iv"]) * 100,
        upside=lambda x: ((1 / x["p_iv"] - 1)* 100).round(2),
    )

    return [valid_stocks, invalid_stocks]


def calculate_index_stocks_iv(
    indexes: Literal["IBOV", "SMLL", "IDIV"] | list[Literal["IBOV", "SMLL", "IDIV"]],
) -> dict[str, list[pd.DataFrame]]:
    if isinstance(indexes, str):
        indexes = [indexes]

    stocks_stats = get_b3_stocks_stats()

    indexes_stocks = [get_index_current_comp(index) for index in indexes]
    indexes_stocks_stats = [
        stocks_stats[stocks_stats["ticker"].isin(index_stocks["ticker"])]
        for index_stocks in indexes_stocks
    ]

    return {
        index: _calculate_iv(stocks)
        for index, stocks in zip(indexes, indexes_stocks_stats)
    }


def calculate_b3_all_stocks_iv() -> list[pd.DataFrame]:
    return _calculate_iv(get_b3_stocks_stats())


if __name__ == "__main__":
    results = calculate_index_stocks_iv(["IBOV", "IDIV"])
    for index, data in results.items():
        print("\n" + index + "\n")
        print(data[0])
        print(data[1])
