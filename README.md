# 📚 Bayesian Spatial Durbin Model workflow for tourism spillover analysis using geographic, trade, and cultural matrices

This repository accompanies the paper:

**“Bayesian Spatial Durbin Model workflow for tourism spillover analysis using geographic, trade, and cultural matrices”**

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


## 🌍 Spatial Weight Matrices

This project develops and compares three types of spatial weight matrices (**W**).

### 1️⃣ Geographic (Inverse Distance)

- Based on geodesic distance between capital cities  
- Weights defined as:  

  `w_ij = 1 / d_ij`

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

  `W_ij = α · W_ij^lang + (1 − α) · W_ij^religion`, with `α = 0.5`

---

## 🧪 Robustness and Validation

Robustness is tested by varying the relative weight of linguistic and rel



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


