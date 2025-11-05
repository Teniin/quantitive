"""
Unit tests for Portfolio class
"""

import pytest
from datetime import datetime
from portfolio_simulator import Portfolio


def test_portfolio_initialization():
    """Test portfolio initialization"""
    portfolio = Portfolio(initial_capital=100000, name="Test Portfolio")
    assert portfolio.initial_capital == 100000
    assert portfolio.cash == 100000
    assert portfolio.name == "Test Portfolio"
    assert len(portfolio.holdings) == 0


def test_buy_stock():
    """Test buying stock"""
    portfolio = Portfolio(initial_capital=100000)
    success = portfolio.buy('AAPL', 100, 150.0)

    assert success == True
    assert portfolio.holdings['AAPL'] == 100
    assert portfolio.cash == 100000 - (100 * 150.0)


def test_buy_insufficient_cash():
    """Test buying with insufficient cash"""
    portfolio = Portfolio(initial_capital=1000)
    success = portfolio.buy('AAPL', 100, 150.0)  # Need $15,000

    assert success == False
    assert 'AAPL' not in portfolio.holdings


def test_sell_stock():
    """Test selling stock"""
    portfolio = Portfolio(initial_capital=100000)
    portfolio.buy('AAPL', 100, 150.0)

    initial_cash = portfolio.cash
    success = portfolio.sell('AAPL', 50, 160.0)

    assert success == True
    assert portfolio.holdings['AAPL'] == 50
    assert portfolio.cash == initial_cash + (50 * 160.0)


def test_sell_insufficient_shares():
    """Test selling more shares than owned"""
    portfolio = Portfolio(initial_capital=100000)
    portfolio.buy('AAPL', 100, 150.0)

    success = portfolio.sell('AAPL', 150, 160.0)

    assert success == False
    assert portfolio.holdings['AAPL'] == 100


def test_get_portfolio_value():
    """Test portfolio value calculation"""
    portfolio = Portfolio(initial_capital=100000)
    portfolio.buy('AAPL', 100, 150.0)
    portfolio.buy('MSFT', 50, 300.0)

    current_prices = {'AAPL': 160.0, 'MSFT': 320.0}
    portfolio_value = portfolio.get_portfolio_value(current_prices)

    expected_value = portfolio.cash + (100 * 160.0) + (50 * 320.0)
    assert portfolio_value == expected_value


def test_get_allocation():
    """Test allocation calculation"""
    portfolio = Portfolio(initial_capital=100000)
    portfolio.buy('AAPL', 100, 150.0)

    current_prices = {'AAPL': 150.0}
    allocation = portfolio.get_allocation(current_prices)

    assert 'AAPL' in allocation
    assert 'CASH' in allocation
    assert abs(sum(allocation.values()) - 100.0) < 0.01  # Should sum to 100%


def test_reset_portfolio():
    """Test portfolio reset"""
    portfolio = Portfolio(initial_capital=100000)
    portfolio.buy('AAPL', 100, 150.0)

    portfolio.reset()

    assert portfolio.cash == portfolio.initial_capital
    assert len(portfolio.holdings) == 0
    assert len(portfolio.transaction_history) == 0


if __name__ == "__main__":
    pytest.main([__file__])
