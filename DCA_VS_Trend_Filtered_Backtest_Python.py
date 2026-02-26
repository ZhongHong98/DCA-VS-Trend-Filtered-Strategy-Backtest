from AlgorithmImports import *
import numpy as np
from datetime import datetime

class DCAWithTrendFilter(QCAlgorithm):

    def Initialize(self):
        
        # ==========================
        # PARAMETERS
        # ==========================
        self.initial_cash = 1000
        self.monthly_contribution = 1000
        self.enable_trend_filter = True
        self.ma_period = 200
        
        self.asset_to_trade = "QQQ"
        self.trend_reference_asset = "QQQ"
        
        self.transaction_fee_rate = 0.0001  # 0.01%
        
        # ==========================
        # BACKTEST PERIOD
        # ==========================
        self.SetStartDate(2010, 2, 11)   # TQQQ inception
        self.SetEndDate(2026, 2, 26)
        self.SetCash(self.initial_cash)
        
        # ==========================
        # ADD SECURITIES
        # ==========================
        self.trade_symbol = self.AddEquity(self.asset_to_trade, Resolution.Daily).Symbol
        self.ref_symbol = self.AddEquity(self.trend_reference_asset, Resolution.Daily).Symbol
        
        # Custom fee model
        self.Securities[self.trade_symbol].SetFeeModel(CustomFeeModel(self.transaction_fee_rate))
        
        # Moving average
        self.ma = self.SMA(self.ref_symbol, self.ma_period, Resolution.Daily)
        
        # Warmup for MA
        self.SetWarmUp(self.ma_period)
        
        # Schedule monthly DCA on 1st trading day
        self.Schedule.On(
            self.DateRules.MonthStart(self.trade_symbol),
            self.TimeRules.AfterMarketOpen(self.trade_symbol, 1),
            self.MonthlyInvestment
        )
        
        # Performance tracking
        self.equity_curve = []
        self.daily_returns = []
        self.last_portfolio_value = None
        self.year_returns = {}
        self.current_year = None
        self.year_start_value = None
        self.days_in_market = 0
        self.total_days = 0
        self.trade_count = 0

    def MonthlyInvestment(self):
        if self.IsWarmingUp:
            return
        
        self.Portfolio.CashBook["USD"].AddAmount(self.monthly_contribution)
        
        if not self.enable_trend_filter:
            self.BuyWithAllCash()
        else:
            if self.Securities[self.ref_symbol].Price > self.ma.Current.Value:
                self.BuyWithAllCash()

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        self.total_days += 1
        
        invested = self.Portfolio[self.trade_symbol].Invested
        
        if invested:
            self.days_in_market += 1
        
        # Trend exit
        if self.enable_trend_filter and invested:
            if self.Securities[self.ref_symbol].Price < self.ma.Current.Value:
                self.Liquidate(self.trade_symbol)
        
        # Track equity curve
        portfolio_value = self.Portfolio.TotalPortfolioValue
        self.equity_curve.append(portfolio_value)
        
        if self.last_portfolio_value:
            daily_return = (portfolio_value / self.last_portfolio_value) - 1
            self.daily_returns.append(daily_return)
        
        self.last_portfolio_value = portfolio_value
        
        # Year tracking
        year = self.Time.year
        if self.current_year != year:
            self.current_year = year
            self.year_start_value = portfolio_value
        
        if year not in self.year_returns:
            self.year_returns[year] = []
        
        if self.last_portfolio_value:
            self.year_returns[year].append(portfolio_value)

    def BuyWithAllCash(self):
        cash = self.Portfolio.Cash
        price = self.Securities[self.trade_symbol].Price
        
        if price > 0:
            quantity = cash / price
            self.MarketOrder(self.trade_symbol, quantity)
            self.trade_count += 1

    def OnEndOfAlgorithm(self):
        
        if len(self.daily_returns) == 0:
            return
        
        total_return = (self.equity_curve[-1] / self.initial_cash) - 1
        
        years = (self.EndDate - self.StartDate).days / 365
        cagr = (1 + total_return) ** (1 / years) - 1
        
        daily_returns = np.array(self.daily_returns)
        
        volatility = np.std(daily_returns) * np.sqrt(252)
        
        sharpe = (np.mean(daily_returns) * 252) / volatility if volatility != 0 else 0
        
        downside_returns = daily_returns[daily_returns < 0]
        downside_std = np.std(downside_returns) * np.sqrt(252) if len(downside_returns) > 0 else 0
        sortino = (np.mean(daily_returns) * 252) / downside_std if downside_std != 0 else 0
        
        # Max Drawdown
        cumulative = np.maximum.accumulate(self.equity_curve)
        drawdown = (self.equity_curve - cumulative) / cumulative
        max_dd = np.min(drawdown)
        
        calmar = cagr / abs(max_dd) if max_dd != 0 else 0
        
        # Worst year
        worst_year = 0
        for year, values in self.year_returns.items():
            if len(values) > 1:
                yearly_return = (values[-1] / values[0]) - 1
                worst_year = min(worst_year, yearly_return)
        
        time_invested = self.days_in_market / self.total_days if self.total_days > 0 else 0
        
        self.Debug(f"CAGR: {round(cagr*100,2)}%")
        self.Debug(f"Sharpe Ratio: {round(sharpe,2)}")
        self.Debug(f"Max Drawdown: {round(max_dd*100,2)}%")
        self.Debug(f"Total Return: {round(total_return*100,2)}%")
        self.Debug(f"Annual Volatility: {round(volatility*100,2)}%")
        self.Debug(f"Worst Year: {round(worst_year*100,2)}%")
        self.Debug(f"Time Invested: {round(time_invested*100,2)}%")
        self.Debug(f"Sortino Ratio: {round(sortino,2)}")
        self.Debug(f"Calmar Ratio: {round(calmar,2)}")
        self.Debug(f"Number of Trades: {self.trade_count}")


class CustomFeeModel(FeeModel):
    def __init__(self, fee_rate):
        self.fee_rate = fee_rate

    def GetOrderFee(self, parameters):
        fee = parameters.Security.Price * abs(parameters.Order.Quantity) * self.fee_rate
        return OrderFee(CashAmount(fee, "USD"))