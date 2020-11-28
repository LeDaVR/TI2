from flask import jsonify
from flaskext.mysql import MySQL
from .conexion import Conexion

class ScheduleModel:

    def __init__ ( self ,app ):
        self.conexion = Conexion(app)
    

    def Turno(self, params ):
        query = """ 
                SELECT gru_tur FROM grupo
                WHERE gru_ide = (
                    SELECT gru_ide FROM silabo_docente
                    WHERE sil_doc_ide = %(sil_doc_ide)s
                )
                """
        self.conexion.cursor.execute(query,params)
        turno = self.conexion.cursor.fetchone()[0]
        verify = 1

        if turno == "Tarde"  and params['tipo_clase'] != 'Laboratorio' :
            verify = 0
        elif turno == "Mañana" and params['tipo_clase'] == 'Laboratorio':
            verify = 0
        
        if verify:
            params['ini_tur'] = '07:00:00'
            params['fin_tur'] = '14:00:00'
        else:
            params['ini_tur'] = '14:00:00'
            params['fin_tur'] = '20:10:00'
        
        query = """
                SELECT ( %(hora_entrada)s >= %(ini_tur)s &&
                         %(hora_salida)s <= %(fin_tur)s
                        )
                """
        self.conexion.cursor.execute(query,params)

        return self.conexion.cursor.fetchone()[0]

    def can_insert(self,params):

        # verificando horario disponible para docente
        query = """ 
                SELECT COUNT(hor_ide) 
                FROM horario 
                WHERE (dia = %(dia)s && aul_ide = %(aul_ide)s &&
                (hora_entrada <= %(hora_salida)s || hora_salida <= %(hora_entrada)s)) ||
                ( 
                SELECT COUNT(h.hor_ide)
                FROM horario h
                INNER JOIN silabo_docente sd
                ON sd.doc_ide = ( SELECT doc_ide FROM silabo_docente 
                                    WHERE sil_doc_ide = %(sil_doc_ide)s 
                                )
                WHERE sd.sil_doc_ide = h.sil_doc_ide && h.dia = %(dia)s &&
                (h.hora_entrada <= %(hora_salida)s || h.hora_salida <= %(hora_salida)s)
                )
                """
        self.conexion.cursor.execute(query,params)
        can_insert = not self.conexion.cursor.fetchone()[0]
        print(can_insert)

        # verificando si hay horas sin horario asignado 
        query =  """
                SELECT ( COALESCE(SUM(TIME_TO_SEC(h.hora_salida)-TIME_TO_SEC(h.hora_entrada)),0) + 
                        TIME_TO_SEC(%(hora_salida)s)-TIME_TO_SEC(%(hora_entrada)s)   
                        <=  sd.horas  * 3000 ) as "insert"
                FROM horario h
                INNER JOIN silabo_docente sd
                ON sd.sil_doc_ide = %(sil_doc_ide)s
                WHERE h.sil_doc_ide = %(sil_doc_ide)s
                """
        self.conexion.cursor.execute(query,params)
        hor_sin_asig = self.conexion.cursor.fetchone()[0]
        can_insert =  can_insert and hor_sin_asig
        can_insert = can_insert and self.Turno(params)
        
        if can_insert:
            return True
        return False
    
    def create_schedule(self,params):
        query = """
                INSERT INTO horario (hora_entrada, hora_salida, aul_ide, dia, sil_doc_ide)
                VALUES ( %(hora_entrada)s, %(hora_salida)s, %(aul_ide)s, %(dia)s, %(sil_doc_ide)s)
                """
        self.conexion.cursor.execute(query,params)
        self.conexion.conn.commit()

        content = { 
            'hor_ide' : self.conexion.cursor.lastrowid , 
            'hora_entrada' : params['hora_entrada'], 
            'hora_salida' : params['hora_salida' ], 
            'aul_ide' : params['aul_ide'], 
            'dia' : params['dia'],
            'sil_doc_ide' : params['sil_doc_ide']
        }

        return jsonify(content)

    def get_schedule(self,params):
        query = """
                SELECT  sd.tipo_clase as "tipo clase",
                        g.gru_nom as "grupo",
                        h.hora_entrada as "hora entrada",
                        h.hora_salida as "hora salida",
                        h.aul_ide as "aula",
                        h.dia as "dia"
                FROM silabo_docente sd
                LEFT JOIN grupo g
                on sd.gru_ide = g.gru_ide
                LEFT JOIN horario h
                on sd.sil_doc_ide = h.sil_doc_ide
                inner join silabo s
                on s.sil_per_aca = %(sil_per_aca)s 
                WHERE sd.sil_ide = s.sil_ide
                """
        self.conexion.cursor.execute(query,params)
        rv = self.conexion.cursor.fetchall()
        data_names = data_names = self.conexion.cursor.description
        print(rv)
        if rv is None:
            data = None
        else:
            data = [] 
            for i in range(len(rv)):
                data.append({})
                for j in range(len(rv[i])):
                    (data[i])[data_names[j][0]] = str(rv[i][j]) 
        return jsonify(data)

    def remove(self, params):
        query = """ delete from horario where hor_ide = %(hor_ide)s;"""
        self.conexion.cursor.execute(query, params)
        self.conexion.conn.commit()

        data = {
            'result' : self.conexion.cursor.lastrowid , 
        }
        return jsonify(data)
    
    def create_group(self,params):
        query = """
                SELECT COUNT(gru_ide) FROM grupo
                WHERE sil_ide = %(sil_ide)s
                """
        self.conexion.cursor.execute(query,params)
        letter = chr(ord("A")+self.conexion.cursor.fetchone()[0])

        data = []
        for i in range(int(params['cantidad'])):
            params['gru_nom'] = letter
            params['gru_tur'] = ('Mañana') if ord(letter)%2 != 0 else ('Tarde')
            query = """
                    INSERT INTO grupo(gru_nom,gru_tur,sil_ide) VALUES
                    (%(gru_nom)s,%(gru_tur)s,%(sil_ide)s);
                    """
            self.conexion.cursor.execute(query,params)
            self.conexion.conn.commit()
            letter = chr(ord(letter)+1)

            data += [{
                'gru_ide' : self.conexion.cursor.lastrowid,
                'gru_nom' : params['gru_nom'],
                'gru_tur' : params['gru_tur'],
                'sil_ide' : params['sil_ide']
            }]

        return jsonify(data)