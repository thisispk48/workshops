"""
2_5_fig_symmetric_transform.py
Standardized Visual Scheme:
- Left: Input Space R^2
- Right: Output Space R^2 (S = [[3, 1], [1, 3]])
- Benchmark: 4-quadrant grid in neutral GREY on BOTH panels
- Vector [1, 0]: Medium Blue (#1976d2)
- Vector [0, 1]: Light Blue (#64b5f6)
- Vector [1, 1]: Dark Navy Blue (#0d47a1) (Coincides with q1, shown alongside)
- Eigenvector 1 (q1 = [1, 1], lambda = 4): Red (#d32f2f)
- Eigenvector 2 (q2 = [-1, 1], lambda = 2): Green (#2e7d32)
- Axis ticks in increments of 1
- Rigid 90° orthogonality between q1 and q2 highlighted on both panels
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

assets_dir = os.path.dirname(os.path.abspath(__file__))

S = np.array([[3.0, 1.0],
              [1.0, 3.0]])

# 4-quadrant benchmark grid
coords = np.array([-2, -1, 0, 1, 2])
grid_x, grid_y = np.meshgrid(coords, coords)
input_points = np.vstack([grid_x.ravel(), grid_y.ravel()]).T
output_points = (S @ input_points.T).T

# Standard Color Palette across all figures
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

# Eigenspace lines on left
t_in = np.linspace(-3.5, 3.5, 50)
ax1.plot(t_in, t_in, color=COLOR_EIG1, linestyle='--', linewidth=1.3, alpha=0.6, label='Eigenspace 1 (y = x)')
ax1.plot(t_in, -t_in, color=COLOR_EIG2, linestyle='--', linewidth=1.3, alpha=0.6, label='Eigenspace 2 (y = -x)')

# 1. e1 = [1, 0] (Medium Blue)
ax1.annotate('', xy=(1, 0), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_E1, lw=3.0, mutation_scale=16), zorder=5)
ax1.scatter([1], [0], color=COLOR_E1, s=45, zorder=6)

# 2. e2 = [0, 1] (Light Blue)
ax1.annotate('', xy=(0, 1), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_E2, lw=3.0, mutation_scale=16), zorder=5)
ax1.scatter([0], [1], color=COLOR_E2, s=45, zorder=6)

# 3. d = [1, 1] (Dark Navy Blue) -> Coincides with q1, drawn with dash/offset
ax1.annotate('', xy=(1, 1), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_DIAG, lw=2.2, linestyle=':', mutation_scale=15), zorder=6)

# 4. q1 = [1, 1] (Red: Eigenvector 1)
ax1.annotate('', xy=(1, 1), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_EIG1, lw=3.2, mutation_scale=18), zorder=5)
ax1.scatter([1], [1], color=COLOR_EIG1, s=50, zorder=7)

# 5. q2 = [-1, 1] (Green: Eigenvector 2)
ax1.annotate('', xy=(-1, 1), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_EIG2, lw=3.2, mutation_scale=18), zorder=5)
ax1.scatter([-1], [1], color=COLOR_EIG2, s=50, zorder=7)

# 90° right-angle indicator between q1 and q2 on left
box_l = 0.4
u1 = np.array([1.0, 1.0]) / np.sqrt(2)
u2 = np.array([-1.0, 1.0]) / np.sqrt(2)
p1 = box_l * u1
p2 = box_l * u1 + box_l * u2
p3 = box_l * u2
ax1.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color='#263238', linewidth=1.3, zorder=8)
ax1.text(0.05, 0.55, '90°', color='#263238', fontweight='bold', fontsize=9, zorder=9)

# Labels Left
ax1.text(1.15, -0.35, r'$\mathbf{e}_1 = [1, 0]^T$', color=COLOR_E1, fontweight='bold', fontsize=10, zorder=8)
ax1.text(0.15, 1.15, r'$\mathbf{e}_2 = [0, 1]^T$', color=COLOR_E2, fontweight='bold', fontsize=10, zorder=8)
ax1.text(1.15, 1.15, r'$\mathbf{q}_1 = [1, 1]^T = \mathbf{d}$', color=COLOR_EIG1, fontweight='bold', fontsize=10, zorder=8)
ax1.text(-1.95, 1.15, r'$\mathbf{q}_2 = [-1, 1]^T$', color=COLOR_EIG2, fontweight='bold', fontsize=10, zorder=8)

ax1.legend(loc='upper left', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8)

# --- RIGHT: Transformed Space ---
ax2.set_title(r'Output Space $\mathbb{R}^2$ (After S = [[3, 1], [1, 3]])', fontsize=13, fontweight='bold', pad=12, color='#263238')
ax2.set_xlabel('X axis', fontsize=11)
ax2.set_ylabel('Y axis', fontsize=11)
ax2.set_xlim(-6.5, 6.5)
ax2.set_ylim(-6.5, 6.5)

# Grey Grid Lines (Transformed) - STRICTLY GREY
grid_transformed = output_points.reshape((5, 5, 2))
for i in range(5):
    ax2.plot(grid_transformed[i, :, 0], grid_transformed[i, :, 1], color=COLOR_GRID, linestyle='-', linewidth=1.0, zorder=1)
    ax2.plot(grid_transformed[:, i, 0], grid_transformed[:, i, 1], color=COLOR_GRID, linestyle='-', linewidth=1.0, zorder=1)

ax2.scatter(output_points[:, 0], output_points[:, 1], color=COLOR_PTS_OUT, s=35, zorder=3, label='Transformed Grid')

# Eigenspace lines shown faintly on right
t_out = np.linspace(-6, 6, 50)
ax2.plot(t_out, t_out, color=COLOR_EIG1, linestyle='--', linewidth=1.3, alpha=0.6, label='Eigenspace 1 (λ₁ = 4)')
ax2.plot(t_out, -t_out, color=COLOR_EIG2, linestyle='--', linewidth=1.3, alpha=0.6, label='Eigenspace 2 (λ₂ = 2)')

# 1. S * e1 = [3, 1] (Medium Blue) -> Rotated & stretched
ax2.annotate('', xy=(3, 1), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_E1, lw=3.0, mutation_scale=16), zorder=5)
ax2.scatter([3], [1], color=COLOR_E1, s=45, zorder=6)

# 2. S * e2 = [1, 3] (Light Blue) -> Rotated & stretched
ax2.annotate('', xy=(1, 3), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_E2, lw=3.0, mutation_scale=16), zorder=5)
ax2.scatter([1], [3], color=COLOR_E2, s=45, zorder=6)

# 3. S * d = [4, 4] (Dark Navy Blue) -> Lies on line y = x (scaled 4x)
ax2.annotate('', xy=(4, 4), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_DIAG, lw=2.2, linestyle=':', mutation_scale=16), zorder=6)

# 4. S * q1 = [4, 4] (Red) -> Scaled 4x along line y = x
ax2.annotate('', xy=(4, 4), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_EIG1, lw=3.2, mutation_scale=18), zorder=5)
ax2.scatter([4], [4], color=COLOR_EIG1, s=55, zorder=7)

# 5. S * q2 = [-2, 2] (Green) -> Scaled 2x along line y = -x
ax2.annotate('', xy=(-2, 2), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLOR_EIG2, lw=3.2, mutation_scale=18), zorder=5)
ax2.scatter([-2], [2], color=COLOR_EIG2, s=55, zorder=7)

# 90° right-angle indicator between transformed q1 and q2 on right
box_r = 0.7
p1_r = box_r * u1
p2_r = box_r * u1 + box_r * u2
p3_r = box_r * u2
ax2.plot([p1_r[0], p2_r[0], p3_r[0]], [p1_r[1], p2_r[1], p3_r[1]], color='#263238', linewidth=1.3, zorder=8)
ax2.text(0.08, 0.95, '90°', color='#263238', fontweight='bold', fontsize=9.5, zorder=9)

# Labels Right
ax2.text(3.15, 0.85, r'$\mathbf{S}\mathbf{e}_1 = [3, 1]^T$', color=COLOR_E1, fontweight='bold', fontsize=9.5, zorder=8)
ax2.text(1.15, 3.15, r'$\mathbf{S}\mathbf{e}_2 = [1, 3]^T$', color=COLOR_E2, fontweight='bold', fontsize=9.5, zorder=8)
ax2.text(4.15, 4.15, r'$\mathbf{S}\mathbf{q}_1 = [4, 4]^T$ (4×, line y=x)', color=COLOR_EIG1, fontweight='bold', fontsize=9.5, zorder=8)
ax2.text(-3.3, 2.15, r'$\mathbf{S}\mathbf{q}_2 = [-2, 2]^T$ (2×, line y=-x)', color=COLOR_EIG2, fontweight='bold', fontsize=9.5, zorder=8)

# Orthogonality guarantee note
ax2.text(-6.1, 4.8, "Symmetric Guarantee:\n• q₁ · q₂ = (1)(-1) + (1)(1) = 0\n• Strictly 90° Orthogonal\n• Pure orthogonal stretching",
         fontsize=8.5, bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#cfd8dc', alpha=0.92), zorder=10)

ax2.legend(loc='lower right', frameon=True, framealpha=0.92, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8)

plt.tight_layout()
png_path = os.path.join(assets_dir, '2_5_fig_symmetric_transform.png')
plt.savefig(png_path, dpi=300)
print(f"Saved {png_path} successfully.")

# -------------------------------------------------------------
# Interactive Standalone HTML (Side-by-Side Plotly)
# -------------------------------------------------------------
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Figure 2.5: Symmetric Matrix Transformation</title>
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
    <h1>Figure 2.5: Symmetric Matrix Transformation S = [[3, 1], [1, 3]]</h1>
    <p>
      Notice the profound contrast with non-diagonal matrices: 
      The eigenvectors <b>q₁ = [1, 1]ᵀ (Red)</b> and <b>q₂ = [-1, 1]ᵀ (Green)</b> are <b>strictly perpendicular at 90°</b> (q₁ · q₂ = 0) on BOTH the left and right! 
      The symmetric matrix stretches space into a rigid rotated orthogonal coordinate system.
    </p>

    <div class="charts-row">
      <div id="plot1" class="chart-col"></div>
      <div id="plot2" class="chart-col"></div>
    </div>

    <div class="legend-box">
      <div><span class="badge" style="background:#1976d2;"></span><b>e₁ = [1, 0]ᵀ (Medium Blue):</b> Lands at [3, 1]ᵀ</div>
      <div><span class="badge" style="background:#64b5f6;"></span><b>e₂ = [0, 1]ᵀ (Light Blue):</b> Lands at [1, 3]ᵀ</div>
      <div><span class="badge" style="background:#0d47a1;"></span><b>d = [1, 1]ᵀ (Navy Blue):</b> Coincides with q₁</div>
      <div><span class="badge" style="background:#d32f2f;"></span><b>Eigenvector q₁ = [1, 1]ᵀ (Red):</b> Scales 4× to [4, 4]ᵀ (Line y = x)</div>
      <div><span class="badge" style="background:#2e7d32;"></span><b>Eigenvector q₂ = [-1, 1]ᵀ (Green):</b> Scales 2× to [-2, 2]ᵀ (Line y = -x, 90° to q₁)</div>
    </div>
  </div>

  <script>
    // Left Chart (Input)
    const tracesLeft = [
      {{
        x: {input_points[:, 0].tolist()},
        y: {input_points[:, 1].tolist()},
        mode: 'markers',
        marker: {{ color: '#9e9e9e', size: 6 }},
        name: 'Benchmark Grid'
      }},
      {{ x: [-4, 4], y: [-4, 4], mode: 'lines', line: {{ color: '#d32f2f', width: 1.5, dash: 'dash' }}, name: 'Eigenspace 1 (y = x)', hoverinfo: 'skip' }},
      {{ x: [-4, 4], y: [4, -4], mode: 'lines', line: {{ color: '#2e7d32', width: 1.5, dash: 'dash' }}, name: 'Eigenspace 2 (y = -x)', hoverinfo: 'skip' }},
      {{ x: [0, 1], y: [0, 0], mode: 'lines+markers', line: {{ color: '#1976d2', width: 4 }}, marker: {{ size: [0, 7] }}, name: 'e₁ [1, 0]' }},
      {{ x: [0, 0], y: [0, 1], mode: 'lines+markers', line: {{ color: '#64b5f6', width: 4 }}, marker: {{ size: [0, 7] }}, name: 'e₂ [0, 1]' }},
      {{ x: [0, 1], y: [0, 1], mode: 'lines+markers', line: {{ color: '#d32f2f', width: 4 }}, marker: {{ size: [0, 8] }}, name: 'q₁ [1, 1] (Eigenvector 1)' }},
      {{ x: [0, -1], y: [0, 1], mode: 'lines+markers', line: {{ color: '#2e7d32', width: 4 }}, marker: {{ size: [0, 8] }}, name: 'q₂ [-1, 1] (Eigenvector 2)' }}
    ];

    const layoutLeft = {{
      title: 'Input Space R²',
      xaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-4.5, 4.5], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 40, r: 20, b: 40, t: 40 }},
      showlegend: false
    }};

    Plotly.newPlot('plot1', tracesLeft, layoutLeft, {{responsive: true}});

    // Right Chart (Output)
    const tracesRight = [
      {{
        x: {output_points[:, 0].tolist()},
        y: {output_points[:, 1].tolist()},
        mode: 'markers',
        marker: {{ color: '#757575', size: 6 }},
        name: 'Transformed Grid'
      }},
      {{ x: [-6, 6], y: [-6, 6], mode: 'lines', line: {{ color: '#d32f2f', width: 1.5, dash: 'dash' }}, name: 'Eigenspace 1 (λ₁ = 4)', hoverinfo: 'skip' }},
      {{ x: [-6, 6], y: [6, -6], mode: 'lines', line: {{ color: '#2e7d32', width: 1.5, dash: 'dash' }}, name: 'Eigenspace 2 (λ₂ = 2)', hoverinfo: 'skip' }},
      {{ x: [0, 3], y: [0, 1], mode: 'lines+markers', line: {{ color: '#1976d2', width: 4 }}, marker: {{ size: [0, 7] }}, name: 'S*e₁ [3, 1]' }},
      {{ x: [0, 1], y: [0, 3], mode: 'lines+markers', line: {{ color: '#64b5f6', width: 4 }}, marker: {{ size: [0, 7] }}, name: 'S*e₂ [1, 3]' }},
      {{ x: [0, 4], y: [0, 4], mode: 'lines+markers', line: {{ color: '#d32f2f', width: 5 }}, marker: {{ size: [0, 9] }}, name: 'S*q₁ [4, 4] (4×)' }},
      {{ x: [0, -2], y: [0, 2], mode: 'lines+markers', line: {{ color: '#2e7d32', width: 5 }}, marker: {{ size: [0, 9] }}, name: 'S*q₂ [-2, 2] (2×)' }}
    ];

    const layoutRight = {{
      title: 'Transformed Space R² (S * v)',
      xaxis: {{ range: [-6.5, 6.5], dtick: 1, zeroline: true, zerolinecolor: '#334155', scaleanchor: 'y' }},
      yaxis: {{ range: [-6.5, 6.5], dtick: 1, zeroline: true, zerolinecolor: '#334155' }},
      margin: {{ l: 40, r: 20, b: 40, t: 40 }},
      showlegend: false
    }};

    Plotly.newPlot('plot2', tracesRight, layoutRight, {{responsive: true}});
  </script>
</body>
</html>
"""

html_path = os.path.join(assets_dir, '2_5_fig_symmetric_transform.html')
with open(html_path, 'w') as f:
    f.write(html_content)
print(f"Saved {html_path} successfully.")
