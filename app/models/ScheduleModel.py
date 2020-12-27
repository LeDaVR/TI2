from flask import jsonify
from flaskext.mysql import MySQL
from .conexion import Conexion
import numpy as np
import pandas as pd
from io import BytesIO
from flask import Flask, send_file
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pretty_html_table import build_table
import pdfkit
from latex import build_pdf
from flask import make_response


class ScheduleModel:

    def __init__ ( self ,conexion):
        self.conexion = conexion
    

    def Turno(self, params ):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        query = """ 
                SELECT gru_tur FROM grupo
                WHERE gru_ide = (
                    SELECT gru_ide FROM silabo_docente
                    WHERE sil_doc_ide = %(sil_doc_ide)s
                )
                """
        cursor.execute(query,params)
        turno = cursor.fetchone()[0]

        query = """
                SELECT tipo_clase FROM silabo_docente
                WHERE sil_doc_ide = %(sil_doc_ide)s
                """
        cursor.execute(query,params)
        params['tipo_clase'] = cursor.fetchone()[0]

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
        cursor.execute(query,params)

        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        return result

    def can_insert(self,params):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        # verificando horario disponible para docente
        query = """ 
                SELECT COUNT(hor_ide) 
                FROM horario 
                WHERE (dia = %(dia)s && aul_ide = %(aul_ide)s &&
                hora_entrada = %(hora_entrada)s && hora_salida =  %(hora_salida)s ) ||
                ( 
                SELECT COUNT(h.hor_ide)
                FROM horario h
                INNER JOIN silabo_docente sd
                ON sd.doc_ide = ( SELECT doc_ide FROM silabo_docente 
                                    WHERE sil_doc_ide = %(sil_doc_ide)s 
                                )
                WHERE sd.sil_doc_ide = h.sil_doc_ide && h.dia = %(dia)s &&
                (h.hora_entrada = %(hora_entrada)s && h.hora_salida = %(hora_salida)s)
                )
                """
        cursor.execute(query,params)
        can_insert = not cursor.fetchone()[0]
        
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
        cursor.execute(query,params)
        hor_sin_asig = cursor.fetchone()[0]
        can_insert =  can_insert and hor_sin_asig
        print(can_insert)
        can_insert = can_insert and self.Turno(params)
        print(can_insert)
        cursor.close()
        conn.close()
        if can_insert:
            return True
        return False
    
    def create_schedule(self,params):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        query = """
                INSERT INTO horario (hora_entrada, hora_salida, aul_ide, dia, sil_doc_ide)
                VALUES ( %(hora_entrada)s, %(hora_salida)s, %(aul_ide)s, %(dia)s, %(sil_doc_ide)s)
                """
        cursor.execute(query,params)
        conn.commit()

        content = { 
            'hor_ide' : cursor.lastrowid , 
            'hora_entrada' : params['hora_entrada'], 
            'hora_salida' : params['hora_salida' ], 
            'aul_ide' : params['aul_ide'], 
            'dia' : params['dia'],
            'sil_doc_ide' : params['sil_doc_ide']
        }
        cursor.close()
        conn.close()

        return jsonify(content)

    def get_schedule(self,params):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()

        horas = [
                ('07:00:00','07:50:00'),('07:50:00','08:40:00'),
                ('08:40:00','08:50:00'),('08:50:00','09:40:00'),
                ('09:40:00','10:30:00'),('10:30:00','10:40:00'),
                ('10:40:00','11:30:00'),('11:30:00','12:20:00'),
                ('12:20:00','13:10:00'),('13:10:00','14:00:00'),
                ('14:00:00','14:50:00'),('14:50:00','15:40:00'),
                ('15:40:00','15:50:00'),('15:50:00','16:40:00'),
                ('16:40:00','17:30:00'),('17:30:00','17:40:00'),
                ('17:40:00','18:30:00'),('18:30:00','19:20:00'),
                ('19:20:00','19:30:00'),('19:30:00','20:10:00')
                ]
        data = []
        query = """
                select h.hor_ide,h.hora_entrada,hora_salida,h.dia,d.doc_ide,
                CONCAT(c.cur_nom,' ',sd.tipo_clase,' (',gr.gru_nom,') ',d.doc_nom,' ',d.doc_ape_mat,' ',d.doc_ape_pat) AS content 
                from horario h
                left join silabo_docente sd
                on sd.sil_doc_ide = h.sil_doc_ide
                left join silabo s
                on s.sil_ide = sd.sil_ide
                left join curso c
                on c.cur_ide = s.cur_ide
                left join docente d
                on d.doc_ide = sd.doc_ide
                left join grupo gr
                on gr.gru_ide = sd.gru_ide
                where h.aul_ide =  %(aul_ide)s and s.sil_per_aca = %(sil_per_aca)s
                """
        cursor.execute(query,params)
        rv = cursor.fetchall()

        row_names = ['hora_entrada','hora_salida','lunes','martes','miercoles','jueves','viernes',
        'doc_lun','doc_mar','doc_mie','doc_jue','doc_vie','lun_ide','mar_ide','mie_ide','jue_ide','vie_ide']

        for i in range(len(horas)):
            row = {}
            for j in row_names:
                row[j] = 'None'
            row['hora_entrada'] = horas[i][0]
            row['hora_salida'] = horas[i][1]
            data += [row]

        data_names = data_names = cursor.description
        

        if rv != None:
            for dat in rv:
                temp = {}
                for i in range(len(dat)):
                    temp[data_names[i][0]] = str(dat[i])
                hora = -1
                if len(temp['hora_entrada']) == 7:
                    temp['hora_entrada'] = '0'+temp['hora_entrada']
                for i in range(len(horas)):
                    if (temp['hora_entrada'] == horas[i][0]):
                        hora = i
                        break
                if temp['dia'] == 'Lunes':
                    data[hora]['lunes'] = temp['content']
                    data[hora]['lun_ide'] = temp['hor_ide']
                    data[hora]['doc_lun'] = temp['doc_ide']
                if temp['dia'] == 'Martes':
                    data[hora]['martes'] = temp['content']
                    data[hora]['mar_ide'] = temp['hor_ide']
                    data[hora]['doc_mar'] = temp['doc_ide']
                if temp['dia'] == 'Miercoles':
                    data[hora]['miercoles'] = temp['content']
                    data[hora]['mie_ide'] = temp['hor_ide']
                    data[hora]['doc_mie'] = temp['doc_ide']
                if temp['dia'] == 'Jueves':
                    data[hora]['jueves'] = temp['content']
                    data[hora]['jue_ide'] = temp['hor_ide']
                    data[hora]['doc_jue'] = temp['doc_ide']
                if temp['dia'] == 'Viernes':
                    data[hora]['viernes'] = temp['content']
                    data[hora]['vie_ide'] = temp['hor_ide']
                    data[hora]['doc_vie'] = temp['doc_ide']
                        
        cursor.close()
        conn.close()
        return jsonify(data)



    def remove(self, params):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        query = """ delete from horario where hor_ide = %(hor_ide)s;"""
        cursor.execute(query, params)
        conn.commit()

        data = {
            'result' : cursor.lastrowid
        }

        cursor.close()
        conn.close()
        return jsonify(data)
    
    def create_group(self,params):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()

        query = """
                SELECT COUNT(gru_ide) FROM grupo
                WHERE sil_ide = %(sil_ide)s
                """
        cursor.execute(query,params)
        letter = chr(ord("A")+cursor.fetchone()[0])

        data = []
        for i in range(int(params['cantidad'])):
            params['gru_nom'] = letter
            params['gru_tur'] = ('Mañana') if ord(letter)%2 != 0 else ('Tarde')
            query = """
                    INSERT INTO grupo(gru_nom,gru_tur,sil_ide) VALUES
                    (%(gru_nom)s,%(gru_tur)s,%(sil_ide)s);
                    """
            cursor.execute(query,params)
            conn.commit()
            letter = chr(ord(letter)+1)

            data += [{
                'gru_ide' : cursor.lastrowid,
                'gru_nom' : params['gru_nom'],
                'gru_tur' : params['gru_tur'],
                'sil_ide' : params['sil_ide']
            }]
        
        cursor.close()
        conn.close()

        return jsonify(data)
    
    def delete_group(self,params):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()

        query = """
                SELECT COUNT(gru_ide) FROM grupo
                WHERE sil_ide = %(sil_ide)s
                """
        cursor.execute(query,params)
        letter = chr(ord("A")+cursor.fetchone()[0]-1)
        params['gru_nom'] = letter

        query = """
                DELETE FROM grupo WHERE gru_nom = %(gru_nom)s && sil_ide = %(sil_ide)s;
                """
        cursor.execute(query,params)
        conn.commit()

        data = {
            'result' : cursor.lastrowid
        }
        
        cursor.close()
        conn.close()

        return jsonify(data)

    def getAsignaturas(self):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        query = """
                SELECT s.sil_ide,c.cur_nom FROM silabo s
                INNER JOIN curso c
                ON s.cur_ide = c.cur_ide
                """
        cursor.execute(query)
        rv = cursor.fetchall()
        data_names = data_names = cursor.description
        if rv is None:
            data = None
        else:
            data = [] 
            for i in range(len(rv)):
                data.append({})
                for j in range(len(rv[i])):
                    (data[i])[data_names[j][0]] = str(rv[i][j]) 
        cursor.close()
        conn.close()
        return jsonify(data)

    def get_groups(self,params):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        query = """
                SELECT gru_ide,gru_nom FROM grupo
                WHERE sil_ide = %(sil_ide)s
                """
        cursor.execute(query,params)
        rv = cursor.fetchall()
        data_names = data_names = cursor.description
        print(rv)
        if rv is None:
            data = None
        else:
            data = [] 
            for i in range(len(rv)):
                data.append({})
                for j in range(len(rv[i])):
                    (data[i])[data_names[j][0]] = str(rv[i][j]) 
        print(data)
        cursor.close()
        conn.close()
        return jsonify(data)
    
    def group_info(self,params):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        query = """    
                SELECT p.doc_nom AS doc_pra,l.doc_nom AS doc_lab,t.doc_nom AS doc_teo,
	                p.sil_doc_ide AS ide_pra,l.sil_doc_ide AS ide_lab,t.sil_doc_ide AS ide_teo
                FROM silabo_docente s
                LEFT JOIN ( 
	                SELECT CONCAT(d.doc_nom," ",d.doc_ape_pat," ",d.doc_ape_mat) as doc_nom ,s.gru_ide,s.sil_doc_ide FROM silabo_docente s 
	                LEFT JOIN docente d ON d.doc_ide = s.doc_ide
	                WHERE s.tipo_clase ="Práctica" ) p
                ON p.gru_ide = s.gru_ide
                LEFT JOIN ( 
	                SELECT CONCAT(d.doc_nom," ",d.doc_ape_pat," ",d.doc_ape_mat) as doc_nom ,s.gru_ide,s.sil_doc_ide FROM silabo_docente s 
	                LEFT JOIN docente d ON d.doc_ide = s.doc_ide 
	                WHERE s.tipo_clase ="Laboratorio" ) l
                ON l.gru_ide = s.gru_ide
                LEFT JOIN ( 
	                SELECT CONCAT(d.doc_nom," ",d.doc_ape_pat," ",d.doc_ape_mat) as doc_nom ,s.gru_ide,s.sil_doc_ide FROM silabo_docente s 
	                LEFT JOIN docente d ON d.doc_ide = s.doc_ide 
	                WHERE s.tipo_clase ="Teoría" ) t
                ON t.gru_ide = s.gru_ide
                WHERE s.gru_ide = %(gru_ide)s LIMIT 1;
                """
        cursor.execute(query,params)
        rv = cursor.fetchone()
        data_names = data_names = cursor.description

        if rv is None:
            rv = {}
        data = {}
        for i in range(len(data_names)):
                data[data_names[i][0]] = "None"
        for i in range(len(rv)):
                data[data_names[i][0]] = str(rv[i]) 

        query = """
                select c.cur_hor_teo AS hor_teo,c.cur_hora_pra as hor_pra,c.cur_hor_lab as hor_lab from curso c
                inner join grupo g
                on g.gru_ide = %(gru_ide)s
                inner join silabo s
                on s.sil_ide = g.sil_ide
                where c.cur_ide = s.cur_ide;
                """
        cursor.execute(query,params)
        rv = cursor.fetchone()
        data_names = data_names = cursor.description
        for i in range(len(rv)):
                data[data_names[i][0]] = str(rv[i]) 

        print(data)
        cursor.close()
        conn.close()
        return jsonify(data)

    def getAulas(self):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        query = """
                SELECT aul_ide, CONCAT(tipo," ",aul_num) as aul_nom FROM aula
                WHERE aul_ava = 1 
                """
        cursor.execute(query)
        rv = cursor.fetchall()
        data_names = data_names = cursor.description
        print(rv)
        if rv is None:
            data = None
        else:
            data = [] 
            for i in range(len(rv)):
                data.append({})
                for j in range(len(rv[i])):
                    (data[i])[data_names[j][0]] = str(rv[i][j]) 
        print(data)
        cursor.close()
        conn.close()
        return jsonify(data)

    def horario_array(self,datos):
        
        array = []
        for i in range(len(datos)):
            default = ''
            if i == 2 or i==5 or i==12 or i == 15 or i == 18:
                default = "DESCANSO"
            arr = []
            arr += [default if (datos[i]['lunes'] == 'None') else datos[i]['lunes']]
            arr += [default if (datos[i]['martes'] == 'None') else datos[i]['martes']]
            arr += [default if (datos[i]['miercoles'] == 'None') else datos[i]['miercoles']]
            arr += [default if (datos[i]['jueves'] == 'None') else datos[i]['jueves']]
            arr += [default if (datos[i]['viernes'] == 'None') else datos[i]['viernes']]
            array += [arr]
        
        return np.array(array)
    
    def horario_index(self,datos):
        array = []
        for i in datos:
            arr = []
            time = i['hora_entrada'][0:5]+"-"+i['hora_salida'][0:5]
            arr += [time]
            array += arr
        
        return array

    def export_excel(self):

        aulas = self.getAulas().json
        params = {
            "sil_per_aca" : "2020-B",
        }

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        

        for i in aulas:
            params['aul_ide'] = i['aul_ide']
            params['aul_nom'] = i['aul_nom']
            columnas = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES"]
            
            datos = self.get_schedule(params).json

            info = self.horario_array(datos)
            index = self.horario_index(datos)

            df_1 = pd.DataFrame(info, columns=columnas,index = index)
            print(df_1)
            
            df_1.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = params['aul_nom'])
            workbook = writer.book
            worksheet = writer.sheets[params['aul_nom']]
            format1 = workbook.add_format({'text_wrap': True,'font_name' : 'Arial', 
                                        'font_size' : 8,'align' : 'center' , 'valign' : 'center'})
            format2 = workbook.add_format({'text_wrap': True,'font_name' : 'Arial', 
                                        'font_size' : 8,'align' : 'center' , 'valign' : 'center',
                                        'border' : 1})
            format3 = workbook.add_format({ 'text_wrap': True,'font_name' : 'Arial', 
                                        'font_size' : 8,'align' : 'center' , 'valign' : 'center',
                                        'bg_color' : '#d3d3d3',})

            worksheet.set_column('A:A',10,format1)
            worksheet.set_column('B:F',30,format1)
            descansos = [4,7,14,17,20]
            worksheet.conditional_format('A1:F21', {'type' : 'no_blanks', 'format' : format2})
            worksheet.conditional_format('A1:F21', {'type' : 'blanks', 'format' : format2})
            for i in descansos:
                worksheet.conditional_format('A'+str(i)+':F'+str(i), {'type' : 'no_blanks', 'format' : format3})
            
        writer.close()
        output.seek(0)
        return send_file(output, attachment_filename="horario.xlsx", as_attachment=True)
    
    def export_html(self):
        html = self.htmlstring()

        output = BytesIO()
        output.write(html.encode('utf-8'))

        output.seek(0)
        
        return send_file(output , attachment_filename="horario.html", as_attachment=True)

    def export_pdf(self):
        html = self.htmlstring()

        output = BytesIO()
        html.encode('utf-8')
        pdf = pdfkit.from_string(html ,False)
        output.write(pdf)

        output.seek(0)
        response = make_response(pdf)
        response.headers['Content-Type'] = "application/pdf; charset=utf-32"
        response.headers['Content-Disposition'] = "inline;filename=output.pdf"

        return send_file(output , attachment_filename="horario.pdf", as_attachment=True)

    def export_latex(self):
        aulas = self.getAulas().json
        params = {
            "sil_per_aca" : "2020-B",
        }

        output = BytesIO()

        latex = ""
        for i in aulas:
            params['aul_ide'] = i['aul_ide']
            params['aul_nom'] = i['aul_nom']

            latex += "\\section{"+params['aul_nom']+"}"
            columnas = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES"]
            
            datos = self.get_schedule(params).json

            info = self.horario_array(datos)
            index = self.horario_index(datos)
            
            df_1 = pd.DataFrame(info, columns=columnas, index = index)
            latex += df_1.to_latex()

        output.write(latex.encode('utf-8'))
        
        output.seek(0)
        pdf = build_pdf(output)
        pdf.save_to('ga.pdf')

        return send_file(output , attachment_filename="horario.html", as_attachment=True)

    def htmlstring(self):
        aulas = self.getAulas().json
        params = {
            "sil_per_aca" : "2020-B",
        }
        html = """
            <head>
            <style>
            
            #horario {
                font-family: Arial, Helvetica, sans-serif;
                border-collapse: collapse;
                margin-left: auto;
                margin-right: auto;
                width:90%;
                table-layout:fixed;
            }

            #horario td, #horario th {
                text-align: center;
                font-size: 12px;
                border: 1px solid #ddd;
                padding: 8px;
            }

            #horario tr:nth-child(3){background-color: #909090 ; color: #FFFFFF;}
            #horario tr:nth-child(6){background-color: #909090 ;color: #FFFFFF;}
            #horario tr:nth-child(13){background-color: #909090 ;color: #FFFFFF;}
            #horario tr:nth-child(16){background-color: #909090 ;color: #FFFFFF;}
            #horario tr:nth-child(19){background-color: #909090 ;color: #FFFFFF;}

            #horario thead {
                padding-top: 12px;
                padding-bottom: 12px;
                text-align: center;
                background-color: #990537;
                font-family: Arial;
                font-size: 12px;
                color: #FFFFFF;
            }
            </style>
            </head>
        """
        for i in aulas:
            params['aul_ide'] = i['aul_ide']
            params['aul_nom'] = i['aul_nom']
            html += "<div style= \"font-family: Arial;font-size: 20px;text-align: center;\">"+params['aul_nom']+"</div>"

            columnas = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES"]
            
            datos = self.get_schedule(params).json

            info = self.horario_array(datos)
            index = self.horario_index(datos)

            new_info = []
            for i in range(len(index)):
                line = [index[i]]
                for j in range(len(info[i])):
                    line += [info[i][j]]
                new_info += [line]
            
            df_1 = pd.DataFrame(info, columns=columnas,index = index)
            tabletipe2 = df_1.to_html()
            index = 0
            for i in range(len(tabletipe2)):
                if tabletipe2[i] == '>':
                    index = i
                    break
            tabletipe2 = "<table id=\"horario\">" + tabletipe2[i+1:len(tabletipe2)]

            html += "<div>"
            html += tabletipe2
            html += "</div>"

        return html