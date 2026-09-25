"""
3_2_fig_covariance_quadrants.py
Visualizes the 3 Stories Told by the Covariance Matrix:
- Panel 1: Positive Covariance (Sigma_1 = [[2.5, +2.0], [+2.0, 2.5]]) -> Upward tilt along line y = x
- Panel 2: Negative Covariance (Sigma_2 = [[2.5, -2.0], [-2.0, 2.5]]) -> Downward tilt along line y = -x
- Panel 3: Zero Covariance (Sigma_3 = [[2.0, 0.0], [0.0, 2.0]]) -> Uncorrelated, no tilt (diagonal matrix)
Standardized Visual Scheme:
- Neutral grey grid on all 3 panels
- Tick intervals of 1
- Clear quadrant labels and tilt lines
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
X_pos, X_neg, X_zero = get_datasets()

# Dataset 1: Positive Covariance (+2.0)
X_c1 = X_pos[:5]
pts_pos = X_pos[5:]
cov_pos = np.array([[2.5, 2.0], [2.0, 2.5]])

# Dataset 2: Negative Covariance (-2.0)
X_c2 = X_neg[:5]
pts_neg = X_neg[5:]
cov_neg = np.array([[2.5, -2.0], [-2.0, 2.5]])

# Dataset 3: Zero Covariance (0.0)
X_c3 = X_zero[:5]
pts_zero = X_zero[5:]
cov_zero = np.array([[2.0, 0.0], [0.0, 2.0]])

# Colors
COLOR_POS = '#1976d2'      # Blue
COLOR_NEG = '#7b1fa2'      # Purple
COLOR_ZERO = '#00897b'     # Teal
COLOR_AXIS = '#37474f'

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6), dpi=300)
fig.patch.set_facecolor('#ffffff')

for ax in (ax1, ax2, ax3):
    ax.set_facecolor('#fafbfc')
    ax.axhline(0, color=COLOR_AXIS, linewidth=1.3, zorder=2)
    ax.axvline(0, color=COLOR_AXIS, linewidth=1.3, zorder=2)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.grid(True, linestyle='--', alpha=0.4, color='#cfd8dc')
    ax.set_aspect('equal')
    for spine in ax.spines.values():
        spine.set_edgecolor('#b0bec5')

t = np.linspace(-4.5, 4.5, 50)

# --- PANEL 1: Positive Covariance ---
ax1.set_title(r'Positive: $\mathbf{\Sigma}_1 = [[2.5, +2.0], [+2.0, 2.5]]$',
              fontsize=11.5, fontweight='bold', pad=12, color='#263238')
ax1.set_xlabel(r'Centered $x_1$ (Deviations)', fontsize=10.5)
ax1.set_ylabel(r'Centered $x_2$ (Deviations)', fontsize=10.5)
ax1.set_xlim(-4.8, 4.8)
ax1.set_ylim(-4.8, 4.8)

ax1.plot(t, t, color='#d32f2f', linestyle='--', linewidth=1.8, alpha=0.75, label='Spine of Spread (y = x)')
ax1.scatter(pts_pos[:, 0], pts_pos[:, 1], color='#90caf9', s=30, alpha=0.5, zorder=3)
ax1.scatter(X_c1[:, 0], X_c1[:, 1], color=COLOR_POS, s=65, edgecolor='#0d47a1', zorder=5, label='5 Data Points')

# Labels
ax1.text(2.0, 3.8, 'Q1: (+)(+) = +', fontsize=9.5, fontweight='bold', color='#1b5e20',
         bbox=dict(boxstyle='round,pad=0.25', facecolor='#e8f5e9', edgecolor='#a5d6a7', alpha=0.9))
ax1.text(-4.3, -4.0, 'Q3: (−)(−) = +', fontsize=9.5, fontweight='bold', color='#1b5e20',
         bbox=dict(boxstyle='round,pad=0.25', facecolor='#e8f5e9', edgecolor='#a5d6a7', alpha=0.9))

ax1.text(-4.5, 2.2, "Positive Cov (+2.0):\n• Q1 & Q3 dominate\n• Cloud tilts UPWARD\n• As Height ↑, Weight ↑",
         fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#cfd8dc', alpha=0.92), zorder=6)

ax1.legend(loc='lower right', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8)

# --- PANEL 2: Negative Covariance ---
ax2.set_title(r'Negative: $\mathbf{\Sigma}_2 = [[2.5, -2.0], [-2.0, 2.5]]$',
              fontsize=11.5, fontweight='bold', pad=12, color='#263238')
ax2.set_xlabel(r'Centered $x_1$ (Deviations)', fontsize=10.5)
ax2.set_ylabel(r'Centered $x_2$ (Deviations)', fontsize=10.5)
ax2.set_xlim(-4.8, 4.8)
ax2.set_ylim(-4.8, 4.8)

ax2.plot(t, -t, color='#2e7d32', linestyle='--', linewidth=1.8, alpha=0.75, label='Spine of Spread (y = -x)')
ax2.scatter(pts_neg[:, 0], pts_neg[:, 1], color='#ce93d8', s=30, alpha=0.5, zorder=3)
ax2.scatter(X_c2[:, 0], X_c2[:, 1], color=COLOR_NEG, s=65, edgecolor='#4a148c', zorder=5, label='5 Data Points')

# Labels
ax2.text(-4.3, 3.8, 'Q2: (−)(+) = −', fontsize=9.5, fontweight='bold', color='#b71c1c',
         bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffebee', edgecolor='#ef9a9a', alpha=0.9))
ax2.text(2.0, -4.0, 'Q4: (+)(−) = −', fontsize=9.5, fontweight='bold', color='#b71c1c',
         bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffebee', edgecolor='#ef9a9a', alpha=0.9))

ax2.text(-4.5, -3.2, "Negative Cov (-2.0):\n• Q2 & Q4 dominate\n• Cloud tilts DOWNWARD\n• As Elevation ↑, Temp ↓",
         fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#cfd8dc', alpha=0.92), zorder=6)

ax2.legend(loc='upper right', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8)

# --- PANEL 3: Zero Covariance ---
ax3.set_title(r'Zero Covariance: $\mathbf{\Sigma}_3 = [[2.0, 0.0], [0.0, 2.0]]$',
              fontsize=11.5, fontweight='bold', pad=12, color='#263238')
ax3.set_xlabel(r'Centered $x_1$ (Deviations)', fontsize=10.5)
ax3.set_ylabel(r'Centered $x_2$ (Deviations)', fontsize=10.5)
ax3.set_xlim(-4.8, 4.8)
ax3.set_ylim(-4.8, 4.8)

# Circular contour guide
theta_circ = np.linspace(0, 2*np.pi, 100)
ax3.plot(2.0 * np.cos(theta_circ), 2.0 * np.sin(theta_circ), color='#00897b', linestyle=':', linewidth=1.5, alpha=0.7, label='Un-tilted Contour')
ax3.scatter(pts_zero[:, 0], pts_zero[:, 1], color='#80cbc4', s=30, alpha=0.5, zorder=3)
ax3.scatter(X_c3[:, 0], X_c3[:, 1], color=COLOR_ZERO, s=65, edgecolor='#004d40', zorder=5, label='5 Data Points')

ax3.text(-4.5, 3.8, 'Symmetric Across Quadrants', fontsize=9.5, fontweight='bold', color='#004d40',
         bbox=dict(boxstyle='round,pad=0.25', facecolor='#e0f2f1', edgecolor='#80cbc4', alpha=0.9))

ax3.text(-4.5, -3.2, "Zero Covariance (0.0):\n• Cross-terms cancel out\n• NO TILT (Diagonal matrix)\n• Knowing x₁ tells nothing of x₂",
         fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#cfd8dc', alpha=0.92), zorder=6)

ax3.legend(loc='upper right', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8)

plt.tight_layout()
png_path = os.path.join(assets_dir, '3_2_fig_covariance_quadrants.png')
plt.savefig(png_path, dpi=300)
print(f"Saved {png_path} successfully.")

# Standalone HTML (Plotly 3-col)
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Figure 3.2: The Three Stories of Covariance</title>
  <script src="https://cdn.plot.ly/plotly-2.29.1.min.js"></script>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0; padding: 20px; background: #f8fafc; color: #1e293b;
    }}
    .container {{
      max-width: 1400px; margin: 0 auto; background: #ffffff;
      border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); padding: 24px;
    }}
    h1 {{ font-size: 22px; margin-top: 0; color: #0f172a; }}
    p {{ line-height: 1.6; color: #475569; font-size: 14px; }}
    .charts-row {{ display: flex; gap: 15px; margin-top: 15px; }}
    .chart-col {{ flex: 1; height: 460px; border: 1px solid #e2e8f0; border-radius: 8px; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Figure 3.2: The Three Stories Told by the Covariance Matrix</h1>
    <p>
      <b>Panel 1 (Positive Covariance, +2.0):</b> Products (+)(+) and (−)(−) in Q1/Q3 dominate; cloud tilts upward.<br>
      <b>Panel 2 (Negative Covariance, -2.0):</b> Products (−)(+) and (+)(−) in Q2/Q4 dominate; cloud tilts downward.<br>
      <b>Panel 3 (Zero Covariance, 0.0):</b> Products cancel across all quadrants; cloud has NO tilt (diagonal matrix).
    </p>
    <div class="charts-row">
      <div id="plot1" class="chart-col"></div>
      <div id="plot2" class="chart-col"></div>
      <div id="plot3" class="chart-col"></div>
    </div>
  </div>
  <script>
    const tracePos = {{ x: {pts_pos[:, 0].tolist()}, y: {pts_pos[:, 1].tolist()}, mode: 'markers', marker: {{ color: '#90caf9', size: 6 }}, name: 'Cloud' }};
    const ptsPos = {{ x: {X_c1[:, 0].tolist()}, y: {X_c1[:, 1].tolist()}, mode: 'markers', marker: {{ color: '#1976d2', size: 9 }}, name: '5 Points' }};
    const linePos = {{ x: [-4.5, 4.5], y: [-4.5, 4.5], mode: 'lines', line: {{ color: '#d32f2f', width: 2, dash: 'dash' }}, name: 'y = x' }};
    Plotly.newPlot('plot1', [tracePos, ptsPos, linePos], {{
      title: 'Positive Covariance (+2.0)',
      xaxis: {{ range: [-4.8, 4.8], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-4.8, 4.8], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 35, r: 15, b: 35, t: 40 }}, showlegend: false
    }}, {{responsive: true}});

    const traceNeg = {{ x: {pts_neg[:, 0].tolist()}, y: {pts_neg[:, 1].tolist()}, mode: 'markers', marker: {{ color: '#ce93d8', size: 6 }}, name: 'Cloud' }};
    const ptsNeg = {{ x: {X_c2[:, 0].tolist()}, y: {X_c2[:, 1].tolist()}, mode: 'markers', marker: {{ color: '#7b1fa2', size: 9 }}, name: '5 Points' }};
    const lineNeg = {{ x: [-4.5, 4.5], y: [4.5, -4.5], mode: 'lines', line: {{ color: '#2e7d32', width: 2, dash: 'dash' }}, name: 'y = -x' }};
    Plotly.newPlot('plot2', [traceNeg, ptsNeg, lineNeg], {{
      title: 'Negative Covariance (-2.0)',
      xaxis: {{ range: [-4.8, 4.8], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-4.8, 4.8], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 35, r: 15, b: 35, t: 40 }}, showlegend: false
    }}, {{responsive: true}});

    const traceZero = {{ x: {pts_zero[:, 0].tolist()}, y: {pts_zero[:, 1].tolist()}, mode: 'markers', marker: {{ color: '#80cbc4', size: 6 }}, name: 'Cloud' }};
    const ptsZero = {{ x: {X_c3[:, 0].tolist()}, y: {X_c3[:, 1].tolist()}, mode: 'markers', marker: {{ color: '#00897b', size: 9 }}, name: '5 Points' }};
    Plotly.newPlot('plot3', [traceZero, ptsZero], {{
      title: 'Zero Covariance (0.0)',
      xaxis: {{ range: [-4.8, 4.8], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-4.8, 4.8], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 35, r: 15, b: 35, t: 40 }}, showlegend: false
    }}, {{responsive: true}});
  </script>
</body>
</html>
"""

html_path = os.path.join(assets_dir, '3_2_fig_covariance_quadrants.html')
with open(html_path, 'w') as f:
    f.write(html_content)
print(f"Saved {html_path} successfully.")
