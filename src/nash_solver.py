import numpy as np
from payoff_matrices import MATRICES, ATTACKER_STRATEGIES, DEFENDER_STRATEGIES


def find_pure_nash_equilibria(matrix):
    attacker_payoffs = matrix[:, :, 0]
    defender_payoffs = matrix[:, :, 1]

    attacker_best_responses = attacker_payoffs == attacker_payoffs.max(axis=0)
    defender_best_responses = defender_payoffs == defender_payoffs.max(axis=1)[:, None]

    equilibria = np.argwhere(attacker_best_responses & defender_best_responses)

    return [
        {
            "attacker_strategy": ATTACKER_STRATEGIES[i],
            "defender_strategy": DEFENDER_STRATEGIES[j],
            "attacker_payoff": attacker_payoffs[i, j],
            "defender_payoff": defender_payoffs[i, j],
        }
        for i, j in equilibria
    ]


if __name__ == "__main__":
    for name, matrix in MATRICES.items():
        print(f"\n{name}")
        equilibria = find_pure_nash_equilibria(matrix)
        for eq in equilibria:
            print(eq)