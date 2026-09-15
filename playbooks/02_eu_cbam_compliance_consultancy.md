# Playbook 02: EU CBAM & Cross-Border Carbon Compliance Advisory

## 1. The Market Opportunity
The European Union's Carbon Border Adjustment Mechanism (CBAM - Regulation EU 2023/956) levies a border tax on carbon-intensive imports into the EU:
- Covered Sectors: Steel, Aluminum, Cement, Fertilizers, Hydrogen, Electricity.
- High Pain Point: Over 4,000 Indian industrial exporters face severe penalties or customs blockages if they fail to report quarterly Scope 1 and Scope 2 embedded emissions in the prescribed EU XML format.
- Value Proposition: Indian SMEs lack expensive ESG consulting teams (Big 4 charge ₹15–₹40 Lakhs per plant). Our software-driven engine calculates emissions and generates the compliant XML filing in minutes for ₹50,000–₹1,50,000 per filing.

---

## 2. Calculation Methodology (Scope 1 & Scope 2)
1. **Scope 1 (Direct Emissions)**:
   $$\text{Scope 1} = \sum (\text{Fuel Consumption } [MWh] \times \text{Fuel Carbon Factor}) + \text{Direct Process Emissions } [tCO_2e]$$
2. **Scope 2 (Indirect Electricity Emissions)**:
   $$\text{Scope 2} = \text{Electricity Consumed } [MWh] \times \text{Grid Emission Factor } (0.716 \text{ tCO}_2e/MWh \text{ India CEA default})$$
3. **Specific Embedded Emissions**:
   $$\text{SEE} = \frac{\text{Scope 1} + \text{Scope 2}}{\text{Total Production Metric Tons}}$$

---

## 3. Execution & Monetization Model
- **Tier 1 (Automated Dossier Generation)**: Exporter inputs fuel bills and production data into `/cbam`; system outputs validated XML + PDF audit report for €499 / ₹45,000 per quarter.
- **Tier 2 (Decarbonization & Renewable Offset Advisory)**: Recommending captive solar PPA or biochar offsets to reduce the CBAM tax delta.
