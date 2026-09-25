"""
3_4_fig_pca_reduction.py
Visualizes Dimensionality Reduction & Information Retention:
- Left: 2D Space with PC1 (Red) and PC2 (Green) at 90°, showing drop errors e = (I - P)x
- Right: 1D Principal Component Representation (z_i = x_i^T * q1), retaining 90% of Total Variance
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

labels = ['A (+2,+1)', 'B (-2,-1)', 'C (+1,+2)', 'D (-1,-2)', 'E (0,0)']

# Principal Components
q1 = np.array([1.0, 1.0]) / np.sqrt(2)
q2 = np.array([-1.0, 1.0]) / np.sqrt(2)

# Projected 1D coordinates (scores): z = X @ q1
z_scores = X_c @ q1
z_cloud = cloud_c @ q1

# Reconstructed points in 2D: x_hat = z * q1
X_recon = np.outer(z_scores, q1)
cloud_recon = np.outer(z_cloud, q1)

# Colors
COLOR_DATA = '#1976d2'     # Medium blue for benchmark points
COLOR_CLOUD = '#90caf9'    # Soft blue for cloud
COLOR_PC1 = '#d32f2f'      # Red
COLOR_PC2 = '#2e7d32'      # Green
COLOR_DROP = '#ff9800'     # Amber/Orange for error drop lines
COLOR_RECON = '#d32f2f'    # Red diamonds for projected points

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
# --- LEFT: 2D Original Space with Projections ---
ax1.set_title(r'2D Original Space: Projections onto PC1 ($\mathbf{P} = \mathbf{q}_1\mathbf{q}_1^T$)',
              fontsize=12.5, fontweight='bold', pad=12, color='#263238')
ax1.set_xlabel(r'Centered $x_1$', fontsize=11)
ax1.set_ylabel(r'Centered $x_2$', fontsize=11)
ax1.set_xlim(-4.5, 4.5)
ax1.set_ylim(-4.5, 4.5)

# PC1 and PC2 lines
t_span = np.linspace(-4.5, 4.5, 50)
ax1.plot(t_span * q1[0], t_span * q1[1], color=COLOR_PC1, linestyle='-', linewidth=2.2, alpha=0.75, label=r'PC1 Axis ($y = x$, $\lambda_1 = 4.50$)')
ax1.plot(t_span * q2[0], t_span * q2[1], color=COLOR_PC2, linestyle='--', linewidth=1.5, alpha=0.6, label=r'PC2 Axis ($y = -x$, $\lambda_2 = 0.50$)')

# 35 Cloud points & reconstructions
ax1.scatter(cloud_c[:, 0], cloud_c[:, 1], color=COLOR_CLOUD, s=30, alpha=0.55, zorder=3, label='Cloud Points (N=35)')
ax1.scatter(cloud_recon[:, 0], cloud_recon[:, 1], color='#ef9a9a', s=25, marker='D', alpha=0.55, zorder=4)

# Orthogonal drop lines (error vectors e = (I - P)x) for 5 benchmark points
for pt, pt_p in zip(X_c, X_recon):
    ax1.plot([pt[0], pt_p[0]], [pt[1], pt_p[1]], color=COLOR_DROP, linestyle='-', linewidth=2.0, zorder=5)

ax1.scatter(X_c[:, 0], X_c[:, 1], color=COLOR_DATA, s=75, edgecolor='#0d47a1', zorder=6, label='Benchmark Points (N=5)')
ax1.scatter(X_recon[:, 0], X_recon[:, 1], color=COLOR_RECON, s=70, marker='D', edgecolor='#b71c1c', zorder=7, label='Reconstructed Shadows (on PC1)')

# 90° right-angle indicator
box_l = 0.4
p1 = box_l * q1
p2 = box_l * q1 + box_l * q2
p3 = box_l * q2
ax1.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color='#263238', linewidth=1.3, zorder=8)
ax1.text(0.05, 0.55, '90°', color='#263238', fontweight='bold', fontsize=9, zorder=9)

# Labels
ax1.text(q1[0]*2.4 + 0.15, q1[1]*2.4, r'$\mathbf{q}_1$ (PC1)', color=COLOR_PC1, fontweight='bold', fontsize=10.5, zorder=7)
ax1.text(q2[0]*1.4 - 0.75, q2[1]*1.4 + 0.1, r'$\mathbf{q}_2$ (PC2)', color=COLOR_PC2, fontweight='bold', fontsize=10.5, zorder=7)

ax1.text(-4.2, 2.5, "Reconstruction Error:\n• Drop error e = (I - P)x\n• Error length² = λ₂ = 0.50\n• Perpendicular to PC1",
         fontsize=8.5, bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#cfd8dc', alpha=0.92), zorder=8)

ax1.legend(loc='lower right', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8.2)

# --- RIGHT: 1D Reduced Coordinate Space ---
ax2.set_title(r'1D Reduced Coordinate Space ($z = \mathbf{x}^T \mathbf{q}_1$)',
              fontsize=12.5, fontweight='bold', pad=12, color='#263238')
ax2.set_xlabel('Principal Component 1 Score ($z_1$)', fontsize=11)
ax2.set_ylabel('(Dimension 2 Compressed Away)', fontsize=11)
ax2.set_xlim(-4.5, 4.5)
ax2.set_ylim(-4.5, 4.5)

# 1D line along horizontal axis
ax2.plot([-4.5, 4.5], [0, 0], color=COLOR_PC1, linestyle='-', linewidth=2.8, alpha=0.8, label='1D Reduced Axis (PC1)')

# 1D cloud points on horizontal axis
ax2.scatter(z_cloud, np.zeros_like(z_cloud), color='#ef9a9a', s=35, marker='D', alpha=0.55, zorder=5, label='Cloud Scores (N=35)')

# 1D benchmark points on horizontal axis
ax2.scatter(z_scores, np.zeros_like(z_scores), color=COLOR_RECON, s=85, marker='D', edgecolor='#b71c1c', zorder=6, label='Benchmark Scores (N=5)')

# Point labels
z_labels = ['A (+2.12)', 'B (-2.12)', 'C (+2.12)', 'D (-2.12)', 'E (0.00)']
for z_val, lbl in zip(z_scores, z_labels):
    offset_y = 0.4 if z_val >= 0 else -0.5
    ax2.text(z_val - 0.5, offset_y, lbl, fontsize=9.5, fontweight='bold', color='#b71c1c', zorder=7)

# Variance summary box
ax2.text(-4.2, 2.2, "Dimensionality Reduction Results:\n• Compressed 2D data down to 1D\n• Captured Variance: λ₁ = 4.50 (90.0%)\n• Discarded Variance: λ₂ = 0.50 (10.0%)\n• Information Preserved: 90.0%!",
         fontsize=8.5, bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#cfd8dc', alpha=0.92), zorder=8)

ax2.legend(loc='lower right', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8.2)

plt.tight_layout()
png_path = os.path.join(assets_dir, '3_4_fig_pca_reduction.png')
plt.savefig(png_path, dpi=300)
print(f"Saved {png_path} successfully.")

# Standalone HTML (Plotly)
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Figure 3.4: PCA Dimensionality Reduction (2D to 1D)</title>
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
    .charts-row {{ display: flex; gap: 15px; margin-top: 15px; }}
    .chart-col {{ flex: 1; height: 500px; border: 1px solid #e2e8f0; border-radius: 8px; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Figure 3.4: PCA Dimensionality Reduction & Information Retention</h1>
    <p>
      <b>Left:</b> The 2D data points (N=40) are projected orthogonally onto <b>PC1 (Red, y = x)</b>. 
      The orange lines represent the reconstruction error vectors <b>e = (I - P)x</b> (from Section 1.6).<br>
      <b>Right:</b> The 1D compressed scores <b>z = xᵀq₁</b>. 
      Retaining only this single 1D coordinate captures <b>90% of the total variance</b> (λ₁ = 4.50 out of 5.00), while losing only 10% (λ₂ = 0.50).
    </p>
    <div class="charts-row">
      <div id="plot1" class="chart-col"></div>
      <div id="plot2" class="chart-col"></div>
    </div>
  </div>
  <script>
    const traceCloud2D = {{
      x: {cloud_c[:, 0].tolist()}, y: {cloud_c[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#90caf9', size: 6, opacity: 0.6 }}, name: 'Cloud Points (N=35)'
    }};
    const trace2DPts = {{
      x: {X_c[:, 0].tolist()}, y: {X_c[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#1976d2', size: 9 }}, name: 'Benchmark Points (N=5)'
    }};
    const traceRecon = {{
      x: {X_recon[:, 0].tolist()}, y: {X_recon[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#d32f2f', size: 9, symbol: 'diamond' }}, name: 'Projected on PC1'
    }};
    const tracePC1Line = {{
      x: [-4.5 * q1[0], 4.5 * q1[0]], y: [-4.5 * q1[1], 4.5 * q1[1]],
      mode: 'lines', line: {{ color: '#d32f2f', width: 3 }}, name: 'PC1 Axis (λ₁ = 4.50)'
    }};
    const tracePC2Line = {{
      x: [-3 * q2[0], 3 * q2[0]], y: [-3 * q2[1], 3 * q2[1]],
      mode: 'lines', line: {{ color: '#2e7d32', width: 2, dash: 'dash' }}, name: 'PC2 Axis (λ₂ = 0.50)'
    }};

    Plotly.newPlot('plot1', [traceCloud2D, trace2DPts, traceRecon, tracePC1Line, tracePC2Line], {{
      title: '2D Space: Projections onto PC1',
      xaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 40, r: 20, b: 40, t: 40 }}, showlegend: false
    }}, {{responsive: true}});

    const trace1DCloud = {{
      x: {z_cloud.tolist()}, y: {np.zeros_like(z_cloud).tolist()},
      mode: 'markers', marker: {{ color: '#ef9a9a', size: 6, opacity: 0.6, symbol: 'diamond' }}, name: 'Cloud Scores (N=35)'
    }};
    const trace1DPts = {{
      x: {z_scores.tolist()}, y: [0, 0, 0, 0, 0],
      mode: 'markers+text', text: ['A (+2.12)', 'B (-2.12)', 'C (+2.12)', 'D (-2.12)', 'E (0)'],
      textposition: 'top center', marker: {{ color: '#d32f2f', size: 10, symbol: 'diamond' }}, name: 'Benchmark Scores (N=5)'
    }};
    const trace1DAxis = {{
      x: [-4.5, 4.5], y: [0, 0],
      mode: 'lines', line: {{ color: '#d32f2f', width: 3 }}, name: '1D PC1 Axis'
    }};

    Plotly.newPlot('plot2', [trace1DAxis, trace1DCloud, trace1DPts], {{
      title: '1D Reduced Space (z = xᵀq₁)',
      xaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      yaxis: {{ range: [-2.0, 2.0], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 40, r: 20, b: 40, t: 40 }}, showlegend: false
    }}, {{responsive: true}});
  </script>
</body>
</html>
"""

html_path = os.path.join(assets_dir, '3_4_fig_pca_reduction.html')
with open(html_path, 'w') as f:
    f.write(html_content)
print(f"Saved {html_path} successfully.")
