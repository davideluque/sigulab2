###################################################################################
##																				 ##
##		Controladores del módulo de información documentada 					 ##
##																				 ##
## 			» Andre Corcuera													 ##
## 			» Angel Morante														 ##
##			» Jawil Ricauter													 ##
## 			» Jonathan Bandes													 ##
## 			» Nairelys Hernandez												 ##
## 			» Rosana Garcia														 ##
##																				 ##
###################################################################################

import time
import datetime

## Pagina de Inicio del modulo de Gestion de Informacion Documentada
def index(): 
	return dict(message="hello from informacion_documentada.py")


# Función que te devuelve los dos últimos dígitos del año en curso.
def anioEnCurso():

	strings = time.strftime("%Y,%m,%d,%H,%M,%S")
	t = strings.split(',')
	year = t[0]
	year = year[2:]

	return year


# Función que regresa la dependencia al que está ligado el personal loggeado
def dependenciaAsociadaUsuario():

	# idDependencia es una variable que contiene el id de la dependencia al que está ligado
	# el usuario loggeado.
	idDependencia =db(db.t_Personal.f_email == auth.user.email).select(db.t_Personal.f_dependencia)[0]
	# dependencia es toda la información de la dependencia ligada al usuario loggeado y se encuentra
	# haciendo match entre el idDependencia y el id de todas las dependencias.
	dependencia = db(db.dependencias.id == idDependencia.f_dependencia).select(db.dependencias.nombre)
	
	return dependencia

# Esta función se encarga de generar el código de registro

def generarCodigoRegistro():

	dependencia = dependenciaAsociadaUsuario()
	nroRegistros = db(db.registros.dependencia_asociada == dependencia).count() + 1

	for x in db().select(db.registros.ALL):
		print("::::::")
		print(type(x.dependencia_asociada))
		print(type(dependencia))
		print(x.dependencia_asociada == dependencia)

	if (nroRegistros < 10):
		nroRegistros = "00" + str(nroRegistros)
	elif (nroRegistros < 100):
		nroRegistros = "0" + str(nroRegistros)
	codDep = db(db.dependencias.nombre == dependencia[0].nombre).select(db.dependencias.ALL)[0]
	codigoRegistro = codDep.codigo_registro + "/" + anioEnCurso() + "-" + nroRegistros

	return codigoRegistro


def analizadorVencimiento():
	print("holi")
	# strings = time.strftime("%Y,%m,%d,%H,%M,%S")
	# t = strings.split(',')
	# fechaActual = t[0] + "-" + t[1] + "-" + t[2]
	# anioActual = t[0]
	# mesActual = t[1]

	# for doc in db().select(db.documentos.ALL):
	# 	anio = ""

	# 	if (doc.fecha_prox_rev != None):
	# 		mes = str(doc.fecha_prox_rev).split("-")[1]
	# 		anio = str(doc.fecha_prox_rev).split("-")[0]


	# 	if (doc.periodo_rev == "Semestral"):

	# 		if (fechaActual == str(doc.fecha_prox_rev)):
	# 			doc.vencimiento = "Si"
	# 	elif (doc.periodo_rev == "Anual"):
	# 		if (str(int(anio) + 1) == anioActual):
	# 			doc.vencimiento = "Si"
	# 	elif (doc.periodo_rev == "Bienal"):
	# 		if (str(int(anio) + 2) == anioActual):
	# 			doc.vencimiento = "Si"
	# 	elif (doc.periodo_rev == "Trienal"):
	# 		if (str(int(anio) + 3) == anioActual):
	# 			doc.vencimiento = "Si"
	# 	elif (doc.periodo_rev == "Quinquenal"):	
	# 		if (str(int(anio) + 4) == anioActual):
	# 			doc.vencimiento = "Si"		




