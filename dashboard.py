"""
Streamlit Dashboard for Portfolio Simulator
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from portfolio_simulator import (
    DataFetcher,
    Portfolio,
    Backtester,
    RiskMetrics,
    MonteCarloSimulator
)
from portfolio_simulator.backtester import BuyAndHoldStrategy, MovingAverageCrossoverStrategy


# Page configuration
st.set_page_config(
    page_title="Portfolio Simulator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main dashboard function"""
    st.markdown('<h1 class="main-header">📈 Portfolio Simulator Dashboard</h1>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Home", "Backtesting", "Monte Carlo Simulation", "Risk Analysis", "Portfolio Manager"]
    )

    if page == "Home":
        show_home()
    elif page == "Backtesting":
        show_backtesting()
    elif page == "Monte Carlo Simulation":
        show_monte_carlo()
    elif page == "Risk Analysis":
        show_risk_analysis()
    elif page == "Portfolio Manager":
        show_portfolio_manager()


def show_home():
    """Show home page"""
    st.header("Welcome to the Portfolio Simulator!")

    st.markdown("""
    This comprehensive portfolio simulator provides tools for:

    - **Backtesting**: Test trading strategies on historical data
    - **Monte Carlo Simulation**: Project future portfolio performance
    - **Risk Analysis**: Calculate comprehensive risk metrics
    - **Portfolio Management**: Track and manage portfolio holdings

    ### Features

    ✅ Multiple trading strategies (Buy & Hold, MA Crossover, and more)
    ✅ Comprehensive risk metrics (Sharpe, Sortino, Max Drawdown, VaR, etc.)
    ✅ Monte Carlo simulations for forecasting
    ✅ Interactive visualizations
    ✅ Real-time market data via yfinance

    ### Getting Started

    Select a page from the sidebar to begin:

    1. **Backtesting** - Test your trading strategies
    2. **Monte Carlo** - Run probabilistic simulations
    3. **Risk Analysis** - Analyze portfolio risk
    4. **Portfolio Manager** - Manage your portfolio

    ---
    """)

    # Quick stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Strategies Available", "2+")
    with col2:
        st.metric("Risk Metrics", "15+")
    with col3:
        st.metric("Data Source", "yfinance")
    with col4:
        st.metric("Simulation Types", "3")


