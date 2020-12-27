package com.ti2.horario.login

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity
import com.ti2.horario.Global
import com.ti2.horario.horario.ActivityHorario
import com.ti2.horario.R
import com.ti2.horario.asignardocente.AsignarDocente
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.io.IOException


class LoginActivity : AppCompatActivity() {
    val client = OkHttpClient()
    var handler = Handler()
    var sessionManagement: SessionManagement? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        sessionManagement = SessionManagement(this)
        var user = sessionManagement!!.getSession()
        login(user.username!!,user.password!!)
    }


    fun login(user: String,password: String) {
        var jsonrequest = "{ \"user\" : \""+ user+"\","+
            "\"password\" : \""+password+"\"}"
        var url = Global.Domain + "/login"
        val mediaType = "application/json; charset=utf-8".toMediaType()
        val requestBody = jsonrequest.toRequestBody(mediaType)
        val request = Request.Builder()
                .url(url)
                .post(requestBody)
                .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.e("Error",url)
                e.printStackTrace()
            }
            override fun onResponse(call: Call, response: Response) {
                onResponse(url,response)
            }
        })
    }

    fun onResponse(url: String,response: Response)
    {
        var jsonObject = JSONObject(response.body!!.string())
        var user = User()
        user.username = jsonObject.getString("usu_user")
        user.password = jsonObject.getString("usu_pass")
        user.doc_ide =  jsonObject.getString("doc_ide")
        user.permission = jsonObject.getString("admin")
        Log.e("De la base de datos",user.permission!!)
        if ( jsonObject.getString("usu_ide") != "None")
        {
            sessionManagement!!.login(user)
            var permissions = sessionManagement!!.getPermissions()
            if ( permissions == "ADMIN" )
            {
                val intent = Intent(this, AsignarDocente::class.java)
                startActivity(intent)
                finish()
            }
            if ( permissions == "DOCENTE")
            {
                val intent = Intent(this, ActivityHorario::class.java)
                startActivity(intent)
                finish()
            }

        }
        else{
            handler.post(object : Runnable{
                override fun run() {
                    draw()
                }
            })
            Log.e("usuario",user.username+user.password)
            //sessionManagement!!.login(user)
        }
    }

    fun draw()
    {
        setContentView(R.layout.login)
        var button = findViewById<Button>(R.id.iniciar_sesion)
        var input_username = findViewById<EditText>(R.id.usuario)
        var input_password = findViewById<EditText>(R.id.contraseña)
        button.setOnClickListener(object : View.OnClickListener{
            override fun onClick(v: View?) {
                var usuario = input_username.text.toString()
                var contrasenia = input_password.text.toString()
                login(usuario,contrasenia)
            }
        })
    }
}