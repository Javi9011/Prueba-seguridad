from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import json
import requests
import datetime
import re


from waitress import serve

from Controladores.ControladorUsuario import ControladorUsuario
from Controladores.ControladorRol import ControladorRol
from Controladores.ControladorPermiso import ControladorPermiso
from Controladores.ControladorPermisosrol import ControladorPermisosrol

controladorUsuario = ControladorUsuario()
controladorRol = ControladorRol()
controladorPermiso = ControladorPermiso()
controladorPermisorol = ControladorPermisosrol()

app=Flask(__name__)
cors=CORS(app)

#Seguridad con JWT
app.config["JWT_SECRET_KEY"]="super-secret"
jwt = JWTManager(app)

@app.before_request
def middleware():

    urlAcceso = request.path
    if (urlAcceso == "/login"):
        pass
    else:
        verify_jwt_in_request()

        infoUsuario = get_jwt_identity()
        idRol = infoUsuario["rol"]["_id"]

        urlAcceso = transformarUrl(urlAcceso)

        urlValidarPermiso = dataConfig["url-backend"] + "/permisos-rol/validar-permiso/rol/" + idRol
        headersValidarPermiso = {"Content-Type": "application/json"}
        bodyValidarPermiso = {
            "url": urlAcceso,
            "metodo": request.method
        }
        respuestaValidarPermiso = requests.get(urlValidarPermiso, json=bodyValidarPermiso, headers=headersValidarPermiso)
        print("Respuesta validar permiso: ", respuestaValidarPermiso)

        if (respuestaValidarPermiso.status_code == 200):
            pass
        else:
            return {"mensaje": "Acceso Denegado"}, 401

def transformarUrl(urlAcceso):
    print("Url antes de transformarla: ", urlAcceso)

    partes = urlAcceso.split("/")
    print("La url dividida es:", partes)
    for palabra in partes:
        if re.search('\\d', palabra):
            urlAcceso = urlAcceso.replace(palabra, "?")

    print("Url después de transformarla:", urlAcceso)
    return urlAcceso

@app.route("/login", methods=["POST"])
def validarUsuario():

    url = dataConfig["url-backend"] + "/usuarios/validar-usuario"
    headers = {"Content-Type": "application/json"}
    bodyRequest = request.get_json()

    response = requests.post(url, json=bodyRequest, headers=headers)

    if (response.status_code == 200):
        print("El usuario se valido correctamente")
        infoUsuario = response.json()

        tiempoToken = datetime.timedelta(seconds=60*60)
        newToken = create_access_token(identity=infoUsuario, expires_delta=tiempoToken)

        return {"token": newToken}
    else:
        return {"mensaje": "Usuario y contraseña ERRONEOS"}, 401


@app.route("/votante", methods=["POST"])
def creandoVotante():
    url = dataConfig["url-backend"] + "/votante"
    headers = {"Content-Type": "application/json"}
    body = request.get_json()

    response = requests.post(url, json=body, headers=headers)

    return response.json()

@app.route("/votante/<string:id>", methods=['GET'])
def buscarUnVotante(id):
    url = dataConfig["url-backend"] + "/votante/" + id
    headers = {"Content-Type": "application/json"}

    response = requests.get(url, headers=headers)

    return response.json()

@app.route("/votante", methods=['GET'])
def buscarTodosLosVotantes():
    url = dataConfig["url-backend"] + "/votante"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()

@app.route("/votante", methods=['PUT'])
def actualizandoUnVotante():
    url = dataConfig["url-backend"] + "/votante"
    headers = {"Content-Type": "application/json"}
    body = request.get_json()

    response = requests.put(url, json=body, headers=headers)
    return response.json()

@app.route("/votante/<string:id>", methods=['DELETE'])
def eliminarVotante(id):
    url = dataConfig["url-backend"] + "/votante/"+id
    headers = {"Content-Type": "application/json"}

    response = requests.delete(url, headers=headers)
    return response.json()

