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
    return "$('#authdiv').html('Esta conexión no es segura. Prueba entrando a la página de nuevo. \
    Si continúas viendo este mensaje, contacta al administrador del sitio.')"

  if not '@' in request.post_vars.email_send:
    return "$('#authdiv').html('Correo inválido. Formato: algo@ejemplo.com')"

  user = auth.login_bare(request.post_vars.email_send, request.post_vars.pass_send)

  if not user:
    return "$('#authdiv').html('Datos de inicio de sesión incorrectos.')"
  else:
    accion = '[Sistema] Ingreso al sistema'
    db.bitacora_general.insert(f_accion = accion)
    url = URL('default','index')
    return '$(location).attr("href", "' + str(url) + '")'

def login():
  """
  @description Login obsoleto. Solo es utilizado para acceder a la página
  como tal y redireccionar en caso de que el usuario ya fue autenticado.

  @return Redirección a la página principal de elección de nuevos módulos
  en caso de que el usuario ya fue autenticado.
  """
  if auth.user:
    return redirect(URL('default', 'index'))

  auth.settings.login_next = URL('default','index')
  
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

  grupo_webmaster = db(db.auth_group.role == "WEBMASTER").select(db.auth_group.id)[0].id
  grupo_director = db(db.auth_group.role == "DIRECTOR").select(db.auth_group.id)[0].id
  grupo_asistente_director = db(db.auth_group.role == "ASISTENTE DEL DIRECTOR").select(
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
  """Valida que la cédula introducida tenga un formato válido.
  Este método se ejecuta cada vez que se abandona el campo "cedula" del
  registro de usuarios.
  """
  ci_format = re.compile("^[0-9]{6,8}$")
  if not re.match(ci_format, request.post_vars.cedula):
    return "jQuery('#auth_cedula__row').addClass('has-error');\
    jQuery('#cedula_error_group').addClass('has-error');\
    jQuery('#cedula_error').html('La cédula debe contener únicamente números. Ej:  12345678');\
    jQuery('#cedula_error_group').show();\
    jQuery('form').submit(false);"

  cedula = request.post_vars.tipo_cedula+request.post_vars.cedula
  personal_register = db(db.t_Personal.f_ci == cedula).select(db.t_Personal.ALL)

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
  """Valida que el correo electrónico introducido tenga un formato válido.
  Este método se ejecuta cada vez que se abandona el campo "Correo Eectrónico"
  del registro de usuarios.
  """
  email_format = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
  if not re.match(email_format, request.post_vars.email):
    return "jQuery('#auth_user_email__row').addClass('has-error');\
    jQuery('#email_error_group').addClass('has-error');\
    jQuery('#email_error').html('Introduce un correo válido. Ej: ejemplo@dominio.com');\
    jQuery('#email_error_group').show();\
    jQuery('form').submit(false);"

  auth_register = db(db.auth_user.email == request.post_vars.email).select(db.auth_user.ALL)
  
  # Verificar que no existe un registro en la base de datos con el email dado.
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
  siguientes grupos: Grupo Webmaster, grupo DIRECTOR, grupo Asistente del
  DIRECTOR o Coordinadora de la Calidad.
  """
  ### Realizar registro de usuario ###
  if request.vars and request.vars.registrar == "do_register":
    auth_register = auth.register_bare(username=request.post_vars.first_name,
                                        last_name=request.post_vars.last_name,
                                        email=request.post_vars.email,
                                        password=request.post_vars.password)
    registrado = request.post_vars.first_name + " "+request.post_vars.last_name+" - "+ request.post_vars.email
    accion = '[Sistema] Registro de nuevo usuario: {}'.format(registrado) 
    db.bitacora_general.insert(f_accion = accion)

    # Si el servidor se cayera en este punto sería un error fatal.
    # Debe haber un mensaje de error cuando un usuario que ingresa no tiene
    # un registro asociado en las tabla personal y membership. Esto puede
    # pasar porquese registró manualmente en appadmin o el caso anteriormente
    # mencionado.

    if auth_register is False:
      """La verificación de usuario ya registrado se hace mediante ajax
      en el método validar email. Ese método deshabilita el registro
      mediante jquery. Se podría hacer una segunda verificación de seguridad
      acá.
      """
      response.flash=T("Usuario ya registrado")

    """Después de haber hecho la verificación de correo electrónico no tomado
    y que la verificación de contraseñas coincide. Es decir, cuando el
    registro fue satisfactorio, se hace una conexión entre el usuario recién
    registrado y las tablas membership y personal. Ademas, se crea una entrada
    en la tabla "es_tecnico" si el usuario tiene el rol de tecnico.
    """
    user = db(db.auth_user.email == request.post_vars.email).select(db.auth_user.ALL)[0]
    es_supervisor = request.post_vars.tipo_supervisor
    es_tecnico = request.post_vars.tipo_personal


    if request.post_vars.rol and es_supervisor :
        rolid = request.post_vars.rol
        roltype = db(db.auth_group.id == int(rolid)).select(db.auth_group.ALL)[0].role
        depid = request.post_vars.dephidden
    elif (es_tecnico):
        rolid = db(db.auth_group.role == "TÉCNICO").select(db.auth_group.ALL)[0].id
        roltype = "TÉCNICO"
        depid= request.post_vars.dephidden
        
    else:
        rolid = db(db.auth_group.role == "PERSONAL INTERNO").select(db.auth_group.ALL)[0].id
        roltype = "PERSONAL INTERNO"
        depid= request.post_vars.dephidden
    # Asocia el usuario al grupo indicado
    membership_register = db.auth_membership.insert(user_id=user.id,
                                                    group_id=rolid,
                                                    dependencia_asociada=depid,
                                                    f_personal_membership=request.post_vars.cedula)


    # Asocia el usuario a un registro genérico en la tabla de personal
    # para que posteriormente ingrese y actualice sus datos.
    nuevo_personal_id = db.t_Personal.insert(f_nombre = request.post_vars.first_name,
                           f_apellido = request.post_vars.last_name,
                           f_ci = request.post_vars.tipo_cedula+request.post_vars.cedula,
                           f_email = request.post_vars.email,
                           f_usuario = user.id,
                           f_dependencia = depid,
                           f_es_supervisor = es_supervisor,
                           f_comentario='Agregue sus datos personales')


    # Mapea el usuario al espacio fisico que tiene a cargo

    if roltype == "TÉCNICO":
      # Se agregan los espacios fisicos seleccionados por el usuario (tags) a la tabla
      # 'es_encargado'
      for trace, espacio in session.tags.iteritems():
        espacio_id = trace.split('-')[2]
        db.es_encargado.insert(espacio_fisico = espacio_id,
                               tecnico = nuevo_personal_id)

    # Registro exitoso. Retornar redirección a la misma página para evitar el
    # problema de doble POST con mensaje de exito y recordatorio de
    # actualización de datos personales.
    session.flash=T("Registro exitoso")
    return redirect('register')

  # Si aun no se ha llenado la forma o el usuario ha vuelto a cargar la pagina de
  # registro, se inicializa (o reestablece) la variable tags con los espacios
  # fisicos seleccionados por el usuario.
  if session.tags is None or not request.vars:
    session.tags = {}

    rolesDeseados=['DIRECTOR', 'ASISTENTE DEL DIRECTOR', 'GESTOR DE SMyDP', 'GESTOR DE PERSONAL', 'COORDINADOR', 'JEFE DE LABORATORIO', 'JEFE DE SECCIÓN', 'PERSONAL DE DEPENDENCIA']
    roles=db(db.auth_group.role.belongs(rolesDeseados)).select(db.auth_group.ALL)

    queryDireccion = db(db.dependencias.nombre == "DIRECCIÓN").select(db.dependencias.ALL).first()
  #Buscamos todas las dependencias cuya unidad de adscripcion sea la direccion
    dependencias=list(db(db.dependencias.unidad_de_adscripcion == queryDireccion.id).select(db.dependencias.ALL))


    idJefeSec = (db(db.auth_group.role == 'JEFE DE SECCIÓN').select(db.auth_group.ALL)).first().id

    prefijos_cedula = ['V-','E-', 'P-']

  return dict(roles=roles, dependencias=dependencias, idJefeSec = idJefeSec, prefijos_cedula=prefijos_cedula )

# Ajax Helper para la dependencia de acuerdo a su unidad de adscripcion
def ajax_unidad_rol():
  rolid = request.post_vars.rolhidden
  roltype = db(db.auth_group.id == int(rolid)).select(db.auth_group.ALL)[0].role
  direccion=db(db.dependencias.nombre == "DIRECCIÓN").select(db.dependencias.ALL)
  labs_y_coordinaciones=list(db(db.dependencias.unidad_de_adscripcion == direccion[0].id).select(db.dependencias.ALL))
  labs = []
  coordinaciones = []
  for i in labs_y_coordinaciones:
    if "LABORATORIO" in i.nombre:
      labs.append(i)
    else:
      coordinaciones.append(i)
  if roltype == "DIRECTOR" or roltype == "ASISTENTE DEL DIRECTOR" or roltype == "GESTOR DE SMyDP":
    lista = direccion
  elif roltype == "COORDINADOR" or roltype == "PERSONAL DE COORDINACIÓN":
    lista = coordinaciones
  elif roltype == "WEBMASTER" or roltype == "CLIENTE INTERNO":
    lista = False
  else:
    lista = labs
  return(dict(lista=lista))

# Ajax helper para crear una membership para el usuario recien registrado
def ajax_membership():

  session.depid = None
  session.rolid = int(request.post_vars.rol)
  session.ci = int(request.post_vars.cedula)
  if request.post_vars.laboratorio:
    session.depid = int(request.post_vars.laboratorio)
  if request.post_vars.seccion:
    session.depid = int(request.post_vars.seccion)
  return dict()

# Ajax Helper para mostrar dependencias a Tecnicos y Jefes de seccion
def ajax_registro_seccion():

  rolid = request.post_vars.rolhidden
  roltype = db(db.auth_group.id == int(rolid)).select(db.auth_group.ALL)[0].role
  secciones=False
  if roltype == "TÉCNICO" or roltype == "JEFE DE SECCIÓN":
    labid = request.post_vars.dephidden
    secciones=list(db(db.dependencias.unidad_de_adscripcion == int(labid)).select(db.dependencias.ALL))

  return dict(lista=secciones)

# Ajax Helper para mostrar espacios fisicos a Tecnicos
def ajax_registro_espacio():

  # Obteniendo la dependencia a la cual pertenece el tecnico
  rolid = request.post_vars.rolhidden
  roltype = db(db.auth_group.id == int(rolid)).select(db.auth_group.ALL)[0].role
  labid = request.post_vars.dephidden
  secid = request.post_vars.seccionhidden

  # Si usuario selecciona otro laboratorio, el id de este cambia, por lo que este laboratorio
  # deja de ser la dependencia de la seccion y no es necesario mostrar los espacios fisicos
  # que ya se habian desplegado. Quiza sea mejor reiniciar los elementos usando JS
  unidadid = int(db(db.dependencias.id == secid).select()[0].unidad_de_adscripcion)
  esta_adscrito = unidadid == int(labid)
  espacios = False

  if roltype == "TÉCNICO" and esta_adscrito:
    espacios = list(db(db.espacios_fisicos.dependencia == int(secid)).select())

  return dict(lista=espacios)


# Guardando los espacios seleccionados por el usuario para guardar en la case de datos
# aquellos espacios de los que el tecnico es responsable
def ajax_seleccionar_espacio():

  rolid = request.post_vars.rolhidden
  roltype = db(db.auth_group.id == int(rolid)).select(db.auth_group.ALL)[0].role
  depid = request.post_vars.dephidden
  secid = request.post_vars.seccionhidden
  espid = request.post_vars.esphidden

  espacio_nombre = db(db.espacios_fisicos.id == int(espid)).select()[0].codigo

  # Cuando se presiona para abrir la lista de espacios fisicos y se vuelve a pisar el boton
  # el evento "onclick" termina llamando esta funcion. Para no agregar ids vacios a session.tags
  if espid != '':
    session.tags[depid + "-" + secid + "-" + espid] = espacio_nombre

  # Los tags se mostraran solo si el usuario es un tecnico
  if roltype != "TÉCNICO":
    session.tags = {}

  return dict(tags=session.tags)

# Elimina de session.tags (la lista de espacios fisicos seleccionados por el usuario) el
# espacio que se desea eliminar
def ajax_eliminar_espacio():

  espid = request.post_vars.borrarhidden
  session.tags.pop(espid)
  return dict(tags=session.tags)

def ajax_mostrar_espacios():

  rolid = request.post_vars.rolhidden
  roltype = db(db.auth_group.id == int(rolid)).select(db.auth_group.ALL)[0].role

  # Los tags se mostraran solo si el usuario es un tecnico
  if roltype != "TÉCNICO":
    session.tags = {}

  return dict(tags=session.tags)


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
  """Despega un cohete espacial SPACE X a Marte.

  @returns Redirección al login.
  """
  accion = '[Sistema] Egreso del sistema'
  db.bitacora_general.insert(f_accion = accion)
  auth.logout()
  return redirect(URL('login'))
