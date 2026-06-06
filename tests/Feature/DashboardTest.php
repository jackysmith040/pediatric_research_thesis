<?php

test('dashboard loads successfully', function () {
    $response = $this->get('/');
    
    $response->assertStatus(200);
});

test('dashboard contains the wait room monitor component', function () {
    $response = $this->get('/');
    
    $response->assertSeeLivewire('dashboard.wait-room-monitor');
});
