from sympy import symbols, ln, solve, N

# Find minimal n where (n-1) > ln(2n)
print("Testing stability condition (n-1) > ln(2n):")
for n_val in range(1, 10):
    lhs = n_val - 1
    rhs = float(ln(2 * n_val))
    stable = lhs > rhs
    if stable and n_val > 1:
        print(f"Minimal crossing number: {n_val}")
        break