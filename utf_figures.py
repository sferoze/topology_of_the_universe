#!/usr/bin/env python3
"""
UTF Visualizations - Publication-Ready Figures
===============================================
Generates the key figures demonstrating the UTF framework's mathematical structure.

Author: Feroze Shahpurwala
Date: September 3, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

# Set publication-quality defaults
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10

# Import our UTF calculations
from utf_core_calculations import UTFConstants, MassFunctional, ConstraintDynamics


def figure_1_stability_criterion():
    """
    Figure 1: The UTF Stability Criterion G(n) = C(n)
    Shows how the critical dimension emerges from balancing connectivity vs cost.
    This is THE fundamental equation from which everything else derives.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    n = np.linspace(0.2, 4, 1000)
    G_n = n - 1  # Connectivity gain (tree graph)
    C_n = np.log(2 * n)  # Descriptive cost (Kolmogorov complexity)
    
    # Plot the functions
    ax.plot(n, G_n, 'b-', linewidth=2.5, label='$G(n) = n - 1$ (Connectivity Gain)')
    ax.plot(n, C_n, 'orange', linewidth=2.5, label='$C(n) = \ln(2n)$ (Descriptive Cost)')
    
    # Mark critical points
    n_crit = 2.6783469900166606534
    ax.plot(n_crit, n_crit - 1, 'ro', markersize=10, zorder=5)
    ax.plot(1, 0, 'mo', markersize=8, zorder=5)
    
    # Add annotations
    ax.annotate(f'$n_{{crit}} \\approx 2.6783$', 
                xy=(n_crit, n_crit - 1), xytext=(n_crit + 0.3, n_crit - 0.5),
                fontsize=14, color='red',
                arrowprops=dict(arrowstyle='->', color='red', lw=1))
    
    ax.annotate('$n = 1$', 
                xy=(1, 0), xytext=(0.7, -0.3),
                fontsize=12, color='purple',
                arrowprops=dict(arrowstyle='->', color='purple', lw=1))
    
    # Styling
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
    ax.axvline(x=n_crit, color='red', linestyle=':', alpha=0.5)
    ax.set_xlabel('Effective Dimensionality $(n)$')
    ax.set_ylabel('Cost / Gain (Nats)')
    ax.set_title('UTF Stability Criterion: $G(n) = C(n)$')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 4)
    ax.set_ylim(-1, 2.5)
    
    plt.tight_layout()
    return fig


