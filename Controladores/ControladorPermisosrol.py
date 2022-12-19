from Repositorios.RepositorioPermisosrol import RepositorioPermisosrol
from Repositorios.RepositorioRol import RepositorioRol
from Repositorios.RepositorioPermiso import RepositorioPermiso
from Modelos.PermisosRol import Permisosrol
from Modelos.Rol import Rol
from Modelos.Permiso import Permiso

class ControladorPermisosrol():

    def __init__(self):
        print("Creando controlador permisos Rol")
        self.repositorioPermisosrol=RepositorioPermisosrol()
        self.repositorioRol=RepositorioRol()
        self.repositorioPermiso=RepositorioPermiso()

    def index(self):
        return self.repositorioPermisosrol.findAll()

    def crearPermisosRol(self,bodyRequest, idRol, idPermiso):
        nuevoPermisorol = Permisosrol(bodyRequest)
        elRol = Rol(self.repositorioRol.findById(idRol))
        elPermiso = Permiso(self.repositorioPermiso.findById(idPermiso))
        nuevoPermisorol.rol = elRol
        nuevoPermisorol.permiso = elPermiso
        print("Permiso-rol a crear en la base de datos: ",nuevoPermisorol.__dict__)
        return self.repositorioPermisosrol.save(nuevoPermisorol)