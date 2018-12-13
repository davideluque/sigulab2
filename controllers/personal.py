#-----------------------------------#
#                                   #
#  Controlador del Modulo Personal  #
#                                   #
#-----------------------------------#

@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
    usuario = db(db.t_Personal.f_email==auth.user.registration_id).select().first()
    if usuario:
        return dict(usuario=usuario, ci=usuario.f_ci)
    else:
        return dict(usuario=usuario)

def busqueda():
    gremios, dependencias, estados, categorias, condiciones, roles, operadores, competencias, nivel= dropdowns()
    return dict(
        gremios=gremios,
        competencias=competencias
    )

def resultados_busqueda():

    from gluon.serializers import json
    from datetime import date, datetime

    rows = db((db.t_Personal.id == db.t_Competencias2.f_Competencia_Personal)
            & (db.t_Personal.id == db.t_Historial_trabajo_nuevo.f_Historial_trabajo_Personal)).select()
    lista = []
    hoy = date.today()
    aniversario_ulab = datetime.strptime('05-06', '%d-%m').date()

    if request.post_vars['fecha_busqueda']:
        aniversario_ulab=aniversario_ulab.replace(
                year=int(request.post_vars['fecha_busqueda'][-4:]))
    else:
        aniversario_ulab=aniversario_ulab.replace(
                year=hoy.year+1 if aniversario_ulab < hoy else hoy.year)

    for row in rows:
        ingreso = row.t_Personal.f_fecha_ingreso_ulab
        aniosAdmin = row.t_Personal.f_fecha_ingreso_admin_publica
        fechaAdmin = request.post_vars.fecha_admin_busqueda

        if (fechaAdmin==""):
            fechaAdmin = date.today()
        else:
            fechaAdmin = datetime.strptime(fechaAdmin, "%d-%m-%Y")
            fechaAdmin = fechaAdmin.date()

        cargos = [row.t_Historial_trabajo_nuevo.f_cargo_hist_1, row.t_Historial_trabajo_nuevo.f_cargo_hist_2,
        row.t_Historial_trabajo_nuevo.f_cargo_hist_3, row.t_Historial_trabajo_nuevo.f_cargo_hist_4, row.t_Historial_trabajo_nuevo.f_cargo_hist_5]

        encontrado = "False"
        for cargo in cargos:
            if (request.post_vars.cargo_busqueda.lower() in cargo.lower()):
                encontrado = "True"
                break

        lista.append({
            'ci' : row.t_Personal.f_ci,
            'nombre' : row.t_Personal.f_nombre+' '+row.t_Personal.f_apellido,
            'correo' : row.t_Personal.f_email,
            'telefono' : row.t_Personal.f_telefono,
            'dependencia' : db.dependencias[row.t_Personal.f_dependencia].nombre,
            'gremio' : row.t_Personal.f_gremio,
            'competencia' : row.t_Competencias2.f_nombre,
            'categorias' : row.t_Competencias2.f_categorias,
            'anios-servicio': (aniversario_ulab-ingreso).days/365 if ingreso else 0,
            'anios-admin': (fechaAdmin-aniosAdmin).days/365 if aniosAdmin else 0,
            'cargo' : encontrado
            })
    return dict(lista=lista, filtros=request.post_vars, ani=aniversario_ulab)

def miFicha():
    return ficha()

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
        separador = ' / '
        extensiones_usb = separador.join(list(filter(bool,
            list(map(lambda x: x.ext_USB, ubicaciones)) +
            list(map(lambda x: x.ext_USB_1, ubicaciones)) +
            list(map(lambda x: x.ext_USB_2, ubicaciones)) +
            list(map(lambda x: x.ext_USB_3, ubicaciones)) +
            list(map(lambda x: x.ext_USB_4, ubicaciones))
        )))
        extensiones_int = separador.join(list(filter(bool,
            list(map(lambda x: x.ext_interna, ubicaciones))
        )))
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

    # Competencias
    competencias = [
            "Administración", "Alimentación", "Ambiente", "Arquitectura", "Arte", "Biología", "Calidad", "Ciencias del Agro",
            "Ciencias del mar", "Comunicación", "Contaduría", "Crecimiento Personal", "Derecho", "Dietética", "Docencia", "Economía",
            "Electrónica", "Estadística", "Filosofía", "Física", "Gerencia", "Gestión", "Humanidades", "Idiomas", "Información",
            "Informática", "Ingeniería", "Letras", "Liderazgo", "Matemática", "Medicina", "Música", "Negocio", "Nutrición",
            "Química", "Recreación", "Salud Laboral", "Seguridad", "Tecnología", "Urbanismo",
            ]

    nivel = ["Bachillerato", "Técnico Medio", "TSU", "Licenciatura", "Especialización", "Maestría", "Doctorado", "Post-Doctorado"]

    return (gremio,departamento,estatus,categoria,condiciones,roles,operadores, competencias, nivel)

