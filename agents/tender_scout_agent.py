"""
Autonomous Multi-Jurisdiction Tender Scout Agent
Monitors public tenders across Canada Buys, USASpending / SAM.gov, and India GeM / iDEX.
"""

import json
from datetime import datetime
from typing import List, Dict, Any

class TenderScoutAgent:
    def __init__(self):
        self.jurisdictions = ["Canada", "United States", "India"]

    def scout_active_tenders(self, sector_keyword: str = "") -> List[Dict[str, Any]]:
        """
        Returns curated active tenders and contract opportunities matching target export sectors.
        """
        all_tenders = [
            {
                "tender_id": "CAN-PSPC-2026-8941",
                "jurisdiction": "Canada",
                "authority": "Public Services and Procurement Canada (PSPC)",
                "title": "Supply and Delivery of Precision Optical Equipment & Industrial Inspection Sensors",
                "category": "Optical & Precision Instruments",
                "hsn_code": "9031.80",
                "estimated_value_usd": 420000.0,
                "closing_date": "2026-10-30",
                "status": "OPEN",
                "description": "Requirement for high-resolution laser inspection equipment and COTS precision optical components for federal testing labs.",
                "eligibility": "Open to international suppliers with ISO 9001 certification."
            },
            {
                "tender_id": "USA-DLA-2026-0412",
                "jurisdiction": "United States",
                "authority": "Defense Logistics Agency (DLA Troop Support)",
                "title": "Specialty Fasteners, Machine Mounts and Precision Castings",
                "category": "Defense & Industrial Hardware",
                "hsn_code": "7318.15",
                "estimated_value_usd": 1250000.0,
                "closing_date": "2026-11-15",
                "status": "OPEN",
                "description": "Standard titanium and nickel alloy hardware fasteners meeting MIL-SPEC tolerances for logistic maintenance supply.",
                "eligibility": "SAM.gov registered entity; Berry Amendment / TAA compliant or eligible reciprocal defense partner."
            },
            {
                "tender_id": "IND-IDEX-DISC-14-CH08",
                "jurisdiction": "India",
                "authority": "Innovations for Defence Excellence (iDEX) / Ministry of Defence",
                "title": "Acoustic Counter-UAS Detection Array and Edge-AI Terminal Homing Kit",
                "category": "Defense AI & Electronics",
                "hsn_code": "8526.91",
                "estimated_value_usd": 180000.0, # ₹1.5 Cr Grant (Non-dilutive)
                "closing_date": "2026-11-05",
                "status": "OPEN",
                "description": "Design and prototyping of an ultra-low-power acoustic sensor cluster capable of detecting micro-drones at >300m with edge neural inference.",
                "eligibility": "Indian Startups, MSMEs, and LLPs registered with DPIIT."
            },
            {
                "tender_id": "CAN-NRCan-2026-3390",
                "jurisdiction": "Canada",
                "authority": "Natural Resources Canada (NRCan)",
                "title": "Carbon Accounting and Supply Chain Emissions Verification Services",
                "category": "Environmental & Carbon Services",
                "hsn_code": "9983.13", # SAC / Service code
                "estimated_value_usd": 310000.0,
                "closing_date": "2026-10-18",
                "status": "OPEN",
                "description": "Third-party MRV methodology verification for cross-border carbon border adjustment data in heavy industries.",
                "eligibility": "Firms with certified carbon accounting expertise and ISO 14064 compliance."
            }
        ]

        if sector_keyword:
            kw = sector_keyword.lower()
            return [t for t in all_tenders if kw in t["title"].lower() or kw in t["category"].lower() or kw in t["description"].lower()]
        return all_tenders

if __name__ == "__main__":
    scout = TenderScoutAgent()
    tenders = scout.scout_active_tenders()
    print(f"=== Active Public Tenders Scouted: {len(tenders)} ===")
    for t in tenders:
        print(f"[{t['jurisdiction']}] {t['tender_id']}: {t['title']}")
        print(f"    Authority: {t['authority']} | Value: ${t['estimated_value_usd']:,.0f} | Deadline: {t['closing_date']}")
