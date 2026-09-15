"""
Autonomous B2B Buyer Outreach Agent
Generates hyper-personalized cold outreach emails and LinkedIn messaging sequences for verified US corporate buyers.
Leverages crawled corporate data, decision-maker titles, and product catalog synergy.
"""

import sqlite3
from typing import Dict, Any, List
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "trade_engine" / "db" / "india_usa_trade.db"

class BuyerOutreachAgent:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(DB_PATH)

    def generate_personalized_pitch(self, buyer_data: Dict[str, Any], target_product: str, cost_advantage_pct: int = 35) -> Dict[str, str]:
        """Crafts a high-impact, B2B wholesale outreach email."""
        company = buyer_data.get("company_name", "Target Partner")
        city = buyer_data.get("city", "USA")
        state = buyer_data.get("state_name", "")
        email = buyer_data.get("scraped_emails", "")
        website = buyer_data.get("website", "")
        
        subject = f"Direct OEM Supply Partnership: High-Volume {target_product} (FOB India / US Landed)"
        
        body = f"""Hi Team at {company},

I hope this finds you well.

I came across {company}'s operations in {city}, {state} ({website}) and noticed your prominent distribution in the retail and wholesale space.

We represent certified, high-volume OEM manufacturers based in India specializing in precision export-grade {target_product}. Given recent shifts in global supply chains, our direct factory-to-warehouse pipeline typically unlocks a {cost_advantage_pct}% to 45% margin advantage compared to domestic US distributors, while strictly maintaining ASTM/ISO quality compliance and full G7/Kimberley Process ethical certification.

Key Operational Highlights:
- Direct Manufacturer Pricing (Eliminating middleman tiers)
- Flexible Terms: Net-30 / Net-60 credit facility available via our Delaware LLC corporate desk
- Fully Insured Door-to-Door Air & Sea Logistics to your US fulfillment centers
- Pre-shipment third-party batch inspection (SGS / Bureau Veritas)

Would you or your procurement director be open to reviewing our current line catalog and landed-cost sheet this week?

Best regards,

Trade Facilitation & Wholesale Desks
Global Trade & Procurement Intelligence Engine
Email: trade-desk@globalprocure.internal
"""
        return {
            "to_email": email,
            "company": company,
            "subject": subject,
            "body": body
        }

    def generate_batch_for_category(self, industry_category: str = "Gems and Jewellery Products", count: int = 3) -> List[Dict[str, str]]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT company_name, city, state_name, website, scraped_emails 
            FROM us_importers_crawled 
            WHERE industry_category = ? AND scraped_emails != ''
            LIMIT ?
        """, (industry_category, count))
        rows = cursor.fetchall()
        conn.close()

        pitches = []
        for r in rows:
            pitch = self.generate_personalized_pitch(dict(r), target_product="10K/14K Fine Finished Jewelry & Lab-Grown Diamonds")
            pitches.append(pitch)
        return pitches

if __name__ == "__main__":
    agent = BuyerOutreachAgent()
    pitches = agent.generate_batch_for_category(count=2)
    print(f"=== Generated {len(pitches)} Buyer Pitches ===")
    for p in pitches:
        print(f"To: {p['to_email']} ({p['company']})")
        print(f"Subject: {p['subject']}")
        print(f"Body Preview:\n{p['body'][:250]}...\n---")
