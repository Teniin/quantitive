"""
Unit tests for RiskMetrics class
"""

import pytest
import numpy as np
import pandas as pd
from portfolio_simulator import RiskMetrics


def test_sharpe_ratio():
    """Test Sharpe ratio calculation"""
    returns = np.array([0.01, 0.02, -0.01, 0.03, 0.01, 0.02])
    sharpe = RiskMetrics.sharpe_ratio(returns, risk_free_rate=0.02)

    assert isinstance(sharpe, float)
    assert not np.isnan(sharpe)


def test_sharpe_ratio_zero_std():
    """Test Sharpe ratio with zero standard deviation"""
    returns = np.array([0.01, 0.01, 0.01, 0.01])
    sharpe = RiskMetrics.sharpe_ratio(returns)

    assert sharpe == 0.0


def test_sortino_ratio():
    """Test Sortino ratio calculation"""
    returns = np.array([0.01, 0.02, -0.01, 0.03, -0.02, 0.01])
    sortino = RiskMetrics.sortino_ratio(returns, risk_free_rate=0.02)

    assert isinstance(sortino, float)
    assert not np.isnan(sortino)


def test_max_drawdown():
    """Test maximum drawdown calculation"""
    returns = pd.Series([0.01, 0.02, -0.05, -0.03, 0.04, 0.02])
    dd_metrics = RiskMetrics.max_drawdown(returns)

    assert 'max_drawdown' in dd_metrics
    assert 'max_drawdown_pct' in dd_metrics
    assert dd_metrics['max_drawdown'] <= 0  # Drawdown is negative


def test_volatility():
    """Test volatility calculation"""
    returns = np.array([0.01, 0.02, -0.01, 0.03, 0.01, 0.02])
    vol = RiskMetrics.volatility(returns)

    assert isinstance(vol, float)
    assert vol > 0


def test_beta():
    """Test beta calculation"""
    portfolio_returns = np.array([0.01, 0.02, -0.01, 0.03, 0.01])
    market_returns = np.array([0.01, 0.015, -0.005, 0.025, 0.01])

    beta = RiskMetrics.beta(portfolio_returns, market_returns)

    assert isinstance(beta, float)
    assert not np.isnan(beta)


def test_value_at_risk():
    """Test VaR calculation"""
    returns = np.random.normal(0.001, 0.02, 1000)
    var = RiskMetrics.value_at_risk(returns, confidence_level=0.95)

    assert isinstance(var, float)
    assert var < 0  # VaR is typically negative


def test_calculate_all_metrics():
    """Test comprehensive metrics calculation"""
    returns = pd.Series(np.random.normal(0.001, 0.02, 100))
    benchmark_returns = pd.Series(np.random.normal(0.001, 0.015, 100))

    metrics = RiskMetrics.calculate_all_metrics(
        returns,
        benchmark_returns,
        risk_free_rate=0.02
    )

    assert 'sharpe_ratio' in metrics
    assert 'sortino_ratio' in metrics
    assert 'max_drawdown' in metrics
    assert 'volatility' in metrics
    assert 'beta' in metrics
    assert 'alpha' in metrics


if __name__ == "__main__":
    pytest.main([__file__])
