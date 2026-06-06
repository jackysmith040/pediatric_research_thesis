<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ $title ?? 'Pediatric Dashboard' }}</title>
        
        <!-- Fonts -->
        <link rel="preconnect" href="https://fonts.bunny.net">
        <link href="https://fonts.bunny.net/css?family=manrope:400,500,600,700|noto-serif:400,700" rel="stylesheet" />
        
        <!-- Livewire Styles/Scripts -->
        @livewireStyles
        
        <!-- Vite Assets -->
        @vite(['resources/css/app.css', 'resources/js/app.js'])
    </head>
    <body class="antialiased bg-[#0e0e0e] text-white selection:bg-indigo-500/30">
        {{ $slot }}
        @livewireScripts
        
        <!-- Fire Alpine Events for Echo Connection Status -->
        <script>
            document.addEventListener('DOMContentLoaded', () => {
                if (window.Echo) {
                    window.Echo.connector.pusher.connection.bind('connected', () => {
                        window.dispatchEvent(new Event('echo-connected'));
                    });
                    window.Echo.connector.pusher.connection.bind('disconnected', () => {
                        window.dispatchEvent(new Event('echo-disconnected'));
                    });
                }
            });
        </script>
    </body>
</html>