# Esta funcion toma la fecha desde el front que tiene
# el formato dd-mm-yyyy y la transforma en el formato
# yyyy-mm-dd
def transformar_fecha_formato_original(fecha):
    if fecha:
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
             "fecha_inicio_1" : transformar_fecha_formato_original(request.post_vars.fecha_inicio_1_add),
             "fecha_final_1" : transformar_fecha_formato_original(request.post_vars.fecha_final_1_add),
             "dependencia_hist_1" : request.post_vars.dependencia_hist_1_add,
             "organizacion_1" : request.post_vars.organizacion_1_add,
             "cargo_hist_1": request.post_vars.cargo_hist_1_add,
             "rol_hist_1": request.post_vars.rol_hist_1_add,
             "fecha_inicio_2" : transformar_fecha_formato_original(request.post_vars.fecha_inicio_2_add),
             "fecha_final_2" : transformar_fecha_formato_original(request.post_vars.fecha_final_2_add),
             "dependencia_hist_2" : request.post_vars.dependencia_hist_2_add,
             "organizacion_2" : request.post_vars.organizacion_2_add,
             "cargo_hist_2": request.post_vars.cargo_hist_2_add,
             "rol_hist_2": request.post_vars.rol_hist_2_add,
             "fecha_inicio_3" : transformar_fecha_formato_original(request.post_vars.fecha_inicio_3_add),
             "fecha_final_3" : transformar_fecha_formato_original(request.post_vars.fecha_final_3_add),
             "dependencia_hist_3" : request.post_vars.dependencia_hist_3_add,
             "organizacion_3" : request.post_vars.organizacion_3_add,
             "cargo_hist_3": request.post_vars.cargo_hist_3_add,
             "rol_hist_3": request.post_vars.rol_hist_3_add,
             "fecha_inicio_4" : transformar_fecha_formato_original(request.post_vars.fecha_inicio_4_add),
             "fecha_final_4" : transformar_fecha_formato_original(request.post_vars.fecha_final_4_add),
             "dependencia_hist_4" : request.post_vars.dependencia_hist_4_add,
             "organizacion_4" : request.post_vars.organizacion_4_add,
             "cargo_hist_4": request.post_vars.cargo_hist_4_add,
             "rol_hist_4": request.post_vars.rol_hist_4_add,
             "fecha_inicio_5" : transformar_fecha_formato_original(request.post_vars.fecha_inicio_5_add),
             "fecha_final_5" : transformar_fecha_formato_original(request.post_vars.fecha_final_5_add),
             "dependencia_hist_5" : request.post_vars.dependencia_hist_5_add,
             "organizacion_5" : request.post_vars.organizacion_5_add,
             "cargo_hist_5": request.post_vars.cargo_hist_5_add,
             "rol_hist_5": request.post_vars.rol_hist_5_add,
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

        # Añadir al historial de trabajo

        db.t_Historial_trabajo_nuevo.update_or_insert(
            db.t_Historial_trabajo_nuevo.f_Historial_trabajo_Personal== personal.select().first().id,
            f_fecha_inicio_1 = dic["fecha_inicio_1"],
            f_fecha_final_1 = dic["fecha_final_1"],
            f_dependencia_hist_1 = dic["dependencia_hist_1"],
            f_organizacion_1 = dic["organizacion_1"],
            f_cargo_hist_1 = dic["cargo_hist_1"],
            f_rol_hist_1 = dic["rol_hist_1"],
            f_fecha_inicio_2 = dic["fecha_inicio_2"],
            f_fecha_final_2 = dic["fecha_final_2"],
            f_dependencia_hist_2 = dic["dependencia_hist_2"],
            f_organizacion_2 = dic["organizacion_2"],
            f_cargo_hist_2 = dic["cargo_hist_2"],
            f_rol_hist_2 = dic["rol_hist_2"],
            f_fecha_inicio_3 = dic["fecha_inicio_3"],
            f_fecha_final_3 = dic["fecha_final_3"],
            f_dependencia_hist_3 = dic["dependencia_hist_3"],
            f_organizacion_3 = dic["organizacion_3"],
            f_cargo_hist_3 = dic["cargo_hist_3"],
            f_rol_hist_3 = dic["rol_hist_3"],
            f_fecha_inicio_4 = dic["fecha_inicio_4"],
            f_fecha_final_4 = dic["fecha_final_4"],
            f_dependencia_hist_4 = dic["dependencia_hist_4"],
            f_organizacion_4 = dic["organizacion_4"],
            f_cargo_hist_4 = dic["cargo_hist_4"],
            f_rol_hist_4 = dic["rol_hist_4"],
            f_fecha_inicio_5 = dic["fecha_inicio_5"],
            f_fecha_final_5 = dic["fecha_final_5"],
            f_dependencia_hist_5 = dic["dependencia_hist_5"],
            f_organizacion_5 = dic["organizacion_5"],
            f_cargo_hist_5 = dic["cargo_hist_5"],
            f_rol_hist_5 = dic["rol_hist_5"],
            f_Historial_trabajo_Personal= personal.select().first().id
            )

        session.ficha_negada=""
        _id = personal.select().first().id
        db(db.es_encargado.tecnico == _id).delete()
        ubicaciones_a_insertar = list(map(
            lambda x: {'tecnico': _id, 'espacio_fisico': x},
            ubicaciones
        ))
        db.es_encargado.bulk_insert(ubicaciones_a_insertar)

        personal = personal.select().first()
        named = db(db.dependencias.id == personal.f_dependencia).select(db.dependencias.ALL)
        if len(named) > 0:
            dep = named.first().nombre
            destinatario = buscarJefe(dep)
            usuario_supervisor = db(db.auth_user.email == destinatario).select().first()
            first_name = usuario_supervisor.first_name
            last_name = usuario_supervisor.last_name
            asunto = '[SIGULAB] Ficha Editada'
            cuerpo = '''
            <html>
            <head>
            <meta charset='UTF-8' />
            </head>
            <body>
            <h3>Saludos, estimado(a) {f_nombre} {f_apellido}</h3>
            <p>
                Le notificamos que la ficha de {f_nombre_validar} {f_apellido_validar}
                fue editada. Le invitamos a validar dicha edición.
            </p>
            </body>
            </html>
            '''.format(f_nombre=first_name, f_apellido=last_name,
            f_nombre_validar=dic['nombre'], f_apellido_validar=dic['apellido'])
            mail.send(destinatario, asunto, cuerpo)

        personal = db(db.t_Personal.f_email == dic['email'] ).select().first()
        __get_competencias(request, personal)
        __get_administrativas(request, personal)
        __get_extension(request, personal)
        __get_proyectos(request, personal)
        __get_trabajos(request, personal)
        __get_cursos(request, personal)
        __get__materias(request,personal)
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
        self.f_organizacion_1 = ""

        def setHist(self, historial):
            pass

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
    gremios, dependencias, estados, categorias, condiciones, roles, operadores, competencias, nivel= dropdowns()

    empleados = validacion_estilo()['empleados']
    idUser = db(db.t_Personal.f_ci == usuario.f_ci).select().first().id
    historial_rows = db(db.t_Historial_trabajo_nuevo.f_Historial_trabajo_Personal == idUser).select().first()


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
        empleados = empleados,
        competencias=competencias,
        nivel=nivel,
        comp_list=lista_competencias(usuario.f_ci),
        admin_list=lista_administrativas(usuario.f_ci),
        ext_list=lista_extension(usuario.f_ci),
        historial = getDictHistorial(historial_rows),
        proy_list = lista_proyectos(usuario.f_ci),
        trabajo_list=lista_trabajo(usuario.f_ci),
        evento_list=lista_cursos(usuario.f_ci),
        materia_list=lista_materias(usuario.f_ci)
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
    personal = db(db.t_Personal.f_ci == ci).select().first()
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
    gremios, dependencias, estados, categorias, condiciones, roles, operadores, competencias, nivel = dropdowns()

    historial_rows = db(db.t_Historial_trabajo_nuevo.f_Historial_trabajo_Personal == elm.id).select().first()

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
        usuario=usuario,
        competencias=competencias,
        nivel=nivel,
        comp_list=lista_competencias(personal['ci']),
        ext_list=lista_extension(personal['ci']),
        admin_list=lista_administrativas(personal['ci']),
        historial=getDictHistorial(historial_rows),
        proy_list=lista_proyectos(usuario.f_ci),
        trabajo_list=lista_trabajo(personal['ci']),
        evento_list=lista_cursos(personal['ci']),
        materia_list=lista_materias(personal['ci'])
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

    usuario = db(db.t_Personal.f_email == personal['email']).select().first()
    first_name = usuario.f_nombre
    last_name = usuario.f_apellido
    email = usuario.f_email
    es_supervisor = usuario.f_es_supervisor
    motivo = usuario.f_comentario if validacion == 'false' else ''
    destinatario = email
    _reason = 'validada' if validacion == 'true' else 'rechazada'
    asunto = '[SIGULAB] Ficha {}'.format(_reason)
    cuerpo = '''
    <html>
    <head>
      <meta charset='UTF-8' />
    </head>
    <body>
      <h3>Saludos, estimado(a) {f_nombre} {f_apellido}</h3>
      <p>
        Le notificamos que su ficha fue {action}
      </p>
      <p>
        {motivo}
      </p>
    </body>
    </html>
    '''.format(f_nombre=first_name, f_apellido=last_name, f_email=email, action=_reason,
        motivo=motivo
      )
    mail.send(destinatario, asunto, cuerpo)
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
        if(correo == "sigulabusb@gmail.com") or (correo == "asis-ulab@usb.ve"):
            notif = db(db.t_Personal.f_por_validar == True).count()
        else:
            dependencia = usuario.f_dependencia
            notif = db((db.t_Personal.f_dependencia == dependencia)&(db.t_Personal.f_es_supervisor == False)&(db.t_Personal.f_por_validar == True)).count()
    else:
        notif=0
    return notif

