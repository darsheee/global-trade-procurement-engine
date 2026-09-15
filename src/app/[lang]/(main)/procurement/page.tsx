"use client";

import React, { useState } from "react";
import { Page, PageContent, Section, H1, H2, Intro, P } from "@/components/Layout";
import { Search, Globe, FileText, CheckCircle2, ShieldAlert, ArrowUpRight, Award, DollarSign } from "lucide-react";

const TENDERS = [
  {
    id: "CAN-PSPC-2026-8941",
    country: "Canada",
    authority: "Public Services and Procurement Canada (PSPC)",
    title: "Supply and Delivery of Precision Optical Equipment & Industrial Inspection Sensors",
    category: "Optical & Precision Instruments",
    hsnCode: "9031.80",
    estimatedValueUsd: 420000,
    closingDate: "2026-10-30",
    status: "OPEN",
    specs: "High-resolution laser inspection equipment and COTS precision optical components for federal testing labs.",
    matchScore: 94
  },
  {
    id: "USA-DLA-2026-0412",
    country: "United States",
    authority: "Defense Logistics Agency (DLA Troop Support)",
    title: "Specialty Fasteners, Machine Mounts and Precision Castings",
    category: "Defense & Industrial Hardware",
    hsnCode: "7318.15",
    estimatedValueUsd: 1250000,
    closingDate: "2026-11-15",
    status: "OPEN",
    specs: "Standard titanium and nickel alloy hardware fasteners meeting MIL-SPEC tolerances for logistic supply.",
    matchScore: 91
  },
  {
    id: "IND-IDEX-DISC-14-CH08",
    country: "India",
    authority: "Innovations for Defence Excellence (iDEX) / MoD",
    title: "Acoustic Counter-UAS Detection Array & Edge-AI Terminal Homing Kit",
    category: "Defense AI & Electronics",
    hsnCode: "8526.91",
    estimatedValueUsd: 180000,
    closingDate: "2026-11-05",
    status: "OPEN",
    specs: "Design and prototyping of an ultra-low-power acoustic sensor cluster detecting micro-drones at >300m range.",
    matchScore: 98
  },
  {
    id: "CAN-NRCan-2026-3390",
    country: "Canada",
    authority: "Natural Resources Canada (NRCan)",
    title: "Carbon Accounting and Cross-Border Supply Chain Verification Services",
    category: "Environmental & Carbon Services",
    hsnCode: "9983.13",
    estimatedValueUsd: 310000,
    closingDate: "2026-10-18",
    status: "OPEN",
    specs: "Third-party MRV methodology verification for industrial cross-border carbon border adjustment data.",
    matchScore: 89
  }
];

