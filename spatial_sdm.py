# -*- coding: utf-8 -*-

# spatial_sdm.py
"""
Spatial SDM (Spatial Durbin Model) for panel data in PyMC.

This module provides utilities to:
- Load and clean spatial weight matrices (W) exported from Excel.
- Align panel data (country-year) with W.
- Fit a Spatial Durbin Model (SDM) with country and time effects.
- Run LOCO (Leave-One-Country-Out) cross-validation.

Assumptions
-----------
1) The panel is balanced for model fitting: NT == N * T.
2) Data passed to the model are sorted by ['year', 'country'] and, within each year,
   all countries appear exactly once in a consistent order.
3) W is square (N x N) and aligned to the same set (and order) of countries as the panel.
   The matrix is row-standardized internally by this module.

Notes
-----
- The likelihood is implemented via `pm.Potential`, including the Jacobian term
  log|I - rho W| computed from the eigenvalues of W.
- `rho` is constrained to (-0.95, 0.95) via a tanh transform.
"""


import numpy as np
import pandas as pd
import pymc as pm
import pytensor.tensor as pt
import arviz as az

def prepare_W_from_excel(W_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Clean a spatial weights matrix loaded from Excel into a square DataFrame.

    Many Excel exports store row labels in a column such as 'Unnamed: 0', and may
    lose column labels. This function attempts to restore a proper square matrix:

    - If an 'Unnamed: 0' column exists, it is treated as the index (row labels).
    - If columns are not object dtype or do not match the index, columns are set
      to match the index.
    - Values are coerced to numeric; non-numeric entries become NaN and are filled with 0.

    Parameters
    ----------
    W_raw : pd.DataFrame
        Raw DataFrame loaded from Excel.

    Returns
    -------
    pd.DataFrame
        Cleaned W with matching index/columns and numeric values.
    """
    W = W_raw.copy()

    if "Unnamed: 0" in W.columns:
        W = W.set_index("Unnamed: 0")

    if (W.columns.dtype != object) or (list(W.columns) != list(W.index)):
        W.columns = W.index

    W = W.apply(pd.to_numeric, errors="coerce").fillna(0.0)
    return W


def row_standardize(W: np.ndarray) -> np.ndarray:
    """
    Row-standardize a weight matrix.

    For each row i:
        W[i, :] <- W[i, :] / sum_j W[i, j]
    Rows with zero sum are left unchanged.

    Parameters
    ----------
    W : np.ndarray
        Weight matrix of shape (N, N).

    Returns
    -------
    np.ndarray
        Row-standardized matrix of shape (N, N) (float64).
    """
    W = W.astype("float64", copy=True)
    row_sums = W.sum(axis=1)
    nz = row_sums != 0
    W[nz, :] = W[nz, :] / row_sums[nz][:, None]
    return W


def align_df_and_W(df: pd.DataFrame, W_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Align a panel DataFrame and spatial weight matrix to a common country set.

    This:
    - casts df['year'] to int
    - finds the intersection of countries in df and W_df.index
    - filters df to those countries
    - subsets W_df to the same countries (rows and columns)

    Parameters
    ----------
    df : pd.DataFrame
        Panel data with at least columns ['country', 'year'].
    W_df : pd.DataFrame
        Spatial weight matrix with countries as index and columns.

    Returns
    -------
    (pd.DataFrame, pd.DataFrame)
        Filtered (df, W_df) aligned to a common set of countries.
    """
    df = df.copy()
    df["year"] = df["year"].astype(int)

    common = sorted(set(df["country"].unique()).intersection(W_df.index))
    df = df[df["country"].isin(common)].copy()
    W_df = W_df.loc[common, common].copy()
    return df, W_df


def make_balanced_panel(df: pd.DataFrame, countries: list[str], years: list[int]) -> pd.DataFrame:
    """
    Filter and sort a panel dataset to a specific (countries, years) set.

    The returned DataFrame is sorted by ['year', 'country'].

    Parameters
    ----------
    df : pd.DataFrame
        Panel data with columns ['country', 'year'].
    countries : list[str]
        Countries to keep.
    years : list[int]
        Years to keep.

    Returns
    -------
    pd.DataFrame
        Filtered and sorted panel.
    """
    df = df.copy()
    df["year"] = df["year"].astype(int)
    df = df[df["country"].isin(countries) & df["year"].isin(years)]
    df = df.sort_values(["year", "country"])
    return df


def shrink_W(W_df: pd.DataFrame, countries_keep: list[str]) -> np.ndarray:
    """
    Subset W to a set of countries and row-standardize.

    Parameters
    ----------
    W_df : pd.DataFrame
        Weight matrix with countries as index/columns.
    countries_keep : list[str]
        Countries to keep.

    Returns
    -------
    np.ndarray
        Row-standardized submatrix W of shape (N_keep, N_keep).
    """
    W_sub = W_df.loc[countries_keep, countries_keep].values.astype("float64")
    return row_standardize(W_sub)


def run_sdm_model(
    df_sorted: pd.DataFrame,
    W_cul06: pd.DataFrame,
    draws: int = 2000,
    tune: int = 2000,
    chains: int = 4,
    target_accept: float = 0.95,
    random_seed: int | None = 123,
    cores: int | None = None,
    progressbar: bool = True,
) -> tuple["arviz.InferenceData", list[str], list[int], np.ndarray]:
    """
    Fit a Spatial Durbin Model (SDM) in PyMC using balanced panel data.

    Model (conceptual)
    ------------------
    Let y_t be N-vector for year t and X_t be N x K. The SDM is:

        (I - rho W) y_t = X_t beta + (W X_t) gamma + alpha + time_alpha_t + eps_t
        eps_t ~ N(0, sigma^2 I)

    with country random effects alpha (hierarchical) and year effects time_alpha.

    Important: This implementation assumes a balanced panel with NT = N*T, and that
    df_sorted is sorted by ['year','country'] with all countries present each year.

    Parameters
    ----------
    df_sorted : pd.DataFrame
        Panel data sorted by ['year','country'] containing columns:
        ['country','year','GDP','Political Stability','exchange rate',
         'Rule of Law: Estimate','inbound'].
    W_cul06 : pd.DataFrame
        Spatial weight matrix (N x N) indexed/columned by countries.
    draws : int
        Number of posterior draws.
    tune : int
        Number of tuning steps.
    chains : int
        Number of MCMC chains.
    target_accept : float
        NUTS target_accept.
    random_seed : int | None
        Seed for reproducibility. Use None for stochastic runs.
    cores : int | None
        Number of CPU cores used by PyMC. If None, PyMC decides.
    progressbar : bool
        Whether to display the sampling progress bar.

    Returns
    -------
    trace : arviz.InferenceData
        Posterior samples.
    countries_sorted : list[str]
        Countries in the internal panel order.
    years_sorted : list[int]
        Years in the internal panel order.
    W_base : np.ndarray
        Row-standardized W used in estimation (N x N).
    """
    df_sorted = df_sorted.copy()
    df_sorted["year"] = df_sorted["year"].astype(int)

    years_sorted = sorted(df_sorted["year"].unique())
    countries_sorted = sorted(df_sorted["country"].unique())
    T, N = len(years_sorted), len(countries_sorted)

    country_to_idx = {c: i for i, c in enumerate(countries_sorted)}
    year_to_idx = {yr: i for i, yr in enumerate(years_sorted)}
    country_idx = df_sorted["country"].map(country_to_idx).to_numpy("int32")
    year_idx = df_sorted["year"].map(year_to_idx).to_numpy("int32")

    X = df_sorted[['GDP', 'Political Stability', 'exchange rate', "Rule of Law: Estimate"]].to_numpy("float64")
    y = df_sorted["inbound"].to_numpy("float64")
    K = X.shape[1]
    NT = X.shape[0]
    assert NT == T * N, "Balanced panel required (NT == T*N)."

    W_base = row_standardize(W_cul06.values.astype("float64"))
    assert W_base.shape == (N, N), "W must be NxN after alignment."

    eig_base = np.linalg.eigvals(W_base).real
    max_abs_eig = float(np.max(np.abs(eig_base)))

    WX = np.zeros((NT, K), dtype="float64")
    for t in range(T):
        X_t = X[t * N:(t + 1) * N, :]
        WX[t * N:(t + 1) * N, :] = W_base @ X_t

    with pm.Model() as sdm_model:
        X_data = pm.Data("X", X)
        WX_data = pm.Data("WX", WX)
        y_data = pm.Data("y", y)
        country_idx_data = pm.Data("country_idx", country_idx)
        year_idx_data = pm.Data("year_idx", year_idx)
        W_base_data = pm.Data("W_base", W_base)
        eig_base_data = pm.Data("eig_base", eig_base)

        beta = pm.Normal("beta", 0.0, 5.0, shape=K)
        gamma = pm.Normal("gamma", 0.0, 5.0, shape=K)

        mu_alpha = pm.Normal("mu_alpha", 0.0, 2.0)
        sigma_alpha = pm.HalfNormal("sigma_alpha", 2.0)
        alpha_raw = pm.Normal("alpha_raw", 0.0, 1.0, shape=N)
        alpha = pm.Deterministic("alpha", mu_alpha + sigma_alpha * alpha_raw)

        time_alpha_raw = pm.Normal("time_alpha_raw", 0.0, 1.0, shape=T)
        time_alpha = pm.Deterministic("time_alpha", time_alpha_raw * 2.0)

        eta = pm.Normal("eta", 0.0, 1.0)
        rho = pm.Deterministic("rho", 0.95 * pt.tanh(eta))

        sigma = pm.HalfNormal("sigma", 2.0)

        XB = pt.dot(X_data, beta) + pt.dot(WX_data, gamma) + alpha[country_idx_data] + time_alpha[year_idx_data]

        y_matrix = pt.reshape(y_data, (T, N))
        A_base = pt.eye(N) - rho * W_base_data
        Ay = pt.reshape(pt.dot(y_matrix, A_base.T), (T * N,))

        eps = Ay - XB

        log_det = T * pt.sum(pt.log(1.0 - rho * eig_base_data))
        ll_const = -0.5 * NT * (pt.log(2.0 * np.pi) + 2.0 * pt.log(sigma))
        ll_quad = -0.5 * pt.sum(eps**2) / (sigma**2)

        pm.Potential("sdm_loglik", ll_const + ll_quad + log_det)

        penalty = pt.switch(pt.lt(pt.abs(rho) * max_abs_eig, 0.9999), 0.0, -1.0e6)
        pm.Potential("stability_penalty", penalty)

        trace = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            target_accept=target_accept,
            max_treedepth=15,
            return_inferencedata=True,
            random_seed=random_seed,
            cores=cores,
            progressbar=progressbar,
        )

    return trace, countries_sorted, years_sorted, W_base


