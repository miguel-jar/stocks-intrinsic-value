import streamlit as st
import plotly.express as ex

from index_current_comp_iv import index_current_comp_iv
from plot_charts import (
    plot_upside_chat,
    plot_price_iv_chat,
    plot_upside_hist,
    plot_pe_upside_chat,
    plot_box_plot,
)


if __name__ == "__main__":
    indexes = ["IBOV", "SMLL", "IDIV"]

    st.set_page_config(page_title="Intrinsic Value Analysis", layout="wide")
    st.title("📈 Graham Intrinsic Value Analysis")
    tabs = st.tabs(indexes)

    for tab, index in zip(tabs, indexes):
        valid_stocks, invalid_stocks = index_current_comp_iv(index)

        with tab:
            st.subheader(f"Valid stocks - {index}")
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

            st.plotly_chart(plot_upside_chat(valid_stocks.copy(), index))
            st.plotly_chart(plot_price_iv_chat(valid_stocks.copy(), index))
            st.plotly_chart(plot_upside_hist(valid_stocks.copy(), index))
            st.plotly_chart(plot_pe_upside_chat(valid_stocks.copy(), index))
            st.plotly_chart(plot_box_plot(valid_stocks.copy(), index))
