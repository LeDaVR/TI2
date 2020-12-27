package com.ti2.horario.asignardocente

import android.app.Dialog
import android.content.Context
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.widget.*
import com.ti2.horario.*
import okhttp3.*
import org.json.JSONArray

class SignatureButton: Object {
    var dialog_cursos: Dialog? = null
    var search_curso: TextView? = null
    var current_signature: Int? = null
    var groupList: GroupList? = null
    var sig_ide: MutableList<String> = mutableListOf()
    var sig_nom: MutableList<String> = mutableListOf()
    var double_list: ArrayList<Dato?> = arrayListOf()

    fun link(groupList: GroupList)
    {
        this.groupList = groupList
    }

    constructor(context: Context,client: OkHttpClient,handler: android.os.Handler,textView: TextView) : super(context,client,handler){
        search_curso = textView

        call(Global.Domain+"/asignaturas","")
        search_curso!!.setOnClickListener( object :  View.OnClickListener {
            override fun onClick(v: View?) {
                call(Global.Domain+"/asignaturas","")
                dialog_cursos = Dialog(context)
                dialog_cursos!!.setContentView(R.layout.dialog_searchable_spinner)
                dialog_cursos!!.getWindow()!!.setLayout(LinearLayout.LayoutParams.WRAP_CONTENT,LinearLayout.LayoutParams.WRAP_CONTENT)
                dialog_cursos!!.window!!.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
                dialog_cursos!!.show()

                var title = dialog_cursos!!.findViewById<TextView>(R.id.title)
                title.setText("Seleccionar Asignatura")
                val editText = dialog_cursos!!.findViewById<EditText>(R.id.edit_text)
                val listview = dialog_cursos!!.findViewById<ListView>(R.id.list_view)


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
                        search_curso!!.setText(adapter.getItem(position)!!.value)
                        current_signature = adapter.getItem(position)!!.id.toInt()
                        groupList!!.update(current_signature.toString())
                        dialog_cursos!!.dismiss()
                    }

                })
            }

        })
    }

    override fun onResponse(link: String, response: Response) {
        if ( link == Global.Domain+"/asignaturas"){
            sig_ide = mutableListOf()
            sig_nom = mutableListOf()
            double_list = arrayListOf()
            val datos: JSONArray = JSONArray(response.body!!.string())

            for ( j in 0..datos.length()-1)
            {
                sig_ide.add(datos.getJSONObject(j).getString("sil_ide"))
                sig_nom.add(datos.getJSONObject(j).getString("cur_nom"))
                double_list.add(Dato(sig_ide[j], sig_nom[j]))
            }
        }
    }
}
