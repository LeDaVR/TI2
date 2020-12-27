package com.ti2.horario.horario

import android.Manifest
import android.app.DownloadManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.os.Handler
import android.util.Log
import android.view.Menu
import android.view.MenuInflater
import android.view.MenuItem
import android.widget.TableLayout
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.Toolbar
import androidx.core.app.ActivityCompat
import com.google.android.material.tabs.TabLayout
import com.ti2.horario.Global
import com.ti2.horario.R
import com.ti2.horario.login.LoginActivity
import com.ti2.horario.login.SessionManagement
import okhttp3.OkHttpClient


class ActivityHorario : AppCompatActivity() {

    val client = OkHttpClient()
    var handler: Handler = Handler()
    var toolbar: Toolbar? = null
    var dowloader: Dowloader? = null
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.horario)
        init()
    }

    fun init()
    {
        dowloader = Dowloader(this@ActivityHorario,client,handler)

        var bar = findViewById<TabLayout>(R.id.aulas)
        var aulas = Aulas(this@ActivityHorario, client, handler, bar)

        var tableLayout = findViewById<TableLayout>(R.id.horario_table)
        var tableHorario = TablaHorario(this@ActivityHorario, client, handler, tableLayout)

        aulas.link(tableHorario)

        toolbar = findViewById<Toolbar>(R.id.toolbar)
        setSupportActionBar(toolbar)
        supportActionBar!!.setTitle("Horario")
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        var inflater: MenuInflater = menuInflater
        inflater.inflate(R.menu.bar_menu,menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        if ( item.itemId == R.id.logout)
        {
            var session  = SessionManagement(this)
            session.logout()
            var intent =  Intent(this, LoginActivity::class.java)
            startActivity(intent)
            finish()
            return true
        }
        if (item.itemId == R.id.excel){
            if (!haverpermission())
                return false
            download(Global.Domain+"/excel_horario","xlsx")

        }
        if (item.itemId == R.id.Pdf){
            if (!haverpermission())
                return false
            download(Global.Domain+"/pdf_horario","pdf")
        }
        if (item.itemId == R.id.Html){
            if (!haverpermission())
                return false
            download(Global.Domain+"/html_horario","html")
        }
        return super.onOptionsItemSelected(item)
    }

    fun haverpermission(): Boolean {
        if (Build.VERSION.SDK_INT >= 23) {
            if (checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE)
                    == PackageManager.PERMISSION_GRANTED &&
                    checkSelfPermission(android.Manifest.permission.READ_EXTERNAL_STORAGE)
                    == PackageManager.PERMISSION_GRANTED) {
                Log.e("Permission error","You have permission")
                return true;
            } else {

                Log.e("Permission error","You have asked for permission")
                ActivityCompat.requestPermissions(this,  arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE), 1)
                ActivityCompat.requestPermissions(this,  arrayOf(Manifest.permission.READ_EXTERNAL_STORAGE), 1)
                return false;
            }
        }
        else { //you dont need to worry about these stuff below api level 23
            Log.e("Permission error","You already have the permission");
            return true;
        }
    }

    fun download(url: String,extension: String){
        val downloadmanager = getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
        val uri = Uri.parse(url)

        val request = DownloadManager.Request(uri)
        request.setTitle("Horario")
        request.setDescription("Downloading")
        request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);

        request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, "horario."+extension)
        downloadmanager.enqueue(request)
    }

}