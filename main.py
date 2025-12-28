import pandas as pd
import streamlit as st

from calculate_iv import calculate_b3_all_stocks_iv
from plot_charts import (
    plot_box_plot,
    plot_pe_upside_chat,
    plot_price_iv_chat,
    plot_upside_chat,
    plot_pe_pbv_piv,
    plot_upside_hist,
)
from tools.get_index_current_comp import get_index_current_comp


def generate_tables(valid_stocks: pd.DataFrame, invalid_stocks: pd.DataFrame):
    st.subheader("Tables")

    with st.expander("Valid stocks", expanded=True):
        st.dataframe(
            valid_stocks,
            column_order=[
                "company",
                "ticker",
                "market_cap",
                "percentage",
                "bvps",
                "eps",
                "price",
                "intrinsic_value",
                "p_e",
                "p_bv",
                "p_iv",
                "margin_of_security",
                "upside",
            ],
            column_config={
                "companyname": st.column_config.TextColumn("company"),
                "market_cap": st.column_config.NumberColumn(format="dollar"),
                "margin_of_security": st.column_config.NumberColumn(
                    "margin_of_security [%]"
                ),
                "upside": st.column_config.NumberColumn("upside [%]"),
            },
        )

    with st.expander("Invalid Stocks (bvps ≤ 0 or eps ≤ 0 or price ≤ 0)"):
        st.dataframe(
            invalid_stocks,
            column_order=[
                "company",
                "ticker",
                "market_cap",
                "percentage",
                "bvps",
                "eps",
                "price",
            ],
            column_config={
                "companyname": st.column_config.TextColumn("company"),
                "market_cap": st.column_config.NumberColumn(format="dollar"),
            },
        )

    valid_stocks["abs_upside"] = abs(valid_stocks["upside"])


def generate_charts(valid_stocks: pd.DataFrame):
    st.subheader("Charts")
    st.plotly_chart(plot_upside_chat(valid_stocks))
    st.plotly_chart(plot_price_iv_chat(valid_stocks))
    st.plotly_chart(plot_upside_hist(valid_stocks))
    st.plotly_chart(plot_pe_upside_chat(valid_stocks))
    st.plotly_chart(plot_pe_pbv_piv(valid_stocks))
    st.plotly_chart(plot_box_plot(valid_stocks))


def generate_metrics(valid_stocks: pd.DataFrame):
    st.subheader("Metrics")
    st.markdown(
        "Metrics calculated using just valid stocks. Stock market cap. used as weight for weighted metrics."
    )

    # Weighted by market cap

    w_upside = valid_stocks["upside"] * valid_stocks["market_cap"]
    avg_upside = round(valid_stocks["upside"].mean(), 2)
    std_upside = round(valid_stocks["upside"].std(ddof=0), 2)
    w_avg_upside = round(w_upside.sum() / valid_stocks["market_cap"].sum(), 2)
    # w_std_upside = round((((valid_stocks["upside"] - w_upside.sum()) ** 2)* valid_stocks["percentage"]).sum() ** (1 / 2), 2)
    std_upside_w_avg = round(
        ((valid_stocks["upside"] - w_avg_upside) ** 2).sum() ** (1 / 2), 2
    )

    up_cells = st.columns(4)
    up_cells[0].metric(
        "Avg. upside",
        value=f"{avg_upside} %",
        border=True,
    )
    up_cells[1].metric(
        "Upside std. deviation",
        value=f"{std_upside} %",
        border=True,
    )
    up_cells[2].metric(
        "Weighted avg. upside",
        value=f"{w_avg_upside} %",
        border=True,
    )
    up_cells[3].metric(
        "Upside std. deviation in reference to weighted avg.",
        value=f"{std_upside_w_avg} %",
        border=True,
    )

    w_ms = valid_stocks["margin_of_security"] * valid_stocks["market_cap"]
    avg_ms = round(valid_stocks["margin_of_security"].mean(), 2)
    std_ms = round(valid_stocks["margin_of_security"].std(ddof=0), 2)
    w_avg_ms = round(w_ms.sum() / valid_stocks["market_cap"].sum(), 2)
    # w_std_ms = round((((valid_stocks["margin_of_security"] - w_ms.sum()) ** 2)* valid_stocks["percentage"]).sum() ** (1 / 2), 2)
    std_ms_w_avg = round(
        ((valid_stocks["margin_of_security"] - w_avg_ms) ** 2).sum() ** (1 / 2), 2
    )

    mid_cells = st.columns(4)
    mid_cells[0].metric(
        "Avg. margin of security",
        value=f"{avg_ms} %",
        border=True,
    )
    mid_cells[1].metric(
        "Margin of security std. deviation",
        value=f"{std_ms} %",
        border=True,
    )
    mid_cells[2].metric(
        "Weighted avg. Margin of security",
        value=f"{w_avg_ms} %",
        border=True,
    )
    mid_cells[3].metric(
        "Margin of security std. deviation in reference to weighted avg.",
        value=f"{std_ms_w_avg} %",
        border=True,
    )

    ponderated_iv = round(
        (valid_stocks["intrinsic_value"] * valid_stocks["market_cap"]).sum()
        / valid_stocks["market_cap"].sum(),
        2,
    )
    ponderated_price = round(
        (valid_stocks["price"] * valid_stocks["market_cap"]).sum()
        / valid_stocks["market_cap"].sum(),
        2,
    )
    ponderated_p_iv = round(
        (valid_stocks["p_iv"] * valid_stocks["market_cap"]).sum()
        / valid_stocks["market_cap"].sum(),
        2,
    )
    ponderated_p_e = round(
        (valid_stocks["p_e"] * valid_stocks["market_cap"]).sum()
        / valid_stocks["market_cap"].sum(),
        2,
    )
    ponderated_p_bv = round(
        (valid_stocks["p_bv"] * valid_stocks["market_cap"]).sum()
        / valid_stocks["market_cap"].sum(),
        2,
    )

    down_cell = st.columns(5)
    down_cell[0].metric(
        "Index ponderated intrinsic value (1:1)", value=ponderated_iv, border=True
    )
    down_cell[1].metric(
        "Index ponderated price(1:1)", value=ponderated_price, border=True
    )
    down_cell[2].metric("Index ponderated p/iv", value=ponderated_p_iv, border=True)
    down_cell[3].metric("Index ponderated p/e", value=ponderated_p_e, border=True)
    down_cell[4].metric("Index ponderated p/bv", value=ponderated_p_bv, border=True)


