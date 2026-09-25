"""
1_4_fig_plane_projection_3d.py
Generates:
1. 1_4_fig_plane_projection_3d.png (High-resolution Matplotlib 3D figure)
2. 1_4_fig_plane_projection_3d.html (Interactive 3D visualization using Plotly via CDN)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

assets_dir = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------------------
# 1. Define Vectors and Calculate Projection
# -------------------------------------------------------------
# Plane spanned by a1 and a2 (columns of matrix A)
a1 = np.array([3.0, 1.0, 0.0])
a2 = np.array([1.0, 3.0, 1.0])
A = np.column_stack([a1, a2])  # 3x2 matrix

# Vector to be projected (floating above the plane)
b = np.array([2.0, 3.0, 4.0])

# Normal equation: (A^T * A) * x_hat = A^T * b
# x_hat = (A^T * A)^(-1) * A^T * b
AtA = A.T @ A
Atb = A.T @ b
x_hat = np.linalg.inv(AtA) @ Atb

# Projected vector on the plane: p = A * x_hat
p = A @ x_hat

# Error vector: e = b - p (must be orthogonal to plane)
e = b - p

print("Vector b:", b)
print("Projection p:", np.round(p, 3))
print("Error e:", np.round(e, 3))
print("Check a1 . e (should be ~0):", np.dot(a1, e))
print("Check a2 . e (should be ~0):", np.dot(a2, e))

# -------------------------------------------------------------
# 2. Matplotlib 3D Static Plot (1_4_fig_plane_projection_3d.png)
# -------------------------------------------------------------
fig = plt.figure(figsize=(9, 7), dpi=300)
ax = fig.add_subplot(111, projection='3d')
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#ffffff')

# Generate grid on the plane: p_grid = u*a1 + v*a2
u_vals = np.linspace(-0.2, 1.3, 20)
v_vals = np.linspace(-0.2, 1.3, 20)
U, V = np.meshgrid(u_vals, v_vals)
X_plane = U * a1[0] + V * a2[0]
Y_plane = U * a1[1] + V * a2[1]
Z_plane = U * a1[2] + V * a2[2]

# Plot translucent plane surface
ax.plot_surface(X_plane, Y_plane, Z_plane, color='#90caf9', alpha=0.35, edgecolor='#64b5f6', linewidth=0.4, antialiased=True)

# Helper function to plot 3D vector arrows
def plot_vector(ax, vec, color, label, lw=2.5):
    ax.quiver(0, 0, 0, vec[0], vec[1], vec[2], color=color, linewidth=lw, arrow_length_ratio=0.08, label=label)

# Plot basis vectors on the plane
plot_vector(ax, a1, '#1565c0', 'Basis vector a1 (in plane)', lw=2.2)
plot_vector(ax, a2, '#0288d1', 'Basis vector a2 (in plane)', lw=2.2)

# Plot projection vector p on the plane
plot_vector(ax, p, '#2e7d32', 'Projection p = A x_hat', lw=3.0)

# Plot vector b floating above
plot_vector(ax, b, '#8e24aa', 'Vector b (in 3D space)', lw=3.0)

# Plot perpendicular drop line (error vector e: from p to b)
ax.plot([p[0], b[0]], [p[1], b[1]], [p[2], b[2]], color='#e53935', linestyle='--', linewidth=2.2, label='Error e = b - p (orthogonal drop)')

# Scatter key endpoints
ax.scatter([b[0]], [b[1]], [b[2]], color='#8e24aa', s=50, depthshade=False)
ax.scatter([p[0]], [p[1]], [p[2]], color='#2e7d32', s=50, depthshade=False)
ax.scatter([0], [0], [0], color='#263238', s=40, depthshade=False)

# Labels
ax.text(b[0], b[1], b[2] + 0.3, ' b [2, 3, 4]', color='#8e24aa', fontweight='bold', fontsize=11)
ax.text(p[0] + 0.1, p[1] - 0.2, p[2] - 0.2, ' p (shadow on plane)', color='#2e7d32', fontweight='bold', fontsize=11)
ax.text((p[0]+b[0])/2 + 0.15, (p[1]+b[1])/2, (p[2]+b[2])/2, ' e (perpendicular)', color='#e53935', fontweight='bold', fontsize=10)
ax.text(a1[0], a1[1], a1[2] - 0.2, ' a1', color='#1565c0', fontweight='bold', fontsize=10)
ax.text(a2[0], a2[1], a2[2] + 0.2, ' a2', color='#0288d1', fontweight='bold', fontsize=10)

# Formatting
ax.set_title('3D Subspace Projection: Projecting Vector b onto a 2D Plane', fontsize=13, fontweight='bold', pad=15, color='#263238')
ax.set_xlabel('X', fontsize=10, labelpad=5)
ax.set_ylabel('Y', fontsize=10, labelpad=5)
ax.set_zlabel('Z', fontsize=10, labelpad=5)
ax.view_init(elev=26, azim=-55)
ax.legend(loc='upper left', frameon=True, framealpha=0.9, facecolor='#ffffff', edgecolor='#cfd8dc', fontsize=8.5)

plt.tight_layout()
png_path = os.path.join(assets_dir, '1_4_fig_plane_projection_3d.png')
plt.savefig(png_path, dpi=300)
print(f"Saved {png_path} successfully.")

# -------------------------------------------------------------
# 3. Interactive Standalone HTML (1_4_fig_plane_projection_3d.html)
# -------------------------------------------------------------
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Interactive 3D Subspace Projection (Vector onto Plane)</title>
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
      max-width: 1000px;
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
      height: 650px;
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
    <h1>Interactive 3D Projection: Vector b onto 2D Plane</h1>
    <p>
      Click and drag with your mouse to <b>rotate</b> the 3D scene. Scroll to <b>zoom</b>. Hover over points or vectors to inspect their 3D coordinates.
    </p>

    <div id="plot"></div>

    <div class="legend-box">
      <div><span class="badge" style="background:#8e24aa;"></span><b>Vector b:</b> [{b[0]}, {b[1]}, {b[2]}] (Original 3D vector)</div>
      <div><span class="badge" style="background:#2e7d32;"></span><b>Projection p:</b> [{p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f}] (Shadow on plane)</div>
      <div><span class="badge" style="background:#e53935;"></span><b>Error e:</b> [{e[0]:.2f}, {e[1]:.2f}, {e[2]:.2f}] (Perpendicular drop line)</div>
      <div><span class="badge" style="background:#60a5fa;"></span><b>Plane:</b> Spanned by a1 and a2</div>
    </div>
  </div>

  <script>
    // Plane mesh coordinates
    const xPlane = {X_plane.tolist()};
    const yPlane = {Y_plane.tolist()};
    const zPlane = {Z_plane.tolist()};

    // Vector line traces
    function makeVectorTrace(xEnd, yEnd, zEnd, color, name, width=6) {{
      return {{
        type: 'scatter3d',
        mode: 'lines+markers',
        x: [0, xEnd],
        y: [0, yEnd],
        z: [0, zEnd],
        line: {{ color: color, width: width }},
        marker: {{ size: [0, 5], color: color }},
        name: name
      }};
    }}

    const tracePlane = {{
      type: 'surface',
      x: xPlane,
      y: yPlane,
      z: zPlane,
      colorscale: [[0, 'rgba(147, 197, 253, 0.4)'], [1, 'rgba(147, 197, 253, 0.4)']],
      showscale: false,
      name: '2D Plane Subspace',
      hoverinfo: 'skip'
    }};

    const traceB = makeVectorTrace({b[0]}, {b[1]}, {b[2]}, '#8e24aa', 'Vector b [2, 3, 4]', 7);
    const traceA1 = makeVectorTrace({a1[0]}, {a1[1]}, {a1[2]}, '#1565c0', 'Basis vector a1 [3, 1, 0]', 5);
    const traceA2 = makeVectorTrace({a2[0]}, {a2[1]}, {a2[2]}, '#0288d1', 'Basis vector a2 [1, 3, 1]', 5);
    const traceP = makeVectorTrace({p[0]}, {p[1]}, {p[2]}, '#2e7d32', 'Projection p [{p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f}]', 8);

    // Drop line trace e (from p to b)
    const traceE = {{
      type: 'scatter3d',
      mode: 'lines',
      x: [{p[0]}, {b[0]}],
      y: [{p[1]}, {b[1]}],
      z: [{p[2]}, {b[2]}],
      line: {{ color: '#e53935', width: 5, dash: 'dash' }},
      name: 'Error e = b - p (Perpendicular drop)'
    }};

    const layout = {{
      margin: {{ l: 0, r: 0, b: 0, t: 0 }},
      scene: {{
        xaxis: {{ title: 'X', range: [-1, 5] }},
        yaxis: {{ title: 'Y', range: [-1, 5] }},
        zaxis: {{ title: 'Z', range: [-1, 5] }},
        camera: {{
          eye: {{ x: 1.4, y: -1.4, z: 1.1 }}
        }}
      }},
      legend: {{
        x: 0,
        y: 1,
        bgcolor: 'rgba(255, 255, 255, 0.85)'
      }}
    }};

    Plotly.newPlot('plot', [tracePlane, traceA1, traceA2, traceB, traceP, traceE], layout, {{responsive: true}});
  </script>
</body>
</html>
"""

html_path = os.path.join(assets_dir, '1_4_fig_plane_projection_3d.html')
with open(html_path, 'w') as f:
    f.write(html_content)
print(f"Saved {html_path} successfully.")
