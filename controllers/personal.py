#-----------------------------------#
#                                   #
#  Controlador del Modulo Personal  #
#                                   #
#-----------------------------------#

def index():
    redirect(URL('listado_estilo'))
    return dict()

#Enviar info a la tabla del listado
def tabla_categoria(tipo):
    tb=[]

    #Buscamos la tabla general de personal
    if tipo =="listado":
        tb = db(db.t_Personal.f_validado == True)(db.t_Personal.f_es_supervisor == False)(db.t_Personal.f_oculto == False).select(db.t_Personal.ALL)

    #Buscamos la tabla general de empleados por validar
    elif tipo == "validacion" :
        usuario =db(db.t_Personal.f_email == auth.user.email).select(db.t_Personal.ALL)
        if(len(usuario)>1): usuario = usuario[1]
        else: usuario = usuario.first()
        es_supervisor = usuario.f_es_supervisor
        dependencia = None
        if es_supervisor:
            if(auth.user.email == "sigulabusb@gmail.com" or auth.user.email =="asis-ulab@usb.ve"):
                tb = db((db.t_Personal.f_por_validar == True)).select(db.t_Personal.ALL)

            else:
                dependencia = str(usuario.f_dependencia)
                tb = db((db.t_Personal.f_dependencia == dependencia)&(db.t_Personal.f_es_supervisor == False)&(db.t_Personal.f_por_validar == True)&(db.t_Personal.f_oculto == False)
                              ).select(db.t_Personal.ALL)


    #Creamos una lista para enviar a la vista
    jsns = []


    #Llenamos la lista con los json
    for elm in tb:

        #Buscamos el nombre de la dependencia con el id que manda la vista
        named = db(db.dependencias.id == elm.f_dependencia).select(db.dependencias.ALL)

        dep= named[0].nombre if len(named) > 0 else None

        if (dep) : idUSuperior = (db(db.dependencias.nombre==dep).select(db.dependencias.ALL)).first().unidad_de_adscripcion
        else: idUSuperior=None
        if (idUSuperior) : Usuperior=(db(db.dependencias.id==idUSuperior).select(db.dependencias.ALL)).first().nombre
        else: Usuperior=None

        jefe = buscarJefe(dep)
        ubicaciones = list(map(
            lambda x: str(x.espacio_fisico),
            db(db.es_encargado.tecnico == elm.id).select(db.es_encargado.ALL)
        ))
        ubicaciones = db(db.espacios_fisicos.id.belongs(ubicaciones)).select()
        extensiones_usb = '/'.join(list(filter(bool,
            list(map(lambda x: x.ext_USB, ubicaciones)) +
            list(map(lambda x: x.ext_USB_1, ubicaciones)) +
            list(map(lambda x: x.ext_USB_2, ubicaciones)) +
            list(map(lambda x: x.ext_USB_3, ubicaciones)) +
            list(map(lambda x: x.ext_USB_4, ubicaciones))
        )))
        extensiones_int = '/'.join(list(filter(bool,
            list(map(lambda x: x.ext_interna, ubicaciones))
        )))
        print(ubicaciones)
        jsns.append(
            {"nombre" : elm.f_nombre,
            "apellido" : elm.f_apellido,
            "ci" : elm.f_ci,
            "email" : elm.f_email,
            "email_alt" : elm.f_email_alt,
            "telefono" : elm.f_telefono,
            "pagina_web" : elm.f_pagina_web,
            "categoria" : elm.f_categoria,
            "cargo" : elm.f_cargo,
            "fecha_ingreso" : elm.f_fecha_ingreso,
            "fecha_salida" : elm.f_fecha_salida,
            "estatus" : elm.f_estatus,
            "dependencia" : dep,
             "celular" : elm.f_celular,
             "persona_contacto" : elm.f_persona_contacto,
             "contacto_emergencia" : elm.f_contacto_emergencia,
             "direccion" : elm.f_direccion,
             "gremio" : elm.f_gremio,
             "fecha_ingreso_usb" : elm.f_fecha_ingreso_usb,
             "fecha_ingreso_ulab" : elm.f_fecha_ingreso_ulab,
             "fecha_ingreso_admin_publica" : elm.f_fecha_ingreso_admin_publica,
             "condicion" : elm.f_condicion,
             "unidad_jerarquica_superior" : Usuperior,
             "rol" : elm.f_rol,
             "extensiones_usb" : extensiones_usb,
             "extensiones_int" : extensiones_int,
             "ubicacion" : '',
             "es_supervisor": elm.f_es_supervisor,
             "validado": elm.f_validado,
             "jefe": jefe
             })
    return jsns