@auth.requires_login(otherwise=URL('modulos', 'login'))
def lista_registros():

	# Generamos el codigo de un registro nuevo.
	cod = generarCodigoRegistro()
	# Buscamos la dependencia asociada al usuario loggeado.
	dependencia = dependenciaAsociadaUsuario()

	dic = {
		"dependencia_asociada":dependencia,
		"codigo": cod,
		"fecha_creacion": request.post_vars.fecha_creacion,
		"descripcion": request.post_vars.descripcion,
		"destinatario": request.post_vars.destinatario,
		"remitente": request.post_vars.remitente,
		"doc_electronico": request.post_vars.doc_electronico,
		"ubicacion_doc_electronico": request.post_vars.ubicacion_doc_electronico,
		"archivo_fisico": request.post_vars.archivo_fisico,
	}

	# Agregams el registro.
	if(dic["descripcion"]!=None):
		db.registros.insert(
			dependencia_asociada=dic["dependencia_asociada"],
			codigo=dic["codigo"],
			fecha_creacion=dic["fecha_creacion"],
			descripcion=dic["descripcion"],
			destinatario=dic["destinatario"],
			remitente=dic["remitente"],
			doc_electronico=dic["doc_electronico"],
			ubicacion_doc_electronico=dic["ubicacion_doc_electronico"],
			archivo_fisico=dic["archivo_fisico"],
		)

	# Hacemos el filtrado (sólo se mostraran registros asociados a cada dependencia)
	registros_mostrar = db(db.registros.dependencia_asociada == dependencia).select(db.registros.ALL)

	return dict(
		registros=registros_mostrar,
		dependencias = db().select(db.dependencias.nombre, db.dependencias.codigo_registro),
	)




@auth.requires_login(otherwise=URL('modulos', 'login'))
def ficha_registro():


	cod = request.args[0] + "/" + request.args[1]
	# Encontramos el registro con el código pasado como parámetro.
	registro =  db(db.registros.codigo == cod).select(db.registros.ALL)
	rgEditable = db(db.registros.codigo == cod)

	# Sección de edición del registro.
	if (request.post_vars.fecha_creacion != None):
		rgEditable.update(
			codigo = cod,
			fecha_creacion = request.post_vars.fecha_creacion,
			descripcion = request.post_vars.descripcion,
			destinatario = request.post_vars.destinatario,
			remitente = request.post_vars.remitente,
			doc_electronico = request.post_vars.doc_electronico,
			ubicacion_doc_electronico = request.post_vars.ubicacion_doc_electronico,
			archivo_fisico = request.post_vars.archivo_fisico,
		)

		redirect(URL('informacion_documentada','ficha_registro',args=[cod]))

	# Sección de eliminación del registro.
	if(request.post_vars.eliminar=="eliminar"):
		db(db.registros.codigo==cod).delete()
		redirect(URL('lista_registros'))
	
	return dict(
		dependencias = db().select(db.dependencias.nombre, db.dependencias.codigo_registro),
		registros=registro
	)




