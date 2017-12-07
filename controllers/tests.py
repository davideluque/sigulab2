from servicios_libreria import *

# ----------------------------------------------------------------------------------------
# Controlador que no sera implementado en la aplicacion final, pueden hacerse pruebas aca
# ----------------------------------------------------------------------------------------

def buscador():
	grupo_lab = db(db.auth_group.role == "Jefe de Laboratorio").select(db.auth_group.id)[0].id
	grupo_dir = db(db.auth_group.role == "Director").select(db.auth_group.id)[0].id
	grupo_asistdir = db(db.auth_group.role == "Asistente del Director").select(db.auth_group.id)[0].id
	grupo_admin = db(db.auth_group.role == "WebMaster").select(db.auth_group.id)[0].id

	info_membership = db(db.auth_membership.user_id == auth.user_id).select()[0]
	user_group_id = info_membership.group_id

	dependencia = info_membership.dependencia_asociada

	rol = 0
	if user_group_id == grupo_dir or user_group_id == grupo_asistdir or user_group_id == grupo_admin:
		rol = 2
	elif user_group_id == grupo_lab:
		rol = 1

	listado_de_servicios = ListaServicios(db, dependencia, rol)

	listado_de_servicios.filtrar_por_tags("laboratorio b", ["nombre", "laboratorio"])

	return dict(grid = listado_de_servicios.filas)