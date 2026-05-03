import os
import numpy as np
import matplotlib.pyplot as plt

from payoff_matrices import IBM
from nash_solver import find_pure_nash_equilibria

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)


def apply_honeypot_penalty(matrix, penalty):
    modified = matrix.copy()

    # HD column index = 2
    modified[:, 2, 1] -= penalty

    return modified


def run_ablation(penalties=np.arange(0, 61, 5)):
    defender_payoffs = []
    equilibrium_labels = []

    for penalty in penalties:
        modified = apply_honeypot_penalty(IBM, penalty)
        equilibria = find_pure_nash_equilibria(modified)

        if equilibria:
            eq = equilibria[0]
            equilibrium_labels.append(f"{eq['attacker_strategy']}-{eq['defender_strategy']}")
            defender_payoffs.append(eq["defender_payoff"])
        else:
            equilibrium_labels.append("None")
            defender_payoffs.append(np.nan)

    return penalties, defender_payoffs, equilibrium_labels


def plot_ablation(penalties, defender_payoffs):
    plt.figure(figsize=(7, 4))
    plt.plot(penalties, defender_payoffs, marker="o")
    plt.axhline(25, linestyle="--", linewidth=2, label="AR payoff baseline")
    plt.xlabel("Additional Honeypot Deployment Cost Penalty (SVU)")
    plt.ylabel("Defender Equilibrium Payoff (SVU)")
    plt.title("Ablation Study: Impact of Honeypot Cost on Defender Utility")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "ablation_honeypot_cost.png"), dpi=300)


if __name__ == "__main__":
    penalties, payoffs, equilibria = run_ablation()

    for p, payoff, eq in zip(penalties, payoffs, equilibria):
        print(f"Penalty {p:>2} SVU | Equilibrium: {eq:<6} | Defender payoff: {payoff}")

    plot_ablation(penalties, payoffs)