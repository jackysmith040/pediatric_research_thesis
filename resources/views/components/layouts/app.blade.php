<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ $title ?? 'Pediatric Dashboard' }}</title>
        
        <!-- Fonts -->
        <link rel="preconnect" href="https://fonts.bunny.net">
        <link href="https://fonts.bunny.net/css?family=manrope:400,500,600,700|noto-serif:400,700" rel="stylesheet" />
        
        <!-- Tailwind CDN for MVP (Bypass NPM requirement) -->
        <script src="https://cdn.tailwindcss.com"></script>
        
        <!-- Livewire Styles/Scripts -->
        @livewireStyles
    </head>
    <body class="antialiased bg-[#0e0e0e] text-white selection:bg-indigo-500/30">
        {{ $slot }}
        @livewireScripts
    </body>
</html>
