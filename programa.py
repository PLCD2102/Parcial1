from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2  # O mysql.connector para MySQL

app = Flask(__name__)  # Aquí estaba el error
CORS(app)

# Configuración de la base de datos (reemplaza con tus credenciales y la IP de la base de datos)
db_config = {
    'dbname': 'users',
    'user': 'parcial',
    'password': '123',
    'host': '52.200.14.166',  # IP de tu instancia EC2 de la base de datos
    'port': '5432'
}

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    return psycopg2.connect(**db_config)

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        nombres = data['nombres']
        apellidos = data['apellidos']
        fecha_nacimiento = data['fecha_nacimiento']
        password = data['password']
        
        # Insertar en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (nombres, apellidos, fecha_nacimiento, password) VALUES (%s, %s, %s, %s)",
            (nombres, apellidos, fecha_nacimiento, password)
        )
        conn.commit()
        cursor.close()
        conn.close()  # Cerrar conexión
        
        return jsonify({"message": "Usuario registrado exitosamente"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombres, apellidos FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()  # Cerrar conexión
        
        return jsonify(users)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':  # También había un error aquí
    app.run(host='0.0.0.0', port=5000)
