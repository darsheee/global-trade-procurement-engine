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
        """Verifies factory FOB, platform markup, CIF landed cost, and gross margins."""
        sku = CORE_SKU_CATALOG[0]  # 2.00ct Round Brilliant
        # loose: 250, mount: 240, igi: 25 -> FOB = 515.0
        expected_fob = 250.0 + 240.0 + 25.0
        
        result = self.pipeline.calculate_sku_arbitrage(sku, platform_margin_pct=18.0)
        self.assertEqual(result["factory_fob_usd"], expected_fob)

        expected_platform_fee = round(expected_fob * 0.18, 2)  # 515 * 0.18 = 92.70
        expected_wholesale = round(expected_fob + expected_platform_fee, 2)  # 607.70
        self.assertEqual(result["platform_take_rate_usd"], expected_platform_fee)
        self.assertEqual(result["wholesale_price_usd"], expected_wholesale)

        # Shipping: $35.0, Duty: 5.5% on wholesale (607.70 * 0.055 = 33.42)
        expected_customs = round(expected_wholesale * 0.055, 2)
        expected_landed = round(expected_wholesale + 35.0 + expected_customs, 2)  # 607.70 + 35 + 33.42 = 676.12
        self.assertEqual(result["us_landed_cost_usd"], expected_landed)

        # Retail: $2250 -> profit: 2250 - 676.12 = 1573.88
        expected_profit = round(2250.0 - expected_landed, 2)
        expected_margin = round((expected_profit / 2250.0) * 100.0, 1)
        self.assertEqual(result["jeweler_profit_usd"], expected_profit)
        self.assertEqual(result["jeweler_gross_margin_pct"], expected_margin)
        self.assertGreater(result["jeweler_gross_margin_pct"], 65.0)

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
        sum_landed = round(sum(i["us_landed_cost_usd"] for i in quote["items"]), 2)
        sum_retail = round(sum(i["us_retail_price_usd"] for i in quote["items"]), 2)
        expected_profit = round(sum_retail - sum_landed, 2)
        expected_margin = round((expected_profit / sum_retail) * 100.0, 1)

        self.assertEqual(quote["total_sample_cost"], sum_landed)
        self.assertEqual(quote["total_retail_value"], sum_retail)
        self.assertEqual(quote["retailer_profit"], expected_profit)
        self.assertEqual(quote["overall_margin_pct"], expected_margin)

        # Proposal text content checks
        proposal = quote["proposal_text"]
        self.assertIn("Apex Fine Jewelers", proposal)
        self.assertIn("Dallas, TX", proposal)
        self.assertIn("CaratGrid", proposal)
        self.assertIn("D K Jewellers", proposal)
        self.assertIn("Malca-Amit / Brink's Global", proposal)
        self.assertIn("HTS 7104.91.00", proposal)

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
        from agents.buyer_outreach_agent import BuyerOutreachAgent
        self.agent = BuyerOutreachAgent()

    def test_generate_lgd_wholesale_memo_pitch(self):
        """Verifies outreach agent creates high-impact LGD memo proposal with real math."""
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

        # Body must mention key ateliers and terms
        body = pitch["body"]
        self.assertIn("The New Age Diamonds", body)
        self.assertIn("D K Jewellers", body)
        self.assertIn("Euler Hermes", body)
        self.assertIn("30-Day Memo", body)
        self.assertIn("Malca-Amit / Brink's Global", body)

        # Check attached quote
        quote = pitch["quote"]
        self.assertEqual(len(quote["items"]), 4)
        self.assertGreater(quote["retailer_profit"], 4000.0)

    def test_batch_lgd_pitches_database_integration(self):
        """Verifies querying crawled US jewelers from database and generating batch pitches."""
        pitches = self.agent.generate_batch_lgd_pitches(count=3)
        self.assertGreaterEqual(len(pitches), 1)
        for p in pitches:
            self.assertTrue(p["company"])
            self.assertTrue(p["subject"])
            self.assertIn("LGD", p["subject"])
            self.assertIn("CaratGrid", p["body"])
            self.assertIn("quote", p)


if __name__ == "__main__":
    unittest.main()

