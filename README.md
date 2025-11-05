# 📈 Portfolio Simulator

A comprehensive quantitative trading and portfolio simulation framework with backtesting, Monte Carlo simulations, and advanced risk analytics.

## 🌟 Features

### Core Capabilities
- **Portfolio Management**: Track holdings, execute trades, and monitor performance
- **Backtesting Engine**: Test trading strategies on historical market data
- **Monte Carlo Simulations**: Probabilistic forecasting of portfolio performance
- **Risk Analytics**: Comprehensive risk metrics including Sharpe, Sortino, VaR, and more
- **Real-time Market Data**: Integration with yfinance for live and historical data
- **Interactive Dashboard**: Streamlit-based web interface for visualization and analysis

### Trading Strategies
- Buy and Hold
- Moving Average Crossover
- Extensible framework for custom strategies

### Risk Metrics
- Sharpe Ratio
- Sortino Ratio
- Calmar Ratio
- Maximum Drawdown
- Value at Risk (VaR)
- Conditional Value at Risk (CVaR)
- Beta and Alpha
- Information Ratio
- Volatility metrics
- And more...

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd quantitive
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Demo

Run the comprehensive demo script:
```bash
python demo.py
```

Or run individual demos:
```bash
# Buy and Hold backtest
python demo.py backtest

# Moving Average Crossover
python demo.py ma

# Monte Carlo simulation
python demo.py monte_carlo

# Historical Monte Carlo
python demo.py historical_mc

# Risk metrics analysis
python demo.py risk

# Portfolio management
python demo.py portfolio
```

### Launching the Dashboard

Start the interactive Streamlit dashboard:
```bash
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📚 Usage Examples

### 1. Backtesting a Strategy

```python
from portfolio_simulator import Backtester
from portfolio_simulator.backtester import BuyAndHoldStrategy

# Define your portfolio
symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
weights = {symbol: 0.25 for symbol in symbols}

# Create strategy
strategy = BuyAndHoldStrategy(symbols, weights)

# Create backtester
backtester = Backtester(
    strategy=strategy,
    initial_capital=100000,
    commission=0.001
)

# Run backtest
results = backtester.run(
    symbols=symbols,
    start_date='2022-01-01',
    end_date='2024-01-01'
)

# Print results
backtester.print_summary()
backtester.plot_results()
```

### 2. Monte Carlo Simulation

```python
from portfolio_simulator import MonteCarloSimulator

# Create simulator
simulator = MonteCarloSimulator(random_seed=42)

# Run simulation
simulations = simulator.simulate_portfolio(
    initial_value=100000,
    expected_return=0.08,  # 8% annual return
    volatility=0.15,       # 15% annual volatility
    time_horizon=252,      # 1 year (trading days)
    n_simulations=1000
)

# Analyze results
simulator.print_summary()
simulator.plot_simulations()
simulator.plot_confidence_intervals()
```

### 3. Risk Analysis

```python
from portfolio_simulator import DataFetcher, RiskMetrics

# Fetch data
data_fetcher = DataFetcher()
returns = data_fetcher.get_returns('AAPL', start_date='2022-01-01', end_date='2024-01-01')
benchmark_returns = data_fetcher.get_returns('SPY', start_date='2022-01-01', end_date='2024-01-01')

# Calculate all risk metrics
metrics = RiskMetrics.calculate_all_metrics(
    returns=returns['AAPL'],
    benchmark_returns=benchmark_returns['SPY'],
    risk_free_rate=0.04
)

# Print metrics
for metric, value in metrics.items():
    print(f"{metric}: {value}")
```

### 4. Portfolio Management

```python
from portfolio_simulator import Portfolio
from datetime import datetime

# Create portfolio
portfolio = Portfolio(initial_capital=100000, name="My Portfolio")

# Execute trades
portfolio.buy('AAPL', 100, 180.0, datetime.now())
portfolio.buy('MSFT', 50, 380.0, datetime.now())

# Get current prices (example)
current_prices = {'AAPL': 185.0, 'MSFT': 390.0}

# Get portfolio summary
summary = portfolio.summary(current_prices)
print(f"Portfolio Value: ${summary['portfolio_value']:,.2f}")
print(f"Total Return: {summary['total_return_pct']}")
```

## 🏗️ Project Structure

```
quantitive/
├── portfolio_simulator/
│   ├── __init__.py              # Package initialization
│   ├── data_fetcher.py          # Market data fetching
│   ├── portfolio.py             # Portfolio management
│   ├── backtester.py            # Backtesting engine
│   ├── risk_metrics.py          # Risk calculations
│   └── monte_carlo.py           # Monte Carlo simulations
├── tests/                       # Unit tests
├── demo.py                      # Demo script
├── dashboard.py                 # Streamlit dashboard
├── requirements.txt             # Dependencies
└── README.md                    # Documentation
```

## 📊 Dashboard Features

The Streamlit dashboard provides an interactive interface with five main sections:

### 1. Home
- Overview of features
- Quick navigation

### 2. Backtesting
- Configure and run strategy backtests
- Interactive parameter adjustment
- Performance visualization
- Detailed metrics and transaction history

### 3. Monte Carlo Simulation
- Parametric and bootstrap simulations
- Adjustable parameters (return, volatility, horizon)
- Probability distributions
- Confidence intervals

### 4. Risk Analysis
- Comprehensive risk metrics
- Performance comparisons
- Visual analytics

### 5. Portfolio Manager
- Add/remove positions
- Track portfolio value
- View allocation
- Transaction history

## 🔧 Technical Details

### Dependencies
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Visualization
- **yfinance**: Market data
- **streamlit**: Web dashboard
- **scipy**: Statistical computations
- **seaborn**: Enhanced visualizations
- **plotly**: Interactive charts

### Data Source
Market data is fetched using the yfinance library, which provides:
- Historical price data
- Real-time quotes
- Company information
- Multiple timeframes and intervals

### Risk Metrics Formulas

**Sharpe Ratio**: `(Return - Risk-Free Rate) / Volatility`

**Sortino Ratio**: `(Return - Risk-Free Rate) / Downside Deviation`

**Calmar Ratio**: `Annualized Return / Max Drawdown`

**Maximum Drawdown**: `(Trough Value - Peak Value) / Peak Value`

**Beta**: `Covariance(Portfolio, Market) / Variance(Market)`

**Alpha**: `Portfolio Return - [Risk-Free Rate + Beta × (Market Return - Risk-Free Rate)]`

## 🎯 Use Cases

1. **Strategy Development**: Test and validate trading strategies before live deployment
2. **Risk Assessment**: Analyze portfolio risk exposure and characteristics
3. **Performance Attribution**: Understand sources of returns and risks
4. **Scenario Analysis**: Explore potential future outcomes via Monte Carlo
5. **Portfolio Optimization**: Compare different asset allocations
6. **Educational**: Learn about quantitative finance and portfolio theory

## 🔮 Future Enhancements

- [ ] Additional trading strategies (Mean Reversion, Momentum, etc.)
- [ ] Multi-factor models
- [ ] Options and derivatives support
- [ ] Machine learning integration
- [ ] Real-time trading capabilities
- [ ] Portfolio optimization algorithms
- [ ] Custom indicator builder
- [ ] Advanced reporting and exports

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📧 Contact

For questions or feedback, please open an issue on the repository.

## 🙏 Acknowledgments

- Market data provided by Yahoo Finance via yfinance
- Built with Python and modern data science libraries
- Inspired by quantitative finance research and best practices

---

**Disclaimer**: This tool is for educational and research purposes only. Past performance does not guarantee future results. Always do your own research before making investment decisions.
