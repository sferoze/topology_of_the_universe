from sympy import symbols, pi, N

# Calculate primordial knot properties
print("Dark matter as primordial knots:")

# Minimal cosmic knot parameters
n_crossings = 3  # minimal stable
l_knot = 1e-15  # m (nuclear scale for primordial era)
rho_nuclear = 2.3e17  # kg/m^3

# Knot volume
V_knot = (n_crossings * l_knot)**3
print(f"Knot volume: {V_knot:.3e} m^3")

# Knot mass
m_knot = rho_nuclear * V_knot
print(f"Knot mass: {m_knot:.3e} kg")

# Convert to solar masses
m_sun = 1.989e30  # kg
m_knot_solar = m_knot / m_sun
print(f"Knot mass: {m_knot_solar:.3e} solar masses")

# Gravitational lensing signature
# Einstein radius for knot at distance D
D_lens = 1e6 * 3.086e16  # 1 Mpc in meters
D_source = 2 * D_lens
G = 6.674e-11  # m^3/kg/s^2
c = 2.998e8  # m/s
theta_E = (4 * G * m_knot / c**2 * D_lens / D_source)**0.5
print(f"Einstein radius: {theta_E:.3e} radians")

# Knot topology creates non-spherical distortion
# Deviation from circular = 1/n_crossings
asymmetry = 1 / n_crossings
print(f"Lensing asymmetry: {asymmetry * 100:.1f}\%")

# Expected output: Small knot mass; 33.3\% asymmetry.