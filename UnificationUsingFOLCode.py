# Unification in First Order Logic
# Question 9 - Implementation in Python

def is_variable(term):
    """Check if a term is a variable (lowercase single letter or starts with lowercase)."""
    return term[0].islower() and term.isalpha()

def is_compound(term):
    """Check if a term is a compound expression like Loves(x, Marcus)."""
    return '(' in term and ')' in term

def get_functor(term):
    """Return the functor (predicate name)."""
    return term.split('(')[0]

def get_args(term):
    """Return list of arguments from a compound term."""
    inside = term[term.find('(')+1 : term.rfind(')')]
    return [x.strip() for x in inside.split(',')]

def occurs_check(var, term, subst):
    """Check if var occurs in term (to avoid infinite substitutions)."""
    if var == term:
        return True
    if is_compound(term):
        for arg in get_args(term):
            if occurs_check(var, substitute(arg, subst), subst):
                return True
    return False

def substitute(term, subst):
    """Apply current substitutions to a term."""
    if is_variable(term) and term in subst:
        return substitute(subst[term], subst)
    elif is_compound(term):
        return get_functor(term) + "(" + ", ".join(substitute(arg, subst) for arg in get_args(term)) + ")"
    return term

def unify(x, y, subst=None):
    """Main Unification algorithm returning most general unifier (MGU)."""
    if subst is None:
        subst = {}

    x = substitute(x, subst)
    y = substitute(y, subst)

    # if same, done
    if x == y:
        return subst

    # if variable
    if is_variable(x):
        if occurs_check(x, y, subst):
            return None
        subst[x] = y
        return subst

    if is_variable(y):
        if occurs_check(y, x, subst):
            return None
        subst[y] = x
        return subst

    # if compound terms
    if is_compound(x) and is_compound(y):
        if get_functor(x) != get_functor(y):
            return None  # different functors
        x_args, y_args = get_args(x), get_args(y)
        if len(x_args) != len(y_args):
            return None  # different arity
        for a, b in zip(x_args, y_args):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst

    # constants mismatch
    return None


# --- Example Runs ---
pairs = [
    ("Man(x)", "Man(Marcus)"),
    ("Loves(x, f(y))", "Loves(g(z), f(a))"),
    ("Knows(John, x)", "Knows(y, Marcus)"),
    ("Knows(x, x)", "Knows(Marcus, Pompeian(Marcus))"),  # should fail
]

for t1, t2 in pairs:
    print(f"\nUnifying: {t1}  AND  {t2}")
    result = unify(t1, t2)
    if result:
        print("MGU =", result)
    else:
        print("Unification Failed")
