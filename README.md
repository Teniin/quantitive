# 📈 Portfolio Simulator

A comprehensive quantitative trading and portfolio simulation framework with backtesting, Monte Carlo simulations, and advanced risk analytics.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Getting Started](#-getting-started)
- [Running the App](#-running-the-app)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [Dashboard Features](#-dashboard-features)
- [Documentation](#-documentation)

---

## ⚡ Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Internet connection (for fetching market data)

### Installation

**1. Get the code:**

```bash
# Option A: Clone from GitHub (if you've pushed it there)
git clone https://github.com/YOUR_GITHUB_USERNAME/quantitive.git
cd quantitive

# Option B: If you already have the code locally
cd /path/to/quantitive
```

> **Note:** Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username if you've pushed this to GitHub.

**2. Create a virtual environment (recommended):**

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the App

### Option 1: Launch the Interactive Dashboard (Recommended)

The modern Vercel-inspired dashboard provides the best user experience:

```bash
streamlit run dashboard.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

**Dashboard Pages:**
- 🏠 **Home** - Overview and features
- 📊 **Backtesting** - Test trading strategies
- 🎲 **Monte Carlo** - Run probabilistic simulations
- ⚠️ **Risk Analysis** - Comprehensive risk metrics
- 💼 **Portfolio** - Manage holdings and track performance

### Option 2: Run Demo Scripts

Run all demos interactively:

```bash
python demo.py
```

Or run specific demos:

```bash
# Backtest a Buy & Hold strategy
python demo.py backtest

# Moving Average Crossover strategy
python demo.py ma

# Monte Carlo simulation
python demo.py monte_carlo

# Historical Monte Carlo
python demo.py historical_mc

# Risk metrics analysis
python demo.py risk

# Portfolio management demo
python demo.py portfolio
```

### Option 3: Use as a Python Library

```python
from portfolio_simulator import Backtester, DataFetcher
from portfolio_simulator.backtester import BuyAndHoldStrategy

# Create and run a backtest
symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
strategy = BuyAndHoldStrategy(symbols, weights={s: 0.25 for s in symbols})

backtester = Backtester(strategy, initial_capital=100000)
results = backtester.run(symbols, '2022-01-01', '2024-01-01')

backtester.print_summary()
backtester.plot_results()
```

---

## 🌟 Features

### Core Capabilities

✅ **Portfolio Management** - Track holdings, execute trades, and monitor performance
✅ **Backtesting Engine** - Test trading strategies on historical market data
✅ **Monte Carlo Simulations** - Probabilistic forecasting with 1000+ scenarios
✅ **Risk Analytics** - 15+ comprehensive risk metrics
✅ **Real-time Market Data** - Integration with yfinance for live and historical data
✅ **Modern UI** - Vercel-inspired Streamlit dashboard with dark theme

### Trading Strategies

- **Buy and Hold** - Long-term investment strategy with custom weights
- **Moving Average Crossover** - Technical analysis strategy (50/200 day MA)
- **Extensible Framework** - Easy to add custom strategies

### Risk Metrics

| Metric | Description |
|--------|-------------|
| Sharpe Ratio | Risk-adjusted return measure |
| Sortino Ratio | Downside risk-adjusted return |
| Calmar Ratio | Return vs. maximum drawdown |
| Maximum Drawdown | Largest peak-to-trough decline |
| Value at Risk (VaR) | Potential loss at confidence level |
| CVaR | Expected loss beyond VaR |
| Beta & Alpha | Market-relative performance |
| Volatility | Price variation measure |

---

## 📚 Usage Examples

### Example 1: Backtesting a Portfolio

```python
from portfolio_simulator import Backtester
from portfolio_simulator.backtester import BuyAndHoldStrategy

# Define portfolio
symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
weights = {'AAPL': 0.25, 'MSFT': 0.25, 'GOOGL': 0.25, 'AMZN': 0.25}

# Create strategy
strategy = BuyAndHoldStrategy(symbols, weights)

# Run backtest
backtester = Backtester(strategy, initial_capital=100000, commission=0.001)
results = backtester.run(
    symbols=symbols,
    start_date='2022-01-01',
    end_date='2024-01-01'
)

# View results
backtester.print_summary()
backtester.plot_results()
```

### Example 2: Monte Carlo Simulation

```python
from portfolio_simulator import MonteCarloSimulator

# Create simulator
simulator = MonteCarloSimulator(random_seed=42)

# Run simulation
simulations = simulator.simulate_portfolio(
    initial_value=100000,
    expected_return=0.08,  # 8% expected annual return
    volatility=0.15,       # 15% annual volatility
    time_horizon=252,      # 1 year (trading days)
    n_simulations=1000
)

# Analyze results
simulator.print_summary()
simulator.plot_simulations()
simulator.plot_confidence_intervals()
```

### Example 3: Risk Analysis

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

# Display metrics
for metric, value in metrics.items():
    print(f"{metric}: {value}")
```

### Example 4: Portfolio Management

```python
from portfolio_simulator import Portfolio
from datetime import datetime

# Create portfolio
portfolio = Portfolio(initial_capital=100000, name="My Portfolio")

# Execute trades
portfolio.buy('AAPL', 100, 180.0, datetime.now())
portfolio.buy('MSFT', 50, 380.0, datetime.now())
portfolio.buy('GOOGL', 75, 140.0, datetime.now())

# Get current prices
current_prices = {'AAPL': 185.0, 'MSFT': 390.0, 'GOOGL': 145.0}

# View summary
summary = portfolio.summary(current_prices)
print(f"Portfolio Value: ${summary['portfolio_value']:,.2f}")
print(f"Total Return: {summary['total_return_pct']}")
print(f"Allocation: {summary['allocation']}")
```

---

## 🏗️ Project Structure

```
quantitive/
├── portfolio_simulator/          # Core package
│   ├── __init__.py              # Package initialization
│   ├── data_fetcher.py          # Market data fetching (yfinance)
│   ├── portfolio.py             # Portfolio management
│   ├── backtester.py            # Backtesting engine + strategies
│   ├── risk_metrics.py          # Risk calculations (15+ metrics)
│   └── monte_carlo.py           # Monte Carlo simulations
│
├── tests/                       # Unit tests
│   ├── __init__.py
│   ├── test_portfolio.py        # Portfolio tests
│   └── test_risk_metrics.py    # Risk metrics tests
│
├── dashboard.py                 # Streamlit web dashboard
├── demo.py                      # Demo scripts
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

---

## 📊 Dashboard Features

The modern Streamlit dashboard provides an intuitive interface with five main sections:

### 1. 🏠 Home
- Platform overview
- Feature highlights with animated cards
- Quick statistics

### 2. 📊 Backtesting
- Strategy configuration panel
- Multiple strategy support
- Interactive performance charts
- Comprehensive metrics table
- Transaction history

### 3. 🎲 Monte Carlo Simulation
- Parametric and bootstrap methods
- Adjustable parameters (return, volatility, horizon)
- Simulation path visualization
- Probability distributions
- Percentile analysis

### 4. ⚠️ Risk Analysis
- 15+ comprehensive risk metrics
- Performance vs. benchmark comparison
- Cumulative returns charts
- Sharpe, Sortino, VaR, CVaR, and more

### 5. 💼 Portfolio Manager
- Add/remove positions
- Real-time portfolio valuation
- Allocation pie chart
- Transaction history
- Performance tracking

### Design Features

The dashboard features a **modern Vercel-inspired design**:

✨ Dark theme with subtle gradients
✨ Glassmorphism effects
✨ Smooth animations and transitions
✨ Professional typography (Inter font)
✨ Responsive layout
✨ Interactive charts with Plotly

---

## 🔧 Technical Details

### Dependencies

- **pandas** (≥2.0.0) - Data manipulation
- **numpy** (≥1.24.0) - Numerical computations
- **matplotlib** (≥3.7.0) - Visualization
- **yfinance** (≥0.2.28) - Market data
- **streamlit** (≥1.28.0) - Web dashboard
- **scipy** (≥1.11.0) - Statistical functions
- **seaborn** (≥0.12.0) - Enhanced plots
- **plotly** (≥5.17.0) - Interactive charts

### Data Source

Market data is fetched using **yfinance**, which provides:
- Historical price data
- Real-time quotes
- Company information
- Multiple timeframes and intervals

### Risk Metrics Formulas

**Sharpe Ratio**
```
Sharpe = (Return - Risk-Free Rate) / Volatility
```

**Sortino Ratio**
```
Sortino = (Return - Risk-Free Rate) / Downside Deviation
```

**Maximum Drawdown**
```
Max DD = (Trough Value - Peak Value) / Peak Value
```

**Value at Risk (VaR)**
```
VaR = Percentile of returns at confidence level
```

---

## 🧪 Running Tests

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_portfolio.py

# Run with coverage
pytest --cov=portfolio_simulator tests/
```

---

## 🎯 Use Cases

1. **Strategy Development** - Test and validate trading strategies before deployment
2. **Risk Assessment** - Analyze portfolio risk exposure and characteristics
3. **Performance Attribution** - Understand sources of returns and risks
4. **Scenario Analysis** - Explore potential future outcomes via Monte Carlo
5. **Portfolio Optimization** - Compare different asset allocations
6. **Education** - Learn about quantitative finance and portfolio theory

---

## 🐛 Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: yfinance data fetch errors**
```bash
# Solution: Check internet connection and try again
# yfinance sometimes has rate limits, wait a few seconds and retry
```

**Issue: Streamlit not opening in browser**
```bash
# Solution: Manually open the URL shown in terminal
# Usually: http://localhost:8501
```

**Issue: Port 8501 already in use**
```bash
# Solution: Use a different port
streamlit run dashboard.py --server.port 8502
```

---

## 🔮 Future Enhancements

- [ ] Additional trading strategies (Mean Reversion, Momentum, etc.)
- [ ] Multi-factor models
- [ ] Options and derivatives support
- [ ] Machine learning integration
- [ ] Real-time trading capabilities
- [ ] Portfolio optimization algorithms (Markowitz, Black-Litterman)
- [ ] Custom indicator builder
- [ ] Advanced reporting and exports (PDF, Excel)
- [ ] API for programmatic access
- [ ] Historical scenario replay

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

- Bug reports
- Feature requests
- Documentation improvements
- Code enhancements

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Support

For questions, issues, or feedback:

- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation

---

## 🙏 Acknowledgments

- Market data provided by **Yahoo Finance** via yfinance
- Built with **Python** and modern data science libraries
- Inspired by quantitative finance research and best practices
- UI design inspired by **Vercel**

---

## ⚠️ Disclaimer

**This tool is for educational and research purposes only.**

- Past performance does not guarantee future results
- Not financial advice
- Always do your own research before making investment decisions
- The authors are not responsible for any financial losses

---

## 📸 Screenshots

### Dashboard Home
![Dashboard Home](https://via.placeholder.com/800x400?text=Dashboard+Home)

### Backtesting Results
![Backtesting](https://via.placeholder.com/800x400?text=Backtesting+Results)

### Monte Carlo Simulation
![Monte Carlo](https://via.placeholder.com/800x400?text=Monte+Carlo+Simulation)

### Risk Analysis
![Risk Analysis](https://via.placeholder.com/800x400?text=Risk+Analysis)

---

**Made with ❤️ for quantitative traders and investors**

⭐ Star this repo if you find it useful!