def buscarJefe(dependencia_trabajador):
    unidad_adscripcion = db(db.dependencias.nombre == dependencia_trabajador).select(db.dependencias.id).first()

    if unidad_adscripcion:
        idJefe = db(db.dependencias.id == unidad_adscripcion.id).select(db.dependencias.id_jefe_dependencia).first().id_jefe_dependencia
    else:
        idGestor = db(db.auth_group.role == "DIRECTOR").select(db.auth_group.id).first().id
        idJefe = db(db.auth_membership.group_id == idGestor).select(db.auth_membership.user_id).first().user_id

    correo = db(db.auth_user.id == idJefe).select(db.auth_user.email).first()
    if correo:
        correo = correo.email
    else:
        correo = None
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
def reporte_listado():
    if request.post_vars:
        accion = '[Personal] Reporte de Personal Generado'
        db.bitacora_general.insert(f_accion = accion)
    return redirect(URL('listado_estilo'))

def lista_competencias(ci):
    query = db((db.t_Personal.id == db.t_Competencias2.f_Competencia_Personal)
            & (db.t_Personal.f_ci == ci))
    rows = query.select(db.t_Competencias2.ALL, orderby=db.t_Competencias2.f_numero)
    return rows

def lista_administrativas(ci):
    query = db((db.t_Personal.id == db.t_Administrativas.f_Administrativas_Personal)
            & (db.t_Personal.f_ci == ci))
    rows = query.select(db.t_Administrativas.ALL, orderby=db.t_Administrativas.f_numero)
    return rows

