import mysql.connector
import string
import random
import subprocess
import threading
import shutil
import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

API_KEY = "idan"

def check_api_key():
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        abort(403)

def generate_license(admin, resource_name):
    length = 12
    characterList = string.ascii_letters + string.digits

    password = ''.join(random.choice(characterList) for _ in range(length))
    license_key = f"{admin}-{password}-{resource_name}"
    return license_key

def execute_powershell(command):
    process = subprocess.Popen(
        ["powershell", "-Command", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    output, error = process.communicate()
    if error:
        return {"status": "error", "output": error}
    else:
        return {"status": "success", "output": output}

@app.route('/generate_license', methods=['POST'])
def generate_license_key():
    check_api_key()

    data = request.get_json()
    admin = data['admin']
    resource_name = data['resource_name']

    license_key = generate_license(admin, resource_name)

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="license"
    )
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO licenses (ip_address, license_key, resource_name) VALUES (%s, %s, %s)''',
                   (admin, license_key, resource_name))

    conn.commit()
    conn.close()

    powershell_command = f"Write-Output 'License generated for {admin}'"
    ps_result = execute_powershell(powershell_command)

    return jsonify({
        "message": "License generated successfully.",
        "license_key": license_key,
        "powershell_output": ps_result
    })


@app.route('/check_license', methods=['POST'])
def check_license():

    data = request.get_json()
    license_key = data['license_key']

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="license"
    )
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM licenses WHERE license_key = %s''', (license_key,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return jsonify({"valid": True, "message": "License is valid."})
    else:
        return jsonify({"valid": False, "message": "License is invalid."})

@app.route('/remove_license', methods=['POST'])
def remove_license():
    check_api_key()

    data = request.get_json()
    license_key = data['license_key']

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="license"
    )
    cursor = conn.cursor()

    cursor.execute('''DELETE FROM licenses WHERE license_key = %s''', (license_key,))
    conn.commit()

    if cursor.rowcount > 0:
        message = "License removed successfully."
    else:
        message = "License not found."

    conn.close()
    
    return jsonify({"message": message})

@app.route('/list_licenses', methods=['GET'])
def list_licenses():
    check_api_key()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="license"
    )
    cursor = conn.cursor()

    cursor.execute('''SELECT license_key, resource_name FROM licenses''')
    result = cursor.fetchall()

    licenses = [{"license_key": row[0], "resource_name": row[1]} for row in result]

    conn.close()

    return jsonify({"licenses": licenses})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
