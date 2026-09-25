"""
1_2_1_example_diagonal_projection.py
Example 1.2.1: Projecting vector v = [2, 4] onto the 45-degree line along x = [1, 1].
Generates:
1. 1_2_1_example_diagonal_projection.png (Matplotlib 300 DPI)
2. 1_2_1_example_diagonal_projection.html (Interactive Plotly via CDN)
"""

import os
import matplotlib.pyplot as plt
import numpy as np

assets_dir = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------------------
# 1. Math Calculation
# -------------------------------------------------------------
x = np.array([1.0, 1.0])
v = np.array([2.0, 4.0])

# Projection matrix P = (x * x^T) / (x^T * x)
P = np.outer(x, x) / np.dot(x, x)
p = P @ v  # [3.0, 3.0]
e = v - p  # [-1.0, 1.0]

print("Vector v:", v)
print("Direction x:", x)
print("Projection Matrix P:\n", P)
print("Projection p:", p)
print("Error e:", e)
print("Check orthogonality (x . e):", np.dot(x, e))

# -------------------------------------------------------------
# 2. Matplotlib Static Figure (1_2_1_example_diagonal_projection.png)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 7.5), dpi=300)

ax.set_facecolor('#fafbfc')
fig.patch.set_facecolor('#ffffff')

# Subspace line y = x
line_t = np.linspace(-0.5, 4.5, 100)
ax.plot(line_t, line_t, color='#90a4ae', linestyle='--', linewidth=1.8, zorder=1, label=r'Subspace $y = x$ (slope = $+1$)')

# Perpendicular drop line (e) from v [2, 4] to p [3, 3]
ax.plot([v[0], p[0]], [v[1], p[1]], color='#e53935', linestyle=':', linewidth=2.2, zorder=2, label=r'Drop line $\mathbf{e}$ (slope = $-1$)')

# Right angle marker at (3, 3)
box = 0.2
u_diag = np.array([-1.0, -1.0]) / np.sqrt(2)
u_perp = np.array([-1.0, 1.0]) / np.sqrt(2)
c1 = p + box * u_perp
c2 = c1 + box * u_diag
c3 = p + box * u_diag
ax.plot([c3[0], c2[0], c1[0]], [c3[1], c2[1], c1[1]], color='#546e7a', linewidth=1.3, zorder=2)

# Vector arrows
# x = [1, 1]
ax.annotate('', xy=x, xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color='#1e88e5', lw=2.5, mutation_scale=16), zorder=3)
# v = [2, 4]
ax.annotate('', xy=v, xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color='#8e24aa', lw=2.8, mutation_scale=18), zorder=3)
# p = [3, 3]
ax.annotate('', xy=p, xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color='#2e7d32', lw=3.2, mutation_scale=20), zorder=4)

# Key points
ax.scatter([0], [0], color='#263238', s=45, zorder=5)
ax.scatter([v[0]], [v[1]], color='#8e24aa', s=55, zorder=5)
ax.scatter([p[0]], [p[1]], color='#2e7d32', s=60, zorder=5)

# Text labels with coordinates
ax.text(v[0] - 0.45, v[1] + 0.15, r'$\mathbf{v} = [2, 4]^T$', fontsize=12, fontweight='bold', color='#8e24aa', zorder=6)
ax.text(x[0] + 0.15, x[1] - 0.25, r'$\mathbf{x} = [1, 1]^T$', fontsize=11, fontweight='bold', color='#1e88e5', zorder=6)
ax.text(p[0] + 0.15, p[1] - 0.25, r'$\mathbf{p} = [3, 3]^T$', fontsize=12, fontweight='bold', color='#2e7d32', zorder=6)
ax.text((v[0]+p[0])/2 - 0.85, (v[1]+p[1])/2 + 0.1, r'$\mathbf{e} = [-1, 1]^T$', fontsize=11, fontweight='bold', color='#e53935', zorder=6)

# Insight box
insight_text = (
    "Orthogonality Check:\n"
    "• Line slope: m₁ = +1\n"
    "• Error slope: m₂ = -1\n"
    "• m₁ × m₂ = -1  (Perpendicular at 90°)"
)
ax.text(0.15, 3.8, insight_text, fontsize=9.5, bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#cfd8dc', alpha=0.95), zorder=6)

# Formatting
ax.set_title('Example 1.2.1: Projection of [2, 4] onto [1, 1]', fontsize=13, fontweight='bold', pad=15, color='#263238')
ax.set_xlabel('X axis', fontsize=11, labelpad=8)
ax.set_ylabel('Y axis', fontsize=11, labelpad=8)
ax.set_xlim(-0.5, 4.5)
ax.set_ylim(-0.5, 4.8)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.4, color='#cfd8dc')
ax.legend(loc='lower right', frameon=True, framealpha=0.9, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=9.5)

