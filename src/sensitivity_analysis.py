import os
import numpy as np
import matplotlib.pyplot as plt

from payoff_matrices import IBM
from nash_solver import find_pure_nash_equilibria

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)


def perturb_matrix(matrix, pct):
    noise = np.random.uniform(-pct, pct, size=matrix.shape)
    return matrix * (1 + noise)


def run_sensitivity(trials=1000, perturbations=(0.05, 0.10, 0.20, 0.30), seed=42):
    np.random.seed(seed)

    stability_rates = []
    error_bars = []

    for pct in perturbations:
        stable_count = 0

        for _ in range(trials):
            perturbed = perturb_matrix(IBM, pct)
            equilibria = find_pure_nash_equilibria(perturbed)

            if equilibria:
                eq = equilibria[0]
                if eq["attacker_strategy"] == "PF" and eq["defender_strategy"] == "HD":
                    stable_count += 1

        rate = stable_count / trials
        stability_rates.append(rate * 100)

        # Binomial standard error
        se = np.sqrt(rate * (1 - rate) / trials) * 100
        error_bars.append(se)

    return perturbations, stability_rates, error_bars


def plot_sensitivity(perturbations, stability_rates, error_bars):
    labels = [f"±{int(p * 100)}%" for p in perturbations]

    plt.figure(figsize=(7, 4))
    plt.bar(labels, stability_rates, yerr=error_bars, capsize=5)
    plt.ylim(0, 105)
    plt.xlabel("Payoff Perturbation Level")
    plt.ylabel("PF-HD Stability Rate (%)")
    plt.title("Sensitivity Analysis of Nash Equilibrium Stability")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "sensitivity.png"), dpi=300)


if __name__ == "__main__":
    perturbations, rates, errors = run_sensitivity()

    for pct, rate, err in zip(perturbations, rates, errors):
        print(f"±{int(pct * 100)}%: {rate:.2f}% stable ± {err:.2f}%")

    plot_sensitivity(perturbations, rates, errors)