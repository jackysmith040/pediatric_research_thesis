<?php

namespace App\Http\Controllers\Api;

use App\Events\TelemetryReceived;
use App\Http\Controllers\Controller;
use App\Http\Requests\StoreTelemetryRequest;
use App\Models\TrafficLog;

class TelemetryController extends Controller
{
    /**
     * Store a newly created resource in storage.
     */
    public function store(StoreTelemetryRequest $request)
    {
        $log = TrafficLog::create($request->validated());

        try {
            event(new TelemetryReceived($log->toArray()));
        } catch (\Exception $e) {
            \Illuminate\Support\Facades\Log::warning('Telemetry broadcast failed (Reverb offline): ' . $e->getMessage());
        }

        return response()->json(['status' => 'success']);
    }
}
