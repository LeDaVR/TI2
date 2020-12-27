package com.ti2.horario

import android.R
import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*


class Global{
    companion object {
        var Domain = "http://192.168.0.8:5000"
    }
}

class Dato{
    var id: String = String()
    var value: String = String()
    constructor(id: String,value: String){
        this.id = id
        this.value = value
    }

    operator fun contains(dato: Dato) = this.value in dato.value
}


class UsersAdapter(context: Context?,resource: Int, users: ArrayList<Dato?>?)
    : ArrayAdapter<Dato?>(context!!, resource, users!!) , Filterable {

    private var mFilter:  ItemFilter? = null
    private var originalData: ArrayList<Dato?>? = users
    private var filteredData: ArrayList<Dato?>? = users

    override fun getCount(): Int {
        return filteredData!!.size
    }
    override fun getItem(position: Int): Dato? {
        return filteredData!![position]
    }

    override fun getItemId(position: Int): Long {
        return position.toLong()
    }



    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        // Get the data item for this position

         var convertView: View? = convertView
        val dato: Dato? = getItem(position)
        // Check if an existing view is being reused, otherwise inflate the view
        if (convertView == null) {
            convertView = LayoutInflater.from(context).inflate(R.layout.simple_list_item_1, parent, false)
        }
        // Lookup view for data population
        val value = convertView!!.findViewById(R.id.text1) as TextView
        // Populate the data into the template view using the data object
        value.setText(dato!!.value)
        // Return the completed view to render on screen
        return convertView
    }

    override fun getFilter(): Filter {
        if (mFilter == null) {
            mFilter = ItemFilter()
        }
        return mFilter!!
    }

    private inner class ItemFilter : Filter() {
        override fun performFiltering(constraint: CharSequence): FilterResults {
            val filterString = constraint.toString().toLowerCase()
            val results = FilterResults()
            val list = originalData
            val count = list!!.size
            val nlist = ArrayList<Dato>(count)
            var filterableString: String
            for (i in 0 until count) {
                filterableString = list[i]!!.value
                if (filterableString.toLowerCase().contains(filterString)) {
                    nlist.add(list[i]!!)
                }
            }
            results.values = nlist
            results.count = nlist.size
            return results
        }

        override fun publishResults(constraint: CharSequence, results: FilterResults) {
            filteredData = results.values as ArrayList<Dato?>
            notifyDataSetChanged()
        }
    }
}
