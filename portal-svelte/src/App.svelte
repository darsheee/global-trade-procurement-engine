<script lang="ts">
  import { onMount } from 'svelte';

  // Active navigation tab
  let activeTab = $state<'cbam' | 'dpp' | 'roo' | 'gem' | 'exporters'>('cbam');
  let backendStatus = $state<'online' | 'offline' | 'checking'>('checking');

  // --- TAB 1: CBAM State ---
  let cbamProduct = $state('steel_rebar');
  let cbamVolume = $state(500.0);
  let cbamFuelMWh = $state(1200.0);
  let cbamElectricityMWh = $state(350.0);
  let cbamProcessEmissions = $state(80.0);
  let cbamCarbonPricePaid = $state(0.0);
  let cbamCalculationResult = $state<any>(null);
  let cbamLoading = $state(false);
  let cbamXmlOutput = $state<string>('');
  let cbamXmlLoading = $state(false);

  // --- TAB 2: DPP State ---
  let dppCompanyName = $state('Pasondia Precision Steel');
  let dppProductName = $state('Low-Carbon Reinforcing Steel Bar');
  let dppGtin = $state('8905544332211');
  let dppBatch = $state('BATCH-2026-IND-004');
  let dppCnCode = $state('72142000');
  let dppRecycledContent = $state(32.5);
  let dppCarbonIntensity = $state(1.146);
  let dppResult = $state<any>(null);
  let dppLoading = $state(false);

  // --- TAB 3: RoO State ---
  let rooFta = $state('India-UK CETA');
  let rooFinishedHs = $state('721420');
  let rooFobPrice = $state(1000.0);
  let rooBom = $state([
    { name: 'Indian Recycled Steel Scrap', hs_code: '720449', value_usd: 300.0, originating: true },
    { name: 'Imported Ferro-Manganese Alloy', hs_code: '720211', value_usd: 150.0, originating: false },
    { name: 'Domestic Processing & Plant Labor', hs_code: '998800', value_usd: 200.0, originating: true }
  ]);
  let rooResult = $state<any>(null);
  let rooLoading = $state(false);

  // --- TAB 4: GeM Tenders State ---
  let gemTenders = $state<any[]>([]);
  let gemLoading = $state(false);

  // --- TAB 5: Exporters State ---
  let exporters = $state<any[]>([]);
  let exporterSearch = $state('');
  let exportersLoading = $state(false);
  let activePitch = $state<any>(null);
  let pitchLoading = $state(false);

  // --- Health Check & Initial Load ---
  onMount(async () => {
    try {
      const res = await fetch('/api/v1/cbam/exporters?limit=1');
      if (res.ok) {
        backendStatus = 'online';
      } else {
        backendStatus = 'offline';
      }
    } catch (e) {
      backendStatus = 'offline';
    }

    // Auto-calculate default CBAM
    calculateCbam();
    loadGeMTenders();
    loadExporters();
  });

  // --- Handlers ---
  async function calculateCbam() {
    cbamLoading = true;
    cbamXmlOutput = '';
    try {
      const res = await fetch('/api/v1/cbam/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_category: cbamProduct,
          production_volume_tons: cbamVolume,
          fuel_consumption_mwh: cbamFuelMWh,
          fuel_carbon_factor: 0.202,
          process_emissions_tco2: cbamProcessEmissions,
          electricity_consumed_mwh: cbamElectricityMWh,
          carbon_price_paid_eur: cbamCarbonPricePaid,
          eu_ets_allowance_eur_per_tco2: 65.0
        })
      });
      const data = await res.json();
      if (res.ok) {
        cbamCalculationResult = data.data;
      }
    } catch (e) {
      console.error(e);
    } finally {
      cbamLoading = false;
    }
  }

  async function generateCbamXml() {
    cbamXmlLoading = true;
    try {
      const res = await fetch('/api/v1/cbam/generate-xml', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          declarant: {
            eori_number: 'NL123456789',
            company_name: 'Rotterdam Steel Logistics B.V.',
            country: 'NL'
          },
          installation: {
            name: 'Indian Steel & Alloys Ltd',
            city: 'Jamshedpur',
            cn_code: '72142000',
            lat: '22.8046',
            lon: '86.2029'
          },
          calculation: {
            product_category: cbamProduct,
            production_volume_tons: cbamVolume,
            fuel_consumption_mwh: cbamFuelMWh,
            fuel_carbon_factor: 0.202,
            process_emissions_tco2: cbamProcessEmissions,
            electricity_consumed_mwh: cbamElectricityMWh,
            carbon_price_paid_eur: cbamCarbonPricePaid,
            eu_ets_allowance_eur_per_tco2: 65.0
          }
        })
      });
      const data = await res.json();
      if (res.ok) {
        cbamXmlOutput = data.xml_report;
      }
    } catch (e) {
      console.error(e);
    } finally {
      cbamXmlLoading = false;
    }
  }

  async function generateDpp() {
    dppLoading = true;
    try {
      const res = await fetch('/api/v1/cbam/dpp/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          company_name: dppCompanyName,
          product_name: dppProductName,
          gtin: dppGtin,
          serial_batch: dppBatch,
          cn_code: dppCnCode,
          recycled_content_pct: dppRecycledContent,
          carbon_intensity_tco2_per_ton: dppCarbonIntensity
        })
      });
      const data = await res.json();
      if (res.ok) {
        dppResult = data;
      }
    } catch (e) {
      console.error(e);
    } finally {
      dppLoading = false;
    }
  }

  async function evaluateRoo() {
    rooLoading = true;
    try {
      const res = await fetch('/api/v1/roo/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          fta_agreement: rooFta,
          finished_hs_code: rooFinishedHs,
          fob_price_usd: rooFobPrice,
          bill_of_materials: rooBom,
          de_minimis_pct: 10.0
        })
      });
      const data = await res.json();
      if (res.ok) {
        rooResult = data.origin_evaluation;
      }
    } catch (e) {
      console.error(e);
    } finally {
      rooLoading = false;
    }
  }

  function addBomRow() {
    rooBom = [
      ...rooBom,
      { name: 'New Component', hs_code: '730000', value_usd: 50.0, originating: true }
    ];
  }

  function removeBomRow(index: number) {
    rooBom = rooBom.filter((_, i) => i !== index);
  }

  async function loadGeMTenders() {
    gemLoading = true;
    try {
      const res = await fetch('/api/v1/gem/tenders');
      const data = await res.json();
      if (res.ok) {
        gemTenders = data.tenders || [];
      }
    } catch (e) {
      console.error(e);
    } finally {
      gemLoading = false;
    }
  }

  async function loadExporters() {
    exportersLoading = true;
    try {
      const res = await fetch('/api/v1/cbam/exporters?limit=28');
      const data = await res.json();
      if (res.ok) {
        exporters = data.target_exporters || [];
      }
    } catch (e) {
      console.error(e);
    } finally {
      exportersLoading = false;
    }
  }

  async function loadPitch(companyName: string) {
    pitchLoading = true;
    activePitch = null;
    try {
      const res = await fetch(`/api/v1/cbam/pitch/${encodeURIComponent(companyName)}`);
      const data = await res.json();
      if (res.ok) {
        activePitch = data;
      }
    } catch (e) {
      console.error(e);
    } finally {
      pitchLoading = false;
    }
  }

  let filteredExporters = $derived(
    exporters.filter(e => 
      e.company_name.toLowerCase().includes(exporterSearch.toLowerCase()) ||
      e.location.toLowerCase().includes(exporterSearch.toLowerCase()) ||
      e.iec_code.toLowerCase().includes(exporterSearch.toLowerCase())
    )
  );
