<?php

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @return void
     */
    public function run()
    {
        // $this->call(UsersTableSeeder::class);
        $this->call(FlightStatusSeeder::class);
        $this->call(AlgorithmsSeeder::class);
        $this->call(RolesTableSeeder::class);
        $this->call(CountriesTableSeeder::class);
        $this->call(CitiesTableSeeder::class);
        $this->call(WindDirectionsTableSeeder::class);
        $this->call(AirlinesTableSeeder::class);
        $this->call(AirportsTableSeeder::class);
    }
}
