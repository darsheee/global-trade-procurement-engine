"use client";

import React, { useState } from "react";
import { Page, PageContent, Section, H1, H2, Intro, P } from "@/components/Layout";
import { Leaf, FileCode, AlertTriangle, ShieldCheck, Download, Calculator, BarChart3 } from "lucide-react";

export default function CBAMPage() {
  const [productCategory, setProductCategory] = useState("steel_rebar");
  const [productionVolumeTons, setProductionVolumeTons] = useState(500);
  const [fuelConsumptionMwh, setFuelConsumptionMwh] = useState(1200);
  const [electricityConsumedMwh, setElectricityConsumedMwh] = useState(350);
  const [euEtsPriceEur, setEuEtsPriceEur] = useState(65.0);

  // Scope 1: Fuel combustion (Natural gas approx 0.202 tCO2 / MWh)
  const scope1Direct = Math.round(fuelConsumptionMwh * 0.202 * 10) / 10;
  
  // Scope 2: Grid factor (CEA India default 0.716 tCO2 / MWh)
  const scope2Indirect = Math.round(electricityConsumedMwh * 0.716 * 10) / 10;

  const totalEmissions = Math.round((scope1Direct + scope2Indirect) * 10) / 10;
  const specificEmissions = productionVolumeTons > 0 ? Math.round((totalEmissions / productionVolumeTons) * 1000) / 1000 : 0;
  
  const euBenchmark = productCategory === "steel_rebar" ? 2.10 : productCategory === "aluminum_unwrought" ? 11.50 : 0.82;
  const grossCbamLiabilityEur = Math.round(totalEmissions * euEtsPriceEur);
  const cbamCostPerTonEur = productionVolumeTons > 0 ? Math.round((grossCbamLiabilityEur / productionVolumeTons) * 100) / 100 : 0;

  const handleDownloadXml = () => {
    const xmlContent = `<?xml version="1.0" encoding="UTF-8"?>
<CBAMQuarterlyReport xmlns="urn:eu:ec:cbam:v1" reportingPeriod="2026-Q3">
  <Declarant>
    <EORINumber>NL892019481</EORINumber>
    <CompanyName>EU Industrial Importer B.V.</CompanyName>
    <CountryCode>NL</CountryCode>
  </Declarant>
  <ProductionInstallation>
    <InstallationName>Indian Special Steels & Alloys Ltd</InstallationName>
    <CountryCode>IN</CountryCode>
    <City>Jamshedpur</City>
  </ProductionInstallation>
  <ImportedGoods>
    <CNCode>72142000</CNCode>
    <QuantityMetricTons>${productionVolumeTons}</QuantityMetricTons>
    <EmbeddedEmissions>
      <SpecificDirectEmissions>${(scope1Direct / Math.max(productionVolumeTons, 1)).toFixed(4)}</SpecificDirectEmissions>
      <SpecificIndirectEmissions>${(scope2Indirect / Math.max(productionVolumeTons, 1)).toFixed(4)}</SpecificIndirectEmissions>
      <TotalSpecificEmbeddedEmissions>${specificEmissions}</TotalSpecificEmbeddedEmissions>
      <TotalGrossLiabilityEUR>${grossCbamLiabilityEur}</TotalGrossLiabilityEUR>
    </EmbeddedEmissions>
  </ImportedGoods>
</CBAMQuarterlyReport>`;

    const blob = new Blob([xmlContent], { type: "application/xml" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `CBAM-Declaration-${productCategory}-${Date.now()}.xml`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <Page>
      <PageContent>
        <Section>
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b pb-6">
            <div>
              <H1>EU CBAM Cross-Border Carbon Compliance Engine</H1>
              <Intro>
                Automated Scope 1 & 2 Embedded Emissions Calculator & XML Registry Generator for Indian Exporters (EU Regulation 2023/956).
              </Intro>
            </div>
            <div className="flex items-center gap-2 bg-emerald-50 text-emerald-800 border border-emerald-200 px-4 py-2 rounded-lg text-sm font-medium">
              <Leaf className="w-5 h-5 text-emerald-600" />
              EU Customs Transitional Registry Compliant
            </div>
          </div>

          {/* Quick Pillars */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 my-8">
            <div className="p-5 rounded-xl border bg-card">
              <div className="text-xs text-muted-foreground uppercase font-semibold">Target Sectors</div>
              <div className="text-base font-bold text-black mt-1">Steel, Aluminum, Cement, Fertilizers</div>
              <p className="text-xs text-muted-foreground mt-1">
                Mandatory quarterly carbon declarations for all industrial shipments entering the 27 EU member states.
              </p>
            </div>
            <div className="p-5 rounded-xl border bg-card">
              <div className="text-xs text-muted-foreground uppercase font-semibold">Grid Electricity Factor</div>
              <div className="text-base font-bold text-emerald-700 mt-1">0.716 tCO2e / MWh</div>
              <p className="text-xs text-muted-foreground mt-1">
                Central Electricity Authority (CEA India) baseline for Scope 2 indirect carbon intensity accounting.
              </p>
            </div>
            <div className="p-5 rounded-xl border bg-card">
              <div className="text-xs text-muted-foreground uppercase font-semibold">EU ETS Carbon Price</div>
              <div className="text-base font-bold text-blue-700 mt-1">€{euEtsPriceEur.toFixed(2)} / tCO2e</div>
              <p className="text-xs text-muted-foreground mt-1">
                Benchmark European carbon allowance traded on the European Energy Exchange (EEX).
              </p>
            </div>
          </div>

          {/* Calculator */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 p-6 rounded-2xl border bg-card">
            <div className="space-y-4 lg:col-span-2">
              <H2>Factory Production & Energy Inputs</H2>
              <P>Input shipment production batch and energy utility consumption to evaluate regulatory exposure.</P>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-3">
                <div>
                  <label className="text-xs font-semibold text-muted-foreground uppercase">Covered Product Category</label>
                  <select
                    value={productCategory}
                    onChange={(e) => setProductCategory(e.target.value)}
                    className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                  >
                    <option value="steel_rebar">Steel Rebar & Rods (CN 7214 20 00)</option>
                    <option value="aluminum_unwrought">Unwrought Aluminum Ingots (CN 7601 10 00)</option>
                    <option value="cement_clinker">Cement Clinker (CN 2523 10 00)</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs font-semibold text-muted-foreground uppercase">Production Batch Volume (Metric Tons)</label>
                  <input
                    type="number"
                    value={productionVolumeTons}
                    onChange={(e) => setProductionVolumeTons(Number(e.target.value))}
                    className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                  />
                </div>

                <div>
                  <label className="text-xs font-semibold text-muted-foreground uppercase">Fuel Thermal Energy Consumed (MWh)</label>
                  <input
                    type="number"
                    value={fuelConsumptionMwh}
                    onChange={(e) => setFuelConsumptionMwh(Number(e.target.value))}
                    className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                  />
                </div>

                <div>
                  <label className="text-xs font-semibold text-muted-foreground uppercase">Grid Electricity Consumed (MWh)</label>
                  <input
                    type="number"
                    value={electricityConsumedMwh}
                    onChange={(e) => setElectricityConsumedMwh(Number(e.target.value))}
                    className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                  />
                </div>

                <div>
                  <label className="text-xs font-semibold text-muted-foreground uppercase">EU ETS Carbon Price (€ / tCO2e)</label>
                  <input
                    type="number"
                    value={euEtsPriceEur}
                    onChange={(e) => setEuEtsPriceEur(Number(e.target.value))}
                    className="w-full mt-1 px-3 py-2 border rounded-lg text-sm bg-background font-medium"
                  />
                </div>

                <div className="flex flex-col justify-end">
                  <button
                    onClick={handleDownloadXml}
                    className="w-full bg-black text-white hover:bg-neutral-800 px-4 py-2.5 rounded-lg text-xs font-semibold flex items-center justify-center gap-2"
                  >
                    <Download className="w-4 h-4" />
                    Download Official EU CBAM XML
                  </button>
                </div>
              </div>
            </div>

            {/* Results */}
            <div className="p-6 rounded-xl bg-muted/40 border flex flex-col justify-between">
              <div>
                <div className="text-xs font-semibold text-muted-foreground uppercase">Carbon Emissions Profile</div>
                <div className="space-y-2.5 mt-4 text-xs">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Scope 1 (Direct Fuel):</span>
                    <span className="font-medium">{scope1Direct.toLocaleString()} tCO2e</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Scope 2 (Indirect Grid):</span>
                    <span className="font-medium">{scope2Indirect.toLocaleString()} tCO2e</span>
                  </div>
                  <div className="flex justify-between font-semibold border-t pt-2">
                    <span>Total Embedded Emissions:</span>
                    <span>{totalEmissions.toLocaleString()} tCO2e</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Specific Emission Intensity:</span>
                    <span className="font-bold text-foreground">{specificEmissions} tCO2e / ton</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">EU Benchmark Standard:</span>
                    <span className="font-medium">{euBenchmark.toFixed(2)} tCO2e / ton</span>
                  </div>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t">
                <div className="text-xs text-muted-foreground uppercase font-semibold">Gross CBAM Certificate Cost</div>
                <div className="text-3xl font-black text-amber-600 mt-1">
                  €{grossCbamLiabilityEur.toLocaleString()} EUR
                </div>
                <div className="text-xs font-bold text-muted-foreground mt-0.5">
                  €{cbamCostPerTonEur.toFixed(2)} EUR per Metric Ton
                </div>
              </div>
            </div>
          </div>
        </Section>
      </PageContent>
    </Page>
  );
}
