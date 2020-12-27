package com.ti2.horario.horario

import android.content.Context
import android.graphics.Color
import android.graphics.Typeface
import android.util.Log
import android.view.Gravity
import android.widget.TableLayout
import android.widget.TableRow
import android.widget.TextView
import androidx.core.view.setPadding
import com.ti2.horario.Global
import com.ti2.horario.Object
import com.ti2.horario.R
import com.ti2.horario.login.SessionManagement
import okhttp3.OkHttpClient
import okhttp3.Response
import org.json.JSONArray

class TablaHorario : Object {
    var tableLayout: TableLayout? = null
    var table: ArrayList<ArrayList<String>>? = null
    var per_aca = String()
    var aul_ide = String()
    var buttons: ArrayList<ScheduleButton>? = null
    constructor(context: Context, client: OkHttpClient, handler: android.os.Handler, tableLayout: TableLayout)
            : super(context,client,handler)
    {
        this.tableLayout  = tableLayout
        tableLayout.setBackgroundColor(Color.rgb(221, 221, 221))
    }

    fun update(per_aca: String,aul_ide: String)
    {
        this.per_aca = per_aca
        this.aul_ide = aul_ide
        var jsonrequest =
                " { \"sil_per_aca\" : " + "\"" + per_aca+ "\" , " +
                        " \"aul_ide\" : " + aul_ide + " } "

        call(Global.Domain+"/get_schedule",jsonrequest)

        Log.e("aulas",aul_ide)
    }

    override fun onResponse(link: String, response: Response) {
        if ( link == Global.Domain+"/get_schedule" )
        {
            var jsonArray = JSONArray(response.body!!.string())

            table = arrayListOf()
            for ( i in 0..jsonArray.length()-1)
            {
                var jsonObject = jsonArray.getJSONObject(i)
                var array = arrayListOf(
                        jsonObject.getString("hora_entrada"),
                        jsonObject.getString("hora_salida"),
                        jsonObject.getString("lunes"),
                        jsonObject.getString("martes"),
                        jsonObject.getString("miercoles"),
                        jsonObject.getString("jueves"),
                        jsonObject.getString("viernes"),
                        jsonObject.getString("doc_lun"),
                        jsonObject.getString("doc_mar"),
                        jsonObject.getString("doc_mie"),
                        jsonObject.getString("doc_jue"),
                        jsonObject.getString("doc_vie"),
                        jsonObject.getString("lun_ide"),
                        jsonObject.getString("mar_ide"),
                        jsonObject.getString("mie_ide"),
                        jsonObject.getString("jue_ide"),
                        jsonObject.getString("vie_ide")
                        )
                table!!.add(array)
            }
            handler.post(object : Runnable{
                override fun run() {
                    draw()
                }
            })
        }
    }

    fun draw(){
        tableLayout!!.removeAllViews()
        buttons = arrayListOf()
        var titlerow = arrayListOf("HORAS","LUNES","MARTES","MIERCOLES","JUEVES","VIERNES")
        normalrow(titlerow,Color.rgb(153, 5, 55),Color.WHITE)

        for ( i in 0..table!!.size-1)
        {
            var time = table!![i][0].substring(0,5) +"-"+table!![i][1].substring(0,5)
            var row = arrayListOf(time,table!![i][2],table!![i][3],table!![i][4],table!![i][5],table!![i][6])
            if (i == 2 || i == 5 || i ==  12  || i == 15 || i == 18)
            {
                for ( j in 1..row.size-1)
                    row[j] = "DESCANSO"
                normalrow(row,Color.GRAY,Color.WHITE)
            }
            else{
                usefulrow(row,i)
                if ( i == 9 ){
                    var TARDE = arrayListOf("TARDE","","","","","")
                    normalrow(TARDE,Color.GRAY,Color.WHITE)
                }
            }

        }
    }

    fun normalrow(names: ArrayList<String>,backgroundColor: Int,textColor: Int)
    {
        var tableRow = TableRow(context)
        for ( i in 0..names.size-1){
            var textView = TextView(context)
            var layoutParams = TableRow.LayoutParams(0,TableRow.LayoutParams.MATCH_PARENT)
            layoutParams.bottomMargin = 1
            layoutParams.rightMargin = 1
            if ( i == 0)
                layoutParams.width = TableRow.LayoutParams.WRAP_CONTENT
            textView.layoutParams = layoutParams
            if (names[i] != "None")
                textView.setText(names[i])
            textView.gravity = Gravity.CENTER
            textView.setPadding(2)
            textView.setTextColor(textColor)
            textView.setBackgroundColor(backgroundColor)

            tableRow.addView(textView)
        }
        tableLayout!!.addView(tableRow)
    }

    fun usefulrow(names: ArrayList<String>,index: Int)
    {
        var day  = arrayListOf("Lunes","Martes","Miercoles","Jueves","Viernes")
        var tableRow = TableRow(context)
        var sessionManagement = SessionManagement(context!!)
        var user = sessionManagement.getSession()
        for ( i in 0..names.size-1){
            var textView = TextView(context)
            var layoutParams = TableRow.LayoutParams(0,TableRow.LayoutParams.MATCH_PARENT)
            layoutParams.bottomMargin = 1
            layoutParams.rightMargin = 1
            if ( i == 0)
                layoutParams.width = TableRow.LayoutParams.WRAP_CONTENT
            textView.layoutParams = layoutParams
            textView.setBackgroundColor(Color.WHITE)
            textView.setTextColor(Color.BLACK)

            if (names[i] == "None" && i != 0)
            {
                textView.setText("\n")
                var scheduleButton = ScheduleButton(context!!, client, handler, textView)
                scheduleButton.link(this)
                scheduleButton.insert()
                scheduleButton.setForInsert(table!![index][0],table!![index][1],aul_ide,day[i-1])
                textView.setBackgroundResource(R.drawable.ripple2)
            }else{
                textView.setText(names[i])
                if ( user.doc_ide == table!![index][i+6])
                {
                    textView.setTypeface(null,Typeface.BOLD)
                    var scheduleButton = ScheduleButton(context!!, client, handler, textView)
                    scheduleButton.link(this)
                    scheduleButton.delete()
                    scheduleButton.setForDelete(table!![index][i+11])
                }
            }
            textView.gravity = Gravity.CENTER
            textView.setPadding(2)

            tableRow.addView(textView)
        }
        tableLayout!!.addView(tableRow)
    }


}