"""
Risk Metrics Module - Calculate various risk and performance metrics
"""

import pandas as pd
import numpy as np
from typing import Union, Optional, Dict
from scipy import stats


class RiskMetrics:
    """
    Calculate portfolio risk and performance metrics
    """

    @staticmethod
    def sharpe_ratio(
        returns: Union[pd.Series, np.ndarray],
        risk_free_rate: float = 0.02,
        periods_per_year: int = 252
    ) -> float:
        """
        Calculate Sharpe Ratio

        Args:
            returns: Series or array of returns
            risk_free_rate: Annual risk-free rate
            periods_per_year: Trading periods per year (252 for daily, 12 for monthly)

        Returns:
            Sharpe ratio
        """
        if isinstance(returns, pd.Series):
            returns = returns.values

        if len(returns) == 0:
            return 0.0

        # Convert annual risk-free rate to period rate
        rf_per_period = (1 + risk_free_rate) ** (1 / periods_per_year) - 1

        excess_returns = returns - rf_per_period
        mean_excess = np.mean(excess_returns)
        std_excess = np.std(excess_returns, ddof=1)

        if std_excess == 0:
            return 0.0

        # Annualize
        sharpe = (mean_excess / std_excess) * np.sqrt(periods_per_year)
        return sharpe

    @staticmethod
    def sortino_ratio(
        returns: Union[pd.Series, np.ndarray],
        risk_free_rate: float = 0.02,
        periods_per_year: int = 252
    ) -> float:
        """
        Calculate Sortino Ratio (only considers downside volatility)

        Args:
            returns: Series or array of returns
            risk_free_rate: Annual risk-free rate
            periods_per_year: Trading periods per year

        Returns:
            Sortino ratio
        """
        if isinstance(returns, pd.Series):
            returns = returns.values

        if len(returns) == 0:
            return 0.0

        # Convert annual risk-free rate to period rate
        rf_per_period = (1 + risk_free_rate) ** (1 / periods_per_year) - 1

        excess_returns = returns - rf_per_period
        mean_excess = np.mean(excess_returns)

        # Calculate downside deviation
        downside_returns = excess_returns[excess_returns < 0]
        if len(downside_returns) == 0:
            return np.inf if mean_excess > 0 else 0.0

        downside_std = np.std(downside_returns, ddof=1)

        if downside_std == 0:
            return 0.0

        # Annualize
        sortino = (mean_excess / downside_std) * np.sqrt(periods_per_year)
        return sortino

    @staticmethod
    def max_drawdown(
        returns: Union[pd.Series, np.ndarray],
        cumulative: bool = False
    ) -> Dict[str, float]:
        """
        Calculate maximum drawdown

        Args:
            returns: Series or array of returns
            cumulative: Whether returns are already cumulative

        Returns:
            Dictionary with max_drawdown, peak_date, trough_date, recovery_date
        """
        if isinstance(returns, np.ndarray):
            returns = pd.Series(returns)

        if len(returns) == 0:
            return {'max_drawdown': 0.0, 'peak_idx': None, 'trough_idx': None}

        # Calculate cumulative returns
        if not cumulative:
            cum_returns = (1 + returns).cumprod()
        else:
            cum_returns = returns

        # Calculate running maximum
        running_max = cum_returns.expanding().max()

        # Calculate drawdown
        drawdown = (cum_returns - running_max) / running_max

        # Find maximum drawdown
        max_dd = drawdown.min()

        # Find the indices
        trough_idx = drawdown.idxmin()
        peak_idx = cum_returns[:trough_idx].idxmax() if len(cum_returns[:trough_idx]) > 0 else None

        # Find recovery date (if any)
        recovery_idx = None
        if peak_idx is not None:
            recovery_series = cum_returns[trough_idx:]
            peak_value = cum_returns[peak_idx]
            recovery_mask = recovery_series >= peak_value
            if recovery_mask.any():
                recovery_idx = recovery_mask.idxmax()

        return {
            'max_drawdown': max_dd,
            'max_drawdown_pct': max_dd * 100,
            'peak_idx': peak_idx,
            'trough_idx': trough_idx,
            'recovery_idx': recovery_idx
        }

    @staticmethod
    def calmar_ratio(
        returns: Union[pd.Series, np.ndarray],
        periods_per_year: int = 252
    ) -> float:
        """
        Calculate Calmar Ratio (annualized return / max drawdown)

        Args:
            returns: Series or array of returns
            periods_per_year: Trading periods per year

        Returns:
            Calmar ratio
        """
        if isinstance(returns, pd.Series):
            returns_array = returns.values
        else:
            returns_array = returns

        if len(returns_array) == 0:
            return 0.0

        # Annualized return
        total_return = np.prod(1 + returns_array) - 1
        n_periods = len(returns_array)
        annualized_return = (1 + total_return) ** (periods_per_year / n_periods) - 1

        # Max drawdown
        max_dd = RiskMetrics.max_drawdown(returns)['max_drawdown']

        if max_dd == 0:
            return 0.0

        return annualized_return / abs(max_dd)

    @staticmethod
    def value_at_risk(
        returns: Union[pd.Series, np.ndarray],
        confidence_level: float = 0.95
    ) -> float:
        """
        Calculate Value at Risk (VaR)

        Args:
            returns: Series or array of returns
            confidence_level: Confidence level (e.g., 0.95 for 95%)

        Returns:
            VaR value
        """
        if isinstance(returns, pd.Series):
            returns = returns.values

        if len(returns) == 0:
            return 0.0

        var = np.percentile(returns, (1 - confidence_level) * 100)
        return var

    @staticmethod
    def conditional_value_at_risk(
        returns: Union[pd.Series, np.ndarray],
        confidence_level: float = 0.95
    ) -> float:
        """
        Calculate Conditional Value at Risk (CVaR) / Expected Shortfall

        Args:
            returns: Series or array of returns
            confidence_level: Confidence level

        Returns:
            CVaR value
        """
        if isinstance(returns, pd.Series):
            returns = returns.values

        if len(returns) == 0:
            return 0.0

        var = RiskMetrics.value_at_risk(returns, confidence_level)
        cvar = returns[returns <= var].mean()
        return cvar

    @staticmethod
    def volatility(
        returns: Union[pd.Series, np.ndarray],
        periods_per_year: int = 252
    ) -> float:
        """
        Calculate annualized volatility

        Args:
            returns: Series or array of returns
            periods_per_year: Trading periods per year

        Returns:
            Annualized volatility
        """
        if isinstance(returns, pd.Series):
            returns = returns.values

        if len(returns) == 0:
            return 0.0

        std = np.std(returns, ddof=1)
        annualized_vol = std * np.sqrt(periods_per_year)
        return annualized_vol

    @staticmethod
    def beta(
        returns: Union[pd.Series, np.ndarray],
        market_returns: Union[pd.Series, np.ndarray]
    ) -> float:
        """
        Calculate beta relative to market

        Args:
            returns: Portfolio returns
            market_returns: Market returns

        Returns:
            Beta value
        """
        if isinstance(returns, pd.Series):
            returns = returns.values
        if isinstance(market_returns, pd.Series):
            market_returns = market_returns.values

        if len(returns) == 0 or len(market_returns) == 0:
            return 0.0

        # Ensure same length
        min_len = min(len(returns), len(market_returns))
        returns = returns[:min_len]
        market_returns = market_returns[:min_len]

        covariance = np.cov(returns, market_returns)[0, 1]
        market_variance = np.var(market_returns, ddof=1)

        if market_variance == 0:
            return 0.0

        return covariance / market_variance

    @staticmethod
    def alpha(
        returns: Union[pd.Series, np.ndarray],
        market_returns: Union[pd.Series, np.ndarray],
        risk_free_rate: float = 0.02,
        periods_per_year: int = 252
    ) -> float:
        """
        Calculate alpha (excess return over CAPM expected return)

        Args:
            returns: Portfolio returns
            market_returns: Market returns
            risk_free_rate: Annual risk-free rate
            periods_per_year: Trading periods per year

        Returns:
            Alpha value (annualized)
        """
        if isinstance(returns, pd.Series):
            returns = returns.values
        if isinstance(market_returns, pd.Series):
            market_returns = market_returns.values

        if len(returns) == 0 or len(market_returns) == 0:
            return 0.0

        # Calculate beta
        beta_value = RiskMetrics.beta(returns, market_returns)

        # Convert risk-free rate to period rate
        rf_per_period = (1 + risk_free_rate) ** (1 / periods_per_year) - 1

        # Calculate average returns
        avg_return = np.mean(returns)
        avg_market_return = np.mean(market_returns)

        # Calculate alpha
        alpha_per_period = avg_return - (rf_per_period + beta_value * (avg_market_return - rf_per_period))

        # Annualize
        alpha_annualized = alpha_per_period * periods_per_year

        return alpha_annualized

    @staticmethod
    def information_ratio(
        returns: Union[pd.Series, np.ndarray],
        benchmark_returns: Union[pd.Series, np.ndarray],
        periods_per_year: int = 252
    ) -> float:
        """
        Calculate Information Ratio

        Args:
            returns: Portfolio returns
            benchmark_returns: Benchmark returns
            periods_per_year: Trading periods per year

        Returns:
            Information ratio
        """
        if isinstance(returns, pd.Series):
            returns = returns.values
        if isinstance(benchmark_returns, pd.Series):
            benchmark_returns = benchmark_returns.values

        if len(returns) == 0 or len(benchmark_returns) == 0:
            return 0.0

        # Calculate tracking error (active returns)
        min_len = min(len(returns), len(benchmark_returns))
        returns = returns[:min_len]
        benchmark_returns = benchmark_returns[:min_len]

        active_returns = returns - benchmark_returns
        avg_active_return = np.mean(active_returns)
        tracking_error = np.std(active_returns, ddof=1)

        if tracking_error == 0:
            return 0.0

        # Annualize
        ir = (avg_active_return / tracking_error) * np.sqrt(periods_per_year)
        return ir

    @staticmethod
    def calculate_all_metrics(
        returns: Union[pd.Series, np.ndarray],
        benchmark_returns: Optional[Union[pd.Series, np.ndarray]] = None,
        risk_free_rate: float = 0.02,
        periods_per_year: int = 252
    ) -> Dict[str, float]:
        """
        Calculate all available risk metrics

        Args:
            returns: Portfolio returns
            benchmark_returns: Optional benchmark returns
            risk_free_rate: Annual risk-free rate
            periods_per_year: Trading periods per year

        Returns:
            Dictionary with all metrics
        """
        if isinstance(returns, pd.Series):
            returns_array = returns.values
        else:
            returns_array = returns

        metrics = {}

        # Basic metrics
        if len(returns_array) > 0:
            total_return = np.prod(1 + returns_array) - 1
            n_periods = len(returns_array)
            annualized_return = (1 + total_return) ** (periods_per_year / n_periods) - 1

            metrics['total_return'] = total_return
            metrics['total_return_pct'] = total_return * 100
            metrics['annualized_return'] = annualized_return
            metrics['annualized_return_pct'] = annualized_return * 100
        else:
            metrics['total_return'] = 0.0
            metrics['total_return_pct'] = 0.0
            metrics['annualized_return'] = 0.0
            metrics['annualized_return_pct'] = 0.0

        # Risk metrics
        metrics['sharpe_ratio'] = RiskMetrics.sharpe_ratio(returns, risk_free_rate, periods_per_year)
        metrics['sortino_ratio'] = RiskMetrics.sortino_ratio(returns, risk_free_rate, periods_per_year)
        metrics['volatility'] = RiskMetrics.volatility(returns, periods_per_year)
        metrics['volatility_pct'] = metrics['volatility'] * 100

        # Drawdown metrics
        dd_metrics = RiskMetrics.max_drawdown(returns)
        metrics['max_drawdown'] = dd_metrics['max_drawdown']
        metrics['max_drawdown_pct'] = dd_metrics['max_drawdown_pct']

        metrics['calmar_ratio'] = RiskMetrics.calmar_ratio(returns, periods_per_year)

        # VaR metrics
        metrics['var_95'] = RiskMetrics.value_at_risk(returns, 0.95)
        metrics['cvar_95'] = RiskMetrics.conditional_value_at_risk(returns, 0.95)

        # Benchmark-relative metrics
        if benchmark_returns is not None:
            metrics['beta'] = RiskMetrics.beta(returns, benchmark_returns)
            metrics['alpha'] = RiskMetrics.alpha(returns, benchmark_returns, risk_free_rate, periods_per_year)
            metrics['information_ratio'] = RiskMetrics.information_ratio(returns, benchmark_returns, periods_per_year)

        return metrics
