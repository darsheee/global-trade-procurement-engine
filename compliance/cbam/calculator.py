"""
EU CBAM (Carbon Border Adjustment Mechanism) Emission Calculation Engine
Implements EU Regulation 2023/956 for Indian Industrial Exporters.
Covers Steel, Aluminum, Cement, Fertilizers, and Hydrogen.
"""

from typing import Dict, Any, Optional

# Grid emission factors (tCO2e / MWh) - India CEA Benchmark
INDIA_GRID_EMISSION_FACTOR = 0.716

# Standard default embedded emission benchmarks (tCO2e / t product)
DEFAULT_BENCHMARKS = {
    "steel_crude": 1.85,
    "steel_rebar": 2.10,
    "aluminum_unwrought": 11.50, # High due to coal-fired captive smelters
    "aluminum_extrusion": 12.80,
    "cement_clinker": 0.82,
    "fertilizer_ammonia": 2.10
}

class CBAMCalculator:
    def __init__(self, grid_factor: float = INDIA_GRID_EMISSION_FACTOR):
        self.grid_factor = grid_factor

    def calculate_embedded_emissions(
        self,
        product_category: str,
        production_volume_tons: float,
        fuel_consumption_mwh: float,
        fuel_carbon_factor: float = 0.202, # Natural gas default tCO2 / MWh
        process_emissions_tco2: float = 0.0,
        electricity_consumed_mwh: float = 0.0,
        carbon_price_paid_eur: float = 0.0,
        eu_ets_allowance_eur_per_tco2: float = 65.0
    ) -> Dict[str, Any]:
        """
        Calculate Scope 1 (Direct), Scope 2 (Indirect), and Total Embedded Emissions.
        Computes the expected EU CBAM certificate liability.
        """
        if production_volume_tons <= 0:
            raise ValueError("Production volume must be greater than 0")

        # Scope 1: Fuel Combustion + Process Emissions
        scope1_fuel = fuel_consumption_mwh * fuel_carbon_factor
        scope1_total = round(scope1_fuel + process_emissions_tco2, 3)

        # Scope 2: Electricity Consumption * Grid Factor
        scope2_total = round(electricity_consumed_mwh * self.grid_factor, 3)

        # Total Embedded Emissions
        total_emissions = round(scope1_total + scope2_total, 3)
        specific_emissions = round(total_emissions / production_volume_tons, 4)

        # Benchmark comparison
        benchmark = DEFAULT_BENCHMARKS.get(product_category, 2.0)
        emissions_vs_benchmark = round(specific_emissions - benchmark, 4)

        # Financial liability in EU (CBAM Certificates needed)
        gross_liability_eur = round(total_emissions * eu_ets_allowance_eur_per_tco2, 2)
        net_liability_eur = max(round(gross_liability_eur - carbon_price_paid_eur, 2), 0.0)
        liability_per_ton_eur = round(net_liability_eur / production_volume_tons, 2)

        return {
            "product_category": product_category,
            "production_volume_tons": production_volume_tons,
            "scope1_direct_tco2": scope1_total,
            "scope2_indirect_tco2": scope2_total,
            "total_embedded_tco2": total_emissions,
            "specific_emissions_tco2_per_ton": specific_emissions,
            "eu_benchmark_tco2_per_ton": benchmark,
            "emissions_delta_vs_benchmark": emissions_vs_benchmark,
            "eu_ets_price_eur_per_ton": eu_ets_allowance_eur_per_tco2,
            "gross_cbam_liability_eur": gross_liability_eur,
            "effective_carbon_price_rebate_eur": carbon_price_paid_eur,
            "net_cbam_liability_eur": net_liability_eur,
            "cbam_cost_per_ton_eur": liability_per_ton_eur
        }

if __name__ == "__main__":
    calc = CBAMCalculator()
    res = calc.calculate_embedded_emissions(
        product_category="steel_rebar",
        production_volume_tons=500.0,
        fuel_consumption_mwh=1200.0,
        process_emissions_tco2=80.0,
        electricity_consumed_mwh=350.0,
        carbon_price_paid_eur=0.0
    )
    print("=== EU CBAM Carbon Compliance Calculation ===")
    for k, v in res.items():
        print(f"{k}: {v}")