def generate_index_metrics(all_index_stocks: pd.DataFrame):
    st.subheader("Index Metrics")
    st.markdown(
        "Metrics calculated using all index stocks. Percentage in index used as weight for weighted metrics."
    )

    # ponderated_iv = round(
    #     (valid_stocks["intrinsic_value"] * valid_stocks["market_cap"]).sum()
    #     / valid_stocks["market_cap"].sum(),
    #     2,
    # )

    all_index_stocks["percentage"] /= 100
    ponderated_price = round(
        (all_index_stocks["price"] * all_index_stocks["percentage"]).sum(), 2
    )
    # ponderated_p_iv = round(
    #     (all_index_stocks["p_iv"] * all_index_stocks["percentage"]).sum(), 2
    # )
    ponderated_p_e = round(
        (all_index_stocks["p_e"] * all_index_stocks["percentage"]).sum(), 2
    )
    ponderated_p_bv = round(
        (all_index_stocks["p_bv"] * all_index_stocks["percentage"]).sum(), 2
    )

    down_cell = st.columns(4)
    # down_cell[0].metric(
    #     "Index ponderated intrinsic value (1:1)",
    #     value=ponderated_iv,
    #     border=True,
    # )
    down_cell[0].metric(
        "Index ponderated price(1:1)",
        value=ponderated_price,
        border=True,
    )
    # down_cell[1].metric(
    #     "Index ponderated p/iv",
    #     value=ponderated_p_iv,
    #     border=True,
    # )
    down_cell[1].metric(
        "Index ponderated p/e",
        value=ponderated_p_e,
        border=True,
    )
    down_cell[2].metric(
        "Index ponderated p/bv",
        value=ponderated_p_bv,
        border=True,
    )


if __name__ == "__main__":
    all_valid_stocks, invalid_stocks = calculate_b3_all_stocks_iv()

    indexes = ["IBOV", "SMLL", "IDIV"]
    indexes_stocks = [get_index_current_comp(index) for index in indexes]
    indexes_valid_stocks = [
        all_valid_stocks[all_valid_stocks["ticker"].isin(stocks["ticker"])]
        .reset_index(drop=True)
        .assign(percentage=stocks["percentage"])
        for stocks in indexes_stocks
    ]
    indexes_invalid_stocks = [
        invalid_stocks[invalid_stocks["ticker"].isin(stocks["ticker"])]
        .reset_index(drop=True)
        .assign(percentage=stocks["percentage"])
        for stocks in indexes_stocks
    ]

    st.set_page_config(page_title="Intrinsic Value Analysis", layout="wide")
    st.title("📈 Graham Intrinsic Value Analysis")
    tabs = st.tabs(indexes + ["All stocks"])

    # All stocks tab
    with tabs[-1]:
        value = st.number_input(
            "Market Cap.",
            min_value=all_valid_stocks["market_cap"].min(),
            max_value=all_valid_stocks["market_cap"].max(),
            step=10000000.0,
            value=100000000.0,
        )

        filtered_valid_stocks = all_valid_stocks.query(
            "market_cap >= @value"
        ).reset_index(drop=True)
        filtered_invalid_stocks = pd.concat(
            [
                invalid_stocks,
                all_valid_stocks.query("market_cap < @value"),
            ],
            ignore_index=True,
        )

        generate_tables(filtered_valid_stocks, filtered_invalid_stocks)
        generate_charts(filtered_valid_stocks)
        generate_metrics(filtered_valid_stocks)

    # Indexes stocks tabs
    for n in range(len(indexes)):
        with tabs[n]:
            vld_s, ivld_s = indexes_valid_stocks[n], indexes_invalid_stocks[n]
            generate_tables(vld_s, ivld_s)
            generate_charts(vld_s)
            generate_metrics(vld_s)
            generate_index_metrics(pd.concat([vld_s, ivld_s]))
