"""
3_3_1_fig_step1_projection.py
Step 1 of the Variance Machine Derivation:
Projecting all N=40 observations onto an arbitrary test direction u (theta = 15°)
- Centered 2D space with 35 cloud points + 5 benchmark points
- Perpendicular drop lines from all 40 points to the line u
- Resulting 1D shadow coordinates z_i = r_tilde_i^T * u along line u
- Matrix operation: z = X_c * u in R^40
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

# Test direction: theta = 15°
theta = np.radians(15.0)
u = np.array([np.cos(theta), np.sin(theta)])

# 1D shadow coordinates (scores): z = X @ u
z_bench = X_c @ u
pts_proj_bench = np.outer(z_bench, u)

z_cloud = cloud_c @ u
pts_proj_cloud = np.outer(z_cloud, u)

# Colors
COLOR_DATA = '#1976d2'     # Blue for benchmark points
COLOR_CLOUD = '#90caf9'    # Soft blue for cloud points
COLOR_U = '#e65100'        # Amber/Orange for direction line u
COLOR_DROP = '#9e9e9e'     # Grey for perpendicular drop lines

fig, ax = plt.subplots(figsize=(8.5, 7.5), dpi=300)
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#fafbfc')

ax.axhline(0, color='#37474f', linewidth=1.2, zorder=2)
ax.axvline(0, color='#37474f', linewidth=1.2, zorder=2)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax.grid(True, linestyle='--', alpha=0.4, color='#cfd8dc')
ax.set_aspect('equal')
for spine in ax.spines.values():
    spine.set_edgecolor('#b0bec5')

ax.set_title(r'Step 1: Projecting All 40 Observations onto Direction $\mathbf{u}$ ($\theta = 15^\circ$)',
             fontsize=12.5, fontweight='bold', pad=14, color='#263238')
ax.set_xlabel(r'Centered $x_1$ (Height deviation, cm)', fontsize=11)
ax.set_ylabel(r'Centered $x_2$ (Weight deviation, kg)', fontsize=11)
ax.set_xlim(-4.5, 4.5)
ax.set_ylim(-4.5, 4.5)

# Line of u
t_vals = np.linspace(-4.5, 4.5, 50)
ax.plot(t_vals * u[0], t_vals * u[1], color=COLOR_U, linestyle='-', linewidth=2.0, alpha=0.8,
        label=r'Line $\mathbf{u}$ ($\theta = 15^\circ$)')

# Arrow for unit vector u
ax.annotate('', xy=(u[0]*2.0, u[1]*2.0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=COLOR_U, lw=3.2, mutation_scale=18), zorder=6)
ax.text(u[0]*2.0 + 0.15, u[1]*2.0 + 0.1, r'$\mathbf{u} = [0.966, 0.259]^T$',
        color=COLOR_U, fontweight='bold', fontsize=10.5, zorder=7)

# Drop lines for 35 cloud points
for pt, pt_p in zip(cloud_c, pts_proj_cloud):
    ax.plot([pt[0], pt_p[0]], [pt[1], pt_p[1]], color=COLOR_DROP, linestyle=':', linewidth=0.9, alpha=0.6, zorder=3)

# Drop lines for 5 benchmark points
for pt, pt_p in zip(X_c, pts_proj_bench):
    ax.plot([pt[0], pt_p[0]], [pt[1], pt_p[1]], color='#e65100', linestyle='--', linewidth=1.4, zorder=3)

# Scatter points: 35 cloud points
ax.scatter(cloud_c[:, 0], cloud_c[:, 1], color=COLOR_CLOUD, s=35, alpha=0.6, zorder=4, label='Cloud Points (N=35)')
ax.scatter(pts_proj_cloud[:, 0], pts_proj_cloud[:, 1], color='#ffb74d', s=25, marker='D', alpha=0.6, zorder=4)

# Scatter points: 5 benchmark points
ax.scatter(X_c[:, 0], X_c[:, 1], color=COLOR_DATA, s=80, edgecolor='#0d47a1', zorder=5, label='Benchmark Points (N=5)')
ax.scatter(pts_proj_bench[:, 0], pts_proj_bench[:, 1], color=COLOR_U, s=70, marker='D', edgecolor='#bf360c', zorder=6,
           label=r'Shadow Scores $\mathbf{z} = \mathbf{X}_c \mathbf{u}$')

# Benchmark callouts
labels = [
    ('Person A (+2, +1)', pts_proj_bench[0], (1.2, -0.6)),
    ('Person B (-2, -1)', pts_proj_bench[1], (-1.8, 0.5)),
    ('Person C (+1, +2)', pts_proj_bench[2], (0.5, 0.8)),
    ('Person D (-1, -2)', pts_proj_bench[3], (-1.5, -0.8)),
    ('Person E (0, 0)', pts_proj_bench[4], (0.4, -0.4))
]
for name, pt, offset in labels:
    ax.annotate(f"{name}\n$z = {pt[0]/u[0]:.2f}$", xy=(pt[0], pt[1]),
                xytext=(pt[0] + offset[0], pt[1] + offset[1]),
                arrowprops=dict(arrowstyle="->", color='#37474f', lw=1.0),
                fontsize=8.0, fontweight='bold', color='#263238',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor='#b0bec5', alpha=0.9))

# Mathematical annotation box
ax.text(-4.2, 2.5,
        "Mathematical Operation:\n"
        r"• Individual score: $z_i = \tilde{\mathbf{r}}_i^T \mathbf{u} \in \mathbb{R}$ (Scalar)" + "\n"
        r"  $(1 \times 2) \times (2 \times 1) = (1 \times 1)$" + "\n"
        r"• Full dataset vector: $\mathbf{z} = \mathbf{X}_c \mathbf{u} \in \mathbb{R}^{40}$" + "\n"
        r"  $(40 \times 2) \times (2 \times 1) = (40 \times 1)$" + "\n"
        "• All 40 2D points cast 1D shadow coordinates onto line u",
        fontsize=8.5, bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffffff', edgecolor='#cfd8dc', alpha=0.95), zorder=8)

ax.legend(loc='lower right', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8.5)

plt.tight_layout()
png_path = os.path.join(assets_dir, '3_3_1_fig_step1_projection.png')
plt.savefig(png_path, dpi=300)
print(f"Saved {png_path} successfully.")

# Standalone HTML (Plotly)
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Figure 3.3a: Step 1 - Projecting All 40 Points onto Direction u</title>
  <script src="https://cdn.plot.ly/plotly-2.29.1.min.js"></script>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0; padding: 20px; background: #f8fafc; color: #1e293b;
    }}
    .container {{
      max-width: 900px; margin: 0 auto; background: #ffffff;
      border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); padding: 24px;
    }}
    h1 {{ font-size: 22px; margin-top: 0; color: #0f172a; }}
    p {{ line-height: 1.6; color: #475569; font-size: 14px; }}
    .chart {{ height: 600px; border: 1px solid #e2e8f0; border-radius: 8px; margin-top: 15px; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Figure 3.3a: Step 1 — Projecting All 40 Points onto Direction u</h1>
    <p>
      Each centered observation vector <b>r̃_i ∈ R²</b> drops perpendicularly onto the line <b>u</b> at θ = 15°.<br>
      The scalar dot product <b>z_i = r̃_iᵀ u</b> yields the 1D shadow coordinate. Stacking all 40 points gives the score vector <b>z = X_c u ∈ R⁴⁰</b>.
    </p>
    <div id="plot" class="chart"></div>
  </div>
  <script>
    const traceCloud = {{
      x: {cloud_c[:, 0].tolist()}, y: {cloud_c[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#90caf9', size: 7, opacity: 0.6 }}, name: 'Cloud Points (N=35)'
    }};
    const traceData = {{
      x: {X_c[:, 0].tolist()}, y: {X_c[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#1976d2', size: 10 }}, name: 'Benchmark Points (N=5)'
    }};
    const traceProjCloud = {{
      x: {pts_proj_cloud[:, 0].tolist()}, y: {pts_proj_cloud[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#ffb74d', size: 6, symbol: 'diamond', opacity: 0.7 }}, name: 'Cloud Shadows'
    }};
    const traceProjBench = {{
      x: {pts_proj_bench[:, 0].tolist()}, y: {pts_proj_bench[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#e65100', size: 9, symbol: 'diamond' }}, name: 'Benchmark Shadows (z = X_c u)'
    }};
    const traceLineU = {{
      x: [-4.5 * u[0], 4.5 * u[0]], y: [-4.5 * u[1], 4.5 * u[1]],
      mode: 'lines', line: {{ color: '#e65100', width: 2.5 }}, name: 'Line u (15°)'
    }};

    Plotly.newPlot('plot', [traceCloud, traceData, traceProjCloud, traceProjBench, traceLineU], {{
      title: 'Step 1: All 40 Observations Projected onto Direction u (θ = 15°)',
      xaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y', title: 'Centered x₁ (Height deviation)' }},
      yaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155', title: 'Centered x₂ (Weight deviation)' }},
      margin: {{ l: 50, r: 30, b: 50, t: 50 }}, showlegend: true, legend: {{ x: 0.7, y: 0.15 }}
    }}, {{responsive: true}});
  </script>
</body>
</html>
"""

html_path = os.path.join(assets_dir, '3_3_1_fig_step1_projection.html')
with open(html_path, 'w') as f:
    f.write(html_content)
print(f"Saved {html_path} successfully.")