export default function ProcurementPage() {
  const [selectedCountry, setSelectedCountry] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState<string>("");

  const filteredTenders = TENDERS.filter((t) => {
    const matchesCountry = selectedCountry === "ALL" || t.country.toUpperCase() === selectedCountry;
    const matchesQuery = !searchQuery || 
      t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.authority.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCountry && matchesQuery;
  });

  return (
    <Page>
      <PageContent>
        <Section>
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b pb-6">
            <div>
              <H1>Global Public Procurement & Tender Radar</H1>
              <Intro>
                Real-time contract opportunities across Canadian Federal Procurement, US Defense Logistics Agency (DLA/SAM.gov), and India Defense iDEX/GeM.
              </Intro>
            </div>
            <div className="flex items-center gap-2 bg-blue-50 text-blue-800 border border-blue-200 px-4 py-2 rounded-lg text-sm font-medium">
              <Award className="w-5 h-5 text-blue-600" />
              Direct Tender Sourcing Brokerage
            </div>
          </div>

          {/* Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 my-8">
            <div className="p-4 rounded-xl border bg-card shadow-sm">
              <div className="text-xs text-muted-foreground uppercase font-semibold">Total Pipeline Value</div>
              <div className="text-2xl font-bold mt-1">$2,160,000</div>
              <div className="text-xs text-emerald-600 mt-1 font-medium">High-probability RFQs</div>
            </div>
            <div className="p-4 rounded-xl border bg-card shadow-sm">
              <div className="text-xs text-muted-foreground uppercase font-semibold">Tracked Jurisdictions</div>
              <div className="text-2xl font-bold mt-1">3 Sovereign Entities</div>
              <div className="text-xs text-blue-600 mt-1 font-medium">Canada, USA, India</div>
            </div>
            <div className="p-4 rounded-xl border bg-card shadow-sm">
              <div className="text-xs text-muted-foreground uppercase font-semibold">Qualified Factory Matches</div>
              <div className="text-2xl font-bold mt-1">14 Certified Plants</div>
              <div className="text-xs text-purple-600 mt-1 font-medium">In trade database</div>
            </div>
            <div className="p-4 rounded-xl border bg-card shadow-sm">
              <div className="text-xs text-muted-foreground uppercase font-semibold">iDEX Defense Grants</div>
              <div className="text-2xl font-bold mt-1">₹1.5–10 Crores</div>
              <div className="text-xs text-amber-600 mt-1 font-medium">100% Non-Dilutive</div>
            </div>
          </div>

          {/* Country Filter buttons & Search */}
          <div className="flex flex-col sm:flex-row gap-3 items-center justify-between mb-6">
            <div className="flex items-center gap-2 w-full sm:w-auto">
              {["ALL", "CANADA", "UNITED STATES", "INDIA"].map((c) => (
                <button
                  key={c}
                  onClick={() => setSelectedCountry(c)}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                    selectedCountry === c
                      ? "bg-black text-white"
                      : "bg-muted text-muted-foreground hover:bg-muted/80 hover:text-black"
                  }`}
                >
                  {c}
                </button>
              ))}
            </div>

            <div className="relative w-full sm:w-72">
              <Search className="absolute left-3 top-2.5 text-muted-foreground w-4 h-4" />
              <input
                type="text"
                placeholder="Filter tenders..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-3 py-1.5 rounded-lg border bg-background text-xs focus:outline-none focus:ring-1 focus:ring-black"
              />
            </div>
          </div>

          {/* Tenders list */}
          <div className="space-y-4">
            {filteredTenders.map((tender) => (
              <div
                key={tender.id}
                className="p-6 rounded-2xl border bg-card hover:shadow-md transition-shadow flex flex-col md:flex-row md:items-center justify-between gap-6"
              >
                <div className="space-y-2 max-w-2xl">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-800 border">
                      {tender.country}
                    </span>
                    <span className="text-xs font-medium text-muted-foreground">
                      {tender.authority}
                    </span>
                    <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">
                      {tender.status}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold leading-snug">{tender.title}</h3>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    {tender.specs}
                  </p>

                  <div className="flex flex-wrap items-center gap-4 text-xs text-muted-foreground pt-1">
                    <span>HSN / Tariff: <strong className="text-foreground">{tender.hsnCode}</strong></span>
                    <span>Deadline: <strong className="text-foreground">{tender.closingDate}</strong></span>
                    <span>ID: <code className="text-[11px]">{tender.id}</code></span>
                  </div>
                </div>

                <div className="flex flex-col md:items-end justify-between border-t md:border-t-0 pt-4 md:pt-0 gap-3 min-w-[200px]">
                  <div className="text-right">
                    <div className="text-xs text-muted-foreground font-semibold uppercase">Estimated Contract Value</div>
                    <div className="text-2xl font-black text-black">
                      ${tender.estimatedValueUsd.toLocaleString()} USD
                    </div>
                  </div>

                  <div className="flex items-center gap-2 w-full md:w-auto">
                    <div className="text-right hidden md:block">
                      <div className="text-[11px] text-muted-foreground">Database Factory Fit</div>
                      <div className="text-xs font-bold text-emerald-700">{tender.matchScore}% Match Score</div>
                    </div>
                    <a
                      href={`/${tender.id}`}
                      className="w-full md:w-auto bg-black text-white hover:bg-neutral-800 px-4 py-2 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5"
                    >
                      <FileText className="w-3.5 h-3.5" />
                      Auto-Draft Bid RFQ
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Section>
      </PageContent>
    </Page>
  );
}