#Login de la prueba tecnica por Nelson Javier Amaya Guerrero
#Metodos CRUD para el usuario
@app.route("/", methods=['GET'])
def testSeguridad():
    json ={}
    json["message"] = "Sevicio de seguridad corriendo......."
    return jsonify(json)

@app.route("/usuario", methods=['POST'])
def crearUsuario():
    data=request.get_json()
    json=controladorUsuario.crearUsuario(data)
    return jsonify(json)

@app.route("/usuario", methods=['GET'])
def buscandoTodosUsers():
    result=controladorUsuario.buscarTodosLosUsuarios()
    if not result:
        return {"resultado": "No se encuentran usuarios"}
    else:
        return jsonify(result)

@app.route("/usuario/<string:id>",methods=['GET'])
def buscarUnUser(id):
    result=controladorUsuario.buscarUnUsuario(id)
    if result is None:
        return {"resultado": "No se encuentran usuario"}
    else:
        return jsonify(result)

@app.route("/usuario/<string:id>", methods=['PUT'])
def actualizandoUser(id):
    data=request.get_json()
    json=controladorUsuario.actualizarUsuario(id,data)
    return jsonify(json)

@app.route("/usuario/<string:id>", methods=['DELETE'])
def eliminandoUser(id):
    result=controladorUsuario.borrarUsuario(id)
    if result is None:
        return {"resultado":"No se elimino usuario"}
    else:
        return jsonify(result)

@app.route("/usuario/<string:idUsuario>/rol/<string:idRol>", methods=['PUT'])
def asignarRolAUsuario(idUsuario,idRol):
    result = controladorUsuario.asignarRol(idUsuario,idRol)
    return jsonify(result)

#Metodos CRUD para el usuario

@app.route("/rol", methods=['POST'])
def creandoRol():
    data=request.get_json()
    json = controladorRol.crearRol(data)
    return jsonify(json)

@app.route("/rol", methods=['GET'])
def buscarRoles():
    result=controladorRol.buscarTodosLosRoles()
    if not result:
        return {"resultado":"No se encuentran roles"}
    else:
        return jsonify(result)

@app.route("/rol/<string:id>", methods=['GET'])
def buscandoUnRol(id):
    result=controladorRol.buscarUnRol(id)
    if result is None:
        return {"resultado":"No se encuentran roles"}
    else:
        return jsonify(result)

@app.route("/rol/<string:id>",methods=['PUT'])
def actualizandoRol(id):
    data=request.get_json()
    json=controladorRol.actualizarRol(id,data)
    return jsonify(json)

@app.route("/rol", methods=['DELETE'])
def eliminandoRoles(id):
    result=controladorRol.borrarRol(id)
    if result is None:
        return {"resultado":"No se elimino"}
    else:
        return jsonify(result)

#Metodos CRUD para el permiso

@app.route("/permiso", methods=['POST'])
def creandoPermisos():
    data=request.get_json()
    json=controladorPermiso.crearPermiso(data)
    return jsonify(json)

@app.route("/permiso", methods=['GET'])
def buscandoTodosPermisos():
    result = controladorPermiso.buscarTodosLosPermisos()
    if not result:
        return {"resultado":"No se encuentran permisos"}
    else:
        return jsonify(result)

@app.route("/permiso/<string:id>", methods=['DELETE'])
def eliminandoPermiso(id):
    result = controladorPermiso.eliminarPermiso(id)
    if result is None:
        return {"resultado":"No es elimino permiso"}
    else:
        return jsonify(result)

@app.route("/permisos-rol/idRol/<string:idRol>/permiso/<string:idPermiso>",methods=['POST'])
def crearResultado(idRol,idPermiso):
    requestBody = request.get_json()
    print("Request body: ",requestBody)
    result=controladorPermisorol.crearPermisosRol(requestBody,idRol,idPermiso)
    return jsonify(result)



def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"]))
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"])