import { NextResponse } from "next/server";
import {
  DELHI_LGD_SUPPLIERS,
  CORE_SKU_CATALOG,
  calculateSkuArbitrage,
  generateWholesaleQuote,
  SupplierInfo,
  CatalogSku,
  SkuArbitrageResult,
  WholesaleQuote
} from "@/lib/trade/lgd-catalog";

export type { SupplierInfo, CatalogSku, SkuArbitrageResult, WholesaleQuote };
export { DELHI_LGD_SUPPLIERS, CORE_SKU_CATALOG, calculateSkuArbitrage, generateWholesaleQuote };

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const buyerName = searchParams.get("buyer") || searchParams.get("buyer_name") || "Apex Fine Jewelers";
  const buyerCity = searchParams.get("city") || searchParams.get("buyer_city") || "Dallas, TX";
  const marginParam = searchParams.get("margin") || searchParams.get("platform_margin_pct");
  const platformMarginPct = marginParam ? parseFloat(marginParam) : 18.0;

  const quote = generateWholesaleQuote(buyerName, buyerCity, platformMarginPct);

  return NextResponse.json({
    success: true,
    quote,
    catalog: CORE_SKU_CATALOG,
    suppliers: DELHI_LGD_SUPPLIERS
  });
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const buyerName = body.buyer_name || body.buyer || "Apex Fine Jewelers";
    const buyerCity = body.buyer_city || body.city || "Dallas, TX";
    const platformMarginPct = typeof body.platform_margin_pct === "number" ? body.platform_margin_pct : 18.0;
    const customSkus = Array.isArray(body.skus) ? body.skus : undefined;

    const quote = generateWholesaleQuote(buyerName, buyerCity, platformMarginPct, customSkus);

    return NextResponse.json({
      success: true,
      quote,
      catalog: CORE_SKU_CATALOG,
      suppliers: DELHI_LGD_SUPPLIERS
    });
  } catch (error: any) {
    return NextResponse.json(
      { success: false, error: error?.message || "Invalid request body" },
      { status: 400 }
    );
  }
}
