<div class="flex flex-col gap-6 h-full">
    <!-- Overcrowding Alert Banner -->
    @if($overcrowdingAlert)
    <div class="w-full bg-red-500/10 border border-red-500/30 rounded-2xl p-5 flex items-start gap-4 text-red-400 animate-pulse shadow-[0_0_20px_rgba(239,68,68,0.15)] transition-all duration-300">
        <svg class="w-6 h-6 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div class="flex flex-col">
            <span class="font-semibold tracking-wide text-sm uppercase">Capacity Warning</span>
            <span class="text-xs opacity-80 mt-1 leading-relaxed">Pediatric load exceeds 30% of standard waiting capacity. Consider dispatching additional triage staff.</span>
        </div>
    </div>
    @endif

    <div class="flex items-center justify-between mb-2">
        <h3 class="text-3xl font-bold tracking-tight text-white">Real-Time Telemetry</h3>
        <span class="flex h-3 w-3 relative">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#0058bc] opacity-75"></span>
            <span class="relative inline-flex rounded-full h-3 w-3 bg-[#0070eb]"></span>
        </span>
    </div>

    <!-- Current Occupancy Cards -->
    <div class="grid grid-cols-2 gap-4">
        <div class="bg-white/5 backdrop-blur-[20px] border border-white/10 rounded-[20px] p-6 hover:bg-white/10 transition-colors duration-500 relative overflow-hidden group">
            <div class="absolute inset-0 bg-gradient-to-br from-[#0058bc]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <span class="text-xs font-semibold text-[#a0a0a5] tracking-[0.1em] uppercase mb-2 block">Pediatric Count</span>
            <div class="text-6xl font-bold tracking-tighter text-white drop-shadow-[0_0_15px_rgba(255,255,255,0.2)]">
                {{ $currentChildren }}
            </div>
        </div>
        <div class="bg-white/5 backdrop-blur-[20px] border border-white/10 rounded-[20px] p-6 hover:bg-white/10 transition-colors duration-500">
            <span class="text-xs font-semibold text-[#a0a0a5] tracking-[0.1em] uppercase mb-2 block">Adult Count</span>
            <div class="text-6xl font-bold tracking-tighter text-[#c1c6d7]">
                {{ $currentAdults }}
            </div>
        </div>
    </div>

    <!-- Daily Totals -->
    <div class="bg-[#1a1c1d]/60 backdrop-blur-[24px] border border-white/10 rounded-[20px] p-6 mt-2 flex-grow">
        <h4 class="text-xs font-semibold text-[#a0a0a5] tracking-[0.15em] uppercase mb-6 pb-4 border-b border-white/10">Daily Aggregates</h4>
        
        <div class="space-y-8">
            <div class="group">
                <div class="flex justify-between text-sm mb-3">
                    <span class="text-white font-medium">Total Pediatric Processed</span>
                    <span class="text-white font-bold tracking-wide">{{ $totalDailyChildren }}</span>
                </div>
                <div class="w-full bg-white/5 h-2 rounded-full overflow-hidden border border-white/5">
                    <div class="bg-[#0058bc] h-full transition-all duration-1000 ease-out shadow-[0_0_10px_#0058bc]" style="width: {{ min(($totalDailyChildren / max(1, $totalDailyAdults + $totalDailyChildren)) * 100, 100) }}%"></div>
                </div>
            </div>

            <div class="group">
                <div class="flex justify-between text-sm mb-3">
                    <span class="text-[#a0a0a5] font-medium">Total Adults Processed</span>
                    <span class="text-[#c1c6d7] font-bold tracking-wide">{{ $totalDailyAdults }}</span>
                </div>
                <div class="w-full bg-white/5 h-2 rounded-full overflow-hidden border border-white/5">
                    <div class="bg-[#717786] h-full transition-all duration-1000 ease-out" style="width: {{ min(($totalDailyAdults / max(1, $totalDailyAdults + $totalDailyChildren)) * 100, 100) }}%"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Generate Report Button -->
    <button wire:click="downloadReport" wire:target="downloadReport" wire:loading.attr="disabled" class="w-full bg-[#f9f9fb] text-[#1a1c1d] font-semibold text-sm tracking-wide px-6 py-4 rounded-full shadow-[0_0_20px_rgba(255,255,255,0.1)] hover:shadow-[0_0_30px_rgba(255,255,255,0.2)] hover:-translate-y-1 transition-all duration-300 flex items-center justify-center gap-3 group disabled:opacity-50 disabled:cursor-not-allowed">
        <svg wire:loading.remove wire:target="downloadReport" class="w-5 h-5 group-hover:scale-110 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <svg wire:loading wire:target="downloadReport" class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span wire:loading.remove wire:target="downloadReport">Generate Capacity Report</span>
        <span wire:loading wire:target="downloadReport">Compiling PDF...</span>
    </button>
</div>
