from flask import Flask
from flask import jsonify
from flaskext.mysql import MySQL
from controllers import *
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

app = Flask(__name__)
userController = UserController(app)
scheduleController = ScheduleController(app)
teacherController = TeacherController(app)

@app.route('/')
def base():
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key = 'some secret key'
    app.run(debug=True) 
