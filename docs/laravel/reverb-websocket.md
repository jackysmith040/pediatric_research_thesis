# ⚡ Reverb WebSockets Explained

## What is Laravel Reverb?
In the old days of the internet, if you wanted to know if data changed on a server, your web browser had to constantly refresh the page or ask the server "Any updates? Any updates? Any updates?" every second (Polling). This is incredibly slow and wastes bandwidth.

**WebSockets** solve this. A WebSocket is an open, continuous tunnel between the user's browser and the server. When the server has new data, it simply pushes it down the tunnel to the browser instantly.

**Laravel Reverb** is a first-party WebSocket server built entirely in PHP. It replaces expensive third-party services like Pusher.

## How we use Reverb in this project
1. Reverb runs on port `8080` (started via `php artisan reverb:start`).
2. The browser loads `echo.js` (Laravel Echo) and connects to `ws://127.0.0.1:8080`.
3. When the `TelemetryController` receives data, it tells Laravel to broadcast it.
4. Laravel sends the data to Reverb.
5. Reverb pushes the data down the open tunnel to the browser.
6. The `TelemetryDashboard` Livewire component catches it and updates the screen.

## The Graceful Degradation (Offline Mode)
What if you forget to start Reverb, or it crashes?
In `wait-room-monitor.blade.php`, we use Alpine.js to listen to the actual heartbeat of the WebSocket.
```html
<div x-data="{ echoConnected: false }"
     @echo-connected.window="echoConnected = true"
     @echo-disconnected.window="echoConnected = false"
     x-on:error.window="echoConnected = false">
```
If the tunnel collapses, `echoConnected` instantly becomes `false`, and the UI swaps the glowing green "Reverb Live" dot to a red "Reverb Offline" badge. Meanwhile, the backend API uses a `try-catch` block so it doesn't crash when Reverb is unreachable.

---

### 🧸 Explain Like I'm 5 (ELI5)
Imagine you are waiting for a very important phone call.
**Polling (The Old Way):** You pick up the phone every 5 seconds, call your friend, ask "Anything new?", hang up, and repeat.
**WebSockets (Reverb):** You call your friend, and *neither of you hangs up the phone*. You just leave the phone on speaker on your desk. When your friend has news, they just talk into the phone, and you hear it instantly.
The "Reverb Offline" badge is just a little red light that turns on if the phone cord gets unplugged!

---

### 👩‍💻 How to Contribute
If you want to add a feature where nurses can type a message in the dashboard and broadcast it to all other computers in the hospital, you would create a new Laravel Event (e.g., `NurseMessageSent`), have it implement `ShouldBroadcastNow`, and use Reverb to push it to a new Livewire component!
