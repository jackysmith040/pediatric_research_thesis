<?php

namespace App\Livewire\Dashboard;

use Livewire\Component;
use Livewire\Attributes\On;
use Livewire\Attributes\Layout;
use App\Models\TrafficLog;

#[Layout('components.layouts.app')]
class WaitRoomMonitor extends Component
{
    public int $currentAdults = 0;
    public int $currentChildren = 0;
    public int $totalDailyAdults = 0;
    public int $totalDailyChildren = 0;
    public bool $overcrowdingAlert = false;

    public function mount()
    {
        $this->loadLatestData();
    }

    public function loadLatestData()
    {
        $latest = TrafficLog::latest('id')->first();
        if ($latest) {
            $this->currentAdults = $latest->current_adults;
            $this->currentChildren = $latest->current_children;
            $this->totalDailyAdults = $latest->total_daily_adults;
            $this->totalDailyChildren = $latest->total_daily_children;
            $this->overcrowdingAlert = $latest->overcrowding_alert;
        }
    }

    #[On('echo:telemetry,TelemetryReceived')]
    public function updateMetrics($payload)
    {
        // Reverb pushes the updated payload via WebSocket
        $this->currentAdults = $payload['current_adults'] ?? $this->currentAdults;
        $this->currentChildren = $payload['current_children'] ?? $this->currentChildren;
        $this->totalDailyAdults = $payload['total_daily_adults'] ?? $this->totalDailyAdults;
        $this->totalDailyChildren = $payload['total_daily_children'] ?? $this->totalDailyChildren;
        $this->overcrowdingAlert = $payload['overcrowding_alert'] ?? $this->overcrowdingAlert;
    }

    public function render()
    {
        return view('livewire.dashboard.wait-room-monitor');
    }
}
