import unittest
import sys
from pathlib import Path

# Ensure root repository directory is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from trade_engine.lgd_b2b_pipeline import (
    LGDB2BPipeline,
    DELHI_LGD_SUPPLIERS,
    CORE_SKU_CATALOG,
)


class TestLGDB2BPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = LGDB2BPipeline()

    def test_delhi_suppliers_roster(self):
        """Verifies verified Delhi atelier partners are correctly registered with compliance codes."""
        suppliers = self.pipeline.get_suppliers()
        self.assertGreaterEqual(len(suppliers), 4)

        supplier_names = [s["company_name"] for s in suppliers]
        self.assertIn("The New Age Diamonds Private Limited", supplier_names)
        self.assertIn("Altin Global LLP", supplier_names)
        self.assertIn("Sequoia Overseas Co", supplier_names)
        self.assertIn("D K Jewellers", supplier_names)

        # Check required fields and IEC codes
        for s in suppliers:
            self.assertTrue(s.get("iec_code"), f"Missing IEC code in {s['company_name']}")
            self.assertTrue(s.get("hub"), f"Missing hub in {s['company_name']}")
            self.assertIn("Delhi", s["hub"])
            self.assertGreater(s.get("production_sla_days", 0), 0)

    def test_catalog_skus_integrity(self):
        """Verifies core 4-piece high-velocity retail starter SKUs."""
        catalog = self.pipeline.get_catalog()
        self.assertEqual(len(catalog), 4)

        sku_codes = [s["sku_code"] for s in catalog]
        self.assertIn("LGD-RING-200-RND", sku_codes)
        self.assertIn("LGD-RING-150-OVL", sku_codes)
        self.assertIn("LGD-BRAC-300-EMR", sku_codes)
        self.assertIn("LGD-STUD-100-RND", sku_codes)

        for sku in catalog:
            self.assertGreater(sku["diamond_carat"], 0)
            self.assertGreater(sku["loose_stone_cost_usd"], 0)
            self.assertGreater(sku["mount_casting_labor_usd"], 0)
            self.assertGreater(sku["igi_certification_usd"], 0)
            self.assertGreater(sku["us_benchmark_retail_usd"], 0)

    def test_sku_arbitrage_math(self):
        """Verifies factory FOB, platform markup, CIF landed cost, and gross margins across all 4 catalog SKUs."""
        # 1. 2.00ct Round Brilliant Solitaire
        res0 = self.pipeline.calculate_sku_arbitrage(CORE_SKU_CATALOG[0], platform_margin_pct=18.0)
        self.assertEqual(res0["factory_fob_usd"], 515.0)
        self.assertEqual(res0["wholesale_price_usd"], 607.70)
        self.assertEqual(res0["customs_duty_usd"], 33.42)
        self.assertEqual(res0["us_landed_cost_usd"], 676.12)
        self.assertEqual(res0["jeweler_profit_usd"], 1573.88)
        self.assertEqual(res0["jeweler_gross_margin_pct"], 70.0)

        # 2. 1.50ct Oval Halo Solitaire
        res1 = self.pipeline.calculate_sku_arbitrage(CORE_SKU_CATALOG[1], platform_margin_pct=18.0)
        self.assertEqual(res1["factory_fob_usd"], 480.0)
        self.assertEqual(res1["wholesale_price_usd"], 566.40)
        self.assertEqual(res1["customs_duty_usd"], 31.15)
        self.assertEqual(res1["us_landed_cost_usd"], 632.55)
        self.assertEqual(res1["jeweler_profit_usd"], 1317.45)
        self.assertEqual(res1["jeweler_gross_margin_pct"], 67.6)

        # 3. 3.00 ctw Tennis Bracelet - Verifies 19 CFR round-half-up half-cent boundary ($1239 * 0.055 = 68.145 -> $68.15)
        res2 = self.pipeline.calculate_sku_arbitrage(CORE_SKU_CATALOG[2], platform_margin_pct=18.0)
        self.assertEqual(res2["factory_fob_usd"], 1050.0)
        self.assertEqual(res2["wholesale_price_usd"], 1239.0)
        self.assertEqual(res2["customs_duty_usd"], 68.15)
        self.assertEqual(res2["us_landed_cost_usd"], 1342.15)
        self.assertEqual(res2["jeweler_profit_usd"], 1607.85)
        self.assertEqual(res2["jeweler_gross_margin_pct"], 54.5)

        # 4. 1.00 ctw Stud Earrings
        res3 = self.pipeline.calculate_sku_arbitrage(CORE_SKU_CATALOG[3], platform_margin_pct=18.0)
        self.assertEqual(res3["factory_fob_usd"], 280.0)
        self.assertEqual(res3["wholesale_price_usd"], 330.40)
        self.assertEqual(res3["customs_duty_usd"], 18.17)
        self.assertEqual(res3["us_landed_cost_usd"], 383.57)
        self.assertEqual(res3["jeweler_profit_usd"], 511.43)
        self.assertEqual(res3["jeweler_gross_margin_pct"], 57.1)

    def test_custom_bom_calculations(self):
        """Verifies dynamic Bill of Materials calculations across gold karats and stone types."""
        # Test 14K Gold Tennis Bracelet simulator defaults
        bom = self.pipeline.calculate_custom_bom(
            gold_karat=14,
            metal_weight_grams=12.0,
            diamond_carats=3.0,
            diamond_type="lgd",
            setting_stone_count=50,
            target_us_retail=1850.0
        )

        # 14K gold = 58.5% purity * $78/g = $45.63/g * 12g = 547.56
        self.assertEqual(bom["raw_gold_cost_usd"], 547.56)
        # India labor = 12 * $2.50 = 30.0
        self.assertEqual(bom["india_labor_cost_usd"], 30.0)
        # Diamond = 3.0 * $95 = 285.0
        self.assertEqual(bom["total_diamond_cost_usd"], 285.0)
        # Setting = 50 * $1.20 = 60.0
        self.assertEqual(bom["setting_labor_cost_usd"], 60.0)
        # Factory FOB = 547.56 + 30.0 + 285.0 + 60.0 = 922.56
        self.assertEqual(bom["factory_fob_cost_usd"], 922.56)

        # US domestic labor comparison should show significant savings
        self.assertGreater(bom["manufacturing_savings_usd"], 300.0)
        self.assertGreater(bom["gross_profit_usd"], 800.0)

    def test_generate_wholesale_quote(self):
        """Verifies end-to-end B2B quotation generation for a US retail jeweler."""
        quote = self.pipeline.generate_wholesale_quote("Apex Fine Jewelers", "Dallas, TX", platform_margin_pct=18.0)

        self.assertEqual(quote["buyer_name"], "Apex Fine Jewelers")
        self.assertEqual(quote["buyer_city"], "Dallas, TX")
        self.assertEqual(len(quote["items"]), 4)

        # Check total calculations consistency
        self.assertEqual(quote["total_wholesale_cost"], 2743.50)
        self.assertEqual(quote["total_sample_cost"], 3034.39)
        self.assertEqual(quote["total_retail_value"], 8045.00)
        self.assertEqual(quote["retailer_profit"], 5010.61)
        self.assertEqual(quote["overall_margin_pct"], 62.3)

        # Proposal text content checks
        proposal = quote["proposal_text"]
        self.assertIn("Apex Fine Jewelers", proposal)
        self.assertIn("Dallas, TX", proposal)
        self.assertIn("CaratGrid", proposal)
        self.assertIn("D K Jewellers", proposal)
        self.assertIn("Malca-Amit / Brink's Global", proposal)
        self.assertIn("HTS 7104.91.00", proposal)
        self.assertIn("Total Wholesale Platform Invoice: $2743.50", proposal)
        self.assertIn("Total Landed Working Capital Required: $3034.39", proposal)
        self.assertIn("Net Retailer Cash Profit: $5010.61", proposal)

    def test_edge_cases(self):
        """Tests zero retail, custom SKU list, and 0% platform margin."""
        # Zero retail price: no division by zero
        zero_retail_sku = {
            "sku_code": "TEST-ZERO",
            "title": "Zero Retail Test",
            "diamond_carat": 1.0,
            "loose_stone_cost_usd": 100.0,
            "mount_casting_labor_usd": 100.0,
            "igi_certification_usd": 10.0,
            "us_benchmark_retail_usd": 0.0
        }
        res = self.pipeline.calculate_sku_arbitrage(zero_retail_sku)
        self.assertEqual(res["jeweler_gross_margin_pct"], 0.0)

        # 0% platform margin
        zero_margin_res = self.pipeline.calculate_sku_arbitrage(zero_retail_sku, platform_margin_pct=0.0)
        self.assertEqual(zero_margin_res["platform_take_rate_usd"], 0.0)
        self.assertEqual(zero_margin_res["wholesale_price_usd"], 210.0)


