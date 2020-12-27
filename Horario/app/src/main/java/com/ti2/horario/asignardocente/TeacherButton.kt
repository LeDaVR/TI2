package com.ti2.horario.asignardocente

import android.app.Dialog
import android.content.Context
import android.graphics.Color
import android.util.Log
import android.view.ViewGroup
import android.widget.*
import androidx.cardview.widget.CardView
import androidx.core.view.setPadding
import com.ti2.horario.Dato
import com.ti2.horario.Global
import com.ti2.horario.Object
import okhttp3.OkHttpClient
import okhttp3.Response
import org.json.JSONArray
import org.json.JSONObject

class TeacherButton : Object {
    var dialog_teacher: Dialog? = null
    var current_teacher: Int? = null
    var cardTeacher: CardView? = null
    var submit: Button? = null

    var doc_ide: MutableList<String> = mutableListOf()
    var doc_nom: MutableList<String> = mutableListOf()
    var teacher_info: MutableList<MutableList<String>> = mutableListOf()
    var doublelist: ArrayList<Dato?>? = arrayListOf()

    constructor(context: Context, client: OkHttpClient, handler: android.os.Handler) : super(context,client,handler){
        call(Global.Domain+"/teachers","")
    }


    fun update(cardView: CardView)
    {
        this.cardTeacher = cardView
        var jsonrequest = """
            { "id" : 
        """.trimIndent() + current_teacher + " } "
        call(Global.Domain+"/teacher_info",jsonrequest)
    }

    fun drawTeacher()
    {
        cardTeacher!!.removeAllViews()
        var tableLayout = TableLayout(context)
        tableLayout.setBackgroundColor(Color.GRAY)
        for ( i in 0..teacher_info[0].size-1)
        {
            addrow(tableLayout,teacher_info[0][i],teacher_info[1][i])
        }
        cardTeacher!!.addView(tableLayout)
    }

    fun addrow(tableLayout: TableLayout,id: String,value: String)
    {
        Log.e(id,value)
        var rowparams  = TableRow.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT)
        var row = TableRow(context)

        var id_text =  TextView(context)
        var value_text = TextView(context)

        id_text.setText(id)
        id_text.setBackgroundColor(Color.WHITE)
        id_text.setPadding(8)
        value_text.setText(value)
        value_text.setBackgroundColor(Color.WHITE)
        value_text.setPadding(8)

        var params  = TableRow.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.MATCH_PARENT, 1f)
        params.rightMargin = 1
        params.bottomMargin = 1
        id_text.layoutParams = params
        value_text.layoutParams = params

        row.addView(id_text)
        row.addView(value_text)
        tableLayout.addView(row)
    }

    override fun onResponse(link: String, response: Response) {
        if ( link == Global.Domain+"/teachers"){
            doc_ide = mutableListOf()
            doc_nom = mutableListOf()
            doublelist = arrayListOf()
            val datos: JSONArray = JSONArray(response.body!!.string())

            for ( j in 0..datos.length()-1)
            {
                doc_ide.add(datos.getJSONObject(j).getString("ID"))
                doc_nom.add(datos.getJSONObject(j).getString("Nombre"))
                doublelist!!.add(Dato(doc_ide[j], doc_nom[j]))
            }
        }
        if ( link == Global.Domain+"/teacher_info"){
            val datos: JSONObject = JSONObject(response.body!!.string())
            teacher_info = mutableListOf()
            teacher_info.add(mutableListOf())
            teacher_info.add(mutableListOf())
            teacher_info[0].add("Nombre")
            teacher_info[1].add(datos.getString("nombre"))
            teacher_info[0].add("Grado Academico")
            teacher_info[1].add(datos.getString("doc_grad_aca"))
            teacher_info[0].add("Especialidad")
            teacher_info[1].add(datos.getString("doc_esp"))
            teacher_info[0].add("Categoria")
            teacher_info[1].add(datos.getString("cat_nom"))
            teacher_info[0].add("Horas Asignadas")
            teacher_info[1].add(datos.getString("hor_asi"))

            handler.post( object: Runnable{
                override fun run() {
                    drawTeacher()
                }
            })
        }
    }
}