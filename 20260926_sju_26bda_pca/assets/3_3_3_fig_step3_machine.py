"""
3_3_3_fig_step3_machine.py
Step 3 of the Variance Machine Derivation:
The Matrix Substitution: Var(X_c * u) = u^T * Sigma * u
- Left Panel: The Continuous Variance Landscape: Var(theta) = 2.5 + 2.0*sin(2*theta)
              Shows PC1 peak (45°, 4.50), PC2 trough (135°, 0.50), and test u (15°, 3.50)
- Right Panel: 2D Data Cloud with Directional Variance Profile
               Shows data cloud with continuous standard deviation envelope r(theta) = sqrt(u^T * Sigma * u)
"""

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

assets_dir = os.path.dirname(os.path.abspath(__file__))
if assets_dir not in sys.path:
    sys.path.insert(0, assets_dir)
get_datasets = __import__("3_0_pca_data_helper").get_datasets

# Load exact 40-point dataset (Case 1: Positive Covariance)
X_pos, _, _ = get_datasets()
X_c = X_pos[:5]
cloud_c = X_pos[5:]

# Covariance matrix: [[2.5, 2.0], [2.0, 2.5]]
Sigma = np.array([[2.5, 2.0],
                  [2.0, 2.5]])

# Angle grid
theta_deg = np.linspace(0, 180, 500)
theta_rad = np.radians(theta_deg)

# Variance along each angle: u(theta)^T * Sigma * u(theta)
# u = [cos theta, sin theta]
# Var(theta) = 2.5 + 2.0 * sin(2*theta)
var_curve = 2.5 + 2.0 * np.sin(2 * theta_rad)

# Colors
COLOR_DATA = '#1976d2'     # Blue
COLOR_CLOUD = '#90caf9'    # Soft blue
COLOR_PC1 = '#d32f2f'      # Red for PC1
COLOR_PC2 = '#2e7d32'      # Green for PC2
COLOR_TEST = '#e65100'     # Orange for test direction (15°)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=300)
fig.patch.set_facecolor('#ffffff')

for ax in (ax1, ax2):
    ax.set_facecolor('#fafbfc')
    for spine in ax.spines.values():
        spine.set_edgecolor('#b0bec5')

# ==============================================================================
# --- LEFT PANEL: Variance vs Orientation Angle ---
# ==============================================================================
ax1.set_title(r'Step 3: The Variance Landscape $\text{Var}(\mathbf{u}) = \mathbf{u}^T \mathbf{\Sigma} \mathbf{u}$',
              fontsize=12.0, fontweight='bold', pad=12, color='#263238')
ax1.set_xlabel(r'Orientation Angle $\theta$ of Direction Vector $\mathbf{u}$', fontsize=11)
ax1.set_ylabel(r'Projected Variance $\mathbf{u}^T \mathbf{\Sigma} \mathbf{u}$', fontsize=11)
ax1.set_xlim(0, 180)
ax1.set_ylim(0, 5.2)
ax1.xaxis.set_major_locator(ticker.MultipleLocator(30))
ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax1.grid(True, linestyle='--', alpha=0.4, color='#cfd8dc')

# Plot continuous variance curve
ax1.plot(theta_deg, var_curve, color='#37474f', linewidth=2.5, label=r'$\text{Var}(\theta) = 2.5 + 2.0\sin(2\theta)$')

# Fill area under curve
ax1.fill_between(theta_deg, 0, var_curve, color='#eceff1', alpha=0.5)