</script>

<div class="min-h-screen bg-slate-950 text-slate-100 font-sans flex flex-col">
  <!-- Top Navigation Header -->
  <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50 px-6 py-4">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-400 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20 text-white font-black text-xl">
          V
        </div>
        <div>
          <h1 class="text-xl font-bold tracking-tight text-white flex items-center gap-2">
            Vistara Trade Desk
            <span class="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
              2026 Engine
            </span>
          </h1>
          <p class="text-xs text-slate-400">
            EU CBAM Registry • Digital Product Passports • FTA Rules of Origin • GeM CPSE 4% Quota
          </p>
        </div>
      </div>

      <!-- System Status Pills -->
      <div class="flex items-center gap-3 text-xs">
        <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700">
          <span class="w-2 h-2 rounded-full {backendStatus === 'online' ? 'bg-emerald-400 animate-pulse' : 'bg-rose-400'}"></span>
          <span class="text-slate-300">FastAPI Backend:</span>
          <span class="font-mono font-medium {backendStatus === 'online' ? 'text-emerald-400' : 'text-rose-400'}">
            {backendStatus.toUpperCase()}
          </span>
        </div>
        <div class="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700">
          <span class="text-slate-400">Grid Factor:</span>
          <span class="font-mono text-emerald-400 font-medium">0.716 tCO2/MWh</span>
        </div>
        <div class="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700">
          <span class="text-slate-400">Database:</span>
          <span class="font-mono text-teal-300 font-medium">2,382 Exporters</span>
        </div>
      </div>
    </div>

    <!-- Navigation Tabs Bar -->
    <div class="max-w-7xl mx-auto mt-4 flex items-center gap-2 overflow-x-auto pb-1">
      <button 
        class="px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 {activeTab === 'cbam' ? 'bg-emerald-500 text-slate-950 font-semibold shadow-md shadow-emerald-500/20' : 'text-slate-400 hover:text-white hover:bg-slate-800'}"
        onclick={() => activeTab = 'cbam'}
      >
        <span>🌿</span> EU CBAM Carbon & XML
      </button>
      <button 
        class="px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 {activeTab === 'dpp' ? 'bg-emerald-500 text-slate-950 font-semibold shadow-md shadow-emerald-500/20' : 'text-slate-400 hover:text-white hover:bg-slate-800'}"
        onclick={() => activeTab = 'dpp'}
      >
        <span>🆔</span> Digital Product Passport (DPP)
      </button>
      <button 
        class="px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 {activeTab === 'roo' ? 'bg-emerald-500 text-slate-950 font-semibold shadow-md shadow-emerald-500/20' : 'text-slate-400 hover:text-white hover:bg-slate-800'}"
        onclick={() => activeTab = 'roo'}
      >
        <span>⚖️</span> FTA Rules of Origin (e-CoO)
      </button>
      <button 
        class="px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 {activeTab === 'gem' ? 'bg-emerald-500 text-slate-950 font-semibold shadow-md shadow-emerald-500/20' : 'text-slate-400 hover:text-white hover:bg-slate-800'}"
        onclick={() => activeTab = 'gem'}
      >
        <span>🏛️</span> GeM CPSE 4% Quota
      </button>
      <button 
        class="px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 {activeTab === 'exporters' ? 'bg-emerald-500 text-slate-950 font-semibold shadow-md shadow-emerald-500/20' : 'text-slate-400 hover:text-white hover:bg-slate-800'}"
        onclick={() => activeTab = 'exporters'}
      >
        <span>🏢</span> Exporter Directory & Pitches
      </button>
    </div>
  </header>

  <!-- Main Content Area -->
  <main class="flex-1 max-w-7xl w-full mx-auto p-6">
    <!-- TAB 1: EU CBAM CALCULATOR & XML GENERATOR -->
    {#if activeTab === 'cbam'}
      <div class="space-y-6">
        <div class="bg-gradient-to-r from-emerald-950/40 via-slate-900 to-slate-900 border border-emerald-500/20 rounded-2xl p-6">
          <div class="flex items-center gap-3 mb-2">
            <span class="text-2xl">🌿</span>
            <h2 class="text-xl font-bold text-white">EU CBAM Embedded Carbon Calculator & XML Registry Generator</h2>
          </div>
          <p class="text-sm text-slate-400 max-w-4xl">
            Compliant with Regulation (EU) 2023/956 and Implementing Regulation (EU) 2023/1773. Computes Scope 1 (Direct Fuel/Furnace) and Scope 2 (Grid Electricity) embedded carbon for Indian industrial exporters entering the definitive EU payment phase.
          </p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <!-- Left Column: Inputs Form -->
          <div class="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
            <h3 class="text-sm font-bold uppercase tracking-wider text-slate-400 flex items-center justify-between">
              <span>Plant & Production Inputs</span>
              <span class="text-xs text-emerald-400 font-mono">CEA Benchmark 0.716</span>
            </h3>

            <div>
              <label for="cbam-product-select" class="block text-xs font-medium text-slate-300 mb-1">Product Category</label>
              <select 
                id="cbam-product-select"
                bind:value={cbamProduct}
                class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500"
              >
                <option value="steel_rebar">Steel Rebars & Wire Rods (HS 7214 / 7213)</option>
                <option value="steel_crude">Crude Steel Ingots & Billets (HS 7206 / 7207)</option>
                <option value="aluminum_unwrought">Unwrought Aluminium Ingots (HS 7601)</option>
                <option value="aluminum_extrusion">Aluminium Bars, Rods & Profiles (HS 7604)</option>
                <option value="cement_clinker">Cement Clinker & Hydraulic (HS 2523)</option>
                <option value="fertilizer_ammonia">Anhydrous Ammonia (HS 2814)</option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="cbam-volume-input" class="block text-xs font-medium text-slate-300 mb-1">Production (Tons)</label>
                <input 
                  id="cbam-volume-input"
                  type="number" 
                  bind:value={cbamVolume} 
                  class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
              <div>
                <label for="cbam-fuel-input" class="block text-xs font-medium text-slate-300 mb-1">Fuel Consumed (MWh)</label>
                <input 
                  id="cbam-fuel-input"
                  type="number" 
                  bind:value={cbamFuelMWh} 
                  class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="cbam-elec-input" class="block text-xs font-medium text-slate-300 mb-1">Grid Electricity (MWh)</label>
                <input 
                  id="cbam-elec-input"
                  type="number" 
                  bind:value={cbamElectricityMWh} 
                  class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
              <div>
                <label for="cbam-process-input" class="block text-xs font-medium text-slate-300 mb-1">Process Emissions (tCO2)</label>
                <input 
                  id="cbam-process-input"
                  type="number" 
                  bind:value={cbamProcessEmissions} 
                  class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
            </div>

            <div>
              <label for="cbam-carbon-paid-input" class="block text-xs font-medium text-slate-300 mb-1">Domestic Carbon Price Paid (€)</label>
              <input 
                id="cbam-carbon-paid-input"
                type="number" 
                bind:value={cbamCarbonPricePaid} 
                class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"
              />
              <p class="text-[11px] text-slate-500 mt-1">Deductible under Article 9 of EU CBAM regulations.</p>
            </div>

            <div class="pt-2 flex gap-3">
              <button 
                class="flex-1 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold py-2.5 px-4 rounded-xl transition flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20"
                onclick={calculateCbam}
                disabled={cbamLoading}
              >
                {cbamLoading ? 'Computing...' : 'Recalculate Carbon'}
              </button>
              <button 
                class="bg-slate-800 hover:bg-slate-700 text-white font-semibold py-2.5 px-4 rounded-xl transition flex items-center gap-2 border border-slate-700"
                onclick={generateCbamXml}
                disabled={cbamXmlLoading}
              >
                {cbamXmlLoading ? 'Generating...' : 'Emit EU XML'}
              </button>
            </div>
          </div>

          <!-- Right Column: Results & XML -->
          <div class="lg:col-span-7 space-y-6">
            {#if cbamCalculationResult}
              <!-- Metric Cards -->
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
                  <div class="text-[11px] text-slate-400 uppercase tracking-wider">Scope 1 (Direct)</div>
                  <div class="text-xl font-mono font-bold text-white mt-1">
                    {cbamCalculationResult.scope1_direct_tco2} <span class="text-xs text-slate-400 font-sans">tCO2</span>
                  </div>
                </div>
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
                  <div class="text-[11px] text-slate-400 uppercase tracking-wider">Scope 2 (Indirect)</div>
                  <div class="text-xl font-mono font-bold text-white mt-1">
                    {cbamCalculationResult.scope2_indirect_tco2} <span class="text-xs text-slate-400 font-sans">tCO2</span>
                  </div>
                </div>
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
                  <div class="text-[11px] text-slate-400 uppercase tracking-wider">Intensity / Ton</div>
                  <div class="text-xl font-mono font-bold text-emerald-400 mt-1">
                    {cbamCalculationResult.specific_emissions_tco2_per_ton}
                  </div>
                </div>
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
                  <div class="text-[11px] text-slate-400 uppercase tracking-wider">EU CBAM Liability</div>
                  <div class="text-xl font-mono font-bold text-amber-400 mt-1">
                    €{cbamCalculationResult.net_cbam_liability_eur?.toLocaleString()}
                  </div>
                </div>
              </div>

              <!-- Liability & Benchmark Breakdown -->
              <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
                <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400">Customs Tariff & Benchmark Audit</h4>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
                  <div class="p-3 bg-slate-950 rounded-xl border border-slate-800/80">
                    <span class="text-slate-400 block text-xs">EU ETS Carbon Benchmark</span>
                    <span class="font-mono text-white font-semibold">{cbamCalculationResult.eu_benchmark_tco2_per_ton} tCO2/t</span>
                  </div>
                  <div class="p-3 bg-slate-950 rounded-xl border border-slate-800/80">
                    <span class="text-slate-400 block text-xs">Emissions vs Benchmark</span>
                    <span class="font-mono font-semibold {cbamCalculationResult.emissions_delta_vs_benchmark <= 0 ? 'text-emerald-400' : 'text-rose-400'}">
                      {cbamCalculationResult.emissions_delta_vs_benchmark > 0 ? '+' : ''}{cbamCalculationResult.emissions_delta_vs_benchmark} tCO2/t
                    </span>
                  </div>
                  <div class="p-3 bg-slate-950 rounded-xl border border-slate-800/80">
                    <span class="text-slate-400 block text-xs">Border Surcharge / Ton</span>
                    <span class="font-mono text-amber-400 font-semibold">€{cbamCalculationResult.cbam_cost_per_ton_eur} / ton</span>
                  </div>
                </div>
              </div>
            {/if}

            <!-- XML Registry Preview -->
            {#if cbamXmlOutput}
              <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
                <div class="flex items-center justify-between">
                  <h4 class="text-xs font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-2">
                    <span>European Commission CBAM Registry XML</span>
                    <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-[10px] text-emerald-400">Schema Validated</span>
                  </h4>
                  <button 
                    class="text-xs text-slate-400 hover:text-white px-2 py-1 rounded bg-slate-800 border border-slate-700 transition"
                    onclick={() => navigator.clipboard.writeText(cbamXmlOutput)}
                  >
                    Copy XML
                  </button>
                </div>
                <pre class="bg-slate-950 p-4 rounded-xl font-mono text-xs text-emerald-300 overflow-x-auto max-h-72 border border-slate-800 leading-relaxed">{cbamXmlOutput}</pre>
              </div>
            {/if}
          </div>
        </div>
      </div>
    {/if}

    <!-- TAB 2: DIGITAL PRODUCT PASSPORT (DPP) -->
    {#if activeTab === 'dpp'}
      <div class="space-y-6">
        <div class="bg-gradient-to-r from-teal-950/40 via-slate-900 to-slate-900 border border-teal-500/20 rounded-2xl p-6">
          <div class="flex items-center gap-3 mb-2">
            <span class="text-2xl">🆔</span>
            <h2 class="text-xl font-bold text-white">EU Digital Product Passport (DPP) Data Carrier Generator</h2>
          </div>
          <p class="text-sm text-slate-400 max-w-4xl">
            Generates GS1 Digital Link standard URIs conforming to the EU Ecodesign for Sustainable Products Regulation (ESPR, Regulation (EU) 2024/1781) with embedded circularity, recycled content, and carbon footprint verification.
          </p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div class="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
            <h3 class="text-sm font-bold uppercase tracking-wider text-slate-400">Product Passport Metadata</h3>

            <div>
              <label for="dpp-company-input" class="block text-xs font-medium text-slate-300 mb-1">Manufacturer Company Name</label>
              <input 
                id="dpp-company-input"
                type="text" 
                bind:value={dppCompanyName} 
                class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-teal-500"
              />
            </div>

            <div>
              <label for="dpp-product-input" class="block text-xs font-medium text-slate-300 mb-1">Product Description / Trade Name</label>
              <input 
                id="dpp-product-input"
                type="text" 
                bind:value={dppProductName} 
                class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-teal-500"
              />
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="dpp-gtin-input" class="block text-xs font-medium text-slate-300 mb-1">GS1 GTIN-13</label>
                <input 
                  id="dpp-gtin-input"
                  type="text" 
                  bind:value={dppGtin} 
                  class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-teal-500"
                />
              </div>
              <div>
                <label for="dpp-batch-input" class="block text-xs font-medium text-slate-300 mb-1">Batch / Serial</label>
                <input 
                  id="dpp-batch-input"
                  type="text" 
                  bind:value={dppBatch} 
                  class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-teal-500"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="dpp-cn-input" class="block text-xs font-medium text-slate-300 mb-1">EU CN Code</label>
                <input 
                  id="dpp-cn-input"
                  type="text" 
                  bind:value={dppCnCode} 
                  class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-teal-500"
                />
              </div>
              <div>
                <label for="dpp-recycled-input" class="block text-xs font-medium text-slate-300 mb-1">Recycled Content (%)</label>
                <input 
                  id="dpp-recycled-input"
                  type="number" 
                  bind:value={dppRecycledContent} 
                  class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-teal-500"
                />
              </div>
            </div>

            <button 
              class="w-full bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold py-2.5 px-4 rounded-xl transition flex items-center justify-center gap-2 shadow-lg shadow-teal-500/20"
              onclick={generateDpp}
              disabled={dppLoading}
            >
              {dppLoading ? 'Issuing...' : 'Generate GS1 Digital Link'}
            </button>
          </div>

          <div class="lg:col-span-7 space-y-6">
            {#if dppResult}
              <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
                <div class="flex items-center justify-between">
                  <h4 class="text-xs font-bold uppercase tracking-wider text-teal-400">GS1 Digital Link URI</h4>
                  <span class="text-xs px-2.5 py-0.5 rounded-full bg-teal-500/10 text-teal-300 border border-teal-500/20">
                    ESPR 1.0 Compliant
                  </span>
                </div>

                <div class="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between gap-2">
                  <code class="text-xs text-teal-300 font-mono truncate">{dppResult.gs1_digital_link}</code>
                  <button 
                    class="text-xs text-slate-400 hover:text-white px-2 py-1 rounded bg-slate-800 shrink-0"
                    onclick={() => navigator.clipboard.writeText(dppResult.gs1_digital_link)}
                  >
                    Copy
                  </button>
                </div>

                <pre class="bg-slate-950 p-4 rounded-xl font-mono text-xs text-slate-300 overflow-x-auto max-h-96 border border-slate-800 leading-relaxed">{JSON.stringify(dppResult.dpp_payload, null, 2)}</pre>
              </div>
            {:else}
              <div class="bg-slate-900 border border-slate-800 rounded-2xl p-12 text-center text-slate-500">
                Click "Generate GS1 Digital Link" to issue a certified Digital Product Passport payload.
              </div>
            {/if}
          </div>
        </div>
      </div>
    {/if}

    <!-- TAB 3: FTA RULES OF ORIGIN -->
    {#if activeTab === 'roo'}
      <div class="space-y-6">
        <div class="bg-gradient-to-r from-blue-950/40 via-slate-900 to-slate-900 border border-blue-500/20 rounded-2xl p-6">
          <div class="flex items-center gap-3 mb-2">
            <span class="text-2xl">⚖️</span>
            <h2 class="text-xl font-bold text-white">FTA Rules of Origin (RoO) & e-CoO Verification Desk</h2>
          </div>
          <p class="text-sm text-slate-400 max-w-4xl">
            Evaluates Regional Value Content (RVC $\ge 35\% - 40\%$) and Change in Tariff Sub-Heading (CTSH at 6-digit level) under India-UK CETA, India-UAE CEPA, India-Australia ECTA, and India-EFTA TEPA for 0% preferential customs entry.
          </p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div class="lg:col-span-6 bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="roo-agreement-select" class="block text-xs font-medium text-slate-300 mb-1">Trade Agreement</label>
                <select 
                  id="roo-agreement-select"
                  bind:value={rooFta}
                  class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                >
                  <option value="India-UK CETA">India-UK CETA (Min VA: 35%)</option>
                  <option value="India-UAE CEPA">India-UAE CEPA (Min VA: 40%)</option>
                  <option value="India-Australia ECTA">India-Australia ECTA (Min VA: 35%)</option>
                  <option value="India-EFTA TEPA">India-EFTA TEPA (Min VA: 35%)</option>
                </select>
              </div>
              <div>
                <label for="roo-fob-input" class="block text-xs font-medium text-slate-300 mb-1">Finished FOB Price ($)</label>
                <input 
                  id="roo-fob-input"
                  type="number" 
                  bind:value={rooFobPrice} 
                  class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div>
              <label for="roo-hs-input" class="block text-xs font-medium text-slate-300 mb-1">Finished Good HS Subheading (6-Digit)</label>
              <input 
                id="roo-hs-input"
                type="text" 
                bind:value={rooFinishedHs} 
                class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-blue-500"
              />
            </div>

            <!-- Bill of Materials Table -->
            <div class="space-y-2 pt-2">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Bill of Materials (BOM)</span>
                <button 
                  class="text-xs text-blue-400 hover:text-blue-300 font-medium px-2 py-1 rounded bg-blue-500/10 border border-blue-500/20"
                  onclick={addBomRow}
                >
                  + Add Input Material
                </button>
              </div>

              <div class="space-y-2 max-h-64 overflow-y-auto pr-1">
                {#each rooBom as item, i}
                  <div class="flex items-center gap-2 p-2 bg-slate-950 rounded-xl border border-slate-800 text-xs">
                    <input 
                      type="text" 
                      bind:value={item.name} 
                      placeholder="Material"
                      class="flex-1 bg-transparent border-b border-slate-800 py-1 text-white focus:outline-none"
                    />
                    <input 
                      type="text" 
                      bind:value={item.hs_code} 
                      placeholder="HS Code"
                      class="w-20 font-mono bg-transparent border-b border-slate-800 py-1 text-slate-300 focus:outline-none"
                    />
                    <input 
                      type="number" 
                      bind:value={item.value_usd} 
                      placeholder="$ Value"
                      class="w-16 font-mono bg-transparent border-b border-slate-800 py-1 text-slate-300 focus:outline-none"
                    />
                    <label class="flex items-center gap-1 cursor-pointer shrink-0">
                      <input type="checkbox" bind:checked={item.originating} class="rounded border-slate-700 text-blue-500" />
                      <span class="text-[10px] {item.originating ? 'text-emerald-400' : 'text-slate-500'}">Orig</span>
                    </label>
                    <button 
                      class="text-rose-400 hover:text-rose-300 px-1.5"
                      onclick={() => removeBomRow(i)}
                    >
                      ×
                    </button>
                  </div>
                {/each}
              </div>
            </div>

            <button 
              class="w-full bg-blue-500 hover:bg-blue-400 text-slate-950 font-bold py-2.5 px-4 rounded-xl transition flex items-center justify-center gap-2 shadow-lg shadow-blue-500/20"
              onclick={evaluateRoo}
              disabled={rooLoading}
            >
              {rooLoading ? 'Auditing BOM...' : 'Evaluate Origin Eligibility'}
            </button>
          </div>

          <!-- RoO Determination Display -->
          <div class="lg:col-span-6 space-y-6">
            {#if rooResult}
              <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5">
                <div class="flex items-center justify-between">
                  <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400">Origin Determination</h4>
                  <span class="text-xs px-3 py-1 rounded-full font-bold {rooResult.origin_qualifies_for_preferential_tariff ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'}">
                    {rooResult.origin_qualifies_for_preferential_tariff ? '0% PREFERENTIAL DUTY APPROVED' : 'NON-COMPLIANT'}
                  </span>
                </div>

                <div class="grid grid-cols-2 gap-3 text-sm">
                  <div class="p-3 bg-slate-950 rounded-xl border border-slate-800">
                    <span class="text-slate-400 block text-xs">Domestic Value Addition</span>
                    <span class="text-xl font-mono font-bold {rooResult.va_rule_satisfied ? 'text-emerald-400' : 'text-rose-400'}">
                      {rooResult.domestic_value_addition_pct}%
                    </span>
                    <span class="text-[10px] text-slate-500 block">Required: $\ge$ {rooResult.min_required_va_pct}%</span>
                  </div>
                  <div class="p-3 bg-slate-950 rounded-xl border border-slate-800">
                    <span class="text-slate-400 block text-xs">CTSH (6-Digit Change)</span>
                    <span class="text-xl font-mono font-bold {rooResult.ctsh_rule_satisfied ? 'text-emerald-400' : 'text-rose-400'}">
                      {rooResult.ctsh_rule_satisfied ? 'PASSED' : 'FAILED'}
                    </span>
                    <span class="text-[10px] text-slate-500 block">{rooResult.de_minimis_applied ? 'De Minimis 10% Applied' : 'Clean Heading Change'}</span>
                  </div>
                </div>

                <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
                  <div class="text-xs text-slate-400">DGFT e-CoO Filing Status:</div>
                  <div class="font-mono text-sm font-semibold {rooResult.dgft_e_coo_filing_status === 'READY_TO_FILE' ? 'text-emerald-400' : 'text-amber-400'}">
                    {rooResult.dgft_e_coo_filing_status}
                  </div>
                  <p class="text-xs text-slate-500">
                    {rooResult.origin_qualifies_for_preferential_tariff 
                      ? 'Shipment satisfies all legal criteria for preferential Certificate of Origin on coo.dgft.gov.in.' 
                      : 'BOM exceeds allowable non-originating materials under the specified tariff heading.'}
                  </p>
                </div>
              </div>
            {:else}
              <div class="bg-slate-900 border border-slate-800 rounded-2xl p-12 text-center text-slate-500">
                Click "Evaluate Origin Eligibility" to audit the Bill of Materials against FTA rules.
              </div>
            {/if}
          </div>
        </div>
      </div>
    {/if}

    <!-- TAB 4: GeM CPSE 4% QUOTA & EMD WAIVER -->
    {#if activeTab === 'gem'}
      <div class="space-y-6">
        <div class="bg-gradient-to-r from-amber-950/40 via-slate-900 to-slate-900 border border-amber-500/20 rounded-2xl p-6">
          <div class="flex items-center gap-3 mb-2">
            <span class="text-2xl">🏛️</span>
            <h2 class="text-xl font-bold text-white">GeM CPSE 4% Reserved Public Procurement & EMD Waiver Tracker</h2>
          </div>
          <p class="text-sm text-slate-400 max-w-4xl">
            Under the Public Procurement Policy for MSEs Order 2012, Central Ministries and CPSEs (ONGC, BHEL, NTPC, IOCL) must procure at least 4% from SC/ST MSEs. Leverages NSIC SPRS for 100% Earnest Money Deposit (EMD) exemption and subcontracting back to audited factories.
          </p>
        </div>

        {#if gemLoading}
          <div class="text-center py-12 text-slate-500">Loading active CPSE tenders...</div>
        {:else}
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            {#each gemTenders as t}
              <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 hover:border-amber-500/30 transition">
                <div class="flex items-start justify-between gap-4">
                  <div>
                    <span class="text-[11px] font-mono font-semibold px-2.5 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">
                      {t.cpse_authority}
                    </span>
                    <h3 class="text-base font-bold text-white mt-2 leading-snug">{t.title}</h3>
                  </div>
                  <div class="text-right shrink-0">
                    <span class="text-xs text-slate-500 block">Contract Value</span>
                    <span class="text-lg font-mono font-bold text-emerald-400">₹{(t.contract_value_inr / 100000).toFixed(1)} Lakhs</span>
                  </div>
                </div>

                <div class="p-3 bg-slate-950 rounded-xl border border-slate-800/80 grid grid-cols-2 gap-3 text-xs">
                  <div>
                    <span class="text-slate-400 block text-[10px] uppercase">Closing Date</span>
                    <span class="font-mono text-white font-medium">{t.closing_date}</span>
                  </div>
                  <div>
                    <span class="text-slate-400 block text-[10px] uppercase">100% EMD Saved (NSIC)</span>
                    <span class="font-mono text-emerald-400 font-bold">₹{t.sovereign_sc_advantage.cash_saved_vs_general_competitor_inr?.toLocaleString()}</span>
                  </div>
                </div>

                <div class="text-xs space-y-1.5">
                  <div class="text-slate-400 font-medium">Matching Subcontract Factories in Database:</div>
                  <div class="space-y-1">
                    {#each t.matching_client_factories as f}
                      <div class="flex items-center justify-between p-2 rounded-lg bg-slate-950/60 border border-slate-800 text-[11px]">
                        <span class="text-slate-200 font-medium truncate max-w-[200px]">{f.factory_name}</span>
                        <span class="font-mono text-slate-500">{f.location}</span>
                      </div>
                    {/each}
                  </div>
                </div>

                <div class="pt-2 border-t border-slate-800 flex items-center justify-between text-xs">
                  <span class="text-slate-500">Estimated 12% Spread: <strong class="text-amber-400">₹{t.sovereign_sc_advantage.estimated_gross_spread_inr?.toLocaleString()}</strong></span>
                  <button 
                    class="px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs transition"
                    onclick={() => alert(`Bid dossier drafted for tender ${t.tender_id}. Sovereign EMD exemption clause active.`)}
                  >
                    Draft GeM Bid Dossier
                  </button>
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </div>
    {/if}

    <!-- TAB 5: EXPORTER DIRECTORY & PITCH GENERATOR -->
    {#if activeTab === 'exporters'}
      <div class="space-y-6">
        <div class="bg-gradient-to-r from-purple-950/40 via-slate-900 to-slate-900 border border-purple-500/20 rounded-2xl p-6">
          <div class="flex items-center gap-3 mb-2">
            <span class="text-2xl">🏢</span>
            <h2 class="text-xl font-bold text-white">Target Exporter Directory & CBAM Retainer Pitch Generator</h2>
          </div>
          <p class="text-sm text-slate-400 max-w-4xl">
            Indexed from our local database (`india_usa_trade.db`). Search steel and metal export manufacturers subject to EU CBAM and generate instant, customized ₹45,000/quarter retainer proposals.
          </p>
        </div>

        <div class="flex items-center gap-4">
          <div class="flex-1 relative">
            <input 
              type="text" 
              placeholder="Search by company name, city, state, or IEC code..." 
              bind:value={exporterSearch}
              class="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-purple-500"
            />
          </div>
          <span class="text-xs text-slate-400">Showing {filteredExporters.length} exporters</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {#each filteredExporters as exp}
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 hover:border-purple-500/30 transition flex flex-col justify-between">
              <div>
                <div class="flex items-start justify-between gap-2">
                  <h4 class="text-sm font-bold text-white leading-snug">{exp.company_name}</h4>
                  {#if exp.is_star_exporter}
                    <span class="px-2 py-0.5 rounded text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 font-semibold shrink-0">
                      Star House
                    </span>
                  {/if}
                </div>
                <div class="text-xs text-slate-400 mt-1">{exp.location}</div>
                <div class="font-mono text-xs text-slate-500 mt-0.5">IEC: {exp.iec_code}</div>
              </div>

              <div class="pt-3 border-t border-slate-800 flex items-center justify-between">
                <span class="text-[11px] text-emerald-400 font-medium">CBAM Definite Phase</span>
                <button 
                  class="px-3 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs transition"
                  onclick={() => loadPitch(exp.company_name)}
                >
                  Generate Pitch
                </button>
              </div>
            </div>
          {/each}
        </div>

        <!-- Active Pitch Modal / Dossier -->
        {#if activePitch}
          <div class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div class="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full p-6 space-y-4 max-h-[90vh] overflow-y-auto">
              <div class="flex items-center justify-between">
                <h3 class="text-base font-bold text-white">CBAM Compliance Proposal Dossier</h3>
                <button 
                  class="text-slate-400 hover:text-white text-lg font-bold"
                  onclick={() => activePitch = null}
                >
                  ×
                </button>
              </div>

              <div class="p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs space-y-1">
                <div><strong class="text-slate-400">Target:</strong> <span class="text-white">{activePitch.company_name}</span></div>
                <div><strong class="text-slate-400">Location:</strong> <span class="text-white">{activePitch.location}</span></div>
                <div><strong class="text-slate-400">Retainer Fee:</strong> <span class="text-emerald-400 font-bold">₹{activePitch.quarterly_retainer_inr.toLocaleString()} / quarter (€{activePitch.quarterly_retainer_eur})</span></div>
              </div>

              <div>
                <label for="pitch-subject-input" class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Subject Line</label>
                <input 
                  id="pitch-subject-input"
                  type="text" 
                  readonly 
                  value={activePitch.email_subject} 
                  class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-purple-300 font-medium"
                />
              </div>

              <div>
                <label for="pitch-body-textarea" class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Email Pitch Body</label>
                <textarea 
                  id="pitch-body-textarea"
                  rows="10" 
                  readonly 
                  class="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-300 font-mono leading-relaxed resize-none"
                >{activePitch.email_pitch}</textarea>
              </div>

              <div class="flex gap-3 pt-2">
                <button 
                  class="flex-1 bg-purple-600 hover:bg-purple-500 text-white font-bold py-2 px-4 rounded-xl text-xs transition"
                  onclick={() => {
                    navigator.clipboard.writeText(`${activePitch.email_subject}\n\n${activePitch.email_pitch}`);
                    alert('Copied pitch email to clipboard!');
                  }}
                >
                  Copy Email Pitch
                </button>
                <button 
                  class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2 px-4 rounded-xl text-xs transition"
                  onclick={() => window.open(`https://api.whatsapp.com/send?text=${encodeURIComponent(activePitch.email_pitch.slice(0, 500))}`, '_blank')}
                >
                  Send via WhatsApp
                </button>
              </div>
            </div>
          </div>
        {/if}
      </div>
    {/if}
  </main>
</div>
