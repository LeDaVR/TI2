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

        @app.route('/get_schedule/<per_aca>', methods=['POST'] )
        def get_schedule(per_aca):
            params = {
                'sil_per_aca' : per_aca
            }
            return self.model.get_schedule(params)

        @app.route('/create_group', methods=['POST'] )
        def create_group():
            params = {
                "cantidad" : request.json['cantidad'],
                "sil_ide" : request.json['sil_ide']
            }
            return self.model.create_group(params)

        @app.route('/create_schedule',methods=['POST'])
        def create_schedule():
            params = {
                'hora_entrada' :  request.json['hora_entrada'],
                'hora_salida' : request.json['hora_salida'],
                'aul_ide' : request.json['aul_ide'],
                'dia' : request.json['dia'],
                'sil_doc_ide' :  request.json['sil_doc_ide']
            }
            
            if self.model.can_insert(params):
                return self.model.create_schedule(params)
            else:
                return jsonify({ 'status' : 'no_disponible'})        

        @app.route('/delete_schedule', methods=['POST'])
        def delete_schedule():
            params = {
                'hor_ide' : request.json['hor_ide']
            }
            return self.model.remove(params)

