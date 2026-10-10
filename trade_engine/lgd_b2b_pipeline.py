"""
LGD B2B Wholesale Pipeline & Arbitrage Matchmaker
Connects verified Delhi/Surat Lab-Grown Diamond manufacturing ateliers with North American independent retail jewelers.
Calculates real-world bill-of-materials (BOM), FOB-to-CIF landed costs, and US retail margin spreads.
"""

import sqlite3
import json
import argparse
from typing import Dict, Any, List, Optional
from pathlib import Path

DB_PATH = Path(__file__).parent / "db" / "india_usa_trade.db"

# Verified Delhi LGD Manufacturing Ateliers from local trade database
DELHI_LGD_SUPPLIERS: List[Dict[str, Any]] = [
    {
        "company_name": "The New Age Diamonds Private Limited",
        "corporate_type": "Private Limited",
        "iec_code": "AAJCN2214K",
        "gstin": "07AAJCN2214K1ZH",
        "turnover_tier": "₹11-25 Cr",
        "hub": "Netaji Subhash Place, Pitampura, Delhi",
        "phone": "+91 98180 63683",
        "email": "info@thenewagediamonds.com",
        "specialization": "CVD/HPHT certified solitaires, engagement rings, 14K/18K custom mounts",
        "production_sla_days": 5
    },
    {
        "company_name": "Altin Global LLP",
        "corporate_type": "LLP",
        "iec_code": "ACLFA5590Q",
        "gstin": "07ACLFA5590Q1ZL",
        "turnover_tier": "₹41-99 Lakhs",
        "hub": "Sector 5 Rohini, Delhi",
        "phone": "+91 93118 52242",
        "email": "altingloballlp@gmail.com",
        "specialization": "14K/18K LGD solitaires, eternity bands, custom diamond luxury watches",
        "production_sla_days": 6
    },
    {
        "company_name": "Sequoia Overseas Co",
        "corporate_type": "Proprietorship",
        "iec_code": "CNQPP2527J",
        "gstin": "07CNQPP2527J1ZI",
        "turnover_tier": "₹1-10 Cr",
        "hub": "Keshav Puram, Tri Nagar, Delhi",
        "specialization": "IGI/GIA certified loose LGD and hallmarked fine jewelry",
        "production_sla_days": 7
    },
    {
        "company_name": "D K Jewellers",
        "corporate_type": "Proprietorship",
        "iec_code": "ACUPG3187C",
        "gstin": "07ACUPG3187C1Z5",
        "turnover_tier": "₹1-10 Cr",
        "hub": "Old Delhi / North Delhi",
        "phone": "+91 11 2325 0000",
        "email": "trade@dkjewellers.in",
        "specialization": "Bridal, couture, and fine everyday jewelry in solid gold, IGI-certified LGD/diamonds, BIS-hallmarked mounts",
        "production_sla_days": 5
    }
]

# Standard high-velocity retail engagement SKUs
CORE_SKU_CATALOG: List[Dict[str, Any]] = [
    {
        "sku_code": "LGD-RING-200-RND",
        "title": "2.00ct Round Brilliant 4-Prong Solitaire Ring",
        "diamond_carat": 2.0,
        "color_clarity": "F/VS1 Ideal Cut (IGI Certified)",
        "gold_karat": 14,
        "gold_grams": 3.5,
        "loose_stone_cost_usd": 250.0,  # $125/ct Surat wholesale
        "mount_casting_labor_usd": 240.0, # 14K gold + Indian bench labor
        "igi_certification_usd": 25.0,
        "us_benchmark_retail_usd": 2250.0
    },
    {
        "sku_code": "LGD-RING-150-OVL",
        "title": "1.50ct Oval Hidden-Halo Solitaire Ring",
        "diamond_carat": 1.5,
        "color_clarity": "E/VVS2 Ideal Cut (IGI Certified)",
        "gold_karat": 14,
        "gold_grams": 3.8,
        "loose_stone_cost_usd": 195.0,  # $130/ct
        "mount_casting_labor_usd": 260.0,
        "igi_certification_usd": 25.0,
        "us_benchmark_retail_usd": 1950.0
    },
    {
        "sku_code": "LGD-BRAC-300-EMR",
        "title": "3.00 ctw Emerald Cut Tennis Bracelet",
        "diamond_carat": 3.0,
        "color_clarity": "F/VS 50-Stone Matched Parcel",
        "gold_karat": 14,
        "gold_grams": 11.5,
        "loose_stone_cost_usd": 330.0,  # $110/ct
        "mount_casting_labor_usd": 680.0,
        "igi_certification_usd": 40.0,
        "us_benchmark_retail_usd": 2950.0
    },
    {
        "sku_code": "LGD-STUD-100-RND",
        "title": "1.00 ctw (0.50ct each) 4-Prong Stud Earrings",
        "diamond_carat": 1.0,
        "color_clarity": "E/VS1 Ideal Cut Matched Pair",
        "gold_karat": 14,
        "gold_grams": 1.8,
        "loose_stone_cost_usd": 120.0,  # $120/ct
        "mount_casting_labor_usd": 140.0,
        "igi_certification_usd": 20.0,
        "us_benchmark_retail_usd": 895.0
    }
]


