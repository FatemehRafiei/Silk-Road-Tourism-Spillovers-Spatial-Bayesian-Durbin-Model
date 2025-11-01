# Construction of Geographic, Trade, and Cultural Proximity Matrices and Bayesian Spatial Durbin Model Workflow for Tourism Spillover Analysis

This repository accompanies the paper **"Construction of geographic, trade, and cultural proximity matrices and Bayesian Spatial Durbin Model workflow for tourism spillover analysis"**, which is part of the project *Culture, Space, and Tourism Spillovers in the Silk Road*.

The project presents a **reproducible spatial econometric workflow** that integrates:
- The construction of **three spatial weight matrices** — geographic (inverse distance), trade-based (dynamic), and cultural (linguistic & religious similarity).
- A **Bayesian Spatial Durbin Model (BSDM)** estimation framework.
- A **nested CES utility model** linking domestic and international tourism consumption with spatial spillovers.

---

## 🧭 Motivation
Tourism in the Silk Road region is shaped by complex spatial interdependencies across geography, trade, and culture.  
This repository provides the computational framework to:
- Quantify tourism spillover effects,
- Compare different types of spatial connectivity,
- Reproduce Bayesian estimation results using public data.

---

## ⚙️ Repository Structure

silkroad-tourism-bayesian-spatial-model/
│
├── data/
│ ├── raw/ # Raw data: UN Comtrade, Pew Research, GeoNames, etc.
│ ├── processed/ # Cleaned and merged datasets
│
├── scripts/
│ ├── 01_build_distance_matrix.py
│ ├── 02_build_trade_matrix.py
│ ├── 03_build_cultural_matrix.py
│ ├── 04_bayesian_sdm_estimation.py
│ └── utils.py # Helper functions for preprocessing and diagnostics
│
├── results/
│ ├── posterior_estimates/
│ ├── figures/
│ └── tables/
│
├── docs/
│ ├── model_derivation.pdf
│ └── supplementary_figures/
│
└── README.md


## 🌍 Spatial Weight Matrices

### Geographic (Inverse Distance)
- Based on geodesic distance between capital cities.
- Weights: \( w_{ij} = 1 / d_{ij} \)
- Row-normalized.

### Trade-Based (Dynamic)
- Constructed annually using **UN Comtrade** bilateral export data.
- Reflects changing trade relationships (2002–2019).

### Cultural (Language + Religion)
- **Linguistic proximity:** Gurevich et al. (2014) Linguistic Proximity Score.  
- **Religious similarity:** Cosine similarity of Pew Research Center’s religious composition data.  
- Final matrix:  
  \[
  W_{ij}^{final} = α W_{ij}^{lang} + (1−α) W_{ij}^{religion}, \quad α = 0.5
  \]

---

## 🧪 Robustness and Validation
We test robustness by altering the relative weight of linguistic and religious similarity:
- α = 0.4, 0.5, 0.6  
Posterior means and HDIs for key parameters remain stable, confirming robustness.

---

## 📊 Data Sources
- **UN Comtrade** – Bilateral trade data  
- **GeoNames** – Geographic coordinates  
- **Pew Research Center (2025)** – Religious composition  
- **Ethnologue / Gurevich et al. (2014)** – Linguistic similarity  

All datasets are publicly available.

---

## 💻 Reproducibility
All Python scripts are written in **Python 3.10+** and use:
- `pandas`, `numpy`, `geopy`, `pymc`, `matplotlib`, and `arviz`.

To reproduce the results:
```bash
git clone https://github.com/YOUR_USERNAME/silkroad-tourism-bayesian-spatial-model.git
cd silkroad-tourism-bayesian-spatial-model
pip install -r requirements.txt
python scripts/04_bayesian_sdm_estimation.py


📜 License

This project is licensed under the MIT License — you may use, modify, and distribute the code with proper attribution.

👩‍💻 Author

Fatemeh Rafiei
Conceptualization · Methodology · Writing – original draft · Visualization · Validation

For correspondence: [Fatemehrafiei@semnan.ac.ir]

📚 Citation

If you use this repository, please cite:

Rafiei, F. (2025). Construction of geographic, trade, and cultural proximity matrices and Bayesian Spatial Durbin Model workflow for tourism spillover analysis.
GitHub repository: https://github.com/FatemehRafiei/silkroad-tourism-bayesian-spatial-model

