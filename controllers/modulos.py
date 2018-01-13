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

@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
  """
  @description Pagina principal de elección de módulos SMyDP o Otros Módulos
  """
  return dict()

@auth.requires_login(otherwise=URL('modulos', 'login'))
def sigulab2():
  return dict()

def authenticate():
  """
  @description Método de autenticación alternativo al formulario de Web2py.
  Hecho mediante ajax.

  @returns Mensajes de error o un redirect HTML si la autenticación es
  satisfactoria.
  """
  if not 'token_send' in request.post_vars:
    return "Esta conexión no es segura. Prueba entrando a la página de nuevo. \
    Si continúas viendo este mensaje, contacta al administrador del sitio."

  if not '@' in request.post_vars.email_send:
    return "Correo inválido. Formato: algo@ejemplo.com"

  user = auth.login_bare(request.post_vars.email_send, request.post_vars.pass_send)
  
  if not user:
    return "Datos de inicio de sesión incorrectos."
  else:
    url = URL('index')
    # Change to success message and redirect in JS.
    return '<meta http-equiv="refresh" content="0; url='+ url + '">'

def login():
  """
  @description Login obsoleto. Solo es utilizado para acceder a la página
  como tal y redireccionar en caso de que el usuario ya fue autenticado.

  @return Redirección a la página principal de elección de nuevos módulos
  en caso de que el usuario ya fue autenticado.
  """
  if auth.user:
    return redirect(URL('index'))

  form=auth.login()
  
  if request.vars['error'] == 'invalid_data':
    return dict(form=form, error="Datos de inicio de sesión incorrectos")
  
  return dict(form=form, error=None)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def editprofile():
  """
  @description Página en donde cada usuario autenticado puede editar su perfil
  y cambiar su contraseña.

  @returns form de edición de usuario autenticado, form de cambio de
  contraseña de usuario autenticado
  """
  return dict(form=auth.profile(), form2=auth.change_password())

def check_role():
  """Método que verifica el grupo del usuario que intenta acceder
  a la página de registro.

  @returns True en caso de que el usuario pertenezca a alguno de los grupos
  autorizados a realizar registros en este sistema. False de lo contrario.
  """

  grupo_webmaster = db(db.auth_group.role == "WebMaster").select(db.auth_group.id)[0].id
  grupo_director = db(db.auth_group.role == "Director").select(db.auth_group.id)[0].id
  grupo_asistente_director = db(db.auth_group.role == "Asistente del Director").select(
    db.auth_group.id)[0].id

  auth_user_group_id = db(db.auth_membership.user_id == auth.user_id).select()[0].group_id

  if (auth_user_group_id == grupo_webmaster) \
   or (auth_user_group_id == grupo_director) \
    or (auth_user_group_id == grupo_asistente_director):
    return True
  elif auth.user.email == 'ulab-calidad@usb.ve':
    return True

  return False

def validar_cedula():

  ci_format = re.compile("^[0-9]+$")
  if not re.match(ci_format, request.post_vars.cedula):
    return "jQuery('#auth_cedula__row').addClass('has-error');\
    jQuery('#cedula_error_group').addClass('has-error');\
    jQuery('#cedula_error').html('La cédula debe contener únicamente números. Ej: 12345678');\
    jQuery('#cedula_error_group').show();\
    jQuery('form').submit(false);"

  personal_register = db(db.t_Personal.f_ci == request.post_vars.cedula).select(db.t_Personal.ALL)
  
  if len(personal_register) != 0:
    return "jQuery('#auth_cedula__row').addClass('has-error');\
    jQuery('#cedula_error_group').addClass('has-error');\
    jQuery('#cedula_error').html('Ya existe un usuario con esta cédula.');\
    jQuery('#cedula_error_group').show();\
    jQuery('form').submit(false);"
  elif request.post_vars.cedula != "":
    return "jQuery('#auth_cedula__row').addClass('has-success');\
    jQuery('#cedula_error_group').hide();\
    jQuery('form').unbind('submit');"
  else:
    return "jQuery('#auth_cedula__row').addClass('has-error');\
    jQuery('#cedula_error_group').addClass('has-error');\
    jQuery('form').submit(false);"

