"""
Backtester Module - Backtesting engine for portfolio strategies
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Callable, Tuple
from datetime import datetime
import matplotlib.pyplot as plt

from .portfolio import Portfolio
from .data_fetcher import DataFetcher
from .risk_metrics import RiskMetrics


class Strategy:
    """
    Base strategy class
    """

    def __init__(self, name: str = "Strategy"):
        """
        Initialize strategy

        Args:
            name: Strategy name
        """
        self.name = name

    def generate_signals(
        self,
        data: pd.DataFrame,
        current_idx: int
    ) -> Dict[str, str]:
        """
        Generate trading signals

        Args:
            data: Price data
            current_idx: Current index in the data

        Returns:
            Dictionary of signals {symbol: 'BUY'/'SELL'/'HOLD'}
        """
        raise NotImplementedError("Subclasses must implement generate_signals")


class BuyAndHoldStrategy(Strategy):
    """
    Simple buy and hold strategy
    """

    def __init__(self, symbols: List[str], weights: Optional[Dict[str, float]] = None):
        """
        Initialize buy and hold strategy

        Args:
            symbols: List of symbols to hold
            weights: Optional weights for each symbol
        """
        super().__init__(name="Buy and Hold")
        self.symbols = symbols
        self.weights = weights or {symbol: 1.0 / len(symbols) for symbol in symbols}
        self.initialized = False

    def generate_signals(
        self,
        data: pd.DataFrame,
        current_idx: int
    ) -> Dict[str, str]:
        """Generate signals - buy once at start, then hold"""
        if not self.initialized:
            self.initialized = True
            return {symbol: 'BUY' for symbol in self.symbols}
        return {symbol: 'HOLD' for symbol in self.symbols}


class MovingAverageCrossoverStrategy(Strategy):
    """
    Moving average crossover strategy
    """

    def __init__(
        self,
        symbols: List[str],
        short_window: int = 50,
        long_window: int = 200
    ):
        """
        Initialize MA crossover strategy

        Args:
            symbols: List of symbols
            short_window: Short MA window
            long_window: Long MA window
        """
        super().__init__(name="MA Crossover")
        self.symbols = symbols
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(
        self,
        data: pd.DataFrame,
        current_idx: int
    ) -> Dict[str, str]:
        """Generate signals based on MA crossover"""
        signals = {}

        # Need enough data for long MA
        if current_idx < self.long_window:
            return {symbol: 'HOLD' for symbol in self.symbols}

        for symbol in self.symbols:
            # Get historical prices
            if symbol in data.columns:
                prices = data[symbol].iloc[:current_idx + 1]

                # Calculate moving averages
                short_ma = prices.iloc[-self.short_window:].mean()
                long_ma = prices.iloc[-self.long_window:].mean()

                # Previous MAs
                short_ma_prev = prices.iloc[-self.short_window - 1:-1].mean()
                long_ma_prev = prices.iloc[-self.long_window - 1:-1].mean()

                # Crossover detection
                if short_ma > long_ma and short_ma_prev <= long_ma_prev:
                    signals[symbol] = 'BUY'
                elif short_ma < long_ma and short_ma_prev >= long_ma_prev:
                    signals[symbol] = 'SELL'
                else:
                    signals[symbol] = 'HOLD'
            else:
                signals[symbol] = 'HOLD'

        return signals


class Backtester:
    """
    Backtesting engine
    """

    def __init__(
        self,
        strategy: Strategy,
        initial_capital: float = 100000.0,
        commission: float = 0.0,
        data_fetcher: Optional[DataFetcher] = None
    ):
        """
        Initialize backtester

        Args:
            strategy: Trading strategy
            initial_capital: Starting capital
            commission: Commission per trade
            data_fetcher: Optional DataFetcher instance
        """
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.commission = commission
        self.data_fetcher = data_fetcher or DataFetcher()
        self.portfolio = Portfolio(initial_capital, name=strategy.name)
        self.results = None

    def run(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        rebalance_frequency: str = 'daily'
    ) -> Dict:
        """
        Run backtest

        Args:
            symbols: List of symbols to trade
            start_date: Start date
            end_date: End date
            rebalance_frequency: Rebalancing frequency

        Returns:
            Dictionary with backtest results
        """
        # Fetch data
        print(f"Fetching data for {symbols} from {start_date} to {end_date}...")
        price_data = self.data_fetcher.get_price_data(
            symbols,
            start_date=start_date,
            end_date=end_date
        )

        if price_data.empty:
            raise ValueError("No data available for the specified period")

        # Reset portfolio
        self.portfolio.reset()

        # Run simulation
        print(f"Running backtest for {self.strategy.name}...")
        for idx in range(len(price_data)):
            current_date = price_data.index[idx]
            current_prices = price_data.iloc[idx].to_dict()

            # Generate signals
            signals = self.strategy.generate_signals(price_data, idx)

            # Execute trades based on signals
            self._execute_signals(signals, current_prices, current_date)

            # Record portfolio state
            self.portfolio.record_portfolio_state(current_date, current_prices)

        # Calculate results
        self.results = self._calculate_results(price_data)

        print("Backtest complete!")
        return self.results

    def _execute_signals(
        self,
        signals: Dict[str, str],
        current_prices: Dict[str, float],
        current_date: datetime
    ):
        """
        Execute trading signals

        Args:
            signals: Trading signals
            current_prices: Current prices
            current_date: Current date
        """
        for symbol, signal in signals.items():
            if symbol not in current_prices:
                continue

            price = current_prices[symbol]
            current_holdings = self.portfolio.holdings.get(symbol, 0)

            if signal == 'BUY':
                # Calculate position size based on strategy weights
                if hasattr(self.strategy, 'weights') and symbol in self.strategy.weights:
                    target_weight = self.strategy.weights[symbol]
                    portfolio_value = self.portfolio.get_portfolio_value(current_prices)
                    target_value = portfolio_value * target_weight
                    target_shares = int(target_value / price)
                    shares_to_buy = target_shares - current_holdings

                    if shares_to_buy > 0:
                        self.portfolio.buy(
                            symbol,
                            shares_to_buy,
                            price,
                            current_date,
                            self.commission
                        )
                else:
                    # Default: invest 80% of available cash
                    available_cash = self.portfolio.cash * 0.8
                    shares = int(available_cash / (price * (1 + self.commission / price)))
                    if shares > 0:
                        self.portfolio.buy(
                            symbol,
                            shares,
                            price,
                            current_date,
                            self.commission
                        )

            elif signal == 'SELL':
                # Sell all holdings
                if current_holdings > 0:
                    self.portfolio.sell(
                        symbol,
                        current_holdings,
                        price,
                        current_date,
                        self.commission
                    )

    def _calculate_results(self, price_data: pd.DataFrame) -> Dict:
        """
        Calculate backtest results and metrics

        Args:
            price_data: Price data

        Returns:
            Dictionary with results
        """
        portfolio_history = self.portfolio.get_portfolio_history_df()

        if portfolio_history.empty:
            return {
                'error': 'No portfolio history available'
            }

        # Calculate returns
        portfolio_returns = self.portfolio.get_returns()

        # Calculate benchmark returns (equal-weighted buy and hold)
        benchmark_returns = price_data.pct_change().mean(axis=1).dropna()

        # Align returns
        common_dates = portfolio_returns.index.intersection(benchmark_returns.index)
        portfolio_returns = portfolio_returns.loc[common_dates]
        benchmark_returns = benchmark_returns.loc[common_dates]

        # Calculate metrics
        metrics = RiskMetrics.calculate_all_metrics(
            portfolio_returns,
            benchmark_returns
        )

        # Final portfolio value
        final_value = portfolio_history['portfolio_value'].iloc[-1]
        total_return = (final_value - self.initial_capital) / self.initial_capital

        results = {
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'total_return_pct': total_return * 100,
            'portfolio_history': portfolio_history,
            'portfolio_returns': portfolio_returns,
            'benchmark_returns': benchmark_returns,
            'transactions': self.portfolio.get_transaction_history_df(),
            'metrics': metrics,
            'strategy_name': self.strategy.name
        }

        return results

    def plot_results(self, figsize: Tuple[int, int] = (15, 10)):
        """
        Plot backtest results

        Args:
            figsize: Figure size
        """
        if self.results is None:
            print("No results to plot. Run backtest first.")
            return

        fig, axes = plt.subplots(3, 1, figsize=figsize)

        # Plot 1: Portfolio value over time
        portfolio_history = self.results['portfolio_history']
        axes[0].plot(portfolio_history.index, portfolio_history['portfolio_value'], label='Portfolio Value', linewidth=2)
        axes[0].axhline(y=self.initial_capital, color='r', linestyle='--', label='Initial Capital')
        axes[0].set_title(f'{self.strategy.name} - Portfolio Value Over Time', fontsize=14, fontweight='bold')
        axes[0].set_ylabel('Portfolio Value ($)')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Plot 2: Cumulative returns
        portfolio_returns = self.results['portfolio_returns']
        benchmark_returns = self.results['benchmark_returns']

        portfolio_cumulative = (1 + portfolio_returns).cumprod()
        benchmark_cumulative = (1 + benchmark_returns).cumprod()

        axes[1].plot(portfolio_cumulative.index, portfolio_cumulative, label='Strategy', linewidth=2)
        axes[1].plot(benchmark_cumulative.index, benchmark_cumulative, label='Benchmark (Buy & Hold)', linewidth=2)
        axes[1].set_title('Cumulative Returns Comparison', fontsize=14, fontweight='bold')
        axes[1].set_ylabel('Cumulative Return')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        # Plot 3: Drawdown
        cumulative = (1 + portfolio_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max

        axes[2].fill_between(drawdown.index, drawdown * 100, 0, alpha=0.3, color='red')
        axes[2].plot(drawdown.index, drawdown * 100, color='red', linewidth=1)
        axes[2].set_title('Drawdown Over Time', fontsize=14, fontweight='bold')
        axes[2].set_ylabel('Drawdown (%)')
        axes[2].set_xlabel('Date')
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

        return fig

    def print_summary(self):
        """Print backtest summary"""
        if self.results is None:
            print("No results available. Run backtest first.")
            return

        print("\n" + "=" * 60)
        print(f"BACKTEST RESULTS: {self.strategy.name}")
        print("=" * 60)

        print(f"\nInitial Capital:  ${self.results['initial_capital']:,.2f}")
        print(f"Final Value:      ${self.results['final_value']:,.2f}")
        print(f"Total Return:     {self.results['total_return_pct']:.2f}%")

        print("\n" + "-" * 60)
        print("PERFORMANCE METRICS")
        print("-" * 60)

        metrics = self.results['metrics']
        print(f"Annualized Return:       {metrics['annualized_return_pct']:.2f}%")
        print(f"Annualized Volatility:   {metrics['volatility_pct']:.2f}%")
        print(f"Sharpe Ratio:            {metrics['sharpe_ratio']:.3f}")
        print(f"Sortino Ratio:           {metrics['sortino_ratio']:.3f}")
        print(f"Calmar Ratio:            {metrics['calmar_ratio']:.3f}")
        print(f"Max Drawdown:            {metrics['max_drawdown_pct']:.2f}%")
        print(f"Value at Risk (95%):     {metrics['var_95']:.4f}")
        print(f"CVaR (95%):              {metrics['cvar_95']:.4f}")

        if 'beta' in metrics:
            print(f"\nBeta:                    {metrics['beta']:.3f}")
            print(f"Alpha (annualized):      {metrics['alpha']:.4f}")
            print(f"Information Ratio:       {metrics['information_ratio']:.3f}")

        print("\n" + "-" * 60)
        print(f"Total Transactions:      {len(self.results['transactions'])}")
        print("=" * 60 + "\n")
