# --- Resolution Example: sneeze(mary) proof ---

from copy import deepcopy

# ---------- UNIFICATION ----------
def unify(x, y, subs):
    """Unify two terms given substitution set."""
    if subs is None:
        return None
    elif x == y:
        return subs
    elif isinstance(x, str) and x.islower():  # variable
        return unify_var(x, y, subs)
    elif isinstance(y, str) and y.islower():
        return unify_var(y, x, subs)
    elif isinstance(x, tuple) and isinstance(y, tuple):
        if x[0] != y[0] or len(x[1]) != len(y[1]):
            return None
        for a, b in zip(x[1], y[1]):
            subs = unify(a, b, subs)
            if subs is None:
                return None
        return subs
    else:
        return None

def unify_var(var, x, subs):
    if var in subs:
        return unify(subs[var], x, subs)
    elif x in subs:
        return unify(var, subs[x], subs)
    elif occurs_check(var, x, subs):
        return None
    else:
        subs = subs.copy()
        subs[var] = x
        return subs

def occurs_check(var, x, subs):
    if var == x:
        return True
    elif isinstance(x, tuple):
        return any(occurs_check(var, arg, subs) for arg in x[1])
    elif x in subs:
        return occurs_check(var, subs[x], subs)
    return False

# ---------- CLAUSE UTILITIES ----------
def substitute(literal, subs):
    pred, args = literal
    new_args = []
    for a in args:
        while a in subs:
            a = subs[a]
        new_args.append(a)
    return (pred, tuple(new_args))

def apply_substitution(clause, subs):
    return [substitute(lit, subs) for lit in clause]

def negate(pred):
    return pred[1:] if pred.startswith('¬') else '¬' + pred

# ---------- RESOLUTION CORE ----------
def resolve(ci, cj):
    resolvents = []
    for li in ci:
        for lj in cj:
            if li[0] == negate(lj[0]):  # complementary
                subs = unify(li[1], lj[1], {})
                if subs is not None:
                    # Apply substitution before combining
                    new_ci = [substitute(l, subs) for l in ci if l != li]
                    new_cj = [substitute(l, subs) for l in cj if l != lj]
                    new_clause = new_ci + new_cj
                    # remove duplicates
                    new_clause = [lit for i, lit in enumerate(new_clause) if lit not in new_clause[:i]]
                    resolvents.append(new_clause)
    return resolvents

def resolution(kb, neg_goal):
    clauses = deepcopy(kb) + [neg_goal]
    print("Initial clauses:")
    for c in clauses:
        print(" ", c)

    step = 1
    while True:
        new = []
        n = len(clauses)
        for i in range(n):
            for j in range(i + 1, n):
                resolvents = resolve(clauses[i], clauses[j])
                for r in resolvents:
                    if not r:
                        print(f"\nStep {step}: Resolved {clauses[i]} and {clauses[j]} => []")
                        print("\n✅ sneeze(mary) is PROVEN (contradiction reached).")
                        return True
                    if r not in new and r not in clauses:
                        new.append(r)
                        print(f"Step {step}: Resolved {clauses[i]} and {clauses[j]} => {r}")
                        step += 1
        if not new:
            print("\n❌ sneeze(mary) CANNOT be proven from KB.")
            return False
        clauses.extend(new)

# ---------- KNOWLEDGE BASE ----------
# Each literal: (predicate, (args,))
# Variables use lowercase letters like x,y
# Constants use lowercase names like mary, felix

kb = [
    [('¬allergies', ('x',)), ('sneeze', ('x',))],                              # allergies(x) -> sneeze(x)
    [('¬cat', ('y',)), ('¬allergicToCats', ('x',)), ('allergies', ('x',))],   # cat(y) ∧ allergicToCats(x) -> allergies(x)
    [('cat', ('felix',))],                                                    # cat(felix)
    [('allergicToCats', ('mary',))]                                           # allergicToCats(mary)
]

neg_goal = [('¬sneeze', ('mary',))]  # negated goal

# ---------- RUN ----------
print("\nResolution proof process:\n")
resolution(kb, neg_goal)
