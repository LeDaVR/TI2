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
    def __init__(self,app):
        self.model = TeacherModel(app)

        @app.route('/teacher_edit')
        def edit():
            print(session)
            if session['user_id'] != None:
                data = self.model.courses(session['user_id'])
                flash(data)
                return render_template('schedules_edit.html')
            else:
                redirect(url_for('login'))
        

        @app.route('/assign_teacher',methods=['POST'])
        def assign_teacher():
            doc_ide = request.json['doc_ide']
            sil_ide = request.json['sil_ide']
            gru_ide = request.json['gru_ide']
            tipo_clase = request.json['tipo_clase']
            horas = request.json['horas']

            if self.model.can_be_assigned(doc_ide,horas):
                return jsonify(self.model.assign_teacher(tipo_clase,horas, gru_ide,doc_ide,sil_ide ) )
            else:
                return jsonify({ 'status' : 'hours_limit_exceded' })

        @app.route('/register_teacher',methods=['POST'])
        def register_teacher():
            return 1
