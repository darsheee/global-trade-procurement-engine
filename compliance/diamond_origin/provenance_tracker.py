"""
G7 Diamond Sanctions & Kimberley Process Origin Provenance Verification Engine
Compliant with G7 import requirements on rough and polished diamonds (HS Code 7102).
Ensures non-Russian origin, rough-to-cut audit trail, and Kimberley Process Certificate mapping.
"""

import json
from datetime import datetime
from typing import Dict, Any, List

class DiamondProvenanceTracker:
    def __init__(self):
        self.compliant_mining_countries = [
            "Botswana", "Canada", "South Africa", "Namibia", "Angola", "Australia", "India"
        ]
        self.restricted_origins = ["Russia", "Russian Federation"]

    def create_provenance_dossier(
        self,
        stock_number: str,
        carat_weight: float,
        shape_cut: str,
        color: str,
        clarity: str,
        rough_origin_country: str,
        rough_kpc_number: str, # Kimberley Process Certificate
        cutting_facility_name: str,
        cutting_city: str,
        lab_cert_type: str = "IGI", # IGI or GIA
        lab_cert_number: str = "",
        is_lab_grown: bool = True
    ) -> Dict[str, Any]:
        """Generate a full provenance dossier for US/EU customs compliance."""
        
        is_g7_compliant = True
        compliance_flags = []

        if not is_lab_grown:
            if rough_origin_country in self.restricted_origins:
                is_g7_compliant = False
                compliance_flags.append("RESTRICTED_ORIGIN: Diamond originates from G7-sanctioned territory.")
            elif rough_origin_country not in self.compliant_mining_countries:
                compliance_flags.append("UNVERIFIED_MINING_COUNTRY: Secondary provenance documentation required.")
            
            if not rough_kpc_number:
                is_g7_compliant = False
                compliance_flags.append("MISSING_KPC: Kimberley Process Certificate number required for natural stones.")
        else:
            compliance_flags.append("LAB_GROWN_DIAMOND: Exempt from G7 natural rough import restrictions. Full synthetic declaration required.")

        dossier = {
            "dossier_id": f"DIA-PROV-{stock_number}-{datetime.utcnow().strftime('%Y%m%d')}",
            "stock_number": stock_number,
            "diamond_classification": "Synthetic/Lab-Grown" if is_lab_grown else "Natural Mined",
            "specifications": {
                "carat": carat_weight,
                "cut": shape_cut,
                "color": color,
                "clarity": clarity
            },
            "custody_chain": {
                "rough_origin": rough_origin_country if not is_lab_grown else "CVD/HPHT Reactor Facility (Surat, India)",
                "kimberley_cert": rough_kpc_number if not is_lab_grown else "N/A (Synthetic)",
                "manufacturing_facility": cutting_facility_name,
                "cutting_location": f"{cutting_city}, India",
                "laboratory_certification": f"{lab_cert_type} #{lab_cert_number}"
            },
            "g7_customs_compliance": {
                "is_cleared_for_us_import": is_g7_compliant,
                "us_customs_hsn_code": "7104.91.0000" if is_lab_grown else "7102.39.0010",
                "audit_status": "VERIFIED" if is_g7_compliant else "REJECTED",
                "compliance_flags": compliance_flags
            },
            "generated_timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return dossier

if __name__ == "__main__":
    tracker = DiamondProvenanceTracker()
    lgd_dossier = tracker.create_provenance_dossier(
        stock_number="SURAT-LGD-4091",
        carat_weight=2.15,
        shape_cut="Round Brilliant Ideal",
        color="E",
        clarity="VVS2",
        rough_origin_country="India",
        rough_kpc_number="",
        cutting_facility_name="Surat Diamond Bourse Advanced Cutting Hub",
        cutting_city="Surat",
        lab_cert_type="IGI",
        lab_cert_number="LG612948102",
        is_lab_grown=True
    )
    print("=== Diamond Provenance Dossier Sample ===")
    print(json.dumps(lgd_dossier, indent=2))
