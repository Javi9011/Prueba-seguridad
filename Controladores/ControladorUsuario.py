from Repositorios.RepositorioUsuario import RepositorioUsuario
from Repositorios.RepositorioRol import RepositorioRol
from Modelos.Usuario import Usuario
from Modelos.Rol import Rol

class ControladorUsuario():
    def __init__(self):
        print("Creando controlador usuario..")
        self.repositorioUsuario=RepositorioUsuario()
        self.repositorioRol=RepositorioRol()

    def crearUsuario(self, bodyRequest):
        print("Creando usuario..")
        elUsuario = Usuario(bodyRequest)
        print("Usuario creado en Base de Datos con ID:",elUsuario.__dict__)
        self.repositorioUsuario.save(elUsuario)
        return True

    def buscarTodosLosUsuarios(self):
        print("Buscando todos los usuarios....")
        return self.repositorioUsuario.findAll()

    def buscarUnUsuario(self,idObject):
        print("Buscando usuario con id: ",idObject)
        usuario=Usuario(self.repositorioUsuario.findById(idObject))
        return usuario.__dict__

    def actualizarUsuario(self,id,elUsuario):
        usuarioActual=Usuario(self.repositorioUsuario.findById(id))
        usuarioActual.seudonimo = elUsuario["seudonimo"]
        usuarioActual.mail = elUsuario["mail"]
        usuarioActual.password = elUsuario["password"]
        return self.repositorioUsuario.save(usuarioActual)

    def borrarUsuario(self,id):
        return self.repositorioUsuario.delete(id)

    def asignarRol(self,idUsuario,idRol):
        usuarioActual = Usuario(self.repositorioUsuario.findById(idUsuario))
        rolActual = Rol(self.repositorioRol.findById(idRol))
        print("Usuario encontrado: ",usuarioActual.__dict__)
        print("Rol encontrado: ",rolActual.__dict__)
        usuarioActual.rol = rolActual
        print("usuario actualizado:",usuarioActual.__dict__)
        return self.repositorioUsuario.save(usuarioActual)
