from flask import Flask
from flask import jsonify
from flaskext.mysql import MySQL
from controllers import *
from models import Conexion
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

app = Flask(__name__)
conexion = Conexion(app)
userController = UserController(app,conexion)
scheduleController = ScheduleController(app,conexion)
teacherController = TeacherController(app,conexion)

@app.route('/')
def base():
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key = 'some secret key'
    app.run('0.0.0.0',debug=True) 
