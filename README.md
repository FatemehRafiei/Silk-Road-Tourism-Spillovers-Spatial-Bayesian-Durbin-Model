# 📚 Construction of Geographic, Trade, and Cultural Proximity Matrices  
## and Bayesian Spatial Durbin Model Workflow for Tourism Spillover Analysis

This repository accompanies the paper:

**“Construction of geographic, trade, and cultural proximity matrices and Bayesian Spatial Durbin Model workflow for tourism spillover analysis”**

This work is part of the project:

**Culture, Space, and Tourism Spillovers in the Silk Road**

The repository presents a **reproducible spatial econometric workflow** that integrates:

- Construction of three spatial weight matrices:
  - Geographic (inverse distance)
  - Trade-based
  - Cultural (linguistic & religious similarity)
- A **Bayesian Spatial Durbin Model (BSDM)** estimation framework
- A **nested CES utility model** linking domestic and international tourism consumption with spatial spillovers

---

## 🧭 Motivation

Tourism in the Silk Road region is shaped by complex spatial interdependencies across **geography, trade, and culture**.

This repository provides a computational framework to:

- Quantify tourism spillover effects  
- Compare different types of spatial connectivity  
- Reproduce Bayesian estimation results using public data  

---

## ⚙️ Repository Structure

To ensure correct indentation and rendering, the directory tree is shown in a single monospace code block:

```plaintext
silkroad-tourism-bayesian-spatial-model/
├── data/
│   ├── df_sorted.xlsx                 # Main panel dataset (country-year wide format)
│   ├── language.harvard.xlsx          # Linguistic proximity data
│   ├── religious.xlsx                 # Religious composition data (Pew Research)
│   ├── trade_2002_2019.xlsx           # Bilateral trade data (UN Comtrade)
│   ├── W_cul04.xlsx                   # Cultural proximity weight matrix
│   ├── W_cul05.xlsx                   # Cultural proximity weight matrix
│   ├── W_cul06.xlsx                   # Cultural proximity weight matrix
│   ├── W_geo.xlsx                    # Geographic distance weight matrix
│   ├── W_trade.xlsx                  # Trade-based weight matrix
│   └── README_data_sources.md        # Description of data sources
├── notebooks/
│   ├── geo_mod.ipynb                 # Bayesian SDM with geographic distance weights
│   ├── trade_mod.ipynb               # Bayesian SDM with trade-based weights
│   └── culture_mod.ipynb             # Bayesian SDM with cultural weights
├── sdm_model/
│   ├── __init__.py
│   ├── sdm_model.py
│   ├── posterior_predict.py
│   ├── morans_I.py
│   └── loco.py
├── docs/
├── LICENSE
└── README.md


## 🌍 Spatial Weight Matrices

This project develops and compares three types of spatial weight matrices (**W**).

### 1️⃣ Geographic (Inverse Distance)

- Based on geodesic distance between capital cities  
- Weights defined as:

\[
w_{ij} = \frac{1}{d_{ij}}
\]

- Row-normalized  

---

### 2️⃣ Trade-Based 


- Constructed annually using **UN Comtrade** bilateral export data  
- Reflects changing trade relationships (2002–2019)

---

### 3️⃣ Cultural (Language + Religion)

- **Linguistic proximity**  
  Gurevich et al. (2014) Linguistic Proximity Score  

- **Religious similarity**  
  Cosine similarity of Pew Research Center religious composition data  

- Composite cultural weight matrix:

\[
W_{ij}^{final} = \alpha W_{ij}^{lang} + (1 - \alpha) W_{ij}^{religion},
\quad \alpha = 0.5
\]


## 🧪 Robustness and Validation

Robustness is tested by varying the relative weight of linguistic and religious similarity:

\[
\alpha = 0.4,\; 0.5,\; 0.6
\]

Posterior means and **Highest Density Intervals (HDIs)** remain stable.

## 📊 Data Sources

The analysis relies on publicly available datasets:

- **UN Comtrade** – Bilateral trade data  
- **GeoNames** – Geographic coordinates  
- **Pew Research Center (2025)** – Religious composition  
- **Ethnologue / Gurevich et al. (2014)** – Linguistic similarity  

---

## 💻 Reproducibility

All scripts are written in **Python 3.10+** and rely on the following libraries:

- `pandas`
- `numpy`
- `geopy`
- `pymc`
- `matplotlib`
- `arviz`

### Reproduce the Results

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/silkroad-tourism-bayesian-spatial-model.git
cd silkroad-tourism-bayesian-spatial-model
## 📜 License

This project is licensed under the **MIT License**.  
You may use, modify, and distribute the code with proper attribution.

---

## 👩‍💻 Author

**Fatemeh Rafiei**

- Conceptualization  
- Methodology  
- Writing – Original Draft  
- Visualization  
- Validation  

📧 **Correspondence:**  
Fatemehrafiei@semnan.ac.ir

---

## 📚 Citation

If you use this repository, please cite:

> Rafiei, F. (2025). *Construction of geographic, trade, and cultural proximity matrices and Bayesian Spatial Durbin Model workflow for tourism spillover analysis*.  
> GitHub repository:  
> https://github.com/FatemehRafiei/silkroad-tourism-bayesian-spatial-model

