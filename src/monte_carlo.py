import os
import numpy as np
import matplotlib.pyplot as plt
from payoff_matrices import IBM
from nash_solver import find_pure_nash_equilibria

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)


def perturb_matrix(matrix, sigma=0.05):
    noise = np.random.normal(0, sigma, size=matrix.shape)
    return matrix * (1 + noise)


def run_monte_carlo(trials=1000, sigma=0.05, seed=42):
    np.random.seed(seed)

    attacker_results = []
    defender_results = []
    stable_count = 0

    for _ in range(trials):
        perturbed = perturb_matrix(IBM, sigma=sigma)
        equilibria = find_pure_nash_equilibria(perturbed)

        if equilibria:
            eq = equilibria[0]
            if eq["attacker_strategy"] == "PF" and eq["defender_strategy"] == "HD":
                stable_count += 1

            attacker_results.append(eq["attacker_payoff"])
            defender_results.append(eq["defender_payoff"])

    return np.array(attacker_results), np.array(defender_results), stable_count / trials

def plot_monte_carlo(attacker_results):
    plt.figure(figsize=(7, 4))
    plt.hist(attacker_results, bins=40, density=True, alpha=0.75)
    plt.axvline(-25, linestyle="--", linewidth=2, label="Theoretical PF-HD payoff")
    plt.xlabel("Attacker Payoff (SVU)")
    plt.ylabel("Probability Density")
    plt.title("Monte Carlo Distribution of Attacker Payoff")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "montecarlo.png"), dpi=300)


def plot_defender_monte_carlo(defender_results):
    plt.figure(figsize=(7, 4))
    plt.hist(defender_results, bins=40, density=True, alpha=0.75)
    plt.axvline(35, linestyle="--", linewidth=2, label="Theoretical PF-HD payoff")
    plt.xlabel("Defender Payoff (SVU)")
    plt.ylabel("Probability Density")
    plt.title("Monte Carlo Distribution of Defender Payoff")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "defender_montecarlo.png"), dpi=300)


if __name__ == "__main__":
    attacker, defender, stability = run_monte_carlo()

    print(f"Mean attacker payoff: {attacker.mean():.2f}")
    print(f"Std attacker payoff: {attacker.std():.2f}")
    print(f"Mean defender payoff: {defender.mean():.2f}")
    print(f"Std defender payoff: {defender.std():.2f}")
    print(f"PF-HD stability rate: {stability * 100:.2f}%")

    plot_monte_carlo(attacker)
    plot_defender_monte_carlo(defender)         