<?php

namespace App\Console\Commands;

use App\Models\TrafficLog;
use Barryvdh\DomPDF\Facade\Pdf;
use Carbon\Carbon;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Storage;

class GenerateDailyPediatricReport extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'report:daily-pediatric';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Generates an automated end-of-day PDF analytical report for pediatric capacity logs.';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $today = Carbon::today();

        $logs = TrafficLog::whereDate('created_at', $today)->get();

        if ($logs->isEmpty()) {
            $this->info('No traffic logs found for today. Skipping report.');

            return;
        }

        $peakHourlyVolume = $logs->max('current_children');
        $averageCount = $logs->avg('current_children');
        $latestLog = $logs->last();

        $data = [
            'date' => $today->format('Y-m-d'),
            'total_children' => $latestLog->total_daily_children,
            'total_adults' => $latestLog->total_daily_adults,
            'peak_children' => $peakHourlyVolume,
            'avg_children' => round($averageCount, 1),
            'alert_count' => $logs->where('overcrowding_alert', true)->count(),
        ];

        // Ensure we have a rudimentary view for the PDF
        // Note: For production, we would use a dedicated Blade template.
        $html = '<h1>Pediatric Daily Capacity Report</h1>';
        $html .= "<p>Date: {$data['date']}</p>";
        $html .= '<ul>';
        $html .= "<li>Total Children: {$data['total_children']}</li>";
        $html .= "<li>Total Adults: {$data['total_adults']}</li>";
        $html .= "<li>Peak Concurrent Children: {$data['peak_children']}</li>";
        $html .= "<li>Average Concurrent Children: {$data['avg_children']}</li>";
        $html .= "<li>Overcrowding Alerts Triggered: {$data['alert_count']}</li>";
        $html .= '</ul>';

        $pdf = Pdf::loadHTML($html);

        $filename = "reports/pediatric_report_{$data['date']}.pdf";
        Storage::put($filename, $pdf->output());

        $this->info("Report generated successfully at {$filename}");
    }
}
