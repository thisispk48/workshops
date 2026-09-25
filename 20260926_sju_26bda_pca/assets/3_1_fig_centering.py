"""
3_1_fig_centering.py
Visualizes Data Centering:
- Left: Raw Data Space with non-zero center of mass mu = [4, 3]
- Right: Centered Data Space R^2 anchored at origin (0, 0)
Standardized Visual Scheme:
- Neutral grey grid on both panels
- Tick intervals of 1
- Tracks 5 concrete benchmark points
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

# Load exact 40-point datasets
X_pos, _, _ = get_datasets()

mu = np.array([4.0, 3.0])
# 5 Concrete benchmark points
X_c = X_pos[:5]
X_raw = X_c + mu

# Remaining 35 points of the cloud
cloud_c = X_pos[5:]
cloud_raw = cloud_c + mu

# Colors
COLOR_RAW = '#455a64'      # Slate grey for raw cloud
COLOR_CENTERED = '#1976d2' # Medium blue for centered cloud
COLOR_MEAN = '#d32f2f'     # Red for mean vector
COLOR_GRID = '#e0e0e0'     # Neutral grey grid

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

# --- LEFT: Raw Data Space ---
ax1.set_title(r'Raw Data Space (Shifted Mean $\mathbf{\mu} = [4, 3]^T$)', fontsize=12.5, fontweight='bold', pad=12, color='#263238')
ax1.set_xlabel('Height ($x_1$)', fontsize=11)
ax1.set_ylabel('Weight ($x_2$)', fontsize=11)
ax1.set_xlim(-1.5, 8.5)
ax1.set_ylim(-1.5, 7.5)

# Background cloud
ax1.scatter(cloud_raw[:, 0], cloud_raw[:, 1], color='#b0bec5', s=30, alpha=0.6, zorder=3)

# 5 Benchmark points
ax1.scatter(X_raw[:, 0], X_raw[:, 1], color=COLOR_RAW, s=70, edgecolor='#263238', linewidth=1.2, zorder=5, label='Raw Data Points')
point_labels = ['A (6,4)', 'B (2,2)', 'C (5,5)', 'D (3,1)', 'E (4,3)']
for pt, lbl in zip(X_raw, point_labels):
    ax1.text(pt[0] + 0.18, pt[1] + 0.18, lbl, fontsize=9, fontweight='bold', color='#263238', zorder=6)

# Mean vector arrow
ax1.annotate('', xy=(mu[0], mu[1]), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_MEAN, lw=3.0, mutation_scale=18), zorder=7)
ax1.scatter([mu[0]], [mu[1]], color=COLOR_MEAN, s=90, zorder=8)
ax1.text(mu[0] - 1.2, mu[1] + 0.4, r'$\mathbf{\mu} = [4, 3]^T$', fontsize=11, fontweight='bold', color=COLOR_MEAN, zorder=9)

ax1.legend(loc='upper left', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8.5)

# --- RIGHT: Centered Data Space ---
ax2.set_title(r'Centered Data Space $\mathbb{R}^2$ ($\mathbf{X}_c = \mathbf{X} - \mathbf{\mu}$)', fontsize=12.5, fontweight='bold', pad=12, color='#263238')
ax2.set_xlabel(r'Centered Height ($\tilde{x}_1 = x_1 - 4$)', fontsize=11)
ax2.set_ylabel(r'Centered Weight ($\tilde{x}_2 = x_2 - 3$)', fontsize=11)
ax2.set_xlim(-5.0, 5.0)
ax2.set_ylim(-4.5, 4.5)

# Centered background cloud
ax2.scatter(cloud_c[:, 0], cloud_c[:, 1], color='#90caf9', s=30, alpha=0.6, zorder=3)

# 5 Centered benchmark points
ax2.scatter(X_c[:, 0], X_c[:, 1], color=COLOR_CENTERED, s=70, edgecolor='#0d47a1', linewidth=1.2, zorder=5, label='Centered Points (Mean = [0,0])')
c_labels = ['A (+2,+1)', 'B (-2,-1)', 'C (+1,+2)', 'D (-1,-2)', 'E (0,0)']
for pt, lbl in zip(X_c, c_labels):
    ax2.text(pt[0] + 0.18, pt[1] + 0.18, lbl, fontsize=9, fontweight='bold', color='#0d47a1', zorder=6)

# Center of mass anchored at (0, 0)
ax2.scatter([0], [0], color=COLOR_MEAN, s=90, zorder=8)
ax2.text(0.2, -0.4, r'Mean $\mathbf{0} = [0, 0]^T$', fontsize=10, fontweight='bold', color=COLOR_MEAN, zorder=9)

# Note box
ax2.text(-4.7, 3.3, "Why Centering Matters:\n• Anchors center of mass at origin (0, 0)\n• Preserves exact shape and spread\n• Enables linear algebra operators T(0) = 0",
         fontsize=8.5, bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#cfd8dc', alpha=0.92), zorder=10)

ax2.legend(loc='lower right', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8.5)

plt.tight_layout()
png_path = os.path.join(assets_dir, '3_1_fig_centering.png')
plt.savefig(png_path, dpi=300)
print(f"Saved {png_path} successfully.")

# Standalone HTML (Plotly)
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Figure 3.1: Data Centering (Raw vs. Centered)</title>
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
    <h1>Figure 3.1: The Geometry of Data Centering</h1>
    <p>
      <b>Left:</b> The raw data cloud is offset with non-zero center of mass <b>μ = [4, 3]ᵀ</b>.<br>
      <b>Right:</b> Subtracting <b>μ</b> translates the entire cloud so its center of mass is anchored at <b>(0, 0)</b>. 
      The shape, distance, and spread of the data are identical, but now linear algebra operators can analyze the variation.
    </p>
    <div class="charts-row">
      <div id="plot1" class="chart-col"></div>
      <div id="plot2" class="chart-col"></div>
    </div>
  </div>
  <script>
    const traceRawCloud = {{
      x: {cloud_raw[:, 0].tolist()}, y: {cloud_raw[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#b0bec5', size: 6 }}, name: 'Raw Cloud'
    }};
    const traceRawPts = {{
      x: {X_raw[:, 0].tolist()}, y: {X_raw[:, 1].tolist()},
      mode: 'markers+text', text: ['A (6,4)', 'B (2,2)', 'C (5,5)', 'D (3,1)', 'E (4,3)'],
      textposition: 'top right', marker: {{ color: '#455a64', size: 10 }}, name: 'Benchmark Points'
    }};
    const traceMeanArrow = {{
      x: [0, 4], y: [0, 3], mode: 'lines+markers', line: {{ color: '#d32f2f', width: 3 }},
      marker: {{ size: [0, 10], color: '#d32f2f' }}, name: 'Mean μ = [4, 3]'
    }};

    Plotly.newPlot('plot1', [traceRawCloud, traceRawPts, traceMeanArrow], {{
      title: 'Raw Data Space',
      xaxis: {{ range: [-1.5, 8.5], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-1.5, 7.5], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 40, r: 20, b: 40, t: 40 }}, showlegend: false
    }}, {{responsive: true}});

    const traceCentCloud = {{
      x: {cloud_c[:, 0].tolist()}, y: {cloud_c[:, 1].tolist()},
      mode: 'markers', marker: {{ color: '#90caf9', size: 6 }}, name: 'Centered Cloud'
    }};
    const traceCentPts = {{
      x: {X_c[:, 0].tolist()}, y: {X_c[:, 1].tolist()},
      mode: 'markers+text', text: ['A (+2,+1)', 'B (-2,-1)', 'C (+1,+2)', 'D (-1,-2)', 'E (0,0)'],
      textposition: 'top right', marker: {{ color: '#1976d2', size: 10 }}, name: 'Centered Points'
    }};
    const traceOrigin = {{
      x: [0], y: [0], mode: 'markers', marker: {{ color: '#d32f2f', size: 10 }}, name: 'Origin (0,0)'
    }};

    Plotly.newPlot('plot2', [traceCentCloud, traceCentPts, traceOrigin], {{
      title: 'Centered Data Space R²',
      xaxis: {{ range: [-5.0, 5.0], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 40, r: 20, b: 40, t: 40 }}, showlegend: false
    }}, {{responsive: true}});
  </script>
</body>
</html>
"""

html_path = os.path.join(assets_dir, '3_1_fig_centering.html')
with open(html_path, 'w') as f:
    f.write(html_content)
print(f"Saved {html_path} successfully.")
