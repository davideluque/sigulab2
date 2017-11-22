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
	listado_de_servicios = ListaServicios(db)
	
	if request.vars.pagina:
		listado_de_servicios.cambiar_pagina(int(request.vars.pagina))

	if request.vars.orden:
		listado_de_servicios.invertir_ordenamiento()

	if request.vars.columna:
		listado_de_servicios.cambiar_columna(request.vars.columna)

	listado_de_servicios.orden_y_filtrado()

	return dict(grid=listado_de_servicios.servicios_a_mostrar,
							pages=listado_de_servicios.rango_paginas,
							actualpage=listado_de_servicios.pagina_central)
