"""
Portfolio Module - Manages portfolio holdings and performance tracking
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class Portfolio:
    """
    Portfolio class for managing holdings and tracking performance
    """

    def __init__(
        self,
        initial_capital: float = 100000.0,
        name: str = "Portfolio"
    ):
        """
        Initialize Portfolio

        Args:
            initial_capital: Starting capital
            name: Portfolio name
        """
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.name = name
        self.holdings = {}  # {symbol: quantity}
        self.cash = initial_capital
        self.transaction_history = []
        self.portfolio_history = []

    def buy(
        self,
        symbol: str,
        quantity: int,
        price: float,
        date: Optional[datetime] = None,
        commission: float = 0.0
    ) -> bool:
        """
        Buy shares

        Args:
            symbol: Ticker symbol
            quantity: Number of shares
            price: Price per share
            date: Transaction date
            commission: Transaction commission

        Returns:
            True if successful, False otherwise
        """
        total_cost = quantity * price + commission

        if total_cost > self.cash:
            return False

        # Update cash
        self.cash -= total_cost

        # Update holdings
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity

        # Record transaction
        self.transaction_history.append({
            'date': date or datetime.now(),
            'type': 'BUY',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'commission': commission,
            'total': total_cost
        })

        return True

    def sell(
        self,
        symbol: str,
        quantity: int,
        price: float,
        date: Optional[datetime] = None,
        commission: float = 0.0
    ) -> bool:
        """
        Sell shares

        Args:
            symbol: Ticker symbol
            quantity: Number of shares
            price: Price per share
            date: Transaction date
            commission: Transaction commission

        Returns:
            True if successful, False otherwise
        """
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            return False

        # Update holdings
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]

        # Update cash
        total_proceeds = quantity * price - commission
        self.cash += total_proceeds

        # Record transaction
        self.transaction_history.append({
            'date': date or datetime.now(),
            'type': 'SELL',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'commission': commission,
            'total': total_proceeds
        })

        return True

    def get_holdings(self) -> Dict[str, int]:
        """Get current holdings"""
        return self.holdings.copy()

    def get_position_value(self, symbol: str, current_price: float) -> float:
        """
        Get the value of a position

        Args:
            symbol: Ticker symbol
            current_price: Current price

        Returns:
            Position value
        """
        if symbol not in self.holdings:
            return 0.0
        return self.holdings[symbol] * current_price

    def get_portfolio_value(self, current_prices: Dict[str, float]) -> float:
        """
        Calculate total portfolio value

        Args:
            current_prices: Dictionary of current prices {symbol: price}

        Returns:
            Total portfolio value
        """
        holdings_value = sum(
            self.holdings.get(symbol, 0) * current_prices.get(symbol, 0)
            for symbol in self.holdings
        )
        return self.cash + holdings_value

    def get_allocation(self, current_prices: Dict[str, float]) -> Dict[str, float]:
        """
        Get portfolio allocation percentages

        Args:
            current_prices: Dictionary of current prices

        Returns:
            Dictionary of allocations {symbol: percentage}
        """
        total_value = self.get_portfolio_value(current_prices)

        if total_value == 0:
            return {}

        allocation = {}
        allocation['CASH'] = (self.cash / total_value) * 100

        for symbol in self.holdings:
            position_value = self.get_position_value(symbol, current_prices.get(symbol, 0))
            allocation[symbol] = (position_value / total_value) * 100

        return allocation

    def record_portfolio_state(
        self,
        date: datetime,
        current_prices: Dict[str, float]
    ):
        """
        Record current portfolio state

        Args:
            date: Current date
            current_prices: Current prices
        """
        portfolio_value = self.get_portfolio_value(current_prices)

        self.portfolio_history.append({
            'date': date,
            'portfolio_value': portfolio_value,
            'cash': self.cash,
            'holdings_value': portfolio_value - self.cash,
            'holdings': self.holdings.copy()
        })

    def get_portfolio_history_df(self) -> pd.DataFrame:
        """
        Get portfolio history as DataFrame

        Returns:
            DataFrame with portfolio history
        """
        if not self.portfolio_history:
            return pd.DataFrame()

        df = pd.DataFrame(self.portfolio_history)
        df.set_index('date', inplace=True)
        return df

    def get_transaction_history_df(self) -> pd.DataFrame:
        """
        Get transaction history as DataFrame

        Returns:
            DataFrame with transaction history
        """
        if not self.transaction_history:
            return pd.DataFrame()

        df = pd.DataFrame(self.transaction_history)
        df.set_index('date', inplace=True)
        return df

    def get_returns(self) -> pd.Series:
        """
        Calculate portfolio returns

        Returns:
            Series of portfolio returns
        """
        history_df = self.get_portfolio_history_df()
        if history_df.empty:
            return pd.Series()

        returns = history_df['portfolio_value'].pct_change()
        return returns.dropna()

    def reset(self):
        """Reset portfolio to initial state"""
        self.capital = self.initial_capital
        self.cash = self.initial_capital
        self.holdings = {}
        self.transaction_history = []
        self.portfolio_history = []

    def summary(self, current_prices: Optional[Dict[str, float]] = None) -> Dict:
        """
        Get portfolio summary

        Args:
            current_prices: Current prices (if not provided, returns basic info)

        Returns:
            Dictionary with portfolio summary
        """
        summary = {
            'name': self.name,
            'initial_capital': self.initial_capital,
            'cash': self.cash,
            'holdings': self.holdings.copy(),
            'num_transactions': len(self.transaction_history)
        }

        if current_prices:
            portfolio_value = self.get_portfolio_value(current_prices)
            total_return = ((portfolio_value - self.initial_capital) / self.initial_capital) * 100

            summary.update({
                'portfolio_value': portfolio_value,
                'total_return': total_return,
                'total_return_pct': f"{total_return:.2f}%",
                'allocation': self.get_allocation(current_prices)
            })

        return summary
