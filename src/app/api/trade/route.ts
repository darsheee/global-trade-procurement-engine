import { NextResponse } from "next/server";
import tradeMetrics from "@/../data/trade/trade_metrics.json";
import usImporters from "@/../data/trade/us_importers_crawled.json";
import exporters from "@/../data/trade/exporters_sample.json";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const type = searchParams.get("type") || "all";
  const query = searchParams.get("q")?.toLowerCase() || "";

  if (type === "metrics") {
    return NextResponse.json(tradeMetrics);
  }

  if (type === "importers") {
    const filtered = query
      ? usImporters.filter(
          (i: any) =>
            i.company_name?.toLowerCase().includes(query) ||
            i.industry_category?.toLowerCase().includes(query) ||
            i.city?.toLowerCase().includes(query)
        )
      : usImporters;
    return NextResponse.json({ total: filtered.length, importers: filtered });
  }

  if (type === "exporters") {
    const filtered = query
      ? exporters.filter(
          (e: any) =>
            e.company_name?.toLowerCase().includes(query) ||
            e.deal_in?.toLowerCase().includes(query) ||
            e.city?.toLowerCase().includes(query) ||
            e.state_name?.toLowerCase().includes(query)
        )
      : exporters;
    return NextResponse.json({ total: filtered.length, exporters: filtered });
  }

  return NextResponse.json({
    metrics: tradeMetrics,
    sampleImporters: usImporters.slice(0, 10),
    sampleExporters: exporters.slice(0, 10)
  });
}