#Mandar informacion a los dropdowns
def dropdowns():

    #Dropdown de gremio
    gremio = ['Docente', 'Administrativo', 'Estudiante']
    #Dropdown de dependencias
    departamento = db(db.dependencias.nombre).select(db.dependencias.ALL)
    #Dropdown de estatus
    estatus = ['Activo', 'Retirado', 'Jubilado']
    #Dropdown de categoria
    categoria = ['Fijo' , 'Contratado', 'Pasantía' , 'Ayudantía']
    #Dropdown de condiciones
    condiciones = ['En funciones', 'Año Sabático', 'Reposo', 'Permiso Pre-Natal', 'Permiso Post-Natal', 'Otro']
    #Dropdown de roles
    roles= ['Director', 'Asistente del Director', 'Gestor de SMyDP ', 'Administrador', 'Coordinador de Adquisiciones', 'Coordinador de Importaciones', 'Coordinador de la Calidad', 'Jefe de Laboratorio', 'Asistente de Laboratorio', 'Jefe de Sección', 'Personal de Dependencia', 'Técnico' ]
    #Dropdown de operadores
    operadores = ['+58414', '+58424', '+58412', '+58416', '+58426']


    return (gremio,departamento,estatus,categoria,condiciones,roles,operadores)

# Esta funcion toma la fecha desde el front que tiene
# el formato dd-mm-yyyy y la transforma en el formato
# yyyy-mm-dd
def transformar_fecha_formato_original(fecha):
    if fecha != '':
        dia = fecha[:2]
        mes = fecha[3:5]
        anio = fecha[6:]
        return anio + "-" + mes + "-" + dia
    else:
        return fecha

