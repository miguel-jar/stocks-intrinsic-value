import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots


def plot_upside_chat(valid_stocks: pd.DataFrame):
    fig = px.scatter(
        valid_stocks,
        x="ticker",
        y="upside",
        color="upside",
        size="market_cap",
        hover_name="ticker",
        hover_data={
            "upside": True,
            "ticker": False,
            "price": True,
            "intrinsic_value": True,
            "market_cap": False,
        },
        title="Upside [%]",
        subtitle="Stocks upside comparring intrinsic value and current price. Bubble size represented by stock market cap.\n upside = ((intrinsic_value / price - 1) * 100) [%]",
    )
    fig.update_layout(title={"font": {"weight": 1000}})

    return fig


def plot_price_iv_chat(valid_stocks: pd.DataFrame):
    fig = px.scatter(
        valid_stocks,
        x="price",
        y="intrinsic_value",
        color="upside",
        size="abs_upside",
        hover_name="ticker",
        hover_data={
            "upside": True,
            "abs_upside": False,
            "ticker": False,
            "price": True,
            "intrinsic_value": True,
            "p_iv": True,
        },
        labels={"intrinsic_value": "intrinsic value"},
        title="Price vs. Intrinsic Value",
        subtitle="Relation between stocks current price and intrinsic value. Bubble size represented by upside.",
    )

    fig.add_scatter(
        x=[0, valid_stocks["price"].max()],
        y=[0, valid_stocks["price"].max()],
        mode="lines",
        name="price = intrinsic value",
    )

    fig.update_layout(title={"font": {"weight": 1000}}, legend_orientation="h")

    return fig


def plot_upside_hist(valid_stocks: pd.DataFrame):
    hist, bin_edges = np.histogram(
        valid_stocks.query("upside < 100000")["upside"], bins=20, density=False
    )
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    intervals = [
        f"{bin_edges[i]:.1f}% to {bin_edges[i + 1]:.1f}%"
        for i in range(len(bin_edges) - 1)
    ]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_bar(
        x=bin_centers,
        y=hist,
        secondary_y=False,
        name="distribution",
        customdata=intervals,  # Pass our interval strings here
        hovertemplate="<b>Interval:</b> %{customdata}<br><b>Count:</b> %{y}<extra></extra>",
    )
    fig.add_scatter(
        x=bin_centers,
        y=hist.cumsum(),
        mode="lines+markers",
        name="Cumulative Sum",
        customdata=(hist.cumsum() / valid_stocks["upside"].size).round(
            2
        ),  # Pass our interval strings here
        hovertemplate="<b>Count:</b> %{y}<br><b>Norm. count:</b> %{customdata}<extra></extra>",
        secondary_y=True,
    )
    fig.update_layout(title={"font": {"weight": 1000}}, legend_orientation="h")

    fig.update_layout(
        title=dict(text="Upside distribution"),
        xaxis=dict(title=dict(text="upside")),
        yaxis=dict(title=dict(text="count")),
    )

    fig.update_yaxes(title_text="Cumulative count", secondary_y=True, showgrid=False)

    return fig


def plot_pe_upside_chat(valid_stocks: pd.DataFrame):
    fig = px.scatter(
        valid_stocks,
        x="p_e",
        y="upside",
        color="upside",
        size="abs_upside",
        hover_name="ticker",
        hover_data={
            "upside": True,
            "p_e": True,
            "abs_upside": False,
            "p_iv": True,
        },
        labels={"p_e": "price / earnings"},
        title="Price / Earnigns vs. Upside [%]",
        subtitle="Relation between stocks current p/e and upside (based on estimated intrinsic value and current price). Bubble size represented by upside.",
    )

    fig.update_layout(title={"font": {"weight": 1000}}, legend_orientation="h")

    return fig


def plot_pe_pbv_piv(valid_stocks: pd.DataFrame):
    fig = px.scatter(
        valid_stocks,
        x="p_e",
        y="p_bv",
        color="upside",
        size="p_iv",
        hover_name="ticker",
        # hover_data={
        #     "upside": True,
        #     "p_e": True,
        #     "abs_upside": False,
        #     "p_iv": True,
        # },
        labels={"p_e": "price / earnings", "p_bv": "price / book value"},
        title="Price / Earnigns vs. Price / Book Value",
        subtitle="Relation between stocks current p/e and p/bv. Bubble size represented by p/iv and color by upside.",
    )

    fig.update_layout(title={"font": {"weight": 1000}}, legend_orientation="h")

    return fig


def plot_box_plot(valid_stocks: pd.DataFrame):
    fig = make_subplots(1, 4)
    fig.add_box(y=valid_stocks["upside"], row=1, col=1, name="upside [%]")
    fig.add_box(y=valid_stocks["p_e"], row=1, col=2, name="price / earnings")
    fig.add_box(y=valid_stocks["p_bv"], row=1, col=3, name="price / book value")
    fig.add_box(y=valid_stocks["p_iv"], row=1, col=4, name="price / intrinsic value")
    fig.update_layout(
        title={"text": "Box Plots", "font": {"weight": 1000}}, legend_orientation="h"
    )

    return fig
