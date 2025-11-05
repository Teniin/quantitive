"""
Streamlit Dashboard for Portfolio Simulator - Modern Vercel-Inspired Design
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

# Modern Vercel-inspired CSS
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0a0a0a 50%, #000000 100%);
        color: #ffffff;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0a 0%, #000000 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Main header with gradient text */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #888888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: -0.02em;
        animation: fadeIn 0.8s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Section headers */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700;
        letter-spacing: -0.01em;
    }

    /* Modern card design with glassmorphism */
    .modern-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }

    .modern-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.5);
    }

    /* Feature cards on home page */
    .feature-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, transparent 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }

    .feature-card:hover::before {
        opacity: 1;
    }

    .feature-card:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%);
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.3));
    }

    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }

    .feature-description {
        color: #a0a0a0;
        line-height: 1.6;
    }

    /* Metric cards */
    .stMetric {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }

    .stMetric:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }

    .stMetric label {
        color: #a0a0a0 !important;
        font-size: 0.875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
        color: #000000;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(255, 255, 255, 0.2);
        letter-spacing: 0.02em;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #f0f0f0 0%, #ffffff 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
    }

    .stButton > button:active {
        transform: translateY(0px);
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }

    /* Labels */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stSlider label {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Slider */
    .stSlider > div > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
    }

    .stSlider [role="slider"] {
        background: #ffffff !important;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3) !important;
    }

    /* Date input */
    .stDateInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }

    /* Radio buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stRadio label {
        color: #ffffff !important;
    }

    /* Success/Error messages */
    .stSuccess {
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 8px !important;
        color: #22c55e !important;
    }

    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 8px !important;
        color: #ef4444 !important;
    }

    .stInfo {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 8px !important;
        color: #3b82f6 !important;
    }

    /* Dataframe styling */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    .stDataFrame [data-testid="stDataFrameResizable"] {
        background: transparent !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #a0a0a0;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff !important;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #ffffff !important;
    }

    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 4rem 2rem;
        margin-bottom: 3rem;
        position: relative;
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 0%, #a0a0a0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        color: #a0a0a0;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Grid layout for features */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }

    /* Gradient accent line */
    .gradient-line {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.3) 50%, transparent 100%);
        margin: 2rem 0;
    }

    /* Chart container */
    .js-plotly-plot {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }

    /* Pulse animation for accents */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
</style>
""", unsafe_allow_html=True)

# Dark theme for Plotly charts
PLOTLY_TEMPLATE = {
    'layout': {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(255,255,255,0.02)',
        'font': {'color': '#ffffff', 'family': 'Inter'},
        'xaxis': {
            'gridcolor': 'rgba(255,255,255,0.1)',
            'zerolinecolor': 'rgba(255,255,255,0.1)',
            'color': '#a0a0a0'
        },
        'yaxis': {
            'gridcolor': 'rgba(255,255,255,0.1)',
            'zerolinecolor': 'rgba(255,255,255,0.1)',
            'color': '#a0a0a0'
        },
        'hovermode': 'x unified',
        'hoverlabel': {
            'bgcolor': 'rgba(0,0,0,0.8)',
            'bordercolor': 'rgba(255,255,255,0.2)',
            'font': {'color': '#ffffff'}
        }
    }
}


