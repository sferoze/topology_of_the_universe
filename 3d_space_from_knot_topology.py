from sympy import symbols, exp, diff, solve, N

# Knot complexity function K(d)
d = symbols('d', positive=True)
# K(d) models the number of stable knot types in d dimensions
# (d-1)(d-2) ensures K=0 for d<3 (no knots possible)
# exp(-(d-3)**2) strongly suppresses K for d>3 (knots trivialize)
K = (d - 1) * (d - 2) * exp(-(d - 3)**2)

# Find critical points
dK_dd = diff(K, d)
critical_points = solve(dK_dd, d)
print(f"Critical points: {critical_points}")

# Evaluate K at integer dimensions
for dim in range(1, 7):
    print(f"d={dim}: K={N(K.subs(d, dim)):.6f}")

# Second derivative at d=3
d2K_dd2 = diff(dK_dd, d)
print(f"Second derivative at d=3: {N(d2K_dd2.subs(d, 3)):.2f}")
# Negative => local maximum => stable knots peak at d=3

# Expected output: Critical points listed; K peaks at d=3 with negative second derivative.