<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');

Route::post('/telemetry', function (Request $request) {
    $log = \App\Models\TrafficLog::create([
        'camera_id' => $request->camera_id,
        'current_adults' => $request->current_adults,
        'current_children' => $request->current_children,
        'total_daily_adults' => $request->total_daily_adults,
        'total_daily_children' => $request->total_daily_children,
        'overcrowding_alert' => $request->overcrowding_alert,
    ]);
    
    broadcast(new \App\Events\TelemetryReceived($log->toArray()))->toOthers();
    return response()->json(['status' => 'success']);
});
