import numpy as np
import random

def objective(state):
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return -conflicts  # Negative because we want to minimize conflicts

def generate_neighbors(state):
    neighbors = []
    n = len(state)
    for col in range(n):
        for row in range(n):
            if row != state[col]:
                neighbor = state.copy()
                neighbor[col] = row
                neighbors.append(neighbor)
    return neighbors

def hill_climbing(objective, initial_state, max_iterations=1000):
    current = initial_state
    current_eval = objective(current)
    for iteration in range(max_iterations):
        neighbors = generate_neighbors(current)
        neighbor_evals = [objective(n) for n in neighbors]
        best_idx = np.argmax(neighbor_evals)
        best_neighbor = neighbors[best_idx]
        best_eval = neighbor_evals[best_idx]

        if best_eval > current_eval:
            current, current_eval = best_neighbor, best_eval
            print(f"Step {iteration+1}: Conflicts = {-current_eval}")
        else:
            print("No better neighbors found. Algorithm converged.")
            break
    return current, current_eval
#n = int(input())
n = 4
initial_state = [random.randint(0, n - 1) for _ in range(n)]
solution, value = hill_climbing(objective, initial_state)

print("\nFinal board (row positions for each column):", solution)
print("Final conflicts:", -value)
