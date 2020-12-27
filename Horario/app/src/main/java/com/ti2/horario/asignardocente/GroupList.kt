package com.ti2.horario.asignardocente

import android.content.Context
import android.graphics.Color
import android.util.Log
import android.view.Gravity
import android.view.View
import android.widget.*
import androidx.cardview.widget.CardView
import androidx.core.view.setPadding
import com.ti2.horario.Global
import com.ti2.horario.Object
import com.ti2.horario.R
import okhttp3.OkHttpClient
import okhttp3.Response
import org.json.JSONArray

class GroupList : Object {
    var group_ide_list: MutableList<String> = mutableListOf()
    var group_name_list: MutableList<String> = mutableListOf()
    var group_info_list: MutableList<GroupInfo> = mutableListOf()
    var groups: LinearLayout? = null
    var teacherButton: TeacherButton? = null
    var mas: Button? = null
    var menos: Button? = null

    var sil_ide: Int? = null


    fun link(teacherButton: TeacherButton)
    {
        this.teacherButton = teacherButton
    }

    constructor(context: Context, client: OkHttpClient, handler: android.os.Handler, linearLayout: LinearLayout)
            : super(context,client,handler) {
        this.groups = linearLayout
    }

    fun update(sil_ide: String){
        var jsonrequest = """
        { "sil_ide" : 
        """.trimIndent() + sil_ide + " }  "
        call(Global.Domain+"/get_groups",jsonrequest)
        this.sil_ide = sil_ide.toInt()
    }

    override fun onResponse(link: String, response: Response) {
        if ( link == Global.Domain+"/get_groups")
        {
            group_ide_list = mutableListOf()
            group_name_list = mutableListOf()

            val datos: JSONArray = JSONArray(response.body!!.string())

            for ( j in 0..datos.length()-1)
            {
                group_ide_list.add(datos.getJSONObject(j).getString("gru_ide"))
                group_name_list.add(datos.getJSONObject(j).getString("gru_nom"))
            }
            handler.post(object : Runnable{
                override fun run() {
                    draw()
                }
            })
        }

        if ( link == Global.Domain+"/create_group")
        {
            update(sil_ide.toString())
        }

        if ( link == Global.Domain+"/delete_group")
        {
            update(sil_ide.toString())
        }

    }

    fun style(textView: TextView){
        textView.setTextColor(Color.rgb(255,255,255))
        textView.setBackgroundColor(Color.rgb(153, 5, 55))
        textView.setPadding(16)
        textView.gravity = Gravity.CENTER
        textView.setBackgroundResource(R.drawable.ripple)
    }

    fun draw()
    {
        groups!!.setPadding(10)
        groups!!.removeAllViews()
        group_info_list = mutableListOf()
        for ( j in 0..group_name_list.size-1)
        {
            var cardView = CardView(context!!)
            cardView.radius = 16.0f
            cardView.setPadding(10)

            var params = LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT,LinearLayout.LayoutParams.WRAP_CONTENT)
            params.bottomMargin = 10
            cardView.layoutParams = params
            var linearLayout = LinearLayout(context)
            linearLayout.orientation = LinearLayout.VERTICAL
            linearLayout.gravity = Gravity.CENTER_VERTICAL

            var textView = TextView(context)
            textView.setText(group_name_list[j])
            style(textView)

            linearLayout.addView(textView)
            cardView.addView(linearLayout)
            groups!!.addView(cardView)


            group_info_list.add(GroupInfo(context!!, client, handler, linearLayout))
            group_info_list[j].link(teacherButton!!)
            textView.setOnClickListener(object : View.OnClickListener{
                override fun onClick(v: View?) {
                    group_info_list[j].changeVisibility()
                    group_info_list[j].setForUpdate(group_ide_list[j],sil_ide!!)
                    group_info_list[j].update()
                }
            })
        }
        groups()
    }

    fun groups(){
        mas!!.setOnClickListener(object : View.OnClickListener{
            override fun onClick(v: View?) {
                var jsonRequest = " { \"cantidad\" : 1 , \"sil_ide\" : "+ sil_ide+  "}"
                call(Global.Domain+"/create_group",jsonRequest)
            }
        })
        menos!!.setOnClickListener(object : View.OnClickListener{
            override fun onClick(v: View?) {
                var jsonRequest = " {  \"sil_ide\" : "+ sil_ide+  "}"
                call(Global.Domain+"/delete_group",jsonRequest)
            }
        })
    }

}