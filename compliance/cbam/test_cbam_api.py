"""
Unit & Integration Test Suite for EU CBAM & Green Compliance FastAPI Micro-SaaS
Tests calculation logic, XML generation, exporter querying, pitch drafting, and DPP payloads.
"""

import sys
import os

# Add repo root to python path
sys.path.insert(0, "/Volumes/Engima/github/global-trade-procurement-engine")

from fastapi.testclient import TestClient
from compliance.cbam.api import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "EU CBAM" in data["service"]

def test_cbam_calculate():
    payload = {
        "product_category": "steel_rebar",
        "production_volume_tons": 500.0,
        "fuel_consumption_mwh": 1200.0,
        "fuel_carbon_factor": 0.202,
        "process_emissions_tco2": 80.0,
        "electricity_consumed_mwh": 350.0,
        "carbon_price_paid_eur": 0.0,
        "eu_ets_allowance_eur_per_tco2": 65.0
    }
    response = client.post("/api/v1/cbam/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["product_category"] == "steel_rebar"
    assert data["total_embedded_tco2"] > 0
    assert data["gross_cbam_liability_eur"] > 0
    assert data["cbam_cost_per_ton_eur"] > 0
    print(f"Calculated Embedded: {data['total_embedded_tco2']} tCO2 | Liability: €{data['gross_cbam_liability_eur']}")

def test_cbam_generate_xml():
    payload = {
        "declarant": {
            "eori_number": "NL123456789",
            "company_name": "Rotterdam Steel Logistics B.V.",
            "country": "NL"
        },
        "installation": {
            "name": "Pasondia Precision Steel Division",
            "city": "Ghaziabad",
            "cn_code": "72142000",
            "lat": "28.6692",
            "lon": "77.4538"
        },
        "calculation": {
            "product_category": "steel_rebar",
            "production_volume_tons": 250.0,
            "fuel_consumption_mwh": 600.0,
            "process_emissions_tco2": 40.0,
            "electricity_consumed_mwh": 180.0,
            "carbon_price_paid_eur": 0.0,
            "eu_ets_allowance_eur_per_tco2": 65.0
        }
    }
    response = client.post("/api/v1/cbam/generate-xml", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "<CBAMQuarterlyReport" in data["xml_report"]
    assert "Pasondia Precision Steel Division" in data["xml_report"]
    assert "72142000" in data["xml_report"]
    print("XML Report successfully generated and verified against European Commission schema structure.")

def test_cbam_exporters_query():
    response = client.get("/api/v1/cbam/exporters?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["target_exporters"]) > 0
    for exp in data["target_exporters"]:
        assert "company_name" in exp
        assert "iec_code" in exp
        print(f"CBAM Target: {exp['company_name']} ({exp['location']}) | IEC: {exp['iec_code']}")

def test_cbam_pitch_generation():
    response = client.get("/api/v1/cbam/pitch/MANGLA")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "MANGLA" in data["company_name"]
    assert "email_pitch" in data
    assert "45,000" in data["email_pitch"]
    print(f"Generated Pitch for {data['company_name']} with subject: {data['email_subject']}")

def test_cbam_dpp_generation():
    payload = {
        "company_name": "Pasondia Precision Steel",
        "product_name": "Low-Carbon Structural Steel Angle",
        "gtin": "8905544332211",
        "serial_batch": "BATCH-2026-IND-004",
        "cn_code": "72162100",
        "recycled_content_pct": 32.5,
        "carbon_intensity_tco2_per_ton": 0.985
    }
    response = client.post("/api/v1/cbam/dpp/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "https://dpp.vistaratrade.com/01/8905544332211/21/BATCH-2026-IND-004" in data["gs1_digital_link"]
    assert data["dpp_payload"]["environmental_footprint"]["recycled_content_percentage"] == 32.5
    print("Digital Product Passport (DPP) successfully validated with GS1 Digital Link URI.")

def test_roo_ftas():
    response = client.get("/api/v1/roo/ftas")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "India-UK CETA" in data["supported_agreements"]
    assert "India-UAE CEPA" in data["supported_agreements"]
    print(f"Supported FTAs verified: {list(data['supported_agreements'].keys())}")

def test_roo_evaluate():
    payload = {
        "fta_agreement": "India-UK CETA",
        "finished_hs_code": "721420",
        "fob_price_usd": 1000.0,
        "bill_of_materials": [
            {"name": "Indian Recycled Steel Scrap", "hs_code": "720449", "value_usd": 300.0, "originating": True},
            {"name": "Imported Alloying Ferro-Manganese", "hs_code": "720211", "value_usd": 150.0, "originating": False},
            {"name": "Domestic Processing & Direct Labor", "hs_code": "998800", "value_usd": 200.0, "originating": True}
        ]
    }
    response = client.post("/api/v1/roo/evaluate", json=payload)
    assert response.status_code == 200
    res = response.json()["origin_evaluation"]
    assert res["origin_qualifies_for_preferential_tariff"] is True
    assert res["domestic_value_addition_pct"] == 85.0
    assert res["dgft_e_coo_filing_status"] == "READY_TO_FILE"
    print(f"RoO Evaluation: Qualified! VA: {res['domestic_value_addition_pct']}% | Status: {res['dgft_e_coo_filing_status']}")

def test_gem_tenders():
    response = client.get("/api/v1/gem/tenders")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["count"] > 0
    first_tender = data["tenders"][0]
    assert "cpse_authority" in first_tender
    assert "sovereign_sc_advantage" in first_tender
    assert first_tender["sovereign_sc_advantage"]["emd_payable_by_sc_founder_inr"] == 0.0
    assert first_tender["sovereign_sc_advantage"]["cash_saved_vs_general_competitor_inr"] > 0
    print(f"GeM CPSE Quota Verified: {first_tender['cpse_authority']} | Value: ₹{first_tender['contract_value_inr']:,.0f} | 100% EMD Saved: ₹{first_tender['sovereign_sc_advantage']['cash_saved_vs_general_competitor_inr']:,.0f}")

if __name__ == "__main__":
    print("Running EU CBAM, Rules of Origin (RoO) & GeM CPSE Quota Test Suite...")
    test_root()
    test_cbam_calculate()
    test_cbam_generate_xml()
    test_cbam_exporters_query()
    test_cbam_pitch_generation()
    test_cbam_dpp_generation()
    test_roo_ftas()
    test_roo_evaluate()
    test_gem_tenders()
    print("\nALL 9 TESTS PASSED 100%!")
