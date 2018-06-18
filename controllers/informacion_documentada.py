#
# Andre Corcuera
# Angel Morante
# Jawil Ricauter
# Jonathan Bandes
# Nairelys Hernandez
# Natascha Gamboa
# Rosana Garcia


# Verifica si el usuario posee alguno de los roles permitidos
# def __check_role():

# 	roles_permitidos = ['WEBMASTER', 'DIRECTOR', 'ASISTENTE DEL DIRECTOR',
#                         'COORDINADOR', 'JEFE DE LABORATORIO', 'JEFE DE SECCIÓN',
#                         'TÉCNICO', 'PERSONAL DE COORDINACIÓN', 'GESTOR DE SMyDP',
#                         'CLIENTE INTERNO']
#     return True in map(lambda x: auth.has_membership(x), roles_permitidos)

#
def __get_documentos(dep_id):
	documentos = []

	#

	return documentos

#
def __acceso_permitido(user, dep_id):
	pass

#          <-- Pagina de Inicio del modulo de Gestion de Informacion Documentada -->
def index(): return dict(message="hello from informacion_documentada.py")

# @auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def lista_documentos():

	# Lista de documentos a mostrar según privilegios del rol del usuario
	documentos = []

	# Datos del usuario conectado
    # user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    # user_id = user.id
    # user_dep_id = user.f_dependencia

	#
	# if auth.has_membership("WEBMASTER") or auth.has_membership("DIRECTOR") or
	# 	auth.has_membership("COORDINADOR") or auth.has_membership("ASISTENTE DEL DIRECTOR"):

	# 	# Pueden ver todos los documentos
	# 	documentos=db().select(db.documentos.ALL)

	# elif auth.has_membership("JEFE DE LABORATORIO"):

	# 	# Sólo puede ver los documentos de su laboratorio en específico.
	# 	# Ejemplo: Si es jefe del laboratorio A, sólo se listan documentos del
	# 	# laboratorio A

	# elif auth.has_membership("JEFE DE SECCIÓN"): pass
	# elif auth.has_membership("TÉCNICO"): pass
	# elif auth.has_membership("PERSONAL DE COORDINACIÓN"): pass
	# elif auth.has_membership("GESTOR DE SMyDP"): pass
	# elif auth.has_membership("CLIENTE INTERNO"): pass
	# else: pass

	print(auth.user.first_name)
	if auth.has_membership("WEBMASTER") or auth.has_membership("DIRECTOR") or auth.user.email=='ulab-calidad@usb.ve':
		documentos = db().select(db.documentos.ALL)
	else:
		print (auth.user.first_name=='Unidad de Administración')
		documentos = db(db.documentos.responsable==auth.user.first_name).select()
	dic = {
	"codigo": request.post_vars.codigo,
	"objetivo": request.post_vars.objetivos,
	"ubicacion_electronica": request.post_vars.ubicacion_electronica,
	"ubicacion_fisica": request.post_vars.ubicacion_fisica,
	# "cod_anexo": request.post_vars.cod_anexo,
	# "nombre_anexo": request.post_vars.nombre_anexo,
	"responsable": request.post_vars.responsable,
	"nombre_doc": request.post_vars.nombre_documento,
	"estatus":"Planificado",
	"periodo_rev":request.post_vars.periodo,
	"aprobado_por": request.post_vars.aprobado,
	"elaborado_actualizado_por": request.post_vars.elaborado,
	# "vigencia":
	"fecha_aprob": request.post_vars.fechaAprobacion,
	"fecha_prox_rev": request.post_vars.fecha_prox_rev,
	"fecha_control_cambio": request.post_vars.fecha_control_cambio,
	"cod_control_cambio": request.post_vars.cod_control_cambio,
	"cod_aprob": request.post_vars.cod_registro,
	"fecha_rev_por_consejo_asesor": request.post_vars.fecha_revision_consejo,
	"rev_por_consejo_asesor": request.post_vars.revision_consejo,
	"fecha_rev_especificaciones_doc":  request.post_vars.fecha_revision_especificaciones,
	"fecha_rev_contenido": request.post_vars.fecha_revision_contenidos,
	"rev_especficaciones_doc_realizado_por": request.post_vars.revision_especificaciones,
	"rev_contenido_realizado_por": request.post_vars.revision_contenido,
	"tipo_doc":request.post_vars.tipo,
	}

	planificado = {
				"tipo_doc": dic["tipo_doc"]=='',
				"responsable":dic["responsable"],
				"fecha_prox_rev":dic["fecha_prox_rev"]
				}
	elaborado = { "codigo":dic["codigo"],
				"objetivo":dic["objetivo"],
				"elaborado_actualizado_por":dic["elaborado_actualizado_por"],
				"periodo_rev":dic["periodo_rev"]
				}
	revisado = {"rev_contenido_realizado_por":dic["rev_contenido_realizado_por"],
				"fecha_rev_contenido":dic["fecha_rev_contenido"],
				"rev_especficaciones_doc_realizado_por":dic["rev_especficaciones_doc_realizado_por"],
				"fecha_rev_especificaciones_doc":dic["fecha_rev_especificaciones_doc"],
				"fecha_rev_por_consejo_asesor":dic["fecha_rev_por_consejo_asesor"],
				"rev_por_consejo_asesor":dic["rev_por_consejo_asesor"],
	}

	aprobado = {
		"aprobado_por":dic["aprobado_por"],
		"fecha_aprob":dic["fecha_aprob"],
		"cod_aprob":dic["cod_aprob"],
	}


	if(not('' in elaborado.values())):

		dic["estatus"] = "Elaborado"
	if(not('' in revisado.values())):

		dic["estatus"] = "Revisado"
	if(not('' in aprobado.values())):

		dic["estatus"] = "Aprobado"
	print(dic["codigo"]!=None)
	if(dic["codigo"]!=None):
		db.documentos.insert(
			codigo=dic["codigo"],
			objetivo=dic["objetivo"],
			ubicacion_electronica=dic["ubicacion_electronica"],
			ubicacion_fisica=dic["ubicacion_fisica"],
			# cod_anexo=dic["cod_anexo"],
			# nombre_anexo=dic["nombre_anexo"],
			responsable=dic["responsable"],
			nombre_doc=dic["nombre_doc"],
			estatus=dic["estatus"],
			periodo_rev=dic["periodo_rev"],
			aprobado_por=dic["aprobado_por"],
			elaborado_actualizado_por=dic["elaborado_actualizado_por"],
			# vigencia=,
			fecha_aprob=dic["fecha_aprob"],
			fecha_prox_rev=dic["fecha_prox_rev"],
			fecha_control_cambio=dic["fecha_control_cambio"],
			cod_control_cambio=dic["cod_control_cambio"],
			cod_aprob=dic["cod_aprob"],
			fecha_rev_por_consejo_asesor=dic["fecha_rev_por_consejo_asesor"],
			rev_por_consejo_asesor=dic["rev_por_consejo_asesor"],
			fecha_rev_especificaciones_doc=dic["fecha_rev_especificaciones_doc"],
			fecha_rev_contenido=dic["fecha_rev_contenido"],
			rev_especficaciones_doc_realizado_por=dic["rev_especficaciones_doc_realizado_por"],
			rev_contenido_realizado_por=dic["rev_contenido_realizado_por"],
			tipo_doc= dic["tipo_doc"],
		)


	return dict(
	            documentos=db().select(db.documentos.ALL),
				doc_aprobado=db(db.documentos.estatus=="Aprobado").count(),
				doc_revision=db(db.documentos.estatus=="Revisado").count(),
				doc_elaboracion=db(db.documentos.estatus=="Elaborado").count(),
				doc_planificacion=db(db.documentos.estatus=="Planificado").count()
				)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def lista_registros(): return dict(message="hello from informacion_documentada.py")

