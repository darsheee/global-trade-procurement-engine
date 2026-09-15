# Playbook 01: Finished Diamond & Lab-Grown Jewelry Export Engine

## 1. The Core Economic Arbitrage
Selling loose diamonds (rough or polished) is a zero-sum, commoditized race to the bottom where profit margins hover between 1.5% and 3.5%. The true, defensible cash-flow engine lies in **Finished Jewelry Export** (rings, tennis bracelets, pendants, earrings in 10K/14K solid gold and 925 sterling silver):
- **Casting Labor Arbitrage**: US domestic jewelry casting costs $15–$25 per gram. Indian high-precision casting hubs (SEEPZ Mumbai, Surat, Jaipur) operate at $1.80–$3.20 per gram.
- **Finished Unit Markups**: A 3.0 ctw tennis bracelet manufactured in Surat for $420 FOB retails in US independent jewelry chains for $1,600–$2,200.
- **Net Profit Spread**: 38% to 55% gross margin.

---

## 2. Corporate & Tax Architecture (The Delaware LLC + Indian LLP Loophole)
To win corporate wholesale accounts with US retailers and avoid crushing Indian corporate taxes:

```
[ US Retailers / Buying Groups (RJO / IJO) ]
                |
          (Pays USD on Net-30)
                v
[ US Delaware / Wyoming LLC (Single-Member Disregarded Entity) ]
  - Functions as the domestic US front-office
  - Holds US EIN, W-9, and US Business Bank Account (Mercury / Brex)
  - Insures invoices through Euler Hermes / Allianz Trade (Net-30 factoring)
                |
      (FOB / CIF Import Payment)
                v
[ Indian Limited Liability Partnership (LLP) (Surat / Mumbai) ]
  - Holds IEC (Import Export Code), GST, and RCMC (GJEPC)
  - Contracts directly with certified diamond bourses and casting units
  - Taxed at 30% flat in India, but profits distributed to partners are 100% EXEMPT under Section 10(2A) of the Income Tax Act.
```

---

## 3. Risk Mitigation & Logistics Infrastructure
1. **Never Stock Unsold Inventory**: Operate strictly on a Made-to-Order (MTO) and CAD-sample approval workflow.
2. **Door-to-Door Insured Transit**: Utilize **Malca-Amit** or **Brink's Global Services** armored air logistics. Coverage is 100% all-risk from Surat dispatch to US retail delivery.
3. **Credit Default Protection**: Use invoice factoring and credit insurance. If a US jeweler defaults on Net-30 payment, the credit insurer pays 90% of the invoice face value within 60 days.

---

## 4. Sales Distribution Channels
- **Independent Jeweler Buying Groups**: Target **RJO (Retail Jewelers Organization)** and **IJO (Independent Jewelers Organization)** which aggregate over 2,000 independent US retail stores.
- **Direct Wholesale Outreach**: Run automated outbound pipelines using `agents/buyer_outreach_agent.py` against our 190 crawled US corporate buyers.
