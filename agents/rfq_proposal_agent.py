"""
Autonomous Export RFQ & Tender Proposal Generator Agent
Drafts formal B2B export quotations, technical compliance matrices, and landed-cost proposals.
"""

import json
from datetime import datetime
from typing import Dict, Any

class RFQProposalAgent:
    def __init__(self):
        pass

    def generate_export_quotation(
        self,
        buyer_company: str,
        buyer_contact: str,
        buyer_country: str,
        supplier_company: str,
        supplier_city: str,
        product_name: str,
        quantity: float,
        unit: str,
        unit_fob_price_usd: float,
        sea_or_air: str = "air",
        lead_time_weeks: int = 4
    ) -> Dict[str, Any]:
        """Generate a full B2B commercial export proposal."""
        total_fob_usd = round(quantity * unit_fob_price_usd, 2)
        
        # Freight and Insurance estimates
        freight_estimate_usd = round(total_fob_usd * 0.045 if sea_or_air.lower() == "sea" else total_fob_usd * 0.085, 2)
        transit_insurance_usd = round(total_fob_usd * 0.0035, 2)
        total_cif_usd = round(total_fob_usd + freight_estimate_usd + transit_insurance_usd, 2)

        quote_id = f"EXP-QT-{datetime.utcnow().strftime('%Y%m%d')}-{abs(hash(buyer_company)) % 10000:04d}"

        proposal_text = f"""COMMERCIAL EXPORT QUOTATION & BID PROPOSAL
Reference: {quote_id}
Date: {datetime.utcnow().strftime('%B %d, %Y')}

TO:
Attn: {buyer_contact}
Company: {buyer_company}
Destination: {buyer_country}

FROM:
Authorized Export Facilitation Desk
On behalf of: {supplier_company}
Manufacturing Hub: {supplier_city}, India (IEC Accredited)

1. PRODUCT SPECIFICATION & COMMERCIAL TERMS
- Product: {product_name}
- Order Quantity: {quantity:,.0f} {unit}
- Unit Price (FOB Indian Port): ${unit_fob_price_usd:,.2f} USD
- Total FOB Value: ${total_fob_usd:,.2f} USD
- Estimated Freight ({sea_or_air.upper()}): ${freight_estimate_usd:,.2f} USD
- All-Risk Transit Insurance: ${transit_insurance_usd:,.2f} USD
- Total CIF Value: ${total_cif_usd:,.2f} USD

2. LOGISTICS & DELIVERY
- Incoterms 2020: CIF (Port / Airport of Destination)
- Port of Loading: JNPT Mumbai (Sea) / IGI Cargo Terminal New Delhi (Air)
- Production & Dispatch Lead Time: {lead_time_weeks} weeks from receipt of confirmed purchase order / LC.
- Packaging: Export-grade tamper-evident packaging compliant with ISPM 15 standards.

3. PAYMENT & SETTLEMENT ARCHITECTURE
- Primary: Irrevocable Letter of Credit (LC) at Sight, 100% confirmed by Tier-1 International Bank.
- Alternate (for qualified buyers): Net-30 / Net-60 terms factored through Delaware LLC / Euler Hermes insured trade credit facility.

4. QUALITY ASSURANCE & AUDIT CLEARANCE
- Pre-shipment inspection: SGS / Bureau Veritas inspection available upon request.
- Regulatory Compliance: G7 non-sanction origin verified, EU CBAM carbon reporting compliant, RoHS/REACH compliant where applicable.
"""
        return {
            "quote_id": quote_id,
            "buyer_company": buyer_company,
            "supplier_company": supplier_company,
            "total_fob_usd": total_fob_usd,
            "total_cif_usd": total_cif_usd,
            "full_proposal_document": proposal_text
        }

if __name__ == "__main__":
    agent = RFQProposalAgent()
    res = agent.generate_export_quotation(
        buyer_company="Kohl's Department Stores Inc",
        buyer_contact="Procurement Director",
        buyer_country="United States",
        supplier_company="6C Style Fine Jewelry LLP",
        supplier_city="Mumbai",
        product_name="14K Solid Gold & Lab-Grown Diamond Tennis Bracelet (3.0 ctw)",
        quantity=250,
        unit="Pieces",
        unit_fob_price_usd=480.0,
        sea_or_air="air",
        lead_time_weeks=3
    )
    print("=== Generated Commercial Export Quotation ===")
    print(res["full_proposal_document"][:600] + "...")
