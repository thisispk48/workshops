"""
3_5_fig_pca_cases.py
Visualizes PCA Across the Three Covariance Cases (40 points each):
- Panel 1: Positive Covariance (Sigma_1 = [[2.5, +2.0], [+2.0, 2.5]])
           PC1 along y = x (45°, lambda_1 = 4.50, 90.0% variance)
           PC2 along y = -x (135°, lambda_2 = 0.50, 10.0% variance)
- Panel 2: Negative Covariance (Sigma_2 = [[2.5, -2.0], [-2.0, 2.5]])
           PC1 along y = -x (-45°, lambda_1 = 4.50, 90.0% variance) - Spine tilted 90°!
           PC2 along y = x (45°, lambda_2 = 0.50, 10.0% variance)
- Panel 3: Zero Covariance (Sigma_3 = [[2.0, 0.0], [0.0, 2.0]])
           Circular cloud, orthogonal axes with equal eigenvalues lambda_1 = lambda_2 = 2.00 (50.0% / 50.0%)
           No dominant spine!

Outputs:
- 3_5_fig_pca_cases.png (300 DPI)
- 3_5_fig_pca_cases.html (Interactive Plotly companion via CDN)
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

# Eigenvectors & Eigenvalues
# Case 1: Pos
cov_pos = np.array([[2.5, 2.0], [2.0, 2.5]])
q1_pos = np.array([1.0, 1.0]) / np.sqrt(2)
q2_pos = np.array([-1.0, 1.0]) / np.sqrt(2)
l1_pos, l2_pos = 4.50, 0.50

# Case 2: Neg
cov_neg = np.array([[2.5, -2.0], [-2.0, 2.5]])
q1_neg = np.array([1.0, -1.0]) / np.sqrt(2)
q2_neg = np.array([1.0, 1.0]) / np.sqrt(2)
l1_neg, l2_neg = 4.50, 0.50

# Case 3: Zero
cov_zero = np.array([[2.0, 0.0], [0.0, 2.0]])
q1_zero = np.array([1.0, 0.0])
q2_zero = np.array([0.0, 1.0])
l1_zero, l2_zero = 2.00, 2.00

# Colors
COLOR_PC1 = '#d32f2f'      # Red for PC1
COLOR_PC2 = '#2e7d32'      # Green for PC2
COLOR_BENCH = '#1565c0'    # Dark blue for 5 benchmark points
COLOR_CLOUD = '#90caf9'    # Soft blue for cloud points
COLOR_AXIS = '#37474f'

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6), dpi=300)
fig.patch.set_facecolor('#ffffff')

configs = [
    {
        'ax': ax1,
        'title': r'Case 1: Positive Covariance ($\mathbf{\Sigma}_1$)',
        'subtitle': r'Height vs. Weight ($\sigma_{12} = +2.0$)',
        'data': X_pos,
        'q1': q1_pos, 'q2': q2_pos,
        'l1': l1_pos, 'l2': l2_pos,
        'text': "PC1: y = x (45°)\n• λ₁ = 4.50 (90.0%)\n• λ₂ = 0.50 (10.0%)\n• Spine tilted up-right",
        'box_x': -4.2, 'box_y': 2.7
    },
    {
        'ax': ax2,
        'title': r'Case 2: Negative Covariance ($\mathbf{\Sigma}_2$)',
        'subtitle': r'Elevation vs. Temp ($\sigma_{12} = -2.0$)',
        'data': X_neg,
        'q1': q1_neg, 'q2': q2_neg,
        'l1': l1_neg, 'l2': l2_neg,
        'text': "PC1: y = -x (-45°)\n• λ₁ = 4.50 (90.0%)\n• λ₂ = 0.50 (10.0%)\n• Spine tilted down-right by 90°!",
        'box_x': -4.2, 'box_y': 2.7
    },
    {
        'ax': ax3,
        'title': r'Case 3: Zero Covariance ($\mathbf{\Sigma}_3$)',
        'subtitle': r'Uncorrelated Noise ($\sigma_{12} = 0.0$)',
        'data': X_zero,
        'q1': q1_zero, 'q2': q2_zero,
        'l1': l1_zero, 'l2': l2_zero,
        'text': "No Dominant Spine!\n• λ₁ = 2.00 (50.0%)\n• λ₂ = 2.00 (50.0%)\n• Circular spread in all directions",
        'box_x': -4.2, 'box_y': 2.7
    }
]

for cfg in configs:
    ax = cfg['ax']
    ax.set_facecolor('#fafbfc')
    ax.axhline(0, color=COLOR_AXIS, linewidth=1.2, zorder=2)
    ax.axvline(0, color=COLOR_AXIS, linewidth=1.2, zorder=2)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.grid(True, linestyle='--', alpha=0.4, color='#cfd8dc')
    ax.set_aspect('equal')
    for spine in ax.spines.values():
        spine.set_edgecolor('#b0bec5')

    ax.set_title(f"{cfg['title']}\n{cfg['subtitle']}", fontsize=11, fontweight='bold', pad=10, color='#263238')
    ax.set_xlabel('Centered Feature 1', fontsize=10)
    ax.set_ylabel('Centered Feature 2', fontsize=10)
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-4.5, 4.5)

    data = cfg['data']
    # 35 cloud points
    ax.scatter(data[5:, 0], data[5:, 1], color=COLOR_CLOUD, s=35, alpha=0.65, zorder=3, label='Cloud Points (N=35)')
    # 5 benchmark points
    ax.scatter(data[:5, 0], data[:5, 1], color=COLOR_BENCH, s=65, edgecolor='#0d47a1', zorder=5, label='Benchmark Points (N=5)')

    # Axes lines
    t = np.linspace(-4.5, 4.5, 50)
    q1, q2 = cfg['q1'], cfg['q2']
    ax.plot(t * q1[0], t * q1[1], color=COLOR_PC1, linestyle='-', linewidth=1.8, alpha=0.7)
    ax.plot(t * q2[0], t * q2[1], color=COLOR_PC2, linestyle='--', linewidth=1.4, alpha=0.6)

    # Vector arrows scaled by standard deviation sqrt(lambda)
    scale1 = np.sqrt(cfg['l1']) * 1.2
    scale2 = np.sqrt(cfg['l2']) * 1.2
    ax.annotate('', xy=(q1[0] * scale1, q1[1] * scale1), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_PC1, lw=3.0, mutation_scale=16), zorder=7)
    ax.annotate('', xy=(q2[0] * scale2, q2[1] * scale2), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_PC2, lw=2.4, mutation_scale=14), zorder=7)

    # Arrow labels
    ax.text(q1[0] * scale1 + 0.15, q1[1] * scale1 + 0.15, r'$\mathbf{q}_1$ (PC1)', color=COLOR_PC1, fontweight='bold', fontsize=9.5, zorder=8)
    ax.text(q2[0] * scale2 + 0.15, q2[1] * scale2 + 0.15, r'$\mathbf{q}_2$ (PC2)', color=COLOR_PC2, fontweight='bold', fontsize=9.5, zorder=8)

    # 90° right angle marker
    box_l = 0.35
    p1 = box_l * q1
    p2 = box_l * q1 + box_l * q2
    p3 = box_l * q2
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color='#263238', linewidth=1.2, zorder=6)

    # Text box
    ax.text(cfg['box_x'], cfg['box_y'], cfg['text'], fontsize=8.2,
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#cfd8dc', alpha=0.92), zorder=8)

    ax.legend(loc='lower right', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=7.5)

plt.tight_layout()
png_path = os.path.join(assets_dir, '3_5_fig_pca_cases.png')
plt.savefig(png_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved {png_path} successfully.")

# --- Generate Interactive Plotly HTML via CDN ---
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Figure 3.5: Principal Components Across Three Covariance Cases</title>
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
    <h1>Figure 3.5: Principal Components Across Three Covariance Cases</h1>
    <p>
      <b>Panel 1 (Positive Covariance, +2.0):</b> PC1 along y = x (45°), capturing 90.0% of total variance (λ₁ = 4.50). PC2 captures 10.0% (λ₂ = 0.50).<br>
      <b>Panel 2 (Negative Covariance, -2.0):</b> PC1 along y = -x (-45°), capturing 90.0% of total variance (λ₁ = 4.50). The spine has tilted 90°!<br>
      <b>Panel 3 (Zero Covariance, 0.0):</b> Both orthogonal axes have equal eigenvalues (λ₁ = λ₂ = 2.00, 50.0% / 50.0%). There is NO single dominant spine!
    </p>
    <div class="charts-row">
      <div id="plot1" class="chart-col"></div>
      <div id="plot2" class="chart-col"></div>
      <div id="plot3" class="chart-col"></div>
    </div>
  </div>
  <script>
    // Panel 1: Positive Covariance
    const tPosCloud = {{ x: {X_pos[5:, 0].tolist()}, y: {X_pos[5:, 1].tolist()}, mode: 'markers', marker: {{ color: '#90caf9', size: 6 }}, name: 'Cloud Points (N=35)' }};
    const tPosBench = {{ x: {X_pos[:5, 0].tolist()}, y: {X_pos[:5, 1].tolist()}, mode: 'markers', marker: {{ color: '#1565c0', size: 9 }}, name: 'Benchmark Points (N=5)' }};
    const tPosPC1 = {{ x: [-4.2, 4.2], y: [-4.2, 4.2], mode: 'lines', line: {{ color: '#d32f2f', width: 2.5 }}, name: 'PC1 (λ₁ = 4.50, 90%)' }};
    const tPosPC2 = {{ x: [3.0, -3.0], y: [-3.0, 3.0], mode: 'lines', line: {{ color: '#2e7d32', width: 2, dash: 'dash' }}, name: 'PC2 (λ₂ = 0.50, 10%)' }};
    Plotly.newPlot('plot1', [tPosCloud, tPosBench, tPosPC1, tPosPC2], {{
      title: 'Positive Covariance: Up-Right Spine',
      xaxis: {{ range: [-4.8, 4.8], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-4.8, 4.8], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 35, r: 15, b: 35, t: 40 }}, showlegend: false
    }}, {{responsive: true}});

    // Panel 2: Negative Covariance
    const tNegCloud = {{ x: {X_neg[5:, 0].tolist()}, y: {X_neg[5:, 1].tolist()}, mode: 'markers', marker: {{ color: '#ce93d8', size: 6 }}, name: 'Cloud Points (N=35)' }};
    const tNegBench = {{ x: {X_neg[:5, 0].tolist()}, y: {X_neg[:5, 1].tolist()}, mode: 'markers', marker: {{ color: '#7b1fa2', size: 9 }}, name: 'Benchmark Points (N=5)' }};
    const tNegPC1 = {{ x: [-4.2, 4.2], y: [4.2, -4.2], mode: 'lines', line: {{ color: '#d32f2f', width: 2.5 }}, name: 'PC1 (λ₁ = 4.50, 90%)' }};
    const tNegPC2 = {{ x: [-3.0, 3.0], y: [-3.0, 3.0], mode: 'lines', line: {{ color: '#2e7d32', width: 2, dash: 'dash' }}, name: 'PC2 (λ₂ = 0.50, 10%)' }};
    Plotly.newPlot('plot2', [tNegCloud, tNegBench, tNegPC1, tNegPC2], {{
      title: 'Negative Covariance: Down-Right Spine',
      xaxis: {{ range: [-4.8, 4.8], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-4.8, 4.8], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 35, r: 15, b: 35, t: 40 }}, showlegend: false
    }}, {{responsive: true}});

    // Panel 3: Zero Covariance
    const tZeroCloud = {{ x: {X_zero[5:, 0].tolist()}, y: {X_zero[5:, 1].tolist()}, mode: 'markers', marker: {{ color: '#80cbc4', size: 6 }}, name: 'Cloud Points (N=35)' }};
    const tZeroBench = {{ x: {X_zero[:5, 0].tolist()}, y: {X_zero[:5, 1].tolist()}, mode: 'markers', marker: {{ color: '#00897b', size: 9 }}, name: 'Benchmark Points (N=5)' }};
    const tZeroPC1 = {{ x: [-3.5, 3.5], y: [0, 0], mode: 'lines', line: {{ color: '#d32f2f', width: 2.5 }}, name: 'PC1 (λ₁ = 2.00, 50%)' }};
    const tZeroPC2 = {{ x: [0, 0], y: [-3.5, 3.5], mode: 'lines', line: {{ color: '#2e7d32', width: 2, dash: 'dash' }}, name: 'PC2 (λ₂ = 2.00, 50%)' }};
    Plotly.newPlot('plot3', [tZeroCloud, tZeroBench, tZeroPC1, tZeroPC2], {{
      title: 'Zero Covariance: Equal Spread (No Spine)',
      xaxis: {{ range: [-4.8, 4.8], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-4.8, 4.8], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 35, r: 15, b: 35, t: 40 }}, showlegend: false
    }}, {{responsive: true}});
  </script>
</body>
</html>
"""

html_path = os.path.join(assets_dir, '3_5_fig_pca_cases.html')
with open(html_path, 'w') as f:
    f.write(html_content)
print(f"Saved {html_path} successfully.")
