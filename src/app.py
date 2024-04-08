from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL
from validaciones import *
app=Flask(__name__)

conexion=MySQL(app)


@app.route('/index', methods=['GET'])
def listar_personajes():
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT codigo, nombre, rango FROM personajes"
        cursor.execute(sql)
        resultado=cursor.fetchall()
        personajes=[]
        for fila in resultado:
            perso={'codigo':fila[0], 'nombre':fila[1], 'rango':fila[2]}
            personajes.append(perso)
        return jsonify({'personajes':personajes, 'mensaje':"personajes listados."})
    except Exception as e:
        return jsonify({'error': "Error al realizar la consulta" + str(e)})
    
def leer_personajes(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, rango FROM personajes WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            curso = {'codigo': datos[0], 'nombre': datos[1], 'rango': datos[2]}
            return curso
        else:
            return None
    except Exception as ex:
        raise ex

        

@app.route('/index/<codigo>', methods = ['GET'])
def buscar_personaje (codigo):
    try:
        pers = leer_personajes(codigo)
        if pers != None:
            return jsonify({'personaje': pers, 'mensaje': "personaje encontrado."})
        else:
            return jsonify({'mensaje': "personaje no encontrado."})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
    
    
@app.route('/index', methods=['POST'])
def crear_personaje():
        rango_valido = validar_rango(request.json['rango'])
        print("Validación de rango:", rango_valido)
        if (validar_codigo(request.json['codigo']) and validar_nombre(request.json['nombre']) and validar_rango(request.json['rango'])):
            try: 
                pers = leer_personajes(request.json['codigo'])
                if pers != None:
                    return jsonify({'mensaje': "El Código ya existe, no se puede duplicar."})
                else:
                    cursor= conexion.connection.cursor()
                    sql = "INSERT INTO personajes (codigo, nombre, rango) VALUES ('{0}', '{1}', {2})".format(request.json['codigo'],request.json['nombre'], request.json['rango'])
                    cursor.execute(sql)
                    conexion.connection.commit()  # Confirma la acción de inserción.
                    return jsonify({'mensaje': "personaje registrado."})
            except Exception as ex:
                return jsonify({'mensaje': "Error" })
        else:
            return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False} )    

@app.route('/index/<codigo>', methods=['DELETE'])
def eliminar_personaje(codigo):
    try:
        pers = leer_personajes(codigo)
        if pers != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM personajes WHERE codigo = '{0}'".format(codigo)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de eliminación.
            return jsonify({'mensaje': "personaje eliminado."})
        else:
            return jsonify({'mensaje': "personaje no encontrado."})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/index/<codigo>', methods=['PUT'])
def actualizar_personaje(codigo):
    if (validar_codigo(codigo) and validar_nombre(request.json['nombre']) and validar_rango(request.json['rango'])):
        try:
            pers = leer_personajes(codigo)
            if pers != None:
                cursor = conexion.connection.cursor()
                sql = "UPDATE personajes SET nombre = '{0}', rango = {1} WHERE codigo = '{2}'".format(request.json['nombre'], request.json['rango'], codigo)
                cursor.execute(sql)
                conexion.connection.commit()  # Confirma la acción de actualización.
                return jsonify({'mensaje': "personaje actualizado."})
            else:
                return jsonify({'mensaje': "personaje no encontrado."})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos"})
    

def pag_no_encontrada(error):
    return "<h1>La pagina no existe</h1>", 404





if __name__=='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,pag_no_encontrada)
    app.run()

