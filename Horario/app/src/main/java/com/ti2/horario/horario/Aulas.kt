package com.ti2.horario.horario

import android.content.Context
import android.util.Log
import com.google.android.material.tabs.TabLayout
import com.ti2.horario.Global
import com.ti2.horario.Object
import okhttp3.OkHttpClient
import okhttp3.Response
import org.json.JSONArray

class Aulas : Object {
    var tabLayout : TabLayout? = null
    var aul_ide : ArrayList<String>? = null
    var aul_name : ArrayList<String>? = null
    var tablaHorario: TablaHorario? = null
    var per_aca = "2020-B"

    fun link(tablaHorario: TablaHorario)
    {
        this.tablaHorario = tablaHorario
    }

    constructor(context: Context, client: OkHttpClient, handler: android.os.Handler,tabLayout: TabLayout) : super(context,client,handler) {
        this.tabLayout = tabLayout
        call(Global.Domain+"/aulas","")
        tabLayout.addOnTabSelectedListener(object: TabLayout.OnTabSelectedListener{
            override fun onTabReselected(tab: TabLayout.Tab?) {

            }
            override fun onTabSelected(tab: TabLayout.Tab?) {
                tablaHorario!!.update(per_aca,aul_ide!![tab!!.position])
            }
            override fun onTabUnselected(tab: TabLayout.Tab?) {

            }
        })
    }

    fun draw()
    {
        tabLayout!!.removeAllTabs()
        for ( i in 0..aul_name!!.size-1)
        {
            Log.e("aulas","creando tab")
            tabLayout!!.addTab(tabLayout!!.newTab())
            tabLayout!!.getTabAt(i)!!.setText(aul_name!![i])
        }
    }

    override fun onResponse(link: String, response: Response) {
        if ( link == Global.Domain+"/aulas")
        {
            aul_ide = arrayListOf()
            aul_name = arrayListOf()
            var jsonArray = JSONArray(response.body!!.string())
            Log.e("aulas",jsonArray.toString())
            for ( i in 0..jsonArray.length()-1){
                aul_ide!!.add(jsonArray.getJSONObject(i).getString("aul_ide"))
                aul_name!!.add(jsonArray.getJSONObject(i).getString("aul_nom"))
            }
            handler.post(object : Runnable{
                override fun run() {
                    draw()
                }
            })
        }
    }


}