def validar_email():

  email_format = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
  
  if not re.match(email_format, request.post_vars.email):
    return "jQuery('#auth_user_email__row').addClass('has-error');\
    jQuery('#email_error_group').addClass('has-error');\
    jQuery('#email_error').html('Introduce un correo válido. Ej: ejemplo@dominio.com');\
    jQuery('#email_error_group').show();\
    jQuery('form').submit(false);"

  auth_register = db(db.auth_user.email == request.post_vars.email).select(db.auth_user.ALL)

  if len(auth_register) != 0:
    return "jQuery('#auth_user_email__row').addClass('has-error');\
    jQuery('#email_error_group').addClass('has-error');\
    jQuery('#email_error').html('Ya existe un usuario con este correo electrónico.');\
    jQuery('#email_error_group').show();\
    jQuery('form').submit(false);"    
  elif request.post_vars.email != "":
    return "jQuery('#auth_user_email__row').addClass('has-success');\
    jQuery('#email_error_group').hide();\
    jQuery('form').unbind('submit');"
  else:
    return "jQuery('#auth_user_email__row').addClass('has-error');\
    jQuery('#email_error_group').addClass('has-error');\
    jQuery('form').submit(false);"

@auth.requires(lambda: check_role())
def register():
  """ El registro de usuarios está habilitado únicamente para los 
  administradores del sitio que son aquellos que pertecen a uno de los
  siguientes grupos: Grupo Webmaster, grupo Director, grupo Asistente del 
  Director o Coordinadora de la Calidad.
  """

  ### Realizar registro de usuario ###
  if request.vars and request.vars.registrar == "do_register":
    auth_register = auth.register_bare(username=request.post_vars.first_name, 
                                       last_name=request.post_vars.last_name,
                                       email=request.post_vars.email, 
                                       password=request.post_vars.password)

    if auth_register is False:
      # La verificación de usuario ya registrado se hace mediante ajax
      # en el método validar email. # Se podría hacer una segunda verificación 
      # de seguridad acá.
      print("Usuario ya registrado.")

    """Después de haber hecho la verificación de correo electrónico no tomado
    y que la verificación de contraseñas coincide. Es decir, cuando el
    registro fue satisfactorio, se hace una conexión entre el usuario recién
    registrado y las tablas membership y personal.
    """
    user = db(db.auth_user.email == request.post_vars.email).select(db.auth_user.ALL)[0]

    if request.post_vars.seccion:
      depid = request.post_vars.seccion # El registrado pertenece directamente a una sección
    else:
      depid = request.post_vars.laboratorio

    membership_register = db.auth_membership.insert(user_id=user.id, 
                                                    group_id=request.post_vars.rol,
                                                    dependencia_asociada=depid,
                                                    f_personal_membership=request.post_vars.cedula)

    if membership_register is False:
      print("Violación en membership (No debería pasar si el usuario \
        no está registrado)")

    db.t_Personal.insert(f_nombre = request.post_vars.first_name,
                           f_apellido = request.post_vars.last_name,
                           f_ci = request.post_vars.cedula,
                           f_email = request.post_vars.email,
                           f_usuario = user.id,
                           f_telefono = 0,
                           f_pagina_web = "N/A",
                           f_categoria = "N/A",
                           f_cargo = "N/A",
                           f_fecha_ingreso = "1/01/1989",
                           f_fecha_salida = "1/02/1989",
                           f_dependencia = depid)
    
    # Registro exitoso. Retornar mensaje de exito y recordatorio de
    # actualización de datos.

  roles=list(db(db.auth_group.role != 'WebMaster').select(db.auth_group.ALL))

  return dict(roles=roles)

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