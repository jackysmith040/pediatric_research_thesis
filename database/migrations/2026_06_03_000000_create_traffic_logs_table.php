<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('traffic_logs', function (Blueprint $table) {
            $table->id();
            $table->string('camera_id');
            $table->integer('current_adults')->default(0);
            $table->integer('current_children')->default(0);
            $table->integer('total_daily_adults')->default(0);
            $table->integer('total_daily_children')->default(0);
            $table->boolean('overcrowding_alert')->default(false);
            $table->timestamp('recorded_at')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('traffic_logs');
    }
};
