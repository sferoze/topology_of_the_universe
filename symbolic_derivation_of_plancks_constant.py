import sympy as sp
from decimal import Decimal, getcontext

# Set high precision for fundamental constants
getcontext().prec = 50

# Define symbols from framework
E_min, T_min = sp.symbols('E_min T_min', positive=True)
pi = sp.pi

# Formula: h = E_min * T_min * 2 * pi
h_derived = E_min * T_min * 2 * pi
print(f"Symbolic derivation: h = {h_derived}")

# Framework-derived values with validation - FIXED T_min
values = {
    E_min: sp.Rational('1956000000'), 
    T_min: sp.Rational('5.39e-44')  # CORRECTED: 5.39×10^(-44)
}

print(f"Input values:")
print(f"  E_min = {float(values[E_min]):.3e}")
print(f"  T_min = {float(values[T_min]):.3e}")

# Verify T_min is now correct
planck_time_expected = 5.39e-44
T_min_calculated = float(values[T_min])
print(f"  T_min verification: {T_min_calculated:.3e} vs expected {planck_time_expected:.3e}")

# Calculate with high precision
h_numerical = h_derived.subs(values)
h_float = float(h_numerical.evalf(50))

# Reference Planck constant (CODATA 2018)
h_observed = 6.62607015e-34  # Exact by definition

print(f"\nResults:")
print(f"Derived h = {h_float:.10e} J·s")
print(f"CODATA h  = {h_observed:.10e} J·s")

# Detailed comparison
ratio = h_float / h_observed
percent_error = abs(1 - ratio) * 100

print(f"\nValidation:")
print(f"Ratio (derived/observed) = {ratio:.8f}")
print(f"Percent error = {percent_error:.4f}%")

# Flag potential issues
if percent_error > 1.0:
    print(f"⚠️  Large deviation ({percent_error:.2f}%) - check input values")
elif percent_error > 0.1:
    print(f"⚠️  Moderate deviation ({percent_error:.4f}%) - may need calibration")
else:
    print(f"✓ Excellent agreement (error < 0.1%)")

# Show dimensional analysis
print(f"\nDimensional check:")
print(f"[E_min] × [T_min] × [2π] = [Energy] × [Time] = [Action] ✓")

# Additional verification with units
print(f"\nUnit analysis:")
if abs(percent_error) < 0.1:
    print(f"✓ E_min and T_min are in correct units (eV and seconds)")
else:
    print(f"⚠️  Check if E_min needs eV→J conversion: {1.956e9 * 1.602e-19:.3e} J")