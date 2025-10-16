import itertools

# Define propositional variables
variables = ['P', 'Q', 'R']

# Define helper for implication
def implies(a, b):
    return (not a) or b

# Define formulas in KB
def f1(Q, P, R):  # Q → P
    return implies(Q, P)

def f2(Q, P, R):  # P → ¬Q
    return implies(P, not Q)

def f3(Q, P, R):  # Q ∨ R
    return Q or R

# Queries
def q1(Q, P, R):  # R
    return R

def q2(Q, P, R):  # R → P
    return implies(R, P)

def q3(Q, P, R):  # Q → R
    return implies(Q, R)

# Generate truth table
print(f"{'P':<5}{'Q':<5}{'R':<5}{'Q→P':<8}{'P→¬Q':<8}{'Q∨R':<8}{'KB True?':<10}")
print("-" * 55)

kb_true_models = []

for P, Q, R in itertools.product([False, True], repeat=3):
    kb = f1(Q,P,R) and f2(Q,P,R) and f3(Q,P,R)
    if kb:
        kb_true_models.append((P, Q, R))
    print(f"{P!s:<5}{Q!s:<5}{R!s:<5}{f1(Q,P,R)!s:<8}{f2(Q,P,R)!s:<8}{f3(Q,P,R)!s:<8}{kb!s:<10}")

# Check entailments
def entails(query):
    for P, Q, R in kb_true_models:
        if not query(Q,P,R):
            return False
    return True

print("\nModels where KB is true:", kb_true_models)
print("\nEntailment results:")
print("KB ⊨ R:", entails(q1))
print("KB ⊨ (R → P):", entails(q2))
print("KB ⊨ (Q → R):", entails(q3))
