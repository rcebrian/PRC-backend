<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateUsersTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('users', function (Blueprint $table) {
            $table->increments('id');
            $table->string('name');
            $table->string('surname');
            $table->string('dni')->unique();
            $table->string('phoneNumber');
            $table->string('email')->unique();
            $table->integer('role')->unsigned();
            $table->foreign('role')->references('id')->on('roles');
            $table->string('flight_id');
            $table->dateTime('date');
            $table->foreign(array('flight_id', 'date'))->references(array('id', 'date'))->on('flights');

        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('users');
    }
}
