from servicios_libreria import *

#------------------------------------------------------------------------------
#
# Controladores de las funcionalidades del modulo de Servicios
#
#------------------------------------------------------------------------------

# Pagina principal del modulo
@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
	return dict()

@auth.requires_login(otherwise=URL('modulos', 'login'))
def usuario():
    return dict(form=auth.profile(), form2=auth.change_password())

@auth.requires_login(otherwise=URL('modulos', 'login'))
def listado():

	servicio = Servicio(db, 'nombre', 1, 1, 'objetivo', 'alcance', 'metodo',
			   'rango', 'incertidumbre', 'item_ensayar', 'requisitos', 'resultados',
			   True, False, True, False, True, 
			   1, 1, 1)

	s = Servicio(db)

	print(servicio.insertar())

	return dict()