def lista_extension(ci):
    query = db((db.t_Personal.id == db.t_Extension2.f_Extension_Personal)
            & (db.t_Personal.f_ci == ci))
    rows = query.select(db.t_Extension2.ALL, orderby=db.t_Extension2.f_numero)
    return rows

def lista_proyectos(ci):
    query = db((db.t_Personal.id == db.t_Proyecto.f_proyecto_Personal)
            & (db.t_Personal.f_ci == ci))
    rows = query.select(db.t_Proyecto.ALL, orderby=db.t_Proyecto.f_numero)
    return rows

def lista_trabajo(ci):
    query = db((db.t_Personal.id == db.t_Trabajos_dirigidos.f_Trabajo_Personal)
            & (db.t_Personal.f_ci == ci))
    rows = query.select(db.t_Trabajos_dirigidos.ALL, orderby=db.t_Trabajos_dirigidos.f_numero)
    return rows

def lista_cursos(ci):
    query = db((db.t_Personal.id == db.t_Cursos.f_Cursos_Personal)
            & (db.t_Personal.f_ci == ci))
    rows = query.select(db.t_Cursos.ALL, orderby=db.t_Cursos.f_numero)
    return rows

def lista_materias(ci):
    query = db((db.t_Personal.f_ci == ci) & (db.t_Personal.id == db.t_Materia2.f_Materia_Personal))
    rows = query.select(db.t_Materia2.ALL, orderby=db.t_Materia2.f_area)
    return rows

