from flask import Flask
from flask import request
from flask import jsonify
from flask import flash
from flaskext.mysql import MySQL
from models import ScheduleModel
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import click
from flask.cli import with_appcontext

class ScheduleController:
    def __init__(self,app):
        self.model = ScheduleModel(app)

        @app.route('/show_schedule', methods=('GET', 'POST'))
        def show():
            data = self.model.horario("1")
            flash(data)
            return render_template('schedules.html')
        

        @app.route('/create_schedule',methods=['POST'])
        def create_schedule():
            hora_entrada =  request.json['hora_entrada']
            hora_salida = request.json['hora_salida']
            aula = request.json['aula']
            dia = request.json['dia']
            sil_doc_ide =  request.json['sil_doc_ide']
            if self.model.can_insert(hora_entrada,hora_salida,dia,aula.sil_doc_ide):
                return jsonify({ 'status' : 'disponible'})  
                #return jsonify(self.model.create_schedule(hora_entrada,hora_salida,hora,dia,sil_doc_ide))
            else:
                return jsonify({ 'status' : 'no_disponible'})        

        @app.route('/delete_schedule',methods=['POST'])
        def delete_schedule():
            return 1

        @app.route('/update_schedule',methods=['POST'])
        def update_schedule():
            return 1