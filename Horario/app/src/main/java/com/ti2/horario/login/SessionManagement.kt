package com.ti2.horario.login

import android.content.Context
import android.content.SharedPreferences
import android.util.Log

class SessionManagement {
    var sharedPreferences: SharedPreferences? = null
    var editor: SharedPreferences.Editor? = null

    constructor(context: Context){
        sharedPreferences = context.getSharedPreferences("SESSION",Context.MODE_PRIVATE)
        editor = sharedPreferences!!.edit()
    }

    fun getSession(): User {
        var user: User = User()
        user.username = sharedPreferences!!.getString("USER_NAME","NULL")
        user.password = sharedPreferences!!.getString("PASSWORD","NULL")
        user.doc_ide = sharedPreferences!!.getString("DOC_IDE","NULL")
        return user
    }

    fun login(user: User) {
        Log.e("Login",user.permission!!)
        editor!!.putString("USER_NAME",user.username).commit()
        editor!!.putString("PASSWORD",user.password).commit()
        editor!!.putString("DOC_IDE",user.doc_ide).commit()
        editor!!.putString("PERMISSIONS","DOCENTE").commit()
        if ( user.permission != "null")
            editor!!.putString("PERMISSIONS","ADMIN").commit()
    }

    fun logout() {
        editor!!.putString("USER_NAME","NULL").commit()
        editor!!.putString("PASSWORD","NULL").commit()
        editor!!.putString("DOC_IDE","NULL").commit()
        editor!!.putString("PERMISSIONS","NULL").commit()
    }

    fun getPermissions(): String? {
        return sharedPreferences!!.getString("PERMISSIONS","NULL")
    }

}