class LGDB2BPipeline:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = Path(db_path) if db_path else DB_PATH
        self.suppliers = list(DELHI_LGD_SUPPLIERS)
        self.catalog = list(CORE_SKU_CATALOG)

    def get_suppliers(self) -> List[Dict[str, Any]]:
        """Returns verified Indian atelier partners."""
        return self.suppliers

    def get_catalog(self) -> List[Dict[str, Any]]:
        """Returns standard high-velocity B2B wholesale SKUs."""
        return self.catalog

    def calculate_sku_arbitrage(self, sku: Dict[str, Any], platform_margin_pct: float = 18.0) -> Dict[str, Any]:
        """Calculates factory FOB, platform markup, CIF landed cost, and US retail margin."""
        factory_fob = round(
            sku["loose_stone_cost_usd"] +
            sku["mount_casting_labor_usd"] +
            sku["igi_certification_usd"],
            2
        )
        
        platform_fee = round(factory_fob * (platform_margin_pct / 100.0), 2)
        wholesale_price_to_us_retailer = round(factory_fob + platform_fee, 2)
        
        # Secured armored air freight (Malca-Amit / Brink's allocated per piece)
        allocated_shipping_usd = 35.0
        # US Customs Duty (HTS 7104.91 / 7113.19: 5.5% on invoice)
        customs_duty_usd = round(wholesale_price_to_us_retailer * 0.055, 2)
        
        total_landed_cost_to_jeweler = round(
            wholesale_price_to_us_retailer + allocated_shipping_usd + customs_duty_usd, 2
        )
        
        retail_price = sku["us_benchmark_retail_usd"]
        jeweler_profit_usd = round(retail_price - total_landed_cost_to_jeweler, 2)
        jeweler_margin_pct = round((jeweler_profit_usd / retail_price) * 100.0, 1) if retail_price > 0 else 0.0
        
        return {
            "sku_code": sku["sku_code"],
            "title": sku["title"],
            "carats": sku["diamond_carat"],
            "factory_fob_usd": factory_fob,
            "platform_take_rate_usd": platform_fee,
            "wholesale_price_usd": wholesale_price_to_us_retailer,
            "allocated_shipping_usd": allocated_shipping_usd,
            "customs_duty_usd": customs_duty_usd,
            "us_landed_cost_usd": total_landed_cost_to_jeweler,
            "us_retail_price_usd": retail_price,
            "jeweler_profit_usd": jeweler_profit_usd,
            "jeweler_gross_margin_pct": jeweler_margin_pct
        }

    def calculate_custom_bom(
        self,
        gold_karat: int = 14,
        metal_weight_grams: float = 12.0,
        diamond_carats: float = 3.0,
        diamond_type: str = "lgd",
        setting_stone_count: int = 50,
        target_us_retail: float = 1850.0
    ) -> Dict[str, Any]:
        """
        Dynamically calculates unit economics & Bill of Materials matching the Next.js interactive simulator.
        Benchmarked against spot gold ($78/g pure 24K), Surat casting vs US workshop labor.
        """
        gold_purity_multiplier = 0.417 if gold_karat == 10 else (0.585 if gold_karat == 14 else 0.75)
        raw_gold_cost = round(metal_weight_grams * (78.0 * gold_purity_multiplier), 2)

        india_labor_cost = round(metal_weight_grams * 2.50, 2)
        us_labor_cost = round(metal_weight_grams * 18.00, 2)

        diamond_cost_per_ct = 95.0 if diamond_type.lower() == "lgd" else 1200.0
        total_diamond_cost = round(diamond_carats * diamond_cost_per_ct, 2)

        setting_labor_cost = round(setting_stone_count * 1.20, 2)
        factory_fob_cost = round(raw_gold_cost + india_labor_cost + total_diamond_cost + setting_labor_cost, 2)

        logistics_insured_cost = 45.0
        us_import_tariff = round(factory_fob_cost * 0.055, 2)
        total_landed_cost = round(factory_fob_cost + logistics_insured_cost + us_import_tariff, 2)

        gross_profit_usd = round(target_us_retail - total_landed_cost, 2)
        gross_margin_pct = round((gross_profit_usd / target_us_retail) * 100.0, 1) if target_us_retail > 0 else 0.0

        us_domestic_cost = round(raw_gold_cost + us_labor_cost + total_diamond_cost + (setting_stone_count * 5.50), 2)
        manufacturing_savings_usd = round(us_domestic_cost - factory_fob_cost, 2)

        return {
            "gold_karat": gold_karat,
            "metal_weight_grams": metal_weight_grams,
            "raw_gold_cost_usd": raw_gold_cost,
            "india_labor_cost_usd": india_labor_cost,
            "diamond_type": diamond_type,
            "diamond_carats": diamond_carats,
            "total_diamond_cost_usd": total_diamond_cost,
            "setting_labor_cost_usd": setting_labor_cost,
            "factory_fob_cost_usd": factory_fob_cost,
            "logistics_insured_cost_usd": logistics_insured_cost,
            "us_import_tariff_usd": us_import_tariff,
            "total_landed_cost_usd": total_landed_cost,
            "target_us_retail_usd": target_us_retail,
            "gross_profit_usd": gross_profit_usd,
            "gross_margin_pct": gross_margin_pct,
            "us_domestic_cost_usd": us_domestic_cost,
            "manufacturing_savings_usd": manufacturing_savings_usd
        }

    def generate_wholesale_quote(
        self,
        buyer_name: str,
        buyer_city: str,
        skus: Optional[List[Dict[str, Any]]] = None,
        platform_margin_pct: float = 18.0
    ) -> Dict[str, Any]:
        """Generates a complete commercial B2B quotation for an independent US jewelry store."""
        catalog_to_use = skus if skus is not None else self.catalog
        items = [self.calculate_sku_arbitrage(sku, platform_margin_pct=platform_margin_pct) for sku in catalog_to_use]
        
        total_wholesale_cost = round(sum(item["wholesale_price_usd"] for item in items), 2)
        total_sample_investment = round(sum(item["us_landed_cost_usd"] for item in items), 2)
        total_sample_retail_value = round(sum(item["us_retail_price_usd"] for item in items), 2)
        total_retailer_profit = round(total_sample_retail_value - total_sample_investment, 2)
        overall_margin_pct = round((total_retailer_profit / total_sample_retail_value) * 100.0, 1) if total_sample_retail_value > 0 else 0.0
        
        proposal_text = f"""================================================================================
B2B EXCLUSIVE WHOLESALE MEMO PROPOSAL: INDIAN LGD FINISHED JEWELRY
Prepared For: {buyer_name} ({buyer_city}, USA)
Facilitated By: CaratGrid / Global Trade Intelligence Engine
Atelier Partners: The New Age Diamonds, Altin Global LLP, Sequoia Overseas, D K Jewellers
================================================================================

Executive Summary:
Unlock 65%–75% gross margins on bridal engagement rings with zero capital lockup.
Direct factory dispatch from certified Delhi/Surat ateliers to your storefront within 5-7 business days.
Fully IGI-certified, hallmarked 14K/18K solid gold, and backed by 30-day memo terms.

Curated 4-Piece Showcase Starter Kit:
--------------------------------------------------------------------------------
"""
        for it in items:
            proposal_text += f"""• {it['title']} ({it['sku_code']}):
  - Factory FOB: ${it['factory_fob_usd']} | Wholesale Invoice: ${it['wholesale_price_usd']}
  - US Landed Cost (CIF Door): ${it['us_landed_cost_usd']}
  - Recommended Retail Price: ${it['us_retail_price_usd']}
  - Your Net Profit Per Piece: ${it['jeweler_profit_usd']} ({it['jeweler_gross_margin_pct']}% Gross Margin)
"""

        proposal_text += f"""--------------------------------------------------------------------------------
Starter Kit Financials:
• Total Wholesale Platform Invoice: ${total_wholesale_cost}
• Total Landed Working Capital Required: ${total_sample_investment}
• Total Retail Sales Value: ${total_sample_retail_value}
• Net Retailer Cash Profit: ${total_retailer_profit} ({overall_margin_pct}% Portfolio Margin)
• Logistics: 100% Insured Door-to-Door Air Courier via Malca-Amit / Brink's Global ($35/piece)
• Customs Classification: US HTS 7104.91.00 (Synthetic Diamonds) / 7113.19 (Gold Jewelry - 5.5% Duty)
• Payment Terms: Net-30 Memo backed by Euler Hermes / Delaware corporate desk
================================================================================
"""
        return {
            "buyer_name": buyer_name,
            "buyer_city": buyer_city,
            "platform_margin_pct": platform_margin_pct,
            "items": items,
            "total_wholesale_cost": total_wholesale_cost,
            "total_sample_cost": total_sample_investment,
            "total_retail_value": total_sample_retail_value,
            "retailer_profit": total_retailer_profit,
            "overall_margin_pct": overall_margin_pct,
            "suppliers": self.suppliers,
            "proposal_text": proposal_text
        }


def main():
    parser = argparse.ArgumentParser(description="CaratGrid LGD B2B Wholesale Pipeline CLI")
    parser.add_argument("--buyer", default="Apex Fine Jewelers", help="Buyer store name")
    parser.add_argument("--city", default="Dallas, TX", help="Buyer location")
    parser.add_argument("--margin", type=float, default=18.0, help="Platform margin percent")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    pipeline = LGDB2BPipeline()
    quote = pipeline.generate_wholesale_quote(args.buyer, args.city, platform_margin_pct=args.margin)
    if args.json:
        print(json.dumps(quote, indent=2))
    else:
        print(quote["proposal_text"])


if __name__ == "__main__":
    main()
