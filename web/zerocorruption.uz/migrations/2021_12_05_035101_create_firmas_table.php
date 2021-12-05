<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateFirmasTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('firmas', function (Blueprint $table) {
            $table->id();
            $table->string('inn');
            // firma nomi
            $table->unsignedBigInteger('fnomid');
            $table->foreign('fnomid')->references('id')->on('firma_noms');
            // rahbar fish
            $table->unsignedBigInteger('rnomid');
            $table->foreign('rnomid')->references('id')->on('rahbars');
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
        Schema::dropIfExists('firmas');
    }
}
