<?php

use App\Livewire\Dashboard\WaitRoomMonitor;
use App\Livewire\LandingPage;
use Illuminate\Support\Facades\Route;

Route::livewire('/', LandingPage::class);
Route::livewire('/dashboard', WaitRoomMonitor::class);
