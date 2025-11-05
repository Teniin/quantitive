"""
Monte Carlo Simulator Module - Monte Carlo simulations for portfolio forecasting
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple
from scipy import stats


class MonteCarloSimulator:
    """
    Monte Carlo simulator for portfolio projections
    """

    def __init__(self, random_seed: Optional[int] = None):
        """
        Initialize Monte Carlo simulator

        Args:
            random_seed: Random seed for reproducibility
        """
        self.random_seed = random_seed
        if random_seed is not None:
            np.random.seed(random_seed)

        self.simulation_results = None

    def simulate_portfolio(
        self,
        initial_value: float,
        expected_return: float,
        volatility: float,
        time_horizon: int,
        n_simulations: int = 1000,
        periods_per_year: int = 252
    ) -> np.ndarray:
        """
        Run Monte Carlo simulation for portfolio

        Args:
            initial_value: Initial portfolio value
            expected_return: Expected annual return
            volatility: Annual volatility
            time_horizon: Number of periods to simulate
            n_simulations: Number of simulations to run
            periods_per_year: Trading periods per year

        Returns:
            Array of simulation results (n_simulations x time_horizon)
        """
        # Convert annual parameters to period parameters
        mu = expected_return / periods_per_year
        sigma = volatility / np.sqrt(periods_per_year)

        # Initialize results array
        simulations = np.zeros((n_simulations, time_horizon + 1))
        simulations[:, 0] = initial_value

        # Run simulations
        for t in range(1, time_horizon + 1):
            # Generate random returns
            random_returns = np.random.normal(mu, sigma, n_simulations)

            # Update portfolio values
            simulations[:, t] = simulations[:, t - 1] * (1 + random_returns)

        self.simulation_results = simulations
        return simulations

    def simulate_from_returns(
        self,
        initial_value: float,
        historical_returns: np.ndarray,
        time_horizon: int,
        n_simulations: int = 1000,
        method: str = 'bootstrap'
    ) -> np.ndarray:
        """
        Run Monte Carlo simulation using historical returns

        Args:
            initial_value: Initial portfolio value
            historical_returns: Array of historical returns
            time_horizon: Number of periods to simulate
            n_simulations: Number of simulations
            method: 'bootstrap' or 'parametric'

        Returns:
            Array of simulation results
        """
        simulations = np.zeros((n_simulations, time_horizon + 1))
        simulations[:, 0] = initial_value

        if method == 'bootstrap':
            # Bootstrap resampling
            for t in range(1, time_horizon + 1):
                # Randomly sample from historical returns
                sampled_returns = np.random.choice(
                    historical_returns,
                    size=n_simulations,
                    replace=True
                )
                simulations[:, t] = simulations[:, t - 1] * (1 + sampled_returns)

        elif method == 'parametric':
            # Parametric approach (assumes normal distribution)
            mu = np.mean(historical_returns)
            sigma = np.std(historical_returns)

            for t in range(1, time_horizon + 1):
                random_returns = np.random.normal(mu, sigma, n_simulations)
                simulations[:, t] = simulations[:, t - 1] * (1 + random_returns)

        else:
            raise ValueError("method must be 'bootstrap' or 'parametric'")

        self.simulation_results = simulations
        return simulations

    def simulate_multi_asset(
        self,
        initial_value: float,
        weights: np.ndarray,
        expected_returns: np.ndarray,
        covariance_matrix: np.ndarray,
        time_horizon: int,
        n_simulations: int = 1000,
        periods_per_year: int = 252
    ) -> np.ndarray:
        """
        Run Monte Carlo simulation for multi-asset portfolio

        Args:
            initial_value: Initial portfolio value
            weights: Asset weights
            expected_returns: Expected annual returns for each asset
            covariance_matrix: Annual covariance matrix
            time_horizon: Number of periods to simulate
            n_simulations: Number of simulations
            periods_per_year: Trading periods per year

        Returns:
            Array of simulation results
        """
        n_assets = len(weights)

        # Convert annual parameters to period parameters
        mu = expected_returns / periods_per_year
        cov = covariance_matrix / periods_per_year

        # Initialize results
        simulations = np.zeros((n_simulations, time_horizon + 1))
        simulations[:, 0] = initial_value

        # Run simulations
        for t in range(1, time_horizon + 1):
            # Generate correlated random returns
            random_returns = np.random.multivariate_normal(mu, cov, n_simulations)

            # Calculate portfolio returns
            portfolio_returns = np.dot(random_returns, weights)

            # Update portfolio values
            simulations[:, t] = simulations[:, t - 1] * (1 + portfolio_returns)

        self.simulation_results = simulations
        return simulations

    def calculate_statistics(
        self,
        simulations: Optional[np.ndarray] = None,
        percentiles: List[float] = [5, 25, 50, 75, 95]
    ) -> Dict:
        """
        Calculate statistics from simulations

        Args:
            simulations: Simulation results (uses stored results if None)
            percentiles: Percentiles to calculate

        Returns:
            Dictionary with statistics
        """
        if simulations is None:
            simulations = self.simulation_results

        if simulations is None:
            raise ValueError("No simulation results available")

        final_values = simulations[:, -1]

        stats_dict = {
            'mean_final_value': np.mean(final_values),
            'median_final_value': np.median(final_values),
            'std_final_value': np.std(final_values),
            'min_final_value': np.min(final_values),
            'max_final_value': np.max(final_values),
            'percentiles': {}
        }

        # Calculate percentiles
        for p in percentiles:
            stats_dict['percentiles'][f'p{p}'] = np.percentile(final_values, p)

        # Probability of profit/loss
        initial_value = simulations[0, 0]
        stats_dict['prob_profit'] = np.mean(final_values > initial_value) * 100
        stats_dict['prob_loss'] = np.mean(final_values < initial_value) * 100

        return stats_dict

    def plot_simulations(
        self,
        simulations: Optional[np.ndarray] = None,
        num_paths: int = 100,
        percentiles: List[float] = [5, 50, 95],
        figsize: Tuple[int, int] = (12, 8)
    ):
        """
        Plot Monte Carlo simulation results

        Args:
            simulations: Simulation results (uses stored results if None)
            num_paths: Number of individual paths to show
            percentiles: Percentiles to highlight
            figsize: Figure size

        Returns:
            Figure object
        """
        if simulations is None:
            simulations = self.simulation_results

        if simulations is None:
            raise ValueError("No simulation results available")

        fig, axes = plt.subplots(2, 1, figsize=figsize)

        # Plot 1: Simulation paths
        n_simulations, time_horizon = simulations.shape

        # Plot subset of paths
        sample_indices = np.random.choice(
            n_simulations,
            min(num_paths, n_simulations),
            replace=False
        )

        for idx in sample_indices:
            axes[0].plot(simulations[idx, :], alpha=0.3, linewidth=0.5, color='gray')

        # Plot percentile paths
        colors = ['red', 'green', 'blue']
        for i, p in enumerate(percentiles):
            percentile_path = np.percentile(simulations, p, axis=0)
            axes[0].plot(
                percentile_path,
                label=f'{p}th percentile',
                linewidth=2,
                color=colors[i % len(colors)]
            )

        axes[0].set_title('Monte Carlo Simulation Paths', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Time Period')
        axes[0].set_ylabel('Portfolio Value ($)')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Plot 2: Distribution of final values
        final_values = simulations[:, -1]
        axes[1].hist(final_values, bins=50, alpha=0.7, edgecolor='black')
        axes[1].axvline(
            np.mean(final_values),
            color='red',
            linestyle='--',
            linewidth=2,
            label=f'Mean: ${np.mean(final_values):,.0f}'
        )
        axes[1].axvline(
            np.median(final_values),
            color='green',
            linestyle='--',
            linewidth=2,
            label=f'Median: ${np.median(final_values):,.0f}'
        )
        axes[1].set_title('Distribution of Final Portfolio Values', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Final Portfolio Value ($)')
        axes[1].set_ylabel('Frequency')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

        return fig

    def plot_confidence_intervals(
        self,
        simulations: Optional[np.ndarray] = None,
        confidence_levels: List[float] = [0.68, 0.95],
        figsize: Tuple[int, int] = (12, 6)
    ):
        """
        Plot confidence intervals over time

        Args:
            simulations: Simulation results
            confidence_levels: Confidence levels to plot
            figsize: Figure size

        Returns:
            Figure object
        """
        if simulations is None:
            simulations = self.simulation_results

        if simulations is None:
            raise ValueError("No simulation results available")

        fig, ax = plt.subplots(figsize=figsize)

        # Calculate percentiles at each time step
        median = np.percentile(simulations, 50, axis=0)
        ax.plot(median, label='Median', linewidth=2, color='green')

        colors = ['blue', 'red']
        alphas = [0.3, 0.2]

        for i, conf_level in enumerate(confidence_levels):
            lower_percentile = (1 - conf_level) / 2 * 100
            upper_percentile = (1 + conf_level) / 2 * 100

            lower = np.percentile(simulations, lower_percentile, axis=0)
            upper = np.percentile(simulations, upper_percentile, axis=0)

            ax.fill_between(
                range(len(median)),
                lower,
                upper,
                alpha=alphas[i],
                color=colors[i],
                label=f'{conf_level*100:.0f}% Confidence Interval'
            )

        ax.set_title('Portfolio Value Confidence Intervals', fontsize=14, fontweight='bold')
        ax.set_xlabel('Time Period')
        ax.set_ylabel('Portfolio Value ($)')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

        return fig

    def print_summary(self, simulations: Optional[np.ndarray] = None):
        """
        Print summary statistics

        Args:
            simulations: Simulation results
        """
        stats = self.calculate_statistics(simulations)

        print("\n" + "=" * 60)
        print("MONTE CARLO SIMULATION RESULTS")
        print("=" * 60)

        if simulations is None:
            simulations = self.simulation_results

        print(f"\nNumber of Simulations: {simulations.shape[0]:,}")
        print(f"Time Horizon: {simulations.shape[1] - 1} periods")
        print(f"Initial Value: ${simulations[0, 0]:,.2f}")

        print("\n" + "-" * 60)
        print("FINAL VALUE STATISTICS")
        print("-" * 60)

        print(f"Mean Final Value:     ${stats['mean_final_value']:,.2f}")
        print(f"Median Final Value:   ${stats['median_final_value']:,.2f}")
        print(f"Std Dev:              ${stats['std_final_value']:,.2f}")
        print(f"Min Final Value:      ${stats['min_final_value']:,.2f}")
        print(f"Max Final Value:      ${stats['max_final_value']:,.2f}")

        print("\n" + "-" * 60)
        print("PERCENTILES")
        print("-" * 60)

        for key, value in stats['percentiles'].items():
            print(f"{key.upper():20s} ${value:,.2f}")

        print("\n" + "-" * 60)
        print("PROBABILITIES")
        print("-" * 60)

        print(f"Probability of Profit: {stats['prob_profit']:.2f}%")
        print(f"Probability of Loss:   {stats['prob_loss']:.2f}%")

        print("=" * 60 + "\n")
