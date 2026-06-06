<div class="min-h-screen bg-[#141517] font-['Inter'] selection:bg-[#0058bc]/30 relative overflow-hidden text-white w-full">
    
    <!-- Navbar -->
    <nav class="w-full px-8 py-6 border-b border-white/5 bg-[#1c1c1e]/80 backdrop-blur-lg fixed top-0 z-50">
        <div class="max-w-[1600px] mx-auto flex justify-between items-center">
            <div class="flex items-center gap-4">
                <a href="/" wire:navigate class="w-10 h-10 rounded-full border border-white/10 flex items-center justify-center hover:bg-white/5 transition-colors">
                    <svg class="w-5 h-5 text-[#a0a0a5]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                </a>
                <h1 class="text-lg font-bold tracking-tight">Clinical Command Center</h1>
            </div>
            
            <div class="flex items-center gap-3"
                 x-data="{ echoConnected: false }"
                 @echo-connected.window="echoConnected = true"
                 @echo-disconnected.window="echoConnected = false"
                 x-on:error.window="echoConnected = false">
                 
                <!-- Online State -->
                <template x-if="echoConnected">
                    <div class="flex items-center gap-3">
                        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_10px_#10b981]"></span>
                        <span class="text-xs font-semibold tracking-wider text-emerald-500 uppercase">Reverb Live</span>
                    </div>
                </template>

                <!-- Offline State -->
                <template x-if="!echoConnected">
                    <div class="flex items-center gap-3">
                        <span class="w-2 h-2 rounded-full bg-red-500 shadow-[0_0_10px_#ef4444]"></span>
                        <span class="text-xs font-semibold tracking-wider text-red-500 uppercase">Reverb Offline</span>
                    </div>
                </template>
            </div>
        </div>
    </nav>

    <!-- Dashboard Content -->
    <main class="pt-28 pb-12 px-8 max-w-[1600px] mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 min-h-screen">
        
        <!-- Left Column: Video Feed (Spans 8 cols) -->
        <div class="lg:col-span-8 flex flex-col h-full">
            <div class="bg-[#1c1c1e] border border-white/10 rounded-[24px] overflow-hidden shadow-2xl flex flex-col flex-grow">
                <!-- Video Header -->
                <div class="px-6 py-5 border-b border-white/5 bg-white/5 flex justify-between items-center">
                    <h2 class="text-sm font-semibold text-[#f9f9fb] uppercase tracking-[0.1em]">Outpatient Triage Camera 01</h2>
                    <span class="text-xs font-mono text-[#0058bc] bg-[#0058bc]/10 px-2 py-1 rounded-full border border-[#0058bc]/20">ws://127.0.0.1:5001</span>
                </div>
                
                <!-- WebSocket Stream Container -->
                <div class="relative w-full flex-grow bg-black flex items-center justify-center overflow-hidden"
                     x-data="{
                        ws: null,
                        streamActive: false,
                        init() {
                            this.connect();
                        },
                        connect() {
                            this.ws = new WebSocket('ws://127.0.0.1:5001/ws/video_feed');
                            this.ws.onopen = () => { this.streamActive = true; };
                            this.ws.onmessage = (event) => {
                                if (event.data instanceof Blob) {
                                    const url = URL.createObjectURL(event.data);
                                    if (this.$refs.videoFeed.src && this.$refs.videoFeed.src.startsWith('blob:')) {
                                        URL.revokeObjectURL(this.$refs.videoFeed.src);
                                    }
                                    this.$refs.videoFeed.src = url;
                                }
                            };
                            this.ws.onclose = () => { this.streamActive = false; setTimeout(() => this.connect(), 2000); };
                            this.ws.onerror = () => { this.streamActive = false; this.ws.close(); };
                        }
                     }">
                     
                    <!-- Offline State -->
                    <div x-show="!streamActive" class="absolute inset-0 flex flex-col items-center justify-center text-[#a0a0a5] z-10 bg-[#1c1c1e]">
                        <svg class="w-12 h-12 mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"></path>
                        </svg>
                        <span class="font-medium tracking-wide">Stream Offline</span>
                        <span class="text-xs mt-1 opacity-70">Initialize CV Engine on Port 5001</span>
                    </div>

                    <!-- Online Feed -->
                    <img 
                        x-show="streamActive"
                        x-ref="videoFeed"
                        alt="Zero-Latency CV Stream Feed" 
                        class="w-full h-full object-cover opacity-90 transition-opacity duration-500"
                    />
                </div>
            </div>
        </div>

        <!-- Right Column: Telemetry Dashboard Island (Spans 4 cols) -->
        <div class="lg:col-span-4 flex flex-col h-full">
            <livewire:dashboard.telemetry-dashboard />
        </div>
    </main>
</div>
