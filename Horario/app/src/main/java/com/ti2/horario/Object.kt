package com.ti2.horario

import android.content.Context
import android.os.Handler
import android.util.Log
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException


open class Object {
    var client: OkHttpClient
    var handler: Handler
    public var context: Context? = null
    constructor(context: Context, client: OkHttpClient, handler: android.os.Handler){
        this.context = context
        this.client = client
        this.handler = handler
    }


    fun call(url: String,jsonrequest: String) {
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
    open fun onResponse(link: String,response: Response) {}

}