#Funcion que toma las variables de la vista
def add_form():
    dic = {"nombre" : request.post_vars.nombre_add,
            "apellido" : request.post_vars.apellido_add,
            "ci" : request.post_vars.ci_add,
            "email" : request.post_vars.email_add,
            "email_alt" : request.post_vars.email_alt_add,
            "telefono" : request.post_vars.telefono_add,
            "pagina_web" : request.post_vars.pagina_web_add,
            "categoria" : request.post_vars.categoria_add,
            "cargo" : request.post_vars.cargo_add,
            "fecha_ingreso" : transformar_fecha_formato_original(request.post_vars.fecha_ingreso_add),
            "fecha_salida" : transformar_fecha_formato_original(request.post_vars.fecha_salida_add),
            "estatus" : request.post_vars.estatus_add,
             "celular" : request.post_vars.operador_add+""+request.post_vars.celular_add,
             "persona_contacto": request.post_vars.persona_contacto,
             "contacto_emergencia" : request.post_vars.contacto_emergencia_add,
             "direccion" : request.post_vars.direccion_add,
             "gremio" : request.post_vars.gremio_add,
             "fecha_ingreso_usb" : transformar_fecha_formato_original(request.post_vars.fecha_ingreso_usb_add),
             "fecha_ingreso_ulab" : transformar_fecha_formato_original(request.post_vars.fecha_ingreso_ulab_add),
             "fecha_ingreso_admin_publica" : transformar_fecha_formato_original(request.post_vars.fecha_ingreso_admin_publica_add),
             "condicion" : request.post_vars.condicion_add,
             "dependencia" : request.post_vars.dependencia_add,
             "rol" : request.post_vars.rol_add,
            }

    ubicaciones = request.post_vars.ubicacion_add
    if type(ubicaciones) == str:
        ubicaciones = [ubicaciones]

    #Si el diccionario no esta vacio
    if (not(None in dic.values())):
        #Insertamos en la base de datos
        personal = db(db.t_Personal.f_email == dic['email'] )
        personal.update(f_nombre = dic["nombre"],
                                f_apellido = dic["apellido"],
                                f_ci = dic["ci"],
                                f_email = dic["email"],
                                f_email_alt = dic["email_alt"],
                                f_telefono = dic["telefono"],
                                f_pagina_web = dic["pagina_web"],
                                f_categoria = dic["categoria"],
                                f_cargo = dic["cargo"],
                                f_fecha_ingreso = dic["fecha_ingreso"],
                                f_fecha_salida = dic["fecha_salida"],
                                f_estatus = dic["estatus"],
                              f_celular= dic["celular"],
            f_persona_contacto = dic['persona_contacto'],
            f_contacto_emergencia= dic["contacto_emergencia"],
            f_direccion= dic["direccion"],
            f_gremio= dic["gremio"],
            f_fecha_ingreso_usb= dic["fecha_ingreso_usb"],
            f_fecha_ingreso_ulab= dic["fecha_ingreso_ulab"],
            f_fecha_ingreso_admin_publica= dic["fecha_ingreso_admin_publica"],
            f_condicion= dic["condicion"],
            f_por_validar=True,
            f_validado=False,
            f_comentario="",
            f_rol= dic["rol"])
        session.ficha_negada=""
        _id = personal.select().first().id
        db(db.es_encargado.tecnico == _id).delete()
        ubicaciones_a_insertar = list(map(
            lambda x: {'tecnico': _id, 'espacio_fisico': x},
            ubicaciones
        ))
        db.es_encargado.bulk_insert(ubicaciones_a_insertar)
        redirect(URL('listado_estilo'))


#Creamos la clase usuario que contiene la informacion del usuario que se entregara a la vista
class Usuario(object):
    """
    Esta clase usuario no tiene ninguna relacion con la base de datos, solamente
    es para facilitar la presentacion en el template.
    """
    def __init__(self, usuario):
        # pagina 1
        self.f_nombre = usuario.f_nombre
        self.f_apellido = usuario.f_apellido
        self.f_ci = usuario.f_ci
        self.f_email = usuario.f_email
        self.f_email_alt = usuario.f_email_alt
        dependencia = usuario.f_dependencia
        dependencia = db(db.dependencias.id == dependencia).select().first()
        self.f_dependencia = dependencia.nombre

        unidad_superior = db(db.dependencias.id == dependencia.unidad_de_adscripcion).select(db.dependencias.nombre)
        self.f_unidad_superior = unidad_superior
        self.f_telefono = usuario.f_telefono

        if(usuario.f_celular):
            self.f_operador = usuario.f_celular[:6]
            self.f_celular = usuario.f_celular[6:]
        else:
            self.f_operador = None
            self.f_celular = usuario.f_celular


        self.f_direccion = usuario.f_direccion
        self.f_persona_contacto = usuario.f_persona_contacto
        self.f_contacto_emergencia = usuario.f_contacto_emergencia
        self.f_pagina_web = usuario.f_pagina_web

        # pagina 2
        self.f_estatus = usuario.f_estatus
        self.f_categoria = usuario.f_categoria
        self.f_condicion = usuario.f_condicion
        self.f_fecha_ingreso = transformar_fecha(usuario.f_fecha_ingreso)
        self.f_fecha_salida = transformar_fecha(usuario.f_fecha_salida)
        self.f_fecha_ingreso_usb = transformar_fecha(usuario.f_fecha_ingreso_usb)
        self.f_fecha_ingreso_ulab = transformar_fecha(usuario.f_fecha_ingreso_ulab)
        self.f_fecha_ingreso_admin_publica = transformar_fecha(usuario.f_fecha_ingreso_admin_publica)

        # pagina 3
        self.f_cargo = usuario.f_cargo
        self.f_gremio = usuario.f_gremio
        self.f_ubicacion = list(map(
            lambda x: str(x.espacio_fisico),
            db(db.es_encargado.tecnico == usuario.id).select()
        ))
        self.f_rol = usuario.f_rol
        # dependencia ya dada arriba
        self.f_es_supervisor = usuario.f_es_supervisor
        self.f_persona_contacto = usuario.f_persona_contacto