def loco_cv(
    df: pd.DataFrame,
    W_df: pd.DataFrame,
    draws: int = 1000,
    tune: int = 1000,
    chains: int = 2,
    target_accept: float = 0.95,
    random_seed: int | None = 123,
    cores: int | None = None,
    progressbar: bool = True,
) -> pd.DataFrame:
    """
    Leave-One-Country-Out (LOCO) cross-validation for SDM.

    For each country c:
    - Remove c from the panel and from W (rows/columns).
    - Row-standardize the shrunken W.
    - Fit the SDM on the remaining countries.
    - Record posterior means of rho, beta, gamma.

    This LOCO implementation is primarily intended to assess parameter sensitivity
    to leaving out a country, rather than to produce out-of-sample predictions for
    the left-out country (which is more subtle for spatial models).

    Parameters
    ----------
    df : pd.DataFrame
        Panel data with columns ['country','year', covariates..., 'inbound'].
    W_df : pd.DataFrame
        Weight matrix aligned to df countries.
    draws, tune, chains, target_accept : see run_sdm_model
        Sampling configuration.
    random_seed : int | None
        Seed for reproducibility across folds. (Each fold uses the same seed; if you
        prefer different seeds per fold, modify inside the loop.)
    cores : int | None
        Number of CPU cores used by PyMC.
    progressbar : bool
        Show progress bars.

    Returns
    -------
    pd.DataFrame
        One row per left-out country with columns:
        ['left_out','status','rho_mean','beta_0'..,'gamma_0'..]
    """
    years = sorted(df["year"].astype(int).unique())
    all_countries = sorted(df["country"].unique())
    results: list[dict] = []

    for left_out in all_countries:
        keep = [c for c in all_countries if c != left_out]

        df_tr = make_balanced_panel(df, keep, years)
        if df_tr.shape[0] != len(years) * len(keep):
            results.append({"left_out": left_out, "status": "skipped_unbalanced"})
            continue

        W_tr = shrink_W(W_df, keep)
        W_tr_df = pd.DataFrame(W_tr, index=keep, columns=keep)

        trace, _, _, _ = run_sdm_model(
            df_tr,
            W_tr_df,
            draws=draws,
            tune=tune,
            chains=chains,
            target_accept=target_accept,
            random_seed=random_seed,
            cores=cores,
            progressbar=progressbar,
        )

        rho_mean = trace.posterior["rho"].mean(dim=("chain", "draw")).item()
        beta_mean = trace.posterior["beta"].mean(dim=("chain", "draw")).values
        gamma_mean = trace.posterior["gamma"].mean(dim=("chain", "draw")).values

        row = {"left_out": left_out, "status": "ok", "rho_mean": rho_mean}
        row.update({f"beta_{i}": float(beta_mean[i]) for i in range(len(beta_mean))})
        row.update({f"gamma_{i}": float(gamma_mean[i]) for i in range(len(gamma_mean))})
        results.append(row)

    return pd.DataFrame(results)