def show_backtesting():
    """Show backtesting page"""
    st.header("📊 Strategy Backtesting")

    # Strategy selection
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Strategy Configuration")

        strategy_type = st.selectbox(
            "Select Strategy",
            ["Buy and Hold", "Moving Average Crossover"]
        )

        # Symbol input
        symbols_input = st.text_input(
            "Stock Symbols (comma-separated)",
            "AAPL,MSFT,GOOGL,AMZN"
        )
        symbols = [s.strip().upper() for s in symbols_input.split(',')]

        # Date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)  # 2 years

        start_date_input = st.date_input("Start Date", start_date)
        end_date_input = st.date_input("End Date", end_date)

        # Initial capital
        initial_capital = st.number_input(
            "Initial Capital ($)",
            min_value=1000,
            max_value=10000000,
            value=100000,
            step=10000
        )

        # Commission
        commission = st.number_input(
            "Commission (%)",
            min_value=0.0,
            max_value=5.0,
            value=0.1,
            step=0.1
        ) / 100

        # Strategy-specific parameters
        if strategy_type == "Moving Average Crossover":
            short_window = st.number_input("Short MA Window", 10, 100, 50)
            long_window = st.number_input("Long MA Window", 100, 300, 200)

        run_backtest = st.button("Run Backtest", type="primary")

    with col2:
        st.subheader("Backtest Results")

        if run_backtest:
            with st.spinner("Running backtest..."):
                try:
                    # Create strategy
                    if strategy_type == "Buy and Hold":
                        weights = {symbol: 1.0 / len(symbols) for symbol in symbols}
                        strategy = BuyAndHoldStrategy(symbols, weights)
                    else:
                        strategy = MovingAverageCrossoverStrategy(
                            symbols,
                            short_window=short_window,
                            long_window=long_window
                        )

                    # Create backtester
                    backtester = Backtester(
                        strategy=strategy,
                        initial_capital=initial_capital,
                        commission=commission
                    )

                    # Run backtest
                    results = backtester.run(
                        symbols=symbols,
                        start_date=start_date_input.strftime('%Y-%m-%d'),
                        end_date=end_date_input.strftime('%Y-%m-%d')
                    )

                    # Display results
                    st.success("Backtest completed!")

                    # Performance metrics
                    st.subheader("Performance Summary")

                    metric_col1, metric_col2, metric_col3 = st.columns(3)

                    with metric_col1:
                        st.metric(
                            "Total Return",
                            f"{results['total_return_pct']:.2f}%",
                            delta=f"${results['final_value'] - initial_capital:,.2f}"
                        )

                    with metric_col2:
                        st.metric(
                            "Sharpe Ratio",
                            f"{results['metrics']['sharpe_ratio']:.3f}"
                        )

                    with metric_col3:
                        st.metric(
                            "Max Drawdown",
                            f"{results['metrics']['max_drawdown_pct']:.2f}%"
                        )

                    # Portfolio value chart
                    st.subheader("Portfolio Value Over Time")

                    portfolio_history = results['portfolio_history']

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=portfolio_history.index,
                        y=portfolio_history['portfolio_value'],
                        mode='lines',
                        name='Portfolio Value',
                        line=dict(color='#1f77b4', width=2)
                    ))
                    fig.add_hline(
                        y=initial_capital,
                        line_dash="dash",
                        line_color="red",
                        annotation_text="Initial Capital"
                    )
                    fig.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Portfolio Value ($)",
                        hovermode='x unified',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Cumulative returns comparison
                    st.subheader("Cumulative Returns vs Benchmark")

                    portfolio_returns = results['portfolio_returns']
                    benchmark_returns = results['benchmark_returns']

                    portfolio_cumulative = (1 + portfolio_returns).cumprod()
                    benchmark_cumulative = (1 + benchmark_returns).cumprod()

                    fig2 = go.Figure()
                    fig2.add_trace(go.Scatter(
                        x=portfolio_cumulative.index,
                        y=portfolio_cumulative,
                        mode='lines',
                        name='Strategy',
                        line=dict(color='green', width=2)
                    ))
                    fig2.add_trace(go.Scatter(
                        x=benchmark_cumulative.index,
                        y=benchmark_cumulative,
                        mode='lines',
                        name='Benchmark',
                        line=dict(color='orange', width=2)
                    ))
                    fig2.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Cumulative Return",
                        hovermode='x unified',
                        height=400
                    )
                    st.plotly_chart(fig2, use_container_width=True)

                    # Detailed metrics
                    st.subheader("Detailed Metrics")

                    metrics_df = pd.DataFrame({
                        'Metric': [
                            'Annualized Return',
                            'Annualized Volatility',
                            'Sharpe Ratio',
                            'Sortino Ratio',
                            'Calmar Ratio',
                            'Max Drawdown',
                            'VaR (95%)',
                            'CVaR (95%)',
                            'Beta',
                            'Alpha'
                        ],
                        'Value': [
                            f"{results['metrics']['annualized_return_pct']:.2f}%",
                            f"{results['metrics']['volatility_pct']:.2f}%",
                            f"{results['metrics']['sharpe_ratio']:.3f}",
                            f"{results['metrics']['sortino_ratio']:.3f}",
                            f"{results['metrics']['calmar_ratio']:.3f}",
                            f"{results['metrics']['max_drawdown_pct']:.2f}%",
                            f"{results['metrics']['var_95']:.4f}",
                            f"{results['metrics']['cvar_95']:.4f}",
                            f"{results['metrics'].get('beta', 0):.3f}",
                            f"{results['metrics'].get('alpha', 0):.4f}"
                        ]
                    })

                    st.dataframe(metrics_df, use_container_width=True, hide_index=True)

                    # Transaction history
                    if not results['transactions'].empty:
                        st.subheader("Transaction History")
                        st.dataframe(results['transactions'], use_container_width=True)

                except Exception as e:
                    st.error(f"Error running backtest: {str(e)}")