#Funcion que envia los datos a la vista
@auth.requires_login(otherwise=URL('modulos', 'login'))
def listado():
    session.ficha_negada = db(db.t_Personal.f_email == auth.user.email).select(db.t_Personal.f_comentario).first().f_comentario

    #Obtenemos el usuario loggeado
    infoUsuario=(db(db.auth_user.id==auth.user.id).select(db.auth_user.ALL)).first()
    usuario = Usuario(infoUsuario.t_Personal.select().first())
    #Obtenemos los datos para el listado
    tabla = tabla_categoria("listado")

    #Dropdown ubicaciones
    idDependencia = db(db.dependencias.nombre == usuario.f_dependencia).select(db.dependencias.id)[0]
    ubicaciones= list(db(db.espacios_fisicos.dependencia == idDependencia).select(db.espacios_fisicos.ALL))
    #Obtenemos los elementos de los dropdowns
    gremios, dependencias, estados, categorias, condiciones, roles, operadores = dropdowns()

    empleados = validacion_estilo()['empleados']


    return dict(
        grid=tabla,
        categorias=categorias,
        dependencias=dependencias,
        estados=estados,
        gremios=gremios,
        condiciones=condiciones,
        roles=roles,
        operadores=operadores,
        ubicaciones=ubicaciones,
        usuario=usuario,
        empleados = empleados
        )

def transformar_fecha(fecha):
    dias_meses = {
        1: '01',
        2: '02',
        3: '03',
        4: '04',
        5: '05',
        6: '06',
        7: '07',
        8: '08',
        9: '09',
    }
    if fecha != None:
        if fecha.day < 10 and fecha.month < 10:
            return dias_meses[fecha.day] + "-" + dias_meses[fecha.month] + "-" + str(fecha.year)
        elif fecha.day < 10:
            return dias_meses[fecha.day] + "-" + str(fecha.month) + "-" + str(fecha.year)
        elif fecha.month < 10:
            return str(fecha.day) + "-" + dias_meses[fecha.month] + "-" + str(fecha.year)
        else:
            return str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year)