def getDictHistorial(historial):
    dic = {}
    if (historial != None):
        dic = {  "f_fecha_inicio_1" : transformar_fecha(historial.f_fecha_inicio_1),
                 "f_fecha_final_1" : transformar_fecha(historial.f_fecha_final_1),
                 "f_dependencia_hist_1" : historial.f_dependencia_hist_1,
                 "f_organizacion_1" : historial.f_organizacion_1,
                 "f_cargo_hist_1": historial.f_cargo_hist_1,
                 "f_rol_hist_1": historial.f_rol_hist_1,
                 "f_fecha_inicio_2" : transformar_fecha(historial.f_fecha_inicio_2),
                 "f_fecha_final_2" : transformar_fecha(historial.f_fecha_final_2),
                 "f_dependencia_hist_2" : historial.f_dependencia_hist_2,
                 "f_organizacion_2" : historial.f_organizacion_2,
                 "f_cargo_hist_2": historial.f_cargo_hist_2,
                 "f_rol_hist_2": historial.f_rol_hist_2,
                 "f_fecha_inicio_3" : transformar_fecha(historial.f_fecha_inicio_3),
                 "f_fecha_final_3" : transformar_fecha(historial.f_fecha_final_3),
                 "f_dependencia_hist_3" : historial.f_dependencia_hist_3,
                 "f_organizacion_3" : historial.f_organizacion_3,
                 "f_cargo_hist_3": historial.f_cargo_hist_3,
                 "f_rol_hist_3": historial.f_rol_hist_3,
                 "f_fecha_inicio_4" : transformar_fecha(historial.f_fecha_inicio_4),
                 "f_fecha_final_4" : transformar_fecha(historial.f_fecha_final_4),
                 "f_dependencia_hist_4" : historial.f_dependencia_hist_4,
                 "f_organizacion_4" : historial.f_organizacion_4,
                 "f_cargo_hist_4": historial.f_cargo_hist_4,
                 "f_rol_hist_4": historial.f_rol_hist_4,
                 "f_fecha_inicio_5" : transformar_fecha(historial.f_fecha_inicio_5),
                 "f_fecha_final_5" : transformar_fecha(historial.f_fecha_final_5),
                 "f_dependencia_hist_5" : historial.f_dependencia_hist_5,
                 "f_organizacion_5" : historial.f_organizacion_5,
                 "f_cargo_hist_5": historial.f_cargo_hist_5,
                 "f_rol_hist_5": historial.f_rol_hist_5,
        }
    else:
        dic = {  "f_fecha_inicio_1" : '',
                 "f_fecha_final_1" : '',
                 "f_dependencia_hist_1" : '',
                 "f_organizacion_1" : '',
                 "f_cargo_hist_1": '',
                 "f_rol_hist_1": '',
                 "f_fecha_inicio_2" : '',
                 "f_fecha_final_2" : '',
                 "f_dependencia_hist_2" : '',
                 "f_organizacion_2" : '',
                 "f_cargo_hist_2": '',
                 "f_rol_hist_2": '',
                 "f_fecha_inicio_3" : '',
                 "f_fecha_final_3" : '',
                 "f_dependencia_hist_3" : '',
                 "f_organizacion_3" : '',
                 "f_cargo_hist_3": '',
                 "f_rol_hist_3": '',
                 "f_fecha_inicio_4" : '',
                 "f_fecha_final_4" : '',
                 "f_dependencia_hist_4" : '',
                 "f_organizacion_4" : '',
                 "f_cargo_hist_4": '',
                 "f_rol_hist_4": '',
                 "f_fecha_inicio_5" : '',
                 "f_fecha_final_5" : '',
                 "f_dependencia_hist_5" : '',
                 "f_organizacion_5" : '',
                 "f_cargo_hist_5": '',
                 "f_rol_hist_5": '',
        }
    return dic

