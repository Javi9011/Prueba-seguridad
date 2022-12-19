from Modelos.Rol import Rol
from Repositorios.RepositorioRol import RepositorioRol

class ControladorRol():

    def __init__(self):
        print("Creando controladro del rol")
        self.repositorioRol=RepositorioRol()

    def crearRol(self,bodyRequest):
        print("Creando rol...")
        elRol=Rol(bodyRequest)
        print("Rol a crear: ",elRol.__dict__)
        self.repositorioRol.save(elRol)
        return True

    def buscarTodosLosRoles(self):
        print("Buscando todos los roles..")
        return self.repositorioRol.findAll()

    def buscarUnRol(self,idObject):
        print("Buscando Rol: ",idObject)
        rol=Rol(self.repositorioRol.findById(idObject))
        return rol.__dict__

    def actualizarRol(self,id,elRol):
        rolActual=Rol(self.repositorioRol.findById(id))
        rolActual.nombre=elRol["nombre"]
        rolActual.descripcion=elRol["descripcion"]
        return self.repositorioRol.save(rolActual)

    def borrarRol(self,id):
        return self.repositorioRol.delete(id)