def main():
    """Main dashboard function"""
    st.markdown('<div class="hero-section"><h1 class="hero-title">Portfolio Simulator</h1><p class="hero-subtitle">Advanced quantitative analysis and backtesting platform</p></div>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown("### Navigation")
    st.sidebar.markdown('<div class="gradient-line"></div>', unsafe_allow_html=True)

    page = st.sidebar.radio(
        "",
        ["🏠 Home", "📊 Backtesting", "🎲 Monte Carlo", "⚠️ Risk Analysis", "💼 Portfolio"],
        label_visibility="collapsed"
    )

    if "Home" in page:
        show_home()
    elif "Backtesting" in page:
        show_backtesting()
    elif "Monte Carlo" in page:
        show_monte_carlo()
    elif "Risk" in page:
        show_risk_analysis()
    elif "Portfolio" in page:
        show_portfolio_manager()


def show_home():
    """Show home page"""

    # Feature cards
    st.markdown('<div class="gradient-line"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Strategy Backtesting</div>
            <div class="feature-description">
                Test trading strategies on historical data with comprehensive performance metrics.
                Support for multiple strategies including Buy & Hold and Moving Average Crossover.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚠️</div>
            <div class="feature-title">Risk Analysis</div>
            <div class="feature-description">
                Calculate 15+ risk metrics including Sharpe Ratio, Sortino Ratio, VaR, CVaR,
                Maximum Drawdown, and more. Compare against benchmarks.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎲</div>
            <div class="feature-title">Monte Carlo Simulation</div>
            <div class="feature-description">
                Run thousands of probabilistic simulations to forecast portfolio performance.
                Parametric and bootstrap methods with confidence intervals.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💼</div>
            <div class="feature-title">Portfolio Management</div>
            <div class="feature-description">
                Track holdings, execute trades, and monitor real-time performance.
                Visualize allocation and transaction history.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-line"></div>', unsafe_allow_html=True)

    # Quick stats
    st.markdown("### Platform Statistics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Strategies", "2+", help="Trading strategies available")
    with col2:
        st.metric("Risk Metrics", "15+", help="Comprehensive risk analysis")
    with col3:
        st.metric("Data Source", "yfinance", help="Real-time market data")
    with col4:
        st.metric("Simulations", "10K+", help="Monte Carlo capabilities")


def show_backtesting():
    """Show backtesting page"""
    st.markdown("## Strategy Backtesting")
    st.markdown("Test your trading strategies on historical market data")
    st.markdown('<div class="gradient-line"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Configuration")

        strategy_type = st.selectbox(
            "Strategy",
            ["Buy and Hold", "Moving Average Crossover"]
        )

        symbols_input = st.text_input(
            "Symbols",
            "AAPL,MSFT,GOOGL,AMZN",
            help="Comma-separated ticker symbols"
        )
        symbols = [s.strip().upper() for s in symbols_input.split(',')]

        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)

        start_date_input = st.date_input("Start Date", start_date)
        end_date_input = st.date_input("End Date", end_date)

        initial_capital = st.number_input(
            "Initial Capital ($)",
            min_value=1000,
            max_value=10000000,
            value=100000,
            step=10000
        )

        commission = st.number_input(
            "Commission (%)",
            min_value=0.0,
            max_value=5.0,
            value=0.1,
            step=0.1
        ) / 100

        if strategy_type == "Moving Average Crossover":
            short_window = st.number_input("Short MA", 10, 100, 50)
            long_window = st.number_input("Long MA", 100, 300, 200)

        run_backtest = st.button("▶ Run Backtest", type="primary")

    with col2:
        st.markdown("### Results")

        if run_backtest:
            with st.spinner("Running backtest..."):
                try:
                    if strategy_type == "Buy and Hold":
                        weights = {symbol: 1.0 / len(symbols) for symbol in symbols}
                        strategy = BuyAndHoldStrategy(symbols, weights)
                    else:
                        strategy = MovingAverageCrossoverStrategy(
                            symbols,
                            short_window=short_window,
                            long_window=long_window
                        )

                    backtester = Backtester(
                        strategy=strategy,
                        initial_capital=initial_capital,
                        commission=commission
                    )

                    results = backtester.run(
                        symbols=symbols,
                        start_date=start_date_input.strftime('%Y-%m-%d'),
                        end_date=end_date_input.strftime('%Y-%m-%d')
                    )

                    st.success("✓ Backtest completed successfully")

                    # Performance metrics
                    metric_col1, metric_col2, metric_col3 = st.columns(3)

                    with metric_col1:
                        st.metric(
                            "Total Return",
                            f"{results['total_return_pct']:.2f}%",
                            delta=f"${results['final_value'] - initial_capital:,.0f}"
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
                    st.markdown("#### Portfolio Value")

                    portfolio_history = results['portfolio_history']

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=portfolio_history.index,
                        y=portfolio_history['portfolio_value'],
                        mode='lines',
                        name='Portfolio',
                        line=dict(color='#22c55e', width=3),
                        fill='tozeroy',
                        fillcolor='rgba(34, 197, 94, 0.1)'
                    ))
                    fig.add_hline(
                        y=initial_capital,
                        line_dash="dash",
                        line_color="rgba(255,255,255,0.3)",
                        annotation_text="Initial"
                    )
                    fig.update_layout(**PLOTLY_TEMPLATE['layout'], height=400)
                    st.plotly_chart(fig, use_container_width=True)

                    # Cumulative returns comparison
                    st.markdown("#### Returns vs Benchmark")

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
                        line=dict(color='#22c55e', width=3)
                    ))
                    fig2.add_trace(go.Scatter(
                        x=benchmark_cumulative.index,
                        y=benchmark_cumulative,
                        mode='lines',
                        name='Benchmark',
                        line=dict(color='#ef4444', width=2, dash='dash')
                    ))
                    fig2.update_layout(**PLOTLY_TEMPLATE['layout'], height=400)
                    st.plotly_chart(fig2, use_container_width=True)

                    # Detailed metrics
                    st.markdown("#### Risk Metrics")

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

                except Exception as e:
                    st.error(f"Error: {str(e)}")


