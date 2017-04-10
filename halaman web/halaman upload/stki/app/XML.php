<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class XML extends Model
{
    protected $table = 'artikel';
    protected $primaryKey = 'id_artikel';
    public $timestamps = true;
    public $incrementing = true;
    protected $fillable = array(
        'nama_file',
        'judul_artikel',
        'tanggal_artikel',
        'keterangan_artikel',
        'kata_kunci_artikel',
        'topik_artikel',
        'lokasi_artikel',
        'penulis_artikel',
        'editor_artikel',
        'isi_artikel',
        'link_artikel',
        'kelompok_pengunggah',
        'nrp_pengunggah'
    );
}
