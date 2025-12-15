📚 Construction of Geographic, Trade, and Cultural Proximity Matrices and Bayesian Spatial Durbin Model Workflow for Tourism Spillover AnalysisThis repository accompanies the paper "Construction of geographic, trade, and cultural proximity matrices and Bayesian Spatial Durbin Model workflow for tourism spillover analysis", which is part of the project Culture, Space, and Tourism Spillovers in the Silk Road.The project presents a reproducible spatial econometric workflow that integrates:The construction of three spatial weight matrices—geographic (inverse distance), trade-based, and cultural (linguistic & religious similarity).A Bayesian Spatial Durbin Model (BSDM) estimation framework.A nested CES utility model linking domestic and international tourism consumption with spatial spillovers.🧭 MotivationTourism in the Silk Road region is shaped by complex spatial interdependencies across geography, trade, and culture.This repository provides the computational framework to:Quantify tourism spillover effects,Compare different types of spatial connectivity,Reproduce Bayesian estimation results using public data.⚙️ Repository Structureبرای اطمینان از نمایش صحیح تورفتگی‌ها، ساختار درختی در یک بلاک کد تک‌فاصله قرار داده شده است.Plaintextsilkroad-tourism-bayesian-spatial-model/
├── data/
│   ├── df_sorted.xlsx                 # Main panel dataset (country-year wide format)
│   ├── language.harvard.xlsx          # Linguistic proximity data
│   ├── religious.xlsx                 # Religious composition data (Pew Research)
│   ├── trade_2002_2019.xlsx           # Bilateral trade data (UN Comtrade)
│   ├── W_cul04.xlsx                   # Cultural proximity weight matrix
│   ├── W_cul05.xlsx                   # Cultural proximity weight matrix
│   ├── W_cul06.xlsx                   # Cultural proximity weight matrix
│   ├── W_geo.xlsx                     # Geographic distance weight matrix
│   ├── W_trade.xlsx                   # Trade-based weight matrix
│   └── README_data_sources.md         # Description of data sources
├── notebooks/
│   ├── geo_mod.ipynb                  # Bayesian SDM with geographic distance weights
│   ├── trade_mod.ipynb                # Bayesian SDM with trade-based weights
│   └── culture_mod.ipynb              # Bayesian SDM with cultural (linguistic + religious) weights
├── sdm_model/                         # Python module with reusable functions
│   ├── __init__.py
│   ├── sdm_model.py
│   ├── posterior_predict.py
│   ├── morans_I.py
│   └── loco.py
├── docs/
├── LICENSE
└── README.md
🌍 Spatial Weight Matricesاین پروژه سه نوع ماتریس وزن فضایی (Spatial Weight Matrix - W) را توسعه داده و مقایسه می‌کند:Geographic (Inverse Distance)Based on geodesic distance between capital cities.Weights: $w_{ij} = 1 / d_{ij}$Row-normalized.Trade-Based (Dynamic)Constructed annually using UN Comtrade bilateral export data.Reflects changing trade relationships (2002 – 2019).Cultural (Language + Religion)Linguistic proximity: Gurevich et al. (2014) Linguistic Proximity Score.Religious similarity: Cosine similarity of Pew Research Center’s religious composition data.Final matrix (Composite W):$$W_{ij}^{final} = \alpha W_{ij}^{lang} + (1 - \alpha) W_{ij}^{religion}, \quad \alpha = 0.5$$🧪 Robustness and ValidationWe test robustness by altering the relative weight of linguistic and religious similarity:$\alpha = 0.4, 0.5, 0.6$Posterior means and HDIs for key parameters remain stable, confirming robustness.📊 Data SourcesThe analysis relies on several publicly available datasets:UN Comtrade – Bilateral trade dataGeoNames – Geographic coordinatesPew Research Center (2025) – Religious compositionEthnologue / Gurevich et al. (2014) – Linguistic similarity💻 ReproducibilityAll Python scripts are written in Python 3.10+ and use the following libraries:pandas, numpy, geopy, pymc, matplotlib, and arviz.To reproduce the results locally, follow these steps:Clone the repository and enter the directory:Bashgit clone https://github.com/YOUR_USERNAME/silkroad-tourism-bayesian-spatial-model.git
cd silkroad-tourism-bayesian-spatial-model
Install dependencies (requires a requirements.txt file):Bashpip install -r requirements.txt
Run the main estimation script:Bashpython scripts/04_bayesian_sdm_estimation.py
Note: The actual script name should be verified in the scripts/ directory.📜 LicenseThis project is licensed under the MIT License—you may use, modify, and distribute the code with proper attribution.👩‍💻 AuthorFatemeh RafieiConceptualization · Methodology · Writing – original draft · Visualization · ValidationFor correspondence: [Fatemehrafiei@semnan.ac.ir]📚 CitationIf you use this repository, please cite:Rafiei, F. (2025). Construction of geographic, trade, and cultural proximity matrices and Bayesian Spatial Durbin Model workflow for tourism spillover analysis.GitHub repository: https://github.com/FatemehRafiei/silkroad-tourism-bayesian-spatial-model
