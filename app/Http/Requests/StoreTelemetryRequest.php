<?php

namespace App\Http\Requests;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Foundation\Http\FormRequest;

class StoreTelemetryRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true; // Webhook from internal system, allowing all for MVP
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'camera_id' => ['required', 'string', 'max:255'],
            'current_adults' => ['required', 'integer', 'min:0'],
            'current_children' => ['required', 'integer', 'min:0'],
            'total_daily_adults' => ['required', 'integer', 'min:0'],
            'total_daily_children' => ['required', 'integer', 'min:0'],
            'overcrowding_alert' => ['required', 'boolean'],
        ];
    }
}
