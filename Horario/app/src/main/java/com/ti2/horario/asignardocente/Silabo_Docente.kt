package com.ti2.horario.asignardocente

import android.content.Context
import android.util.Log
import android.widget.Button
import com.ti2.horario.Global
import com.ti2.horario.Object
import okhttp3.OkHttpClient
import okhttp3.Response

class Silabo_Docente : Object {

    var button: Button? = null
    var sil_ide: Int? = null
    var gru_ide: Int? = null
    var doc_ide: Int? = null
    var tipo_clase: String? =null
    var horas: Int? = null
    var groupInfo: GroupInfo? = null
    var sil_doc_ide: String? = null

    constructor(context: Context, client: OkHttpClient, handler: android.os.Handler) : super(context,client,handler){

    }

    fun link(button: Button)
    {
        this.button = button
    }


    fun setForInsert(sil_ide: Int,gru_ide: Int,tipo_clase: String,horas: Int){
        this.sil_ide = sil_ide
        this.gru_ide = gru_ide
        this.tipo_clase = tipo_clase
        this.horas = horas
    }
    fun insert(groupInfo: GroupInfo)
    {
        this.groupInfo = groupInfo
        var jsonrequest = " { \"doc_ide\" : " + doc_ide.toString() +
            " , \"sil_ide\" :  " + sil_ide.toString() +
            " , \"gru_ide\" : " + gru_ide.toString() +
            " , \"tipo_clase\" : \"" + tipo_clase + "\" " +
            " , \"horas\" : " + horas.toString() + " } "


        call(Global.Domain+"/assign_teacher",jsonrequest)
    }

    fun setForDelete(sil_doc_ide: String){
        this.sil_doc_ide = sil_doc_ide
    }

    fun delete(groupInfo: GroupInfo){
        this.groupInfo = groupInfo
        var jsonrequest = " { \"sil_doc_ide\" : " + sil_doc_ide + " } "

        call(Global.Domain+"/unassign_teacher",jsonrequest)
    }

    override fun onResponse(link: String, response: Response) {

        if (link == Global.Domain+"/unassign_teacher")
        {
            groupInfo!!.update()
        }
        if (link == Global.Domain+"/assign_teacher")
        {
            groupInfo!!.update()
        }

    }

}