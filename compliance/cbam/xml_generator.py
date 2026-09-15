"""
EU CBAM Transitional Registry XML Generator
Compliant with European Commission CBAM Implementing Regulation (EU) 2023/1773.
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from typing import Dict, Any

def generate_cbam_declaration_xml(declarant_info: Dict[str, str], installation_info: Dict[str, str], emission_data: Dict[str, Any]) -> str:
    root = ET.Element("CBAMQuarterlyReport", {
        "xmlns": "urn:eu:ec:cbam:v1",
        "reportId": f"CBAM-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "reportingPeriod": "2026-Q3"
    })

    # Header / Declarant Info
    declarant = ET.SubElement(root, "Declarant")
    ET.SubElement(declarant, "EORINumber").text = declarant_info.get("eori_number", "NL123456789")
    ET.SubElement(declarant, "CompanyName").text = declarant_info.get("company_name", "EU Importer B.V.")
    ET.SubElement(declarant, "CountryCode").text = declarant_info.get("country", "NL")

    # Installation / Indian Manufacturer
    installation = ET.SubElement(root, "ProductionInstallation")
    ET.SubElement(installation, "InstallationName").text = installation_info.get("name", "Indian Steel & Alloys Ltd")
    ET.SubElement(installation, "CountryCode").text = "IN"
    ET.SubElement(installation, "City").text = installation_info.get("city", "Jamshedpur")
    ET.SubElement(installation, "Latitude").text = str(installation_info.get("lat", "22.8046"))
    ET.SubElement(installation, "Longitude").text = str(installation_info.get("lon", "86.2029"))

    # Goods & Emissions
    goods = ET.SubElement(root, "ImportedGoods")
    ET.SubElement(goods, "CNCode").text = installation_info.get("cn_code", "72142000") # Concrete reinforcing bars
    ET.SubElement(goods, "QuantityMetricTons").text = str(emission_data.get("production_volume_tons", 0))
    
    emissions = ET.SubElement(goods, "EmbeddedEmissions")
    ET.SubElement(emissions, "SpecificDirectEmissions").text = str(round(emission_data.get("scope1_direct_tco2", 0) / max(emission_data.get("production_volume_tons", 1), 1), 4))
    ET.SubElement(emissions, "SpecificIndirectEmissions").text = str(round(emission_data.get("scope2_indirect_tco2", 0) / max(emission_data.get("production_volume_tons", 1), 1), 4))
    ET.SubElement(emissions, "TotalSpecificEmbeddedEmissions").text = str(emission_data.get("specific_emissions_tco2_per_ton", 0))
    ET.SubElement(emissions, "TotalGrossLiabilityEUR").text = str(emission_data.get("gross_cbam_liability_eur", 0))

    xml_str = ET.tostring(root, encoding="utf-8")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
    return pretty_xml

if __name__ == "__main__":
    declarant = {"eori_number": "DE987654321", "company_name": "Hamburg Metal Importers GmbH", "country": "DE"}
    installation = {"name": "Tata Special Steels Division", "city": "Jamshedpur", "cn_code": "72142000"}
    emissions = {"production_volume_tons": 500.0, "scope1_direct_tco2": 322.4, "scope2_indirect_tco2": 250.6, "specific_emissions_tco2_per_ton": 1.146, "gross_cbam_liability_eur": 37245.0}
    xml_out = generate_cbam_declaration_xml(declarant, installation, emissions)
    print("=== Generated Sample EU CBAM XML Declaration ===")
    print(xml_out[:400] + "...")
