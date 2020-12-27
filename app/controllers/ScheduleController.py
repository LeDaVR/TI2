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
    def __init__(self,app,conexion):
        self.model = ScheduleModel(conexion)

        @app.route('/get_schedule', methods=['POST'] )
        def get_schedule():
            params = {
                "sil_per_aca" : request.json['sil_per_aca'],
                "aul_ide" : request.json['aul_ide']
            }
            return self.model.get_schedule(params)

        @app.route('/create_group', methods=['POST'] )
        def create_group():
            params = {
                "cantidad" : request.json['cantidad'],
                "sil_ide" : request.json['sil_ide']
            }
            return self.model.create_group(params)

        @app.route('/delete_group',methods=['POST'])
        def delete_group():
            params= {
                "sil_ide" : request.json['sil_ide']
            }
            return self.model.delete_group(params)

        @app.route('/get_groups',methods=['POST'])
        def get_groups():
            params = {
                'sil_ide' : request.json['sil_ide']
            }
            return self.model.get_groups(params)

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

        @app.route('/group_info',methods=['POST'])
        def group_info():
            params = {
                'gru_ide' : request.json['gru_ide']
            }    
            return self.model.group_info(params)

        @app.route('/delete_schedule', methods=['POST'])
        def delete_schedule():
            params = {
                'hor_ide' : request.json['hor_ide']
            }
            return self.model.remove(params)

        @app.route('/asignaturas',methods=['POST'])
        def asignaturas():
            return self.model.getAsignaturas()

        @app.route('/aulas',methods=['POST'])
        def aulas():
            return self.model.getAulas()

        @app.route('/excel_horario',methods=['GET'])
        def excel():
            return self.model.export_excel()

        @app.route('/html_horario',methods=['GET'])
        def html():
            return self.model.export_html()
        
        @app.route('/latex_horario',methods=['GET'])
        def latex():
            return self.model.export_latex()

        @app.route('/pdf_horario',methods=['GET'])
        def pdf():
            return self.model.export_pdf()