@auth.requires_login(otherwise=URL('modulos', 'login'))
def ficha():
    # Obtenemos la cédula
    ci = request.args[0]

    # Buscamos en la base de datos
    personal = db(db.t_Personal.f_ci == ci).select()[0]
    infoUsuario = db(db.t_Personal.f_ci == ci).select(db.t_Personal.ALL).first()
    usuario = Usuario(infoUsuario)

    #Obtenemos el usuario loggeado
    infoUsuario_logged=(db(db.auth_user.id==auth.user.id).select(db.auth_user.ALL)).first()
    usuario_logged = Usuario(infoUsuario_logged.t_Personal.select().first())

    #Buscamos el nombre de la dependencia con el id que manda la vista
    elm = personal
    named = db(db.dependencias.id == elm.f_dependencia).select(db.dependencias.ALL)

    dep= named[0].nombre if len(named) > 0 else None

    if (dep) : idUSuperior = (db(db.dependencias.nombre==dep).select(db.dependencias.ALL)).first().unidad_de_adscripcion
    else: idUSuperior=None
    if (idUSuperior) : Usuperior=(db(db.dependencias.id==idUSuperior).select(db.dependencias.ALL)).first().nombre
    else: Usuperior=None
    ext_USB = ''
    ext_int = ''
    if ext_USB: ext_USB=ext_USB.ext_USB[0]
    if ext_int: ext_int=ext_int.ext_interna

    # db(db.es_encargado.tecnico == usuario.id).select()
    ubicaciones = list(map(
        lambda x: x.espacio_fisico,
        db(db.es_encargado.tecnico == infoUsuario.id).select()
    ))
    ubicaciones = db(db.espacios_fisicos.id.belongs(ubicaciones)).select()

    personal ={
        "nombre" : elm.f_nombre,
        "apellido" : elm.f_apellido,
        "ci" : elm.f_ci,
        "email" : elm.f_email,
        "email_alt" : elm.f_email_alt,
        "telefono" : elm.f_telefono,
        "pagina_web" : elm.f_pagina_web,
        "categoria" : elm.f_categoria,
        "cargo" : elm.f_cargo,
        "fecha_ingreso" : transformar_fecha(elm.f_fecha_ingreso),
        "fecha_salida" : transformar_fecha(elm.f_fecha_salida),
        "estatus" : elm.f_estatus,
        "dependencia" : dep,
        "celular" : elm.f_celular,
        "persona_contacto" : elm.f_persona_contacto,
        "contacto_emergencia" : elm.f_contacto_emergencia,
        "direccion" : elm.f_direccion,
        "gremio" : elm.f_gremio,
        "fecha_ingreso_usb" : transformar_fecha(elm.f_fecha_ingreso_usb),
        "fecha_ingreso_ulab" : transformar_fecha(elm.f_fecha_ingreso_ulab) ,
        "fecha_ingreso_admin_publica" : transformar_fecha(elm.f_fecha_ingreso_admin_publica),
        "condicion" : elm.f_condicion,
        "unidad_jerarquica_superior" : Usuperior,
        "rol" : elm.f_rol,
        "extension_USB" : ext_USB,
        "extension_interna" : ext_int,
        "ubicaciones" : ubicaciones,
        "es_supervisor": elm.f_es_supervisor,
        "validado": elm.f_validado,
        "por_validar": elm.f_por_validar,
        "jefe": buscarJefe(dep)
    }

    validacion = request.post_vars.validacion
    if(validacion == "true" or validacion == "false"):
        cambiar_validacion(validacion, personal)



    #Dropdown ubicaciones
    idDependencia = db(db.dependencias.nombre == usuario.f_dependencia).select(db.dependencias.id)[0]
    ubicaciones= list(db(db.espacios_fisicos.dependencia == idDependencia).select(db.espacios_fisicos.ALL))
    #Obtenemos los elementos de los dropdowns
    gremios, dependencias, estados, categorias, condiciones, roles, operadores = dropdowns()

    print(usuario)

    return dict(
        personal=personal,
        categorias=categorias,
        dependencias=dependencias,
        estados=estados,
        gremios=gremios,
        condiciones=condiciones,
        roles=roles,
        operadores=operadores,
        ubicaciones=ubicaciones,
        usuario_logged=usuario_logged,
        usuario = usuario
    )

def cambiar_validacion(validacion, personal):
    if(validacion == "true"):
        mensaje = ''
        db(db.t_Personal.f_email == personal['email']).update(f_por_validar=False, f_validado=True, f_comentario=mensaje)
        accion = '[Personal] Ficha Validada de Personal '+ personal['nombre']+ " "+personal['apellido'] 
        db.bitacora_general.insert(f_accion = accion)
    elif (validacion == "false"):
        mensaje = request.post_vars.razon_add
        db(db.t_Personal.f_email == personal['email']).update(
            f_por_validar=False, f_validado=False, f_comentario='Motivo de Rechazo: {}'.format(mensaje))
        cuerpo = ' \n Estimado usuario la ficha de personal que envio para ser validada fue rechazada por su supervisor,\nMotivo de Rechazo:\n\t {}'.format(mensaje)
        
        #__enviar_correo(personal['email'],'[SIGULAB] Ficha Personal Rechazada',cuerpo)
        __enviar_correo('gabrieleduardogg@gmail.com','[SIGULAB] Ficha Personal Rechazada',cuerpo)
    redirect(URL('listado_estilo'))