def figure_2_rapid_convergence():
    """
    Figure 2: Rapid Convergence of Informational Freedom I(t)
    Demonstrates the double exponential decay ensuring unique outcome.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    utf = UTFConstants()
    dynamics = ConstraintDynamics(utf)
    
    t = np.linspace(0, 8, 1000)
    I_ratio = dynamics.informational_freedom(t)
    
    # Use log scale for dramatic visualization
    ax.semilogy(t, I_ratio, 'purple', linewidth=3, label='Double Exponential Decay')
    
    # Mark convergence time
    t_conv = dynamics.convergence_time()
    ax.axvline(x=t_conv, color='red', linestyle='--', linewidth=2, 
               label=f'Stabilization ($t_{{conv}} \\approx {t_conv:.2f}$)')
    
    # Styling
    ax.set_xlabel('Information-Theoretic Time $(t)$')
    ax.set_ylabel('Normalized Freedom $\\mathcal{I}(t)/\\mathcal{I}(0)$ (Log Scale)')
    ax.set_title('Rapid Convergence of Informational Freedom $\\mathcal{I}(t)$')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')
    ax.set_xlim(0, 8)
    ax.set_ylim(1e-35, 1)
    
    plt.tight_layout()
    return fig


def figure_3_cross_correlation():
    """
    Figure 3: Cross-Constant Correlation (The Xi Slope)
    Shows the linear relationship between alpha and mass ratio deviations.
    This proves both constants emerge from the same underlying dynamics.
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    
    utf = UTFConstants()
    
    # Theoretical values
    A0 = utf.A0
    B0 = utf.B0
    alpha_inv_derived = utf.get_alpha_inverse()
    mu_derived = utf.get_mu_proton_electron()
    
    # Observed values
    alpha_inv_obs = 137.035999084
    mu_obs = 1836.15267343
    
    # Create coordinate arrays for the line
    alpha_range = np.array([137.035, 137.056])
    mu_line = B0 + utf.Xi * (alpha_range - A0)
    
    # Plot the theoretical line
    ax.plot(alpha_range, mu_line, 'k--', linewidth=2, 
            label=f'Derived Slope $\\Xi \\approx {utf.Xi:.4f}$')
    
    # Plot points
    ax.scatter([A0], [B0], s=200, c='blue', marker='s', 
               label=f'Bare Topological Values ($A_0, B_0$)', zorder=5)
    ax.scatter([alpha_inv_derived], [mu_derived], s=200, c='green', 
               label='Derived Physical Values (UTF)', zorder=5)
    ax.scatter([alpha_inv_obs], [mu_obs], s=150, c='red', marker='x', 
               label='Observed (CODATA)', zorder=5, linewidths=3)
    
    # Styling
    ax.set_xlabel('Fine Structure Constant $\\alpha^{-1}$')
    ax.set_ylabel('Proton-Electron Mass Ratio $\\mu_{p/e}$')
    ax.set_title('Cross-Constant Correlation: The $\\Xi$ Slope (P4)')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    # Set appropriate limits
    ax.set_xlim(137.033, 137.057)
    ax.set_ylim(1836.08, 1836.16)
    
    plt.tight_layout()
    return fig


