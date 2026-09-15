import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const {
      productCategory = "steel_rebar",
      productionVolumeTons = 100,
      fuelConsumptionMwh = 200,
      electricityConsumedMwh = 80,
      fuelFactor = 0.202,
      gridFactor = 0.716,
      euEtsPriceEur = 65.0
    } = body;

    const scope1 = Number((fuelConsumptionMwh * fuelFactor).toFixed(2));
    const scope2 = Number((electricityConsumedMwh * gridFactor).toFixed(2));
    const totalEmissions = Number((scope1 + scope2).toFixed(2));
    const specificEmissions = Number((totalEmissions / Math.max(productionVolumeTons, 1)).toFixed(3));
    const grossLiabilityEur = Number((totalEmissions * euEtsPriceEur).toFixed(2));
    const liabilityPerTonEur = Number((grossLiabilityEur / Math.max(productionVolumeTons, 1)).toFixed(2));

    return NextResponse.json({
      productCategory,
      productionVolumeTons,
      scope1DirectTco2: scope1,
      scope2IndirectTco2: scope2,
      totalEmbeddedTco2: totalEmissions,
      specificEmissionsPerTon: specificEmissions,
      grossCbamLiabilityEur: grossLiabilityEur,
      liabilityPerTonEur
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
}
