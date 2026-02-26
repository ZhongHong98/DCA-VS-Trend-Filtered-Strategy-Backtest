# DCA-VS-Trend-Filtered-Strategy-Backtest
QQQ &amp; TQQQ Comparative Study (2010–2026)

## 📌 Project Objective

This study evaluates whether applying a 200-day Moving Average (MA200) trend filter improves long-term performance and risk-adjusted returns for:

- QQQ (Nasdaq 100 ETF)

- TQQQ (3x Leveraged Nasdaq 100 ETF)

All strategies use:

- Monthly Dollar Cost Averaging (DCA)

- $1,000 initial capital

- $1,000 monthly contribution

- 0.01% transaction fee

- Dividends reinvested

- Fractional shares allowed

- Backtest period: Feb 11, 2010 – Feb 26, 2026

- Start date aligned with TQQQ inception

## 📊 Strategy Comparison Results

| Strategy   | CAGR   | Sharpe | Max DD  | Total Return | Volatility | Worst Year | Time Invested | Sortino | Calmar | Trades |
| ---------- | ------ | ------ | ------- | ------------ | ---------- | ---------- | ------------- | ------- | ------ | ------ |
| QQQ DCA    | 55.45% | 1.30   | -33.75% | 106,654.80%  | 37.93%     | -31.69%    | 99.73%        | 3.06    | 1.64   | 189    |
| QQQ MA200  | 51.34% | 1.28   | -17.91% | 69,755.80%   | 35.58%     | -7.74%     | 77.93%        | 3.38    | 2.87   | 160    |
| TQQQ DCA   | 76.66% | 1.13   | -81.56% | 805,531.87%  | 68.70%     | -79.57%    | 99.73%        | 1.63    | 0.94   | 189    |
| TQQQ MA200 | 70.35% | 1.19   | -56.97% | 453,201.61%  | 55.34%     | -28.74%    | 77.99%        | 1.66    | 1.23   | 160    |

## 📈 Performance Metric Definitions

### CAGR (Compound Annual Growth Rate)

Annualized return over the full period.
Measures long-term growth rate.

### Sharpe Ratio

Risk-adjusted return based on total volatility.
Higher is better.

### Max Drawdown

Largest peak-to-trough portfolio decline.
Measures worst capital loss.

### Total Return

Overall portfolio growth over entire period.

### Annual Volatility

Standard deviation of annualized returns.
Measures risk level.

### Worst Calendar Year

Worst single-year return.

### Time Invested

Percentage of time portfolio was invested (not in cash).

### Sortino Ratio

Risk-adjusted return considering only downside volatility.
More precise than Sharpe for long-term investing.

### Calmar Ratio

CAGR divided by Max Drawdown.
Measures return per unit of drawdown risk.

### Number of Trades

Total buy/sell executions.

## 🔎 Analysis & Comparison
### 🟢 QQQ DCA vs QQQ MA200

DCA produced higher CAGR (55.45% vs 51.34%)

MA200 dramatically reduced Max Drawdown (-17.91% vs -33.75%)

Worst year significantly improved (-7.74% vs -31.69%)

Calmar ratio much higher (2.87 vs 1.64)

### 👉 Conclusion:
MA200 reduces downside risk substantially with only minor return sacrifice.
For risk-adjusted performance, QQQ MA200 is superior.

## 🔴 TQQQ DCA vs TQQQ MA200

- Pure DCA delivered highest CAGR (76.66%)

- However, drawdown was extreme (-81.56%)

- Worst year nearly -80%

- MA200 reduced drawdown to -56.97%

- Volatility reduced from 68.70% to 55.34%

- Calmar ratio improved (1.23 vs 0.94)

### 👉 Conclusion:
Trend filtering significantly reduces catastrophic losses in leveraged ETFs.
However, volatility remains high.

## 🏆 Overall Strategy Evaluation
### 🥇 Highest Return:

TQQQ DCA

But:

- Extremely high risk

- 80% drawdown is psychologically and practically difficult to sustain

### 🥈 Best Risk-Adjusted Performance:

QQQ MA200

Reasons:

- Strong CAGR (51%)

- Very controlled drawdown (-17.91%)

- Best Calmar ratio (2.87)

- Best Sortino ratio (3.38)

- Improved worst-year performance

This strategy offers the most balanced return-to-risk profile.

## 💡 Key Insights

1. Leverage amplifies both gains and losses dramatically.

2. MA200 trend filter significantly reduces drawdowns.

3. Risk-adjusted metrics favor filtered strategies.

4. Time in market drops to ~78% under MA200 filter.

5. Leveraged DCA without risk control can lead to extreme losses.

## ⚠ Important Disclaimer

- Backtest period begins February 11, 2010, aligned with TQQQ inception.

- Major financial crises prior to 2010 (e.g., Dot-com crash 2000, Global Financial Crisis 2008) are not included.

- Results may differ significantly if earlier crisis periods were included.

- Backtesting does not guarantee future performance.

- No slippage modeling beyond basic assumptions.

- Market regime during 2010–2026 was largely tech-growth dominated.

## 🎯 Final Conclusion

If prioritizing:

- Maximum return → TQQQ DCA

- Balanced growth & controlled risk → QQQ MA200

- Leverage with some protection → TQQQ MA200

From a portfolio construction perspective,
QQQ MA200 provides the most stable and risk-efficient performance.

## 🛠 How to Modify Strategy Parameters

This project is fully parameterized.
You can adjust the following variables in the Python algorithm:

```Python
self.initial_cash = 1000
self.monthly_contribution = 1000
self.enable_trend_filter = True
self.ma_period = 200

self.asset_to_trade = "TQQQ"
self.trend_reference_asset = "QQQ"

self.SetStartDate(2010, 2, 11)
self.SetEndDate(2026, 2, 26)
```

Adjustable Parameters
| Parameter               | Description                    |
| ----------------------- | ------------------------------ |
| `initial_cash`          | Starting portfolio capital     |
| `monthly_contribution`  | Monthly DCA amount             |
| `enable_trend_filter`   | Enable/disable MA filter       |
| `ma_period`             | Moving average lookback period |
| `asset_to_trade`        | Asset being purchased          |
| `trend_reference_asset` | Asset used for MA signal       |
| `start_date`            | Backtest start                 |
| `end_date`              | Backtest end                   |

This allows flexible testing of:

- Different MA lengths (100, 150, 250)

- Different ETFs

- Different capital allocations

- Different market periods

📁 Python file: [View Python File](Python/DCA_VS_Trend_Filtered_Backtest_Python.py)

## 📚 Tools Used

Python

QuantConnect Lean Engine

Numpy

Time-series performance analysis