@auth.requires_login(otherwise=URL('modulos', 'login'))
def lista_documentos():

	analizadorVencimiento()

	dic = {

		##### Planificación
		"dependencia_asociada":dependenciaAsociadaUsuario(),
		"nombre_doc": request.post_vars.nombre_documento,
		"tipo_doc":request.post_vars.tipo,
		"otro_tipo":request.post_vars.otro_tipo,
		"responsable": request.post_vars.responsable,
		"codigo": request.post_vars.codigo,
		"objetivo": request.post_vars.objetivos,
		"periodo_rev":request.post_vars.periodo,


		##### Elaboración
		"fecha_prox_rev": request.post_vars.fecha_prox_rev,
		"anexo_code1": request.post_vars.anexo_code1,
		"anexo_name1": request.post_vars.anexo_name1,
		"anexo_code2": request.post_vars.anexo_code2,
		"anexo_name2": request.post_vars.anexo_name2,
		"anexo_code3": request.post_vars.anexo_code3,
		"anexo_name3": request.post_vars.anexo_name3,
		"anexo_code4": request.post_vars.anexo_code4,
		"anexo_name4": request.post_vars.anexo_name4,
		"anexo_code5": request.post_vars.anexo_code5,
		"anexo_name5": request.post_vars.anexo_name5,
		"elaborador0": request.post_vars.elaborador0,
		"elaborador1": request.post_vars.elaborador1,
		"elaborador2": request.post_vars.elaborador2,
		"elaborador3": request.post_vars.elaborador3,
		"elaborador4": request.post_vars.elaborador4,


		##### Revisión
		"rev_contenido_realizado_por": request.post_vars.revision_contenido,
		"fecha_rev_contenido": request.post_vars.fecha_revision_contenidos,
		"rev_especficaciones_doc_realizado_por": request.post_vars.revision_especificaciones,		
		"fecha_rev_especificaciones_doc":  request.post_vars.fecha_revision_especificaciones,
		"fecha_rev_por_consejo_asesor": request.post_vars.fecha_revision_consejo,


		##### Aprobación
		"aprobado_por": request.post_vars.aprobado,
		"fecha_aprob": request.post_vars.fechaAprobacion,
		"cod_aprob": request.post_vars.cod_registro,
		"ubicacion_fisica": request.post_vars.ubicacion_fisica,
		"ubicacion_electronica": request.post_vars.ubicacion_electronica,
		"cod_control_cambio": request.post_vars.cod_control_cambio,
		"fecha_control_cambio": request.post_vars.fecha_control_cambio,
		"ccelaborado": request.post_vars.ccelaborado,
		"registro_fisico": request.post_vars.registro_fisico,
		"registro_electronico": request.post_vars.registro_electronico,
		"vinculo": request.post_vars.vinculo,

		##### Estatus inicial
		"estatus":"Planificado"
			
		
	}



	planificado = {
		"tipo_doc": dic["tipo_doc"]=='',
		"responsable":dic["responsable"],
		"nombre_doc":dic["nombre_doc"]
	}

	elaborado = { 
		"codigo": dic["codigo"],
		"objetivo": dic["objetivo"],
		"periodo_rev": dic["periodo_rev"],
		"fecha_prox_rev": dic["fecha_prox_rev"]
	}

	revisado = {
		"rev_contenido_realizado_por":dic["rev_contenido_realizado_por"],
		"fecha_rev_contenido":dic["fecha_rev_contenido"],
		"rev_especficaciones_doc_realizado_por":dic["rev_especficaciones_doc_realizado_por"],
		"fecha_rev_especificaciones_doc":dic["fecha_rev_especificaciones_doc"],
		"fecha_rev_por_consejo_asesor":dic["fecha_rev_por_consejo_asesor"]
	}

	aprobado = {
		"aprobado_por":dic["aprobado_por"],
		"fecha_aprob":dic["fecha_aprob"],
		"cod_aprob":dic["cod_aprob"]
	}


	if(not('' in elaborado.values())):
		dic["estatus"] = "Elaborado"

	if(not('' in revisado.values())):
		dic["estatus"] = "Revisado"

	if(not('' in aprobado.values())):
		dic["estatus"] = "Aprobado"

	

	##### Agregamos el documento
	if(dic["codigo"]!=None):
		db.documentos.insert(

			dependencia_asociada=dic["dependencia_asociada"],
			nombre_doc=dic["nombre_doc"],
			tipo_doc=dic["tipo_doc"],
			otro_tipo=dic["otro_tipo"],
			responsable=dic["responsable"],
			codigo=dic["codigo"],
			objetivo=dic["objetivo"],
			periodo_rev=dic["periodo_rev"],
			fecha_prox_rev=dic["fecha_prox_rev"],
			anexo_code1=dic["anexo_code1"],
			anexo_name1=dic["anexo_name1"],
			anexo_code2=dic["anexo_code2"],
			anexo_name2=dic["anexo_name2"],
			anexo_code3=dic["anexo_code3"],
			anexo_name3=dic["anexo_name3"],
			anexo_code4=dic["anexo_code4"],
			anexo_name4=dic["anexo_name4"],						
			anexo_code5=dic["anexo_code5"],
			anexo_name5=dic["anexo_name5"],
			elaborador0=dic["elaborador0"],
			elaborador1=dic["elaborador1"],
			elaborador2=dic["elaborador2"],
			elaborador3=dic["elaborador3"],
			elaborador4=dic["elaborador4"],
			rev_contenido_realizado_por=dic["rev_contenido_realizado_por"],
			fecha_rev_contenido=dic["fecha_rev_contenido"],
			rev_especficaciones_doc_realizado_por=dic["rev_especficaciones_doc_realizado_por"],
			fecha_rev_especificaciones_doc=dic["fecha_rev_especificaciones_doc"],
			fecha_rev_por_consejo_asesor=dic["fecha_rev_por_consejo_asesor"],
			aprobado_por=dic["aprobado_por"],
			fecha_aprob=dic["fecha_aprob"],
			cod_aprob=dic["cod_aprob"],
			ubicacion_fisica=dic["ubicacion_fisica"],
			ubicacion_electronica=dic["ubicacion_electronica"],
			cod_control_cambio=dic["cod_control_cambio"],
			fecha_control_cambio=dic["fecha_control_cambio"],
			ccelaborado=dic["ccelaborado"],
			registro_fisico=dic["registro_fisico"],
			registro_electronico=dic["registro_electronico"],
			vinculo=dic["vinculo"],
			estatus=dic["estatus"],
			visibilidad="Si",
			vencimiento="No"

			
		
		)

		db.registros.insert(
			dependencia_asociada=dic["dependencia_asociada"],
			codigo= generarCodigoRegistro(),
			fecha_creacion=dic["fecha_prox_rev"],
			descripcion="Carga de Documento",
			destinatario="Destinatario",
			remitente=dic["responsable"],
			doc_electronico=dic["registro_electronico"],
			ubicacion_doc_electronico=dic["ubicacion_electronica"],
			archivo_fisico=dic["ubicacion_fisica"],
		)



	dependencasOrdenadas = db().select(db.dependencias.nombre, db.dependencias.codigo_registro, orderby=db.dependencias.nombre)


	return dict(

	    documentos=db().select(db.documentos.ALL),
		doc_aprobado=db(db.documentos.estatus=="Aprobado").count(),
		doc_revision=db(db.documentos.estatus=="Revisado").count(),
		doc_elaboracion=db(db.documentos.estatus=="Elaborado").count(),
		doc_planificacion=db(db.documentos.estatus=="Planificado").count(),
		dependencias = dependencasOrdenadas,
		depAsoc=dependenciaAsociadaUsuario()[0].nombre,

	)



