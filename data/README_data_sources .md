# 📊 Data Sources and Usage in Model

This document summarizes all datasets used in the paper  
**"Construction of Geographic, Trade, and Cultural Proximity Matrices and Bayesian Spatial Durbin Model Workflow for Tourism Spillover Analysis"**.

---

## 🧭 Economic and Tourism Indicators

1. **GDP per capita, PPP (constant 2021 international $)**  
   **Source**: World Bank  
   **Description**:  
   International Comparison Program, World Bank | World Development Indicators database, World Bank | Eurostat-OECD PPP Programme.  
   **Used in model**: *ln-transformed*

2. **International tourism, number of arrivals**  
   **Source**: World Bank  
   **Description**:  
   World Tourism Organization, *Yearbook of Tourism Statistics*, *Compendium of Tourism Statistics*, and data files.  
   **Used in model**: *ln-transformed (dependent variable)*

3. **Political Stability and Absence of Violence/Terrorism: Estimate**  
   **Source**: World Bank  
   **Description**:  
   Measures perceptions of the likelihood of political instability and/or politically-motivated violence, including terrorism.  
   The estimate represents the country's score on the aggregate indicator, expressed in standard normal units, ranging approximately from -2.5 (weak) to 2.5 (strong).  
   **Used in model**: *Raw form (not transformed)*

4. **Official exchange rate (LCU per US$, period average)**  
   **Source**: World Bank  
   **Description**:  
   International Monetary Fund, *International Financial Statistics*.  
   **Used in model**: *ln-transformed*

5. **Rule of Law**
  **Source**: Worldwide Governance Indicators (World Bank)
  **Description**: This indicator reflects perceptions of the extent to which agents have confidence in and abide by the rules of society, including the quality of contract enforcement, property rights, the police, and the courts, as well as the likelihood of crime and violence.
  **Used in model**: Raw score or standardized score (specify if applicable)

---

## 💼 Trade-Based Indicators

