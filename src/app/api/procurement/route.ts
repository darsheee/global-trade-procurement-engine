import { NextResponse } from "next/server";

const TENDERS = [
  {
    id: "CAN-PSPC-2026-8941",
    country: "Canada",
    authority: "Public Services and Procurement Canada (PSPC)",
    title: "Precision Optical Equipment & Industrial Inspection Sensors",
    category: "Optical & Precision Instruments",
    hsnCode: "9031.80",
    estimatedValueUsd: 420000,
    closingDate: "2026-10-30",
    status: "OPEN"
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
    status: "OPEN"
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
    status: "OPEN"
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
    status: "OPEN"
  }
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const country = searchParams.get("country");
  const query = searchParams.get("q")?.toLowerCase();

  let results = TENDERS;
  if (country) {
    results = results.filter(t => t.country.toLowerCase() === country.toLowerCase());
  }
  if (query) {
    results = results.filter(t => 
      t.title.toLowerCase().includes(query) ||
      t.category.toLowerCase().includes(query) ||
      t.authority.toLowerCase().includes(query)
    );
  }

  return NextResponse.json({ total: results.length, tenders: results });
}
