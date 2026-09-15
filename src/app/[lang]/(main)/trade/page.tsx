"use client";

import React, { useState } from "react";
import { Page, PageContent, Section, H1, H2, Intro, P } from "@/components/Layout";
import usImportersData from "@/../data/trade/us_importers_crawled.json";
import exportersData from "@/../data/trade/exporters_sample.json";
import metricsData from "@/../data/trade/trade_metrics.json";
import { Search, Building2, Globe, Mail, Phone, ArrowUpRight, Calculator, ShieldCheck } from "lucide-react";

export default function TradePage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [activeTab, setActiveTab] = useState<"importers" | "exporters" | "calculator">("importers");
  
  // Calculator state
  const [fobPrice, setFobPrice] = useState(350);
  const [retailPrice, setRetailPrice] = useState(1200);
  const [weightKg, setWeightKg] = useState(0.25);
  const [mode, setMode] = useState<"air" | "sea">("air");

  const freightCost = mode === "air" ? Math.max(weightKg * 8.5, 25) : Math.max(weightKg * 0.45, 150);
  const insurance = Math.round(fobPrice * 0.0035 * 100) / 100;
  const cif = Math.round((fobPrice + freightCost + insurance) * 100) / 100;
  const duty = Math.round(cif * 0.055 * 100) / 100;
  const mpf = Math.min(Math.max(Math.round(cif * 0.003464 * 100) / 100, 31.67), 614.35);
  const totalLanded = Math.round((cif + duty + mpf) * 100) / 100;
  const marginUsd = Math.round((retailPrice - totalLanded) * 100) / 100;
  const marginPct = retailPrice > 0 ? Math.round((marginUsd / retailPrice) * 100) : 0;

  const filteredImporters = usImportersData.filter((b: any) =>
    b.company_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    b.industry_category?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    b.city?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredExporters = exportersData.filter((e: any) =>
    e.company_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    e.deal_in?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    e.city?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Page>
      <PageContent>
        <Section>
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b pb-6">
            <div>
              <H1>Bilateral Global Trade & Supplier Radar</H1>
              <Intro>
                Matching {metricsData.total_exporters?.toLocaleString()} Verified Indian Manufacturers with {metricsData.total_importers} US Corporate Importers & Wholesalers.
              </Intro>
            </div>
            <div className="flex items-center gap-2 bg-emerald-50 text-emerald-800 border border-emerald-200 px-4 py-2 rounded-lg text-sm font-medium">
              <ShieldCheck className="w-5 h-5 text-emerald-600" />
              Delaware LLC + Indian LLP Compliant
            </div>
          </div>

          {/* Quick Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 my-8">
            <div className="p-4 rounded-xl border bg-card shadow-sm">
              <div className="text-xs text-muted-foreground uppercase font-semibold">Indian Exporters</div>
              <div className="text-2xl font-bold mt-1">{metricsData.total_exporters?.toLocaleString()}</div>
              <div className="text-xs text-emerald-600 mt-1 font-medium">IEC & Star Certified</div>
            </div>
            <div className="p-4 rounded-xl border bg-card shadow-sm">
              <div className="text-xs text-muted-foreground uppercase font-semibold">US Corporate Buyers</div>
              <div className="text-2xl font-bold mt-1">{metricsData.total_importers}</div>
              <div className="text-xs text-blue-600 mt-1 font-medium">Direct Emails & Contacts</div>
            </div>
            <div className="p-4 rounded-xl border bg-card shadow-sm">
              <div className="text-xs text-muted-foreground uppercase font-semibold">Active Products Catalog</div>
              <div className="text-2xl font-bold mt-1">{metricsData.total_products?.toLocaleString()}</div>
              <div className="text-xs text-purple-600 mt-1 font-medium">48 Major Categories</div>
            </div>
            <div className="p-4 rounded-xl border bg-card shadow-sm">
              <div className="text-xs text-muted-foreground uppercase font-semibold">HSN Harmonized Codes</div>
              <div className="text-2xl font-bold mt-1">{metricsData.total_hsn_codes?.toLocaleString()}</div>
              <div className="text-xs text-amber-600 mt-1 font-medium">Tariff Classified</div>
            </div>
          </div>

          {/* Tabs */}
          <div className="flex border-b mb-6">
            <button
              onClick={() => setActiveTab("importers")}
              className={`pb-3 px-4 text-sm font-semibold border-b-2 transition-colors ${
                activeTab === "importers"
                  ? "border-black text-black"
                  : "border-transparent text-muted-foreground hover:text-black"
              }`}
            >
              US Corporate Importers ({filteredImporters.length})
            </button>
            <button
              onClick={() => setActiveTab("exporters")}
              className={`pb-3 px-4 text-sm font-semibold border-b-2 transition-colors ${
                activeTab === "exporters"
                  ? "border-black text-black"
                  : "border-transparent text-muted-foreground hover:text-black"
              }`}
            >
              Indian Verified Exporters ({filteredExporters.length})
            </button>
            <button
              onClick={() => setActiveTab("calculator")}
              className={`pb-3 px-4 text-sm font-semibold border-b-2 transition-colors flex items-center gap-1.5 ${
                activeTab === "calculator"
                  ? "border-black text-black"
                  : "border-transparent text-muted-foreground hover:text-black"
              }`}
            >
              <Calculator className="w-4 h-4" />
              Landed Cost & Arbitrage Calculator
            </button>
          </div>

          {/* Search bar */}
          {activeTab !== "calculator" && (
            <div className="relative mb-6">
              <Search className="absolute left-3.5 top-3 text-muted-foreground w-4 h-4" />
              <input
                type="text"
                placeholder="Search by company, product category, city, or state..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 rounded-lg border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-black/10"
              />
            </div>
          )}

          {/* Tab Content: US Importers */}
          {activeTab === "importers" && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filteredImporters.slice(0, 30).map((buyer: any, idx: number) => (
                <div key={idx} className="p-5 rounded-xl border bg-card hover:shadow-md transition-shadow flex flex-col justify-between">
                  <div>
                    <div className="flex items-start justify-between gap-2">
                      <h3 className="font-bold text-base">{buyer.company_name}</h3>
                      <span className="text-xs px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 font-medium whitespace-nowrap">
                        {buyer.industry_category || "Wholesale / Retail"}
                      </span>
                    </div>
                    <div className="text-xs text-muted-foreground mt-1">
                      {buyer.city}, {buyer.state_name}
                    </div>
                    {buyer.website_title && (
                      <p className="text-xs text-foreground/80 mt-2 line-clamp-2">
                        {buyer.website_title}
                      </p>
                    )}
                  </div>

                  <div className="mt-4 pt-3 border-t flex flex-wrap items-center justify-between gap-2 text-xs">
                    <div className="flex items-center gap-3 text-muted-foreground">
                      {buyer.website && (
                        <a href={buyer.website.startsWith("http") ? buyer.website : `https://${buyer.website}`} target="_blank" rel="noreferrer" className="hover:text-black flex items-center gap-1">
                          <Globe className="w-3.5 h-3.5" /> Website
                        </a>
                      )}
                      {buyer.scraped_emails && (
                        <span className="flex items-center gap-1 text-emerald-700 font-medium">
                          <Mail className="w-3.5 h-3.5" /> {buyer.scraped_emails.split(",")[0]}
                        </span>
                      )}
                    </div>
                    <span className="text-[11px] text-muted-foreground">ID: {buyer.buyer_id}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Tab Content: Indian Exporters */}
          {activeTab === "exporters" && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filteredExporters.slice(0, 30).map((exp: any, idx: number) => (
                <div key={idx} className="p-5 rounded-xl border bg-card hover:shadow-md transition-shadow flex flex-col justify-between">
                  <div>
                    <div className="flex items-start justify-between gap-2">
                      <h3 className="font-bold text-base">{exp.company_name}</h3>
                      <span className="text-xs px-2.5 py-1 rounded-full bg-amber-50 text-amber-800 font-medium whitespace-nowrap">
                        IEC: {exp.iec_code || "Verified"}
                      </span>
                    </div>
                    <div className="text-xs text-muted-foreground mt-1">
                      {exp.city}, {exp.state_name}
                    </div>
                    <div className="text-xs text-foreground/80 mt-2 line-clamp-2 font-medium">
                      Deals in: {exp.deal_in || "Precision Manufacturing & Export"}
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t flex items-center justify-between text-xs text-muted-foreground">
                    <span>Products: {exp.total_products || 1}</span>
                    <span className="text-emerald-700 font-medium">Star Exporter Accredited</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Tab Content: Arbitrage Calculator */}
          {activeTab === "calculator" && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 p-6 rounded-2xl border bg-card">
              <div className="space-y-4 lg:col-span-2">
                <H2>Finished Goods Landed Cost & Margin Simulator</H2>
                <P>
                  Calculate exact FOB to CIF costs, US customs duty, harbor processing, and profit spreads for direct factory-to-store distribution.
                </P>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                  <div>
                    <label className="text-xs font-semibold text-muted-foreground uppercase">Unit FOB Factory Cost (USD)</label>
                    <input
                      type="number"
                      value={fobPrice}
                      onChange={(e) => setFobPrice(Number(e.target.value))}
                      className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-muted-foreground uppercase">Target US Retail / Wholesale Price (USD)</label>
                    <input
                      type="number"
                      value={retailPrice}
                      onChange={(e) => setRetailPrice(Number(e.target.value))}
                      className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-muted-foreground uppercase">Product Gross Weight (kg)</label>
                    <input
                      type="number"
                      step="0.05"
                      value={weightKg}
                      onChange={(e) => setWeightKg(Number(e.target.value))}
                      className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-muted-foreground uppercase">Shipping Mode</label>
                    <select
                      value={mode}
                      onChange={(e: any) => setMode(e.target.value)}
                      className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                    >
                      <option value="air">Express Air Cargo ($8.50/kg)</option>
                      <option value="sea">Ocean Freight LCL/FCL ($0.45/kg)</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Result Summary Card */}
              <div className="p-6 rounded-xl bg-muted/40 border flex flex-col justify-between">
                <div>
                  <div className="text-xs font-semibold text-muted-foreground uppercase">Financial Breakdown</div>
                  <div className="space-y-2 mt-4 text-xs">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">FOB Factory Price:</span>
                      <span className="font-medium">${fobPrice.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Est. Freight ({mode.toUpperCase()}):</span>
                      <span className="font-medium">${freightCost.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Marine Insurance (0.35%):</span>
                      <span className="font-medium">${insurance.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between font-semibold border-t pt-2">
                      <span>CIF Destination Value:</span>
                      <span>${cif.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">US Customs Tariff (5.5%):</span>
                      <span className="font-medium">${duty.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Merchandise Processing Fee:</span>
                      <span className="font-medium">${mpf.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between font-bold text-sm border-t pt-2">
                      <span>Total Landed Cost:</span>
                      <span className="text-blue-700">${totalLanded.toFixed(2)}</span>
                    </div>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t">
                  <div className="text-xs text-muted-foreground uppercase font-semibold">Net Arbitrage Spread</div>
                  <div className="text-3xl font-extrabold text-emerald-600 mt-1">
                    ${marginUsd.toFixed(2)}
                  </div>
                  <div className="text-xs font-bold text-emerald-700 mt-0.5">
                    {marginPct}% Gross Margin
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
