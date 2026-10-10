/**
 * LGD B2B Wholesale Catalog, Supplier Data, and Margin Calculator
 * Used by CaratGrid / AuraB2B cross-border pipeline.
 */

export interface SupplierInfo {
  company_name: string;
  corporate_type: string;
  iec_code: string;
  gstin?: string;
  turnover_tier: string;
  hub: string;
  phone?: string;
  email?: string;
  specialization: string;
  production_sla_days: number;
}

export interface CatalogSku {
  sku_code: string;
  title: string;
  diamond_carat: number;
  color_clarity: string;
  gold_karat: number;
  gold_grams: number;
  loose_stone_cost_usd: number;
  mount_casting_labor_usd: number;
  igi_certification_usd: number;
  us_benchmark_retail_usd: number;
}

export interface SkuArbitrageResult {
  sku_code: string;
  title: string;
  carats: number;
  factory_fob_usd: number;
  platform_take_rate_usd: number;
  wholesale_price_usd: number;
  allocated_shipping_usd: number;
  customs_duty_usd: number;
  us_landed_cost_usd: number;
  us_retail_price_usd: number;
  jeweler_profit_usd: number;
  jeweler_gross_margin_pct: number;
}

export interface WholesaleQuote {
  buyer_name: string;
  buyer_city: string;
  platform_margin_pct: number;
  items: SkuArbitrageResult[];
  total_wholesale_cost: number;
  total_sample_cost: number;
  total_retail_value: number;
  retailer_profit: number;
  overall_margin_pct: number;
  suppliers: SupplierInfo[];
  proposal_text: string;
  generated_at: string;
}

// Verified Delhi LGD ateliers from master database
export const DELHI_LGD_SUPPLIERS: SupplierInfo[] = [
  {
    company_name: "The New Age Diamonds Private Limited",
    corporate_type: "Private Limited",
    iec_code: "AAJCN2214K",
    gstin: "07AAJCN2214K1ZH",
    turnover_tier: "₹11-25 Cr",
    hub: "Netaji Subhash Place, Pitampura, Delhi",
    phone: "+91 98180 63683",
    email: "info@thenewagediamonds.com",
    specialization: "CVD/HPHT certified solitaires, engagement rings, 14K/18K custom mounts",
    production_sla_days: 5
  },
  {
    company_name: "Altin Global LLP",
    corporate_type: "LLP",
    iec_code: "ACLFA5590Q",
    gstin: "07ACLFA5590Q1ZL",
    turnover_tier: "₹41-99 Lakhs",
    hub: "Sector 5 Rohini, Delhi",
    phone: "+91 93118 52242",
    email: "altingloballlp@gmail.com",
    specialization: "14K/18K LGD solitaires, eternity bands, custom diamond luxury watches",
    production_sla_days: 6
  },
  {
    company_name: "Sequoia Overseas Co",
    corporate_type: "Proprietorship",
    iec_code: "CNQPP2527J",
    gstin: "07CNQPP2527J1ZI",
    turnover_tier: "₹1-10 Cr",
    hub: "Keshav Puram, Tri Nagar, Delhi",
    specialization: "IGI/GIA certified loose LGD and hallmarked fine jewelry",
    production_sla_days: 7
  },
  {
    company_name: "D K Jewellers",
    corporate_type: "Proprietorship",
    iec_code: "ACUPG3187C",
    gstin: "07ACUPG3187C1Z5",
    turnover_tier: "₹1-10 Cr",
    hub: "Old Delhi / North Delhi",
    phone: "+91 11 2325 0000",
    email: "trade@dkjewellers.in",
    specialization: "Bridal, couture, and fine everyday jewelry in solid gold, IGI-certified LGD/diamonds, BIS-hallmarked mounts",
    production_sla_days: 5
  }
];

