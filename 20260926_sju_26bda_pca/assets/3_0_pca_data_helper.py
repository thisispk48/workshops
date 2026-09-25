"""
pca_data_helper.py
Generates the exact, reproducible 40-point datasets for Part 3:
- Case 1: Positive Covariance (Sigma = [[2.5, 2.0], [2.0, 2.5]])
- Case 2: Negative Covariance (Sigma = [[2.5, -2.0], [-2.0, 2.5]])
- Case 3: Zero Covariance (Sigma = [[2.0, 0.0], [0.0, 2.0]])

Each dataset features:
- N = 40 points in total.
- The first 5 points are EXACTLY the clean integer benchmark individuals (Persons A to E).
- The sample mean is strictly [0.0, 0.0].
- The sample covariance (1 / 39) * X_c^T * X_c strictly matches the target matrix Sigma!
"""

import numpy as np

def build_dataset_with_5_benchmarks(pts5, cov_target, N=40, seed=42):
    pts5 = np.array(pts5, dtype=float)
    S_target = (N - 1) * cov_target
    S5 = pts5.T @ pts5
    S_rem = S_target - S5
    cov_rem = S_rem / (N - 5)
    
    rng = np.random.RandomState(seed)
    raw_rem = rng.multivariate_normal([0, 0], cov_rem, size=N - 5)
    raw_rem -= np.mean(raw_rem, axis=0) # ensure zero mean
    
    curr_S = raw_rem.T @ raw_rem
    L_curr = np.linalg.cholesky(curr_S)
    L_rem = np.linalg.cholesky(S_rem)
    pts_rem = (raw_rem @ np.linalg.inv(L_curr).T) @ L_rem.T
    
    return np.vstack([pts5, pts_rem])

def get_datasets():
    # Case 1: Height vs. Weight (Positive Covariance +2.0)
    pts5_pos = [
        [2.0, 1.0],   # Person A
        [-2.0, -1.0], # Person B
        [1.0, 2.0],   # Person C
        [-1.0, -2.0], # Person D
        [0.0, 0.0]    # Person E
    ]
    cov_pos = np.array([[2.5, 2.0], [2.0, 2.5]])
    X_pos = build_dataset_with_5_benchmarks(pts5_pos, cov_pos, N=40, seed=42)

    # Case 2: Elevation vs. Temperature (Negative Covariance -2.0)
    pts5_neg = [
        [2.0, -1.0],
        [-2.0, 1.0],
        [1.0, -2.0],
        [-1.0, 2.0],
        [0.0, 0.0]
    ]
    cov_neg = np.array([[2.5, -2.0], [-2.0, 2.5]])
    X_neg = build_dataset_with_5_benchmarks(pts5_neg, cov_neg, N=40, seed=42)

    # Case 3: Uncorrelated Noise (Zero Covariance 0.0)
    pts5_zero = [
        [2.0, 0.0],
        [-2.0, 0.0],
        [0.0, 2.0],
        [0.0, -2.0],
        [0.0, 0.0]
    ]
    cov_zero = np.array([[2.0, 0.0], [0.0, 2.0]])
    X_zero = build_dataset_with_5_benchmarks(pts5_zero, cov_zero, N=40, seed=42)

    return X_pos, X_neg, X_zero