def show_monte_carlo():
    """Show Monte Carlo simulation page"""
    st.markdown("## Monte Carlo Simulation")
    st.markdown("Probabilistic portfolio forecasting with thousands of scenarios")
    st.markdown('<div class="gradient-line"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Parameters")

        simulation_type = st.selectbox(
            "Method",
            ["Parametric (Normal Distribution)", "Historical Bootstrap"]
        )

        initial_value = st.number_input(
            "Initial Value ($)",
            min_value=1000,
            max_value=10000000,
            value=100000,
            step=10000
        )

        if simulation_type == "Parametric (Normal Distribution)":
            expected_return = st.slider(
                "Expected Return (%)",
                -20.0, 50.0, 8.0, 0.5
            ) / 100

            volatility = st.slider(
                "Volatility (%)",
                1.0, 50.0, 15.0, 0.5
            ) / 100
        else:
            symbol = st.text_input("Symbol", "SPY")
            lookback_years = st.slider("Lookback (years)", 1, 10, 5)

        time_horizon = st.number_input(
            "Horizon (days)",
            min_value=30,
            max_value=2520,
            value=252,
            step=30
        )

        n_simulations = st.slider(
            "Simulations",
            100, 10000, 1000, 100
        )

        run_simulation = st.button("▶ Run Simulation", type="primary")

    with col2:
        st.markdown("### Results")

        if run_simulation:
            with st.spinner("Running simulation..."):
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

                    stats = simulator.calculate_statistics()

                    st.success("✓ Simulation completed successfully")

                    # Key statistics
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

                    with metric_col1:
                        st.metric("Mean", f"${stats['mean_final_value']:,.0f}")
                    with metric_col2:
                        st.metric("Median", f"${stats['median_final_value']:,.0f}")
                    with metric_col3:
                        st.metric("Profit Prob", f"{stats['prob_profit']:.1f}%")
                    with metric_col4:
                        st.metric("Max", f"${stats['max_final_value']:,.0f}")

                    # Simulation paths
                    st.markdown("#### Simulation Paths")

                    sample_size = min(100, n_simulations)
                    sample_indices = np.random.choice(n_simulations, sample_size, replace=False)

                    fig = go.Figure()

                    for idx in sample_indices:
                        fig.add_trace(go.Scatter(
                            x=list(range(time_horizon + 1)),
                            y=simulations[idx, :],
                            mode='lines',
                            line=dict(color='rgba(255,255,255,0.1)', width=0.5),
                            showlegend=False,
                            hoverinfo='skip'
                        ))

                    percentiles = [5, 50, 95]
                    colors = ['#ef4444', '#22c55e', '#3b82f6']

                    for p, color in zip(percentiles, colors):
                        percentile_path = np.percentile(simulations, p, axis=0)
                        fig.add_trace(go.Scatter(
                            x=list(range(time_horizon + 1)),
                            y=percentile_path,
                            mode='lines',
                            name=f'{p}th Percentile',
                            line=dict(color=color, width=3)
                        ))

                    fig.update_layout(**PLOTLY_TEMPLATE['layout'], height=500)
                    st.plotly_chart(fig, use_container_width=True)

                    # Distribution
                    st.markdown("#### Distribution")

                    final_values = simulations[:, -1]

                    fig2 = go.Figure()
                    fig2.add_trace(go.Histogram(
                        x=final_values,
                        nbinsx=50,
                        name='Distribution',
                        marker_color='#3b82f6',
                        opacity=0.7
                    ))
                    fig2.add_vline(
                        x=stats['mean_final_value'],
                        line_dash="dash",
                        line_color="#22c55e",
                        annotation_text="Mean"
                    )
                    fig2.update_layout(**PLOTLY_TEMPLATE['layout'], height=400)
                    st.plotly_chart(fig2, use_container_width=True)

                    # Percentiles
                    st.markdown("#### Percentile Analysis")

                    percentile_df = pd.DataFrame({
                        'Percentile': ['5th', '25th', '50th', '75th', '95th'],
                        'Value': [
                            f"${stats['percentiles']['p5']:,.2f}",
                            f"${stats['percentiles']['p25']:,.2f}",
                            f"${stats['percentiles']['p50']:,.2f}",
                            f"${stats['percentiles']['p75']:,.2f}",
                            f"${stats['percentiles']['p95']:,.2f}"
                        ]
                    })

                    st.dataframe(percentile_df, use_container_width=True, hide_index=True)

                except Exception as e:
                    st.error(f"Error: {str(e)}")


def show_risk_analysis():
    """Show risk analysis page"""
    st.markdown("## Risk Analysis")
    st.markdown("Comprehensive risk metrics and performance analysis")
    st.markdown('<div class="gradient-line"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Configuration")

        symbol = st.text_input("Symbol", "AAPL")
        benchmark = st.text_input("Benchmark", "SPY")

        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)

        start_date_input = st.date_input("Start Date", start_date, key="risk_start")
        end_date_input = st.date_input("End Date", end_date, key="risk_end")

        risk_free_rate = st.slider(
            "Risk-Free Rate (%)",
            0.0, 10.0, 4.0, 0.1
        ) / 100

        analyze = st.button("▶ Analyze", type="primary")

    with col2:
        st.markdown("### Results")

        if analyze:
            with st.spinner("Analyzing..."):
                try:
                    data_fetcher = DataFetcher()

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

                    metrics = RiskMetrics.calculate_all_metrics(
                        returns=portfolio_returns[symbol],
                        benchmark_returns=benchmark_returns[benchmark],
                        risk_free_rate=risk_free_rate
                    )

                    st.success("✓ Analysis completed")

                    # Display metrics
                    st.markdown(f"#### Metrics for {symbol}")

                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("Total Return", f"{metrics['total_return_pct']:.2f}%")
                    with metric_col2:
                        st.metric("Ann. Return", f"{metrics['annualized_return_pct']:.2f}%")
                    with metric_col3:
                        st.metric("Volatility", f"{metrics['volatility_pct']:.2f}%")

                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("Sharpe", f"{metrics['sharpe_ratio']:.3f}")
                    with metric_col2:
                        st.metric("Sortino", f"{metrics['sortino_ratio']:.3f}")
                    with metric_col3:
                        st.metric("Max DD", f"{metrics['max_drawdown_pct']:.2f}%")

                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("Beta", f"{metrics['beta']:.3f}")
                    with metric_col2:
                        st.metric("Alpha", f"{metrics['alpha']:.4f}")
                    with metric_col3:
                        st.metric("VaR (95%)", f"{metrics['var_95']:.4f}")

                    # Chart
                    st.markdown("#### Cumulative Returns")

                    portfolio_cumulative = (1 + portfolio_returns[symbol]).cumprod()
                    benchmark_cumulative = (1 + benchmark_returns[benchmark]).cumprod()

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=portfolio_cumulative.index,
                        y=portfolio_cumulative,
                        mode='lines',
                        name=symbol,
                        line=dict(color='#3b82f6', width=3)
                    ))
                    fig.add_trace(go.Scatter(
                        x=benchmark_cumulative.index,
                        y=benchmark_cumulative,
                        mode='lines',
                        name=benchmark,
                        line=dict(color='#ef4444', width=2, dash='dash')
                    ))
                    fig.update_layout(**PLOTLY_TEMPLATE['layout'], height=400)
                    st.plotly_chart(fig, use_container_width=True)

                except Exception as e:
                    st.error(f"Error: {str(e)}")