// Standard 4-Piece Showcase Memo Starter Kit
export const CORE_SKU_CATALOG: CatalogSku[] = [
  {
    sku_code: "LGD-RING-200-RND",
    title: "2.00ct Round Brilliant 4-Prong Solitaire Ring",
    diamond_carat: 2.0,
    color_clarity: "F/VS1 Ideal Cut (IGI Certified)",
    gold_karat: 14,
    gold_grams: 3.5,
    loose_stone_cost_usd: 250.0,
    mount_casting_labor_usd: 240.0,
    igi_certification_usd: 25.0,
    us_benchmark_retail_usd: 2250.0
  },
  {
    sku_code: "LGD-RING-150-OVL",
    title: "1.50ct Oval Hidden-Halo Solitaire Ring",
    diamond_carat: 1.5,
    color_clarity: "E/VVS2 Ideal Cut (IGI Certified)",
    gold_karat: 14,
    gold_grams: 3.8,
    loose_stone_cost_usd: 195.0,
    mount_casting_labor_usd: 260.0,
    igi_certification_usd: 25.0,
    us_benchmark_retail_usd: 1950.0
  },
  {
    sku_code: "LGD-BRAC-300-EMR",
    title: "3.00 ctw Emerald Cut Tennis Bracelet",
    diamond_carat: 3.0,
    color_clarity: "F/VS 50-Stone Matched Parcel",
    gold_karat: 14,
    gold_grams: 11.5,
    loose_stone_cost_usd: 330.0,
    mount_casting_labor_usd: 680.0,
    igi_certification_usd: 40.0,
    us_benchmark_retail_usd: 2950.0
  },
  {
    sku_code: "LGD-STUD-100-RND",
    title: "1.00 ctw (0.50ct each) 4-Prong Stud Earrings",
    diamond_carat: 1.0,
    color_clarity: "E/VS1 Ideal Cut Matched Pair",
    gold_karat: 14,
    gold_grams: 1.8,
    loose_stone_cost_usd: 120.0,
    mount_casting_labor_usd: 140.0,
    igi_certification_usd: 20.0,
    us_benchmark_retail_usd: 895.0
  }
];

export function calculateSkuArbitrage(
  sku: CatalogSku,
  platformMarginPct: number = 18.0
): SkuArbitrageResult {
  const safeMarginPct = typeof platformMarginPct === "number" && !isNaN(platformMarginPct)
    ? Math.max(0, platformMarginPct)
    : 18.0;

  const factoryFob = Math.round((sku.loose_stone_cost_usd + sku.mount_casting_labor_usd + sku.igi_certification_usd) * 100) / 100;
  const platformFee = Math.round(factoryFob * (safeMarginPct / 100) * 100) / 100;
  const wholesalePrice = Math.round((factoryFob + platformFee) * 100) / 100;

  const allocatedShipping = 35.0;
  const customsDuty = Math.round(wholesalePrice * 0.055 * 100) / 100;
  const totalLandedCost = Math.round((wholesalePrice + allocatedShipping + customsDuty) * 100) / 100;

  const retailPrice = sku.us_benchmark_retail_usd;
  const jewelerProfit = Math.round((retailPrice - totalLandedCost) * 100) / 100;
  const jewelerMarginPct = retailPrice > 0 ? Math.round((jewelerProfit / retailPrice) * 1000) / 10 : 0;

  return {
    sku_code: sku.sku_code,
    title: sku.title,
    carats: sku.diamond_carat,
    factory_fob_usd: factoryFob,
    platform_take_rate_usd: platformFee,
    wholesale_price_usd: wholesalePrice,
    allocated_shipping_usd: allocatedShipping,
    customs_duty_usd: customsDuty,
    us_landed_cost_usd: totalLandedCost,
    us_retail_price_usd: retailPrice,
    jeweler_profit_usd: jewelerProfit,
    jeweler_gross_margin_pct: jewelerMarginPct
  };
}