def ficha():
	uname = request.args[0]
	row = db(db.documentos.codigo==uname).select()


	dic = {
	"codigo": request.post_vars.codigo,
	"objetivo": request.post_vars.objetivos,
	"ubicacion_electronica": request.post_vars.ubicacion_electronica,
	"ubicacion_fisica": request.post_vars.ubicacion_fisica,
	# "cod_anexo": request.post_vars.cod_anexo,
	# "nombre_anexo": request.post_vars.nombre_anexo,
	"responsable": request.post_vars.responsable,
	"nombre_doc": request.post_vars.nombre_documento,
	"estatus":"Planificado",
	"periodo_rev":request.post_vars.periodo,
	"aprobado_por": request.post_vars.aprobado,
	"elaborado_actualizado_por": request.post_vars.elaborado,
	# "vigencia":
	"fecha_aprob": request.post_vars.fechaAprobacion,
	"fecha_prox_rev": request.post_vars.fecha_prox_rev,
	"fecha_control_cambio": request.post_vars.fecha_control_cambio,
	"cod_control_cambio": request.post_vars.cod_control_cambio,
	"cod_aprob": request.post_vars.cod_registro,
	"fecha_rev_por_consejo_asesor": request.post_vars.fecha_revision_consejo,
	"rev_por_consejo_asesor": request.post_vars.revision_consejo,
	"fecha_rev_especificaciones_doc":  request.post_vars.fecha_revision_especificaciones,
	"fecha_rev_contenido": request.post_vars.fecha_revision_contenidos,
	"rev_especficaciones_doc_realizado_por": request.post_vars.revision_especificaciones,
	"rev_contenido_realizado_por": request.post_vars.revision_contenido,
	"tipo_doc":request.post_vars.tipo,
	}

	documento =  db(db.documentos.codigo==uname)
	if(request.post_vars.button=="Submit"):

		documento.update(

				objetivo=dic["objetivo"],
				ubicacion_electronica=dic["ubicacion_electronica"],
				ubicacion_fisica=dic["ubicacion_fisica"],
				# cod_anexo=dic["cod_anexo"],
				# nombre_anexo=dic["nombre_anexo"],
				#responsable=dic["responsable"],
				nombre_doc=dic["nombre_doc"],
				#estatus=dic["estatus"],
				periodo_rev=dic["periodo_rev"],
				aprobado_por=dic["aprobado_por"],
				elaborado_actualizado_por=dic["elaborado_actualizado_por"],

				fecha_aprob=dic["fecha_aprob"],
				fecha_prox_rev=dic["fecha_prox_rev"],
				fecha_control_cambio=dic["fecha_control_cambio"],
				cod_control_cambio=dic["cod_control_cambio"],
				cod_aprob=dic["cod_aprob"],
				fecha_rev_por_consejo_asesor=dic["fecha_rev_por_consejo_asesor"],
				rev_por_consejo_asesor=dic["rev_por_consejo_asesor"],
				fecha_rev_especificaciones_doc=dic["fecha_rev_especificaciones_doc"],
				fecha_rev_contenido=dic["fecha_rev_contenido"],
				rev_especficaciones_doc_realizado_por=dic["rev_especficaciones_doc_realizado_por"],
				rev_contenido_realizado_por=dic["rev_contenido_realizado_por"],
				tipo_doc= dic["tipo_doc"],
			)
	if(request.post_vars.eliminar=="eliminar"):
		db(db.documentos.codigo==uname).delete()
		redirect(URL('..', 'sigulab2','informacion_documentada',''))

	### END ###
	return dict(message=row	)
