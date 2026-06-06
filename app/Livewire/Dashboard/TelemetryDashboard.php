<?php

namespace App\Livewire\Dashboard;

use App\Models\TrafficLog;
use App\Services\ReportGenerator;
use Illuminate\View\View;
use Livewire\Attributes\Isolate;
use Livewire\Attributes\On;
use Livewire\Component;

#[Isolate]
class TelemetryDashboard extends Component
{
    public int $currentAdults = 0;

    public int $currentChildren = 0;

    public int $totalDailyAdults = 0;

    public int $totalDailyChildren = 0;

    public bool $overcrowdingAlert = false;

    public function mount(): void
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
    public function updateMetrics(array $payload): void
    {
        $data = $payload['payload'] ?? $payload;
        
        $this->currentAdults = $data['current_adults'] ?? $this->currentAdults;
        $this->currentChildren = $data['current_children'] ?? $this->currentChildren;
        $this->totalDailyAdults = $data['total_daily_adults'] ?? $this->totalDailyAdults;
        $this->totalDailyChildren = $data['total_daily_children'] ?? $this->totalDailyChildren;
        $this->overcrowdingAlert = $data['overcrowding_alert'] ?? $this->overcrowdingAlert;
    }

    public function downloadReport(ReportGenerator $generator)
    {
        return $generator->generate(['download']);
    }

    public function render(): View
    {
        return view('livewire.dashboard.telemetry-dashboard');
    }
}
