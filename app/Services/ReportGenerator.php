<?php

namespace App\Services;

use App\Models\TrafficLog;
use Barryvdh\DomPDF\Facade\Pdf;
use Carbon\Carbon;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Storage;

class ReportGenerator
{
    /**
     * Generate the report based on configured modes.
     *
     * @param  array|null  $modes  Provide modes to override config (e.g. ['download'])
     * @return mixed
     */
    public function generate(?array $modes = null)
    {
        $modes = $modes ?? config('reports.modes', ['download']);

        // Fetch data for today
        $today = Carbon::today();
        $logs = TrafficLog::whereDate('created_at', $today)->get();

        $latest = $logs->last();
        $totalAdults = $latest ? $latest->total_daily_adults : 0;
        $totalChildren = $latest ? $latest->total_daily_children : 0;

        $peakAdults = $logs->max('current_adults') ?? 0;
        $peakChildren = $logs->max('current_children') ?? 0;
        $alertsCount = $logs->where('overcrowding_alert', true)->count();

        $data = [
            'date' => $today->format('F j, Y'),
            'totalAdults' => $totalAdults,
            'totalChildren' => $totalChildren,
            'peakAdults' => $peakAdults,
            'peakChildren' => $peakChildren,
            'alertsCount' => $alertsCount,
        ];

        $pdf = Pdf::loadView('pdf.daily-capacity', $data);
        $filename = 'capacity-report-'.$today->format('Y-m-d').'.pdf';

        $output = $pdf->output();

        if (in_array('local', $modes)) {
            Storage::disk('local')->put("reports/{$filename}", $output);
            Log::info("Daily capacity report saved to local storage: {$filename}");
        }

        if (in_array('email', $modes)) {
            $email = config('reports.email', 'admin@example.com');
            Mail::raw("Attached is the daily capacity report for {$data['date']}.", function ($message) use ($email, $output, $filename) {
                $message->to($email)
                    ->subject("Daily Capacity Report - {$filename}")
                    ->attachData($output, $filename, ['mime' => 'application/pdf']);
            });
            Log::info("Daily capacity report emailed to {$email}");
        }

        if (in_array('download', $modes)) {
            return response()->streamDownload(function () use ($output) {
                echo $output;
            }, $filename, ['Content-Type' => 'application/pdf']);
        }

        return true;
    }
}
