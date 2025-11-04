## 📊 Data Sources and Usage in Model

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

5. **UNESCO World Heritage Sites (total number)**  
   **Source**: UNESCO World Heritage Centre  
   **URL**: [https://whc.unesco.org/en/list/](https://whc.unesco.org/en/list/)  
   **Used in model**: *Not included directly*

6. **Air transport, passengers carried**  
   **Source**: World Bank (assumed)  
   **Description**: Number of passengers carried by air transport.  
   **Used in model**: *ln-transformed*

7. **`politunesco` (interaction term)**  
   **Description**: Interaction between Political Stability and number of UNESCO World Heritage Sites.  
   **Used in model**: *As a constructed interaction term*

8. **Rule of Law**
  **Source**: Worldwide Governance Indicators (World Bank)
  **Description**: This indicator reflects perceptions of the extent to which agents have confidence in and abide by the rules of society, including the quality of contract enforcement, property rights, the police, and the courts, as well as the likelihood of crime and violence.
  **Used in model**: Raw score or standardized score (specify if applicable)


```python

```