# Landmark 1: PC1 Peak (45°, 4.50)
ax1.plot(45, 4.5, marker='o', markersize=9, color=COLOR_PC1, zorder=6)
ax1.axvline(45, color=COLOR_PC1, linestyle=':', linewidth=1.4, alpha=0.7)
ax1.annotate('PC1 Maximum (45°)\n' + r'$\text{Var} = \lambda_1 = 4.50$',
             xy=(45, 4.5), xytext=(55, 4.6),
             arrowprops=dict(arrowstyle="->", color=COLOR_PC1, lw=1.3),
             fontsize=9, fontweight='bold', color=COLOR_PC1,
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffebee', edgecolor='#ef5350', alpha=0.9))

# Landmark 2: PC2 Trough (135°, 0.50)
ax1.plot(135, 0.5, marker='o', markersize=9, color=COLOR_PC2, zorder=6)
ax1.axvline(135, color=COLOR_PC2, linestyle=':', linewidth=1.4, alpha=0.7)
ax1.annotate('PC2 Minimum (135°)\n' + r'$\text{Var} = \lambda_2 = 0.50$',
             xy=(135, 0.5), xytext=(100, 1.2),
             arrowprops=dict(arrowstyle="->", color=COLOR_PC2, lw=1.3),
             fontsize=9, fontweight='bold', color=COLOR_PC2,
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#e8f5e9', edgecolor='#66bb6a', alpha=0.9))

# Landmark 3: Step 1 Test Angle (15°, 3.50)
ax1.plot(15, 3.5, marker='D', markersize=8, color=COLOR_TEST, zorder=6)
ax1.annotate('Test Vector (15°)\n' + r'$\text{Var} = 3.50$',
             xy=(15, 3.5), xytext=(18, 2.5),
             arrowprops=dict(arrowstyle="->", color=COLOR_TEST, lw=1.3),
             fontsize=8.5, fontweight='bold', color=COLOR_TEST,
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#fff3e0', edgecolor='#ffb74d', alpha=0.9))

# Landmark 4: Standard axes (0° and 90°)
ax1.plot([0, 90], [2.5, 2.5], marker='s', markersize=6, color='#546e7a', linestyle='none', zorder=5)
ax1.text(2, 2.65, r'Height Axis ($0^\circ, s_1^2 = 2.5$)', fontsize=8, color='#546e7a', fontweight='bold')
ax1.text(92, 2.65, r'Weight Axis ($90^\circ, s_2^2 = 2.5$)', fontsize=8, color='#546e7a', fontweight='bold')

ax1.legend(loc='lower left', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8.5)

# ==============================================================================
# --- RIGHT PANEL: 2D Space & Standard Deviation Envelope ---
# ==============================================================================
ax2.set_title(r'The 2D Directional Variance Envelope $\sigma(\mathbf{u}) = \sqrt{\mathbf{u}^T \mathbf{\Sigma} \mathbf{u}}$',
              fontsize=12.0, fontweight='bold', pad=12, color='#263238')
ax2.set_xlabel(r'Centered $x_1$ (Height deviation)', fontsize=11)
ax2.set_ylabel(r'Centered $x_2$ (Weight deviation)', fontsize=11)
ax2.set_xlim(-4.5, 4.5)
ax2.set_ylim(-4.5, 4.5)
ax2.axhline(0, color='#37474f', linewidth=1.2, zorder=2)
ax2.axvline(0, color='#37474f', linewidth=1.2, zorder=2)
ax2.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax2.grid(True, linestyle='--', alpha=0.4, color='#cfd8dc')
ax2.set_aspect('equal')

# Scatter 40 centered data points
ax2.scatter(cloud_c[:, 0], cloud_c[:, 1], color=COLOR_CLOUD, s=30, alpha=0.55, zorder=3, label='Cloud Points (N=35)')
ax2.scatter(X_c[:, 0], X_c[:, 1], color=COLOR_DATA, s=75, edgecolor='#0d47a1', zorder=4, label='Benchmark Points (N=5)')

# Directional envelope: r(theta) = sqrt(u^T * Sigma * u)
all_theta = np.linspace(0, 2*np.pi, 300)
r_env = np.sqrt(2.5 + 2.0 * np.sin(2 * all_theta))
env_x = r_env * np.cos(all_theta)
env_y = r_env * np.sin(all_theta)
ax2.plot(env_x, env_y, color='#d32f2f', linestyle='--', linewidth=2.0, alpha=0.85, label=r'Spread Envelope $\sigma(\mathbf{u})$')

# Draw PC1 and PC2 arrows
q1 = np.array([1.0, 1.0]) / np.sqrt(2)
q2 = np.array([-1.0, 1.0]) / np.sqrt(2)
u_test = np.array([np.cos(np.radians(15)), np.sin(np.radians(15))])

ax2.annotate('', xy=(q1[0]*np.sqrt(4.5), q1[1]*np.sqrt(4.5)), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_PC1, lw=3.0, mutation_scale=16), zorder=6)
ax2.text(q1[0]*np.sqrt(4.5) + 0.1, q1[1]*np.sqrt(4.5) - 0.2, r'PC1 ($\sigma = 2.12$)', color=COLOR_PC1, fontweight='bold', fontsize=9.5)

ax2.annotate('', xy=(q2[0]*np.sqrt(0.5), q2[1]*np.sqrt(0.5)), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_PC2, lw=2.5, mutation_scale=14), zorder=6)
ax2.text(q2[0]*np.sqrt(0.5) - 1.2, q2[1]*np.sqrt(0.5) + 0.2, r'PC2 ($\sigma = 0.71$)', color=COLOR_PC2, fontweight='bold', fontsize=9.5)

ax2.annotate('', xy=(u_test[0]*np.sqrt(3.5), u_test[1]*np.sqrt(3.5)), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_TEST, lw=2.5, mutation_scale=14), zorder=6)
ax2.text(u_test[0]*np.sqrt(3.5) + 0.1, u_test[1]*np.sqrt(3.5) + 0.1, r'$\mathbf{u}$ (15°)', color=COLOR_TEST, fontweight='bold', fontsize=9.5)

