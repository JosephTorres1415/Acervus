from flask import Flask, render_template, request, redirect, url_for, session
from POO import *
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "clave_secreta_indexzero"


cliente = MongoClient("mongodb+srv://josephtc1415_db_user:UCXGS3MH9uxraxZB@flask.nzttsy6.mongodb.net/")
base_datos = cliente["indexzero"]
coleccion = base_datos["lenguajes"]

coleccion_usuarios = base_datos["usuarios"]

if coleccion_usuarios.find_one({"rol": "admin"}) is None:
    admin_unico = {
        "nombre": "Josph_Admin",
        "email": "admin@indexzero.com",
        "password": "admin123",
        "rol": "admin"
    }
    coleccion_usuarios.insert_one(admin_unico)


@app.route('/')

def index():
    lista_lenguajes = leer_todos_los_lenguajes()
    profesiones = ["Ingeniero de software","Desarrollador Front End", "Desarrollador Backend","Desarrollador Full Stack","Analista de datos","DevOps","Redes informaticas"]
    return render_template('index.html', lenguajes=lista_lenguajes[:10],profesiones=profesiones)



#----------ROL ADMIN --------------#


@app.route('/Crear_lenguaje', methods = ['GET', 'POST'])
def registrar_lenguajes():

    if session.get('rol') != 'admin':
        return redirect(url_for('index'))



    if request.method == 'POST':
        datos = request.form.to_dict()
        nuevo_lenguaje = Lenguaje(
            nombre= datos['nombre'],
            descripcion= datos['descripcion']
        )

        diccionario_mongo = {
            "nombre": nuevo_lenguaje.nombre,
            "descripcion": nuevo_lenguaje.descripcion,
            "tutoriales": []
        }

        coleccion.insert_one(diccionario_mongo)



        return redirect(url_for('registrar_lenguajes'))
    elif request.method == 'GET':
        lista_lenguajes = leer_todos_los_lenguajes()
        return render_template('registrar_lenguajes.html',lenguajes=lista_lenguajes)

    return render_template('registrar_lenguajes.html')


@app.route('/Crear_clase/<nombre>', methods=['GET', 'POST'])
def crear_clases(nombre):

    if session.get('rol') != 'admin':
        return redirect(url_for('index'))

    doc = coleccion.find_one({"nombre": nombre})

    lenguaje_actual = Lenguaje(doc["nombre"], doc["descripcion"]) if doc else None

    if request.method == 'POST':
        datos = request.form.to_dict()
        nuevo_tutorial_dict = {
            "titulo": datos['Titulo'],
            "lecciones": [
                {
                    "contenido": datos['Contenido'],
                    "codigo_ejemplo": datos['Codigo']
                }
            ]

        }

        coleccion.update_one(
            {"nombre": nombre},
            {"$push": {"tutoriales": nuevo_tutorial_dict}}
        )
        return redirect(url_for('crear_clases', nombre=nombre))
    return render_template('agregar_lecciones.html', lenguaje=lenguaje_actual)



#.................................................................................................................#


def leer_todos_los_lenguajes():
    lenguajes_objetos = []

    for doc in coleccion.find():

        obj_lenguaje = Lenguaje(doc["nombre"], doc["descripcion"])

        for tut in doc["tutoriales"]:
            obj_tutorial = Tutorial(tut["titulo"])

            for lec in tut["lecciones"]:
                obj_leccion = Leccion(lec["contenido"], lec["codigo_ejemplo"])
                obj_tutorial.agregar_leccion(obj_leccion)

            obj_lenguaje.agregar_tutorial(obj_tutorial)

        lenguajes_objetos.append(obj_lenguaje)

    return lenguajes_objetos







@app.route('/tutoriales')
def mostrar_tutoriales():

    lista_lenguajes = leer_todos_los_lenguajes()

    return render_template('tutoriales.html', lenguajes=lista_lenguajes)


@app.route('/ver_clases/<nombre>')
def ver_clases(nombre):

    lista_lenguajes = leer_todos_los_lenguajes()
    lenguaje_actual = None

    for l in lista_lenguajes:
        if l.nombre == nombre:
            lenguaje_actual = l
            break

    tutorial_seleccionado = None
    tutorial_anterior = None
    tutorial_siguiente = None

    if lenguaje_actual and lenguaje_actual.tutoriales:
        titulo_elegido = request.args.get('tema')
        indice_actual = 0

        if titulo_elegido:
            for i,t in enumerate(lenguaje_actual.tutoriales):
                if t.titulo == titulo_elegido:
                    indice_actual = i
                    break

        tutorial_seleccionado = lenguaje_actual.tutoriales[indice_actual]

        if indice_actual > 0 :
            tutorial_anterior = lenguaje_actual.tutoriales[indice_actual - 1]

        if indice_actual < len(lenguaje_actual.tutoriales) - 1:
            tutorial_siguiente = lenguaje_actual.tutoriales[indice_actual + 1]


    return render_template('ver_clases.html', lenguaje=lenguaje_actual,tutorial_actual = tutorial_seleccionado, tutorial_anterior = tutorial_anterior, tutorial_siguiente = tutorial_siguiente)


@app.route('/legajo')
def mostrar_legajo():
    return render_template('legajo.html')

@app.route('/hoja_rutas')
def mostrar_hoja_rutas():
    return render_template('hoja_rutas.html')

#------------ LOGIN -------------#



@app.route('/registro', methods=['GET', 'POST'])
def registro():
    mensaje_error = None
    if request.method == 'POST':
        datos = request.form.to_dict()

        usuario_existente = coleccion_usuarios.find_one({"nombre": datos["nombre"]})
        if usuario_existente:
            mensaje_error = "El usuario ya existe"

        else:
            nuevo_usuario = Usuario(datos["nombre"], datos["email"], datos["password"])

            usuario_dict = {
                "nombre": nuevo_usuario.nombre,
                "email": nuevo_usuario.email,
                "password": nuevo_usuario.password,
                "rol" : "estudiante"
            }

            coleccion_usuarios.insert_one(usuario_dict)

            return redirect(url_for('login'))
    return render_template('registro.html', error=mensaje_error)



@app.route('/login', methods=['GET', 'POST'])
def login():
    mensaje_error = None
    if request.method == 'POST':

        datos = request.form.to_dict()

        usuario = coleccion_usuarios.find_one({
            "email" : datos["email"],
            "password" : datos["password"]

        })

        if usuario:

            session["usuario_nombre"] = usuario["nombre"]
            session["rol"] = usuario["rol"]

            return redirect(url_for("index"))

        else:
            mensaje_error = "Gmail o contraseña incorrectas"
    return render_template('login.html', error=mensaje_error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))




if __name__ == "__main__":
    app.run()





