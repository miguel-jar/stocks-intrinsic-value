import streamlit as st
import pandas as pd

from calculate_iv import calculate_index_stocks_iv, calculate_b3_all_stocks_iv
from plot_charts import (
    plot_box_plot,
    plot_pe_upside_chat,
    plot_price_iv_chat,
    plot_upside_chat,
    plot_upside_hist,
)

if __name__ == "__main__":
    indexes = ["IBOV", "SMLL", "IDIV"]

    st.set_page_config(page_title="Intrinsic Value Analysis", layout="wide")
    st.title("📈 Graham Intrinsic Value Analysis")  
    tabs = st.tabs(indexes + ["All stocks"])

    data = [calculate_index_stocks_iv(index) for index in indexes]
    data.append(calculate_b3_all_stocks_iv())

    for n in range(len(tabs)):
        valid_stocks, invalid_stocks = data[n]
        tab = tabs[n]

        with tab:
            value = st.slider("Market Cap Filter", min_value=valid_stocks["market_cap"].min(), max_value=valid_stocks["market_cap"].max(), step=1000.0)
            print(value)
            valid_stocks = valid_stocks.query("market_cap >= @value")
            invalid_stocks = pd.concat([invalid_stocks, valid_stocks.query("market_cap < @value")])

            st.subheader("Valid stocks")
            with st.expander("Hide / Show", expanded=True):
                st.dataframe(
                    valid_stocks,
                    column_order=[
                        "company",
                        "ticker",
                        "bvps",
                        "eps",
                        "price",
                        "iv",
                        "p_e",
                        "p_bv",
                        "p_iv",
                        "ms",
                        "upside",
                    ],
                    column_config={
                        "companyname": st.column_config.TextColumn("company"),
                        "iv": st.column_config.NumberColumn("intrinsic value"),
                        "ms": st.column_config.NumberColumn(
                            "margin of security", format="percent"
                        ),
                        "upside": st.column_config.NumberColumn(format="percent"),
                    },
                )

            with st.expander("Show Invalid Stocks (bvps ≤ 0 or eps ≤ 0)"):
                st.dataframe(
                    invalid_stocks,
                    column_config={
                        "companyname": st.column_config.TextColumn("company"),
                    },
                )

            st.plotly_chart(plot_upside_chat(valid_stocks.copy()))
            st.plotly_chart(plot_price_iv_chat(valid_stocks.copy()))
            st.plotly_chart(plot_upside_hist(valid_stocks.copy()))
            st.plotly_chart(plot_pe_upside_chat(valid_stocks.copy()))
            st.plotly_chart(plot_box_plot(valid_stocks.copy()))
