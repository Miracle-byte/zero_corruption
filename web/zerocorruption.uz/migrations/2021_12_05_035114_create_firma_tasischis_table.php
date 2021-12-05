<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateFirmaTasischisTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('firma_tasischis', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('fid');
            $table->foreign('fid')->references('id')->on('firmas');
            $table->unsignedBigInteger('tid');
            $table->foreign('tid')->references('id')->on('tasischis');
            $table->string('ulush');
            //$table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('firma_tasischis');
    }
}
