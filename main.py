import pandas as pd
import streamlit as st

from calculate_iv import calculate_b3_all_stocks_iv
from plot_charts import (
    plot_box_plot,
    plot_pe_upside_chat,
    plot_price_iv_chat,
    plot_upside_chat,
    plot_upside_hist,
)
from tools.get_index_current_comp import get_index_current_comp


def generate_tables_n_charts(valid_stocks: pd.DataFrame, invalid_stocks: pd.DataFrame):
    # Tables
    with st.expander("Valid stocks", expanded=True):
        st.dataframe(
            valid_stocks,
            column_order=[
                "company",
                "ticker",
                "market_cap",
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
            column_config={
                "companyname": st.column_config.TextColumn("company"),
            },
        )

    valid_stocks["abs_upside"] = abs(valid_stocks["upside"])

    # Charts
    st.plotly_chart(plot_upside_chat(valid_stocks))
    st.plotly_chart(plot_price_iv_chat(valid_stocks))
    st.plotly_chart(plot_upside_hist(valid_stocks))
    st.plotly_chart(plot_pe_upside_chat(valid_stocks))
    st.plotly_chart(plot_box_plot(valid_stocks))


if __name__ == "__main__":
    all_valid_stocks, invalid_stocks = calculate_b3_all_stocks_iv()

    indexes = ["IBOV", "SMLL", "IDIV"]
    indexes_stocks = [get_index_current_comp(index) for index in indexes]
    indexes_valid_stocks = [
        all_valid_stocks[all_valid_stocks["ticker"].isin(stocks["ticker"])].reset_index(
            drop=True
        )
        for stocks in indexes_stocks
    ]
    indexes_invalid_stocks = [
        invalid_stocks[invalid_stocks["ticker"].isin(stocks["ticker"])].reset_index(
            drop=True
        )
        for stocks in indexes_stocks
    ]

    st.set_page_config(page_title="Intrinsic Value Analysis", layout="wide")
    st.title("📈 Graham Intrinsic Value Analysis")
    tabs = st.tabs(indexes + ["All stocks"])

    # Add Market Cap. fillter for last tab (all stocks)
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

        generate_tables_n_charts(filtered_valid_stocks, filtered_invalid_stocks)

    for n in range(len(indexes)):
        with tabs[n]:
            vld_s, ivld_s = indexes_valid_stocks[n], indexes_invalid_stocks[n]
            generate_tables_n_charts(vld_s, ivld_s)

            # Statistics

            stocks_percentages = indexes_stocks[0][
                indexes_stocks[0]["ticker"].isin(vld_s["ticker"])
            ]["percentage"] / 100

            avg_upside = round(vld_s["upside"].mean(), 2)
            std_upside = round(vld_s["upside"].std(), 2)
            avg_ms = round(vld_s["margin_of_security"].mean(), 2)
            std_ms = round(vld_s["upside"].std(ddof=0), 2)
            ponderated_iv = round(
                (vld_s["intrinsic_value"] * stocks_percentages).sum(),
                2,
            )
            ponderated_price = round(
                (vld_s["price"] * stocks_percentages).sum(),
                2,
            )
            ponderated_p_iv = round(
                (vld_s["p_iv"] * stocks_percentages).sum(),
                2,
            )
            ponderated_p_e = round(
                (vld_s["p_e"] * stocks_percentages).sum(),
                2,
            )

            up_cells = st.columns(4)
            up_cells[0].metric("Avg. upside", value=f"{avg_upside} %", border=True)
            up_cells[1].metric(
                "Avg. margin of security", value=f"{avg_ms} %", border=True
            )
            up_cells[2].metric(
                "Index ponderated intrinsic value (1:1)",
                value=ponderated_iv,
                border=True,
            )
            up_cells[3].metric(
                "Index ponderated p/iv",
                value=ponderated_p_iv,
                border=True,
            )

            down_cells = st.columns(4)
            down_cells[0].metric(
                "Upside std. deviation", value=f"{std_upside} %", border=True
            )
            down_cells[1].metric(
                "Margin of security std. deviation", value=f"{std_ms} %", border=True
            )
            down_cells[2].metric(
                "Index ponderated price(1:1)", value=ponderated_price, border=True
            )
            down_cells[3].metric(
                "Index ponderated p/e",
                value=ponderated_p_e,
                border=True,
            )
