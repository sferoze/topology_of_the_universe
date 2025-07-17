from sympy import symbols, ln, N

# Model Hubble parameter evolution from knot dynamics
t, t0, H0, alpha = symbols('t t0 H0 alpha', positive=True)

# Information growth drives expansion
# Knot unknotting rate increases with total information
unknotting_rate = alpha * ln(t / t0)

# Hubble parameter
H = H0 * (1 + unknotting_rate)
print("Hubble parameter evolution H(t):")
print(f"H(t) = H0 * (1 + alpha * ln(t/t0))")

# Numerical example with values
values_now = {t: 13.8e9, t0: 13.8e9, H0: 70, alpha: 0.1}
H_now = N(H.subs(values_now))
print(f"H(now) = {H_now:.1f} km/s/Mpc")

# Future prediction (20 Gyr)
values_future = values_now.copy()
values_future[t] = 20e9
H_future = N(H.subs(values_future))
print(f"H(20 Gyr) = {H_future:.1f} km/s/Mpc")

# Far future (100 Gyr)
values_far = values_now.copy()
values_far[t] = 100e9
H_far = N(H.subs(values_far))
print(f"H(100 Gyr) = {H_far:.1f} km/s/Mpc")

# Expected output: H(t) formula; sample values as shown.