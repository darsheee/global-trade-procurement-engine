# Global Trade, Procurement Intelligence & Export Startup Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Next.js 15](https://img.shields.io/badge/Next.js-15.4-black)](https://nextjs.org/)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-brightgreen.svg)](https://python.org)
[![Upstream: BuildCanada/CanadaSpends](https://img.shields.io/badge/Upstream-BuildCanada%2FCanadaSpends-red)](https://github.com/BuildCanada/CanadaSpends)

An **All-In-One Intelligence & Execution Engine** combining the civic spending transparency architecture of **BuildCanada's CanadaSpends** with global bilateral trade data, multi-country public procurement tracking, finished diamond/jewelry arbitrage, EU CBAM carbon compliance, and autonomous AI agents for export brokerage.

---

## Strategic Pillars & Modules

```
                        GLOBAL TRADE & PROCUREMENT ENGINE
                                        │
    ┌───────────────────┬───────────────┴───────────────┬───────────────────┐
    ▼                   ▼                               ▼                   ▼
[ Procurement Radar ] [ Bilateral Trade Match ]     [ Finished Jewelry ]  [ Carbon Compliance ]
• Canada PSPC / Buys • 2,382 Indian Exporters       • 10K/14K Gold BOM    • EU CBAM (2023/956)
• US DLA / SAM.gov  • 190 US Corporate Buyers       • Surat LGD vs Retail • Scope 1 & Scope 2
• India GeM / iDEX  • 4,123 Products & HSNs         • Delaware LLC + LLP  • XML Registry Gen
```

### 1. Multi-Jurisdiction Public Procurement Radar (`/procurement`)
- **Canada Federal & Provincial**: Track public accounts, grants, contracts, and proactive disclosures across Canadian federal agencies and crown corporations.
- **United States Federal Procurement**: Ingest opportunities from Defense Logistics Agency (DLA) and SAM.gov with Buy American / TAA waiver tracking.
- **India Public Procurement & Defense (GeM / iDEX)**: Monitor Government e-Marketplace tenders (including mandatory 25% MSME quotas and 4% SC/ST reservations) and Ministry of Defence iDEX DISC challenges offering ₹1.5 Cr to ₹10 Cr non-dilutive startup grants.

### 2. Bilateral Trade & Supplier Matchmaker (`/trade`)
- Grounded in an audited SQLite master database (`trade_engine/db/india_usa_trade.db`):
  - **2,382 Indian Exporters**: Filterable by IEC accreditation, star-export rating, and manufacturing hubs (Mumbai, Surat, Delhi NCR, Bangalore).
  - **190 US Corporate Importers**: Full web-crawled profiles with direct executive emails, phone numbers, corporate addresses, and product line matches.
  - **4,123 Products & 14,566 HSN Codes**: Complete tariff schedule classification with automated FOB-to-CIF landed-cost modeling.

### 3. Finished Diamond & Jewelry Arbitrage Pipeline (`/jewelry`)
- **Labor Arbitrage**: Capitalizes on $2.50/g Indian precision casting vs. $18/g US domestic casting costs.
- **Lab-Grown Diamond (LGD) Spread**: Sourcing CVD/HPHT certified stones from Surat at ~$95/ct to supply US retail chains where finished pieces retail at 55%+ gross margins.
- **Corporate Tax Architecture**:
  - Invoices routed in USD to a **US Delaware/Wyoming LLC** (disregarded single-member entity).
  - Back-to-back export settlements to an **Indian LLP** where partner profit distributions are **100% tax-exempt under Section 10(2A)** of the Indian Income Tax Act.
- **Risk Mitigation**: Euler Hermes / Allianz Trade credit insurance guaranteeing 90% payout on Net-30 / Net-60 buyer terms.

### 4. Cross-Border Carbon Compliance Engine (`/cbam`)
- Implements European Union Regulation (EU) 2023/956 (Carbon Border Adjustment Mechanism):
  - Automated calculation of Scope 1 direct emissions (fuel combustion) and Scope 2 indirect emissions using India's Central Electricity Authority (CEA) benchmark (0.716 tCO2e/MWh).
  - Specific Embedded Emissions (SEE) benchmarks for steel, aluminum, cement, and fertilizers.
  - 1-click generation of the official EU CBAM Transitional Registry XML declaration.

### 5. Autonomous AI Multi-Agent Trade & Tender Hunters (`agents/`)
- `tender_scout_agent.py`: Continuously monitors public procurement feeds, extracts technical requirements, and tags matching HSN codes.
- `supplier_match_agent.py`: Cross-matches tender specifications with verified suppliers in the master database.
- `rfq_proposal_agent.py`: Auto-generates formal commercial quotation letters, Incoterms FOB/CIF pricing sheets, and technical compliance matrices.
- `buyer_outreach_agent.py`: Generates hyper-personalized cold outreach emails and LinkedIn sequences for the 190 crawled US corporate buyers.

---

## Directory Architecture

```
├── agents/                           # Autonomous AI multi-agent broker scripts
│   ├── tender_scout_agent.py         # Multi-country tender parser
│   ├── supplier_match_agent.py       # Supplier scoring & recommendation
│   ├── rfq_proposal_agent.py         # Commercial export quotation generator
│   └── buyer_outreach_agent.py       # Personalized B2B email sequence generator
│
├── compliance/                       # Regulatory & compliance engines
│   ├── cbam/                         # EU CBAM Scope 1/2 calculator & XML generator
│   └── diamond_origin/               # G7 Kimberley Process & sanctions provenance tracker
│
├── playbooks/                        # Operational blueprints & startup execution manuals
│   ├── 01_finished_jewelry_export_playbook.md
│   ├── 02_eu_cbam_compliance_consultancy.md
│   ├── 03_defense_idex_startup_playbook.md
│   └── 04_public_procurement_brokerage.md
│
├── trade_engine/                     # Core bilateral trade datasets & Python engine
│   ├── db/india_usa_trade.db         # SQLite master database (12MB)
│   ├── data/                         # Clean CSV and indexed JSON datasets
│   ├── matchmaker.py                 # Supplier-buyer matching & margin calculator
│   └── India_USA_Trade_Facilitation_Master.xlsx
│
└── src/                              # Next.js 15 Web Application (TypeScript, Tailwind v4)
    ├── app/
    │   ├── [lang]/(main)/trade/      # Bilateral Trade & Supplier Radar view
    │   ├── [lang]/(main)/procurement/# Multi-Country Public Procurement Radar view
    │   ├── [lang]/(main)/jewelry/    # Finished Jewelry Arbitrage Simulator view
    │   ├── [lang]/(main)/cbam/       # EU CBAM Carbon Compliance view
    │   ├── [lang]/(main)/spending/   # Canada Federal Spending view (CanadaSpends)
    │   └── api/                      # REST APIs (/api/trade, /api/cbam, /api/procurement)
    └── components/                   # UI design system, Recharts & D3 data visualizers
```

---

## Quick Start Guide

### 1. Web Application (Next.js)

```bash
# Clone the repository
git clone https://github.com/darsheee/global-trade-procurement-engine.git
cd global-trade-procurement-engine

# Install dependencies (requires Node.js 20+)
corepack enable
pnpm install

# Run the development server
pnpm dev
```

Visit `http://localhost:3000/en/trade` to explore the Trade Radar, or `http://localhost:3000/en/procurement` for live tenders.

### 2. Python Trade Engine & AI Agents

```bash
# Run the Trade Matchmaker
python3 trade_engine/matchmaker.py

# Run the EU CBAM Carbon Compliance Engine
python3 compliance/cbam/calculator.py

# Run the Autonomous Tender Scout
python3 agents/tender_scout_agent.py

# Generate B2B Outreach Pitches for US Importers
python3 agents/buyer_outreach_agent.py
```

---

## Upstream Synchronization

To pull latest updates from the upstream BuildCanada repository:

```bash
git fetch upstream
git merge upstream/main
```

---

## License

This project is licensed under the MIT License, preserving upstream civic open-source terms.
