"use client";

import React, { useState } from "react";
import { Page, PageContent, Section, H1, H2, Intro, P } from "@/components/Layout";
import { Sparkles, DollarSign, TrendingUp, ShieldCheck, Landmark, CheckCircle2, ArrowRight } from "lucide-react";

export default function JewelryPage() {
  // Input parameters for finished piece
  const [jewelryType, setJewelryType] = useState("tennis_bracelet");
  const [goldKarat, setGoldKarat] = useState<10 | 14 | 18>(14);
  const [metalWeightGrams, setMetalWeightGrams] = useState(12.0);
  const [diamondCarats, setDiamondCarats] = useState(3.0);
  const [diamondType, setDiamondType] = useState<"lgd" | "natural">("lgd");
  const [targetUsRetail, setTargetUsRetail] = useState(1850);

  // Economic calculation benchmarks:
  // Gold spot rate benchmark: approx $78/gram for pure 24K gold
  // 10K = 41.7% gold, 14K = 58.5% gold, 18K = 75.0% gold
  const goldPurityMultiplier = goldKarat === 10 ? 0.417 : goldKarat === 14 ? 0.585 : 0.75;
  const rawGoldCost = metalWeightGrams * (78.0 * goldPurityMultiplier);

  // Casting labor: India SEEPZ/Surat casting ($2.50/g) vs US casting ($18.00/g)
  const indiaLaborCost = metalWeightGrams * 2.50;
  const usLaborCost = metalWeightGrams * 18.00;

  // Diamond cost per carat: LGD ($95/ct Surat wholesale) vs Natural ($1,200/ct SI1/G)
  const diamondCostPerCt = diamondType === "lgd" ? 95.0 : 1200.0;
  const totalDiamondCost = diamondCarats * diamondCostPerCt;

  // Setting labor: $1.20 per stone in India (approx 50 stones for 3ct bracelet)
  const settingLaborCost = 50 * 1.20;

  // Total Indian Factory FOB cost
  const factoryFobCost = Math.round((rawGoldCost + indiaLaborCost + totalDiamondCost + settingLaborCost) * 100) / 100;

  // Logistics & Insurance (Door to Door via Brink's/Malca-Amit air)
  const logisticsInsuredCost = 45.0;
  const usImportTariff = Math.round(factoryFobCost * 0.055 * 100) / 100; // 5.5% HSN 7113.19
  const totalLandedCost = Math.round((factoryFobCost + logisticsInsuredCost + usImportTariff) * 100) / 100;

  // Margins
  const grossProfitUsd = Math.round((targetUsRetail - totalLandedCost) * 100) / 100;
  const grossMarginPct = targetUsRetail > 0 ? Math.round((grossProfitUsd / targetUsRetail) * 100) : 0;

  // US domestic production comparison cost
  const usDomesticCost = Math.round((rawGoldCost + usLaborCost + totalDiamondCost + (50 * 5.50)) * 100) / 100;
  const manufacturingSavingsUsd = Math.round((usDomesticCost - factoryFobCost) * 100) / 100;

  return (
    <Page>
      <PageContent>
        <Section>
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b pb-6">
            <div>
              <H1>Finished Diamond & Lab-Grown Jewelry Pipeline</H1>
              <Intro>
                High-Margin Finished Goods Arbitrage: Surat Precision Casting vs. US Retail & Wholesale Distribution.
              </Intro>
            </div>
            <div className="flex items-center gap-2 bg-purple-50 text-purple-800 border border-purple-200 px-4 py-2 rounded-lg text-sm font-medium">
              <Sparkles className="w-5 h-5 text-purple-600" />
              55%+ Net Realized Gross Margin
            </div>
          </div>

          {/* Strategic Pillar Banner */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 my-8">
            <div className="p-5 rounded-xl border bg-card">
              <div className="flex items-center gap-2 text-sm font-bold text-black">
                <Landmark className="w-4 h-4 text-emerald-600" />
                Delaware LLC + Indian LLP
              </div>
              <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                Invoices paid in USD on Net-30 to US LLC front-office. Indian LLP receives export remittances with 100% tax-free partner distributions under Section 10(2A).
              </p>
            </div>
            <div className="p-5 rounded-xl border bg-card">
              <div className="flex items-center gap-2 text-sm font-bold text-black">
                <ShieldCheck className="w-4 h-4 text-blue-600" />
                Net-30 Euler Hermes Insurance
              </div>
              <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                Never hold loose unsold inventory. Sell to verified RJO/IJO independent jeweler chains with 90% credit default insurance backing every purchase order.
              </p>
            </div>
            <div className="p-5 rounded-xl border bg-card">
              <div className="flex items-center gap-2 text-sm font-bold text-black">
                <TrendingUp className="w-4 h-4 text-amber-600" />
                Labor & Setting Arbitrage
              </div>
              <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                $2.50/g Indian casting + $1.20 micro-prong diamond setting vs $18/g casting and $5.50 setting in US workshops saves over $350 per piece on labor alone.
              </p>
            </div>
          </div>

          {/* Interactive Calculator */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 p-6 rounded-2xl border bg-card">
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
        </Section>
      </PageContent>
    </Page>
  );
}
