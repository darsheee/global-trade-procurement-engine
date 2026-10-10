"use client";

import React, { useState, useMemo } from "react";
import { Page, PageContent, Section, H1, H2, Intro, P } from "@/components/Layout";
import {
  Sparkles,
  DollarSign,
  TrendingUp,
  ShieldCheck,
  Landmark,
  CheckCircle2,
  ArrowRight,
  Package,
  Building2,
  Copy,
  Check,
  FileText,
  Percent,
  Layers,
  Calculator,
  Truck
} from "lucide-react";
import {
  CORE_SKU_CATALOG,
  DELHI_LGD_SUPPLIERS,
  generateWholesaleQuote,
  CatalogSku
} from "@/lib/trade/lgd-catalog";

export default function JewelryPage() {
  // Mode switcher: "wholesale" (CaratGrid B2B Memo) vs "custom" (Single-Piece Unit Simulator)
  const [activeTab, setActiveTab] = useState<"wholesale" | "custom">("wholesale");

  // Wholesale Mode Parameters
  const [buyerName, setBuyerName] = useState("Apex Fine Jewelers");
  const [buyerCity, setBuyerCity] = useState("Dallas, TX");
  const [platformMarginPct, setPlatformMarginPct] = useState(18.0);
  const [copiedMemo, setCopiedMemo] = useState(false);

  // Compute live wholesale quote
  const wholesaleQuote = useMemo(() => {
    return generateWholesaleQuote(buyerName, buyerCity, platformMarginPct);
  }, [buyerName, buyerCity, platformMarginPct]);

  const handleCopyMemo = async () => {
    try {
      await navigator.clipboard.writeText(wholesaleQuote.proposal_text);
      setCopiedMemo(true);
      setTimeout(() => setCopiedMemo(false), 2500);
    } catch {
      // Fallback
    }
  };

  // Custom Simulator Parameters (Original single-piece model)
  const [jewelryType, setJewelryType] = useState("tennis_bracelet");
  const [goldKarat, setGoldKarat] = useState<10 | 14 | 18>(14);
  const [metalWeightGrams, setMetalWeightGrams] = useState(12.0);
  const [diamondCarats, setDiamondCarats] = useState(3.0);
  const [diamondType, setDiamondType] = useState<"lgd" | "natural">("lgd");
  const [targetUsRetail, setTargetUsRetail] = useState(1850);

  // Economic calculation benchmarks:
  const goldPurityMultiplier = goldKarat === 10 ? 0.417 : goldKarat === 14 ? 0.585 : 0.75;
  const rawGoldCost = metalWeightGrams * (78.0 * goldPurityMultiplier);
  const indiaLaborCost = metalWeightGrams * 2.50;
  const usLaborCost = metalWeightGrams * 18.00;
  const diamondCostPerCt = diamondType === "lgd" ? 95.0 : 1200.0;
  const totalDiamondCost = diamondCarats * diamondCostPerCt;
  const settingLaborCost = 50 * 1.20;

  const factoryFobCost = Math.round((rawGoldCost + indiaLaborCost + totalDiamondCost + settingLaborCost) * 100) / 100;
  const logisticsInsuredCost = 45.0;
  const usImportTariff = Math.round(factoryFobCost * 0.055 * 100) / 100;
  const totalLandedCost = Math.round((factoryFobCost + logisticsInsuredCost + usImportTariff) * 100) / 100;

  const grossProfitUsd = Math.round((targetUsRetail - totalLandedCost) * 100) / 100;
  const grossMarginPct = targetUsRetail > 0 ? Math.round((grossProfitUsd / targetUsRetail) * 100) : 0;

  const usDomesticCost = Math.round((rawGoldCost + usLaborCost + totalDiamondCost + 50 * 5.50) * 100) / 100;
  const manufacturingSavingsUsd = Math.round((usDomesticCost - factoryFobCost) * 100) / 100;

  return (
    <Page>
      <PageContent>
        <Section>
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b pb-6">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-semibold px-2 py-0.5 rounded bg-purple-100 text-purple-800 uppercase tracking-wide">
                  CaratGrid / AuraB2B Pipeline
                </span>
                <span className="text-xs text-muted-foreground">Delhi · Surat · New York</span>
              </div>
              <H1>Cross-Border Finished LGD Jewelry Platform</H1>
              <Intro>
                Factory-Direct Finished Goods Arbitrage: Linking Verified Delhi Ateliers with US Independent Retail Jewelers.
              </Intro>
            </div>
            <div className="flex items-center gap-2 bg-purple-50 text-purple-800 border border-purple-200 px-4 py-2 rounded-lg text-sm font-medium self-start md:self-auto">
              <Sparkles className="w-5 h-5 text-purple-600" />
              65%–75% Gross Margin Arbitrage
            </div>
          </div>

          {/* Strategic Pillar Banner */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 my-8">
            <div className="p-5 rounded-xl border bg-card shadow-sm">
              <div className="flex items-center gap-2 text-sm font-bold text-foreground">
                <Landmark className="w-4 h-4 text-emerald-600" />
                Delaware LLC + Indian LLP
              </div>
              <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                Invoices paid in USD on Net-30 to US LLC front-office desk. Indian export remittances enjoy tax-free LLP partner distributions under Section 10(2A).
              </p>
            </div>
            <div className="p-5 rounded-xl border bg-card shadow-sm">
              <div className="flex items-center gap-2 text-sm font-bold text-black">
                <ShieldCheck className="w-4 h-4 text-blue-600" />
                30-Day Memo + Euler Hermes
              </div>
              <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                Risk-free consignment terms for verified US storefronts. Purchase orders backed by 90% trade credit insurance default protection.
              </p>
            </div>
            <div className="p-5 rounded-xl border bg-card shadow-sm">
              <div className="flex items-center gap-2 text-sm font-bold text-black">
                <TrendingUp className="w-4 h-4 text-amber-600" />
                Labor & Setting Arbitrage
              </div>
              <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                $2.50/g Indian casting + $1.20 micro-prong setting vs $18/g casting and $5.50 setting in US workshops saves over $350 per piece on bench labor alone.
              </p>
            </div>
          </div>

          {/* Dual-Mode Selector Tabs */}
          <div className="flex items-center gap-3 p-1.5 bg-muted/60 rounded-xl max-w-lg mb-8 border">
            <button
              onClick={() => setActiveTab("wholesale")}
              className={`flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg text-xs font-semibold transition-all ${
                activeTab === "wholesale"
                  ? "bg-background text-foreground shadow-sm border"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              <Package className="w-4 h-4 text-purple-600" />
              B2B Wholesale Memo Starter Kit
            </button>
            <button
              onClick={() => setActiveTab("custom")}
              className={`flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg text-xs font-semibold transition-all ${
                activeTab === "custom"
                  ? "bg-background text-foreground shadow-sm border"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              <Calculator className="w-4 h-4 text-emerald-600" />
              Single-Piece Unit Simulator
            </button>
          </div>

          {/* TAB 1: B2B WHOLESALE MEMO STARTER KIT GENERATOR */}
          {activeTab === "wholesale" && (
            <div className="space-y-8">
              {/* Buyer & Memo Parameters */}
              <div className="p-6 rounded-2xl border bg-card shadow-sm">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b pb-4 mb-6">
                  <div>
                    <H2 className="mb-1">Wholesale Showcase Memo Generator</H2>
                    <p className="text-xs text-muted-foreground">
                      Configure target US storefront credentials to generate an instant FOB/CIF commercial memo quotation with 4 high-velocity engagement pieces.
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={handleCopyMemo}
                      className="inline-flex items-center gap-1.5 px-3.5 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-xs font-medium transition-colors shadow-sm"
                    >
                      {copiedMemo ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                      {copiedMemo ? "Copied Proposal!" : "Copy Memo Quotation"}
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="text-xs font-semibold text-muted-foreground uppercase">Target US Retail Jeweler</label>
                    <input
                      type="text"
                      value={buyerName}
                      onChange={(e) => setBuyerName(e.target.value)}
                      placeholder="e.g. Apex Fine Jewelers"
                      className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-muted-foreground uppercase">Storefront Location (City, State)</label>
                    <input
                      type="text"
                      value={buyerCity}
                      onChange={(e) => setBuyerCity(e.target.value)}
                      placeholder="e.g. Dallas, TX"
                      className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-muted-foreground uppercase">Platform Wholesale Markup (%)</label>
                    <input
                      type="number"
                      step="0.5"
                      min="5"
                      max="40"
                      value={platformMarginPct}
                      onChange={(e) => setPlatformMarginPct(Number(e.target.value))}
                      className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                    />
                  </div>
                </div>
              </div>

              {/* Portfolio Financial Performance Summary */}
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3 p-5 rounded-2xl bg-purple-50/70 border border-purple-200">
                <div className="p-3 bg-white rounded-xl border border-purple-100 shadow-xs">
                  <div className="text-[11px] font-semibold text-muted-foreground uppercase">Wholesale Invoice</div>
                  <div className="text-lg font-bold text-purple-950 mt-1">
                    ${wholesaleQuote.total_wholesale_cost.toFixed(2)}
                  </div>
                  <div className="text-[10px] text-muted-foreground mt-0.5">Factory FOB + platform</div>
                </div>

                <div className="p-3 bg-white rounded-xl border border-purple-100 shadow-xs">
                  <div className="text-[11px] font-semibold text-muted-foreground uppercase">Total Landed (CIF)</div>
                  <div className="text-lg font-bold text-purple-900 mt-1">
                    ${wholesaleQuote.total_sample_cost.toFixed(2)}
                  </div>
                  <div className="text-[10px] text-purple-700 font-medium mt-0.5">Air courier + 5.5% duty</div>
                </div>

                <div className="p-3 bg-white rounded-xl border border-purple-100 shadow-xs">
                  <div className="text-[11px] font-semibold text-muted-foreground uppercase">Suggested Retail</div>
                  <div className="text-lg font-bold text-gray-900 mt-1">
                    ${wholesaleQuote.total_retail_value.toFixed(2)}
                  </div>
                  <div className="text-[10px] text-muted-foreground mt-0.5">Independent US retail</div>
                </div>

                <div className="p-3 bg-white rounded-xl border border-emerald-200 shadow-xs">
                  <div className="text-[11px] font-semibold text-emerald-800 uppercase">Jeweler Cash Profit</div>
                  <div className="text-lg font-extrabold text-emerald-600 mt-1">
                    ${wholesaleQuote.retailer_profit.toFixed(2)}
                  </div>
                  <div className="text-[10px] text-emerald-700 font-medium mt-0.5">Net realized cash</div>
                </div>

                <div className="col-span-2 md:col-span-1 p-3 bg-emerald-600 text-white rounded-xl shadow-xs">
                  <div className="text-[11px] font-semibold text-emerald-100 uppercase">Portfolio Margin</div>
                  <div className="text-2xl font-black mt-1">
                    {wholesaleQuote.overall_margin_pct.toFixed(1)}%
                  </div>
                  <div className="text-[10px] text-emerald-100 mt-0.5">Zero capital lockup</div>
                </div>
              </div>

              {/* 4-Piece Showcase Starter Kit Line Items */}
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-base font-bold text-foreground">Curated 4-Piece Showcase Line Items</h3>
                    <p className="text-xs text-muted-foreground">Certified finished goods manufactured by verified Delhi ateliers with IGI certification.</p>
                  </div>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
                    Door-to-Door Insured Air Freight Included
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {wholesaleQuote.items.map((it, idx) => (
                    <div key={it.sku_code} className="p-5 rounded-xl border bg-card shadow-sm hover:shadow-md transition-shadow">
                      <div className="flex items-start justify-between gap-2 border-b pb-3 mb-3">
                        <div>
                          <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-muted text-muted-foreground">
                            {it.sku_code}
                          </span>
                          <h4 className="text-sm font-bold text-foreground mt-1.5">{it.title}</h4>
                          <div className="text-xs text-muted-foreground mt-0.5">
                            {CORE_SKU_CATALOG[idx]?.color_clarity} · {CORE_SKU_CATALOG[idx]?.gold_karat}K Solid Gold ({CORE_SKU_CATALOG[idx]?.gold_grams}g)
                          </div>
                        </div>
                        <span className="text-xs font-bold px-2 py-1 rounded bg-emerald-50 text-emerald-700 border border-emerald-200 whitespace-nowrap">
                          {it.jeweler_gross_margin_pct.toFixed(1)}% Margin
                        </span>
                      </div>

                      <div className="grid grid-cols-2 gap-3 text-xs mb-4">
                        <div className="space-y-1">
                          <div className="text-muted-foreground">Factory FOB Cost:</div>
                          <div className="font-semibold text-foreground">${it.factory_fob_usd.toFixed(2)}</div>
                          <div className="text-muted-foreground">Wholesale Invoice:</div>
                          <div className="font-semibold text-purple-700">${it.wholesale_price_usd.toFixed(2)}</div>
                        </div>
                        <div className="space-y-1">
                          <div className="text-muted-foreground">US Landed (CIF Door):</div>
                          <div className="font-semibold text-foreground">${it.us_landed_cost_usd.toFixed(2)}</div>
                          <div className="text-muted-foreground">US Benchmark Retail:</div>
                          <div className="font-semibold text-foreground">${it.us_retail_price_usd.toFixed(2)}</div>
                        </div>
                      </div>

                      <div className="pt-3 border-t flex items-center justify-between bg-muted/20 -mx-5 -mb-5 px-5 py-3 rounded-b-xl">
                        <span className="text-xs font-medium text-muted-foreground">Net Profit Per Piece:</span>
                        <span className="text-sm font-extrabold text-emerald-600">
                          +${it.jeweler_profit_usd.toFixed(2)}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Verified Delhi Atelier Partners */}
              <div className="p-6 rounded-2xl border bg-card shadow-sm">
                <div className="flex items-center gap-2 mb-2">
                  <Building2 className="w-5 h-5 text-purple-600" />
                  <h3 className="text-base font-bold text-foreground">Verified Delhi Atelier Manufacturing Network</h3>
                </div>
                <p className="text-xs text-muted-foreground mb-5">
                  Direct production contracts with vetted exporters registered under the Directorate General of Foreign Trade (DGFT) and the Gem & Jewellery Export Promotion Council (GJEPC).
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {DELHI_LGD_SUPPLIERS.map((s) => (
                    <div key={s.iec_code} className="p-4 rounded-xl border bg-muted/20 text-xs space-y-2">
                      <div className="font-bold text-foreground line-clamp-1">{s.company_name}</div>
                      <div className="text-[11px] text-muted-foreground">{s.hub}</div>
                      <div className="flex items-center gap-1.5 pt-1">
                        <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-muted font-medium">
                          IEC: {s.iec_code}
                        </span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-blue-50 text-blue-700 font-medium">
                          {s.production_sla_days}-Day SLA
                        </span>
                      </div>
                      <p className="text-[11px] text-muted-foreground line-clamp-2 pt-1 border-t">
                        {s.specialization}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Formatted Memo Proposal Preview */}
              <div className="p-6 rounded-2xl border bg-card shadow-sm">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <FileText className="w-5 h-5 text-purple-600" />
                    <h3 className="text-base font-bold text-foreground">Generated Commercial Memo Quotation</h3>
                  </div>
                  <button
                    onClick={handleCopyMemo}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-muted hover:bg-muted/80 text-foreground rounded-lg text-xs font-semibold transition-colors border"
                  >
                    {copiedMemo ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                    {copiedMemo ? "Copied" : "Copy Raw Memo"}
                  </button>
                </div>
                <pre className="p-4 bg-muted/50 rounded-xl text-xs font-mono text-muted-foreground whitespace-pre-wrap overflow-x-auto border leading-relaxed">
                  {wholesaleQuote.proposal_text}
                </pre>
              </div>
            </div>
          )}

          {/* TAB 2: SINGLE-PIECE UNIT SIMULATOR (ORIGINAL SIMULATOR) */}
          {activeTab === "custom" && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 p-6 rounded-2xl border bg-card shadow-sm">
              <div className="space-y-4 lg:col-span-2">
                <H2>Unit Economics & Bill of Materials Simulator</H2>
                <P>Configure piece parameters to simulate exact Surat FOB casting cost, door-to-door vaulting, and US wholesale spreads.</P>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-3">
                  <div>
                    <label className="text-xs font-semibold text-muted-foreground uppercase">Gold Alloy Karat</label>
                    <select
                      value={goldKarat}
                      onChange={(e: any) => setGoldKarat(Number(e.target.value) as any)}
                      className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                    >
                      <option value={10}>10K Solid Gold (41.7% Pure - US Volume Leader)</option>
                      <option value={14}>14K Solid Gold (58.5% Pure - Fine Jewelry Standard)</option>
                      <option value={18}>18K Solid Gold (75.0% Pure - Luxury Flagship)</option>
                    </select>
                  </div>

                  <div>
                    <label className="text-xs font-semibold text-muted-foreground uppercase">Metal Weight (Grams)</label>
                    <input
                      type="number"
                      step="0.5"
                      value={metalWeightGrams}
                      onChange={(e) => setMetalWeightGrams(Number(e.target.value))}
                      className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                    />
                  </div>

                  <div>
                    <label className="text-xs font-semibold text-muted-foreground uppercase">Diamond Classification</label>
                    <select
                      value={diamondType}
                      onChange={(e: any) => setDiamondType(e.target.value)}
                      className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                    >
                      <option value="lgd">Lab-Grown Diamond (CVD/HPHT - Surat Hub @ $95/ct)</option>
                      <option value="natural">Natural Mined Diamond (G7 / KPC Cleared @ $1,200/ct)</option>
                    </select>
                  </div>

                  <div>
                    <label className="text-xs font-semibold text-muted-foreground uppercase">Total Diamond Weight (Carats)</label>
                    <input
                      type="number"
                      step="0.25"
                      value={diamondCarats}
                      onChange={(e) => setDiamondCarats(Number(e.target.value))}
                      className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                    />
                  </div>

                  <div>
                    <label className="text-xs font-semibold text-muted-foreground uppercase">Target US Retail Sale Price (USD)</label>
                    <input
                      type="number"
                      value={targetUsRetail}
                      onChange={(e) => setTargetUsRetail(Number(e.target.value))}
                      className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                    />
                  </div>

                  <div className="flex flex-col justify-end">
                    <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-xs text-emerald-800">
                      <strong>US Manufacturing Cost:</strong> ${usDomesticCost.toFixed(2)} USD.<br />
                      Direct factory sourcing saves <strong>${manufacturingSavingsUsd.toFixed(2)} USD</strong> per piece.
                    </div>
                  </div>
                </div>
              </div>

              {/* Financial Output Card */}
              <div className="p-6 rounded-xl bg-muted/40 border flex flex-col justify-between">
                <div>
                  <div className="text-xs font-semibold text-muted-foreground uppercase">Bill of Materials (BOM)</div>
                  <div className="space-y-2 mt-4 text-xs">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Gold Alloy ({metalWeightGrams}g @ {goldKarat}K):</span>
                      <span className="font-medium">${rawGoldCost.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Casting Labor (Surat Hub):</span>
                      <span className="font-medium">${indiaLaborCost.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Diamonds ({diamondCarats}ct {diamondType.toUpperCase()}):</span>
                      <span className="font-medium">${totalDiamondCost.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Stone Setting Labor (50 stones):</span>
                      <span className="font-medium">${settingLaborCost.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between font-semibold border-t pt-2">
                      <span>Factory FOB Price:</span>
                      <span>${factoryFobCost.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Insured Door Delivery (Brink's):</span>
                      <span className="font-medium">${logisticsInsuredCost.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">US Customs Tariff (5.5%):</span>
                      <span className="font-medium">${usImportTariff.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between font-bold text-sm border-t pt-2">
                      <span>Total US Landed Cost:</span>
                      <span className="text-purple-700">${totalLandedCost.toFixed(2)}</span>
                    </div>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t">
                  <div className="text-xs text-muted-foreground uppercase font-semibold">Net In-Hand Profit Per Unit</div>
                  <div className="text-3xl font-extrabold text-emerald-600 mt-1">
                    ${grossProfitUsd.toFixed(2)}
                  </div>
                  <div className="text-xs font-bold text-emerald-700 mt-0.5">
                    {grossMarginPct}% Realized Gross Margin
                  </div>
                </div>
              </div>
            </div>
          )}
        </Section>
      </PageContent>
    </Page>
  );
}
