from flask import Flask, render_template, request, redirect, url_for
from POO import *
from pymongo import MongoClient

app = Flask(__name__)

cliente = MongoClient("mongodb+srv://josephtc1415_db_user:UCXGS3MH9uxraxZB@flask.nzttsy6.mongodb.net/")
base_datos = cliente["indexzero"]
coleccion = base_datos["lenguajes"]


plataforma = PlataformaAprendizaje()



@app.route('/')

def index():
    lista_lenguajes = leer_todos_los_lenguajes()
    return render_template('index.html', lenguajes=lista_lenguajes)

@app.route('/Crear_lenguaje', methods = ['GET', 'POST'])
def registrar_lenguajes():
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

        #plataforma.registar_lenguaje(nuevo_lenguaje)

        return redirect(url_for('registrar_lenguajes'))
    elif request.method == 'GET':
        lista_lenguajes = leer_todos_los_lenguajes()
        return render_template('registrar_lenguajes.html',lenguajes=lista_lenguajes)

    return render_template('registrar_lenguajes.html')



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



@app.route('/Crear_clase/<nombre>', methods = ['GET', 'POST'])
def crear_clases(nombre):

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
            {"$push":{"tutoriales": nuevo_tutorial_dict}}
        )
        return redirect(url_for('crear_clases', nombre=nombre))
    return render_template('agregar_lecciones.html', lenguaje=lenguaje_actual)

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

    return render_template('ver_clases.html', lenguaje=lenguaje_actual)


if __name__ == "__main__":
    app.run()



