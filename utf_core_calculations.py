# File: utf_core_calculations.py
# Description: Core mathematical derivations for the Unified Topological Framework (UTF).
# Aligned with the Zero-Parameter version of the paper.

import mpmath

def calculate_utf_parameters(dps=100):
    """
    Calculates all fundamental parameters of the UTF at the specified precision.
    """
    # Set precision
    mpmath.mp.dps = dps
    
    # 1. Fundamental Mathematical Constants
    PI = mpmath.pi
    LN2 = mpmath.ln(2)
    E = mpmath.e
    
    # 2. The Critical Dimension (n_crit) (Theorem 2.3)
    # n-1 = ln(2n) => Solved using Lambert W function on the W_-1 branch (n>1)
    W_input = -1 / (2 * E)
    N_CRIT = -mpmath.lambertw(W_input, k=-1)
    D = 3
    DELTA_D = D - N_CRIT
    
    # 3. Geometric Constants (Volume of Figure-Eight Knot Complement) (Sec 3.3)
    # V = 2 * Gieseking Constant = 2 * Im(Li2(exp(i*pi/3)))
    I = mpmath.j
    Z = mpmath.exp(I * PI / 3)
    # Using polylog(s, z) for Li_s(z)
    GIESEKING = mpmath.im(mpmath.polylog(2, Z))
    V_M = 2 * GIESEKING
    
    # 4. Dynamic Constants (ZFP - Derived from Holographic Efficiency E=2.5) (Theorem 7.4)
    # eta = (12 * V_M) / (5 * PI)
    ETA = (12 * V_M) / (5 * PI)
    D_FLOW = 2 / ETA
    
    # 5. Complexity Measures (Sec 6)
    C_M = 137
    C_EFF = 105
    R = 8
    SCALE_RATIO = mpmath.mpf(C_M) / R # 17.125
    
    # 6. Boundary Corrections (Derived) (Theorem 10.5)
    # epsilon = -V_M / C_EFF (Theorem 10.4: Vol_Ncrit(M) = V_M)
    EPSILON = -V_M / C_EFF
    
    # Xi = -(sqrt(PI) + Delta_D/24) (Negative sign verified)
    XI = -(mpmath.sqrt(PI) + DELTA_D/24)
    
    # delta = Xi * epsilon
    DELTA = XI * EPSILON
    
    # 7. Bare Predictions (A_0, B_0) (Sec 10.1, 10.2)
    # A_0 = PI^4 * V_M * ln(2)
    A_0 = (PI**4) * V_M * LN2
    
    # B_0 = 6 * PI^5
    B_0 = 6 * (PI**5)
    
    # 8. Final Predictions (P1, P2)
    ALPHA_INV_PRED = A_0 + EPSILON
    MU_P_E_PRED = B_0 + DELTA
    
    # 9. Mass Functional Coefficients (Normalized) (Sec 9.4.1)
    # Kappa' = 288 / (5 * PI)
    KAPPA_PRIME = 288 / (5 * PI)
    
    # Mu' = Delta_D * PI
    MU_PRIME = DELTA_D * PI
    
    # Store results in a dictionary
    results = {
        'N_CRIT': N_CRIT,
        'DELTA_D': DELTA_D,
        'V_M': V_M,
        'ETA': ETA,
        'D_FLOW': D_FLOW,
        'A_0': A_0,
        'B_0': B_0,
        'EPSILON': EPSILON,
        'XI': XI,
        'DELTA': DELTA,
        'ALPHA_INV_PRED': ALPHA_INV_PRED,
        'MU_P_E_PRED': MU_P_E_PRED,
        'KAPPA_PRIME': KAPPA_PRIME,
        'MU_PRIME': MU_PRIME,
        'SCALE_RATIO': SCALE_RATIO
    }
    
    return results

def calculate_dH_shift(params, target_ratio, V_k, Chi_k):
    """
    Calculates the required Hausdorff dimension shift (Appendix B.3).
    Solves the Dynamic Mass Functional quadratic equation for E, then finds dH.
    (Implements the methodology of Appendix D.3)
    """
    KAPPA_PRIME = params['KAPPA_PRIME']
    MU_PRIME = params['MU_PRIME']
    SCALE_RATIO = params['SCALE_RATIO']
    V_M = params['V_M']
    N_CRIT = params['N_CRIT']

    # Calculate normalized electron mass (K=4_1, Chi=1)
    T_V_e = KAPPA_PRIME * V_M * SCALE_RATIO
    T_S_e = MU_PRIME * 1
    M_e_norm = T_V_e + T_S_e

    # Calculate terms for the target particle K
    T_V_k = KAPPA_PRIME * V_k * SCALE_RATIO
    T_S_k = MU_PRIME * Chi_k

    M_k_target = M_e_norm * target_ratio

    # Solve the quadratic equation: T_S_k * E^2 - M_k_target * E + T_V_k = 0
    a = T_S_k
    b = -M_k_target
    c = T_V_k

    Discriminant = b**2 - 4*a*c
    # Select the positive root for E>1
    E_k = (-b + mpmath.sqrt(Discriminant)) / (2*a)

    # Delta_dH = ln(E) / N_CRIT
    Delta_dH_Info = mpmath.ln(E_k) / N_CRIT
    return Delta_dH_Info, E_k

if __name__ == '__main__':
    # Execute calculations and print summary
    # Using 50 dps as used in the paper's validation
    params = calculate_utf_parameters(dps=50)
    
    print(f"UTF Core Calculations (Precision: {mpmath.mp.dps} d.p.)")
    print("-" * 40)
    print(f"N_CRIT (Critical Dim):  {params['N_CRIT']}")
    print(f"V_M (Volume of M):      {params['V_M']}")
    print(f"ETA (ZFP Impedance):    {params['ETA']}")
    print("-" * 40)
    print(f"XI (Correlation Slope): {params['XI']}")
    print(f"Alpha^-1 (Predicted):   {params['ALPHA_INV_PRED']}")
    print(f"Mu p/e (Predicted):     {params['MU_P_E_PRED']}")
    print("-" * 40)
    
    # Mass Hierarchy Example (Muon K=5_2) (Appendix B.3)
    # Using high-precision V(5_2) consistent with SnapPy/literature
    V_mu = mpmath.mpf("2.82812208833078364648431674386305795281099081748397")
    # Observed Ratio (Using value consistent with paper Appendix B)
    M_MU_E_RATIO_OBS = mpmath.mpf("206.77") 
    
    Delta_dH_mu, E_mu = calculate_dH_shift(params, M_MU_E_RATIO_OBS, V_mu, 1)
    print(f"Muon Enhancement (E):   {E_mu}")
    print(f"Muon Delta dH_Info:     {Delta_dH_mu}")