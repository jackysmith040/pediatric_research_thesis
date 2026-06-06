<?php

namespace App\Livewire;

use Livewire\Attributes\Title;
use Livewire\Component;

#[Title('The Invisible Child')]
class LandingPage extends Component
{
    public function render()
    {
        return view('livewire.landing-page')
            ->layout('components.layouts.app', [
                'description' => 'We act as an unsleeping eye, counting and tracking every pediatric patient to ensure no child is forgotten.',
            ]);
    }
}
