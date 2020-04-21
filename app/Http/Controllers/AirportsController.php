<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;

class AirportsController extends Controller
{
    public static function insertURL($json, $airport)
    {
        // Get airport_id: it depends of the iata and the country
        $json['airport_id'] = DB::table('airports')
            ->select('airports.id')
            ->join('cities as c', 'c.id', '=', 'airports.city_id')
            ->join ('countries as co', 'c.country_id', '=', 'co.id')
            ->where('iata', $json['airport_id'])
            ->where('co.name', $airport)
            ->first()->id;

        DB::table('airports')->where('id', $json['airport_id'])
            ->update(array('airport_url' => $json['airport_url']));
    }

    public static function getAirportURL($airport_id)
    {
        $url = DB::table('airports')
            ->select('airport_url')
            ->where('id', $airport_id)->first();
        if (is_null($url)){
            return null;
        } else {
            return $url->airport_url;
        }
    }
}
