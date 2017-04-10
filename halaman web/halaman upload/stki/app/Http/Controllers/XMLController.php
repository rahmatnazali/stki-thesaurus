<?php

namespace App\Http\Controllers;

use App\XML;
use Illuminate\Http\Request;

use App\Http\Requests;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Input;
use Carbon\Carbon;
use Illuminate\Support\Facades\Session;

class XMLController extends Controller
{
    public function upload(){
        return view("pages.xml.upload");
    }

    public function xmlupload(){
        $nrp = Input::get('nrp');
        $file = Input::file('fileToUpload');
        if($file->getClientOriginalExtension() == 'xml'){
            $destinationPath = 'xmllistfileupload'; // upload path
            $fileName = $file->getClientOriginalName(); // renameing image
            $file->move($destinationPath, $fileName); // uploading file to given path
            $contents = File::get($destinationPath."/".$fileName);
            $contents = str_replace("\n","",$contents);
            $contents = str_replace("\t","",$contents);
            $xml=simplexml_load_string($contents);
            if($xml->tanggal != "" && $xml->judul != "" && $xml->kata_kunci != "" && $xml->isi != "" && $xml->link != "" && $xml->id != ""){
                $date = explode("/",$xml->tanggal);
                $date = Carbon::create("20".$date[2], $date[1], $date[0], 0);
                $insert = new XML();
                $insert->judul_artikel = $xml->judul;
                $insert->tanggal_artikel = $date;
                $insert->kata_kunci_artikel = $xml->kata_kunci;
                $insert->isi_artikel = $xml->isi;
                $insert->link_artikel = $xml->link;
                $insert->nama_file = $xml->id;
                $insert->nrp_pengunggah = $nrp;
                $insert->save();
                Session::flash('notif','Berhasil Upload');
            } else {
                Session::flash('notif','Gagal Upload, Isi XML tidak lengkap');
            }
        } else {
            Session::flash('notif','Gagal Upload, Dokumen tidak diketahui');
        }
        return redirect()->to("/#notif");
    }
}
