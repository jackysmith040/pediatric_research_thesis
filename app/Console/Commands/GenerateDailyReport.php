<?php

namespace App\Console\Commands;

use App\Services\ReportGenerator;
use Illuminate\Console\Command;

class GenerateDailyReport extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'report:generate {--mode= : Comma-separated override modes}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Generate the daily capacity PDF report';

    /**
     * Execute the console command.
     */
    public function handle(ReportGenerator $generator)
    {
        $this->info('Generating daily report...');

        $modeOverride = $this->option('mode');
        $modes = $modeOverride ? explode(',', $modeOverride) : null;

        $generator->generate($modes);

        $this->info('Report generation completed successfully.');
    }
}
