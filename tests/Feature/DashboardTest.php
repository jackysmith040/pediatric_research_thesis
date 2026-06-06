<?php

use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

test('landing page loads successfully', function () {
    $response = $this->get('/');
    $response->assertStatus(200);
});

test('dashboard loads successfully and contains the wait room monitor', function () {
    $response = $this->get('/dashboard');

    $response->assertStatus(200);
    $response->assertSeeLivewire('dashboard.wait-room-monitor');
});
