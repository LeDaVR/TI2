package com.ti2.horario.horario

import android.content.Context
import android.os.Environment
import android.util.Log
import com.ti2.horario.Object
import okhttp3.OkHttpClient
import okhttp3.Response
import java.io.*


class Dowloader : Object{
    var ext: String? = null
    constructor(context: Context, client: OkHttpClient, handler: android.os.Handler)
            : super(context,client,handler) {}

    fun setExtension(extension: String){
        this.ext = extension
    }

    fun download(url: String){
        call(url,"")
    }

    override fun onResponse(link: String, response: Response) {
        try {
            var count = 0
            Log.e("dowload",link)
            var open: InputStream = response.body!!.byteStream()
            var directory = File(Environment.DIRECTORY_DOWNLOADS)
            var file_name = "horario."+ext
            directory.mkdirs()
            var outputfile = File(Environment.getExternalStorageDirectory().toString()+"/"+Environment.DIRECTORY_DOWNLOADS,file_name)

            var fos = FileOutputStream(outputfile)
            open.copyTo(fos)
            fos.close()
        }
        catch (io: IOException){
            io.printStackTrace()
        }
    }

}