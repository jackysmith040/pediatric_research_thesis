<div class="min-h-screen bg-[#0e0e0e] text-[#e5e2e1] font-['Manrope'] selection:bg-indigo-500/30">
    <!-- Navbar -->
    <nav class="w-full border-b border-[#262626] bg-[#141313]/80 backdrop-blur-md px-8 py-4 flex justify-between items-center sticky top-0 z-50">
        <div class="flex items-center gap-4">
            <div class="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 shadow-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
            </div>
            <h1 class="text-xl font-bold font-['Noto_Serif'] text-white tracking-tight">Pediatric Tracker</h1>
        </div>
        <div class="flex items-center gap-4 text-sm font-semibold tracking-wider text-neutral-400">
            <span x-data="{ connected: false }" 
                  @echo-connected.window="connected = true" 
                  @echo-disconnected.window="connected = false"
                  class="flex items-center gap-2">
                <span class="relative flex h-3 w-3">
                  <span x-show="connected" class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-3 w-3" :class="connected ? 'bg-emerald-500' : 'bg-red-500'"></span>
                </span>
                <span x-text="connected ? 'LIVE WEBSOCKET' : 'DISCONNECTED'"></span>
            </span>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-[1400px] mx-auto px-8 py-10 grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        <!-- Left Column: Video Feed (Spans 8 cols) -->
        <div class="lg:col-span-8 flex flex-col gap-6">
            <div class="bg-[#121212] border border-[#262626] rounded-2xl overflow-hidden shadow-2xl group relative">
                <!-- Video Header -->
                <div class="px-6 py-4 border-b border-[#262626] bg-[#1a1a1a]/50 flex justify-between items-center">
                    <h2 class="text-sm font-semibold text-neutral-300 uppercase tracking-widest">Outpatient Waiting Area CCTV</h2>
                    <span class="text-xs text-neutral-500">Port 5001 • YOLO26n</span>
                </div>
                
                <!-- MJPEG Stream Container -->
                <div class="relative w-full aspect-video bg-black overflow-hidden flex items-center justify-center">
                    <img 
                        src="http://127.0.0.1:5001/video_feed" 
                        alt="Live CV Stream Feed" 
                        class="w-full h-full object-cover opacity-90 group-hover:opacity-100 transition-opacity duration-500"
                        onerror="this.onerror=null; this.outerHTML='<div class=\'text-neutral-500 flex flex-col items-center\'><svg class=\'w-12 h-12 mb-2\' fill=\'none\' stroke=\'currentColor\' viewBox=\'0 0 24 24\'><path stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'1.5\' d=\'M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636\'></path></svg><span>Stream Offline. Please start the CV Engine.</span></div>';"
                    />
                </div>
            </div>

            <!-- Overcrowding Alert Banner -->
            @if($overcrowdingAlert)
            <div class="w-full bg-red-500/10 border border-red-500/30 rounded-xl p-4 flex items-center gap-4 text-red-400 animate-pulse">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <div class="flex flex-col">
                    <span class="font-bold text-sm">Capacity Warning</span>
                    <span class="text-xs opacity-80">Pediatric load exceeds 30% of standard waiting capacity.</span>
                </div>
            </div>
            @endif
        </div>

        <!-- Right Column: Telemetry Dashboard (Spans 4 cols) -->
        <div class="lg:col-span-4 flex flex-col gap-6">
            
            <h3 class="font-['Noto_Serif'] text-3xl text-white font-light tracking-tight mb-2">Real-Time Capacity</h3>

            <!-- Current Occupancy Cards -->
            <div class="grid grid-cols-2 gap-4">
                <div class="bg-[#121212] border border-[#262626] rounded-xl p-6 hover:border-[#404040] transition-colors duration-300">
                    <span class="text-xs font-semibold text-neutral-400 block tracking-wider uppercase mb-1">Current Pediatric</span>
                    <div class="text-5xl font-['Noto_Serif'] text-white drop-shadow-md" wire:transition>
                        {{ $currentChildren }}
                    </div>
                </div>
                <div class="bg-[#121212] border border-[#262626] rounded-xl p-6 hover:border-[#404040] transition-colors duration-300">
                    <span class="text-xs font-semibold text-neutral-400 block tracking-wider uppercase mb-1">Current Adults</span>
                    <div class="text-5xl font-['Noto_Serif'] text-neutral-300" wire:transition>
                        {{ $currentAdults }}
                    </div>
                </div>
            </div>

            <!-- Daily Totals -->
            <div class="bg-[#1c1c1e]/60 backdrop-blur-md border border-[#333] rounded-xl p-6 mt-4">
                <h4 class="text-sm font-semibold text-white tracking-wide mb-6 border-b border-[#333] pb-3">Daily Aggregates</h4>
                
                <div class="space-y-6">
                    <div>
                        <div class="flex justify-between text-sm mb-2">
                            <span class="text-neutral-400">Total Pediatric Processed</span>
                            <span class="text-white font-semibold">{{ $totalDailyChildren }}</span>
                        </div>
                        <div class="w-full bg-[#2a2a2a] h-1.5 rounded-full overflow-hidden">
                            <div class="bg-gradient-to-r from-purple-500 to-indigo-500 h-full transition-all duration-500" style="width: {{ min(($totalDailyChildren / max(1, $totalDailyAdults + $totalDailyChildren)) * 100, 100) }}%"></div>
                        </div>
                    </div>

                    <div>
                        <div class="flex justify-between text-sm mb-2">
                            <span class="text-neutral-400">Total Adults Processed</span>
                            <span class="text-white font-semibold">{{ $totalDailyAdults }}</span>
                        </div>
                        <div class="w-full bg-[#2a2a2a] h-1.5 rounded-full overflow-hidden">
                            <div class="bg-neutral-500 h-full transition-all duration-500" style="width: {{ min(($totalDailyAdults / max(1, $totalDailyAdults + $totalDailyChildren)) * 100, 100) }}%"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Generate Report Button -->
            <button class="mt-auto w-full bg-white text-black font-semibold text-sm px-6 py-4 rounded-xl shadow-[0_0_20px_rgba(255,255,255,0.1)] hover:shadow-[0_0_30px_rgba(255,255,255,0.2)] hover:-translate-y-0.5 transition-all duration-300 flex items-center justify-center gap-2 group">
                <svg class="w-5 h-5 text-neutral-800 group-hover:scale-110 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Download Nightly PDF Early
            </button>
        </div>
    </main>
</div>
