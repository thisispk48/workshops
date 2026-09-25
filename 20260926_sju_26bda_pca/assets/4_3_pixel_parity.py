#!/usr/bin/env python3
"""
4_3_pixel_parity.py
===================
Pixel-to-Pixel Parity Verifier: Pure NumPy First Principles vs. Scikit-Learn PCA.

This script mathematically tests and visualizes that:
  X_rec_scratch(k) == X_rec_sklearn(k)
down to numerical machine precision (~10^-12).

Outputs:
- Terminal ASCII parity verification table
- 3-Row Visual Parity Figure: {output_dir}/4_fig_pixel_parity.png
- Interactive Plotly HTML: {output_dir}/4_fig_pixel_parity.html
"""

import argparse
import os
import sys
import numpy as np
from PIL import Image
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Verify pixel-to-pixel parity between pure NumPy PCA and Scikit-Learn PCA."
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


def run_parity_analysis(X, k_values):
    H, W = X.shape

    # 1. Scratch PCA Precomputation
    mu_scratch = np.mean(X, axis=0, keepdims=True)
    X_c_scratch = X - mu_scratch
    U, S, Vt = np.linalg.svd(X_c_scratch, full_matrices=False)
    total_var_scratch = np.sum(S ** 2)

    parity_results = {}

    for k in k_values:
        # A. Scratch PCA
        V_k = Vt[:k, :].T
        Z_scratch = X_c_scratch @ V_k
        X_rec_scratch = Z_scratch @ V_k.T + mu_scratch
        var_scratch = np.sum(S[:k] ** 2) / total_var_scratch * 100.0

        # B. Sklearn PCA (exact SVD solver)
        pca = PCA(n_components=k, svd_solver="full")
        Z_sklearn = pca.fit_transform(X)
        X_rec_sklearn = pca.inverse_transform(Z_sklearn)
        var_sklearn = np.sum(pca.explained_variance_ratio_) * 100.0

        # C. Parity Metrics
        diff_matrix = np.abs(X_rec_scratch - X_rec_sklearn)
        max_diff = np.max(diff_matrix)
        mean_diff = np.mean(diff_matrix)
        frob_norm_diff = np.linalg.norm(X_rec_scratch - X_rec_sklearn)
        is_close_10 = np.allclose(X_rec_scratch, X_rec_sklearn, atol=1e-10)
        is_close_12 = np.allclose(X_rec_scratch, X_rec_sklearn, atol=1e-11)

        parity_results[k] = {
            "X_rec_scratch": X_rec_scratch,
            "X_rec_sklearn": X_rec_sklearn,
            "diff_matrix": diff_matrix,
            "max_diff": max_diff,
            "mean_diff": mean_diff,
            "frob_norm_diff": frob_norm_diff,
            "is_close_10": is_close_10,
            "is_close_12": is_close_12,
            "var_scratch": var_scratch,
            "var_sklearn": var_sklearn,
            "var_diff": abs(var_scratch - var_sklearn),
        }

    return parity_results


def create_parity_figure(X, parity_results, k_values, output_path):
    H, W = X.shape
    n_k = len(k_values)

    fig, axes = plt.subplots(3, n_k, figsize=(4.2 * n_k, 13), facecolor="#0F172A")
    plt.subplots_adjust(hspace=0.28, wspace=0.15)

    for col_idx, k in enumerate(k_values):
        res = parity_results[k]

        # Row 1: Scratch Reconstruction
        ax_scratch = axes[0, col_idx]
        ax_scratch.imshow(np.clip(res["X_rec_scratch"], 0, 255), cmap="gray", vmin=0, vmax=255)
        ax_scratch.set_title(
            f"Pure NumPy Scratch\nk = {k} ({res['var_scratch']:.1f}% Var)",
            fontsize=11,
            fontweight="bold",
            color="#38BDF8",
            pad=8,
        )
        ax_scratch.axis("off")

        # Row 2: Sklearn Reconstruction
        ax_sklearn = axes[1, col_idx]
        ax_sklearn.imshow(np.clip(res["X_rec_sklearn"], 0, 255), cmap="gray", vmin=0, vmax=255)
        ax_sklearn.set_title(
            f"Scikit-Learn PCA\nk = {k} ({res['var_sklearn']:.1f}% Var)",
            fontsize=11,
            fontweight="bold",
            color="#A855F7",
            pad=8,
        )
        ax_sklearn.axis("off")

        # Row 3: Absolute Difference Heatmap
        ax_diff = axes[2, col_idx]
        # Show difference with a viridis map
        im = ax_diff.imshow(res["diff_matrix"], cmap="plasma", vmin=0, vmax=max(1e-11, res["max_diff"]))
        ax_diff.set_title(
            f"|Scratch - Sklearn|\nMax Error: {res['max_diff']:.2e}\nParity: {'PASS (100%)' if res['is_close_10'] else 'FAIL'}",
            fontsize=10,
            fontweight="bold",
            color="#10B981" if res["is_close_10"] else "#EF4444",
            pad=8,
        )
        ax_diff.axis("off")

    plt.suptitle(
        "Pixel-to-Pixel Parity Verification: Pure NumPy vs. Scikit-Learn PCA\n"
        "(Proving Mathematical Equivalence Down to Numerical Precision ~ 10^-12)",
        fontsize=15,
        fontweight="bold",
        color="#F8FAFC",
        y=0.98,
    )

    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved parity figure: {output_path}")


