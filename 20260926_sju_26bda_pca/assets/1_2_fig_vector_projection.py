"""
01_vector_projection_2d.py
Generates:
1. 01_vector_projection_2d.png (High-resolution Matplotlib 2D figure)
2. 01_vector_projection_2d.html (Interactive 2D visualization using Plotly via CDN)
"""

import os
import matplotlib.pyplot as plt
import numpy as np

assets_dir = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------------------
# 1. Define Vectors and Calculate Projection
# -------------------------------------------------------------
a = np.array([5.0, 2.0])
v = np.array([2.0, 4.0])

# Projection: p = ((v . a) / (a . a)) * a
scalar_proj = np.dot(v, a) / np.dot(a, a)
p = scalar_proj * a

# Error vector: e = v - p
e = v - p

# -------------------------------------------------------------
# 2. Matplotlib Static Figure (1_2_fig_vector_projection.png)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

ax.set_facecolor('#fafbfc')
fig.patch.set_facecolor('#ffffff')

# Subspace line spanned by a
line_t = np.linspace(-0.5, 1.4, 100)
line_x = [t * a[0] for t in line_t]
line_y = [t * a[1] for t in line_t]
ax.plot(line_x, line_y, color='#b0bec5', linestyle='--', linewidth=1.5, zorder=1, label='Subspace spanned by a (Line)')

# Drop line
ax.plot([v[0], p[0]], [v[1], p[1]], color='#e53935', linestyle=':', linewidth=2, zorder=2, label='Error vector e = v - p (drop line)')

# Right-angle marker
box_size = 0.25
u_a = a / np.linalg.norm(a)
u_e = e / np.linalg.norm(e)
corner_1 = p + box_size * u_e
corner_2 = corner_1 - box_size * u_a
corner_3 = p - box_size * u_a
ax.plot([corner_3[0], corner_2[0], corner_1[0]], [corner_3[1], corner_2[1], corner_1[1]], color='#78909c', linewidth=1.2, zorder=2)

# Vector arrows
ax.annotate('', xy=a, xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color='#1e88e5', lw=2.5, mutation_scale=18), zorder=3)
ax.annotate('', xy=v, xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color='#8e24aa', lw=2.5, mutation_scale=18), zorder=3)
ax.annotate('', xy=p, xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color='#2e7d32', lw=3.2, mutation_scale=20), zorder=4)

# Text labels
ax.text(v[0] - 0.4, v[1] + 0.15, r'$\mathbf{v} = [2, 4]^T$', fontsize=12, fontweight='bold', color='#8e24aa', zorder=5)
ax.text(a[0] + 0.15, a[1] - 0.1, r'$\mathbf{a} = [5, 2]^T$', fontsize=12, fontweight='bold', color='#1e88e5', zorder=5)
ax.text(p[0] + 0.1, p[1] - 0.35, r'$\mathbf{p} = \mathrm{proj}_{\mathbf{a}}(\mathbf{v})$', fontsize=12, fontweight='bold', color='#2e7d32', zorder=5)
ax.text((v[0] + p[0])/2 + 0.15, (v[1] + p[1])/2 + 0.1, r'$\mathbf{e} \perp \mathbf{a}$', fontsize=11, fontweight='bold', color='#e53935', zorder=5)

# Origin
ax.scatter([0], [0], color='#263238', s=40, zorder=5)
ax.text(-0.25, -0.3, '(0, 0)', fontsize=10, color='#546e7a')

ax.set_title('2D Vector Projection: Orthogonal Shadow onto a Line', fontsize=14, pad=15, fontweight='bold', color='#263238')
ax.set_xlabel('X axis', fontsize=11, labelpad=8, color='#37474f')
ax.set_ylabel('Y axis', fontsize=11, labelpad=8, color='#37474f')
ax.set_xlim(-1, 6.5)
ax.set_ylim(-1, 5.5)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.35, color='#b0bec5')
ax.legend(loc='upper left', frameon=True, framealpha=0.9, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=9.5)