def __get_competencias(request, personal):
    params = {}
    competencias = []
    for i in range(1,11):
        params = {
                'f_nombre' : request.post_vars['competencia{}_nombre'.format(i)],
                'f_categoria' : request.post_vars['competencia{}_categoria'.format(i)],
                'f_observaciones' : request.post_vars['competencia{}_observaciones'.format(i)],
                'f_numero': i,
                'f_Competencia_Personal': personal.id
                }
        if ( params['f_nombre'] and params['f_categoria'] ):
            try:
                db.t_Competencias2.update_or_insert(
                        (db.t_Competencias2.f_numero==i)&
                        (db.t_Competencias2.f_Competencia_Personal==personal.id),
                        f_nombre=params['f_nombre'],
                        f_categorias=params['f_categoria'],
                        f_observaciones= params['f_observaciones'],
                        f_numero= params['f_numero'],
                        f_Competencia_Personal= params['f_Competencia_Personal'],
                        )
            except Exception as e:
                print(e)

        else:
            try:
                db( (db.t_Competencias2.f_Competencia_Personal == personal.id)
                    & (db.t_Competencias2.f_numero == i)).delete()
            except Exception as e:
                print(e)

    return competencias

def __get_administrativas(request, personal):
    params = {}
    administrativas = []
    for i in range(1, 6):
        params = {
                'f_fecha_inicio': transformar_fecha_formato_original(request.post_vars['administrativa{0}_desde'.format(i)]),
                'f_fecha_final': transformar_fecha_formato_original(request.post_vars['administrativa{0}_hasta'.format(i)]),
                'f_cargo': request.post_vars['administrativa{0}_cargo'.format(i)],
                'f_institucion': request.post_vars['administrativa{0}_institucion'.format(i)],
                'f_numero': i,
                'f_Administrativas_Personal': personal.id
                }
        if not( None in params.values() or '' in params.values()):
            try:
                db.t_Administrativas.update_or_insert(
                        (db.t_Administrativas.f_numero==i)
                        & (db.t_Administrativas.f_Administrativas_Personal==personal.id),
                        f_fecha_inicio=params['f_fecha_inicio'],
                        f_fecha_final=params['f_fecha_final'],
                        f_institucion=params['f_institucion'],
                        f_cargo=params['f_cargo'],
                        f_numero=params['f_numero'],
                        f_Administrativas_Personal=params['f_Administrativas_Personal'],
                        )
                administrativas.append(params)
            except Exception as e:
                print(e)
        else:
            try:
                db( (db.t_Administrativas.f_Administrativas_Personal == personal.id)
                    & (db.t_Administrativas.f_numero == i)).delete()
            except Exception as e:
                print(e)

    return BEAUTIFY(administrativas)
    # return administrativas