def summarize_sdm_trace(trace, countries_sorted, years_sorted, round_to=4, verbose=True):
    """
    Summarize posterior results from the SDM model.

    Parameters
    ----------
    trace : arviz.InferenceData
        Posterior samples from run_sdm_model.
    countries_sorted : list[str]
        Country names in the model's panel order.
    years_sorted : list[int]
        Years in the model's panel order.
    round_to : int, default=4
        Decimals used in the ArviZ summary table.
    verbose : bool, default=True
        If True, prints tables to stdout.

    Returns
    -------
    summary_main : pd.DataFrame
        Summary of main coefficients: rho, beta, gamma, sigma.
    df_alpha : pd.DataFrame
        Posterior mean and SD of country effects (alpha).
    df_time_alpha : pd.DataFrame
        Posterior mean and SD of time effects (time_alpha).
    """
    summary_main = az.summary(
        trace, var_names=["rho", "beta", "gamma", "sigma"], round_to=round_to
    )

    alpha_post = trace.posterior["alpha"]
    alpha_mean = alpha_post.mean(dim=("chain", "draw")).values
    alpha_sd = alpha_post.std(dim=("chain", "draw")).values

    time_post = trace.posterior["time_alpha"]
    time_mean = time_post.mean(dim=("chain", "draw")).values
    time_sd = time_post.std(dim=("chain", "draw")).values

    df_alpha = pd.DataFrame({
        "country": countries_sorted,
        "alpha_mean": alpha_mean,
        "alpha_sd": alpha_sd
    })

    df_time_alpha = pd.DataFrame({
        "year": years_sorted,
        "time_alpha_mean": time_mean,
        "time_alpha_sd": time_sd
    })

    if verbose:
        print("Main coefficients summary:\n", summary_main)
        print("\nCountry effects (alpha):\n", df_alpha)
        print("\nTime effects (time_alpha):\n", df_time_alpha)

    return summary_main, df_alpha, df_time_alpha