export function generateWholesaleQuote(
  buyerName: string,
  buyerCity: string,
  platformMarginPct: number = 18.0,
  customSkus?: CatalogSku[]
): WholesaleQuote {
  const safeMarginPct = typeof platformMarginPct === "number" && !isNaN(platformMarginPct)
    ? Math.max(0, platformMarginPct)
    : 18.0;
  const catalog = customSkus || CORE_SKU_CATALOG;
  const items = catalog.map((sku) => calculateSkuArbitrage(sku, safeMarginPct));

  const totalWholesaleCost = Math.round(items.reduce((acc, i) => acc + i.wholesale_price_usd, 0) * 100) / 100;
  const totalSampleCost = Math.round(items.reduce((acc, i) => acc + i.us_landed_cost_usd, 0) * 100) / 100;
  const totalRetailValue = Math.round(items.reduce((acc, i) => acc + i.us_retail_price_usd, 0) * 100) / 100;
  const retailerProfit = Math.round((totalRetailValue - totalSampleCost) * 100) / 100;
  const overallMarginPct = totalRetailValue > 0 ? Math.round((retailerProfit / totalRetailValue) * 1000) / 10 : 0;

  const proposalText = `================================================================================
B2B EXCLUSIVE WHOLESALE MEMO PROPOSAL: INDIAN LGD FINISHED JEWELRY
Prepared For: ${buyerName} (${buyerCity}, USA)
Facilitated By: CaratGrid / Global Trade Intelligence Engine
Atelier Partners: The New Age Diamonds, Altin Global LLP, Sequoia Overseas, D K Jewellers
================================================================================

Executive Summary:
Unlock 65%–75% gross margins on bridal engagement rings with zero capital lockup.
Direct factory dispatch from certified Delhi/Surat ateliers to your storefront within 5-7 business days.
Fully IGI-certified, hallmarked 14K/18K solid gold, and backed by 30-day memo terms.

Curated 4-Piece Showcase Starter Kit:
--------------------------------------------------------------------------------
${items
  .map(
    (it) => `• ${it.title} (${it.sku_code}):
  - Factory FOB: $${it.factory_fob_usd.toFixed(2)} | Wholesale Invoice: $${it.wholesale_price_usd.toFixed(2)}
  - US Landed Cost (CIF Door): $${it.us_landed_cost_usd.toFixed(2)}
  - Recommended Retail Price: $${it.us_retail_price_usd.toFixed(2)}
  - Your Net Profit Per Piece: $${it.jeweler_profit_usd.toFixed(2)} (${it.jeweler_gross_margin_pct.toFixed(1)}% Gross Margin)`
  )
  .join("\n")}
--------------------------------------------------------------------------------
Starter Kit Financials:
• Total Wholesale Platform Invoice: $${totalWholesaleCost.toFixed(2)}
• Total Landed Working Capital Required: $${totalSampleCost.toFixed(2)}
• Total Retail Sales Value: $${totalRetailValue.toFixed(2)}
• Net Retailer Cash Profit: $${retailerProfit.toFixed(2)} (${overallMarginPct.toFixed(1)}% Portfolio Margin)
• Logistics: 100% Insured Door-to-Door Air Courier via Malca-Amit / Brink's Global ($35/piece)
• Customs Classification: US HTS 7104.91.00 (Synthetic Diamonds) / 7113.19 (Gold Jewelry - 5.5% Duty)
• Payment Terms: Net-30 Memo backed by Euler Hermes / Delaware corporate desk
================================================================================`;

  return {
    buyer_name: buyerName,
    buyer_city: buyerCity,
    platform_margin_pct: safeMarginPct,
    items,
    total_wholesale_cost: totalWholesaleCost,
    total_sample_cost: totalSampleCost,
    total_retail_value: totalRetailValue,
    retailer_profit: retailerProfit,
    overall_margin_pct: overallMarginPct,
    suppliers: DELHI_LGD_SUPPLIERS,
    proposal_text: proposalText,
    generated_at: new Date().toISOString()
  };
}
