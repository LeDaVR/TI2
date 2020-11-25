from flask import jsonify
from flaskext.mysql import MySQL
from .conexion import Conexion

class ScheduleModel:

    def __init__ ( self ,app ):
        self.conexion = Conexion(app)
    

    def Turno(self,sil_doc_ide,tipo_clase):
        query = """ 
                SELECT COUNT(*) FROM grupo g
                WHERE sil_ide = (
                    SELECT sil_ide FROM silabo_docente
                    WHERE sil_doc_ide = %(sil_doc_ide)s
                )
                """
        turno = "Mañana"
        self.conexion.cursor.execute(query)
        result = self.conexion.fetchone()[0]
        if result == 1:
            return "Sin Definir"
        elif not result%2 and tipo_clase != 'Laboratorio':
            turno = 'Tarde'
        elif result%2 and tipo_clase == 'Laboratorio':
            turno = 'Tarde'
        return Turno



    def can_insert(self,hora_entrada,hora_salida,dia,aula,sil_doc_ide):
        params = {
            'hora_entrada' : hora_entrada,
            'hora_salida' : hora_salida,
            'dia' : dia,
            'aula' : aula
        }

        query = """ SELECT COUNT(hor_ide) 
                    FROM horario
                    WHERE dia = %(dia)s && aula = %(aula)s &&
                    (hora_entrada <= %(hora_salida)s || hora_salida <= %(hora_entrada)s) """

        self.conexion.cursor.execute(query,params)

        result = self.conexion.cursor.fetchone()

        if result[0] == 0:
            return True
        return False
    