from flask import jsonify
from flaskext.mysql import MySQL 



class Conexion:
    def __init__ ( self , app ):
        self.mysql = MySQL()
        app.config[ 'MYSQL_DATABASE_USER'] = 'root'
        app.config[ 'MYSQL_DATABASE_PASSWORD'] = 'root'
        app.config[ 'MYSQL_DATABASE_DB'] = 'TI2'
        app.config[ 'MYSQL_DATABASE_HOST'] = '127.0.0.1'
        self.mysql.init_app(app)


    def getConexion(self):
        return self.mysql.connect()


    
