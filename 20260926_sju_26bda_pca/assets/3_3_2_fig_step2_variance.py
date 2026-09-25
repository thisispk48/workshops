"""
3_3_2_fig_step2_variance.py
Step 2 of the Variance Machine Derivation:
Calculating the 1D Variance of the Shadows along Line u (theta = 15°)
- Top Panel: The 1D line u isolated horizontally as a score axis (z in [-4.5, 4.5])
             Shows mean z_bar = 0 (fulcrum) and the 40 individual scores
- Bottom Panel: Squared deviations z_i^2 = (z_i - 0)^2 for each individual
                Sum of squares = z^T * z = 136.50
                Sample Variance = (1 / 39) * z^T * z = 3.50
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

# Test direction: theta = 15°
theta = np.radians(15.0)
u = np.array([np.cos(theta), np.sin(theta)])

# 1D shadow coordinates (scores): z = X @ u
z_all = X_pos @ u
z_bench = z_all[:5]
z_cloud = z_all[5:]

# Colors
COLOR_DATA = '#1976d2'     # Blue for benchmark points
COLOR_CLOUD = '#90caf9'    # Soft blue for cloud points
COLOR_U = '#e65100'        # Amber/Orange for direction line u
COLOR_MEAN = '#d32f2f'     # Red for mean line / fulcrum

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), dpi=300, gridspec_kw={'height_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')

for ax in (ax1, ax2):
    ax.set_facecolor('#fafbfc')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.grid(True, linestyle='--', alpha=0.4, color='#cfd8dc')
    for spine in ax.spines.values():
        spine.set_edgecolor('#b0bec5')

# ==============================================================================
# --- TOP PANEL: 1D Score Line with Center of Mass at Zero ---
# ==============================================================================
ax1.set_title(r'Step 2: 1D Distribution of Shadow Scores along Line $\mathbf{u}$ ($\bar{z} = 0$)',
              fontsize=12.0, fontweight='bold', pad=12, color='#263238')
ax1.set_xlabel(r'Shadow Coordinate $z_i = \tilde{\mathbf{r}}_i^T \mathbf{u}$', fontsize=11)
ax1.set_xlim(-4.5, 4.5)
ax1.set_ylim(-0.8, 1.2)
ax1.get_yaxis().set_visible(False)

# Draw baseline line
ax1.axhline(0, color=COLOR_U, linewidth=2.5, alpha=0.7, zorder=2)

# Mean marker (fulcrum at z = 0)
ax1.axvline(0, color=COLOR_MEAN, linestyle='--', linewidth=1.8, alpha=0.85, zorder=3)
ax1.plot(0, -0.25, marker='^', markersize=14, color=COLOR_MEAN, zorder=7)
ax1.text(0.1, -0.45, r'Center of Mass $\bar{z} = 0.0$', color=COLOR_MEAN, fontweight='bold', fontsize=9.5)

# Jitter for cloud points to show density
np.random.seed(42)
cloud_jitter = np.random.uniform(-0.15, 0.15, size=len(z_cloud))
ax1.scatter(z_cloud, cloud_jitter, color=COLOR_CLOUD, s=45, alpha=0.7, zorder=4, label='Cloud Scores (N=35)')

# Benchmark points on the line
bench_y = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
ax1.scatter(z_bench, bench_y, color=COLOR_DATA, s=90, edgecolor='#0d47a1', zorder=6, label='Benchmark Scores (N=5)')

# Labels for benchmark points
bench_labels = ['Person A (+2.19)', 'Person B (-2.19)', 'Person C (+1.48)', 'Person D (-1.48)', 'Person E (0.00)']
bench_offsets = [(0.1, 0.45), (-1.2, 0.45), (0.1, 0.25), (-1.2, 0.25), (0.1, 0.6)]
for lab, val, off in zip(bench_labels, z_bench, bench_offsets):
    ax1.annotate(lab, xy=(val, 0), xytext=(val + off[0], off[1]),
                 arrowprops=dict(arrowstyle="->", color='#37474f', lw=1.0),
                 fontsize=8.0, fontweight='bold', color='#263238',
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor='#b0bec5', alpha=0.9))

ax1.legend(loc='upper right', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8.5)

# ==============================================================================
# --- BOTTOM PANEL: Squared Deviations z_i^2 ---
# ==============================================================================
ax2.set_title(r'Contribution to Variance: Squared Deviations $z_i^2 = (z_i - \bar{z})^2$',
              fontsize=12.0, fontweight='bold', pad=12, color='#263238')
ax2.set_xlabel(r'Shadow Coordinate $z_i$', fontsize=11)
ax2.set_ylabel(r'Squared Deviation $z_i^2$', fontsize=11)
ax2.set_xlim(-4.5, 4.5)
ax2.set_ylim(0, 16)

# Plot parabola of squared deviation: y = x^2
x_curve = np.linspace(-4.5, 4.5, 100)
ax2.plot(x_curve, x_curve**2, color='#9e9e9e', linestyle=':', linewidth=1.5, alpha=0.7, label=r'Squared Error Curve $y = z^2$')

# Stems for 35 cloud points
for zi in z_cloud:
    ax2.plot([zi, zi], [0, zi**2], color='#ffb74d', linewidth=1.0, alpha=0.5, zorder=3)
ax2.scatter(z_cloud, z_cloud**2, color='#ff9800', s=30, alpha=0.7, zorder=4)

# Stems for 5 benchmark points
for zi in z_bench:
    ax2.plot([zi, zi], [0, zi**2], color='#d32f2f', linewidth=2.0, zorder=5)
ax2.scatter(z_bench, z_bench**2, color='#d32f2f', s=70, edgecolor='#b71c1c', zorder=6, label='Benchmark Points $z_i^2$')

# Annotation box for Step 2
ax2.text(-4.2, 8.5,
         "Variance Formula:\n"
         r"• Mean: $\bar{z} = \frac{1}{N}\sum z_i = 0.0$ (Strictly zero due to centering)" + "\n"
         r"• Sum of Squares: $\sum_{i=1}^{40} z_i^2 = \mathbf{z}^T \mathbf{z} = 136.50$" + "\n"
         r"• Sample Variance: $\text{Var}(\mathbf{z}) = \frac{1}{N-1} \mathbf{z}^T \mathbf{z} = \frac{136.50}{39} = \mathbf{3.50}$" + "\n"
         r"• Dimension Check: $\frac{1}{39} (1 \times 40) \times (40 \times 1) = (1 \times 1)$ Scalar",
         fontsize=8.5, bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffffff', edgecolor='#cfd8dc', alpha=0.95), zorder=8)

ax2.legend(loc='upper right', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8.5)

plt.tight_layout()
png_path = os.path.join(assets_dir, '3_3_2_fig_step2_variance.png')
plt.savefig(png_path, dpi=300)
print(f"Saved {png_path} successfully.")

# Standalone HTML (Plotly)
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Figure 3.3b: Step 2 - Calculating 1D Variance of Shadows</title>
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
    .chart {{ height: 550px; border: 1px solid #e2e8f0; border-radius: 8px; margin-top: 15px; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Figure 3.3b: Step 2 — Calculating 1D Variance of the Shadows</h1>
    <p>
      Because the data was centered, the average of all 40 shadow coordinates is strictly <b>z̄ = 0</b>.<br>
      The sample variance is simply the average squared distance from zero: <b>Var(z) = (1 / 39) * zᵀz = 136.50 / 39 = 3.50</b>.
    </p>
    <div id="plot" class="chart"></div>
  </div>
  <script>
    const traceCloud = {{
      x: {z_cloud.tolist()}, y: Array({len(z_cloud)}).fill(0),
      mode: 'markers', marker: {{ color: '#90caf9', size: 8, opacity: 0.6 }}, name: 'Cloud Scores (N=35)'
    }};
    const traceBench = {{
      x: {z_bench.tolist()}, y: Array({len(z_bench)}).fill(0),
      mode: 'markers', marker: {{ color: '#1976d2', size: 11 }}, name: 'Benchmark Scores (N=5)'
    }};
    const traceCurve = {{
      x: {x_curve.tolist()}, y: {(x_curve**2).tolist()},
      mode: 'lines', line: {{ color: '#9e9e9e', width: 1.5, dash: 'dot' }}, name: 'y = z²'
    }};
    const traceSqBench = {{
      x: {z_bench.tolist()}, y: {(z_bench**2).tolist()},
      mode: 'markers', marker: {{ color: '#d32f2f', size: 10 }}, name: 'Benchmark z²'
    }};

    Plotly.newPlot('plot', [traceCurve, traceCloud, traceBench, traceSqBench], {{
      title: 'Step 2: 1D Scores & Squared Deviations (Var = 3.50)',
      xaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155', title: '1D Coordinate z' }},
      yaxis: {{ range: [-0.5, 16], title: 'Squared Deviation z²' }},
      margin: {{ l: 50, r: 30, b: 50, t: 50 }}, showlegend: true
    }}, {{responsive: true}});
  </script>
</body>
</html>
"""

html_path = os.path.join(assets_dir, '3_3_2_fig_step2_variance.html')
with open(html_path, 'w') as f:
    f.write(html_content)
print(f"Saved {html_path} successfully.")
