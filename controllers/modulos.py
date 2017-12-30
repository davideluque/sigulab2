#!/usr/bin/ python
# encoding=utf8  

# Caracteres especiales dentro de campos secretos (agregados por web2py)
# no son aceptados por ciertos navegadores/terminales
#import sys  
  
#sys.setdefaultencoding('utf8')

import re

#-------------------------------------
#
# Controladores integrados/en conjunto
#
#-------------------------------------

# Pagina, botones de eleccion entre nuestros modulos
# o SMDP

@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
	return dict()

@auth.requires_login(otherwise=URL('modulos', 'login'))
def sigulab2():
	return dict()

#-------------------------------------
# Autenticacion y manejo de cuenta
# ToDo login
# ToDo Mostrar errores mejor
# ToDo Boton para volver a la pantalla de eleccion de modulos
#
# ToDo register
# ToDo Validar, mientras se escribe, los campos (?)
# ToDo Mostrar errores
# ToDo Nombre y Apellido solo letras guiones espacios y caracteres especiales
# ToDo Cambiar tamaño de los dropdowns
# ToDo Boton para volver al login
# ToDo Asegurar que se vea que cada campo es obligatorio (?)
# ToDo correo de verificacion (?) + correo de aprobacion
#
# ToDo resetpassword
# ToDo Boton para volver al Login
# ToDo Mostrar errores mejor
#
# ToDo recoverpassword
# ToDo Vistas enteras
# ToDo Boton para ir al login
# 
#-------------------------------------

def authenticate():

	if not 'token_send' in request.post_vars:
		return "Esta conexión no es segura. Prueba entrando a la página de nuevo. \
		Si continuas viendo este mensaje, contacta al administrador del sitio."

	if not '@' in request.post_vars.email_send:
		return "Correo inválido. Formato: algo@ejemplo.com"

	user = auth.login_bare(request.post_vars.email_send, request.post_vars.pass_send)
	
	if not user:
		return "Datos de inicio de sesión incorrectos."
	else:
		url = URL('index')
		return '<meta http-equiv="refresh" content="0; url='+ url + '">'

# Inicio de Sesion
def login():
	if auth.user:
		return redirect(URL('index'))

	form=auth.login()
	
	if request.vars['error'] == 'invalid_data':
		return dict(form=form, error="Datos de inicio de sesión incorrectos")
	
	return dict(form=form, error=None)

# Perfil de Usuario
@auth.requires_login(otherwise=URL('modulos', 'login'))
def editprofile():
	return dict(form=auth.profile(), form2=auth.change_password())

# Registro de usuarios- Incluye la creacion del rol
def register():
	if auth.user:
		return redirect(URL('index'))
	form=auth.register()
	roles=list(db(db.auth_group.role != 'WebMaster').select(db.auth_group.ALL))
	return dict(form=form, roles=roles)

def redireccionando():
	user = db(db.auth_user.id > 0).select(db.auth_user.ALL)[-1]
	
	print(session.ci)

	db.auth_membership.insert(user_id=user, group_id=session.rolid, dependencia_asociada=session.depid, f_personal_membership = session.ci)
 	
 	db.t_Personal.insert(f_nombre = user.first_name,
                                f_apellido = user.last_name,
                                f_ci = session.ci,
                                f_email = user.email,
                                f_telefono = 0,
                                f_pagina_web = "N/A",
                                f_categoria = "Administrativo",
                                f_cargo = "N/A",
                                f_fecha_ingreso = "1/01/1989",
                                f_fecha_salida = "1/02/1989",
                                f_dependencia = session.depid
                                )
	session.forget()
	return redirect(URL('index'))

# Ajax Helper para la dependencia de acuerdo a su unidad de adscripcion
def ajax_unidad_rol():
	rolid = request.post_vars.dependenciahidden
	roltype = db(db.auth_group.id == int(rolid)).select(db.auth_group.ALL)[0].role
	direccion=db(db.dependencias.nombre == "Dirección").select(db.dependencias.ALL)
	labs_y_coordinaciones=list(db(db.dependencias.unidad_de_adscripcion == direccion[0].id).select(db.dependencias.ALL))
	labs = []
	coordinaciones = []
	for i in labs_y_coordinaciones:
		if "Laboratorio" in i.nombre:
			labs.append(i)
		else:
			coordinaciones.append(i)
	if roltype == "Director" or roltype == "Asistente del Director" or roltype == "Gestor de SMyDP":
		lista = direccion
	elif roltype == "Coordinador" or roltype == "Personal de Coordinación":
		lista = coordinaciones
	elif roltype == "WebMaster" or roltype == "Cliente Interno":
		lista = False
	else:
		lista = labs
	return(dict(lista=lista))

# Ajax helper para crear una membership para el usuario recien registrado
def ajax_membership():
	session.depid = None
	session.rolid = int(request.post_vars.rol)
	session.ci = int(request.post_vars.cedula)
	print(request.post_vars.cedula)
	if request.post_vars.laboratorio:
		session.depid = int(request.post_vars.laboratorio)
	if request.post_vars.seccion:
		session.depid = int(request.post_vars.seccion)
	return dict()

# Ajax Helper para mostrar dependencias a Tecnicos y Jefes de seccion
def ajax_registro_seccion(): 
	rolid = request.post_vars.dependenciahidden
	roltype = db(db.auth_group.id == int(rolid)).select(db.auth_group.ALL)[0].role
	secciones=False
	if roltype == "Técnico" or roltype == "Jefe de Sección":
		labid = request.post_vars.seccionhidden
		secciones=list(db(db.dependencias.unidad_de_adscripcion == int(labid)).select(db.dependencias.ALL))

	return dict(lista=secciones)

# Recuperacion de Contraseña (pedido) 
def resetpassword():
	site_url = URL('default', 'recoverpassword', host=True)


	# ToDo No escriban caracteres especiales! (clave en vez de contraseña) se muere por alguna razon...
	auth.messages.reset_password = 'Hola! Por favor, ingresa en el siguiente enlace ' + site_url+ '/?key='+'%(key)s para ' + \
								   'recuperar tu clave de acceso.'
	form = auth.request_reset_password()
	return dict(form=form)

def logout():
	auth.logout()
	return redirect(URL('login'))