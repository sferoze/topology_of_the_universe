import sympy as sp

# Define symbols from framework
E_min, T_min = sp.symbols('E_min T_min', positive=True)
pi = sp.pi

# Formula: h = E_min * T_min * 2 * pi
h_derived = E_min * T_min * 2 * pi

# Show symbolic form
print(f"h = {h_derived}")  # Output: h = 2*pi*E_min*T_min

# Validate with framework-derived values
values = {E_min: 1.956e9, T_min: 5.39e-44}
h_numerical = h_derived.subs(values).evalf()
print(f"Numerical value: {h_numerical:.3e} J s")
print("Observed value: 6.626e-34 J s")
print(f"Ratio: {abs(h_numerical / 6.626e-34):.7f}")

# Expected output: Symbolic h; numerical value close to observed, ratio ~1.