def __get_extension(request, personal):
    params = {}
    extension = []
    for i in range(1, 6):
        params = {
                'f_fecha_inicio': transformar_fecha_formato_original(
                    request.post_vars['extension{0}_desde'.format(i)]),
                'f_fecha_final': transformar_fecha_formato_original(
                    request.post_vars['extension{0}_hasta'.format(i)]),
                'f_nombre': request.post_vars['extension{0}_nombre'.format(i)],
                'f_institucion': request.post_vars['extension{0}_institucion'.format(i)],
                'f_descripcion': request.post_vars['extension{0}_descripcion'.format(i)],
                'f_categoria': request.post_vars['extension{0}_categoria'.format(i)],
                'f_numero': i,
                'f_Extension_Personal': personal.id
                }
        if not( None in params.values() or '' in params.values()):
            try:
                db.t_Extension2.update_or_insert(
                        (db.t_Extension2.f_numero==i)
                        & (db.t_Extension2.f_Extension_Personal==personal.id),
                        f_fecha_inicio=params['f_fecha_inicio'],
                        f_fecha_final=params['f_fecha_final'],
                        f_institucion=params['f_institucion'],
                        f_nombre=params['f_nombre'],
                        f_descripcion=params['f_descripcion'],
                        f_categoria=params['f_categoria'],
                        f_numero=params['f_numero'],
                        f_Extension_Personal=params['f_Extension_Personal'],
                        )
                extension.append(params)
            except Exception as e:
                print(e)
        else:
            try:
                db( (db.t_Extension2.f_Extension_Personal == personal.id)
                    & (db.t_Extension2.f_numero == i)).delete()
            except Exception as e:
                print(e)
    return BEAUTIFY(extension)

def __get_proyectos(request, personal):
    params = {}
    proyecto = []
    for i in range(1, 11):
        params = {
                'f_categoria': request.post_vars['proyecto{0}_categoria'.format(i)],
                'f_fecha_inicio': transformar_fecha_formato_original(
                    request.post_vars['proyecto{0}_desde'.format(i)]),
                'f_fecha_fin': transformar_fecha_formato_original(
                    request.post_vars['proyecto{0}_hasta'.format(i)]),
                'f_titulo': request.post_vars['proyecto{0}_titulo'.format(i)],
                'f_responsabilidad': request.post_vars['proyecto{0}_responsabilidad'.format(i)],
                'f_resultados': request.post_vars['proyecto{0}_resultados'.format(i)],
                'f_institucion': request.post_vars['proyecto{0}_institucion'.format(i)],
                'f_numero': i,
                'f_proyecto_Personal': personal.id
                }
        if not( None in params.values() or '' in  params.values()):
            try:
                db.t_Proyecto.update_or_insert(
                        (db.t_Proyecto.f_numero==i)
                        & (db.t_Proyecto.f_proyecto_Personal==personal.id),
                        f_categoria=params['f_categoria'],
                        f_fecha_inicio=params['f_fecha_inicio'],
                        f_fecha_fin=params['f_fecha_fin'],
                        f_titulo=params['f_titulo'],
                        f_responsabilidad=params['f_responsabilidad'],
                        f_resultados=params['f_resultados'],
                        f_institucion=params['f_institucion'],
                        f_numero=params['f_numero'],
                        f_proyecto_Personal=params['f_proyecto_Personal'],
                        )
                proyecto.append(params)
            except Exception as e:
                print(e)
        else:
            try:
                db( (db.t_Proyecto.f_proyecto_Personal == personal.id)
                    & (db.t_Proyecto.f_numero == i)).delete()
            except Exception as e:
                print(e)
    return proyecto


