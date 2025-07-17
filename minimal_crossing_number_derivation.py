from sympy import symbols, ln, solve, N

print("Testing stability condition (n-1) > ln(2n):")
print("n\t(n-1)\tln(2n)\tStable")
print("-" * 35)

minimal_n = None
for n_val in range(1, 10):
    lhs = n_val - 1
    rhs = float(ln(2 * n_val))
    stable = lhs > rhs
    
    print(f"{n_val}\t{lhs}\t{rhs:.3f}\t{stable}")
    
    if stable and minimal_n is None:
        minimal_n = n_val

if minimal_n:
    print(f"\nMinimal crossing number: {minimal_n}")
else:
    print(f"\nNo solution found in range 1-9")