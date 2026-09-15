"""
Bilateral Trade Matchmaker & Arbitrage Engine
Integrates 2,382 Indian Exporters, 190 US Corporate Buyers, and 4,123 Products.
"""

import sqlite3
from typing import List, Dict, Any, Optional
from pathlib import Path

DB_PATH = Path(__file__).parent / "db" / "india_usa_trade.db"

class TradeMatchmaker:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = Path(db_path) if db_path else DB_PATH
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found at {self.db_path}")

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def find_suppliers_by_keyword(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search Indian manufacturers by product keyword or company description."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            pattern = f"%{query}%"
            cursor.execute("""
                SELECT DISTINCT
                    e.supplier_id,
                    e.company_name,
                    e.city,
                    e.state_name,
                    e.iec_code,
                    e.deal_in,
                    p.product_name,
                    p.sku,
                    p.price_value,
                    p.currency
                FROM exporters e
                JOIN products p ON e.supplier_id = p.supplier_id
                WHERE p.product_name LIKE ? OR e.deal_in LIKE ? OR e.company_description LIKE ?
                ORDER BY e.company_name ASC
                LIMIT ?
            """, (pattern, pattern, pattern, limit))
            return [dict(row) for row in cursor.fetchall()]

    def get_us_importers_by_category(self, category: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieve verified US importers by industry category with direct contact info."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            pattern = f"%{category}%"
            cursor.execute("""
                SELECT 
                    buyer_id,
                    company_name,
                    industry_category,
                    city,
                    state_name,
                    website,
                    scraped_emails,
                    scraped_phones,
                    target_hub_match
                FROM us_importers_crawled
                WHERE industry_category LIKE ? OR company_name LIKE ?
                ORDER BY company_name ASC
                LIMIT ?
            """, (pattern, pattern, limit))
            return [dict(row) for row in cursor.fetchall()]

    def calculate_landed_cost_and_margin(
        self,
        fob_cost_usd: float,
        shipping_mode: str = "air",
        weight_kg: float = 1.0,
        customs_duty_pct: float = 5.5,
        target_retail_usd: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculate complete landed cost, insurance, tariff, and arbitrage margin.
        Air freight benchmark: $8.50/kg for precious/high-value; Sea: $0.45/kg (FCL equivalent)
        """
        freight_rate_per_kg = 8.50 if shipping_mode.lower() == "air" else 0.45
        freight_cost = max(weight_kg * freight_rate_per_kg, 25.0 if shipping_mode.lower() == "air" else 150.0)
        
        # Marine/Transit Insurance (approx 0.35% of CIF)
        insurance_cost = round(fob_cost_usd * 0.0035, 2)
        
        # CIF Value
        cif_value = round(fob_cost_usd + freight_cost + insurance_cost, 2)
        
        # Customs Tariff (Duty)
        customs_duty = round(cif_value * (customs_duty_pct / 100.0), 2)
        
        # Merchandise Processing Fee (MPF) for US (0.3464%, min $31.67, max $614.35)
        mpf = min(max(cif_value * 0.003464, 31.67), 614.35)
        
        total_landed_cost = round(cif_value + customs_duty + mpf, 2)
        
        gross_margin_usd = round(target_retail_usd - total_landed_cost, 2) if target_retail_usd > total_landed_cost else 0.0
        gross_margin_pct = round((gross_margin_usd / target_retail_usd) * 100.0, 1) if target_retail_usd > 0 else 0.0
        
        return {
            "fob_cost_usd": fob_cost_usd,
            "freight_cost": freight_cost,
            "insurance_cost": insurance_cost,
            "cif_value": cif_value,
            "customs_duty_pct": customs_duty_pct,
            "customs_duty_usd": customs_duty,
            "merchandise_processing_fee": round(mpf, 2),
            "total_landed_cost_usd": total_landed_cost,
            "target_retail_usd": target_retail_usd,
            "gross_margin_usd": gross_margin_usd,
            "gross_margin_pct": gross_margin_pct
        }

if __name__ == "__main__":
    mm = TradeMatchmaker()
    suppliers = mm.find_suppliers_by_keyword("Diamond", limit=3)
    print("=== Sample Suppliers ===")
    for s in suppliers:
        print(f" - {s.get('company_name')} ({s.get('city')}, {s.get('state_name')}): {s.get('product_name')}")
        
    buyers = mm.get_us_importers_by_category("Jewelry", limit=3)
    print("\n=== Sample US Importers ===")
    for b in buyers:
        print(f" - {b.get('company_name')} ({b.get('city')}, {b.get('state_name')}) | Email: {b.get('scraped_emails')}")
        
    cost = mm.calculate_landed_cost_and_margin(fob_cost_usd=250.0, weight_kg=0.2, target_retail_usd=750.0)
    print(f"\n=== Arbitrage Margin ===")
    print(f"Landed Cost: ${cost['total_landed_cost_usd']} | Target Retail: ${cost['target_retail_usd']} | Margin: {cost['gross_margin_pct']}%")
