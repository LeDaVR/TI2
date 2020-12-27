package com.ti2.horario.horario

import android.app.Dialog
import android.content.Context
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.text.Editable
import android.text.Layout
import android.text.TextWatcher
import android.util.Log
import android.view.View
import android.widget.*
import com.ti2.horario.*
import com.ti2.horario.login.SessionManagement
import okhttp3.OkHttpClient
import okhttp3.Response
import org.json.JSONArray
import org.json.JSONObject

class ScheduleButton : Object {
    var textView: TextView? = null
    var dialog: Dialog? = null
    var hora_entrada = String()
    var hora_salida = String()
    var aul_ide = String()
    var dia = String()
    var hor_ide = String()
    var double_list: ArrayList<Dato?> = arrayListOf()
    var current_doc_ide: Int? = null
    var tablaHorario: TablaHorario? = null

    var sil_doc_ide: Int? = null
    constructor(context: Context, client: OkHttpClient, handler: android.os.Handler, textView: TextView)
            : super(context,client,handler)
    {
        this.textView  = textView

    }

    fun insert(){
        this.textView!!.setOnClickListener(object : View.OnClickListener{
            override fun onClick(v: View?) {
                list()
            }
        })
    }

    fun delete(){
        this.textView!!.setOnClickListener(object : View.OnClickListener{
            override fun onClick(v: View?) {
                delete_confirm()
            }
        })
    }


    fun link(tablaHorario: TablaHorario)
    {
        this.tablaHorario = tablaHorario
    }

    fun setForInsert(hora_entrada: String,hora_salida: String,aul_ide: String,dia: String)
    {
        this.hora_entrada = hora_entrada
        this.hora_salida = hora_salida
        this.aul_ide = aul_ide
        this.dia = dia
    }

    fun setForDelete(hor_ide: String){
        this.hor_ide = hor_ide
    }

    fun list(){
        var sessionManagement = SessionManagement(context!!)
        var user = sessionManagement.getSession()
        var jsonrequest = "{  \"doc_ide\" : "+user.doc_ide+" } "
        call(Global.Domain+"/schedule_to_chose",jsonrequest)
    }

    fun drawList(){
        dialog = Dialog(context!!)
        dialog!!.setContentView(R.layout.dialog_searchable_spinner)
        dialog!!.getWindow()!!.setLayout(640,LinearLayout.LayoutParams.WRAP_CONTENT)
        dialog!!.window!!.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
        dialog!!.show()

        val title = dialog!!.findViewById<TextView>(R.id.title)
        title.setText("Asignaturas")

        val editText = dialog!!.findViewById<EditText>(R.id.edit_text)
        val listview = dialog!!.findViewById<ListView>(R.id.list_view)


        val adapter = UsersAdapter(context,
                android.R.layout.simple_list_item_1, double_list)

        listview.adapter = adapter

        editText.addTextChangedListener(object: TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {

            }

            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                adapter.getFilter().filter(s)
            }

            override fun afterTextChanged(s: Editable?) {

            }
        })

        listview.setOnItemClickListener(object: AdapterView.OnItemClickListener{
            override fun onItemClick(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                current_doc_ide = adapter.getItem(position)!!.id.toInt()
                create_schedule()
                dialog!!.dismiss()
            }

        })
    }

    fun create_schedule(){
        Log.e("create_schedule",current_doc_ide.toString())
        var jsonrequest =
                " { \"hora_entrada\" : \"" + hora_entrada + "\" ,"+
                "  \"hora_salida\" : \"" + hora_salida + "\" ,"+
                "  \"aul_ide\" : " + aul_ide + " ,"+
                "  \"dia\" : \"" + dia + "\" ,"+
                "  \"sil_doc_ide\" : " + current_doc_ide + " }"
        Log.e("create_schedule",jsonrequest)
        call(Global.Domain+"/create_schedule",jsonrequest)
    }

    fun delete_confirm(){
        handler.post(object : Runnable{
            override fun run() {
                dialog = Dialog(context!!)
                dialog!!.setContentView(R.layout.dialog_delete)
                dialog!!.getWindow()!!.setLayout(LinearLayout.LayoutParams.WRAP_CONTENT,LinearLayout.LayoutParams.WRAP_CONTENT)
                dialog!!.window!!.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
                dialog!!.show()

                var accept = dialog!!.findViewById<Button>(R.id.confirm_button)
                var cancel = dialog!!.findViewById<Button>(R.id.cancel_button)

                accept.setOnClickListener(object : View.OnClickListener{
                    override fun onClick(v: View?) {
                        call(Global.Domain+"/delete_schedule","{ \"hor_ide\" : "+hor_ide+"}")
                        dialog!!.dismiss()
                    }
                })

                cancel.setOnClickListener(object : View.OnClickListener{
                    override fun onClick(v: View?) {
                        dialog!!.dismiss()
                    }
                })

            }
        })

    }

    override fun onResponse(link: String, response: Response) {
        if ( link == Global.Domain+"/schedule_to_chose")
        {
            var jsonArray = JSONArray(response.body!!.string())
            double_list = arrayListOf()
            var jsonObject: JSONObject
            for ( i in 0..jsonArray.length()-1){
                jsonObject = jsonArray.getJSONObject(i)
                var id = jsonObject.getString("sil_doc")
                var name  = jsonObject.getString("asignatura")+
                        " Grupo ("+jsonObject.getString("grupo")+
                        ") "+jsonObject.getString("tipo_clase")
                double_list.add(Dato(id,name))
            }
            handler.post(object : Runnable{
                override fun run() {
                    drawList()
                }
            })
        }
        if (link == Global.Domain+"/create_schedule")
        {
            tablaHorario!!.update(tablaHorario!!.per_aca,tablaHorario!!.aul_ide)
        }
        if ( link == Global.Domain+"/delete_schedule" )
        {
            tablaHorario!!.update(tablaHorario!!.per_aca,tablaHorario!!.aul_ide)
        }
    }

}