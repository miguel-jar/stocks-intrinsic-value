# stocks-intrinsic-value

📈 Graham Intrinsic Value Analysis
A comprehensive financial analysis dashboard built with Streamlit to evaluate Brazilian (B3) stocks. This tool calculates the Benjamin Graham Intrinsic Value and provides deep insights through weighted metrics, interactive charts, and index-specific breakdowns (IBOV, SMLL, IDIV).

---

Benjamin Graham Intrinsic Value CalculationThe Graham number is used to estimate a stock's fundamental value by balancing its earnings power and asset value1. The logic implemented in this project (specifically within calculate_b3_all_stocks_iv) typically follows the classic formula:$$V = \sqrt{22.5 \times EPS \times BVPS}$$Where:$V$: Intrinsic Value 2$22.5$: The Graham multiplier (representing a P/E of 15 and a P/BV of 1.5) 3$EPS$: Earnings Per Share 4$BVPS$: Book Value Per Share 5

---

🚀 Features
Intrinsic Value Calculation: Automatically calculates fair value based on earnings (EPS) and book value (BVPS).

Index-Specific Analysis: Compare stock performance and valuation across major B3 indexes: IBOV, SMLL, and IDIV.

Weighted Metrics: View market-cap-weighted averages for upside, margin of security, P/E, and P/BV.

Interactive Visualizations: Includes upside histograms, box plots, and P/E vs. Upside scatter plots powered by Plotly.

Data Filtering: Dynamically filter "All Stocks" based on minimum market capitalization to focus on relevant opportunities.

---

🛠️ Tech Stack
Language: Python 3.12

Dashboard: Streamlit

Data Manipulation: Pandas

Charts: Plotly

Environment Management: Conda or Pip

---

📦 Installation

```bash
# Create the environment from the environment.yml file
conda env create -f environment.yml

# Activate the environment
conda activate intrinsic-value
```

```bash
pip install -r requirements.txt
```

---

🖥️ How to Run

After installing the dependencies, launch the dashboard by running:

```bash
streamlit run main.py
```