from collections import deque

# Pretty print state
def fmt(state):
    return '\n'.join(' '.join(str(state[3*r + c]) for c in range(3)) for r in range(3))

# Solvability check (inversions)
def is_solvable(state):
    arr = [x for x in state if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    return inv % 2 == 0

# Generate successors (possible moves)
def successors(state):
    idx = state.index(0)
    r, c = divmod(idx, 3)
    moves = []
    # Up
    if r > 0:
        ni = (r-1)*3 + c
        lst = list(state); lst[idx], lst[ni] = lst[ni], lst[idx]
        moves.append((tuple(lst), 'Up'))
    # Down
    if r < 2:
        ni = (r+1)*3 + c
        lst = list(state); lst[idx], lst[ni] = lst[ni], lst[idx]
        moves.append((tuple(lst), 'Down'))
    # Left
    if c > 0:
        ni = r*3 + (c-1)
        lst = list(state); lst[idx], lst[ni] = lst[ni], lst[idx]
        moves.append((tuple(lst), 'Left'))
    # Right
    if c < 2:
        ni = r*3 + (c+1)
        lst = list(state); lst[idx], lst[ni] = lst[ni], lst[idx]
        moves.append((tuple(lst), 'Right'))
    return moves

# Depth-limited search
def dls(state, goal, limit, path, path_moves, visited):
    if state == goal:
        return path_moves[:]
    if limit == 0:
        return None
    for (succ, mv) in successors(state):
        if succ in visited:
            continue
        visited.add(succ)
        path.append(succ)
        path_moves.append(mv)
        res = dls(succ, goal, limit-1, path, path_moves, visited)
        if res is not None:
            return res
        path_moves.pop()
        path.pop()
        visited.remove(succ)
    return None

# IDDFS driver
def iddfs(start, goal, max_depth):
    if not is_solvable(start):
        return None, "Unsolvable puzzle"
    for depth in range(max_depth+1):
        visited = set([start])
        path = [start]
        path_moves = []
        res = dls(start, goal, depth, path, path_moves, visited)
        if res is not None:
            return res, f"Solved at depth {len(res)}"
    return None, "Not found within depth limit"

# Example usage
if __name__ == "__main__":
    goal = (1, 2, 3,
            4, 5, 6,
            7, 8, 0)

    # ✅ Testcase 1: Solvable within limit
    start1 = (4, 2, 3,
              1, 0, 6,
              5, 7, 8)   # Only one move away
    sol1, msg1 = iddfs(start1, goal, max_depth=20)
    print("Testcase 1:")
    print(fmt(start1))
    print("Result:", msg1)
    print("Moves:", sol1, "\n")

    # ❌ Testcase 2: Solvable but not within depth limit
    start2 = (1, 2, 3,
              4, 5, 6,
              0, 7, 8)   # Needs more than 2 moves
    sol2, msg2 = iddfs(start2, goal, max_depth=4)
    print("Testcase 2:")
    print(fmt(start2))
    print("Result:", msg2)
    print("Moves:", sol2)