def show_monte_carlo():
    """Show Monte Carlo simulation page"""
    st.header("🎲 Monte Carlo Simulation")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Simulation Parameters")

        simulation_type = st.selectbox(
            "Simulation Type",
            ["Parametric (Normal Distribution)", "Historical Bootstrap"]
        )

        initial_value = st.number_input(
            "Initial Portfolio Value ($)",
            min_value=1000,
            max_value=10000000,
            value=100000,
            step=10000
        )

        if simulation_type == "Parametric (Normal Distribution)":
            expected_return = st.slider(
                "Expected Annual Return (%)",
                -20.0, 50.0, 8.0, 0.5
            ) / 100

            volatility = st.slider(
                "Annual Volatility (%)",
                1.0, 50.0, 15.0, 0.5
            ) / 100
        else:
            symbol = st.text_input("Stock Symbol for Historical Data", "SPY")
            lookback_years = st.slider("Historical Lookback (years)", 1, 10, 5)

        time_horizon = st.number_input(
            "Time Horizon (days)",
            min_value=30,
            max_value=2520,
            value=252,
            step=30
        )

        n_simulations = st.slider(
            "Number of Simulations",
            100, 10000, 1000, 100
        )

        run_simulation = st.button("Run Simulation", type="primary")

    with col2:
        st.subheader("Simulation Results")

        if run_simulation:
            with st.spinner("Running Monte Carlo simulation..."):
                try:
                    simulator = MonteCarloSimulator(random_seed=42)

                    if simulation_type == "Parametric (Normal Distribution)":
                        simulations = simulator.simulate_portfolio(
                            initial_value=initial_value,
                            expected_return=expected_return,
                            volatility=volatility,
                            time_horizon=time_horizon,
                            n_simulations=n_simulations
                        )
                    else:
                        # Fetch historical data
                        data_fetcher = DataFetcher()
                        end_date = datetime.now().strftime('%Y-%m-%d')
                        start_date = (datetime.now() - timedelta(days=365*lookback_years)).strftime('%Y-%m-%d')

                        returns = data_fetcher.get_returns(symbol, start_date, end_date)

                        simulations = simulator.simulate_from_returns(
                            initial_value=initial_value,
                            historical_returns=returns[symbol].values,
                            time_horizon=time_horizon,
                            n_simulations=n_simulations,
                            method='bootstrap'
                        )

                    # Calculate statistics
                    stats = simulator.calculate_statistics()

                    st.success("Simulation completed!")

                    # Display key statistics
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

                    with metric_col1:
                        st.metric(
                            "Mean Final Value",
                            f"${stats['mean_final_value']:,.0f}"
                        )

                    with metric_col2:
                        st.metric(
                            "Median Final Value",
                            f"${stats['median_final_value']:,.0f}"
                        )

                    with metric_col3:
                        st.metric(
                            "Prob. of Profit",
                            f"{stats['prob_profit']:.1f}%"
                        )

                    with metric_col4:
                        st.metric(
                            "Max Final Value",
                            f"${stats['max_final_value']:,.0f}"
                        )

                    # Plot simulation paths
                    st.subheader("Simulation Paths")

                    # Sample paths for visualization
                    sample_size = min(100, n_simulations)
                    sample_indices = np.random.choice(n_simulations, sample_size, replace=False)

                    fig = go.Figure()

                    # Add sample paths
                    for idx in sample_indices:
                        fig.add_trace(go.Scatter(
                            x=list(range(time_horizon + 1)),
                            y=simulations[idx, :],
                            mode='lines',
                            line=dict(color='lightgray', width=0.5),
                            showlegend=False,
                            hoverinfo='skip'
                        ))

                    # Add percentile paths
                    percentiles = [5, 50, 95]
                    colors = ['red', 'green', 'blue']

                    for p, color in zip(percentiles, colors):
                        percentile_path = np.percentile(simulations, p, axis=0)
                        fig.add_trace(go.Scatter(
                            x=list(range(time_horizon + 1)),
                            y=percentile_path,
                            mode='lines',
                            name=f'{p}th Percentile',
                            line=dict(color=color, width=3)
                        ))

                    fig.update_layout(
                        xaxis_title="Time Period (days)",
                        yaxis_title="Portfolio Value ($)",
                        hovermode='x unified',
                        height=500
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    # Distribution of final values
                    st.subheader("Distribution of Final Portfolio Values")

                    final_values = simulations[:, -1]

                    fig2 = go.Figure()
                    fig2.add_trace(go.Histogram(
                        x=final_values,
                        nbinsx=50,
                        name='Final Values',
                        marker_color='#1f77b4'
                    ))
                    fig2.add_vline(
                        x=stats['mean_final_value'],
                        line_dash="dash",
                        line_color="red",
                        annotation_text=f"Mean: ${stats['mean_final_value']:,.0f}"
                    )
                    fig2.update_layout(
                        xaxis_title="Final Portfolio Value ($)",
                        yaxis_title="Frequency",
                        height=400
                    )

                    st.plotly_chart(fig2, use_container_width=True)

                    # Percentile table
                    st.subheader("Percentile Analysis")

                    percentile_df = pd.DataFrame({
                        'Percentile': ['5th', '25th', '50th', '75th', '95th'],
                        'Final Value': [
                            f"${stats['percentiles']['p5']:,.2f}",
                            f"${stats['percentiles']['p25']:,.2f}",
                            f"${stats['percentiles']['p50']:,.2f}",
                            f"${stats['percentiles']['p75']:,.2f}",
                            f"${stats['percentiles']['p95']:,.2f}"
                        ]
                    })

                    st.dataframe(percentile_df, use_container_width=True, hide_index=True)

                except Exception as e:
                    st.error(f"Error running simulation: {str(e)}")


def show_risk_analysis():
    """Show risk analysis page"""
    st.header("⚠️ Risk Analysis")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Analysis Configuration")

        symbol = st.text_input("Stock Symbol", "AAPL")
        benchmark = st.text_input("Benchmark Symbol", "SPY")

        # Date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)

        start_date_input = st.date_input("Start Date", start_date, key="risk_start")
        end_date_input = st.date_input("End Date", end_date, key="risk_end")

        risk_free_rate = st.slider(
            "Risk-Free Rate (%)",
            0.0, 10.0, 4.0, 0.1
        ) / 100

        analyze = st.button("Analyze Risk", type="primary")

    with col2:
        st.subheader("Risk Metrics")

        if analyze:
            with st.spinner("Calculating risk metrics..."):
                try:
                    data_fetcher = DataFetcher()

                    # Fetch returns
                    portfolio_returns = data_fetcher.get_returns(
                        symbol,
                        start_date_input.strftime('%Y-%m-%d'),
                        end_date_input.strftime('%Y-%m-%d')
                    )

                    benchmark_returns = data_fetcher.get_returns(
                        benchmark,
                        start_date_input.strftime('%Y-%m-%d'),
                        end_date_input.strftime('%Y-%m-%d')
                    )

                    # Calculate metrics
                    metrics = RiskMetrics.calculate_all_metrics(
                        returns=portfolio_returns[symbol],
                        benchmark_returns=benchmark_returns[benchmark],
                        risk_free_rate=risk_free_rate
                    )

                    st.success("Analysis completed!")

                    # Display metrics in cards
                    st.subheader(f"Risk Metrics for {symbol}")

                    # Row 1
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("Total Return", f"{metrics['total_return_pct']:.2f}%")
                    with metric_col2:
                        st.metric("Annualized Return", f"{metrics['annualized_return_pct']:.2f}%")
                    with metric_col3:
                        st.metric("Volatility", f"{metrics['volatility_pct']:.2f}%")

                    # Row 2
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.3f}")
                    with metric_col2:
                        st.metric("Sortino Ratio", f"{metrics['sortino_ratio']:.3f}")
                    with metric_col3:
                        st.metric("Max Drawdown", f"{metrics['max_drawdown_pct']:.2f}%")

                    # Row 3
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("Beta", f"{metrics['beta']:.3f}")
                    with metric_col2:
                        st.metric("Alpha", f"{metrics['alpha']:.4f}")
                    with metric_col3:
                        st.metric("VaR (95%)", f"{metrics['var_95']:.4f}")

                    # Cumulative returns chart
                    st.subheader("Cumulative Returns Comparison")

                    portfolio_cumulative = (1 + portfolio_returns[symbol]).cumprod()
                    benchmark_cumulative = (1 + benchmark_returns[benchmark]).cumprod()

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=portfolio_cumulative.index,
                        y=portfolio_cumulative,
                        mode='lines',
                        name=symbol,
                        line=dict(color='blue', width=2)
                    ))
                    fig.add_trace(go.Scatter(
                        x=benchmark_cumulative.index,
                        y=benchmark_cumulative,
                        mode='lines',
                        name=benchmark,
                        line=dict(color='orange', width=2)
                    ))
                    fig.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Cumulative Return",
                        hovermode='x unified',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Complete metrics table
                    st.subheader("Complete Risk Metrics")

                    metrics_df = pd.DataFrame({
                        'Metric': list(metrics.keys()),
                        'Value': [str(v) for v in metrics.values()]
                    })

                    st.dataframe(metrics_df, use_container_width=True, hide_index=True)

                except Exception as e:
                    st.error(f"Error analyzing risk: {str(e)}")


