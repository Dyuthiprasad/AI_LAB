import itertools

variables = ['W12', 'W21', 'S11']

def implies(a, b):
    return (not a) or b

def biconditional(a, b):
    return (a and b) or ((not a) and (not b))

def rule_S11(W12, W21, S11):
    # S11 ↔ (W12 ∨ W21)
    return biconditional(S11, (W12 or W21))

def observed_fact(S11):
    return not S11

def KB(W12, W21, S11):
    return rule_S11(W12, W21, S11) and observed_fact(S11)
def query(W12, W21, S11):
    return not W12

print(f"{'W12':<6}{'W21':<6}{'S11':<6}{'KB':<8}{'¬W12 (Query)':<12}")
print("-" * 45)

kb_true_models = []

for W12, W21, S11 in itertools.product([False, True], repeat=3):
    kb = KB(W12, W21, S11)
    q = query(W12, W21, S11)
    if kb:
        kb_true_models.append((W12, W21, S11))
    print(f"{W12!s:<6}{W21!s:<6}{S11!s:<6}{kb!s:<8}{q!s:<12}")

def entails():
    for W12, W21, S11 in kb_true_models:
        if not query(W12, W21, S11):
            return False
    return True

print("\nModels where KB is true:", kb_true_models)
print("\nDoes KB entail ¬W(1,2)? :", entails())