def figure_4_mass_hierarchy():
    """
    Figure 4: Mass Hierarchy Resolution via Fractal Energy Reorganization
    Shows how energy transfers from volume to surface terms with increasing complexity.
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    
    utf = UTFConstants()
    mass_func = MassFunctional(utf)
    
    # Calculate masses for each generation
    particles = ['4_1', '5_2', '7_2']
    labels = ['$(4_1)$', '$(5_2)$', '$(7_2)$']
    ratios = [1.0, 206.77, 3477.23]
    
    # Get required delta_dH values
    delta_dH_values = [0]  # electron baseline
    for particle, ratio in zip(particles[1:], ratios[1:]):
        delta_dH, _ = mass_func.solve_for_delta_dH(particle, ratio)
        delta_dH_values.append(delta_dH)
    
    # Calculate volume and surface contributions
    volume_terms = []
    surface_terms = []
    
    for particle, delta_dH in zip(particles, delta_dH_values):
        knot = mass_func.knot_data[particle]
        vol_term = (mass_func.kappa_prime * knot['volume'] * 17.125 * 
                   mass_func.S_suppression(delta_dH))
        surf_term = mass_func.mu_prime * mass_func.E_enhancement(delta_dH)
        volume_terms.append(vol_term)
        surface_terms.append(surf_term)
    
    # Create bar chart with log scale
    x = np.arange(len(particles))
    width = 0.6
    
    # Stack the contributions
    bars1 = ax.bar(x, volume_terms, width, label='Volume Term (Suppressed by $S(d_H)$)',
                   color='lightblue', edgecolor='black')
    bars2 = ax.bar(x, surface_terms, width, bottom=volume_terms,
                   label='Surface Term (Enhanced by $E(d_H)$)', 
                   color='salmon', edgecolor='black')
    
    # Add mass ratio labels
    for i, (ratio, label) in enumerate(zip(ratios, labels)):
        total_height = volume_terms[i] + surface_terms[i]
        ax.text(i, total_height * 1.1, f'{ratio:.2f}', 
                ha='center', va='bottom', fontsize=12, fontweight='bold')
        ax.text(i, total_height * 0.5, f'$m_{{{label[1:-1]}}}/m_e$', 
                ha='center', va='center', fontsize=10)
    
    # Styling
    ax.set_yscale('log')
    ax.set_ylabel('Mass Normalized to Electron $(m/m_e)$')
    ax.set_title('Mass Hierarchy Resolution via Fractal Energy Reorganization')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(1e-5, 1e4)
    
    plt.tight_layout()
    return fig


def figure_5_iterative_folding_3d():
    """
    Figure 5: 3D Visualization of Iterative Constraint Propagation
    Shows the fractal folding mechanism as a complex dynamical system.
    """
    fig = plt.figure(figsize=(12, 10))
    
    # Create two subplots - 3D trajectory and 2D projection
    ax1 = fig.add_subplot(111, projection='3d')
    
    utf = UTFConstants()
    
    # Simulate the iterative map: z_{k+1} = z_k^2 + z_0 + ΔD·C_k
    n_iterations = 500
    z0 = complex(-0.7, 0.25)  # Initial condition related to holonomy
    
    # Generate trajectory
    trajectory = []
    z = z0
    for k in range(n_iterations):
        C_k = np.exp(k * utf.Delta_D / 100)  # Constraint growth
        z = z**2 + z0 + utf.Delta_D * C_k / 100
        
        # Add logarithmic step for visualization
        log_step = np.log(abs(z) + 1)
        trajectory.append([z.real, z.imag, log_step])
        
        # Check for divergence
        if abs(z) > 10:
            break
    
    trajectory = np.array(trajectory)
    
    # Color map based on iteration number
    colors = plt.cm.viridis(np.linspace(0, 1, len(trajectory)))
    
    # Plot the 3D trajectory
    for i in range(len(trajectory) - 1):
        ax1.plot(trajectory[i:i+2, 0], trajectory[i:i+2, 1], trajectory[i:i+2, 2],
                color=colors[i], alpha=0.8)
    
    # Add start and end markers
    ax1.scatter(*trajectory[0], s=100, c='yellow', marker='o', 
               edgecolors='black', linewidth=2, zorder=5)
    ax1.scatter(*trajectory[-1], s=100, c='red', marker='*', 
               edgecolors='black', linewidth=2, zorder=5)
    
    # Styling
    ax1.set_xlabel('Re(z)')
    ax1.set_ylabel('Im(z)')
    ax1.set_zlabel('log(|z| + 1) (Time)')
    ax1.set_title(f'3D Visualization of Iterative Constraint Propagation (Fractal Folding)\n'
                  f'$z_0 = ({z0.real:.1f} + {z0.imag:.2f}i)$')
    
    # Add text box with parameters
    textstr = 'Attractor Projection (Complex Plane)'
    ax1.text2D(0.65, 0.95, textstr, transform=ax1.transAxes,
              fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Set view angle for best visualization
    ax1.view_init(elev=20, azim=45)
    ax1.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def save_all_figures(save_dir='./utf_figures/'):
    """
    Generate and save all publication-ready figures.
    """
    import os
    os.makedirs(save_dir, exist_ok=True)
    
    print("Generating UTF Framework Figures...")
    print("=" * 50)
    
    figures = {
        'fig1_stability_criterion': figure_1_stability_criterion(),
        'fig2_rapid_convergence': figure_2_rapid_convergence(),
        'fig3_cross_correlation': figure_3_cross_correlation(),
        'fig4_mass_hierarchy': figure_4_mass_hierarchy(),
        'fig5_iterative_folding': figure_5_iterative_folding_3d()
    }
    
    for name, fig in figures.items():
        filepath = os.path.join(save_dir, f'{name}.png')
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filepath}")
        plt.close(fig)
    
    print("=" * 50)
    print("All figures generated successfully!")
    return figures


if __name__ == "__main__":
    # Generate all figures
    figures = save_all_figures()
    
    # Display them if running interactively
    plt.show()