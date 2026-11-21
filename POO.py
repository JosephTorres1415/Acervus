class PlataformaAprendizaje():
    def __init__(self):
        self.lenguajes = []
        self.usuarios = []

    def registar_lenguaje(self, lenguaje):
        self.lenguajes.append(lenguaje)

    def registrar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def listar_lenguajes(self):
        for lenguaje in self.lenguajes:
            print(lenguaje)

    def listar_usuarios(self):
        for usuario in self.usuarios:
            print(usuario)


class Lenguaje():
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
        self.tutoriales = []

    def __str__(self):
        return f"lenguaje {self.nombre} - cantidad de clases -> {len(self.tutoriales)} "

    def agregar_tutorial(self, tutorial):
        self.tutoriales.append(tutorial)

    def eliminar_tutorial(self, tutorial):
        self.tutoriales.remove(tutorial)

    def listar_tutoriales(self):
        for tutorial in self.tutoriales:
            print(tutorial)




class Tutorial():
    def __init__(self, titulo):
        self.titulo = titulo
        self.lecciones = []

    def __str__(self):
        return f"{self.titulo} contiene una cantidad de {len(self.lecciones)} lecciones"

    def agregar_leccion(self, leccion):
        self.lecciones.append(leccion)

    def listar_lecciones(self):
        for leccion in self.lecciones:
            print(leccion)


class Leccion():
    def __init__(self, contenido, codigo_ejemplo):
        self.contenido = contenido
        self.codigo_ejemplo = codigo_ejemplo

    def mostrar_leccion(self):
        f""" 
             {self.contenido}
             {self.codigo_ejemplo}  """


class Usuario():
    def __init__(self, nombre, email, password):
        self.nombre = nombre
        self.email = email
        self.password = password

    def __str__(self):
        return f"name: {self.nombre} - email: {self.email} - password:{self.password}"








