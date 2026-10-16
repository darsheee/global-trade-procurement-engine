"""
FastAPI Micro-SaaS Engine: EU CBAM & Green Trade Compliance
Vistara Trade Acceleration & Compliance Desk (2026)

Implements Regulation (EU) 2023/956 and Implementing Regulation (EU) 2023/1773.
Provides:
1. Scope 1 & Scope 2 Embedded Emissions Calculator
2. European Commission CBAM Transitional Registry XML Generator
3. Digital Product Passport (DPP) GS1 Data-Carrier Link Generator
4. Database Integration with 28 Steel/Metal Exporters in india_usa_trade.db
"""

import os
import sqlite3
import re
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from compliance.cbam.calculator import CBAMCalculator, DEFAULT_BENCHMARKS, INDIA_GRID_EMISSION_FACTOR
from compliance.cbam.xml_generator import generate_cbam_declaration_xml
from compliance.rules_of_origin.engine import RulesOfOriginEngine, FTA_CONFIGS
from agents.tender_scout_agent import TenderScoutAgent

app = FastAPI(
    title="EU CBAM & Green Trade Compliance Engine",
    version="1.0.0",
    description="Automated Scope 1/2 carbon accounting, XML registry generation, and exporter targeting for EU CBAM 2026 compliance."
)

DB_PATH = "/Volumes/Engima/india_usa_trade_data/db/india_usa_trade.db"

# --- Pydantic Data Models ---

class CBAMCalculationRequest(BaseModel):
    product_category: str = Field(..., example="steel_rebar", description="Product category: steel_crude, steel_rebar, aluminum_unwrought, aluminum_extrusion, cement_clinker, fertilizer_ammonia")
    production_volume_tons: float = Field(..., gt=0, example=500.0, description="Quarterly production or shipment volume in metric tons")
    fuel_consumption_mwh: float = Field(..., ge=0, example=1200.0, description="Total fuel consumed in MWh")
    fuel_carbon_factor: float = Field(0.202, ge=0, example=0.202, description="Fuel carbon emission factor (tCO2/MWh, default 0.202 for natural gas)")
    process_emissions_tco2: float = Field(0.0, ge=0, example=80.0, description="Direct chemical process emissions in tCO2")
    electricity_consumed_mwh: float = Field(0.0, ge=0, example=350.0, description="Electricity consumed from grid in MWh")
    carbon_price_paid_eur: float = Field(0.0, ge=0, example=0.0, description="Carbon price already paid in country of origin (INR converted to EUR)")
    eu_ets_allowance_eur_per_tco2: float = Field(65.0, gt=0, example=65.0, description="Current EU ETS carbon allowance price in EUR/tCO2")

class DeclarantInfo(BaseModel):
    eori_number: str = Field("NL123456789", example="NL123456789")
    company_name: str = Field("EU Importer B.V.", example="EU Importer B.V.")
    country: str = Field("NL", example="NL")

class InstallationInfo(BaseModel):
    name: str = Field("Indian Steel & Alloys Ltd", example="Indian Steel & Alloys Ltd")
    city: str = Field("Jamshedpur", example="Jamshedpur")
    cn_code: str = Field("72142000", example="72142000")
    lat: str = Field("22.8046", example="22.8046")
    lon: str = Field("86.2029", example="86.2029")

class CBAMReportRequest(BaseModel):
    declarant: DeclarantInfo
    installation: InstallationInfo
    calculation: CBAMCalculationRequest

class DPPRequest(BaseModel):
    company_name: str = Field(..., example="Tata Special Steels")
    product_name: str = Field(..., example="Low-Carbon Reinforcing Steel Bar")
    gtin: str = Field(..., example="8901234567890", description="Global Trade Item Number")
    serial_batch: str = Field(..., example="BATCH-2026-Q3-001")
    cn_code: str = Field(..., example="72142000")
    recycled_content_pct: float = Field(25.0, ge=0, le=100)
    carbon_intensity_tco2_per_ton: float = Field(1.146, ge=0)

