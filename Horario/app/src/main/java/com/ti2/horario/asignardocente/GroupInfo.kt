package com.ti2.horario.asignardocente

import android.app.Dialog
import android.content.Context
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.text.Editable
import android.text.Layout
import android.text.TextWatcher
import android.util.Log
import android.view.Gravity
import android.view.View
import android.view.View.VISIBLE
import android.view.ViewGroup
import android.widget.*
import androidx.cardview.widget.CardView
import androidx.core.view.setMargins
import com.ti2.horario.Global
import com.ti2.horario.Object
import com.ti2.horario.R
import com.ti2.horario.UsersAdapter
import okhttp3.OkHttpClient
import okhttp3.Response
import org.json.JSONObject

class GroupInfo : Object {
    var doc_teo: String = String()
    var doc_lab: String = String()
    var doc_pra: String = String()
    var ide_teo: String = String()
    var ide_lab: String = String()
    var ide_pra: String = String()
    var hor_teo: String = String()
    var hor_lab: String = String()
    var hor_pra: String = String()

    var dialog: Dialog? = null
    var linearLayout: LinearLayout? = null
    var tableLayout: TableLayout? = null
    var teacherButton: TeacherButton? = null
    var silabo_docente: MutableList<Silabo_Docente> = mutableListOf()
    var cardTeacher: CardView? = null

    var sil_ide: Int? = null
    var gru_ide: Int? = null
    var current_teacher: Int? = null


    fun link(teacherButton: TeacherButton)
    {
        this.teacherButton = teacherButton
    }

    constructor(context: Context, client: OkHttpClient, handler: android.os.Handler,linearLayout: LinearLayout)
            : super(context,client,handler) {
        this.linearLayout = linearLayout
        tableLayout = TableLayout(context)
        tableLayout!!.visibility = View.GONE
        linearLayout.addView(tableLayout)
    }

    fun changeVisibility(){
        var visible = tableLayout!!.visibility
        if ( visible == VISIBLE)
            tableLayout!!.visibility = View.GONE
        else
            tableLayout!!.visibility = VISIBLE
    }

    fun setForUpdate(gru_ide:  String,sil_ide: Int){
        this.gru_ide = gru_ide.toInt()
        this.sil_ide = sil_ide
    }

    fun update()
    {
        var jsonrequest = """
        { "gru_ide" : 
        """.trimIndent() + gru_ide + " }  "
        call(Global.Domain+"/group_info",jsonrequest)
    }

    override fun onResponse(link: String, response: Response) {
        val datos: JSONObject = JSONObject(response.body!!.string())
        doc_teo = datos.getString("doc_teo")
        doc_lab = datos.getString("doc_lab")
        doc_pra = datos.getString("doc_pra")
        ide_teo = datos.getString("ide_teo")
        ide_lab = datos.getString("ide_lab")
        ide_pra = datos.getString("ide_pra")
        hor_teo = datos.getString("hor_teo")
        hor_lab = datos.getString("hor_lab")
        hor_pra = datos.getString("hor_pra")

        handler.post(object : Runnable{
            override fun run() {
                draw()
            }
        })
    }



    fun draw()
    {
        drawtable(tableLayout!!)
    }

    fun drawtable(tableLayout: TableLayout)
    {
        tableLayout.removeAllViews()
        tableLayout.gravity = Gravity.CENTER
        tableLayout.setBackgroundColor(Color.GRAY)
        var tipes = arrayOf("Teoría","Práctica","Laboratorio")
        var ides = arrayOf(ide_teo,ide_pra,ide_lab)
        var values = arrayOf(doc_teo,doc_pra,doc_lab)
        var horas = arrayOf(hor_teo,hor_pra,hor_lab)
        silabo_docente = mutableListOf()

        for ( i in 0..tipes.size-1)
        {
            var tableRow = TableRow(context)
            tableRow.gravity = Gravity.CENTER
            var params  = TableRow.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT, 0.4f)
            params.setMargins(20)
            tableRow.layoutParams
            tableRow.setBackgroundColor(Color.WHITE)

            params  = TableRow.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, 0.4f)
            params.rightMargin = 1
            params.bottomMargin = 1