# Annotation box for Step 3
ax2.text(-4.2, 2.5,
         "The Variance Machine:\n"
         r"• $\text{Var}(\mathbf{X}_c \mathbf{u}) = \mathbf{u}^T \mathbf{\Sigma} \mathbf{u}$" + "\n"
         r"• $(1 \times 2) \times (2 \times 2) \times (2 \times 1) = (1 \times 1)$" + "\n"
         "• No re-projecting of 40 raw points!\n"
         r"• Continuous variance output for any $\mathbf{u}$",
         fontsize=8.2, bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#cfd8dc', alpha=0.95), zorder=8)

ax2.legend(loc='lower right', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8.2)

plt.tight_layout()
png_path = os.path.join(assets_dir, '3_3_3_fig_step3_machine.png')
plt.savefig(png_path, dpi=300)
print(f"Saved {png_path} successfully.")

# Standalone HTML (Plotly)
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Figure 3.3c: Step 3 - The Variance Machine</title>
  <script src="https://cdn.plot.ly/plotly-2.29.1.min.js"></script>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0; padding: 20px; background: #f8fafc; color: #1e293b;
    }}
    .container {{
      max-width: 1200px; margin: 0 auto; background: #ffffff;
      border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); padding: 24px;
    }}
    h1 {{ font-size: 22px; margin-top: 0; color: #0f172a; }}
    p {{ line-height: 1.6; color: #475569; font-size: 14px; }}
    .charts-row {{ display: flex; gap: 20px; margin-top: 15px; }}
    .chart-col {{ flex: 1; height: 500px; border: 1px solid #e2e8f0; border-radius: 8px; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Figure 3.3c: Step 3 — The Variance Machine: Var(X_c u) = uᵀΣu</h1>
    <p>
      <b>Left:</b> The continuous variance curve as direction <b>u(θ)</b> rotates from 0° to 180°. It peaks at θ = 45° with <b>λ₁ = 4.50 (PC1)</b> and troughs at θ = 135° with <b>λ₂ = 0.50 (PC2)</b>.<br>
      <b>Right:</b> The 2D spread envelope σ(u) = √(uᵀΣu) overlaid on the 40 centered data points. The compact 2×2 covariance matrix <b>Σ</b> instantaneously predicts spread in any direction.
    </p>
    <div class="charts-row">
      <div id="plot1" class="chart-col"></div>
      <div id="plot2" class="chart-col"></div>
    </div>
  </div>
  <script>
    const traceCurve = {{
      x: {theta_deg.tolist()}, y: {var_curve.tolist()},
      mode: 'lines', line: {{ color: '#37474f', width: 3 }}, name: 'Variance uᵀΣu'
    }};
    const tracePeak = {{
      x: [45], y: [4.5], mode: 'markers+text', text: ['PC1 Peak (4.50)'], textposition: 'top center',
      marker: {{ color: '#d32f2f', size: 10 }}, name: 'PC1 Peak (45°)'
    }};
    const traceTrough = {{
      x: [135], y: [0.5], mode: 'markers+text', text: ['PC2 Trough (0.50)'], textposition: 'bottom center',
      marker: {{ color: '#2e7d32', size: 10 }}, name: 'PC2 Trough (135°)'
    }};
    const traceTest = {{
      x: [15], y: [3.5], mode: 'markers+text', text: ['Test u (3.50)'], textposition: 'top right',
      marker: {{ color: '#e65100', size: 10, symbol: 'diamond' }}, name: 'Test u (15°)'
    }};

    Plotly.newPlot('plot1', [traceCurve, tracePeak, traceTrough, traceTest], {{
      title: 'Variance vs. Orientation Angle θ',
      xaxis: {{ range: [0, 180], dtick: 30, title: 'Orientation Angle θ (°)' }},
      yaxis: {{ range: [0, 5.2], dtick: 1, title: 'Projected Variance uᵀΣu' }},
      margin: {{ l: 50, r: 20, b: 50, t: 40 }}
    }}, {{responsive: true}});

    const traceCloud2 = {{
      x: {cloud_c[:, 0].tolist()}, y: {cloud_c[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#90caf9', size: 6, opacity: 0.6 }}, name: 'Cloud Points'
    }};
    const traceBench2 = {{
      x: {X_c[:, 0].tolist()}, y: {X_c[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#1976d2', size: 9 }}, name: 'Benchmark Points'
    }};
    const traceEnv = {{
      x: {env_x.tolist()}, y: {env_y.tolist()},
      mode: 'lines', line: {{ color: '#d32f2f', width: 2, dash: 'dash' }}, name: 'Spread Envelope σ(u)'
    }};

    Plotly.newPlot('plot2', [traceCloud2, traceBench2, traceEnv], {{
      title: '2D Spread Envelope σ(u) = √(uᵀΣu)',
      xaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 40, r: 20, b: 40, t: 40 }}
    }}, {{responsive: true}});
  </script>
</body>
</html>
"""

html_path = os.path.join(assets_dir, '3_3_3_fig_step3_machine.html')
with open(html_path, 'w') as f:
    f.write(html_content)
print(f"Saved {html_path} successfully.")
