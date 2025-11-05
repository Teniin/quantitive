"""
Demo script showcasing the portfolio simulator capabilities
"""

import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

from portfolio_simulator import (
    DataFetcher,
    Portfolio,
    Backtester,
    RiskMetrics,
    MonteCarloSimulator
)
from portfolio_simulator.backtester import BuyAndHoldStrategy, MovingAverageCrossoverStrategy


def demo_backtest_buy_and_hold():
    """Demo: Buy and hold strategy backtest"""
    print("\n" + "="*70)
    print("DEMO 1: BUY AND HOLD STRATEGY BACKTEST")
    print("="*70)

    # Define portfolio
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    weights = {
        'AAPL': 0.25,
        'MSFT': 0.25,
        'GOOGL': 0.25,
        'AMZN': 0.25
    }

    # Create strategy
    strategy = BuyAndHoldStrategy(symbols, weights)

    # Create backtester
    backtester = Backtester(
        strategy=strategy,
        initial_capital=100000,
        commission=0.001  # 0.1% commission
    )

    # Run backtest
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365*2)).strftime('%Y-%m-%d')

    results = backtester.run(
        symbols=symbols,
        start_date=start_date,
        end_date=end_date
    )

    # Print summary
    backtester.print_summary()

    # Plot results
    backtester.plot_results()

    return backtester


def demo_backtest_ma_crossover():
    """Demo: Moving average crossover strategy"""
    print("\n" + "="*70)
    print("DEMO 2: MOVING AVERAGE CROSSOVER STRATEGY")
    print("="*70)

    # Define portfolio
    symbols = ['SPY']  # S&P 500 ETF

    # Create strategy
    strategy = MovingAverageCrossoverStrategy(
        symbols=symbols,
        short_window=50,
        long_window=200
    )

    # Create backtester
    backtester = Backtester(
        strategy=strategy,
        initial_capital=100000,
        commission=0.001
    )

    # Run backtest
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365*3)).strftime('%Y-%m-%d')

    results = backtester.run(
        symbols=symbols,
        start_date=start_date,
        end_date=end_date
    )

    # Print summary
    backtester.print_summary()

    # Plot results
    backtester.plot_results()

    return backtester


def demo_monte_carlo():
    """Demo: Monte Carlo simulation"""
    print("\n" + "="*70)
    print("DEMO 3: MONTE CARLO SIMULATION")
    print("="*70)

    # Create simulator
    simulator = MonteCarloSimulator(random_seed=42)

    # Simulation parameters
    initial_value = 100000
    expected_return = 0.08  # 8% expected annual return
    volatility = 0.15  # 15% annual volatility
    time_horizon = 252  # 1 year of trading days
    n_simulations = 1000

    print(f"\nRunning {n_simulations} simulations...")
    print(f"Initial Value: ${initial_value:,}")
    print(f"Expected Annual Return: {expected_return*100}%")
    print(f"Annual Volatility: {volatility*100}%")
    print(f"Time Horizon: {time_horizon} days")

    # Run simulation
    simulations = simulator.simulate_portfolio(
        initial_value=initial_value,
        expected_return=expected_return,
        volatility=volatility,
        time_horizon=time_horizon,
        n_simulations=n_simulations
    )

    # Print statistics
    simulator.print_summary()

    # Plot results
    simulator.plot_simulations(num_paths=100)
    simulator.plot_confidence_intervals()

    return simulator


def demo_historical_monte_carlo():
    """Demo: Monte Carlo simulation using historical returns"""
    print("\n" + "="*70)
    print("DEMO 4: HISTORICAL MONTE CARLO SIMULATION")
    print("="*70)

    # Fetch historical data
    data_fetcher = DataFetcher()
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365*5)).strftime('%Y-%m-%d')

    print(f"\nFetching historical data for SPY...")
    returns = data_fetcher.get_returns(
        symbols='SPY',
        start_date=start_date,
        end_date=end_date
    )

    # Create simulator
    simulator = MonteCarloSimulator(random_seed=42)

    # Run simulation using bootstrap method
    initial_value = 100000
    time_horizon = 252  # 1 year
    n_simulations = 1000

    print(f"\nRunning {n_simulations} bootstrap simulations...")
    print(f"Based on {len(returns)} days of historical returns")

    simulations = simulator.simulate_from_returns(
        initial_value=initial_value,
        historical_returns=returns['SPY'].values,
        time_horizon=time_horizon,
        n_simulations=n_simulations,
        method='bootstrap'
    )

    # Print statistics
    simulator.print_summary()

    # Plot results
    simulator.plot_simulations(num_paths=100)

    return simulator


