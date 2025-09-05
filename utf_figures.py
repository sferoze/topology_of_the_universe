# File: utf_figures.py
# Description: Generates figures for the UTF paper based on the core calculations.

import numpy as np
import matplotlib.pyplot as plt
import mpmath
import os

# Create the utf_figures directory if it doesn't exist
output_dir = "utf_figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# Import the core calculation module
try:
    import utf_core_calculations as utf_core
except ImportError:
    print("Error: utf_core_calculations.py not found. Cannot generate figures.")
    exit()

# Configuration for matplotlib style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'dejavuserif' # Ensures LaTeX-style rendering
plt.rcParams['figure.dpi'] = 150  # Higher resolution for saved figures

# Load constants using the core module
# We use 50 dps here to ensure consistency when converting mpf to float
params_mpf = utf_core.calculate_utf_parameters(dps=50)
# Convert mpf objects to standard floats for plotting compatibility
params = {k: float(v) for k, v in params_mpf.items() if isinstance(v, mpmath.ctx_mp_python.mpf)}

N_CRIT = params['N_CRIT']
DELTA_D = params['DELTA_D']

def plot_stability_criterion():
    """Figure 1: The Stability Criterion n-1 = ln(2n) (Sec 2.2.1)"""
    
    n = np.linspace(0.1, 4, 500)
    G_n = n - 1
    C_n = np.log(2 * n)

    plt.figure(figsize=(8, 5))
    plt.plot(n, G_n, label=r'Connectivity Gain $G(n) = n-1$', color='blue', linewidth=2)
    plt.plot(n, C_n, label=r'Descriptive Cost $C(n) = \ln(2n)$', color='red', linewidth=2)

    # Highlight intersections
    # n=1 (Trivial/Unstable)
    plt.scatter([1], [0], color='gray', zorder=5, label='Trivial Solution (n=1)')

    # n_crit (Stable Solution)
    plt.scatter([N_CRIT], [N_CRIT-1], color='black', zorder=5, s=80, facecolors='gold', edgecolors='k')
    plt.text(N_CRIT + 0.1, N_CRIT - 1.2, f'$n_{{crit}} \\approx {N_CRIT:.4f}$ (Stable)', fontsize=12, verticalalignment='top')

    plt.xlabel('Degrees of Freedom (n)', fontsize=12)
    plt.ylabel('Information (nats)', fontsize=12)
    plt.title('The Fundamental Stability Criterion', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.axhline(0, color='k', linewidth=0.5)
    plt.xlim(0, 4)
    plt.ylim(-1.5, 2.5)
    
    # Save the figure
    filepath = os.path.join(output_dir, "figure1_stability_criterion.png")
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close()  # Close to free memory
    print(f"Saved Figure 1: {filepath}")

def plot_rapid_convergence():
    """Figure 2: Rapid Convergence of Informational Freedom I(t) (Sec 5.4)"""
    
    # I(t) = I(0) * exp(-(N_CRIT*C0/k) * (exp(k*t) - 1))
    # Assuming C0=1, k=DeltaD, I(0)=1 (Appendix D.4)
    k = DELTA_D
    C_0 = 1
    
    t = np.linspace(0, 8, 500)
    factor = (N_CRIT * C_0) / k
    I_t = np.exp(-factor * (np.exp(k * t) - 1))

    # t_conv calculation (Appendix D.4)
    target_exponent = np.log(1e30) # ln(10^30)
    t_conv = (1/k) * np.log(1 + target_exponent * (k / (N_CRIT * C_0)))

    plt.figure(figsize=(8, 5))
    plt.semilogy(t, I_t, color='purple', linewidth=2)
    
    plt.axhline(1e-30, color='red', linestyle='--', label='Stability Threshold ($10^{-30}$)')
    plt.axvline(t_conv, color='black', linestyle=':')
    plt.text(t_conv + 0.1, 1e-1, f'$t_{{conv}} \\approx {t_conv:.4f}$', fontsize=12)

    plt.xlabel('Information-Theoretic Time (t)', fontsize=12)
    plt.ylabel(r'$\mathcal{I}(t) / \mathcal{I}(0)$ (Log Scale)', fontsize=12)
    plt.title('Rapid Convergence via Double Exponential Decay', fontsize=14)
    plt.legend()
    plt.grid(True, which="both", linestyle='--', alpha=0.6)
    plt.xlim(0, 8)
    plt.ylim(1e-35, 1)

    # Save the figure
    filepath = os.path.join(output_dir, "figure2_rapid_convergence.png")
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved Figure 2: {filepath}")

def plot_mass_hierarchy():
    """Figure 3: Lepton Mass Hierarchy Resolution (Data from Appendix B)"""
    
    # Observed Ratios (Using values consistent with Appendix B)
    ratios = [1, 206.77, 3477.23]
    labels = [r'Electron ($4_1$)', r'Muon ($5_2$)', r'Tau ($7_2$)']
    
    # Required Delta dH_Info (Calculated in Appendix B.3)
    # These values are derived by running the mass functional solver in utf_core_calculations.py
    # Using the high-precision results from that script for accuracy.
    dH_shifts = [0, 4.3982521124, 5.4520336351]

    plt.figure(figsize=(9, 6))
    
    # Plotting Mass Ratio vs dH_Info Shift
    plt.semilogy(dH_shifts, ratios, marker='o', linestyle='-', color='darkgreen', markersize=8)

    for i, label in enumerate(labels):
        plt.text(dH_shifts[i] + 0.1, ratios[i], label, fontsize=11, verticalalignment='center')

    # Highlighting the exponential dependency E = exp(n_crit * dH)
    plt.text(2.5, 1e4, r'Driven by $E(\Delta d_{H}) = e^{n_{crit} \cdot \Delta d_{H}}$', fontsize=12, color='darkgreen')

    plt.xlabel(r'Required Informational Hausdorff Dimension Shift ($\Delta d_{H,\mathrm{Info}}$)', fontsize=12)
    plt.ylabel(r'Mass Ratio ($m_X / m_e$) (Log Scale)', fontsize=12)
    plt.title('Lepton Mass Hierarchy via Fractal Dynamics', fontsize=14)
    plt.grid(True, which="both", linestyle='--', alpha=0.6)
    plt.xlim(-0.5, 6)
    plt.ylim(0.5, 1e5)

    # Save the figure
    filepath = os.path.join(output_dir, "figure3_mass_hierarchy.png")
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved Figure 3: {filepath}")

def generate_all_figures():
    """Generate and save all figures"""
    print(f"\nGenerating UTF figures in '{output_dir}' directory...")
    print("=" * 50)
    
    plot_stability_criterion()
    plot_rapid_convergence()
    plot_mass_hierarchy()
    
    print("=" * 50)
    print(f"All figures successfully saved to '{output_dir}' directory")
    print("\nGenerated files:")
    for filename in os.listdir(output_dir):
        if filename.endswith('.png'):
            filepath = os.path.join(output_dir, filename)
            size_kb = os.path.getsize(filepath) / 1024
            print(f"  - {filename} ({size_kb:.1f} KB)")

if __name__ == '__main__':
    generate_all_figures()