# Playbook 04: Public Procurement & Tender Brokerage Architecture

## 1. What is Public Procurement Brokering?
Governments around the world (Canada, United States, India) spend trillions of dollars purchasing everyday commercial goods:
- Canada: Federal public accounts, PSPC proactive disclosures, and CanadaBuys contracts ($30B+ annually).
- United States: DLA, GSA Advantage, SAM.gov, and USASpending ($600B+ federal discretionary spend).
- India: Government e-Marketplace (GeM) with mandatory 25% MSME procurement quotas and 4% SC/ST enterprise reservations.

Small domestic government suppliers frequently win contracts but lack low-cost manufacturing capacity. By matching public contract requirements with certified Indian factories, you can act as a **Back-to-Back Sourcing Broker**:
- Secure the tender or partner with an existing registered prime contractor.
- Source the product at 40% lower FOB price from an Indian factory in our database.
- Capture the arbitrage spread upon milestone inspection and government disbursement.

---

## 2. The 3-Step Execution Pipeline
1. **Radar Ingestion**: Run `agents/tender_scout_agent.py` to identify active tenders under $500,000 with clear commercial specifications (hardware, apparel, tools, optical gear, eco-packaging).
2. **Instant Supplier Shortlist**: Run `trade_engine/matchmaker.py` to pull top Indian factories with IEC and star-export ratings.
3. **Automated Bid Drafting**: Run `agents/rfq_proposal_agent.py` to output technical compliance matrices and commercial quotation letters ready for submission.
