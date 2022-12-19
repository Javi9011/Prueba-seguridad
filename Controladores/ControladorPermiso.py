from Modelos.Permiso import Permiso
from Repositorios.RepositorioPermiso import RepositorioPermiso

class ControladorPermiso():

    def __init__(self):
        print("creando controlador permiso..")
        self.repositorioPermiso=RepositorioPermiso()

    def crearPermiso(self, bodyRequest):
        print("Creando permisos...")
        elPermiso = Permiso(bodyRequest)
        print("Permiso a crear en la base de datos: ",elPermiso.__dict__)
        self.repositorioPermiso.save(elPermiso)
        return True

    def buscarTodosLosPermisos(self):
        return self.repositorioPermiso.findAll()


    def eliminarPermiso(self,id):
        return self.repositorioPermiso.delete(id)
