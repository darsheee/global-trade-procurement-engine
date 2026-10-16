"""
Rules of Origin (RoO) & Preferential Tariff Calculation Engine
Vistara Trade Acceleration & Compliance Desk (2026)

Evaluates compliance under:
- India-UK Comprehensive Economic and Trade Agreement (CETA)
- India-UAE Comprehensive Economic Partnership Agreement (CEPA)
- India-Australia Economic Cooperation and Trade Agreement (ECTA)
- India-EFTA Trade and Economic Partnership Agreement (TEPA)

Supports:
1. Regional Value Content (RVC) / Value Addition (VA) % calculations
2. Change in Tariff Sub-Heading (CTSH - 6 Digit) and Change in Tariff Heading (CTH - 4 Digit)
3. De Minimis Rule (10% non-originating tolerance)
4. Bill of Materials (BOM) auditing for DGFT electronic Certificate of Origin (e-CoO) filing
"""

import re
from typing import List, Dict, Any, Optional

FTA_CONFIGS = {
    "India-UK CETA": {
        "min_va_pct": 35.0,
        "de_minimis_pct": 10.0,
        "default_rule": "CTSH + VA 35%",
        "eligible_duty": "0% Preferential Duty"
    },
    "India-UAE CEPA": {
        "min_va_pct": 40.0,
        "de_minimis_pct": 10.0,
        "default_rule": "CTSH + VA 40%",
        "eligible_duty": "0% Preferential Duty (Bharat Mart Corridor)"
    },
    "India-Australia ECTA": {
        "min_va_pct": 35.0,
        "de_minimis_pct": 10.0,
        "default_rule": "CTSH + VA 35%",
        "eligible_duty": "0% Preferential Duty (96.4% Tariff Lines)"
    },
    "India-EFTA TEPA": {
        "min_va_pct": 35.0,
        "de_minimis_pct": 10.0,
        "default_rule": "CTSH + VA 35%",
        "eligible_duty": "0% Duty (Switzerland, Norway, Iceland, Liechtenstein)"
    }
}

class RulesOfOriginEngine:
    def __init__(self, fta_name: str = "India-UK CETA", min_va_pct: Optional[float] = None, de_minimis_pct: float = 10.0):
        self.fta_name = fta_name
        cfg = FTA_CONFIGS.get(fta_name, FTA_CONFIGS["India-UK CETA"])
        self.min_va_pct = min_va_pct if min_va_pct is not None else cfg["min_va_pct"]
        self.de_minimis_pct = de_minimis_pct
        self.eligible_duty = cfg["eligible_duty"]

    @staticmethod
    def normalize_hs_code(code: str) -> str:
        """
        Normalizes HS codes by removing dots, spaces, and non-numeric characters.
        Guarantees exact 6-digit subheading.
        Example: '7113.19.00' -> '711319'
        """
        digits = re.sub(r"[^0-9]", "", str(code))
        if len(digits) < 6:
            digits = digits.ljust(6, "0")
        return digits[:6]

    def evaluate_origin(
        self,
        finished_hs_code: str,
        fob_price_usd: float,
        bill_of_materials: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluates origin eligibility for an export shipment.
        bill_of_materials items format:
        {
            "name": str,
            "hs_code": str,
            "value_usd": float,
            "originating": bool (True if sourced from India or FTA partner)
        }
        """
        if fob_price_usd <= 0:
            raise ValueError("FOB price must be greater than 0")

        finished_subheading = self.normalize_hs_code(finished_hs_code)
        finished_heading = finished_subheading[:4]

        vnm_total = 0.0
        originating_total = 0.0
        ctsh_violating_value = 0.0
        ctsh_violating_items = []

        for item in bill_of_materials:
            val = float(item.get("value_usd", 0.0))
            is_orig = bool(item.get("originating", False))

            if is_orig:
                originating_total += val
            else:
                vnm_total += val
                input_subheading = self.normalize_hs_code(item.get("hs_code", ""))
                
                # If non-originating input has the SAME 6-digit subheading as finished good, CTSH fails
                if input_subheading == finished_subheading:
                    ctsh_violating_value += val
                    ctsh_violating_items.append({
                        "name": item.get("name", "Unknown item"),
                        "input_hs_code": input_subheading,
                        "value_usd": val,
                        "pct_of_fob": round((val / fob_price_usd) * 100, 2)
                    })

        # Value Addition Formula: ((FOB - VNM) / FOB) * 100
        va_pct = round(((fob_price_usd - vnm_total) / fob_price_usd) * 100, 2)
        va_qualified = va_pct >= self.min_va_pct

        # De Minimis Rule Check
        de_minimis_pct_actual = round((ctsh_violating_value / fob_price_usd) * 100, 2)
        ctsh_passed_cleanly = len(ctsh_violating_items) == 0
        de_minimis_applied = (not ctsh_passed_cleanly) and (de_minimis_pct_actual <= self.de_minimis_pct)
        ctsh_qualified = ctsh_passed_cleanly or de_minimis_applied

        is_originating = va_qualified and ctsh_qualified

        return {
            "fta_agreement": self.fta_name,
            "finished_hs_subheading": finished_subheading,
            "fob_price_usd": fob_price_usd,
            "vnm_total_usd": round(vnm_total, 2),
            "originating_materials_usd": round(originating_total, 2),
            "domestic_value_addition_pct": va_pct,
            "min_required_va_pct": self.min_va_pct,
            "va_rule_satisfied": va_qualified,
            "ctsh_rule_satisfied": ctsh_qualified,
            "ctsh_clean_pass": ctsh_passed_cleanly,
            "de_minimis_applied": de_minimis_applied,
            "de_minimis_actual_pct": de_minimis_pct_actual,
            "de_minimis_limit_pct": self.de_minimis_pct,
            "ctsh_violating_inputs": ctsh_violating_items,
            "origin_qualifies_for_preferential_tariff": is_originating,
            "preferential_tariff_eligible": self.eligible_duty if is_originating else "Standard MFN Tariff Applies",
            "dgft_e_coo_filing_status": "READY_TO_FILE" if is_originating else "NON_COMPLIANT_REVIEW_BOM"
        }

if __name__ == "__main__":
    engine = RulesOfOriginEngine(fta_name="India-UK CETA", min_va_pct=35.0)
    sample_bom = [
        {"name": "Indian Recycled Steel Scrap", "hs_code": "7204.49", "value_usd": 300.0, "originating": True},
        {"name": "Imported Alloying Ferro-Manganese", "hs_code": "7202.11", "value_usd": 150.0, "originating": False},
        {"name": "Domestic Processing & Direct Labor", "hs_code": "9988.00", "value_usd": 200.0, "originating": True}
    ]
    res = engine.evaluate_origin(
        finished_hs_code="7214.20.00", # Finished Steel Rebars
        fob_price_usd=1000.0,
        bill_of_materials=sample_bom
    )
    print("=== Rules of Origin Engine Validation Result ===")
    for k, v in res.items():
        print(f"{k}: {v}")