def __get_trabajos(request, personal):
    params = {}
    trabajos = []
    for i in range(1,6):
        params = {
                'f_titulo_trabajo' : request.post_vars['trabajo{}_titulo_trabajo'.format(i)],
                'f_nivel' : request.post_vars['trabajo{}_nivel'.format(i)],
                'f_anio' : request.post_vars['trabajo{}_anio'.format(i)],
                'f_estudiantes' : request.post_vars['trabajo{}_estudiantes'.format(i)],
                'f_institucion' : request.post_vars['trabajo{}_institucion'.format(i)],
                'f_numero': i,
                'f_Trabajo_Personal': personal.id
                }
        if not(None in params.values() or '' in params.values()):
            try:
                db.t_Trabajos_dirigidos.update_or_insert(
                        (db.t_Trabajos_dirigidos.f_numero==i)&
                        (db.t_Trabajos_dirigidos.f_Trabajo_Personal==personal.id),
                        f_titulo_trabajo=params['f_titulo_trabajo'],
                        f_nivel=params['f_nivel'],
                        f_anio= params['f_anio'],
                        f_estudiantes= params['f_estudiantes'],
                        f_institucion= params['f_institucion'],
                        f_numero= params['f_numero'],
                        f_Trabajo_Personal= params['f_Trabajo_Personal'],
                        )
                trabajos.append(params)
            except Exception as e:
                print(e)
        else:
            try:
                db( (db.t_Trabajos_dirigidos.f_Trabajo_Personal == personal.id)
                    & (db.t_Trabajos_dirigidos.f_numero == i)).delete()
            except Exception as e:
                print(e)

    return trabajos

def __get_cursos(request, personal):
    params = {}
    cursos = []
    for i in range(1,11):
        params = {
                'f_categorias' : request.post_vars['evento{0}_categoria'.format(i)],
                'f_anio' : request.post_vars['evento{0}_anio'.format(i)],
                'f_formacion' : request.post_vars['evento{0}_formacion'.format(i)],
                'f_horas' : request.post_vars['evento{0}_horas'.format(i)],
                'f_dictadoPor' : request.post_vars['evento{0}_dictadoPor'.format(i)],
                'f_numero': i,
                'f_Cursos_Personal': personal.id
                }
        if not( None in params.values() or '' in params.values()):
            try:
                db.t_Cursos.update_or_insert(
                    (db.t_Cursos.f_numero==i)
                    & (db.t_Cursos.f_Cursos_Personal==personal.id),
                    f_categorias=params['f_categorias'],
                    f_anio=params['f_anio'],
                    f_formacion= params['f_formacion'],
                    f_horas= params['f_horas'],
                    f_dictadoPor= params['f_dictadoPor'],
                    f_numero= params['f_numero'],
                    f_Cursos_Personal= params['f_Cursos_Personal'],)
                cursos.append(params)
            except Exception as e:
                print(e)
        else:
            try:
                db( (db.t_Cursos.f_Cursos_Personal == personal.id)
                    & (db.t_Cursos.f_numero == i)).delete()
            except Exception as e:
                print(e)
    return BEAUTIFY(cursos)

def __get__materias(request, personal):
    params = {}
    materia = []
    for i in range(1,6):
        params = {
            'f_area' : request.post_vars['materia{}_area'.format(i)],
            'f_codigo' : request.post_vars['materia{}_codigo'.format(i)],
            'f_nombre_materia' : request.post_vars['materia{}_nombre_materia'.format(i)],
            'f_fecha_inicio_materia' : transformar_fecha_formato_original(request.post_vars['materia{}_fecha_inicio_materia'.format(i)]),
            'f_fecha_final_materia' : transformar_fecha_formato_original(request.post_vars['materia{}_fecha_final_materia'.format(i)]),
            'f_numero' : i,
            'f_Materia_Personal' : personal.id
        }
        if not ( None in params.values() or '' in params.values()):
            try:
                db.t_Materia2.update_or_insert(
                    (db.t_Materia2.f_numero == i) & (db.t_Materia2.f_Materia_Personal == personal.id),
                    f_area = params['f_area'],
                    f_codigo = params['f_codigo'],
                    f_nombre_materia = params['f_nombre_materia'],
                    f_fecha_inicio_materia = params['f_fecha_inicio_materia'],
                    f_fecha_final_materia = params['f_fecha_final_materia'],
                    f_numero= params['f_numero'],
                    f_Materia_Personal= params['f_Materia_Personal'],
                    )
                materia.append(params)
            except Exception as e:
                print(e)
        else:
            try:
                db( (db.t_Materia2.f_Materia_Personal == personal.id)
                    & (db.t_Materia2.f_numero == i)).delete()
            except Exception as e:
                print(e)
    return materia
