<?php

namespace App\Models\Fligths;

use Illuminate\Database\Eloquent\Model;

class Airport extends Model
{
    protected $fillable = [
        'id', 'name', 'city_id', 'iata', 'icao', 'latitude','longitude', 'altitude','timezone','dst','tz'
    ];

    // disable timestamps created_at & updated_at
    public $timestamps = false;
}