# --- Endpoints ---

@app.get("/")
def root():
    return {
        "service": "EU CBAM & Green Compliance Micro-SaaS",
        "regulation": "Regulation (EU) 2023/956",
        "phase": "Definitive Payment Phase 2026",
        "endpoints": [
            "/api/v1/cbam/calculate",
            "/api/v1/cbam/generate-xml",
            "/api/v1/cbam/exporters",
            "/api/v1/cbam/pitch/{company_name}",
            "/api/v1/cbam/dpp/generate"
        ]
    }

@app.post("/api/v1/cbam/calculate")
def calculate_cbam(req: CBAMCalculationRequest):
    """
    Computes Scope 1, Scope 2, Total Embedded Emissions, and EU CBAM Certificate Liability.
    """
    calc = CBAMCalculator(grid_factor=INDIA_GRID_EMISSION_FACTOR)
    try:
        res = calc.calculate_embedded_emissions(
            product_category=req.product_category,
            production_volume_tons=req.production_volume_tons,
            fuel_consumption_mwh=req.fuel_consumption_mwh,
            fuel_carbon_factor=req.fuel_carbon_factor,
            process_emissions_tco2=req.process_emissions_tco2,
            electricity_consumed_mwh=req.electricity_consumed_mwh,
            carbon_price_paid_eur=req.carbon_price_paid_eur,
            eu_ets_allowance_eur_per_tco2=req.eu_ets_allowance_eur_per_tco2
        )
        return {"status": "success", "data": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/cbam/generate-xml")
def generate_xml(req: CBAMReportRequest):
    """
    Generates European Commission CBAM Transitional Registry-compliant XML.
    """
    calc = CBAMCalculator()
    emissions = calc.calculate_embedded_emissions(
        product_category=req.calculation.product_category,
        production_volume_tons=req.calculation.production_volume_tons,
        fuel_consumption_mwh=req.calculation.fuel_consumption_mwh,
        fuel_carbon_factor=req.calculation.fuel_carbon_factor,
        process_emissions_tco2=req.calculation.process_emissions_tco2,
        electricity_consumed_mwh=req.calculation.electricity_consumed_mwh,
        carbon_price_paid_eur=req.calculation.carbon_price_paid_eur,
        eu_ets_allowance_eur_per_tco2=req.calculation.eu_ets_allowance_eur_per_tco2
    )

    xml_content = generate_cbam_declaration_xml(
        declarant_info=req.declarant.dict(),
        installation_info=req.installation.dict(),
        emission_data=emissions
    )

    return {
        "status": "success",
        "xml_report": xml_content,
        "summary": {
            "total_embedded_tco2": emissions["total_embedded_tco2"],
            "gross_liability_eur": emissions["gross_cbam_liability_eur"],
            "reporting_period": "2026-Q3"
        }
    }

@app.get("/api/v1/cbam/exporters")
def list_target_steel_exporters(limit: int = Query(30, ge=1, le=100)):
    """
    Queries local india_usa_trade.db for Indian exporters in Metal & Articles of Metal
    subject to EU CBAM regulations.
    """
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Local trade database not found")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT supplier_id, company_name, iec_code, city, state_name, deal_in, 
               is_star_exporter, total_products, catalog_listed_products
        FROM exporters
        WHERE industry_category LIKE '%Metal%' 
           OR industry_category LIKE '%Engineering%'
           OR deal_in LIKE '%Steel%'
        ORDER BY is_star_exporter DESC, total_products DESC
        LIMIT ?;
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    exporters = []
    for r in rows:
        exporters.append({
            "supplier_id": r[0],
            "company_name": r[1],
            "iec_code": r[2],
            "location": f"{r[3]}, {r[4]}",
            "deal_in": r[5],
            "is_star_exporter": bool(r[6]),
            "total_products": r[7],
            "catalog_listed_products": r[8],
            "cbam_applicable": True,
            "target_sectors": ["Steel Products (HS 72, 73)", "Aluminium Articles (HS 76)"]
        })

    return {
        "status": "success",
        "count": len(exporters),
        "target_exporters": exporters
    }

@app.get("/api/v1/cbam/pitch/{company_name}")
def generate_exporter_pitch(company_name: str):
    """
    Generates a personalized CBAM Compliance & Retainer Pitch for a specific Indian manufacturer.
    """
    clean_name = company_name.strip()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT company_name, iec_code, city, state_name, total_products
        FROM exporters
        WHERE company_name LIKE ?
        LIMIT 1;
    """, (f"%{clean_name}%",))
    row = cursor.fetchone()
    conn.close()

    if not row:
        target_name = clean_name
        city = "Delhi NCR"
        iec = "PENDING"
    else:
        target_name = row[0]
        iec = row[1]
        city = f"{row[2]}, {row[3]}"

    email_subject = f"Mandatory EU CBAM Carbon Compliance: Avoiding 25% Customs Border Tariffs on {target_name}'s European Shipments"

    email_body = f"""Dear Managing Director / CFO,

I am writing regarding {target_name}'s metal and engineering export shipments to the European Union under IEC {iec}.

As of 2026, the European Union's Carbon Border Adjustment Mechanism (EU CBAM) has entered its definitive enforcement phase. European importers of steel, iron, and aluminium products (HS Codes 72, 73, and 76) are now legally required to submit verified quarterly embedded carbon declarations (Scope 1 and Scope 2 emissions) and purchase CBAM certificates.

The Immediate Threat:
If {target_name} does not provide verified plant-level embedded carbon data (in compliant European Commission XML format), EU customs applies punitive default carbon values. This will impose an estimated €65–€85/ton border penalty (20% to 35% tariff-equivalent surcharge) on your European buyers, making your shipments uncompetitive compared to compliant competitors.

Our Solution (Vistara Green Trade Desk):
1. Plant Carbon Audit: We compute your exact Scope 1 (fuel/furnace) and Scope 2 (grid electricity) specific emissions per ton using CEA-certified emission factors.
2. Official XML Registry Filing: We generate validated CBAM quarterly declarations formatted for direct upload to the European Commission Transitional Registry.
3. Buyer Retainer Pass-Through: We coordinate directly with your German, Dutch, and Italian importers' customs brokers.

Our Fee: Fixed retainer of ₹45,000 (€500) per quarterly declaration (vs. Big-4 consultancies charging €25,000+).

Could we schedule a 10-minute briefing call this Thursday at 3:30 PM to run a sample carbon calculation on your primary export product?

Warm regards,
[Founder Name]
Principal Trade Facilitation Partner | Vistara Trade Acceleration Desk
GIFT City & New Delhi Corridor Liaison
WhatsApp/Phone: +91-XXXXXXXXXX"""

    return {
        "status": "success",
        "company_name": target_name,
        "iec_code": iec,
        "location": city,
        "email_subject": email_subject,
        "email_pitch": email_body,
        "quarterly_retainer_inr": 45000,
        "quarterly_retainer_eur": 500
    }

@app.post("/api/v1/cbam/dpp/generate")
def generate_dpp(req: DPPRequest):
    """
    Generates an EU Digital Product Passport (DPP) data carrier payload complying with
    GS1 Digital Link URI specifications and the Ecodesign for Sustainable Products Regulation (ESPR).
    """
    # GS1 Digital Link standard URI
    gs1_uri = f"https://dpp.vistaratrade.com/01/{req.gtin}/21/{req.serial_batch}"

    dpp_payload = {
        "@context": ["https://schema.org", "https://gs1.org/voc/"],
        "type": "DigitalProductPassport",
        "dpp_version": "1.0-ESPR",
        "gs1_digital_link": gs1_uri,
        "identification": {
            "gtin": req.gtin,
            "serial_or_batch": req.serial_batch,
            "product_name": req.product_name,
            "manufacturer": req.company_name,
            "country_of_origin": "IN",
            "cn_code": req.cn_code
        },
        "environmental_footprint": {
            "carbon_intensity_tco2_per_ton": req.carbon_intensity_tco2_per_ton,
            "recycled_content_percentage": req.recycled_content_pct,
            "cbam_scope1_scope2_declared": True,
            "lifecycle_standard": "ISO 14067 / GHG Protocol"
        },
        "circularity_and_durability": {
            "recyclability_score": "Class A (100% Recyclable Steel/Metal)",
            "hazardous_substances_declared": False,
            "reach_compliant": True
        },
        "verification": {
            "issuer": "Vistara Trade Acceleration & Compliance Desk",
            "issued_at": datetime.utcnow().isoformat() + "Z",
            "verification_status": "Self-Declared & Audit Ready"
        }
    }

    return {
        "status": "success",
        "gs1_digital_link": gs1_uri,
        "dpp_payload": dpp_payload
    }

# --- Rules of Origin (RoO) Endpoints & Models ---

class BOMItem(BaseModel):
    name: str = Field(..., example="Imported Alloy Ingot")
    hs_code: str = Field(..., example="720211")
    value_usd: float = Field(..., ge=0, example=150.0)
    originating: bool = Field(False, example=False, description="True if sourced domestically from India or treaty partner")

class RoOEvaluationRequest(BaseModel):
    fta_agreement: str = Field("India-UK CETA", example="India-UK CETA", description="Trade agreement: India-UK CETA, India-UAE CEPA, India-Australia ECTA, India-EFTA TEPA")
    finished_hs_code: str = Field(..., example="721420", description="Finished product 6-digit HS subheading")
    fob_price_usd: float = Field(..., gt=0, example=1000.0, description="Free on Board (FOB) invoice price in USD")
    bill_of_materials: List[BOMItem]
    min_va_override: Optional[float] = Field(None, description="Optional override for minimum value addition %")
    de_minimis_pct: float = Field(10.0, ge=0, le=20, example=10.0, description="De Minimis tolerance % for non-originating inputs failing CTSH")

@app.get("/api/v1/roo/ftas")
def list_supported_ftas():
    """
    Returns supported Free Trade Agreements and statutory preferential rules.
    """
    return {
        "status": "success",
        "supported_agreements": FTA_CONFIGS
    }

@app.post("/api/v1/roo/evaluate")
def evaluate_rules_of_origin(req: RoOEvaluationRequest):
    """
    Evaluates Rules of Origin (RoO) compliance under India-UK CETA, UAE CEPA, Australia ECTA, or EFTA TEPA.
    Computes domestic Value Addition %, CTSH compliance, and generates DGFT e-CoO readiness status.
    """
    engine = RulesOfOriginEngine(
        fta_name=req.fta_agreement,
        min_va_pct=req.min_va_override,
        de_minimis_pct=req.de_minimis_pct
    )
    try:
        bom_dicts = [item.dict() for item in req.bill_of_materials]
        result = engine.evaluate_origin(
            finished_hs_code=req.finished_hs_code,
            fob_price_usd=req.fob_price_usd,
            bill_of_materials=bom_dicts
        )
        return {
            "status": "success",
            "origin_evaluation": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Public Procurement & GeM CPSE 4% Quota Endpoints ---

@app.get("/api/v1/gem/tenders")
def list_cpse_reserved_tenders(sector: Optional[str] = None):
    """
    Returns active Central Public Sector Enterprise (CPSE) tenders subject to the mandatory 4% SC/ST quota on GeM.
    Calculates 100% NSIC SPRS EMD waiver cash savings and matches candidate back-to-back manufacturing factories.
    """
    scout = TenderScoutAgent(db_path=DB_PATH)
    results = scout.scout_sc_reserved_tenders(sector_filter=sector)
    return {
        "status": "success",
        "sovereign_policy": "Public Procurement Policy for MSEs Order 2012 (4% SC/ST Quota)",
        "count": len(results),
        "tenders": results
    }
