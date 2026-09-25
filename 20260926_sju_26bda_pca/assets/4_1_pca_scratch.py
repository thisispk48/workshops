#!/usr/bin/env python3
"""
4_1_pca_scratch.py
==================
First-Principles PCA Image Compression using Pure NumPy.

Key Pedagogical Steps:
1. Load image as an H x W matrix X in R^(H x W).
2. Compute mean row vector mu in R^(1 x W) and center: X_c = X - mu.
3. Compute singular value decomposition: U, S, Vt = np.linalg.svd(X_c, full_matrices=False).
4. Project onto k leading principal axes: Z = X_c @ Vt[:k, :].T  in R^(H x k).
5. Reconstruct low-rank image: X_rec = Z @ Vt[:k, :] + mu  in R^(H x W).
6. Calculate compression ratio, explained variance, and reconstruction RMSE.

Outputs:
- Individual reconstructed images: {output_dir}/monalisa_scratch_k{k}.png
- Multi-panel comparison figure: {output_dir}/4_fig_pca_scratch.png
- Interactive Plotly HTML: {output_dir}/4_fig_pca_scratch.html
"""

import argparse
import os
import sys
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="First-principles PCA image compression using pure NumPy."
    )
    parser.add_argument(
        "--image-path",
        type=str,
        default="assets/4_monalisa.png",
        help="Path to input image file (default: assets/4_monalisa.png)",
    )
    parser.add_argument(
        "--components",
        type=str,
        default="5,20,50,100",
        help="Comma-separated component counts k (default: '5,20,50,100')",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="assets",
        help="Directory to save output figures (default: 'assets')",
    )
    return parser.parse_args()


