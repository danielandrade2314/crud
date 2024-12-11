from flask import Flask
from flask_cors import CORS
from flask import jsonify, request
import pymysql

app = Flask(__name__)  # Crea una instancia de la aplicación Flask

# Permite acceder desde una API externa
CORS(app)

# Función para conectarse a la base de datos MySQL
def conectar(vhost, vuser, vpass, vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn

# Ruta para consulta general del baúl de contraseñas
@app.route("/")
def consulta_general():
    try: # sirve para manejar errores
        conn = conectar('localhost', 'root', '052312', 'gestor_contrasena') # Establece la conexión con la base de datos MySQL usando los parámetros proporcionados.
        cur = conn.cursor() # Crea un cursor para ejecutar consultas SQL.
        cur.execute("""SELECT * FROM baul""") # Ejecuta una consulta SQL para obtener todos los registros de la tabla "baul".
        datos = cur.fetchall() # Obtiene todos los resultados de la consulta y los almacena en "datos".
        data = [] # Inicializa una lista vacía para almacenar los datos en formato de diccionario.

        for row in datos: # Itera sobre cada fila de los resultados de la consulta.
            dato = {'id_baul': row[0],  # ID único del registro.
                    'Plataforma': row[1],  # Nombre de la plataforma (ejemplo: "Facebook").
                     'usuario': row[2],    # Nombre de usuario asociado a la plataforma.
                     'clave': row[3]}  # Contraseña asociada al usuario.
            
            data.append(dato)   # Agrega el diccionario a la lista "data".

        cur.close() # para cerrar el cursor
        conn.close() # para cerrar la conexion con la base de datos
        return jsonify({'baul': data, 'mensaje': 'Baúl de contraseñas'}) # para devolver los valores encontrados
    except Exception as ex: #
        return jsonify({'mensaje': 'Error sin datos'})

# Ruta para consulta individual de un registro en el baúl
@app.route("/consulta/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    try:
        conn = conectar('localhost', 'root', '052312', 'gestor_contrasena') # conexiond
        cur = conn.cursor()
        cur.execute("""SELECT * FROM baul where id_baul='{}'""".format(codigo))
        datos = cur.fetchone()  # Recupera la primera fila del resultado de la consulta SQL
        cur.close()
        conn.close()
        return jsonify(datos)
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})
#Ruta para registrar un nuevo registro en el baúl
@app.route("/registro/", methods=['POST'])
def registro():
    try:
        conn = conectar('localhost', 'root', '052312', 'gestor_contrasena')
        cur = conn.cursor()
        x = cur.execute("""
            INSERT INTO baul (plataforma, usuario, clave)
            VALUES (%s, %s, %s)
        """, (request.json['plataforma'], request.json['usuario'], request.json['clave']))
        conn.commit()  # Para confirmar la inserción de la información
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})
#Ruta para eliminar un registro específico en el baúl
@app.route("/eliminar/<codigo>", methods=['DELETE'])
def eliminar(codigo):
    try:
        conn = conectar('localhost', 'root', '052312', 'gestor_contrasena')
        cur = conn.cursor()
        x = cur.execute("""
            DELETE FROM baul WHERE id_baul=%s
        """, (codigo,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})
#Ruta para actualizar un registro específico en el baúl
@app.route("/actualizar/<codigo>", methods=['PUT'])
def actualizar(codigo):
    try:
        # Conexión a la base de datos
        conn = conectar('localhost', 'root', '052312', 'gestor_contrasena')
        cur = conn.cursor()

        # Consulta SQL para actualizar un registro
        x = cur.execute("""
            UPDATE baul
            SET plataforma=%(plataforma)s, usuario=%(usuario)s, clave=%(clave)s
            WHERE id_baul=%(id_baul)s
        """, {
            'plataforma': request.json['plataforma'],
            'usuario': request.json['usuario'],
            'clave': request.json['clave'],
            'id_baul': codigo
        })

        # Confirmar los cambios
        conn.commit()
        cur.close()
        conn.close()

        # Retornar un mensaje de éxito
        return jsonify({'mensaje': 'Registro Actualizado'})

    except Exception as ex:
        # Manejar excepciones
        print(ex)
        return jsonify({'mensaje': 'Error'})
    
if __name__ == '__main__':
    app.run(debug=True)