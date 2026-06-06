<?php

namespace App\Livewire\Dashboard;

use Illuminate\View\View;
use Livewire\Attributes\Layout;
use Livewire\Component;

#[Layout('components.layouts.app')]
class WaitRoomMonitor extends Component
{
    public function render(): View
    {
        return view('livewire.dashboard.wait-room-monitor');
    }
}
