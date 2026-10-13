"""
src/significance.py
Paired and unpaired statistical significance testing for tokenizer comparisons.
"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, wilcoxon

try:
    from statsmodels.stats.multitest import multipletests
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False


def get_paired_fertility(
    df: pd.DataFrame,
    language: str,
    tokenizer_a: str,
    tokenizer_b: str,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extracts two aligned 1D numpy arrays of tokens_per_word for the same sentences,
    one for tokenizer_a and one for tokenizer_b, in identical sentence order.
    
    Reconstructs sentence pairing by row index within (language, tokenizer) groups,
    matching the evaluation benchmark execution order.
    """
    df = df.copy()
    if "sentence_idx" not in df.columns:
        df["sentence_idx"] = df.groupby(["language", "tokenizer"]).cumcount()

    subset = df[(df["language"] == language) & (df["tokenizer"].isin([tokenizer_a, tokenizer_b]))]
    wide = subset.pivot(index="sentence_idx", columns="tokenizer", values="tokens_per_word")
    wide = wide.dropna(subset=[tokenizer_a, tokenizer_b])
    return wide[tokenizer_a].to_numpy(dtype=float), wide[tokenizer_b].to_numpy(dtype=float)


def paired_wilcoxon_test(
    scores_a: np.ndarray,
    scores_b: np.ndarray,
    zero_method: str = "wilcox",
    alternative: str = "two-sided",
) -> Dict[str, float]:
    """
    Performs standard paired Wilcoxon signed-rank test.
    Tests whether the median difference (scores_a - scores_b) is zero.
    """
    res = wilcoxon(scores_a, scores_b, zero_method=zero_method, alternative=alternative)
    return {
        "statistic": float(res.statistic),
        "p_value": float(res.pvalue),
    }


def paired_bootstrap_ci(
    scores_a: np.ndarray,
    scores_b: np.ndarray,
    n_iterations: int = 1000,
    ci: float = 0.95,
    seed: int = 42,
) -> Dict[str, float]:
    """
    Computes bootstrap confidence interval on the mean difference (scores_a - scores_b)
    and percentage fertility reduction by resampling sentence pairs with replacement.
    
    Percentage reduction is defined as: -100 * (mean_a - mean_b) / mean_b
    (positive value indicates tokenizer_a is more compact than tokenizer_b).
    """
    rng = np.random.default_rng(seed)
    n = len(scores_a)
    diffs = scores_a - scores_b
    boot_diff_means = np.empty(n_iterations)
    boot_pct_reductions = np.empty(n_iterations)

    mean_b_orig = scores_b.mean()

    for i in range(n_iterations):
        idx = rng.integers(0, n, size=n)
        sample_a = scores_a[idx]
        sample_b = scores_b[idx]
        sample_diff = sample_a - sample_b
        boot_diff_means[i] = sample_diff.mean()
        # Relative reduction relative to baseline mean
        boot_pct_reductions[i] = -100.0 * (sample_a.mean() - sample_b.mean()) / sample_b.mean()

    lower_pct = (1.0 - ci) / 2.0 * 100.0
    upper_pct = (1.0 + ci) / 2.0 * 100.0

    diff_ci_low, diff_ci_high = np.percentile(boot_diff_means, [lower_pct, upper_pct])
    pct_ci_low, pct_ci_high = np.percentile(boot_pct_reductions, [lower_pct, upper_pct])

    return {
        "mean_diff": float(diffs.mean()),
        "diff_ci_low": float(diff_ci_low),
        "diff_ci_high": float(diff_ci_high),
        "pct_reduction": float(-100.0 * diffs.mean() / mean_b_orig),
        "pct_ci_low": float(pct_ci_low),
        "pct_ci_high": float(pct_ci_high),
    }


def unpaired_bootstrap_ci(
    scores_a: np.ndarray,
    scores_b: np.ndarray,
    n_iterations: int = 1000,
    ci: float = 0.95,
    seed: int = 42,
) -> Dict[str, float]:
    """
    Computes bootstrap confidence interval on the difference between two independent samples
    (mean_a - mean_b) by independent resampling with replacement (used for cross-lingual RQ3).
    """
    rng = np.random.default_rng(seed)
    n_a = len(scores_a)
    n_b = len(scores_b)
    boot_diffs = np.empty(n_iterations)

    for i in range(n_iterations):
        sample_a = rng.choice(scores_a, size=n_a, replace=True)
        sample_b = rng.choice(scores_b, size=n_b, replace=True)
        boot_diffs[i] = sample_a.mean() - sample_b.mean()

    lower_pct = (1.0 - ci) / 2.0 * 100.0
    upper_pct = (1.0 + ci) / 2.0 * 100.0
    ci_low, ci_high = np.percentile(boot_diffs, [lower_pct, upper_pct])

    return {
        "mean_diff": float(scores_a.mean() - scores_b.mean()),
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
    }


def apply_holm_bonferroni(
    p_values: Union[List[float], np.ndarray, pd.Series],
    alpha: float = 0.05,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Applies Holm-Bonferroni step-down multiple testing correction.
    Returns (reject_flags, corrected_p_values).
    """
    p_arr = np.asarray(p_values, dtype=float)
    if HAS_STATSMODELS:
        reject, corrected_p, _, _ = multipletests(p_arr, alpha=alpha, method="holm")
        return reject, corrected_p

    # Pure Python/NumPy Fallback for Holm-Bonferroni
    n = len(p_arr)
    sort_indices = np.argsort(p_arr)
    sorted_p = p_arr[sort_indices]

    adjusted_p = np.empty(n)
    for i, p in enumerate(sorted_p):
        adjusted_p[i] = min(1.0, p * (n - i))

    # Enforce monotonicity: adjusted_p[i] = max(adjusted_p[i], adjusted_p[i-1])
    for i in range(1, n):
        adjusted_p[i] = max(adjusted_p[i], adjusted_p[i - 1])

    # Reorder back to original positions
    final_p = np.empty(n)
    final_p[sort_indices] = adjusted_p
    reject = final_p < alpha
    return reject, final_p
