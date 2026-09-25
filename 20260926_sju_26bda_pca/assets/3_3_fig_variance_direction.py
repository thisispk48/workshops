"""
3_3_fig_variance_direction.py
Visualizes Variance Along a Direction: Var(X_c * u) = u^T * Sigma * u
- Left: Worst Direction q2 (PC2, Green at 135°) where points collapse into a dense clump:
        Var(Xq2) = lambda2 = 0.50 (Points collide, massive drop errors, distinction lost)
- Right: Optimal Direction q1 (PC1, Red at 45°) where spread is maximized:
         Var(Xq1) = lambda1 = 4.50 (90% of variance retained, minimal drop errors)
Standardized Visual Scheme:
- Neutral grey grid on both panels
- Tick intervals of 1
- PC1 in Red (#d32f2f), PC2 in Green (#2e7d32)
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
X_c = X_pos[:5]      # 5 benchmark points
cloud_c = X_pos[5:]  # 35 cloud points

# Covariance matrix: [[2.5, 2.0], [2.0, 2.5]]
Sigma = np.array([[2.5, 2.0],
                  [2.0, 2.5]])

# Principal Component directions
q1 = np.array([1.0, 1.0]) / np.sqrt(2)   # PC1 (Optimal, 45°)
q2 = np.array([-1.0, 1.0]) / np.sqrt(2)  # PC2 (Worst, 135°)

var_q1 = float(q1 @ Sigma @ q1) # 4.50
var_q2 = float(q2 @ Sigma @ q2) # 0.50

# Projections on PC2 (Worst Direction - Clumping)
z_q2_bench = X_c @ q2
pts_proj_q2_bench = np.outer(z_q2_bench, q2)

z_q2_cloud = cloud_c @ q2
pts_proj_q2_cloud = np.outer(z_q2_cloud, q2)

# Projections on PC1 (Optimal Direction - Max Spread)
z_q1_bench = X_c @ q1
pts_proj_q1_bench = np.outer(z_q1_bench, q1)

z_q1_cloud = cloud_c @ q1
pts_proj_q1_cloud = np.outer(z_q1_cloud, q1)

# Colors
COLOR_DATA = '#1976d2'     # Medium blue for benchmark points
COLOR_CLOUD = '#90caf9'    # Soft blue for cloud points
COLOR_PC1 = '#d32f2f'      # Red for PC1
COLOR_PC2 = '#2e7d32'      # Green for PC2
COLOR_DROP = '#9e9e9e'     # Grey for projection drop lines

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), dpi=300)
fig.patch.set_facecolor('#ffffff')

for ax in (ax1, ax2):
    ax.set_facecolor('#fafbfc')
    ax.axhline(0, color='#37474f', linewidth=1.2, zorder=2)
    ax.axvline(0, color='#37474f', linewidth=1.2, zorder=2)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.grid(True, linestyle='--', alpha=0.4, color='#cfd8dc')
    ax.set_aspect('equal')
    for spine in ax.spines.values():
        spine.set_edgecolor('#b0bec5')

# ==============================================================================
# --- LEFT: Worst Direction q2 (PC2: Dense Clump & Overlap) ---
# ==============================================================================
ax1.set_title(r'Worst Direction: $\mathbf{q}_2$ (PC2, $\theta = 135^\circ$ — Collapsed Clump)',
              fontsize=12.0, fontweight='bold', pad=12, color='#263238')
ax1.set_xlabel(r'Centered $x_1$ (Height deviation)', fontsize=11)
ax1.set_ylabel(r'Centered $x_2$ (Weight deviation)', fontsize=11)
ax1.set_xlim(-4.5, 4.5)
ax1.set_ylim(-4.5, 4.5)

# PC2 line
t_q = np.linspace(-4.5, 4.5, 50)
ax1.plot(t_q * q2[0], t_q * q2[1], color=COLOR_PC2, linestyle='-', linewidth=2.0, alpha=0.75, label=r'PC2 Line ($y = -x$, $\lambda_2 = 0.50$)')

# PC2 vector arrow
ax1.annotate('', xy=(q2[0]*1.8, q2[1]*1.8), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_PC2, lw=3.2, mutation_scale=18), zorder=6)
ax1.text(q2[0]*1.8 - 0.6, q2[1]*1.8 + 0.15, r'$\mathbf{q}_2$', color=COLOR_PC2, fontweight='bold', fontsize=11, zorder=7)

# Drop lines and projected points on PC2
for pt, pt_p in zip(X_c, pts_proj_q2_bench):
    ax1.plot([pt[0], pt_p[0]], [pt[1], pt_p[1]], color='#e65100', linestyle=':', linewidth=1.5, zorder=3)

# 35 cloud points & shadows on PC2
ax1.scatter(cloud_c[:, 0], cloud_c[:, 1], color=COLOR_CLOUD, s=30, alpha=0.55, zorder=4, label='Cloud Points (N=35)')
ax1.scatter(pts_proj_q2_cloud[:, 0], pts_proj_q2_cloud[:, 1], color='#a5d6a7', s=25, marker='D', alpha=0.55, zorder=4)

# 5 benchmark points & shadows
ax1.scatter(X_c[:, 0], X_c[:, 1], color=COLOR_DATA, s=75, edgecolor='#0d47a1', zorder=5, label='Benchmark Points (N=5)')
ax1.scatter(pts_proj_q2_bench[:, 0], pts_proj_q2_bench[:, 1], color=COLOR_PC2, s=65, marker='D', edgecolor='#1b5e20', zorder=6, label='Shadows on PC2 (Collapsed Clump)')

# Collision Callouts for Benchmark Points
ax1.annotate('A & D Collide\n(-0.71)', xy=(pts_proj_q2_bench[0, 0], pts_proj_q2_bench[0, 1]),
             xytext=(pts_proj_q2_bench[0, 0] + 0.8, pts_proj_q2_bench[0, 1] - 0.9),
             arrowprops=dict(arrowstyle="->", color='#b71c1c', lw=1.3),
             fontsize=8.5, fontweight='bold', color='#b71c1c',
             bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffebee', edgecolor='#ef5350', alpha=0.9))

ax1.annotate('B & C Collide\n(+0.71)', xy=(pts_proj_q2_bench[1, 0], pts_proj_q2_bench[1, 1]),
             xytext=(pts_proj_q2_bench[1, 0] - 1.8, pts_proj_q2_bench[1, 1] + 0.5),
             arrowprops=dict(arrowstyle="->", color='#b71c1c', lw=1.3),
             fontsize=8.5, fontweight='bold', color='#b71c1c',
             bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffebee', edgecolor='#ef5350', alpha=0.9))

# Annotation box for Left Panel
ax1.text(-4.2, 2.5, "Severe Information Loss (Dense Clump):\n• Var(Xq₂) = q₂ᵀΣq₂ = λ₂ = 0.50\n• 40 points crushed into narrow span [-1.38, +1.51]\n• Benchmark collision: A & D both get -0.71\n• Benchmark collision: B & C both get +0.71\n• Cannot distinguish individuals from 1D scores!",
         fontsize=8.2, bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#ef9a9a', alpha=0.95), zorder=8)

ax1.legend(loc='lower right', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8.2)

# ==============================================================================
# --- RIGHT: Optimal Direction q1 (PC1: Maximum Spread & Clear Distinction) ---
# ==============================================================================
ax2.set_title(r'Optimal Direction: $\mathbf{q}_1$ (PC1, $\theta = 45^\circ$ — Maximum Spread)',
              fontsize=12.0, fontweight='bold', pad=12, color='#263238')
ax2.set_xlabel(r'Centered $x_1$ (Height deviation)', fontsize=11)
ax2.set_ylabel(r'Centered $x_2$ (Weight deviation)', fontsize=11)
ax2.set_xlim(-4.5, 4.5)
ax2.set_ylim(-4.5, 4.5)

# PC1 axis line
ax2.plot(t_q * q1[0], t_q * q1[1], color=COLOR_PC1, linestyle='-', linewidth=2.0, alpha=0.75, label=r'PC1 Line ($y = x$, $\lambda_1 = 4.50$)')
ax2.plot(t_q * q2[0], t_q * q2[1], color=COLOR_PC2, linestyle='--', linewidth=1.2, alpha=0.45, label=r'PC2 Line ($y = -x$, $\lambda_2 = 0.50$)')

# Arrow for q1 and q2
ax2.annotate('', xy=(q1[0]*2.2, q1[1]*2.2), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_PC1, lw=3.2, mutation_scale=18), zorder=6)
ax2.annotate('', xy=(q2[0]*1.4, q2[1]*1.4), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_PC2, lw=2.4, mutation_scale=14), zorder=6)

# Drop lines and projected points on PC1
for pt, pt_p in zip(X_c, pts_proj_q1_bench):
    ax2.plot([pt[0], pt_p[0]], [pt[1], pt_p[1]], color=COLOR_DROP, linestyle=':', linewidth=1.4, zorder=3)

# 35 cloud points & shadows on PC1
ax2.scatter(cloud_c[:, 0], cloud_c[:, 1], color=COLOR_CLOUD, s=30, alpha=0.55, zorder=4, label='Cloud Points (N=35)')
ax2.scatter(pts_proj_q1_cloud[:, 0], pts_proj_q1_cloud[:, 1], color='#ef9a9a', s=25, marker='D', alpha=0.55, zorder=4)

# 5 benchmark points & shadows
ax2.scatter(X_c[:, 0], X_c[:, 1], color=COLOR_DATA, s=75, edgecolor='#0d47a1', zorder=5, label='Benchmark Points (N=5)')
ax2.scatter(pts_proj_q1_bench[:, 0], pts_proj_q1_bench[:, 1], color=COLOR_PC1, s=65, marker='D', edgecolor='#b71c1c', zorder=6, label='Shadows on PC1 (Max Spread)')

# 90° right-angle indicator
box_l = 0.4
p1 = box_l * q1
p2 = box_l * q1 + box_l * q2
p3 = box_l * q2
ax2.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color='#263238', linewidth=1.3, zorder=8)
ax2.text(0.05, 0.55, '90°', color='#263238', fontweight='bold', fontsize=9, zorder=9)

# Labels
ax2.text(q1[0]*2.2 + 0.15, q1[1]*2.2, r'$\mathbf{q}_1$ (PC1)', color=COLOR_PC1, fontweight='bold', fontsize=10.5, zorder=7)
ax2.text(q2[0]*1.4 - 0.7, q2[1]*1.4 + 0.1, r'$\mathbf{q}_2$ (PC2)', color=COLOR_PC2, fontweight='bold', fontsize=10.5, zorder=7)

# Annotation box for Right Panel
ax2.text(-4.2, 2.3, "Maximum Information Retained (Max Spread):\n• Var(Xq₁) = q₁ᵀΣq₁ = λ₁ = 4.50\n• Retains 90% of Total Variance (4.5 / 5.0)\n• Points spread widely across span [-4.59, +4.21]\n• Clear separation between individuals\n• Minimal drop errors (Pythagorean theorem)",
         fontsize=8.2, bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#a5d6a7', alpha=0.95), zorder=8)

ax2.legend(loc='lower right', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8.2)

plt.tight_layout()
png_path = os.path.join(assets_dir, '3_3_fig_variance_direction.png')
plt.savefig(png_path, dpi=300)
print(f"Saved {png_path} successfully.")

# Standalone HTML (Plotly)
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Figure 3.3: Worst Direction (PC2 Clump) vs. Optimal Direction (PC1 Spread)</title>
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
    <h1>Figure 3.3: Why Maximize Variance? Worst Line (PC2 Clumping) vs. Best Line (PC1 Spread)</h1>
    <p>
      <b>Left (Worst Direction - PC2 at 135°):</b> Points collapse into a dense, uninformative clump with <b>Var = λ₂ = 0.50</b>. Individuals collide (Person A & D both get -0.71; Person B & C both get +0.71), destroying individual distinguishability.<br>
      <b>Right (Optimal Direction - PC1 at 45°):</b> Data spreads widely across 9 units with <b>Var = λ₁ = 4.50</b> (retaining 90% of total variance). Every individual is distinctly separated with minimal error drop lines!
    </p>
    <div class="charts-row">
      <div id="plot1" class="chart-col"></div>
      <div id="plot2" class="chart-col"></div>
    </div>
  </div>
  <script>
    const traceCloudLeft = {{
      x: {cloud_c[:, 0].tolist()}, y: {cloud_c[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#90caf9', size: 6, opacity: 0.6 }}, name: 'Cloud Points (N=35)'
    }};
    const traceDataLeft = {{
      x: {X_c[:, 0].tolist()}, y: {X_c[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#1976d2', size: 9 }}, name: 'Benchmark Points (N=5)'
    }};
    const traceProjLeft = {{
      x: {pts_proj_q2_bench[:, 0].tolist()}, y: {pts_proj_q2_bench[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#2e7d32', size: 8, symbol: 'diamond' }}, name: 'Shadows on PC2'
    }};
    const traceLinePC2 = {{
      x: [-4.5 * q2[0], 4.5 * q2[0]], y: [-4.5 * q2[1], 4.5 * q2[1]],
      mode: 'lines', line: {{ color: '#2e7d32', width: 2.5 }}, name: 'PC2 Line (λ₂ = 0.50)'
    }};

    Plotly.newPlot('plot1', [traceCloudLeft, traceDataLeft, traceProjLeft, traceLinePC2], {{
      title: 'Worst Direction: PC2 Clump (Variance = 0.50)',
      xaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 40, r: 20, b: 40, t: 40 }}, showlegend: false
    }}, {{responsive: true}});

    const traceCloudRight = {{
      x: {cloud_c[:, 0].tolist()}, y: {cloud_c[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#90caf9', size: 6, opacity: 0.6 }}, name: 'Cloud Points (N=35)'
    }};
    const traceDataRight = {{
      x: {X_c[:, 0].tolist()}, y: {X_c[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#1976d2', size: 9 }}, name: 'Benchmark Points (N=5)'
    }};
    const traceProjRight = {{
      x: {pts_proj_q1_bench[:, 0].tolist()}, y: {pts_proj_q1_bench[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#d32f2f', size: 9, symbol: 'diamond' }}, name: 'Shadows on PC1'
    }};
    const tracePC1 = {{
      x: [-4.5 * q1[0], 4.5 * q1[0]], y: [-4.5 * q1[1], 4.5 * q1[1]],
      mode: 'lines', line: {{ color: '#d32f2f', width: 3 }}, name: 'PC1 (λ₁ = 4.50)'
    }};
    const tracePC2_dash = {{
      x: [-3 * q2[0], 3 * q2[0]], y: [-3 * q2[1], 3 * q2[1]],
      mode: 'lines', line: {{ color: '#2e7d32', width: 1.5, dash: 'dash' }}, name: 'PC2 (λ₂ = 0.50)'
    }};

    Plotly.newPlot('plot2', [traceCloudRight, traceDataRight, traceProjRight, tracePC1, tracePC2_dash], {{
      title: 'Optimal Direction: PC1 Spread (Variance = 4.50)',
      xaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 40, r: 20, b: 40, t: 40 }}, showlegend: false
    }}, {{responsive: true}});
  </script>
</body>
</html>
"""

html_path = os.path.join(assets_dir, '3_3_fig_variance_direction.html')
with open(html_path, 'w') as f:
    f.write(html_content)
print(f"Saved {html_path} successfully.")
