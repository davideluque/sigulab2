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

	user = db(db.auth_user.email == request.post_vars.email).select(db.auth_user.ALL)
	
	try:
		user = user[0]

		auth.messages.reset_password = '<html>\
  <head>\
    <title>Restablecer tu contraseña de SIGULAB</title>\
  </head>\
  <body style="width: 100%% ;height: 100%%;margin: 0;line-height: 1.4;background-color: #F2F4F6;color: #74787E; -webkit-text-size-adjust: none; font-family: Arial, Helvetica, sans-serif; box-sizing: border-box;">\
    <span style="display: none">Recibimos una solicitud para restablecer tu contraseña para acceder a SIGULAB con el correo '+user.email+'</span>\
        <table style="width: 100%%;margin: 0;padding: 0;-premailer-width: 100%%;-premailer-cellpadding: 0;-premailer-cellspacing: 0;background-color: #F2F4F6;" width="100%%" cellpadding="0" cellspacing="0">\
      <tr>\
        <td align="center">\
          <table style="width: 100%%;margin: 0;padding: 0;-premailer-width: 100%%;-premailer-cellpadding: 0;-premailer-cellspacing: 0;" width="100%%" cellpadding="0" cellspacing="0">\
            <tr>\
              <td style="padding: 25px 0; text-align: center;">\
                <a href="" style="font-size: 16px;font-weight: bold;color: #bbbfc3;text-decoration: none;text-shadow: 0 1px 0 white;">\
        SIGULAB\
      </a>\
              </td>\
            </tr>\
            <tr>\
              <td style="width: 100%%;margin: 0;padding: 0;-premailer-width: 100%%;-premailer-cellpadding: 0;-premailer-cellspacing: 0;border-top: 1px solid #EDEFF2;border-bottom: 1px solid #EDEFF2;background-color: #FFFFFF;" width="100%%" cellpadding="0" cellspacing="0">\
                <table style="width: 570px;margin: 0 auto;padding: 0;-premailer-width: 570px;-premailer-cellpadding: 0;-premailer-cellspacing: 0;background-color: #FFFFFF;" align="center" width="570" cellpadding="0" cellspacing="0">\
                  <tr>\
                    <td style="padding: 35px;">\
                      <p style="margin-top: 0; color: #74787E;font-size: 16px;line-height: 1.5em;">Hola '+ user.first_name + ' ' + user.last_name +'. Recientemente recibimos una petición de reiniciar la contraseña para acceder a SIGULAB con tu correo electrónico.</p>\
                      <p style="margin-top: 0; color: #74787E;font-size: 16px;line-height: 1.5em;">Para cambiar tu contraseña por favor haz clic en el siguiente botón:</p>\
                      <table style="width: 100%%;margin: 30px auto;padding: 0;-premailer-width: 100%%;-premailer-cellpadding: 0;-premailer-cellspacing: 0;text-align: center;" align="center" width="100%%" cellpadding="0" cellspacing="0">\
                        <tr>\
                          <td align="center">\
                            <table width="100%%" border="0" cellspacing="0" cellpadding="0">\
                              <tr>\
                                <td align="center">\
                                  <table border="0" cellspacing="0" cellpadding="0">\
                                    <tr>\
                                      <td>\
                                        <a href="'+site_url+'/?key='+'%(key)s" style="background-color: #3869D4; border-top: 10px solid #3869D4; border-right: 18px solid #3869D4; border-bottom: 10px solid #3869D4; border-left: 18px solid #3869D4; display: inline-block; color: #FFF; text-decoration: none; border-radius: 3px; box-shadow: 0 2px 3px rgba(0, 0, 0, 0.16);-webkit-text-size-adjust: none;" target="_blank">Cambiar mi contraseña</a>\
                                      </td>\
                                    </tr>\
                                  </table>\
                                </td>\
                              </tr>\
                            </table>\
                          </td>\
                        </tr>\
                      </table>\
                      <p style="margin-top: 0; color: #74787E;font-size: 16px;line-height: 1.5em;">Si no utilizas SIGULAB o no solicitaste restablecer tu contraseña, por favor ignora este correo.</p>\
                      <p style="margin-top: 0; color: #74787E;font-size: 16px;line-height: 1.5em;">Saludos Cordiales,\
                        <br>El equipo SIGULAB</p>\
                      <table style="margin-top: 25px;padding-top: 25px;border-top: 1px solid #EDEFF2;">\
                        <tr>\
                          <td>\
                            <p style="font-size: 12px;">Si estás teniendo dificultades con el botón de arriba, copia y pega el enlace de abajo en tu navegador.</p>\
                            <p style="font-size: 12px;">'+site_url+'/?key='+'%(key)s</p>\
                          </td>\
                        </tr>\
                      </table>\
                    </td>\
                  </tr>\
                </table>\
              </td>\
            </tr>\
            <tr>\
              <td>\
                <table class="email-footer" align="center" width="570" cellpadding="0" cellspacing="0">\
                  <tr>\
                    <td class="content-cell" align="center">\
                      <p style="font-size: 12px;text-align: center;">&copy; 2017 SIGULAB.</p>\
                      <p style="font-size: 12px;text-align: center;">\
                        Unidad de Laboratorios\
                        <br>Universidad Simón Bolívar\
                        <br>Sede Sartenejas, Baruta, Edo. Miranda - Apartado 89000 - Cable Unibolivar - Caracas Venezuela. Teléfono +58 0212-9063111\
                        <br>Sede Litoral, Camurí Grande, Edo. Vargas Parroquia Naiguatá. Teléfono +58 0212-9069000\
                      </p>\
                    </td>\
                  </tr>\
                </table>\
              </td>\
            </tr>\
          </table>\
        </td>\
      </tr>\
    </table>\
  </body>\
 	</html>'
	except:
		pass

	form = auth.request_reset_password()
	return dict(form=form)

def logout():
	auth.logout()
	return redirect(URL('login'))