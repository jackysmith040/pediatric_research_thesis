<?php

namespace App\Restify;

use App\Events\TelemetryReceived;
use App\Models\TrafficLog;
use Binaryk\LaravelRestify\Fields\Id;
use Binaryk\LaravelRestify\Http\Requests\RestifyRequest;
use Binaryk\LaravelRestify\Repositories\Repository;
use Illuminate\Support\Facades\Event;

class TrafficLogRepository extends Repository
{
    public static string $model = TrafficLog::class;

    public function fields(RestifyRequest $request): array
    {
        return [
            Id::make('id'),
            field('camera_id')->rules('required', 'string'),
            field('current_adults')->rules('required', 'integer'),
            field('current_children')->rules('required', 'integer'),
            field('total_daily_adults')->rules('required', 'integer'),
            field('total_daily_children')->rules('required', 'integer'),
            field('overcrowding_alert')->rules('required', 'boolean'),
        ];
    }

    public static function stored(RestifyRequest $request, $repository)
    {
        // Broadcast the telemetry event via Reverb WebSockets
        broadcast(new TelemetryReceived($repository->model()->toArray()))->toOthers();
    }
}