for spine in ax.spines.values():
    spine.set_edgecolor('#b0bec5')

plt.tight_layout()
png_path = os.path.join(assets_dir, '1_2_fig_vector_projection.png')
plt.savefig(png_path, dpi=300)
print(f"Saved {png_path} successfully.")

# -------------------------------------------------------------
# 3. Interactive Standalone HTML (1_2_fig_vector_projection.html)
# -------------------------------------------------------------
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Interactive 2D Vector Projection</title>
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
      max-width: 900px;
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
    <h1>Interactive 2D Projection: Vector v onto Vector a</h1>
    <p>
      Hover over the vectors to see their coordinates. Click and drag to pan, scroll to zoom.
    </p>

    <div id="plot"></div>

    <div class="legend-box">
      <div><span class="badge" style="background:#8e24aa;"></span><b>Vector v:</b> [{v[0]}, {v[1]}] (Original vector)</div>
      <div><span class="badge" style="background:#1e88e5;"></span><b>Direction a:</b> [{a[0]}, {a[1]}] (Direction line)</div>
      <div><span class="badge" style="background:#2e7d32;"></span><b>Projection p:</b> [{p[0]:.2f}, {p[1]:.2f}] (Shadow)</div>
      <div><span class="badge" style="background:#e53935;"></span><b>Error e:</b> [{e[0]:.2f}, {e[1]:.2f}] (Perpendicular drop)</div>
    </div>
  </div>

  <script>
    const traceSubspace = {{
      x: [-2.5, 7.5],
      y: [-1.0, 3.0],
      mode: 'lines',
      line: {{ color: '#b0bec5', width: 2, dash: 'dash' }},
      name: 'Subspace Line (spanned by a)',
      hoverinfo: 'skip'
    }};

    const traceV = {{
      x: [0, {v[0]}],
      y: [0, {v[1]}],
      mode: 'lines+markers',
      line: {{ color: '#8e24aa', width: 5 }},
      marker: {{ size: [0, 8], color: '#8e24aa' }},
      name: 'Vector v [{v[0]}, {v[1]}]'
    }};

    const traceA = {{
      x: [0, {a[0]}],
      y: [0, {a[1]}],
      mode: 'lines+markers',
      line: {{ color: '#1e88e5', width: 4 }},
      marker: {{ size: [0, 8], color: '#1e88e5' }},
      name: 'Direction a [{a[0]}, {a[1]}]'
    }};

    const traceP = {{
      x: [0, {p[0]}],
      y: [0, {p[1]}],
      mode: 'lines+markers',
      line: {{ color: '#2e7d32', width: 6 }},
      marker: {{ size: [0, 9], color: '#2e7d32' }},
      name: 'Projection p [{p[0]:.2f}, {p[1]:.2f}]'
    }};

    const traceE = {{
      x: [{p[0]}, {v[0]}],
      y: [{p[1]}, {v[1]}],
      mode: 'lines',
      line: {{ color: '#e53935', width: 3, dash: 'dot' }},
      name: 'Error e = v - p (Drop line)'
    }};

    const layout = {{
      xaxis: {{ title: 'X axis', range: [-1, 7], scaleanchor: 'y', scaleratio: 1, zeroline: true }},
      yaxis: {{ title: 'Y axis', range: [-1, 6], zeroline: true }},
      margin: {{ l: 40, r: 20, b: 40, t: 20 }},
      legend: {{
        x: 0.02,
        y: 0.98,
        bgcolor: 'rgba(255, 255, 255, 0.9)'
      }}
    }};

    Plotly.newPlot('plot', [traceSubspace, traceA, traceV, traceP, traceE], layout, {{responsive: true}});
  </script>
</body>
</html>
"""

html_path = os.path.join(assets_dir, '1_2_fig_vector_projection.html')
with open(html_path, 'w') as f:
    f.write(html_content)
print(f"Saved {html_path} successfully.")