def show_portfolio_manager():
    """Show portfolio manager page"""
    st.markdown("## Portfolio Manager")
    st.markdown("Track holdings and manage your portfolio")
    st.markdown('<div class="gradient-line"></div>', unsafe_allow_html=True)

    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = Portfolio(100000, "My Portfolio")

    portfolio = st.session_state.portfolio

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Transaction")

        transaction_type = st.selectbox("Type", ["Buy", "Sell"])
        symbol = st.text_input("Symbol", "AAPL", key="pm_symbol")
        quantity = st.number_input("Quantity", min_value=1, value=100)
        price = st.number_input("Price ($)", min_value=0.01, value=100.0, step=0.01)

        if st.button("▶ Execute", type="primary"):
            if transaction_type == "Buy":
                success = portfolio.buy(symbol, quantity, price, datetime.now())
                if success:
                    st.success(f"✓ Bought {quantity} {symbol}")
                else:
                    st.error("Insufficient cash")
            else:
                success = portfolio.sell(symbol, quantity, price, datetime.now())
                if success:
                    st.success(f"✓ Sold {quantity} {symbol}")
                else:
                    st.error("Insufficient shares")

        if st.button("Reset Portfolio"):
            portfolio.reset()
            st.session_state.portfolio = portfolio
            st.success("✓ Portfolio reset")

    with col2:
        st.markdown("### Summary")

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

                metric_col1, metric_col2, metric_col3 = st.columns(3)
                with metric_col1:
                    st.metric("Value", f"${summary['portfolio_value']:,.2f}")
                with metric_col2:
                    st.metric("Cash", f"${summary['cash']:,.2f}")
                with metric_col3:
                    st.metric("Return", summary['total_return_pct'])

                if summary['holdings']:
                    st.markdown("#### Holdings")

                    holdings_data = []
                    for sym, qty in summary['holdings'].items():
                        value = qty * current_prices.get(sym, 0)
                        holdings_data.append({
                            'Symbol': sym,
                            'Qty': qty,
                            'Price': f"${current_prices.get(sym, 0):.2f}",
                            'Value': f"${value:,.2f}",
                            'Allocation': f"{summary['allocation'].get(sym, 0):.1f}%"
                        })

                    holdings_df = pd.DataFrame(holdings_data)
                    st.dataframe(holdings_df, use_container_width=True, hide_index=True)

                    # Allocation chart
                    st.markdown("#### Allocation")

                    fig = go.Figure(data=[go.Pie(
                        labels=list(summary['allocation'].keys()),
                        values=list(summary['allocation'].values()),
                        hole=.4,
                        marker=dict(
                            colors=['#3b82f6', '#22c55e', '#ef4444', '#f59e0b', '#8b5cf6'],
                            line=dict(color='#000000', width=2)
                        )
                    )])
                    fig.update_layout(**PLOTLY_TEMPLATE['layout'], height=400, showlegend=True)
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.info("No holdings. Add transactions to get started.")


if __name__ == "__main__":
    main()
