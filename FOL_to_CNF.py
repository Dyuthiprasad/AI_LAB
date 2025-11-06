import itertools

def negate_literal(literal):
    if literal.startswith('~'):
        return literal[1:]
    else:
        return '~' + literal

def resolve(ci, cj):
    resolvents = set()
    for di in ci:
        for dj in cj:
            if di == negate_literal(dj):
                new_clause = (ci - {di}) | (cj - {dj})
                resolvents.add(frozenset(new_clause))
    return resolvents

def resolution(kb, query):
    clauses = kb.copy()
    clauses.append({negate_literal(query)})
    
    print("Initial Clauses:")
    for i, c in enumerate(clauses):
        print(f"C{i+1}: {c}")
    
    new = set()
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i+1, n)]
        
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if frozenset() in resolvents:
                print("\nEmpty clause derived -> Contradiction found!")
                return True
            new |= resolvents
        
        if new.issubset(set(map(frozenset, clauses))):
            return False
        for c in new:
            if set(c) not in clauses:
                clauses.append(set(c))

if __name__ == "__main__":
    KB = [
        {'~P', 'Q'},
        {'~Q', 'R'},
        {'P'}
    ]
    query = 'R'

    result = resolution(KB, query)
    print("\nResult:")
    if result:
        print("Query", query, "is TRUE (Proved using Resolution)")
    else:
        print("Query", query, "cannot be proven from KB")