class TestBuyerOutreachAgent(unittest.TestCase):
    def setUp(self):
        from agents.buyer_outreach_agent import BuyerOutreachAgent, extract_valid_emails
        self.agent = BuyerOutreachAgent()
        self.extract_valid_emails = extract_valid_emails

    def test_email_sanitization(self):
        """Verifies extract_valid_emails rejects CSS/JS scraper artifacts and accepts real emails."""
        self.assertEqual(self.extract_valid_emails("wght@100..900"), [])
        self.assertEqual(self.extract_valid_emails("aos@2.3.1"), [])
        self.assertEqual(self.extract_valid_emails(""), [])
        self.assertEqual(self.extract_valid_emails("info@greatdiam.com"), ["info@greatdiam.com"])
        
        multi = self.extract_valid_emails("info@realgemsinc.com, online@realgemsinc.com")
        self.assertEqual(multi, ["info@realgemsinc.com", "online@realgemsinc.com"])

    def test_generate_lgd_wholesale_memo_pitch(self):
        """Verifies outreach agent creates high-impact LGD memo proposal with real math and formatted currency."""
        sample_buyer = {
            "company_name": "Solomon Brothers Fine Jewelry",
            "city": "Atlanta",
            "state_name": "Georgia",
            "scraped_emails": "buyers@solomonbrothers.com",
            "website": "https://solomonbrothers.com"
        }
        pitch = self.agent.generate_lgd_wholesale_memo_pitch(sample_buyer, platform_margin_pct=18.0)
        self.assertEqual(pitch["company"], "Solomon Brothers Fine Jewelry")
        self.assertEqual(pitch["to_email"], "buyers@solomonbrothers.com")
        self.assertIn("Solomon Brothers Fine Jewelry", pitch["subject"])
        self.assertIn("65%+", pitch["subject"])

        # Body must mention key ateliers and terms with .2f currency formatting
        body = pitch["body"]
        self.assertIn("The New Age Diamonds", body)
        self.assertIn("D K Jewellers", body)
        self.assertIn("Euler Hermes", body)
        self.assertIn("30-Day Memo", body)
        self.assertIn("Malca-Amit / Brink's Global", body)
        self.assertIn("Landed $676.12", body)
        self.assertIn("Suggested Retail $2250.00", body)
        self.assertIn("Total Working Capital Outlay: $3034.39", body)

        # Check attached quote
        quote = pitch["quote"]
        self.assertEqual(len(quote["items"]), 4)
        self.assertGreater(quote["retailer_profit"], 4000.0)

    def test_batch_lgd_pitches_database_integration(self):
        """Verifies querying crawled US jewelers from database, prioritizing valid emails, and generating batch pitches."""
        pitches = self.agent.generate_batch_lgd_pitches(count=3)
        self.assertGreaterEqual(len(pitches), 1)
        # First pitch must have a verified valid email
        self.assertTrue(pitches[0]["to_email"])
        self.assertIn("@", pitches[0]["to_email"])
        for p in pitches:
            self.assertTrue(p["company"])
            self.assertTrue(p["subject"])
            self.assertIn("LGD", p["subject"])
            self.assertIn("CaratGrid", p["body"])
            self.assertIn("quote", p)
            # Ensure no CSS/JS scraper artifacts ever leak into to_email
            self.assertNotIn("wght@", p["to_email"])
            self.assertNotIn("aos@", p["to_email"])

if __name__ == "__main__":
    unittest.main()

