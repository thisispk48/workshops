"""
2_3_fig_diagonal_transform.py
Standardized Visual Scheme:
- Left: Input Space R^2
- Right: Output Space R^2 (D = [[3, 0], [0, 2]])
- Benchmark: 4-quadrant grid {-2, -1, 0, 1, 2}^2 in soft neutral GREY on BOTH panels
- Vector [1, 0]: Medium Blue (#1976d2)
- Vector [0, 1]: Light Blue (#64b5f6)
- Vector [1, 1]: Dark Navy Blue (#0d47a1)
- Eigenvector 1 (lambda = 3): Red (#d32f2f)
- Eigenvector 2 (lambda = 2): Green (#2e7d32)
- Axis ticks in increments of 1
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

assets_dir = os.path.dirname(os.path.abspath(__file__))

D = np.array([[3.0, 0.0],
              [0.0, 2.0]])

# 4-quadrant benchmark grid
coords = np.array([-2, -1, 0, 1, 2])
grid_x, grid_y = np.meshgrid(coords, coords)
input_points = np.vstack([grid_x.ravel(), grid_y.ravel()]).T
output_points = (D @ input_points.T).T

# Standard Color Palette
COLOR_E1 = '#1976d2'      # Medium Blue: [1, 0]
COLOR_E2 = '#64b5f6'      # Light Blue:  [0, 1]
COLOR_DIAG = '#0d47a1'    # Dark Navy:   [1, 1]
COLOR_EIG1 = '#d32f2f'    # Red:         Eigenvector 1
COLOR_EIG2 = '#2e7d32'    # Green:       Eigenvector 2
COLOR_GRID = '#e0e0e0'    # Neutral Grey Grid
COLOR_PTS_IN = '#9e9e9e'  # Soft Grey Points (Input)
COLOR_PTS_OUT = '#757575' # Slate Grey Points (Output)

# -------------------------------------------------------------
# Matplotlib Figure (Side-by-Side)
# -------------------------------------------------------------
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

# --- LEFT: Input Space ---
ax1.set_title(r'Input Space $\mathbb{R}^2$', fontsize=13, fontweight='bold', pad=12, color='#263238')
ax1.set_xlabel('X axis', fontsize=11)
ax1.set_ylabel('Y axis', fontsize=11)
ax1.set_xlim(-4.5, 4.5)
ax1.set_ylim(-4.5, 4.5)

# Grey Grid Lines (Input)
for c in coords:
    ax1.plot([c, c], [-2, 2], color=COLOR_GRID, linestyle='-', linewidth=1.0, zorder=1)
    ax1.plot([-2, 2], [c, c], color=COLOR_GRID, linestyle='-', linewidth=1.0, zorder=1)

ax1.scatter(input_points[:, 0], input_points[:, 1], color=COLOR_PTS_IN, s=28, zorder=3, label='Benchmark Grid')

# Eigenspace lines shown faintly
ax1.plot([-4, 4], [0, 0], color=COLOR_EIG1, linestyle='--', linewidth=1.3, alpha=0.5, label='Eigenspace 1 (y = 0)')
ax1.plot([0, 0], [-4, 4], color=COLOR_EIG2, linestyle='--', linewidth=1.3, alpha=0.5, label='Eigenspace 2 (x = 0)')

# Vectors on Left
# e1 = [1, 0] (Medium Blue) -> Lies on Red Eigenspace
ax1.annotate('', xy=(1, 0), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_E1, lw=3.0, mutation_scale=16), zorder=5)
ax1.scatter([1], [0], color=COLOR_E1, s=45, zorder=6)

# e2 = [0, 1] (Light Blue) -> Lies on Green Eigenspace
ax1.annotate('', xy=(0, 1), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_E2, lw=3.0, mutation_scale=16), zorder=5)
ax1.scatter([0], [1], color=COLOR_E2, s=45, zorder=6)

# d = [1, 1] (Dark Navy Blue)
ax1.annotate('', xy=(1, 1), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_DIAG, lw=3.0, mutation_scale=16), zorder=5)
ax1.scatter([1], [1], color=COLOR_DIAG, s=45, zorder=6)

# Labels Left
ax1.text(1.15, -0.35, r'$\mathbf{e}_1 = [1, 0]^T$', color=COLOR_E1, fontweight='bold', fontsize=10, zorder=7)
ax1.text(0.15, 1.15, r'$\mathbf{e}_2 = [0, 1]^T$', color=COLOR_E2, fontweight='bold', fontsize=10, zorder=7)
ax1.text(1.15, 1.15, r'$\mathbf{d} = [1, 1]^T$', color=COLOR_DIAG, fontweight='bold', fontsize=10, zorder=7)

ax1.legend(loc='upper left', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8.5)

# --- RIGHT: Transformed Space ---
ax2.set_title(r'Output Space $\mathbb{R}^2$ (After D = [[3, 0], [0, 2]])', fontsize=13, fontweight='bold', pad=12, color='#263238')
ax2.set_xlabel('X axis', fontsize=11)
ax2.set_ylabel('Y axis', fontsize=11)
ax2.set_xlim(-7.5, 7.5)
ax2.set_ylim(-5.5, 5.5)

# Grey Grid Lines (Transformed) - STRICTLY GREY
for c in coords:
    ax2.plot([3*c, 3*c], [-4, 4], color=COLOR_GRID, linestyle='-', linewidth=1.0, zorder=1)
    ax2.plot([-6, 6], [2*c, 2*c], color=COLOR_GRID, linestyle='-', linewidth=1.0, zorder=1)

ax2.scatter(output_points[:, 0], output_points[:, 1], color=COLOR_PTS_OUT, s=35, zorder=3, label='Transformed Grid')

# Eigenspace lines shown faintly on right
ax2.plot([-7, 7], [0, 0], color=COLOR_EIG1, linestyle='--', linewidth=1.3, alpha=0.5, label='Eigenspace 1 (λ₁ = 3)')
ax2.plot([0, 0], [-5, 5], color=COLOR_EIG2, linestyle='--', linewidth=1.3, alpha=0.5, label='Eigenspace 2 (λ₂ = 2)')

# Vectors on Right (EXACT SAME COLORS)
# D * e1 = [3, 0] (Medium Blue) -> Scaled 3x on Red Eigenspace
ax2.annotate('', xy=(3, 0), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_E1, lw=3.2, mutation_scale=18), zorder=5)
ax2.scatter([3], [0], color=COLOR_E1, s=55, zorder=6)

# D * e2 = [0, 2] (Light Blue) -> Scaled 2x on Green Eigenspace
ax2.annotate('', xy=(0, 2), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_E2, lw=3.2, mutation_scale=18), zorder=5)
ax2.scatter([0], [2], color=COLOR_E2, s=55, zorder=6)

# D * d = [3, 2] (Dark Navy Blue) -> Direction changed!
ax2.annotate('', xy=(3, 2), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_DIAG, lw=3.2, mutation_scale=18), zorder=5)
ax2.scatter([3], [2], color=COLOR_DIAG, s=55, zorder=6)

# Labels Right
ax2.text(3.2, -0.4, r'$\mathbf{D}\mathbf{e}_1 = [3, 0]^T$ (3×, SAME direction)', color=COLOR_E1, fontweight='bold', fontsize=9.5, zorder=7)
ax2.text(0.15, 2.2, r'$\mathbf{D}\mathbf{e}_2 = [0, 2]^T$ (2×, SAME direction)', color=COLOR_E2, fontweight='bold', fontsize=9.5, zorder=7)
ax2.text(3.2, 2.2, r'$\mathbf{D}\mathbf{d} = [3, 2]^T$ (Direction changed!)', color=COLOR_DIAG, fontweight='bold', fontsize=9.5, zorder=7)

ax2.legend(loc='upper left', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8.5)

plt.tight_layout()
png_path = os.path.join(assets_dir, '2_3_fig_diagonal_transform.png')
plt.savefig(png_path, dpi=300)
print(f"Saved {png_path} successfully.")

# -------------------------------------------------------------
# Standalone Interactive HTML
# -------------------------------------------------------------
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Figure 2.3: Diagonal Matrix Transformation</title>
  <script src="https://cdn.plot.ly/plotly-2.29.1.min.js"></script>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 20px;
      background: #f8fafc;
      color: #1e293b;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
      padding: 24px;
    }}
    h1 {{
      font-size: 22px;
      margin-top: 0;
      color: #0f172a;
    }}
    p {{
      line-height: 1.6;
      color: #475569;
      font-size: 14px;
    }}
    .charts-row {{
      display: flex;
      gap: 20px;
      margin-top: 15px;
    }}
    .chart-col {{
      flex: 1;
      height: 520px;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
    }}
    .legend-box {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      margin-top: 20px;
      padding: 12px 16px;
      background: #f1f5f9;
      border-radius: 8px;
      font-size: 13px;
    }}
    .badge {{
      display: inline-block;
      width: 12px;
      height: 12px;
      border-radius: 3px;
      margin-right: 6px;
      vertical-align: middle;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Figure 2.3: Diagonal Matrix Transformation D = [[3, 0], [0, 2]]</h1>
    <p>
      Notice the unified color scheme: <b>[1, 0]ᵀ (Medium Blue)</b> and <b>[0, 1]ᵀ (Light Blue)</b> lie on the invariant eigenspace lines (Red and Green) and preserve their direction. 
      In contrast, <b>[1, 1]ᵀ (Dark Navy Blue)</b> visibly tilts to [3, 2]ᵀ.
    </p>

    <div class="charts-row">
      <div id="plot1" class="chart-col"></div>
      <div id="plot2" class="chart-col"></div>
    </div>

    <div class="legend-box">
      <div><span class="badge" style="background:#1976d2;"></span><b>Vector [1, 0]ᵀ (Medium Blue):</b> Scales 3× to [3, 0]ᵀ (Direction preserved on Red line)</div>
      <div><span class="badge" style="background:#64b5f6;"></span><b>Vector [0, 1]ᵀ (Light Blue):</b> Scales 2× to [0, 2]ᵀ (Direction preserved on Green line)</div>
      <div><span class="badge" style="background:#0d47a1;"></span><b>Vector [1, 1]ᵀ (Dark Navy):</b> Lands at [3, 2]ᵀ (Direction changed!)</div>
      <div><span class="badge" style="background:#d32f2f;"></span><b>Eigen-axis 1 (Red):</b> y = 0 (λ₁ = 3)</div>
      <div><span class="badge" style="background:#2e7d32;"></span><b>Eigen-axis 2 (Green):</b> x = 0 (λ₂ = 2)</div>
    </div>
  </div>

  <script>
    function makeGrid(coords, mx, my, color) {{
      const traces = [];
      coords.forEach(c => {{
        traces.push({{ x: [c*mx, c*mx], y: [-2*my, 2*my], mode: 'lines', line: {{ color: color, width: 1 }}, showlegend: false, hoverinfo: 'skip' }});
        traces.push({{ x: [-2*mx, 2*mx], y: [c*my, c*my], mode: 'lines', line: {{ color: color, width: 1 }}, showlegend: false, hoverinfo: 'skip' }});
      }});
      return traces;
    }}
    const coords = [-2, -1, 0, 1, 2];

    // Left Chart (Input)
    const tracesLeft = [
      ...makeGrid(coords, 1, 1, '#e2e8f0'),
      {{ x: [-4, 4], y: [0, 0], mode: 'lines', line: {{ color: '#d32f2f', width: 1.5, dash: 'dash' }}, name: 'Eigen-axis 1 (y=0)' }},
      {{ x: [0, 0], y: [-4, 4], mode: 'lines', line: {{ color: '#2e7d32', width: 1.5, dash: 'dash' }}, name: 'Eigen-axis 2 (x=0)' }},
      {{ x: {input_points[:, 0].tolist()}, y: {input_points[:, 1].tolist()}, mode: 'markers', marker: {{ color: '#94a3b8', size: 6 }}, name: 'Grid Points' }},
      {{ x: [0, 1], y: [0, 0], mode: 'lines+markers', line: {{ color: '#1976d2', width: 5 }}, marker: {{ size: [0, 8] }}, name: '[1, 0]ᵀ (Med Blue)' }},
      {{ x: [0, 0], y: [0, 1], mode: 'lines+markers', line: {{ color: '#64b5f6', width: 5 }}, marker: {{ size: [0, 8] }}, name: '[0, 1]ᵀ (Light Blue)' }},
      {{ x: [0, 1], y: [0, 1], mode: 'lines+markers', line: {{ color: '#0d47a1', width: 5 }}, marker: {{ size: [0, 8] }}, name: '[1, 1]ᵀ (Dark Blue)' }}
    ];
    const layoutLeft = {{
      title: 'Input Space R²',
      xaxis: {{ range: [-4, 4], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-4, 4], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 40, r: 20, b: 40, t: 40 }},
      showlegend: false
    }};
    Plotly.newPlot('plot1', tracesLeft, layoutLeft, {{responsive: true}});

    // Right Chart (Output)
    const tracesRight = [
      ...makeGrid(coords, 3, 2, '#e2e8f0'),
      {{ x: [-7, 7], y: [0, 0], mode: 'lines', line: {{ color: '#d32f2f', width: 1.5, dash: 'dash' }}, name: 'Eigen-axis 1' }},
      {{ x: [0, 0], y: [-5, 5], mode: 'lines', line: {{ color: '#2e7d32', width: 1.5, dash: 'dash' }}, name: 'Eigen-axis 2' }},
      {{ x: {output_points[:, 0].tolist()}, y: {output_points[:, 1].tolist()}, mode: 'markers', marker: {{ color: '#64748b', size: 6 }}, name: 'Transformed Grid' }},
      {{ x: [0, 3], y: [0, 0], mode: 'lines+markers', line: {{ color: '#1976d2', width: 6 }}, marker: {{ size: [0, 9] }}, name: 'D*[1, 0]' }},
      {{ x: [0, 0], y: [0, 2], mode: 'lines+markers', line: {{ color: '#64b5f6', width: 6 }}, marker: {{ size: [0, 9] }}, name: 'D*[0, 1]' }},
      {{ x: [0, 3], y: [0, 2], mode: 'lines+markers', line: {{ color: '#0d47a1', width: 6 }}, marker: {{ size: [0, 9] }}, name: 'D*[1, 1]' }}
    ];
    const layoutRight = {{
      title: 'Output Space R² (D * v)',
      xaxis: {{ range: [-7, 7], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-5, 5], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 40, r: 20, b: 40, t: 40 }},
      showlegend: false
    }};
    Plotly.newPlot('plot2', tracesRight, layoutRight, {{responsive: true}});
  </script>
</body>
</html>
"""

html_path = os.path.join(assets_dir, '2_3_fig_diagonal_transform.html')
with open(html_path, 'w') as f:
    f.write(html_content)
print(f"Saved {html_path} successfully.")
