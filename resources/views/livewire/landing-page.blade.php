<div class="bg-[#1c1c1e] text-[#f9f9fb] font-['Inter'] min-h-screen relative w-full selection:bg-[#0058bc]/30">
    
    <!-- Background Elements Container (Fixes double scrollbars) -->
    <div class="fixed inset-0 w-full h-full overflow-hidden pointer-events-none z-0">
        <div class="absolute top-[-20%] left-[-10%] w-[50vw] h-[50vw] bg-[#0058bc] rounded-full mix-blend-screen filter blur-[150px] opacity-20 animate-pulse"></div>
        <div class="absolute bottom-[-20%] right-[-10%] w-[60vw] h-[60vw] bg-[#adc6ff] rounded-full mix-blend-screen filter blur-[150px] opacity-10"></div>
    </div>

    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">

    <!-- Navbar -->
    <nav class="w-full fixed top-0 z-50 px-6 py-6 transition-all duration-300" data-aos="fade-down" data-aos-duration="1000">
        <div class="max-w-7xl mx-auto flex justify-between items-center bg-[#1c1c1e]/40 backdrop-blur-[24px] border border-white/5 rounded-full px-6 py-3">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-[#0058bc] flex items-center justify-center shadow-[0_0_15px_rgba(0,88,188,0.3)]">
                    <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                </div>
                <span class="text-sm font-semibold tracking-wide text-white">The Invisible Child</span>
            </div>
            <a href="/dashboard" wire:navigate class="px-5 py-2 rounded-full bg-white text-[#1c1c1e] font-semibold text-xs tracking-wide hover:scale-105 hover:bg-[#f3f3f5] transition-all duration-300">
                Command Center
            </a>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="relative z-10 w-full flex flex-col items-center">
        
        <!-- Act 1: The Problem -->
        <section class="w-full min-h-screen flex flex-col items-center justify-center px-6 pt-20">
            <div class="max-w-4xl text-center flex flex-col items-center">
                <span data-aos="fade-up" data-aos-duration="1000" class="text-xs font-semibold tracking-[0.2em] uppercase text-[#0058bc] mb-6 block">
                    The Reality of the ER
                </span>
                
                <h1 data-aos="fade-up" data-aos-duration="1200" data-aos-delay="100" class="text-6xl md:text-8xl font-bold tracking-tighter text-white mb-8 leading-[1.1]">
                    Small. Quiet.<br>
                    <span class="text-transparent bg-clip-text bg-gradient-to-r from-white to-[#717786]">Easily Lost.</span>
                </h1>
                
                <p data-aos="fade-up" data-aos-duration="1200" data-aos-delay="200" class="text-lg md:text-xl text-[#a0a0a5] max-w-2xl font-light leading-relaxed mb-12">
                    In the chaos of an overcrowded waiting room, the most vulnerable patients are the hardest to track. When pediatric loads spike, traditional systems fail to adapt. They become invisible.
                </p>

                <div data-aos="fade-up" data-aos-duration="1200" data-aos-delay="300">
                    <a href="#act-2" class="w-12 h-12 rounded-full border border-white/10 flex items-center justify-center hover:bg-white/5 transition-colors duration-300">
                        <svg class="w-5 h-5 text-white/50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                        </svg>
                    </a>
                </div>
            </div>
        </section>

        <!-- Act 2: The Solution -->
        <section id="act-2" class="w-full min-h-screen flex flex-col items-center justify-center px-6 border-t border-white/5 bg-[#1a1c1d]/50">
            <div class="max-w-6xl w-full grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
                
                <div data-aos="fade-right" data-aos-duration="1200" class="order-2 md:order-1">
                    <div class="relative w-full aspect-[4/3] rounded-[24px] bg-[#1c1c1e] border border-white/10 overflow-hidden shadow-2xl flex items-center justify-center">
                        <!-- Abstract representation of the AI eye -->
                        <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-[#0058bc]/20 via-transparent to-transparent"></div>
                        <div class="relative w-32 h-32 rounded-full border border-[#0058bc]/40 flex items-center justify-center animate-[spin_10s_linear_infinite]">
                            <div class="w-24 h-24 rounded-full border border-[#0058bc]/60 border-t-transparent animate-[spin_5s_linear_infinite_reverse]"></div>
                            <div class="absolute w-2 h-2 rounded-full bg-[#adc6ff] shadow-[0_0_10px_#adc6ff]"></div>
                        </div>
                    </div>
                </div>

                <div data-aos="fade-left" data-aos-duration="1200" class="order-1 md:order-2 flex flex-col justify-center">
                    <span class="text-xs font-semibold tracking-[0.2em] uppercase text-[#0058bc] mb-6 block">
                        The Solution
                    </span>
                    <h2 class="text-4xl md:text-5xl font-bold tracking-tight text-white mb-6 leading-tight">
                        An unsleeping eye.
                    </h2>
                    <p class="text-[#a0a0a5] text-lg font-light leading-relaxed mb-8">
                        Our decoupled Zero-Latency Architecture streams raw video at 30 FPS while an underlying YOLOv8 neural network instantly tracks and classifies every individual in the frame.
                    </p>
                    <ul class="space-y-4">
                        <li class="flex items-start gap-4">
                            <span class="w-1.5 h-1.5 rounded-full bg-[#0058bc] mt-2.5"></span>
                            <span class="text-[#f9f9fb] text-sm leading-relaxed"><strong>Islands of Data:</strong> Livewire isolates telemetry streams, protecting the UI from freezing.</span>
                        </li>
                        <li class="flex items-start gap-4">
                            <span class="w-1.5 h-1.5 rounded-full bg-[#0058bc] mt-2.5"></span>
                            <span class="text-[#f9f9fb] text-sm leading-relaxed"><strong>Decoupled Inference:</strong> Neural networks process in parallel, allowing the video feed to remain flawlessly smooth.</span>
                        </li>
                    </ul>
                </div>
            </div>
        </section>

        <!-- Act 3: The Impact -->
        <section class="w-full min-h-[80vh] flex flex-col items-center justify-center px-6 border-t border-white/5">
            <div class="max-w-4xl text-center flex flex-col items-center">
                <span data-aos="fade-up" data-aos-duration="1000" class="text-xs font-semibold tracking-[0.2em] uppercase text-[#0058bc] mb-6 block">
                    The Impact
                </span>
                
                <h2 data-aos="fade-up" data-aos-duration="1200" data-aos-delay="100" class="text-5xl md:text-7xl font-bold tracking-tighter text-white mb-8">
                    No child forgotten.
                </h2>
                
                <p data-aos="fade-up" data-aos-duration="1200" data-aos-delay="200" class="text-lg md:text-xl text-[#a0a0a5] max-w-2xl font-light leading-relaxed mb-12">
                    Staff are proactively alerted before the pediatric threshold is reached. Daily capacity aggregates are multimodally generated. We remove the cognitive load so you can focus on saving lives.
                </p>

                <div data-aos="fade-up" data-aos-duration="1200" data-aos-delay="300">
                    <a href="/dashboard" wire:navigate class="px-8 py-4 rounded-full bg-white text-[#1c1c1e] font-semibold text-sm hover:scale-105 transition-all duration-300 shadow-[0_0_20px_rgba(255,255,255,0.15)]">
                        Launch The Command Center
                    </a>
                </div>
            </div>
        </section>

    </main>

    <footer class="w-full text-center py-12 text-[#717786] text-xs font-medium tracking-[0.15em] uppercase border-t border-white/5 relative z-10">
        The Invisible Child &bull; Pediatric Intelligence
    </footer>

    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            AOS.init({ once: true });
        });
        document.addEventListener('livewire:navigated', function() {
            AOS.init({ once: true });
        });
    </script>
</div>
