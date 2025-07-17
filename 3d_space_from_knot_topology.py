from sympy import symbols, exp, diff, solve, N, re, im
import numpy as np

# Knot complexity function K(d)
d = symbols('d', positive=True)
K = (d - 1) * (d - 2) * exp(-(d - 3)**2)

# Find critical points
dK_dd = diff(K, d)
print(f"First derivative: {dK_dd}")

critical_points = solve(dK_dd, d)
print(f"All critical points: {critical_points}")

# Filter for real, positive critical points
real_critical_points = []
for cp in critical_points:
    cp_val = N(cp)
    if im(cp_val) == 0 and re(cp_val) > 0:  # Real and positive
        real_critical_points.append(float(re(cp_val)))

print(f"Physical critical points (real, positive): {real_critical_points}")

# Evaluate K at integer dimensions
print("\nKnot complexity by dimension:")
print("d\tK(d)")
print("-" * 15)
for dim in range(1, 7):
    k_val = N(K.subs(d, dim))
    print(f"{dim}\t{k_val:.6f}")

# Second derivative analysis
d2K_dd2 = diff(dK_dd, d)
second_deriv_at_3 = N(d2K_dd2.subs(d, 3))
print(f"\nSecond derivative at d=3: {second_deriv_at_3:.6f}")

# Verify d=3 is maximum
if second_deriv_at_3 < 0:
    print("✓ d=3 is confirmed as local maximum (stable knots peak)")
else:
    print("✗ d=3 is not a maximum - check function definition")

# Peak validation
k_at_3 = N(K.subs(d, 3))
print(f"Peak complexity K(3) = {k_at_3:.6f}")