"""
Autonomous B2B Buyer Outreach Agent
Generates hyper-personalized cold outreach emails and LinkedIn messaging sequences for verified US corporate buyers.
Leverages crawled corporate data, decision-maker titles, and product catalog synergy.
Integrated with CaratGrid LGD B2B Wholesale Pipeline for verified Delhi ateliers.
"""

import sqlite3
import sys
import argparse
import json
import re
from typing import Dict, Any, List, Optional
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from trade_engine.lgd_b2b_pipeline import LGDB2BPipeline

DB_PATH = REPO_ROOT / "trade_engine" / "db" / "india_usa_trade.db"


def extract_valid_emails(raw_text: str) -> List[str]:
    """
    Extracts valid email addresses from raw text/crawled strings.
    Filters out CSS/JS build artifacts, font weights (wght@100..900), or package tags (aos@2.3.1).
    """
    if not raw_text:
        return []
    candidates = [e.strip() for e in re.split(r"[\s,;]+", str(raw_text)) if e.strip()]
    valid = []
    # Strict email pattern requiring valid alpha TLD of at least 2 characters
    pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$")
    for c in candidates:
        if pattern.match(c) and ".." not in c:
            valid.append(c)
    return valid


class BuyerOutreachAgent:
    def __init__(self, db_path: str = None):
        self.db_path = str(db_path or DB_PATH)
        self.pipeline = LGDB2BPipeline(db_path=self.db_path)

    def generate_personalized_pitch(
        self,
        buyer_data: Dict[str, Any],
        target_product: str,
        cost_advantage_pct: int = 35
    ) -> Dict[str, str]:
        """Crafts a high-impact, B2B wholesale outreach email."""
        company = buyer_data.get("company_name", "Target Partner")
        city = buyer_data.get("city", "USA")
        state = buyer_data.get("state_name", "")
        valid_emails = extract_valid_emails(buyer_data.get("scraped_emails", ""))
        email = valid_emails[0] if valid_emails else ""
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

    def generate_lgd_wholesale_memo_pitch(
        self,
        buyer_data: Dict[str, Any],
        platform_margin_pct: float = 18.0
    ) -> Dict[str, Any]:
        """
        Generates a customized B2B wholesale memo pitch targeting independent US retail jewelers.
        Embeds real unit economics, verified Delhi manufacturing provenance, and 30-day memo terms.
        """
        company = buyer_data.get("company_name", "Valued Retail Partner")
        city = buyer_data.get("city", "USA")
        state = buyer_data.get("state_name", "")
        valid_emails = extract_valid_emails(buyer_data.get("scraped_emails", ""))
        email = valid_emails[0] if valid_emails else ""
        website = buyer_data.get("website", "")
        location_str = f"{city}, {state}".strip(", ") if state else city

        quote = self.pipeline.generate_wholesale_quote(
            buyer_name=company,
            buyer_city=location_str,
            platform_margin_pct=platform_margin_pct
        )

        subject = f"B2B Memo Showcase: Direct Delhi Finished LGD Collection for {company} (65%+ Gross Margin)"

        body = f"""Hi Team at {company},

I hope you are having a productive week.

I reviewed {company}'s fine jewelry showcase in {location_str} {f'({website})' if website else ''} and noticed your strong customer trust in bridal and luxury diamond jewelry.

Through CaratGrid, we connect premier North American independent jewelers directly with India's top certified lab-grown diamond manufacturing ateliers in Delhi and Surat—specifically The New Age Diamonds, Altin Global LLP, Sequoia Overseas, and D K Jewellers.

By bypassing multi-tier domestic US diamond wholesalers, your storefront can capture 65% to 75% gross margins with zero dead inventory risk:

Curated 4-Piece Showcase Memo Starter Kit:
- 2.00ct Round Brilliant Solitaire (LGD-RING-200-RND): Landed ${quote['items'][0]['us_landed_cost_usd']:.2f} | Suggested Retail ${quote['items'][0]['us_retail_price_usd']:.2f} (Profit: ${quote['items'][0]['jeweler_profit_usd']:.2f}/pc · {quote['items'][0]['jeweler_gross_margin_pct']:.1f}%)
- 1.50ct Oval Hidden-Halo Solitaire (LGD-RING-150-OVL): Landed ${quote['items'][1]['us_landed_cost_usd']:.2f} | Suggested Retail ${quote['items'][1]['us_retail_price_usd']:.2f} (Profit: ${quote['items'][1]['jeweler_profit_usd']:.2f}/pc · {quote['items'][1]['jeweler_gross_margin_pct']:.1f}%)
- 3.00 ctw Emerald Cut Tennis Bracelet (LGD-BRAC-300-EMR): Landed ${quote['items'][2]['us_landed_cost_usd']:.2f} | Suggested Retail ${quote['items'][2]['us_retail_price_usd']:.2f} (Profit: ${quote['items'][2]['jeweler_profit_usd']:.2f}/pc · {quote['items'][2]['jeweler_gross_margin_pct']:.1f}%)
- 1.00 ctw Stud Earrings (LGD-STUD-100-RND): Landed ${quote['items'][3]['us_landed_cost_usd']:.2f} | Suggested Retail ${quote['items'][3]['us_retail_price_usd']:.2f} (Profit: ${quote['items'][3]['jeweler_profit_usd']:.2f}/pc · {quote['items'][3]['jeweler_gross_margin_pct']:.1f}%)

Key Commercial Terms:
• Total Working Capital Outlay: ${quote['total_sample_cost']:.2f} (Retail Value: ${quote['total_retail_value']:.2f} | Net Profit: ${quote['retailer_profit']:.2f})
• Risk-Free 30-Day Memo Consignment: Display in your showcases before settling invoice.
• Backed by Euler Hermes Trade Credit: Invoicing managed via our Delaware LLC corporate desk.
• Logistics & Compliance: Door-to-door insured air dispatch via Malca-Amit / Brink's Global (US Customs HTS 7104.91.00 / 7113.19 cleared).
• Certification: IGI / GIA laser-inscribed certificates and BIS-hallmarked 14K/18K gold.

Would you be open to receiving our complete line sheet and approving a 30-day memo trial for your counter this month?

Best regards,

Procurement & Wholesale Desk
CaratGrid / Global Trade Intelligence Engine
Email: wholesale@caratgrid.internal
"""
        return {
            "company": company,
            "city": city,
            "state": state,
            "to_email": email,
            "website": website,
            "subject": subject,
            "body": body,
            "quote": quote
        }

    def generate_batch_for_category(
        self,
        industry_category: str = "Gems and Jewellery Products",
        count: int = 3
    ) -> List[Dict[str, str]]:
        if not Path(self.db_path).exists():
            return []
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT company_name, city, state_name, website, scraped_emails 
            FROM us_importers_crawled 
            WHERE industry_category = ?
        """, (industry_category,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()

        # Prioritize buyers with verified valid emails
        rows.sort(key=lambda b: (
            0 if len(extract_valid_emails(b.get("scraped_emails", ""))) > 0 else 1,
            b.get("company_name", "")
        ))

        pitches = []
        for r in rows[:count]:
            pitch = self.generate_personalized_pitch(r, target_product="10K/14K Fine Finished Jewelry & Lab-Grown Diamonds")
            pitches.append(pitch)
        return pitches

    def generate_batch_lgd_pitches(
        self,
        count: int = 5,
        platform_margin_pct: float = 18.0
    ) -> List[Dict[str, Any]]:
        """Queries crawled US jewelry importers from local database and crafts tailored LGD memo pitches."""
        if not Path(self.db_path).exists():
            return []
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT company_name, city, state_name, website, scraped_emails
            FROM us_importers_crawled
            WHERE industry_category = 'Gems and Jewellery Products'
        """)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()

        # Prioritize verified corporate jewelers with valid scraped emails, then website presence, then name
        def buyer_sort_key(b):
            emails = extract_valid_emails(b.get("scraped_emails", ""))
            has_valid_email = 0 if len(emails) > 0 else 1
            has_website = 0 if b.get("website") else 1
            return (has_valid_email, has_website, b.get("company_name", ""))

        rows.sort(key=buyer_sort_key)
        selected_rows = rows[:count]

        pitches = []
        for r in selected_rows:
            pitch = self.generate_lgd_wholesale_memo_pitch(r, platform_margin_pct=platform_margin_pct)
            pitches.append(pitch)
        return pitches


def main():
    parser = argparse.ArgumentParser(description="Autonomous B2B Buyer Outreach Agent CLI")
    parser.add_argument("--lgd", action="store_true", help="Generate LGD wholesale memo pitches")
    parser.add_argument("--count", type=int, default=3, help="Number of pitches to generate")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    agent = BuyerOutreachAgent()
    if args.lgd:
        pitches = agent.generate_batch_lgd_pitches(count=args.count)
        if args.json:
            print(json.dumps(pitches, indent=2))
        else:
            print(f"=== Generated {len(pitches)} LGD Wholesale Memo Pitches ===")
            for p in pitches:
                print(f"Target: {p['company']} ({p['city']}, {p['state']})")
                print(f"Subject: {p['subject']}")
                print(f"Preview:\n{p['body'][:300]}...\n---")
    else:
        pitches = agent.generate_batch_for_category(count=args.count)
        print(f"=== Generated {len(pitches)} Generic Buyer Pitches ===")
        for p in pitches:
            print(f"To: {p['to_email']} ({p['company']})")
            print(f"Subject: {p['subject']}")
            print(f"Body Preview:\n{p['body'][:250]}...\n---")


if __name__ == "__main__":
    main()