def demo_risk_metrics():
    """Demo: Risk metrics calculation"""
    print("\n" + "="*70)
    print("DEMO 5: RISK METRICS ANALYSIS")
    print("="*70)

    # Fetch data
    data_fetcher = DataFetcher()
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365*2)).strftime('%Y-%m-%d')

    print(f"\nFetching data for AAPL and SPY (benchmark)...")

    # Get returns
    portfolio_returns = data_fetcher.get_returns('AAPL', start_date, end_date)
    benchmark_returns = data_fetcher.get_returns('SPY', start_date, end_date)

    # Calculate metrics
    print("\nCalculating comprehensive risk metrics...")
    metrics = RiskMetrics.calculate_all_metrics(
        returns=portfolio_returns['AAPL'],
        benchmark_returns=benchmark_returns['SPY'],
        risk_free_rate=0.04
    )

    # Print metrics
    print("\n" + "-"*70)
    print("RISK METRICS FOR AAPL")
    print("-"*70)
    print(f"Total Return:           {metrics['total_return_pct']:.2f}%")
    print(f"Annualized Return:      {metrics['annualized_return_pct']:.2f}%")
    print(f"Annualized Volatility:  {metrics['volatility_pct']:.2f}%")
    print(f"Sharpe Ratio:           {metrics['sharpe_ratio']:.3f}")
    print(f"Sortino Ratio:          {metrics['sortino_ratio']:.3f}")
    print(f"Calmar Ratio:           {metrics['calmar_ratio']:.3f}")
    print(f"Max Drawdown:           {metrics['max_drawdown_pct']:.2f}%")
    print(f"Value at Risk (95%):    {metrics['var_95']:.4f}")
    print(f"CVaR (95%):             {metrics['cvar_95']:.4f}")
    print(f"Beta (vs SPY):          {metrics['beta']:.3f}")
    print(f"Alpha (annualized):     {metrics['alpha']:.4f}")
    print(f"Information Ratio:      {metrics['information_ratio']:.3f}")
    print("-"*70)

    # Plot cumulative returns comparison
    fig, ax = plt.subplots(figsize=(12, 6))

    portfolio_cumulative = (1 + portfolio_returns['AAPL']).cumprod()
    benchmark_cumulative = (1 + benchmark_returns['SPY']).cumprod()

    ax.plot(portfolio_cumulative.index, portfolio_cumulative, label='AAPL', linewidth=2)
    ax.plot(benchmark_cumulative.index, benchmark_cumulative, label='SPY (Benchmark)', linewidth=2)
    ax.set_title('Cumulative Returns: AAPL vs SPY', fontsize=14, fontweight='bold')
    ax.set_ylabel('Cumulative Return')
    ax.set_xlabel('Date')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def demo_portfolio_management():
    """Demo: Portfolio management"""
    print("\n" + "="*70)
    print("DEMO 6: PORTFOLIO MANAGEMENT")
    print("="*70)

    # Create portfolio
    portfolio = Portfolio(initial_capital=100000, name="Tech Portfolio")

    print(f"\nInitial Capital: ${portfolio.initial_capital:,}")

    # Simulate some trades
    print("\nExecuting trades...")

    current_prices = {
        'AAPL': 180.0,
        'MSFT': 380.0,
        'GOOGL': 140.0,
        'AMZN': 170.0
    }

    # Buy stocks
    portfolio.buy('AAPL', 100, 180.0)
    print("  ✓ Bought 100 shares of AAPL at $180")

    portfolio.buy('MSFT', 50, 380.0)
    print("  ✓ Bought 50 shares of MSFT at $380")

    portfolio.buy('GOOGL', 75, 140.0)
    print("  ✓ Bought 75 shares of GOOGL at $140")

    portfolio.buy('AMZN', 60, 170.0)
    print("  ✓ Bought 60 shares of AMZN at $170")

    # Get portfolio summary
    summary = portfolio.summary(current_prices)

    print("\n" + "-"*70)
    print("PORTFOLIO SUMMARY")
    print("-"*70)
    print(f"Portfolio Value:  ${summary['portfolio_value']:,.2f}")
    print(f"Cash:             ${summary['cash']:,.2f}")
    print(f"Total Return:     {summary['total_return_pct']}")

    print("\nHoldings:")
    for symbol, quantity in summary['holdings'].items():
        value = quantity * current_prices[symbol]
        print(f"  {symbol:6s} {quantity:4d} shares @ ${current_prices[symbol]:6.2f} = ${value:10,.2f}")

    print("\nAllocation:")
    for symbol, pct in summary['allocation'].items():
        print(f"  {symbol:6s} {pct:6.2f}%")

    print("-"*70)


def main():
    """Run all demos"""
    print("\n" + "="*70)
    print("PORTFOLIO SIMULATOR - COMPREHENSIVE DEMO")
    print("="*70)
    print("\nThis demo will showcase all features of the portfolio simulator:")
    print("1. Buy and Hold Strategy Backtest")
    print("2. Moving Average Crossover Strategy")
    print("3. Monte Carlo Simulation")
    print("4. Historical Monte Carlo Simulation")
    print("5. Risk Metrics Analysis")
    print("6. Portfolio Management")
    print("\n" + "="*70)

    input("\nPress Enter to start Demo 1 (Buy and Hold Backtest)...")
    demo_backtest_buy_and_hold()

    input("\nPress Enter to start Demo 2 (MA Crossover Strategy)...")
    demo_backtest_ma_crossover()

    input("\nPress Enter to start Demo 3 (Monte Carlo Simulation)...")
    demo_monte_carlo()

    input("\nPress Enter to start Demo 4 (Historical Monte Carlo)...")
    demo_historical_monte_carlo()

    input("\nPress Enter to start Demo 5 (Risk Metrics)...")
    demo_risk_metrics()

    input("\nPress Enter to start Demo 6 (Portfolio Management)...")
    demo_portfolio_management()

    print("\n" + "="*70)
    print("DEMO COMPLETE!")
    print("="*70)
    print("\nTo run the Streamlit dashboard, execute:")
    print("  streamlit run dashboard.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Run individual demos or all at once
    import sys

    if len(sys.argv) > 1:
        demo_name = sys.argv[1]
        if demo_name == "backtest":
            demo_backtest_buy_and_hold()
        elif demo_name == "ma":
            demo_backtest_ma_crossover()
        elif demo_name == "monte_carlo":
            demo_monte_carlo()
        elif demo_name == "historical_mc":
            demo_historical_monte_carlo()
        elif demo_name == "risk":
            demo_risk_metrics()
        elif demo_name == "portfolio":
            demo_portfolio_management()
        else:
            print(f"Unknown demo: {demo_name}")
            print("Available demos: backtest, ma, monte_carlo, historical_mc, risk, portfolio")
    else:
        # Run all demos
        main()
