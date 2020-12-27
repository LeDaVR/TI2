package com.ti2.horario.asignardocente

import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.view.Menu
import android.view.MenuInflater
import android.view.MenuItem
import androidx.appcompat.widget.Toolbar
import androidx.appcompat.app.AppCompatActivity
import com.ti2.horario.R
import com.ti2.horario.login.LoginActivity
import com.ti2.horario.login.SessionManagement
import okhttp3.*


class AsignarDocente : AppCompatActivity() {

    val client = OkHttpClient()
    var handler: Handler = Handler()

    var schedules: SignatureButton? = null
    var groupList: GroupList? = null
    var teacherButton: TeacherButton? = null
    var toolbar: Toolbar? = null

    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        setContentView(R.layout.asignar_docente)
        init()
    }

    fun init()
    {
        schedules = SignatureButton(this@AsignarDocente, client, handler, findViewById(R.id.search_curso))
        groupList = GroupList(this@AsignarDocente, client, handler, findViewById(R.id.groups))
        groupList!!.mas = findViewById(R.id.mas)
        groupList!!.menos = findViewById(R.id.menos)

        schedules!!.link(groupList!!)

        teacherButton = TeacherButton(this@AsignarDocente, client, handler)
        groupList!!.link(teacherButton!!)

        toolbar = findViewById<Toolbar>(R.id.toolbar2)
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
            var intent =  Intent(this,LoginActivity::class.java)
            startActivity(intent)
            finish()
            return true
        }
        return super.onOptionsItemSelected(item)
    }

}