def load_image_as_matrix(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at {image_path}")
    img = Image.open(image_path).convert("L")
    X = np.array(img, dtype=np.float64)
    return X


def pca_compress_scratch(X, k_values):
    H, W = X.shape
    total_pixels = H * W

    # Step 1: Center the data matrix
    mu = np.mean(X, axis=0, keepdims=True)  # (1, W)
    X_c = X - mu                            # (H, W)

    # Step 2: Singular Value Decomposition (SVD)
    U, S, Vt = np.linalg.svd(X_c, full_matrices=False)
    total_variance = np.sum(S ** 2)

    results = {}
    for k in k_values:
        # Step 3: Extract top k principal axes
        V_k = Vt[:k, :].T  # (W, k)

        # Step 4: 1D Compression (Projection into k-dim latent space)
        Z = X_c @ V_k      # (H, k)

        # Step 5: 2D Reconstruction (Decompression back to image space)
        X_rec = Z @ V_k.T + mu  # (H, W)
        X_rec_clipped = np.clip(X_rec, 0, 255)

        # Metrics
        explained_var = np.sum(S[:k] ** 2) / total_variance * 100.0
        stored_numbers = (H * k) + (k * W) + W
        compression_ratio = (1.0 - (stored_numbers / total_pixels)) * 100.0
        rmse = np.sqrt(np.mean((X - X_rec_clipped) ** 2))

        results[k] = {
            "X_rec": X_rec_clipped,
            "explained_var": explained_var,
            "compression_ratio": compression_ratio,
            "stored_numbers": stored_numbers,
            "rmse": rmse,
        }

    # Cumulative variance across all components for elbow plot
    cum_var_all = np.cumsum(S ** 2) / total_variance * 100.0

    return mu, S, results, cum_var_all


def create_matplotlib_figure(X, results, cum_var_all, k_values, output_path):
    H, W = X.shape
    total_pixels = H * W

    fig = plt.figure(figsize=(18, 11), facecolor="#0F172A")
    gs = fig.add_gridspec(2, 3, hspace=0.28, wspace=0.22)

    # 1. Original Image
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.imshow(X, cmap="gray", vmin=0, vmax=255)
    ax0.set_title(
        f"Original Image\n{H} x {W} ({total_pixels:,} numbers) | 100% Info",
        fontsize=13,
        fontweight="bold",
        color="#F8FAFC",
        pad=10,
    )
    ax0.axis("off")

    # 2-5: Reconstructions for each k
    grid_coords = [(0, 1), (0, 2), (1, 0), (1, 1)]
    colors = ["#EF4444", "#F59E0B", "#10B981", "#3B82F6"]

    for idx, (k, coord) in enumerate(zip(k_values, grid_coords)):
        res = results[k]
        ax = fig.add_subplot(gs[coord[0], coord[1]])
        ax.imshow(res["X_rec"], cmap="gray", vmin=0, vmax=255)
        ax.set_title(
            f"Rank k = {k} Components (NumPy Scratch)\n"
            f"Var: {res['explained_var']:.1f}% | Storage Saved: {res['compression_ratio']:.1f}%\n"
            f"Stored: {res['stored_numbers']:,} numbers | RMSE: {res['rmse']:.2f}",
            fontsize=11,
            fontweight="bold",
            color=colors[idx % len(colors)],
            pad=10,
        )
        ax.axis("off")

    # 6: Cumulative Explained Variance Curve (Elbow Plot)
    ax_elbow = fig.add_subplot(gs[1, 2])
    ax_elbow.set_facecolor("#1E293B")
    for spine in ax_elbow.spines.values():
        spine.set_color("#475569")

    n_comp_plot = min(150, len(cum_var_all))
    x_axis = np.arange(1, n_comp_plot + 1)
    ax_elbow.plot(x_axis, cum_var_all[:n_comp_plot], color="#38BDF8", linewidth=2.5, label="Cumulative Explained Var")
    ax_elbow.axhline(90, color="#F59E0B", linestyle="--", alpha=0.7, label="90% Threshold")
    ax_elbow.axhline(95, color="#10B981", linestyle="--", alpha=0.7, label="95% Threshold")
    ax_elbow.axhline(99, color="#EF4444", linestyle="--", alpha=0.7, label="99% Threshold")

    for k in k_values:
        if k <= n_comp_plot:
            v = cum_var_all[k - 1]
            ax_elbow.scatter([k], [v], s=70, zorder=5)
            ax_elbow.annotate(
                f"k={k}\n{v:.1f}%",
                (k, v),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
                fontsize=9,
                color="#F8FAFC",
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#0F172A", edgecolor="#64748B", alpha=0.8),
            )

    ax_elbow.set_title("Information Retention Curve (Eigenvalue Spectrum)", fontsize=12, fontweight="bold", color="#F8FAFC")
    ax_elbow.set_xlabel("Number of Principal Components (k)", fontsize=10, color="#CBD5E1")
    ax_elbow.set_ylabel("Cumulative Explained Variance (%)", fontsize=10, color="#CBD5E1")
    ax_elbow.tick_params(colors="#94A3B8")
    ax_elbow.set_ylim(80, 101)
    ax_elbow.grid(True, linestyle=":", alpha=0.3, color="#64748B")
    ax_elbow.legend(facecolor="#0F172A", edgecolor="#475569", labelcolor="#F8FAFC", fontsize=8, loc="lower right")

    plt.suptitle(
        "First-Principles PCA Image Compression (Pure NumPy Implementation)",
        fontsize=16,
        fontweight="bold",
        color="#F8FAFC",
        y=0.98,
    )

    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved static figure: {output_path}")


def create_plotly_html(X, results, cum_var_all, k_values, output_path):
    fig = make_subplots(
        rows=2,
        cols=3,
        subplot_titles=[
            f"Original ({X.shape[0]}x{X.shape[1]})",
            f"k = {k_values[0]} ({results[k_values[0]]['explained_var']:.1f}% Var)",
            f"k = {k_values[1]} ({results[k_values[1]]['explained_var']:.1f}% Var)",
            f"k = {k_values[2]} ({results[k_values[2]]['explained_var']:.1f}% Var)",
            f"k = {k_values[3]} ({results[k_values[3]]['explained_var']:.1f}% Var)",
            "Cumulative Explained Variance Curve",
        ],
    )

    # 1. Original
    fig.add_trace(go.Heatmap(z=X, colorscale="Gray", showscale=False), row=1, col=1)

    # 2-5. Reconstructions
    coords = [(1, 2), (1, 3), (2, 1), (2, 2)]
    for k, coord in zip(k_values, coords):
        fig.add_trace(
            go.Heatmap(z=results[k]["X_rec"], colorscale="Gray", showscale=False),
            row=coord[0],
            col=coord[1],
        )

    # 6. Spectrum Curve
    n_plot = min(150, len(cum_var_all))
    fig.add_trace(
        go.Scatter(
            x=list(range(1, n_plot + 1)),
            y=cum_var_all[:n_plot],
            mode="lines",
            line=dict(color="#38BDF8", width=3),
            name="Cumulative Variance %",
        ),
        row=2,
        col=3,
    )

    fig.update_layout(
        title="Interactive First-Principles PCA Image Compression (Pure NumPy)",
        template="plotly_dark",
        height=800,
        width=1200,
        paper_bgcolor="#0F172A",
        plot_bgcolor="#1E293B",
    )

    fig.write_html(output_path)
    print(f"Saved interactive HTML: {output_path}")


def main():
    args = parse_arguments()
    os.makedirs(args.output_dir, exist_ok=True)

    k_values = [int(x.strip()) for x in args.components.split(",")]

    print("=" * 70)
    print(f"Running Pure NumPy PCA on: {args.image_path}")
    print(f"Component ranks (k): {k_values}")
    print("=" * 70)

    X = load_image_as_matrix(args.image_path)
    H, W = X.shape

    mu, S, results, cum_var_all = pca_compress_scratch(X, k_values)

    # Save individual reconstructed images
    base_name = os.path.splitext(os.path.basename(args.image_path))[0]
    for k in k_values:
        rec_path = os.path.join(args.output_dir, f"{base_name}_scratch_k{k}.png")
        Image.fromarray(results[k]["X_rec"].astype(np.uint8)).save(rec_path)
        print(f"Saved individual image: {rec_path}")

    # Save summary figures
    png_path = os.path.join(args.output_dir, "4_1_fig_pca_scratch.png")
    html_path = os.path.join(args.output_dir, "4_1_fig_pca_scratch.html")

    create_matplotlib_figure(X, results, cum_var_all, k_values, png_path)
    create_plotly_html(X, results, cum_var_all, k_values, html_path)

    # Print Summary Table
    print("\n" + "=" * 70)
    print(f"{'k':<5} | {'Explained Var (%)':<18} | {'Storage Saved (%)':<18} | {'Stored Numbers':<15} | {'RMSE':<8}")
    print("-" * 70)
    for k in k_values:
        res = results[k]
        print(f"{k:<5} | {res['explained_var']:<18.2f} | {res['compression_ratio']:<18.2f} | {res['stored_numbers']:<15,d} | {res['rmse']:<8.2f}")
    print("=" * 70)


if __name__ == "__main__":
    main()
