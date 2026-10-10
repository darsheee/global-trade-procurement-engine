import { describe, it, expect } from "bun:test";
import {
  DELHI_LGD_SUPPLIERS,
  CORE_SKU_CATALOG,
  calculateSkuArbitrage,
  generateWholesaleQuote
} from "./lgd-catalog";

describe("LGD B2B Wholesale Catalog & Margin Engine", () => {
  it("should have all 4 verified Delhi ateliers with IEC compliance codes", () => {
    expect(DELHI_LGD_SUPPLIERS.length).toBeGreaterThanOrEqual(4);
    const names = DELHI_LGD_SUPPLIERS.map((s) => s.company_name);
    expect(names).toContain("The New Age Diamonds Private Limited");
    expect(names).toContain("Altin Global LLP");
    expect(names).toContain("Sequoia Overseas Co");
    expect(names).toContain("D K Jewellers");

    for (const supplier of DELHI_LGD_SUPPLIERS) {
      expect(supplier.iec_code).toBeTruthy();
      expect(supplier.hub).toContain("Delhi");
      expect(supplier.production_sla_days).toBeGreaterThan(0);
    }
  });

  it("should verify core 4-piece catalog SKUs integrity", () => {
    expect(CORE_SKU_CATALOG.length).toBe(4);
    const skuCodes = CORE_SKU_CATALOG.map((s) => s.sku_code);
    expect(skuCodes).toEqual([
      "LGD-RING-200-RND",
      "LGD-RING-150-OVL",
      "LGD-BRAC-300-EMR",
      "LGD-STUD-100-RND"
    ]);

    for (const sku of CORE_SKU_CATALOG) {
      expect(sku.loose_stone_cost_usd).toBeGreaterThan(0);
      expect(sku.mount_casting_labor_usd).toBeGreaterThan(0);
      expect(sku.igi_certification_usd).toBeGreaterThan(0);
      expect(sku.us_benchmark_retail_usd).toBeGreaterThan(0);
    }
  });

  it("should compute accurate SKU landed cost and margins with round-half-up customs duty", () => {
    // Test 3.00 ctw Tennis Bracelet (LGD-BRAC-300-EMR) half-cent duty boundary (1239 * 0.055 = 68.145 -> $68.15)
    const tennisBracelet = CORE_SKU_CATALOG[2];
    const res = calculateSkuArbitrage(tennisBracelet, 18.0);

    expect(res.factory_fob_usd).toBe(1050.0);
    expect(res.platform_take_rate_usd).toBe(189.0);
    expect(res.wholesale_price_usd).toBe(1239.0);
    expect(res.customs_duty_usd).toBe(68.15);
    expect(res.us_landed_cost_usd).toBe(1342.15);
    expect(res.us_retail_price_usd).toBe(2950.0);
    expect(res.jeweler_profit_usd).toBe(1607.85);
    expect(res.jeweler_gross_margin_pct).toBe(54.5);
  });

  it("should generate a consistent complete 4-piece wholesale quote", () => {
    const quote = generateWholesaleQuote("Apex Fine Jewelers", "Dallas, TX", 18.0);

    expect(quote.buyer_name).toBe("Apex Fine Jewelers");
    expect(quote.buyer_city).toBe("Dallas, TX");
    expect(quote.items.length).toBe(4);

    // Verify exact portfolio totals
    expect(quote.total_wholesale_cost).toBe(2743.5);
    expect(quote.total_sample_cost).toBe(3034.39);
    expect(quote.total_retail_value).toBe(8045.0);
    expect(quote.retailer_profit).toBe(5010.61);
    expect(quote.overall_margin_pct).toBe(62.3);

    // Proposal text content checks
    expect(quote.proposal_text).toContain("Apex Fine Jewelers");
    expect(quote.proposal_text).toContain("Dallas, TX");
    expect(quote.proposal_text).toContain("Total Wholesale Platform Invoice: $2743.50");
    expect(quote.proposal_text).toContain("Total Landed Working Capital Required: $3034.39");
    expect(quote.proposal_text).toContain("Net Retailer Cash Profit: $5010.61");
  });

  it("should handle edge cases safely (NaN margin, negative margin, zero retail)", () => {
    // NaN margin falls back to 18.0
    const nanQuote = generateWholesaleQuote("Test", "City", NaN);
    expect(nanQuote.platform_margin_pct).toBe(18.0);
    expect(nanQuote.total_wholesale_cost).toBe(2743.5);

    // Zero retail SKU
    const zeroRetailSku = {
      sku_code: "TEST-ZERO",
      title: "Zero Retail",
      diamond_carat: 1.0,
      color_clarity: "F/VS",
      gold_karat: 14,
      gold_grams: 2.0,
      loose_stone_cost_usd: 100,
      mount_casting_labor_usd: 100,
      igi_certification_usd: 10,
      us_benchmark_retail_usd: 0
    };
    const zeroRes = calculateSkuArbitrage(zeroRetailSku);
    expect(zeroRes.jeweler_gross_margin_pct).toBe(0);
    expect(zeroRes.jeweler_profit_usd).toBe(-zeroRes.us_landed_cost_usd);
  });
});
