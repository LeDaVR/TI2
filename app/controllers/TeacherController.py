from flask import Flask
from flask import request
from flask import jsonify
from flask import flash
from flaskext.mysql import MySQL
from models import TeacherModel
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import click
from flask.cli import with_appcontext

class TeacherController:
    def __init__(self,app,conexion):
        self.model = TeacherModel(conexion)

        @app.route('/schedule_to_chose',methods=['POST'])
        def schedule_to_chose():
            params = {
                'id' : request.json['doc_ide']
            } 
            return self.model.schedule_to_chose(params)

        @app.route('/assign_teacher',methods=['POST'])
        def assign_teacher():
            params = {
                'doc_ide' : request.json['doc_ide'],
                'sil_ide' : request.json['sil_ide'],
                'gru_ide' : request.json['gru_ide'],
                'tipo_clase' : request.json['tipo_clase'],
                'horas' : request.json['horas']
            }
                
            if self.model.can_be_assigned(params):
                return jsonify(self.model.assign_teacher( params ) )
            else:
                return jsonify({ 'status' : 'no se puede asignar' })
        
        @app.route('/unassign_teacher',methods=['POST'])
        def unassign_teacher():
            params = {
                'sil_doc_ide' : request.json['sil_doc_ide']
            }
                
            return jsonify(self.model.unassign( params ) )

        @app.route('/teacher_signature',methods=['POST'])
        def teacher_signature():
            params = {
                'doc_ide' : request.json['doc_ide'],
                'sil_ide' : request.json['sil_ide']
            }
                
            return self.model.teacher_signature(params)


        @app.route('/register_teacher', methods=['POST'])
        def register_teacher():
            params = {
                'nombre' : request.json['nombre'],
                'ape_mat' : request.json['ape_mat'],
                'ape_pat' : request.json['ape_pat'],
                'grad_aca' : request.json['grad_aca'],
                'doc_esp' : request.json['doc_esp'],
                'cat_ide' : request.json['cat_ide'],
                'dep_ide' : request.json['dep_ide']
            }
            return self.model.register(params)

        @app.route('/teachers',methods=['POST'])
        def teachers():
            return self.model.teachers()

        @app.route('/teacher_info',methods=['POST'])
        def teacherinfo():
            params = {
                'id' : request.json['id']
            }
            return self.model.teacher_info(params)