            var tipo_clase = TextView(context)
            tipo_clase.layoutParams = params
            tipo_clase.setText(tipes[i])
            tipo_clase.setBackgroundColor(Color.WHITE)
            tableRow.addView(tipo_clase)

            params = TableRow.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, 0.6f)
            params.rightMargin = 1
            params.bottomMargin = 1

            var docente = TextView(context)
            docente.layoutParams = params
            if (values[i] != "None")
                docente.setText(values[i])
            docente.setBackgroundColor(Color.WHITE)
            tableRow.addView(docente)


            var button =  Button(context)
            button.setText("+")
            if (values[i] != "None")
                button.setText("-")

            tableRow.addView(button)

            silabo_docente.add(Silabo_Docente(context!!, client, handler))

            if (button.text == "+")
                toButton(button,i,tipes[i],horas[i])
            else{
                silabo_docente[i].setForDelete(ides[i])
                button.setOnClickListener(object : View.OnClickListener{
                    override fun onClick(v: View?) {
                        silabo_docente[i].delete(this@GroupInfo)
                    }
                })

            }


            tableLayout.addView(tableRow)
        }
    }

    fun toButton(search_teacher: Button,index: Int,tipo_clase: String,horas: String)
    {
        search_teacher.setOnClickListener( object :  View.OnClickListener {
            override fun onClick(v: View?) {
                dialog = Dialog(context!!)
                dialog!!.setContentView(R.layout.dialog_searchable_spinner)
                dialog!!.window!!.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
                dialog!!.getWindow()!!.setLayout(LinearLayout.LayoutParams.WRAP_CONTENT,LinearLayout.LayoutParams.WRAP_CONTENT)
                dialog!!.show()

                var linearLayout = dialog!!.findViewById<LinearLayout>(R.id.linearLayout)
                var title = dialog!!.findViewById<TextView>(R.id.title)
                var searchView = dialog!!.findViewById<TextView>(R.id.edit_text)
                var listView = dialog!!.findViewById<ListView>(R.id.list_view)

                var layoutParams = LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT,LinearLayout.LayoutParams.MATCH_PARENT)
                cardTeacher = CardView(context!!)
                cardTeacher!!.layoutParams = layoutParams
                linearLayout.addView(cardTeacher)
                var submit = Button(context)
                submit.setText("Asignar")
                submit.setBackgroundResource(R.drawable.ripple)

                silabo_docente[index].link(submit)

                silabo_docente[index].setForInsert(sil_ide!!,gru_ide!!,tipo_clase,horas.toInt())

                linearLayout.addView(submit)


                val adapter = UsersAdapter(context!!,
                        android.R.layout.simple_list_item_1, teacherButton!!.doublelist)
                listView.adapter = adapter


                searchView.setOnClickListener(object : View.OnClickListener{
                    override fun onClick(v: View?) {
                        searchView.setFocusableInTouchMode(true);
                        searchView.setFocusable(true);
                        listView.visibility = VISIBLE
                    }
                })



                searchView.addTextChangedListener(object: TextWatcher {
                    override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {

                    }

                    override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                        adapter.filter.filter(s)
                        adapter.getFilter().filter(s)
                    }

                    override fun afterTextChanged(s: Editable?) {

                    }
                })

                listView.setOnItemClickListener(object: AdapterView.OnItemClickListener{
                    override fun onItemClick(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                        searchView.setFocusableInTouchMode(false);
                        searchView.setFocusable(false);


                        current_teacher = adapter.getItem(position)!!.id.toInt()
                        teacherButton!!.current_teacher = current_teacher
                        silabo_docente[index].doc_ide = current_teacher
                        teacherButton!!.update(cardTeacher!!)
                        listView.visibility = View.GONE
                    }

                })

                submit.setOnClickListener(object : View.OnClickListener{
                    override fun onClick(v: View?) {
                        silabo_docente[index].insert(this@GroupInfo)
                        dialog!!.dismiss()
                    }
                })
            }

        })
    }


}