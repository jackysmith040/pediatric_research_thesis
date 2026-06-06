# 🏛️ Laravel Backend Architecture

Welcome to the **Laravel Command Center**! This is the web application that Hospital Administrators look at.

## What is it?
The backend is built on **Laravel 13** and **Livewire 4**. It serves as the data ingestion hub and the real-time UI provider.

## How it works (The Data Flow)
1. **The API (`routes/api.php` & `TelemetryController.php`):**
   The Python CV Engine hits the `POST /api/telemetry` endpoint every 3 seconds. The `TelemetryController` validates this data using `StoreTelemetryRequest.php`.
2. **Database (`TrafficLog.php`):**
   Once validated, the data is saved to a SQLite database. This creates a permanent historical log so we can generate reports at the end of the day.
3. **Broadcasting (`TelemetryReceived.php`):**
   Immediately after saving to the database, the Controller fires a `TelemetryReceived` event. This event implements `ShouldBroadcastNow`, meaning Laravel instantly throws this data over to the Reverb WebSocket server.
4. **Livewire Frontend (`TelemetryDashboard.php`):**
   The `telemetry-dashboard.blade.php` file is listening to the Reverb WebSocket using the `#[On('echo:telemetry,TelemetryReceived')]` PHP attribute. The moment data flies through the socket, Livewire updates the HTML numbers on the screen without the user having to refresh the page!

## Livewire Islands (`#[Isolate]`)
Livewire normally updates the entire page when state changes. Because our telemetry data updates every 3 seconds, updating the whole page would cause the MJPEG video feed to flicker constantly.
To fix this, we put `#[Isolate]` on the `TelemetryDashboard` component. This turns the telemetry card into an isolated "Island". It updates itself independently without touching the rest of the HTML.

---

### 🧸 Explain Like I'm 5 (ELI5)
Imagine the Laravel Backend is a giant Post Office.
The Python CV Engine is a mailman who drops off a letter every 3 seconds. 
The API is the clerk who checks if the letter has a stamp.
The Database is the filing cabinet where a copy of the letter is saved forever.
The WebSocket is a massive loudspeaker on the roof of the post office. The moment the letter is filed, the loudspeaker shouts the contents of the letter.
The Livewire Frontend is a person standing in the street listening to the loudspeaker, writing the numbers on a chalkboard for everyone to see.

---

### 👩‍💻 How to Contribute
If you want to add a new database table (e.g., `doctors_on_duty`), you would use Laravel Artisan: `php artisan make:model Doctor -m`. Then you would create a new Livewire component (`php artisan make:livewire DoctorList`) to display them on the dashboard!