1. **Bilateral Trade Flows (Exports, current US$)**  
   **Source**: United Nations Comtrade Database  
   **URL**: [https://comtrade.un.org](https://comtrade.un.org)  
   **Description**:  
   Annual bilateral export data among Silk Road countries (2002–2019).  
   Used to construct **dynamic trade weight matrices (Wₜᵣₐdₑ,ₜ)**, capturing evolving economic linkages.  
   **Used in model**: *Row-normalized; time-varying weights.*  

2. **Trade-Based Spatial Matrix**  
   **Formula**:


$$
W_{trade,t}^{ij} = \frac{X_{ij,t}}{\sum_{j} X_{ij,t}}
$$

where $X_{ij,t}$ represents exports from country *i* to country *j* in year *t*.  
Each matrix is symmetric and normalized annually.




   
## 🌍 Cultural and Linguistic Indicators

1. **Religious Composition (2010–2020)**  
   **Source**: Pew Research Center  
   **URL**: [https://www.pewresearch.org/religion/feature/religious-composition-by-country-2010-2020/](https://www.pewresearch.org/religion/feature/religious-composition-by-country-2010-2020/)  
   **Description**:  
   Dataset of global religious composition estimates for 2010 and 2020. The dataset provides percentage distributions of seven major religious groups (Christians, Muslims, Unaffiliated, Hindus, Buddhists, Jews, and Others) for each country.  
   Used to calculate **cosine similarity** between countries’ religious compositions, forming the *religious proximity matrix (W₍religion₎)* used in the Bayesian Spatial Durbin Model.  
   **Used in model**: *Normalized vector representation; cosine similarity; symmetric matrix.*  
   **Citation**:  
   Hackett, Conrad, Marcin Stonawski, Yunping Tong, Stephanie Kramer, and Anne Fengyan Shi (2025).  
   *Dataset of Global Religious Composition Estimates for 2010 and 2020.* Pew Research Center.  
   DOI: [10.58094/vhrw-k516](https://doi.org/10.58094/vhrw-k516)

2. **Linguistic Proximity Score (LPS)**  
   **Source**: Gurevich et al. (2014), *Linguistic Proximity Database*  
   **Description**:  
   Measures the similarity between languages spoken across countries by accounting for both native and acquired languages as well as the depth of shared linguistic family branches.  
   The LPS matrix is symmetric and row-normalized (diagonal elements set to zero) to meet the requirements of spatial econometric modeling.  
   **Used in model**: *Row-normalized; used to construct the linguistic similarity matrix (W₍lang₎)*.  
   **Citation**:  
   Gurevich, T., Kenney, M., and Wurm, S. (2014). *Linguistic Proximity Database.* Harvard Dataverse.  

3. **Cultural Proximity Matrix (Final Composite)**  
   **Source**: Constructed variable based on linguistic and religious proximity matrices.  
   **Description**:  
   The final cultural proximity matrix combines linguistic and religious similarity using equal weights (α = 0.5).  
   This approach captures both linguistic and religious closeness among Silk Road countries, reflecting the multidimensional nature of cultural affinity.  
   **Formula**:  
   \( W_{cult} = 0.5W_{lang} + 0.5W_{religion} \)  
   **Used in model**: *Row-normalized; used in Bayesian Spatial Durbin Model to estimate cultural spillover effects.*


---


## 🗺️ Geographic Indicators

**Source**:  
Historical roles of the listed cities along the Silk Road corridor were compiled primarily from the [UNESCO World Heritage Centre](https://whc.unesco.org), accessed June 2025.  
The descriptions reflect each location’s historical significance as key nodes, trading hubs, or cultural centers in the Silk Road network.

### Table 5. Geographic Coordinates of Selected Silk Road Cities

| Country | City | Latitude (°N) | Longitude (°E) | Historical / Cultural Significance |
|----------|------|---------------|----------------|------------------------------------|
| **Azerbaijan** | Shamakhi | 40.6317 | 48.1482 | Cultural and commercial center during the Safavid and earlier periods |
| **China** | Xi'an | 34.3416 | 108.9398 | Starting point of the Silk Road; capital of the Tang Empire |
| **Egypt** | Fustat (Old Cairo) | 30.0060 | 31.2315 | Trade hub along southern Silk Road routes |
| **Georgia** | Kutaisi | 42.2679 | 42.7180 | Historic city on the Caucasus branch of the Silk Road |
| **India** | Leh, Ladakh | 34.1526 | 77.5770 | Main passage via Kashmir and Tibet; connection to Buddhist routes |
| **Iran** | Semnan | 35.5760 | 53.3950 | Central Silk Road section in Iran; key station between Rey and Damghan |
| **Italy** | Venice | 45.4408 | 12.3155 | Western terminus of the maritime Silk Road; key trade center with the East |
| **Kazakhstan** | Taraz | 42.9000 | 71.3667 | An important ancient center on the Central Asia Silk Road route |
| **Kyrgyzstan** | Tash Rabat | 41.1000 | 75.3500 | Significant caravanserai on the mountainous route |
| **Saudi Arabia** | Jeddah | 21.4858 | 39.1925 | A major port for maritime trade connected to the Maritime Silk Road |
| **Türkiye** | Kayseri | 38.7312 | 35.4787 | Central Anatolian city, key role in the Iran–Levant trade route |

---

These coordinates were used to compute the **geodesic distance matrix**, where the spatial weights are defined as:


**Formula:**

$$
w_{ij} = \frac{1}{d_{ij}}
$$

where $d_{ij}$ denotes the great-circle (geodesic) distance between countries *i* and *j*,  
and $w_{ij}$ represents the inverse-distance spatial weight.

Each weight $w_{ij}$ is computed as the reciprocal of the great-circle distance between country *i* and *j*, calculated using the `geopy` Python library.  
The resulting matrix is **row-normalized** so that the total influence of neighboring countries equals 1 for each observation.



## 🧾 Notes
- All variables are annual (2002–2019) and harmonized across 11 Silk Road countries.
- Raw data are stored in `/data/raw/` and processed datasets in `/data/processed/`.
- All data are publicly available and reproducible via open sources listed above.

---

**Author:**  
Fatemeh Rafiei  
*Conceptualization · Methodology · Data Curation · Writing – Original Draft*



```python

```