def show_portfolio_manager():
    """Show portfolio manager page"""
    st.header("💼 Portfolio Manager")

    st.markdown("""
    Manage your portfolio holdings and track performance.
    """)

    # Initialize session state
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = Portfolio(100000, "My Portfolio")

    portfolio = st.session_state.portfolio

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Add Transaction")

        transaction_type = st.selectbox("Transaction Type", ["Buy", "Sell"])
        symbol = st.text_input("Symbol", "AAPL", key="pm_symbol")
        quantity = st.number_input("Quantity", min_value=1, value=100)
        price = st.number_input("Price ($)", min_value=0.01, value=100.0, step=0.01)

        if st.button("Execute Transaction", type="primary"):
            if transaction_type == "Buy":
                success = portfolio.buy(symbol, quantity, price, datetime.now())
                if success:
                    st.success(f"Bought {quantity} shares of {symbol} at ${price}")
                else:
                    st.error("Insufficient cash for this transaction")
            else:
                success = portfolio.sell(symbol, quantity, price, datetime.now())
                if success:
                    st.success(f"Sold {quantity} shares of {symbol} at ${price}")
                else:
                    st.error("Insufficient shares for this transaction")

        if st.button("Reset Portfolio"):
            portfolio.reset()
            st.session_state.portfolio = portfolio
            st.success("Portfolio reset!")

    with col2:
        st.subheader("Portfolio Summary")

        # Get current prices for holdings
        if portfolio.holdings:
            try:
                data_fetcher = DataFetcher()
                current_prices = {}
                for sym in portfolio.holdings.keys():
                    try:
                        current_prices[sym] = data_fetcher.get_latest_price(sym)
                    except:
                        current_prices[sym] = 0.0

                summary = portfolio.summary(current_prices)

                # Display summary metrics
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                with metric_col1:
                    st.metric("Portfolio Value", f"${summary['portfolio_value']:,.2f}")
                with metric_col2:
                    st.metric("Cash", f"${summary['cash']:,.2f}")
                with metric_col3:
                    st.metric("Total Return", summary['total_return_pct'])

                # Holdings table
                if summary['holdings']:
                    st.subheader("Holdings")

                    holdings_data = []
                    for sym, qty in summary['holdings'].items():
                        value = qty * current_prices.get(sym, 0)
                        holdings_data.append({
                            'Symbol': sym,
                            'Quantity': qty,
                            'Price': f"${current_prices.get(sym, 0):.2f}",
                            'Value': f"${value:,.2f}",
                            'Allocation': f"{summary['allocation'].get(sym, 0):.2f}%"
                        })

                    holdings_df = pd.DataFrame(holdings_data)
                    st.dataframe(holdings_df, use_container_width=True, hide_index=True)

                    # Allocation pie chart
                    st.subheader("Portfolio Allocation")

                    fig = go.Figure(data=[go.Pie(
                        labels=list(summary['allocation'].keys()),
                        values=list(summary['allocation'].values()),
                        hole=.3
                    )])
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Error fetching current prices: {str(e)}")
        else:
            st.info("No holdings in portfolio. Add transactions to get started.")

        # Transaction history
        transactions = portfolio.get_transaction_history_df()
        if not transactions.empty:
            st.subheader("Transaction History")
            st.dataframe(transactions, use_container_width=True)


if __name__ == "__main__":
    main()