@auth.requires_login(otherwise=URL('modulos', 'login'))
def ficha():

	uname = request.args[0]
	row = db(db.documentos.codigo==uname).select()



	documento =  db(db.documentos.codigo==uname)


	if(request.post_vars.elaborado=="elaborado"):
		print("elaborado")
		documento.update(
			estatus="Elaborado",
			periodo_rev=request.post_vars.periodo,
			objetivo=request.post_vars.objetivos,
			fecha_prox_rev= request.post_vars.fecha_prox_rev,
			anexo_code1= request.post_vars.anexo_code2,
			anexo_name1= request.post_vars.anexo_name2,
			anexo_code2= request.post_vars.anexo_code3,
			anexo_name2= request.post_vars.anexo_name3,
			anexo_code3= request.post_vars.anexo_code4,
			anexo_name3= request.post_vars.anexo_name4,
			anexo_code4= request.post_vars.anexo_code5,
			anexo_name4= request.post_vars.anexo_name5,
			anexo_code5= request.post_vars.anexo_code6,
			anexo_name5= request.post_vars.anexo_name6,
			elaborador0= request.post_vars.elaborador1,
			elaborador1= request.post_vars.elaborador2,
			elaborador2= request.post_vars.elaborador3,
			elaborador3= request.post_vars.elaborador4,
			elaborador4= request.post_vars.elaborador5,
		)
	elif (request.post_vars.revisado=="revisado"):

		print("revisado")
		documento.update(estatus="Revisado",

			periodo_rev=request.post_vars.periodo,
			objetivo=request.post_vars.objetivos,
			fecha_prox_rev= request.post_vars.fecha_prox_rev,
			anexo_code1= request.post_vars.anexo_code2,
			anexo_name1= request.post_vars.anexo_name2,
			anexo_code2= request.post_vars.anexo_code3,
			anexo_name2= request.post_vars.anexo_name3,
			anexo_code3= request.post_vars.anexo_code4,
			anexo_name3= request.post_vars.anexo_name4,
			anexo_code4= request.post_vars.anexo_code5,
			anexo_name4= request.post_vars.anexo_name5,
			anexo_code5= request.post_vars.anexo_code6,
			anexo_name5= request.post_vars.anexo_name6,
			elaborador0= request.post_vars.elaborador1,
			elaborador1= request.post_vars.elaborador2,
			elaborador2= request.post_vars.elaborador3,
			elaborador3= request.post_vars.elaborador4,
			elaborador4= request.post_vars.elaborador5,
			rev_contenido_realizado_por = request.post_vars.revision_contenido,
        	fecha_rev_contenido = request.post_vars.fecha_revision_contenidos,
        	rev_especficaciones_doc_realizado_por = request.post_vars.revision_especificaciones,
       		fecha_rev_especificaciones_doc = request.post_vars.fecha_revision_especificaciones,
       		rev_por_consejo_asesor = request.post_vars.revision_consejo,
       		fecha_rev_por_consejo_asesor = 	request.post_vars.fecha_revision_consejo)
	elif(request.post_vars.aprobado=="aprobado"):
		print("aprobado")
		documento.update(estatus="Aprobado",
			periodo_rev=request.post_vars.periodo,
			objetivo=request.post_vars.objetivos,
			fecha_prox_rev= request.post_vars.fecha_prox_rev,
			anexo_code1= request.post_vars.anexo_code2,
			anexo_name1= request.post_vars.anexo_name2,
			anexo_code2= request.post_vars.anexo_code3,
			anexo_name2= request.post_vars.anexo_name3,
			anexo_code3= request.post_vars.anexo_code4,
			anexo_name3= request.post_vars.anexo_name4,
			anexo_code4= request.post_vars.anexo_code5,
			anexo_name4= request.post_vars.anexo_name5,
			anexo_code5= request.post_vars.anexo_code6,
			anexo_name5= request.post_vars.anexo_name6,
			elaborador0= request.post_vars.elaborador1,
			elaborador1= request.post_vars.elaborador2,
			elaborador2= request.post_vars.elaborador3,
			elaborador3= request.post_vars.elaborador4,
			elaborador4= request.post_vars.elaborador5,
			rev_contenido_realizado_por = request.post_vars.revision_contenido,
        	fecha_rev_contenido = request.post_vars.fecha_revision_contenidos,
        	rev_especficaciones_doc_realizado_por = request.post_vars.revision_especificaciones,
       		fecha_rev_especificaciones_doc = request.post_vars.fecha_revision_especificaciones,
       		rev_por_consejo_asesor = request.post_vars.revision_consejo,
       		fecha_rev_por_consejo_asesor = 	request.post_vars.fecha_revision_consejo,
       		aprobado_por = request.post_vars.aprobado_por,
        	fecha_aprob = request.post_vars.fechaAprobacion,
        	cod_aprob = request.post_vars.cod_registro,
        	cod_control_cambio = request.post_vars.cod_controlCambios,
        	fecha_control_cambio = request.post_vars.fechaControlCambios,
        	ubicacion_fisica = request.post_vars.ubicacion_fisica,
        	ubicacion_electronica = request.post_vars.ubicacion_electronica
        )

	if(request.post_vars.eliminar=="eliminar"):
		db(db.documentos.codigo==uname).delete()
		redirect(URL('lista_documentos'))

	if(request.post_vars.visibilidad != None):
		if request.post_vars.visibilidad == "Si":
			documento.update(visibilidad="Si")
			redirect(URL('informacion_documentada','ficha',args=[uname]))
		if request.post_vars.visibilidad == "No":
			documento.update(visibilidad="No")
			redirect(URL('informacion_documentada','ficha',args=[uname]))



	
	return dict(
		documentos=row,
		dependencias=db().select(db.dependencias.nombre, db.dependencias.codigo_registro),
		
	) 