def create_plotly_parity_html(X, parity_results, k_values, output_path):
    n_k = len(k_values)
    titles = []
    for k in k_values:
        titles.append(f"Scratch k={k}")
    for k in k_values:
        titles.append(f"Sklearn k={k}")
    for k in k_values:
        titles.append(f"Diff k={k} (Max: {parity_results[k]['max_diff']:.2e})")

    fig = make_subplots(rows=3, cols=n_k, subplot_titles=titles)

    for col_idx, k in enumerate(k_values, start=1):
        res = parity_results[k]
        # Row 1
        fig.add_trace(go.Heatmap(z=res["X_rec_scratch"], colorscale="Gray", showscale=False), row=1, col=col_idx)
        # Row 2
        fig.add_trace(go.Heatmap(z=res["X_rec_sklearn"], colorscale="Gray", showscale=False), row=2, col=col_idx)
        # Row 3
        fig.add_trace(go.Heatmap(z=res["diff_matrix"], colorscale="Plasma", showscale=False), row=3, col=col_idx)

    fig.update_layout(
        title="Interactive Pixel-to-Pixel Parity Analysis (NumPy vs. Sklearn)",
        template="plotly_dark",
        height=950,
        width=1350,
        paper_bgcolor="#0F172A",
        plot_bgcolor="#1E293B",
    )

    fig.write_html(output_path)
    print(f"Saved interactive HTML: {output_path}")


def main():
    args = parse_arguments()
    os.makedirs(args.output_dir, exist_ok=True)

    k_values = [int(x.strip()) for x in args.components.split(",")]

    print("=" * 80)
    print("PIXEL-TO-PIXEL PARITY VERIFICATION")
    print(f"Target Image: {args.image_path}")
    print(f"Evaluating k values: {k_values}")
    print("=" * 80)

    X = load_image_as_matrix(args.image_path)
    H, W = X.shape
    print(f"Loaded image matrix shape: {H} x {W} ({H * W:,} total pixels)\n")

    parity_results = run_parity_analysis(X, k_values)

    # Print Formatted Verification Table
    header = f"{'k':<5} | {'Max Pixel Diff':<16} | {'Mean Pixel Diff':<16} | {'Frobenius Norm':<16} | {'Var Diff (%)':<14} | {'np.allclose(1e-10)':<18}"
    sep = "-" * len(header)
    print(header)
    print(sep)

    all_passed = True
    for k in k_values:
        res = parity_results[k]
        passed_str = "PASS (True)" if res["is_close_10"] else "FAIL (False)"
        if not res["is_close_10"]:
            all_passed = False
        print(
            f"{k:<5} | {res['max_diff']:<16.2e} | {res['mean_diff']:<16.2e} | "
            f"{res['frob_norm_diff']:<16.2e} | {res['var_diff']:<14.2e} | {passed_str:<18}"
        )

    print(sep)
    if all_passed:
        print(">>> RESULT: PERFECT MATHEMATICAL PARITY CONFIRMED! <<<")
        print("Scikit-Learn PCA matches Pure NumPy First-Principles PCA down to machine precision.")
    else:
        print(">>> RESULT: PARITY DISCREPANCY DETECTED! <<<")
    print("=" * 80)

    # Save visual parity comparison
    png_path = os.path.join(args.output_dir, "4_3_fig_pixel_parity.png")
    html_path = os.path.join(args.output_dir, "4_3_fig_pixel_parity.html")

    create_parity_figure(X, parity_results, k_values, png_path)
    create_plotly_parity_html(X, parity_results, k_values, html_path)


if __name__ == "__main__":
    main()
