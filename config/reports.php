<?php

return [
    /*
    |--------------------------------------------------------------------------
    | Report Delivery Modes
    |--------------------------------------------------------------------------
    |
    | Here you may specify the delivery modes for the nightly generated
    | capacity reports. Available options: 'download', 'local', 'email'.
    | The modes should be specified as a comma-separated list.
    |
    */

    'modes' => explode(',', env('REPORT_MODES', 'download')),

    /*
    |--------------------------------------------------------------------------
    | Report Email Address
    |--------------------------------------------------------------------------
    |
    | The email address that the automated reports will be sent to if
    | the 'email' mode is enabled in the configuration.
    |
    */

    'email' => env('REPORT_EMAIL', 'admin@example.com'),
];