for spine in ax.spines.values():
    spine.set_edgecolor('#b0bec5')

plt.tight_layout()
png_path = os.path.join(assets_dir, '1_2_1_example_diagonal_projection.png')
plt.savefig(png_path, dpi=300)
print(f"Saved {png_path} successfully.")

# -------------------------------------------------------------
# 3. Interactive Standalone HTML (1_2_1_example_diagonal_projection.html)
# -------------------------------------------------------------
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Interactive Example 1.2.1: 2D Diagonal Projection</title>
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
      max-width: 850px;
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
    #plot {{
      width: 100%;
      height: 550px;
    }}
    .legend-box {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      margin-top: 15px;
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
    <h1>Example 1.2.1: Projecting Vector v [2, 4] onto Line x [1, 1]</h1>
    <p>
      Notice the perpendicular drop: line <i>y = x</i> has slope +1, and drop line <i>e</i> has slope -1. 
      Their product is -1, confirming the 90° angle. Hover over points to inspect coordinates.
    </p>

    <div id="plot"></div>

    <div class="legend-box">
      <div><span class="badge" style="background:#8e24aa;"></span><b>Vector v:</b> [2, 4] (Original)</div>
      <div><span class="badge" style="background:#1e88e5;"></span><b>Vector x:</b> [1, 1] (Diagonal line)</div>
      <div><span class="badge" style="background:#2e7d32;"></span><b>Projection p:</b> [3, 3] (Shadow)</div>
      <div><span class="badge" style="background:#e53935;"></span><b>Error e:</b> [-1, 1] (Slope = -1, Orthogonal drop)</div>
    </div>
  </div>

  <script>
    const traceSubspace = {{
      x: [-0.5, 4.5],
      y: [-0.5, 4.5],
      mode: 'lines',
      line: {{ color: '#90a4ae', width: 2, dash: 'dash' }},
      name: 'Subspace Line y = x (slope = +1)',
      hoverinfo: 'skip'
    }};

    const traceV = {{
      x: [0, 2],
      y: [0, 4],
      mode: 'lines+markers',
      line: {{ color: '#8e24aa', width: 5 }},
      marker: {{ size: [0, 9], color: '#8e24aa' }},
      name: 'Vector v [2, 4]'
    }};

    const traceX = {{
      x: [0, 1],
      y: [0, 1],
      mode: 'lines+markers',
      line: {{ color: '#1e88e5', width: 4 }},
      marker: {{ size: [0, 8], color: '#1e88e5' }},
      name: 'Vector x [1, 1]'
    }};

    const traceP = {{
      x: [0, 3],
      y: [0, 3],
      mode: 'lines+markers',
      line: {{ color: '#2e7d32', width: 6 }},
      marker: {{ size: [0, 10], color: '#2e7d32' }},
      name: 'Projection p [3, 3]'
    }};

    const traceE = {{
      x: [3, 2],
      y: [3, 4],
      mode: 'lines+markers',
      line: {{ color: '#e53935', width: 3, dash: 'dot' }},
      marker: {{ size: [0, 6], color: '#e53935' }},
      name: 'Error e = [-1, 1] (slope = -1)'
    }};

    const layout = {{
      xaxis: {{ title: 'X axis', range: [-0.5, 4.5], scaleanchor: 'y', scaleratio: 1, zeroline: true }},
      yaxis: {{ title: 'Y axis', range: [-0.5, 4.8], zeroline: true }},
      margin: {{ l: 40, r: 20, b: 40, t: 20 }},
      legend: {{
        x: 0.55,
        y: 0.15,
        bgcolor: 'rgba(255, 255, 255, 0.9)'
      }}
    }};

    Plotly.newPlot('plot', [traceSubspace, traceX, traceV, traceP, traceE], layout, {{responsive: true}});
  </script>
</body>
</html>
"""

html_path = os.path.join(assets_dir, '1_2_1_example_diagonal_projection.html')
with open(html_path, 'w') as f:
    f.write(html_content)
print(f"Saved {html_path} successfully.")