@auth.requires_login(otherwise=URL('modulos', 'login'))
def listado_estilo():
    return listado()

@auth.requires_login(otherwise=URL('modulos', 'login'))
def validacion():
    usuario =db(db.t_Personal.f_email == auth.user.email).select(db.t_Personal.ALL).first()
    if(usuario.f_es_supervisor == False):
        redirect(URL('listado'))
    #diccionario = listado()
    dic = { 'empleados' : buscarEmpleados()}
    return dic

@auth.requires_login(otherwise=URL('modulos', 'login'))
def validacion_estilo():
    val = contar_notificaciones(auth.user.email)
    infoUsuario=(db(db.auth_user.id==auth.user.id).select(db.auth_user.ALL)).first()
    usuario = Usuario(infoUsuario.t_Personal.select().first())

    session.validaciones_pendientes = val
    #dic = { 'empleados' : buscarEmpleados()}
    dic = { 'empleados' : tabla_categoria("validacion")}
    return dic

def contar_notificaciones(correo):
    #usuario =db(db.t_Personal.f_email == auth.user.email).select(db.t_Personal.ALL)
    usuario =db(db.t_Personal.f_email == correo).select(db.t_Personal.ALL)
    
    if(len(usuario)>1): usuario = usuario[1]
    else: usuario = usuario.first()
    es_supervisor = usuario.f_es_supervisor
    dependencia = None
    if es_supervisor:
        if(auth.user.email == "sigulabusb@gmail.com") or (auth.user.email == "asis-ulab@usb.ve"):
            notif = db(db.t_Personal.f_por_validar == True).count()
        else:
            dependencia = usuario.f_dependencia
            notif = db((db.t_Personal.f_dependencia == dependencia)&(db.t_Personal.f_es_supervisor == False)&(db.t_Personal.f_por_validar == True)).count()
    else:
        notif=0
    return notif

def buscarJefe(dependencia_trabajador):
    unidad_adscripcion = db(db.dependencias.nombre == dependencia_trabajador).select(db.dependencias.id)[0].id

    if unidad_adscripcion:
        idJefe = db(db.dependencias.id == unidad_adscripcion).select(db.dependencias.id_jefe_dependencia).first().id_jefe_dependencia
    else:
        idGestor = db(db.auth_group.role == "DIRECTOR").select(db.auth_group.id).first().id
        idJefe = db(db.auth_membership.group_id == idGestor).select(db.auth_membership.user_id).first().user_id

    correo = db(db.auth_user.id == idJefe).select(db.auth_user.email)[0].email
    return correo

#Funcion para ocultar 
def eliminar():
    if auth.user.email != 'sigulabusb@gmail.com':
        return redirect(URL('listado_estilo'))
    ci = request.post_vars.cedula_eliminar

    personal = db(db.t_Personal.f_ci == ci).select(db.t_Personal.ALL).first()

    db(db.t_Personal.f_ci == ci).update(f_oculto = True)

    accion = '[Personal] Ficha Ocultada de Personal '+ personal.f_nombre+ " "+personal.f_apellido 
    db.bitacora_general.insert(f_accion = accion)
    redirect(URL('listado_estilo'))

def reporte():
    tabla=tabla_categoria()
    personas=[]
    for persona in tabla:
        personas.append(persona)
    return dict(personas=personas)

def __enviar_correo(destinatario, asunto, cuerpo):
    mail = auth.settings.mailer
    mail.send(destinatario, asunto, cuerpo)