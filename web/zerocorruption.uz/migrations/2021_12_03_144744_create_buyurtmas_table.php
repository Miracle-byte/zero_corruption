<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateBuyurtmasTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('buyurtmas', function (Blueprint $table) {
            $table->id();
            $table->string('turi');
            $table->integer('lotnum');
            $table->date('start_date');
            $table->dateTime('end_datetime');
            $table->integer('count');
            $table->string('nom');
            $table->bigInteger('start_narx');
            $table->bigInteger('end_narx');
            $table->text('zakazchik');
            $table->string('zakazchik_inn');
            $table->unsignedBigInteger('glid');
            $table->foreign('glid')->references('id')->on('golibs');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('buyurtmas');
    }
}
