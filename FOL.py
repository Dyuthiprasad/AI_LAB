# Forward Reasoning (Forward Chaining) in First Order Logic
# Question 11 – Marcus example

# --- Knowledge Base ---

facts = {
    "Man(Marcus)",
    "Pompeian(Marcus)"
}

rules = [
    ("Pompeian(x)", "Roman(x)"),
    ("Roman(x)", "Loyal(x)"),
    ("Man(x)", "Person(x)"),
    ("Person(x)", "Mortal(x)")
]

query = "Mortal(Marcus)"


# --- Helper Functions ---

def substitute(statement, var, const):
    """Replace variable (x) with constant (Marcus)."""
    return statement.replace(var, const)


def forward_chaining(facts, rules, query):
    """Perform forward chaining until query is derived or nothing new is added."""
    derived = set(facts)

    while True:
        new_inference = False
        for premise, conclusion in rules:
            # We assume only one variable (x) for simplicity
            var = "x"

            # For each fact, see if it matches the premise when substituting x
            for fact in list(derived):
                if substitute(premise, var, "Marcus") == fact:
                    inferred = substitute(conclusion, var, "Marcus")
                    if inferred not in derived:
                        print(f"Inferred: {inferred} from {fact} using {premise} -> {conclusion}")
                        derived.add(inferred)
                        new_inference = True
                        if inferred == query:
                            return True, derived
        if not new_inference:
            break

    return (query in derived), derived


# --- Run Forward Reasoning ---

result, derived_facts = forward_chaining(facts, rules, query)

print("\n--- Final Facts Derived ---")
for f in derived_facts:
    print(f)

print("\nQuery:", query)
print("Result:", "TRUE ✅ (Marcus is Mortal)" if result else "FALSE ❌ (Not provable)")
