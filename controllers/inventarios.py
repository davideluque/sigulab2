# -*- coding: utf-8 -*-
'''
Controlador de las vistas relacionadas a la gestión de inventarios,
vehículos y solicitudes de préstamos.
'''

# Importamos el diccionario con las categorias de los vehiculos.
from info_inventarios import CATEGORIAS_VEHICULOS, CLASIFICACIONES_VEHICULOS
from datetime import datetime

# < -------- Funciones privadas de Inventarios ------------>

# Función que envía un correo con los datos suministrados
def __enviar_correo(destinatario, asunto, cuerpo):
    mail = auth.settings.mailer
    mail.send(destinatario, asunto, cuerpo)

# Función que parsea como entero y retorna None en caso de no poder
def __safe_int(n):
    try:
        return int(n)
    except:
        return None

# Función que determina el estado de un documento secundario de vehículo como string,
# de acuerdo a su estado actual y la ficha que se revisa
def __get_estado_documento_vh(estado_actual, ficha="salida"):

    if ficha == "salida":
        if estado_actual == 0:
            return "No entregado"
        if estado_actual in [1, 2, 3]:
            return "Entregado"
    else:
        if estado_actual == 2:
            return "Devuelto"
        if estado_actual == 3:
            return "No devuelto"

    return None

# Funcion que devuelve un diccionario, con las categorias y
#subcategorias de los vehiculos
def __obtener_categorias():
    return CATEGORIAS_VEHICULOS

# Funcion que devuelve un diccionario, con las clasificaciones
# de los vehiculos
def __obtener_clasificaciones():
    return CLASIFICACIONES_VEHICULOS

# Verifica si el usuario que intenta acceder al controlador tiene alguno de los
# roles necesarios
def __check_role():
    roles_permitidos = ['WEBMASTER', 'DIRECTOR', 'ASISTENTE DEL DIRECTOR',
                        'COORDINADOR', 'PERSONAL DE DEPENDENCIA', 'TÉCNICO',
                        'JEFE DE LABORATORIO', 'JEFE DE SECCIÓN', 'PERSONAL INTERNO',
                        'GESTOR DE SMyDP']
    return True in [auth.has_membership(x) for x in roles_permitidos]

# Determina si el id de la dependencia es valido. Retorna False si el id no existe
# o es de un tipo incorrecto
def __is_valid_id(id_, tabla):
    try:
        int(id_)
    except:
        return False

    # Retorna si el id recibido existe en la base de datos
    return db(tabla.id == int(id_)).select()

# Determina si una variable "booleana" pasada como parametro con GET es realmente
# 'True' o 'False' (request.vars almacena todo como strings)
def __is_bool(bool_var):
    return bool_var in ['True', 'False']

# Dado el nombre de una dependencia, retorna el id de esta si la encuentra o
# None si no lo hace
def __find_dep_id(nombre):

    dep_id = db(db.dependencias.nombre == nombre).select()[0].id
    return dep_id

# Dado el id de un espacio fisico, retorna las sustancias que componen el inventario
# de ese espacio.
def __get_inventario_espacio(espacio_id=None):
    return db(db.bien_mueble.bm_espacio_fisico == espacio_id).select()

# Dado el id de un bien mueble, retorna las fichas de mantenimiento del bien.
def __get_mantenimiento_bm(bm_id=None):
    return db(db.historial_mantenimiento_bm.hmbm_nro == bm_id).select()


# Dado el id de un vehículo, retorna el historial de préstamo del vehículo
def __get_prestamos_vh(vh_id=None):
    prestamos = list(db(db.historial_prestamo_vh.hpvh_vh_id == vh_id).select())
    prestamos.reverse()

    prestamos_final = list()
    for prestamo in prestamos:
        if "Vehículo devuelto" == prestamo.hpvh_estatus or "Denegada" == prestamo.hpvh_estatus:
            prestamos_final.append(prestamo)

    return prestamos_final

# Dado el id de un espacio fisico, retorna las sustancias que componen el inventario
# de ese espacio.
def __get_inventario_materiales_espacio(espacio_id=None):
    return db( (db.sin_bn.sb_espacio == espacio_id) & (db.sin_bn.sb_clasificacion == 'Material de Laboratorio') ).select()

# Dado el id de un espacio fisico, retorna los consumibles que componen el inventario
# de ese espacio.
def __get_inventario_consumibles_espacio(espacio_id=None):
    return db((db.sin_bn.sb_espacio == espacio_id) & (db.sin_bn.sb_clasificacion == 'Consumible') ).select()

# Dado el id de un espacio fisico, retorna las herramientas que componen el inventario
# de ese espacio.
def __get_inventario_herramientas_espacio(espacio_id=None):
    return db(db.herramienta.hr_espacio_fisico == espacio_id).select()

# Retorna las hojas o dependencias que no tienen hijos (posiblemente secciones) y
# que estan por debajo de la dependencia dada.
# "jerarquia" tiene la forma:
#       {'dependencia1': [dep_hija1,
#                        .
#                        .
#                         dep_hijan]
#        'dependencia2': [dep_hija1,
#                         .
#                         .
#                         dep_hijam]
#     }
# Si una dependencia no tiene otras adscritas, entonces no aparece en "jerarquia"
def __get_leaves(dep_id, jerarquia):

    if dep_id not in jerarquia:
        return [dep_id]
    else:
        l = []
        for d in jerarquia[dep_id]:
            l = l + __get_leaves(d, jerarquia)
        return l


# Dada una lista de ids de dependencias que no poseen otras adscritas a ellas,
# retorna los ids de espacios fisicos en la base de datos que tienen a estas
# dependencias como secciones
def __filtrar_espacios(hojas):

    espacios = []
    for dep_id in hojas:
        nuevos_espacios = [esp.id for esp in db(db.espacios_fisicos.dependencia == dep_id).select()]
        if nuevos_espacios:
            espacios = espacios + nuevos_espacios
    return espacios

# Dado el id de una dependencia, retorna una lista con los ids de todos los
# espacios fisicos que pertenecen a esta. Si el id es de la ULAB, retorna
# todos los espacios fisicos
def __get_espacios(dep_id):
    espacios = []

    dependencias = db(db.dependencias.id > 0).select()

    # Creando lista de adyacencias
    lista_adyacencias = {dep.id: dep.unidad_de_adscripcion for dep in dependencias}

    # Representando la jerarquia con la forma {'dependencia': [dep_hija1, dep_hija2]}
    jerarquia = {}

    for hijo, padre in lista_adyacencias.iteritems():
        # Si el padre es None, es porque se trata de la unidad de laboratorios
        # que no tiene padre (nivel mas alto de la jerarquia)
        if padre is not None:
            if padre in jerarquia:
                jerarquia[padre].append(hijo)
            else:
                jerarquia[padre] = [hijo]

    hojas = __get_leaves(int(dep_id), jerarquia)

    espacios = __filtrar_espacios(hojas)

    return espacios

# Agrega los inventarios de los espacios en la lista "espacios"
def __sumar_inventarios(espacios):

    inventario_total = []
    for esp_id in espacios:
        inventario_total += __get_inventario_espacio(esp_id)
                      
    return inventario_total

def __sumar_inventarios_materiales(espacios):

    inventario_total = []
    for esp_id in espacios:
        inventario_total += __get_inventario_materiales_espacio(esp_id)
                      
    return inventario_total


def __sumar_inventarios_consumibles(espacios):

    inventario_total = []
    for esp_id in espacios:
        inventario_total += __get_inventario_consumibles_espacio(esp_id)
                      
    return inventario_total

def __sumar_inventarios_herramientas(espacios):

    inventario_total = []
    for esp_id in espacios:
        inventario_total += __get_inventario_herramientas_espacio(esp_id)
                      
    return inventario_total

# Dado el id de una dependencia, retorna una lista con el agregado de los bm
# que existen en los espacios fisicos que pertenecen a esta.
def __get_inventario_dep(dep_id):

    inventario = {}

    # Obteniendo lista de espacios bajo la dependencia con id dep_id
    espacios = __get_espacios(dep_id)

    # Agrega los inventarios de los espacios en la lista "espacios"
    inventario = __sumar_inventarios(espacios)

    return inventario


# Dado el id de una dependencia, retorna una lista con el agregado de los materiales
# que existen en los espacios fisicos que pertenecen a esta.
def __get_inventario_materiales_dep(dep_id):

    inventario = {}

    # Obteniendo lista de espacios bajo la dependencia con id dep_id
    espacios = __get_espacios(dep_id)

    # Agrega los inventarios de los espacios en la lista "espacios"
    inventario = __sumar_inventarios_materiales(espacios)

    return inventario


# Dado el id de una dependencia, retorna una lista con el agregado de los consumibles
# que existen en los espacios fisicos que pertenecen a esta.
def __get_inventario_consumibles_dep(dep_id):

    inventario = {}

    # Obteniendo lista de espacios bajo la dependencia con id dep_id
    espacios = __get_espacios(dep_id)

    # Agrega los inventarios de los espacios en la lista "espacios"
    inventario = __sumar_inventarios_consumibles(espacios)

    return inventario

# Dado el id de una dependencia, retorna una lista con el agregado de las herramientas
# que existen en los espacios fisicos que pertenecen a esta.
def __get_inventario_herramientas_dep(dep_id):

    inventario = {}

    # Obteniendo lista de espacios bajo la dependencia con id dep_id
    espacios = __get_espacios(dep_id)

    # Agrega los inventarios de los espacios en la lista "espacios"
    inventario = __sumar_inventarios_herramientas(espacios)

    return inventario

# Dado el id de un usuario, determina los ids de las dependencias de las cuales es jefe
def __es_jefe_de(user_id):
    dependencias = db(db.dependencias.id).select()

    lista_ids = set()
    for dep in dependencias:
        if dep['id_jefe_dependencia'] == user_id:
            lista_ids.add(dep['id'])

    return lista_ids

# Determina la cadena jerárquica de dependencias
def __ids_dependencias_jefe(dep_id):
    try:
        dependencia = db(db.dependencias.id == dep_id).select().first()
    except:
        return set()

    ids_validos = set()
    ids_validos.add(dep_id)

    while dep_id != 1:
        dep_id = dependencia['unidad_de_adscripcion']
        ids_validos.add(dep_id)
        try:
            dependencia = db(db.dependencias.id == dep_id).select().first()
        except:
            return ids_validos

    return ids_validos

# Dado el id de un usuario y el id de un vehículo, determina si el usuario puede
# ver el vehícuo dada su visibilidad
def __puede_ver_vehiculo(user_id, vh_id):
    try:
        vehiculo = db(db.vehiculo.id == vh_id).select().first()
    except:
        return False

    # Los que son visibles los puede ver todo el mundo
    if vehiculo['vh_oculto'] == 0:
        return True

    # El super-usuario puede ver todos los vehículos
    if auth.user.id == 1:
        return True

    # El responsable siempre puede ver su vehiculo
    if vehiculo['vh_responsable'] == user_id:
        return True

    # El custodio siempre puede ver su vehiculo
    if vehiculo['vh_custodio'] == user_id:
        return True

    # El personal de la misma dependencia siempre puede ver su vehiculo
    try:
        personal = db(db.t_Personal.f_usuario == user_id).select()[0]
        dependencia_id = personal.f_dependencia
    except:
        return False

    if vehiculo['vh_dependencia'] == dependencia_id:
        return True

    # Por último revisamos cadenas de jefes
    dep_es_jefe_usuario = __es_jefe_de(user_id)
    dep_jefes_autorizados = __ids_dependencias_jefe(vehiculo['vh_dependencia'])

    # Intersección entre los departamentos que el usuario es jefe
    # y los departamenos autorizados
    inter = dep_es_jefe_usuario.intersection(dep_jefes_autorizados)

    # Si alguno coincide, puede ver
    if len(inter) is not 0:
        return True

    # Si ningún criterio se cumple, impedimos la visibilidad
    return False

def __es_jefe_dep_vh(user_id, vh_id):

    # Obtenemos el vehículo
    try:
        vehiculo = db(db.vehiculo.id == vh_id).select().first()
    except KeyError:
        return False

    # Revisamos cadenas de jefes
    dep_es_jefe_usuario = __es_jefe_de(user_id)
    dep_jefes_autorizados = __ids_dependencias_jefe(vehiculo['vh_dependencia'])

    # Intersección entre los departamentos que el usuario es jefe
    # y los departamenos autorizados
    inter = dep_es_jefe_usuario.intersection(dep_jefes_autorizados)

    # Si alguno coincide, puede ver
    if len(inter) is not 0:
        return True

    # Si ningún criterio se cumple, impedimos la visibilidad
    return False

# Dado el id de una dependencia, retorna los vehiculos que pertenecen
# a esa dependencia.
def __get_vh_dep(dep_id=None):
    lista_vh = []
    query_vehiculos = db(db.vehiculo.vh_dependencia == dep_id).select()

    # Filtramos los eliminados
    for vehiculo in query_vehiculos:
        if vehiculo.vh_eliminar != 1:
            lista_vh.append(vehiculo)

    return lista_vh

# Dada la placa de un vehiculo, retorna las fichas de mantenimiento del vehiculo.
def __get_mantenimiento_vh(vh_id=None):
    mantenimiento = db(db.historial_mantenimiento_vh.hmvh_vh_id == vh_id).select()
    mantenimiento_ordenado = sorted(
        mantenimiento,
        key=lambda x: (x.hmvh_fecha_solicitud-datetime(1970,1,1)).total_seconds()
    )
    return mantenimiento_ordenado

# Registra una nueva entrada de mantenimiento para el vehículo dado
def __registrar_mantenimiento_vh(vehiculo, fecha_solicitud, nro_registro, proveedor, contacto,
                                 telf_contacto, motivo, tipo, descripcion, fecha_inicio, fecha_fin,
                                 piezas_reparadas, piezas_sustituidas, accion, observaciones,
                                 mant_id=None, modificacion=False):

    # Si ya está guardada esa orden de servicio y queremos agregarla
    if not modificacion and db(db.historial_mantenimiento_vh.hmvh_nro_registro == nro_registro).select():
        session.flash = "El Nº Registro (O/S) %s ya ha sido ingresado anteriormente." % nro_registro
        return False
    
    # Agregamos el registro nuevo
    if not modificacion:
        nuevo_id = db.historial_mantenimiento_vh.insert(
            hmvh_vh_id=vehiculo,
            hmvh_fecha_solicitud=fecha_solicitud,
            hmvh_nro_registro=nro_registro,
            hmvh_proveedor=proveedor,
            hmvh_contacto=contacto,
            hmvh_telf_contacto=telf_contacto,
            hmvh_motivo=motivo,
            hmvh_tipo=tipo,
            hmvh_descripcion=descripcion,
            hmvh_fecha_inicio=fecha_inicio,
            hmvh_fecha_fin=fecha_fin,
            hmvh_piezas_reparadas=piezas_reparadas,
            hmvh_piezas_sustituidas=piezas_sustituidas,
            hmvh_accion=accion,
            hmvh_observaciones=observaciones,
            hmvh_crea_mantenimiento=auth.user.id
        )

        db.bitacora_general.insert(
            f_accion="[inventarios] Creado historial de mantenimiento de vehículo con O/S {}".format(nro_registro)
        )

        return nuevo_id
    elif modificacion and mant_id is not None:
        id_mod = db(db.historial_mantenimiento_vh.id == mant_id).update(
            hmvh_vh_id=vehiculo,
            hmvh_fecha_solicitud=fecha_solicitud,
            hmvh_nro_registro=nro_registro,
            hmvh_proveedor=proveedor,
            hmvh_contacto=contacto,
            hmvh_telf_contacto=telf_contacto,
            hmvh_motivo=motivo,
            hmvh_tipo=tipo,
            hmvh_descripcion=descripcion,
            hmvh_fecha_inicio=fecha_inicio,
            hmvh_fecha_fin=fecha_fin,
            hmvh_piezas_reparadas=piezas_reparadas,
            hmvh_piezas_sustituidas=piezas_sustituidas,
            hmvh_accion=accion,
            hmvh_observaciones=observaciones,
            hmvh_crea_mantenimiento=auth.user.id
        )

        db.bitacora_general.insert(
            f_accion="[inventarios] Modificado historial de mantenimiento de vehículo con O/S {}".format(nro_registro)
        )

        return id_mod
    
    return False

# Registra un nueva bm en el espacio fisico indicado. Si el bm ya
# existe en el inventario, genera un mensaje con flash y no anade de nuevo
# el bm.
def __agregar_bm(nombre, no_bien, no_placa, marca, modelo, serial,
                 descripcion, material, color, calibrar, fecha_calibracion,
                 unidad_med, ancho, largo, alto, diametro, movilidad, uso,
                 estatus, nombre_cat, subcategoria, cod_loc, localizacion,
                 espacio, unidad_ad, dependencia, user, clasificacion):

    # Si ya existe el BM en el inventario
    if db(db.bien_mueble.bm_num == no_bien).select():
        bm = db(db.bien_mueble.bm_num == no_bien).select()[0]

        response.flash = "El BM \"{0}\" ya ha sido ingresado anteriormente \
                          al espacio \"{1}\".".format(bm.bm_nombre, bm.bm_espacio_fisico)
        return False

    if not unidad_med:
        ancho = None
        largo = None
        alto = None
        diametro = None

    # Si no, se agrega al inventario del espacio fisico la nueva sustancia
    db.bien_mueble.insert(
        bm_nombre=nombre,
        bm_num=no_bien,
        bm_placa=no_placa,
        bm_marca=marca,
        bm_modelo=modelo,
        bm_serial=serial,
        bm_descripcion=descripcion,
        bm_material=material,
        bm_color=color,
        bm_calibrar=calibrar,
        bm_fecha_calibracion=fecha_calibracion,
        bm_unidad=unidad_med,
        bm_ancho=ancho,
        bm_largo=largo,
        bm_alto=alto,
        bm_diametro=diametro,
        bm_movilidad=movilidad,
        bm_uso=uso,
        bm_estatus=estatus,
        bm_categoria=nombre_cat,
        bm_subcategoria=subcategoria,
        bm_codigo_localizacion=cod_loc,
        bm_localizacion=localizacion,
        bm_espacio_fisico=espacio,
        bm_unidad_de_adscripcion=unidad_ad,
        bm_depedencia=dependencia,
        bm_crea_ficha=user,
        bm_clasificacion=clasificacion
    )

    db.bitacora_general.insert(
        f_accion="[inventarios] Añadido el bien mueble num: {}".format(no_bien)
    )
    return redirect(URL(args=request.args, vars=request.get_vars, host=True))

# Registra un nuevo vehículo en la dependencia indicada. Si el vehiculo ya
# existe en el inventario, genera un mensaje con flash y no anade de nuevo
# el mismo.
def __agregar_vh(marca, modelo, ano, serial_motor, serial_carroceria, serial_chasis,
                 placa, intt, observaciones, lugar_pernocta, color, clase, uso, dependencia,
                 servicio, tara, tara_md, nro_puestos, nro_ejes, capacidad_carga, propietario,
                 responsable, telf_responsable, custodio, telf_custodio, sudebip_localizacion,
                 sudebip_codigo_localizacion, sudebip_categoria, sudebip_subcategoria,
                 sudebip_categoria_especifica, fecha_adquisicion, nro_adquisicion, origen,
                 proveedor, proveedor_rif, num, tipo, clasificacion, rines,
                 capacidad_carga_md, ubicacion_custodio, extension_custodio, extension_responsable,
                 donante, contacto_donante, oculto=0):

    # Si ya existe el VH en el inventario
    if db(db.vehiculo.vh_placa == placa).select():
        vh = db(db.vehiculo.vh_placa == placa).select()[0]

        nombre_dependencia = db(db.dependencias.id == vh.vh_dependencia).select()[0].nombre
        response.flash = "El vehiculo de placa \"{0}\" ya ha sido ingresado anteriormente \
                          a la dependencia \"{1}\".".format(vh.vh_placa, nombre_dependencia)
        return False

    # Si ya existe el numero de VH:
    if db(db.vehiculo.vh_num == int(num)).select():
        vh = db(db.vehiculo.vh_num == int(num)).select()[0]

        nombre_dependencia = db(db.dependencias.id == vh.vh_dependencia).select()[0].nombre
        response.flash = "El vehiculo de número \"{0}\" ya ha sido ingresado anteriormente \
                          a la dependencia \"{1}\".".format(vh.vh_num, nombre_dependencia)
        return False

    # Validación de seriales:
    if db(db.vehiculo.vh_serial_carroceria == serial_carroceria).select():
        vh = db(db.vehiculo.vh_serial_carroceria == serial_carroceria).select()[0]

        nombre_dependencia = db(db.dependencias.id == vh.vh_dependencia).select()[0].nombre
        response.flash = "El vehiculo de serial de carrocería \"{0}\" ya ha sido ingresado anteriormente \
                          a la dependencia \"{1}\".".format(vh.vh_serial_carroceria, nombre_dependencia)
        return False

    if db(db.vehiculo.vh_serial_chasis == serial_chasis).select():
        vh = db(db.vehiculo.vh_serial_chasis == serial_chasis).select()[0]

        nombre_dependencia = db(db.dependencias.id == vh.vh_dependencia).select()[0].nombre
        response.flash = "El vehiculo de serial de chasis \"{0}\" ya ha sido ingresado anteriormente \
                          a la dependencia \"{1}\".".format(vh.vh_serial_chasis, nombre_dependencia)
        return False

    if db(db.vehiculo.vh_serial_motor == serial_motor).select():
        vh = db(db.vehiculo.vh_serial_motor == serial_motor).select()[0]

        nombre_dependencia = db(db.dependencias.id == vh.vh_dependencia).select()[0].nombre
        response.flash = "El vehiculo de serial de motor \"{0}\" ya ha sido ingresado anteriormente \
                          a la dependencia \"{1}\".".format(vh.vh_serial_motor, nombre_dependencia)
        return False

    if db(db.vehiculo.vh_intt == intt).select():
        vh = db(db.vehiculo.vh_intt == intt).select()[0]

        nombre_dependencia = db(db.dependencias.id == vh.vh_dependencia).select()[0].nombre
        response.flash = "El vehiculo de número de autorización INTT \"{0}\" ya ha sido ingresado anteriormente \
                          a la dependencia \"{1}\".".format(vh.vh_intt, nombre_dependencia)
        return False

    # Se agrega el nuevo vehiculo a la base de datos
    db.vehiculo.insert(
        vh_num=int(num),
        vh_marca=marca,
        vh_modelo=modelo,
        vh_ano=ano,
        vh_extension_custodio=extension_custodio,
        vh_ubicacion_custodio=ubicacion_custodio,
        vh_serial_motor=serial_motor,
        vh_serial_carroceria=serial_carroceria,
        vh_serial_chasis=serial_chasis,
        vh_placa=placa,
        vh_rines=rines,
        vh_capacidad_carga_md=capacidad_carga_md,
        vh_intt=intt,
        vh_tipo=tipo,
        vh_clasificacion=clasificacion,
        vh_observaciones=observaciones,
        vh_lugar_pernocta=lugar_pernocta,
        vh_color=color,
        vh_clase=clase,
        vh_uso=uso,
        vh_servicio=servicio,
        vh_tara=tara,
        vh_tara_md=tara_md,
        vh_nro_puestos=nro_puestos,
        vh_nro_ejes=nro_ejes,
        vh_capacidad_carga=capacidad_carga,
        vh_propietario=propietario,
        vh_responsable=responsable,
        vh_telf_responsable=telf_responsable,
        vh_extension_responsable=extension_responsable,
        vh_custodio=custodio,
        vh_telf_custodio=telf_custodio,
        vh_sudebip_localizacion=sudebip_localizacion,
        vh_sudebip_codigo_localizacion=sudebip_codigo_localizacion,
        vh_sudebip_categoria=sudebip_categoria,
        vh_sudebip_subcategoria=sudebip_subcategoria,
        vh_sudebip_categoria_especifica=sudebip_categoria_especifica,
        vh_fecha_adquisicion=fecha_adquisicion,
        vh_origen=origen,
        vh_nro_adquisicion=nro_adquisicion,
        vh_proveedor=proveedor,
        vh_proveedor_rif=proveedor_rif,
        vh_donante=donante,
        vh_contacto_donante=contacto_donante,
        vh_oculto=oculto,
        vh_dependencia=dependencia,
        vh_crea_ficha=auth.user.id
        )

    db.bitacora_general.insert(
        f_accion="[inventarios] Añadido el vehiculo de placa : {}".format(placa)
    )

    session.flash = "El vehículo ha sido agregado satisfactoriamente."
    return redirect(URL(args=request.args, vars=request.get_vars, host=True))

# Registra un nuevo mantenimiento a un bm indicado.
def __agregar_mantenimiento_bm(no_bien, fecha_sol, codigo, tipo, servicio, accion,
                descripcion, proveedor, fecha_inicio, fecha_fin, tiempo_ejec,
                fecha_cert, observacion):

    db.historial_mantenimiento_bm.insert(
            hmbm_nro=no_bien,
            hmbm_fecha_sol=fecha_sol,
            hmbm_codigo=codigo,
            hmbm_tipo=tipo,
            hmbm_servicio=servicio,
            hmbm_accion=accion,
            hmbm_descripcion=descripcion,
            hmbm_proveedor=proveedor,
            hmbm_fecha_inicio=fecha_inicio,
            hmbm_fecha_fin= fecha_fin,
            hmbm_tiempo_ejec=tiempo_ejec,
            hmbm_fecha_cert=fecha_cert,
            hmbm_observacion=observacion
        )
    db.bitacora_general.insert(
        f_accion="[inventarios] Añadido historial de mantenimiento del bien mueble num: {}".format(no_bien)
    )
    return redirect(URL(args=request.args, vars=request.get_vars, host=True))


# Registra un nueva material/consumible en el espacio fisico indicado. Si el bm ya
# existe en el inventario, genera un mensaje con flash y no anade de nuevo
# el bm.
def __agregar_material(nombre, marca, modelo, cantidad, espacio, ubicacion,
                descripcion, aforado, calibrar, capacidad, unidad, unidad_dim,
                 ancho, largo, alto, diametro, material, material_sec, presentacion,
                 unidades,total, unidad_adscripcion, dependencia, user , clasificacion):

    espacio_nombre = db(db.espacios_fisicos.id == espacio).select().first().codigo
    # Si ya existe el BM en el inventario
    if (db( (db.sin_bn.sb_nombre == nombre) & (db.sin_bn.sb_espacio==espacio) ).select()):
        #bm = db(db.bien_mueble.bm_num == no_bien).select()[0]

        response.flash = "El BM \"{0}\" ya ha sido ingresado anteriormente \
                          en este espacio.".format(nombre)
        return False

    if not unidad_dim:
        ancho = None
        largo = None
        alto = None
        diametro = None

    # Si no, se agrega al inventario del espacio fisico la nueva sustancia
    db.sin_bn.insert(
        sb_cantidad=cantidad,
        sb_nombre=nombre,
        sb_marca=marca,
        sb_modelo=modelo,
        sb_descripcion=descripcion,
        sb_material=material,
        sb_material_sec=material_sec,
        sb_calibrar= calibrar,
        sb_unidad=unidad,
        sb_ancho=ancho,
        sb_largo=largo,
        sb_alto=alto,
        sb_diametro=diametro,
        sb_espacio=espacio,
        sb_clasificacion=clasificacion,
        sb_presentacion=presentacion,
        sb_unidades=unidades,
        sb_total=total,
        sb_aforado=aforado,
        sb_ubicacion=ubicacion,
        sb_capacidad=capacidad,
        sb_unidad_dim=unidad_dim,
        sb_unidad_de_adscripcion=unidad_adscripcion,
        sb_depedencia=dependencia,
        sb_crea_ficha=user,
    )
    db.bitacora_general.insert(
        f_accion="[inventarios] Añadido material de laboratorio. Nombre: {} Espacio físico: {}".format(nombre, espacio_nombre)
    )
    return redirect(URL(args=request.args, vars=request.get_vars, host=True))

# Registra un nueva material/consumible en la tabla de modiciaciones. Si el bm ya
# existe en el inventario, genera un mensaje con flash y no anade de nuevo
# el bm.
def __agregar_material_modificar(nombre, marca, modelo, cantidad, espacio, ubicacion,
                descripcion, aforado, calibrar, capacidad, unidad, unidad_dim,
                 ancho, largo, alto, diametro, material, material_sec, presentacion,
                 unidades,total, user , clasificacion, descripcion_mod):

    espacio_nombre = db(db.espacios_fisicos.id == espacio).select().first().codigo
    if (db( (db.modificacion_sin_bn.msb_nombre == nombre) & (db.modificacion_sin_bn.msb_espacio==espacio) ).select()):
        #bm = db(db.bien_mueble.bm_num == no_bien).select()[0]

        response.flash = "El  \"{0}\" tiene una modificación pendiente \
                          Por los momentos no se enviarán solicitudes de modificación.".format(clasificacion)
        return False

    response.flash = "Se ha enviado una solicidad de modificación del \"{0}\"  \"{1}\" \
                        .".format(clasificacion,nombre)

    if not unidad_dim:
        ancho = None
        largo = None
        alto = None
        diametro = None

    # Si no, se agrega al inventario del espacio fisico la nueva sustancia
    inv_id = db.modificacion_sin_bn.insert(
        msb_cantidad = cantidad,
        msb_nombre = nombre,  
        msb_marca = marca,
        msb_modelo = modelo,
        msb_descripcion = descripcion,
        msb_material = material,
        msb_material_sec = material_sec,
        msb_calibrar =  calibrar,
        msb_unidad = unidad,
        msb_ancho = ancho,
        msb_largo = largo,
        msb_alto = alto,
        msb_diametro = diametro,
        msb_espacio = espacio,
        msb_presentacion = presentacion,
        msb_unidades = unidades,
        msb_total = total,
        msb_aforado = aforado,
        msb_ubicacion = ubicacion,
        msb_capacidad = capacidad,
        msb_unidad_dim = unidad_dim,
        msb_modifica_ficha = user,
        msb_desc = descripcion_mod
    )
    db.bitacora_general.insert(
        f_accion="[inventarios] Añadida solicitud de modificación de un material de laboratorio. Nombre: {} Espacio físico: ".format(nombre, espacio_nombre)
    )
    response.flash = "Se ha realizado exitosamente la solicitud de modificación del material de laboratorio " + str(nombre)
    return True
    #return redirect(URL(args=request.args, vars=request.get_vars, host=True))

# Agrega una nueva solicitud de préstamos
def __solicitar_prestamo_vh(
        solicitante, vehiculo, fecha_solicitud, fecha_prevista_salida, fecha_prevista_devolucion,
        tiempo_previsto, tiempo_previsto_md, ruta, motivo_prestamo, nombre_conductor, ci_conductor,
        nro_conductor, licencia_conducir, certificado_medico, certificado_psicologico,
        nombre_usuario, ci_usuario, nro_usuario):

    usuario = db(db.auth_user.id == solicitante).select().first()
    vh = db(db.vehiculo.id == vehiculo).select().first()

    prestamo_id = db.historial_prestamo_vh.insert(
        hpvh_vh_id=vehiculo,
        hpvh_fecha_solicitud=fecha_solicitud,
        hpvh_fecha_prevista_salida=fecha_prevista_salida,
        hpvh_fecha_prevista_devolucion=fecha_prevista_devolucion,
        hpvh_solicitante=solicitante,
        hpvh_motivo=motivo_prestamo,
        hpvh_ruta=ruta,
        hpvh_tiempo_estimado_uso=tiempo_previsto,
        hpvh_tiempo_estimado_uso_md=tiempo_previsto_md,
        hpvh_conductor=nombre_conductor,
        hpvh_ci_conductor=ci_conductor,
        hpvh_nro_celular_conductor=nro_conductor,
        hpvh_nro_licencia_conductor=licencia_conducir,
        hpvh_certificado_psicologico=certificado_psicologico,
        hpvh_certificado_medico=certificado_medico,
        hpvh_usuario=nombre_usuario,
        hpvh_nro_celular_usuario=nro_usuario,
        hpvh_ci_usuario=ci_usuario
    )

    db.bitacora_general.insert(
        f_accion="[préstamos] Creada solicitud de préstamos. Vehículo: {}. Solicitante: {}".format(
            vh.vh_marca + " " + vh.vh_modelo + " " + vh.vh_placa,
            usuario.first_name + " " + usuario.last_name
        )
    )

    asunto_solicitud = "[SIGULAB] Solicitud #{} de Préstamo de Vehículos".format(prestamo_id)

    # Enviamos notificación al responsable patrimonial
    email_responsable = db(db.auth_user.id == vh.vh_responsable).select().first().email
    mensaje_solicitud_responsable = ("Estimado usuario, por medio de la presente le notificamos que el usuario {} {} ha SOLICITADO " + \
                                    "un préstamo de código #{} al vehículo {} {} {}, del cual usted es Responsable Patrimonial, " + \
                                    "en fecha {}. Para obtener más detalles del préstamo, ingrese a SIGULAB, módulo de " + \
                                    "gestión de INVENTARIOS, sección SOLICITUDES.").format(
                                    usuario.first_name,
                                    usuario.last_name,
                                    prestamo_id,
                                    vh.vh_marca,
                                    vh.vh_modelo,
                                    vh.vh_placa,
                                    datetime.now()
    )

    __enviar_correo(
        email_responsable,
        asunto_solicitud,
        mensaje_solicitud_responsable
    )

    # Enviamos notificación al solicitante
    email_solicitante = usuario.email
    mensaje_rechazo_solicitante = ("Estimado usuario, por medio de la presente le notificamos que usted ha SOLICITADO " + \
                                    "un préstamo de código #{} al vehículo {} {} {}, " + \
                                    "en fecha {}. Recibirá una notificación por correo electrónico al momento de que la " + \
                                    "solicitud sea aprobada o rechazada por el personal autorizado.").format(
                                    prestamo_id,
                                    vh.vh_marca,
                                    vh.vh_modelo,
                                    vh.vh_placa,
                                    datetime.now()
    )

    # Manda correo rechazo a solicitante
    __enviar_correo(
        email_solicitante,
        asunto_solicitud,
        mensaje_rechazo_solicitante
    )

    return True

# Registra un nueva material/consumible en el espacio fisico indicado. Si el bm ya
# existe en el inventario, genera un mensaje con flash y no anade de nuevo
# el bm.
def __agregar_herramienta(nombre, num, marca, modelo, serial, presentacion, numpiezas,
                contenido, descripcion, material, unidad, ancho, largo, alto, diametro,
                ubicacion, observacion, espacio,unidad_adscripcion, dependencia, user):

    espacio_nombre = db(db.espacios_fisicos.id == espacio).select().first().codigo
    # Si ya existe el BM en el inventario
    if (db( (db.herramienta.hr_nombre == nombre) & (db.herramienta.hr_espacio_fisico==espacio) & (db.herramienta.hr_ubicacion==ubicacion)).select()):
        #bm = db(db.bien_mueble.bm_num == no_bien).select()[0]

        response.flash = "El BM \"{0}\" ya ha sido ingresado anteriormente \
                          en este espacio.".format(nombre)
        return False
    if num:
        if (db((db.herramienta.hr_num == num)).select()):
            response.flash = "El BM con Nro de Bien Nacional \"{0}\" ya ha \
                            sido ingresado anteriormente.".format(num)
            return False

    # Verificamos si la variable es un conjunto o una unidad
    if presentacion=='Unidad':
        numpiezas='1'
        contenido=None
        descripcion=None

    if not unidad:
        ancho = None
        largo = None
        alto = None
        diametro = None

    # Si no, se agrega al inventario del espacio fisico la nueva sustancia
    inv_id = db.herramienta.insert(
        hr_nombre = nombre,
        hr_num=num,  
        hr_marca = marca,
        hr_modelo = modelo,
        hr_serial = serial,
        hr_presentacion = presentacion,
        hr_numpiezas= numpiezas,
        hr_contenido =contenido,
        hr_descripcion = descripcion,
        hr_material = material,
        hr_unidad = unidad,
        hr_ancho = ancho,
        hr_largo = largo,
        hr_alto = alto,
        hr_diametro = diametro,
        hr_espacio_fisico = espacio,
        hr_ubicacion = ubicacion,
        hr_observacion= observacion,
        hr_unidad_de_adscripcion = unidad_adscripcion,
        hr_depedencia = dependencia,
        hr_crea_ficha = user,
    )
    db.bitacora_general.insert(
        f_accion="[inventarios] Añadida una herramienta. Nombre: {}. Espacio físico: {}".format(nombre, espacio_nombre)
    )
    return redirect(URL(args=request.args, vars=request.get_vars, host=True))

def __agregar_herramienta_modificar(nombre, num, marca, modelo, serial, presentacion, numpiezas,
                contenido, descripcion, material, unidad, ancho, largo, alto, diametro,
                ubicacion, observacion, motivo, espacio,unidad_adscripcion, dependencia, user1, user2):

    espacio_nombre = db(db.espacios_fisicos.id == espacio).select().first().codigo
    if (db( (db.modificacion_herramienta.mhr_nombre == nombre) & (db.modificacion_herramienta.mhr_espacio_fisico==espacio) & (db.modificacion_herramienta.mhr_ubicacion==ubicacion)).select()):
        #bm = db(db.bien_mueble.bm_num == no_bien).select()[0]

        response.flash = "La herramienta \"{0}\" tiene una modificación pendiente \
                          Por los momentos no se enviarán solicitudes de modificación.".format(nombre)
        return False

    response.flash = "Se ha enviado una solicidad de modificación de la herramienta \"{0}\" \
                        .".format(nombre)

        # Verificamos si la variable es un conjunto o una unidad
    if presentacion=='Unidad':
        numpiezas='1'
        contenido=None
        descripcion=None

    if not unidad:
        ancho = None
        largo = None
        alto = None
        diametro = None

    # Si no, se agrega al inventario del espacio fisico la nueva sustancia
    inv_id = db.modificacion_herramienta.insert(
        mhr_nombre =nombre,
        mhr_num=num,  
        mhr_marca=marca,
        mhr_modelo=modelo,
        mhr_serial=serial,
        mhr_presentacion=presentacion,
        mhr_numpiezas= numpiezas,
        mhr_contenido =contenido,
        mhr_descripcion=descripcion,
        mhr_material=material,
        mhr_unidad=unidad,
        mhr_ancho=ancho,
        mhr_largo=largo,
        mhr_alto=alto,
        mhr_diametro=diametro,
        mhr_espacio_fisico=espacio,
        mhr_ubicacion=ubicacion,
        mhr_observacion= observacion,
        mhr_motivo=motivo,
        mhr_unidad_de_adscripcion=unidad_adscripcion,
        mhr_depedencia=dependencia,
        mhr_crea_ficha=user1,
        mhr_modifica_ficha=user2
    )
    db.bitacora_general.insert(
        f_accion="[inventarios] Añadida una solicitud de modificación de herramienta. Nombre: {}. Espacio físico: {}".format(nombre, espacio_nombre)
    )
    response.flash = "Se ha realizado exitosamente la solicitud de modificación de la herramienta " + str(nombre)
    return True
    #return redirect(URL(args=request.args, vars=request.get_vars, host=True))

# Funcion para agregar una modificacion pendiente a un vehiculo
def __agregar_modificar_vehiculo(id_vh, marca, modelo, ano, serial_motor, serial_carroceria, serial_chasis,
                                 placa, intt, observaciones, lugar_pernocta, color, clase, uso, dependencia,
                                 servicio, tara, tara_md, nro_puestos, nro_ejes, capacidad_carga, propietario,
                                 responsable, telf_responsable, custodio, telf_custodio, sudebip_localizacion,
                                 sudebip_codigo_localizacion, sudebip_categoria, sudebip_subcategoria,
                                 sudebip_categoria_especifica, fecha_adquisicion, nro_adquisicion, origen,
                                 proveedor, proveedor_rif, num, tipo, clasificacion, user, rines,
                                 capacidad_carga_md, ubicacion_custodio, extension_custodio, extension_responsable,
                                 donante, contacto_donante, motivo, oculto=0):

    # Si ya existe una modificacion pendiente al vehículo
    if db(db.modificacion_vehiculo.mvh_id_vehiculo == id_vh).select():
        vh = db(db.vehiculo.id== id_vh).select()[0] #Se busca de la tabla de vh POR ID (no varía)
        response.flash = "El vehiculo de placa \"{0}\" tiene una modificación pendiente \
                        Por los momentos no se enviarán solicitudes de modificación.".format(placa)
        return False

    db.modificacion_vehiculo.insert(
        mvh_id_vehiculo=id_vh,
        mvh_marca=marca,
        mvh_modelo=modelo,
        mvh_ano=ano,
        mvh_serial_motor=serial_motor,
        mvh_serial_carroceria=serial_carroceria,
        mvh_serial_chasis=serial_chasis,
        mvh_placa=placa,
        mvh_intt=intt,
        mvh_observaciones=observaciones,
        mvh_lugar_pernocta=lugar_pernocta,
        mvh_color=color,
        mvh_clase=clase,
        mvh_uso=uso,
        mvh_dependencia=dependencia,
        mvh_servicio=servicio,
        mvh_tara=tara,
        mvh_tara_md=tara_md,
        mvh_nro_puestos=nro_puestos,
        mvh_nro_ejes=nro_ejes,
        mvh_capacidad_carga=capacidad_carga,
        mvh_propietario=propietario,
        mvh_responsable=responsable,
        mvh_telf_responsable=telf_responsable,
        mvh_custodio=custodio,
        mvh_telf_custodio=telf_custodio,
        mvh_sudebip_localizacion=sudebip_localizacion,
        mvh_sudebip_codigo_localizacion=sudebip_codigo_localizacion,
        mvh_sudebip_categoria=sudebip_categoria,
        mvh_sudebip_subcategoria=sudebip_subcategoria,
        mvh_sudebip_categoria_especifica=sudebip_categoria_especifica,
        mvh_fecha_adquisicion=fecha_adquisicion,
        mvh_nro_adquisicion=nro_adquisicion,
        mvh_origen=origen,
        mvh_proveedor=proveedor,
        mvh_proveedor_rif=proveedor_rif,
        mvh_num=num,
        mvh_tipo=tipo,
        mvh_clasificacion=clasificacion,
        mvh_modifica_ficha=user,
        mvh_rines=rines,
        mvh_capacidad_carga_md=capacidad_carga_md,
        mvh_ubicacion_custodio=ubicacion_custodio,
        mvh_extension_custodio=extension_custodio,
        mvh_extension_responsable=extension_responsable,
        mvh_donante=donante,
        mvh_contacto_donante=contacto_donante,
        mvh_motivo=motivo,
        mvh_oculto=oculto
    )

    db.bitacora_general.insert(
        f_accion="[inventarios] Añadida solicitud de modificación del vehiculo de placa {}".format(placa)
    )
    response.flash = "Se ha realizado exitosamente la solicitud de modificación del vehiculo de placa %s." % placa 
    return True


# Dado el id de una depencia y conociendo si es un espacio fisico o una dependencia
# comun, determina si el usuario tiene privilegios suficientes para obtener informacion
# de esta
def __acceso_permitido(user, dep_id, es_espacio, es_direccion=False):
    """
    Args:
        * user_id (str): id del usuario en la tabla t_Personal (diferente de auth.user.id)
        * dep_id (str): id de la dependencia a la cual pertenece el recurso que se
            desea acceder
        * es_espacio (str): 'True' si el usuario viene de seleccionar un espacio
            fisico
    """
    # Valor a retornar que determina si el usuario tiene o no acceso al recurso
    permitido = False

    # dep_actual es un apuntador que permitira recorrer la jerarquia de dependencias
    # desde dep_id hasta usuario_dep. Si dep_actual no encuentra usuario_dep
    # entonces se esta tratando de acceder a una dependencia sin permisos suficientes
    dep_actual = dep_id

    # Si el usuario es tecnico se busca en la tabla de es_encargado si el usuario
    # es encargado del espacio con id dep_id
    if auth.has_membership("PERSONAL INTERNO") or auth.has_membership("TÉCNICO"):
        encargado = db(db.es_encargado.espacio_fisico == dep_id).select().first()
        if encargado:
            permitido = encargado.tecnico == user.id

    else:
        # Dependencia a la que pertenece el usuario o que tiene a cargo
        usuario_dep = user.f_dependencia

        # Buscando todas las dependencias para conocer la lista de adyacencias con
        # la jerarquia de la ULAB
        dependencias = db(db.dependencias.id > 0).select(
                                db.dependencias.nombre,
                                db.dependencias.id,
                                db.dependencias.unidad_de_adscripcion)

        # Creando lista de adyacencias
        lista_adyacencias = {dep.id: dep.unidad_de_adscripcion for dep in dependencias}

        # Buscando el id de la direccion para saber si ya se llego a la raiz
        direccion_id = __find_dep_id('DIRECCIÓN')

        # Si dep_id es un espacio fisico, se sube un nivel en la jerarquia (hasta
        # las secciones) ya que los espacios fisicos no aparecen en la lista de
        # adyacencias pero si las secciones a las que pertenecen
        if es_espacio == "True" and not es_direccion:
            dep_actual = db(db.espacios_fisicos.id == dep_id).select().first().dependencia

        while dep_actual is not None:

            # Si en el camino hacia la raiz se encontro la dependencia a la que
            # pertenece el usuario, entonces si hay privilegios suficientes
            if dep_actual == usuario_dep:
                permitido = True
                break
            # Si ya se llego a la raiz, terminar el while
            if dep_actual == direccion_id:
                break
            else:
                dep_actual = lista_adyacencias[dep_actual]

    return permitido

# Retorna un string con la descripcion de un registro de la bitacora de acuerdo
# a si es un ingreso (sompra, suministro almacen u otorgado por otra seccion)
# o un egreso (docencia, invenstigacion o extension)
def __get_descripcion(registro):
    descripcion = ""

    if registro.f_concepto[0] == "Ingreso":
        # Si es un ingreso por compra, se muestra el
        # Compra a "Proveedor" según Factura No. "No. Factura" de fecha "Fecha de compra"
        if registro.f_tipo_ingreso[0] == "Compra":
            compra = db(db.t_Compra.id == registro.f_compra).select()[0]
           
            # Datos de la compra
            proveedor = compra.f_institucion
            nro_factura = compra.f_nro_factura
            fecha_compra = compra.f_fecha

            fecha = fecha_compra

            descripcion = "Compra a \"{0}\" según Factura No. \"{1}\" con fecha"\
                         " \"{2}\"".format(proveedor, nro_factura, fecha)

        # Si es un ingreso por almacen
        # Suministro por el almacén del Laboratorio "X"
        elif registro.f_tipo_ingreso[0] == "Almacén":
            almacen = db(db.espacios_fisicos.id == registro.f_almacen).select()[0]
            dep_id = almacen.dependencia
            dep = db(db.dependencias.id == dep_id).select()[0]

            # Asumiendo que siempre habra un laboratorio sobre la seccion a la que
            descripcion = "Suministrado por el almacén de la dependencia "\
                          "\"{0}\"".format(dep.nombre)

        elif registro.f_tipo_ingreso[0] == "Solicitud":
            # Respuesta a la solicitud en la que se otorgo la sustancia
            respuesta = db(db.t_Respuesta.id == registro.f_respuesta_solicitud
                          ).select()[0]

            # Espacio desde el que se acepto proveer la sustancia
            espacio = db(db.espacios_fisicos.id == respuesta.f_espacio).select()[0]

            # Seccion a la que pertenece ese espacio
            seccion = db(db.dependencias.id == espacio.dependencia).select()[0]

            # Laboratorio al que pertenece esa seccion
            lab = db(db.dependencias.id == seccion.unidad_de_adscripcion).select()[0]

            descripcion = "Otorgado por la Sección \"{0}\" del \"{1}\" "\
                          "en calidad de \"{2}\"".format(seccion.nombre,
                          lab.nombre, respuesta.f_calidad[0])
        elif registro.f_tipo_ingreso[0] == "Ingreso inicial":
            descripcion = "Ingreso inicial de la sustancia al inventario"

    else:
        # Si es un consumo por Docencia
        if registro.f_tipo_egreso[0] == "Docencia":
            servicio = db(db.servicios.id == registro.f_servicio).select()[0]

            nombre = servicio.nombre

            descripcion = "Ejecución de la práctica \"{0}\"".format(nombre)
        elif registro.f_tipo_egreso[0] == "Investigación":
            servicio = db(db.servicios.id == registro.f_servicio).select()[0]

            nombre = servicio.nombre

            descripcion = "Ejecución del proyecto de investigación \"{0}\"".format(nombre)
           
        elif registro.f_tipo_egreso[0] == "Extensión":
            servicio = db(db.servicios.id == registro.f_servicio).select()[0]

            nombre = servicio.nombre

            descripcion = "Ejecución del servicio \"{0}\"".format(nombre)
           
        # Cuando es un egreso en respuesta a una solicitud
        else:
           
            # Respuesta a la solicitud en la que se solicito la sustancia
            respuesta = db(db.t_Respuesta.id == registro.f_respuesta_solicitud
                          ).select()[0]

            # Solicitud que hizo que por aceptarla se sacara material
            solicitud = db(db.t_Solicitud_smydp.id == respuesta.f_solicitud
                          ).select()[0]

            # Espacio desde el que se solicito la sustancia
            espacio = db(db.espacios_fisicos.id == solicitud.f_espacio).select()[0]

            # Seccion a la que pertenece ese espacio
            seccion = db(db.dependencias.id == espacio.dependencia).select()[0]

            # Laboratorio al que pertenece esa seccion
            lab = db(db.dependencias.id == seccion.unidad_de_adscripcion).select()[0]

            descripcion = "Otorgado a la Sección \"{0}\" del \"{1}\" "\
                          "en calidad de \"{2}\"".format(seccion.nombre,
                          lab.nombre, respuesta.f_calidad[0])
       

    return descripcion

def __agregar_modificar_bm(nombre, no_bien, no_placa, marca, modelo, serial,
                descripcion, material, color, calibrar, fecha_calibracion,
                unidad_med, ancho, largo, alto, diametro, movilidad, uso,
                estatus, nombre_cat, subcategoria, cod_loc, localizacion, descripcion_mod, user):
    # Si ya existe el BM en el inventario
    if (db(db.modificacion_bien_mueble.mbn_num == no_bien).select()):
        bm = db(db.bien_mueble.bm_num == no_bien).select()[0] #Se busca de la tabla de bm para tener el nombre original
        response.flash = "El  \"{0}\" tiene una modificación pendiente \
                        Por los momentos no se enviarán solicitudes de modificación.".format(nombre)
        return False
    # Si no, se agrega al inventario del espacio fisico la nueva sustancia

    if not unidad_med:
        ancho = None
        largo = None
        alto = None
        diametro = None

    inv_id = db.modificacion_bien_mueble.insert(
            mbn_nombre = nombre,
            mbn_num = no_bien,
            mbn_placa = no_placa,
            mbn_marca = marca,
            mbn_modelo = modelo,
            mbn_serial = serial,
            mbn_descripcion = descripcion,
            mbn_material = material,
            mbn_color = color,
            mbn_calibrar =  calibrar,
            mbn_fecha_calibracion = fecha_calibracion,
            mbn_unidad = unidad_med,
            mbn_ancho = ancho,
            mbn_largo = largo,
            mbn_alto = alto,
            mbn_diametro = diametro,
            mbn_movilidad = movilidad,
            mbn_uso = uso,
            mbn_estatus = estatus,
            mbn_categoria = nombre_cat,
            mbn_subcategoria = subcategoria,
            mbn_codigo_localizacion = cod_loc,
            mbn_localizacion = localizacion,
            mbn_desc =  descripcion_mod,
            mbn_modifica_ficha = user
        )
    db.bitacora_general.insert(
        f_accion="[inventarios] Añadida solicitud de modificación del bien mueble número {}".format(no_bien)
    )
    response.flash = "Se ha realizado exitosamente la solicitud de modificación del bien mueble " + str(nombre)
    #return redirect(URL(args=request.args, vars=request.get_vars, host=True))
    return True


# < -------- Final Funciones privadas de SMDYP ------------>

# < ------- Vistas del modulo de inventario -------->
def index():
    validaciones_pendientes = validaciones()
    prestamos_pendientes = prestamos()['cant_prestamos']
    numero_validaciones = 0
    if (
        len(validaciones_pendientes['inventario'][0]) != 0 or \
        len(validaciones_pendientes['inventario'][1]) != 0 or \
        len(validaciones_pendientes['inventario'][2]) != 0 or \
        len(validaciones_pendientes['inventario_eliminar'][0]) != 0 or \
        len(validaciones_pendientes['inventario_eliminar'][1]) != 0 or \
        len(validaciones_pendientes['inventario_eliminar'][2]) != 0 or \
        len(validaciones_pendientes['inventario_eliminar_vehiculos']) != 0 or \
        len(validaciones_pendientes['inventario_vehiculos']) != 0
    ):
        numero_validaciones = len(validaciones_pendientes['inventario'][0]) + \
        len(validaciones_pendientes['inventario'][1]) + \
        len(validaciones_pendientes['inventario'][2]) + \
        len(validaciones_pendientes['inventario_eliminar'][0]) + \
        len(validaciones_pendientes['inventario_eliminar'][1]) + \
        len(validaciones_pendientes['inventario_eliminar'][2]) + \
        len(validaciones_pendientes['inventario_vehiculos']) + \
        len(validaciones_pendientes['inventario_eliminar_vehiculos'])

    return dict(
        numero_validaciones=numero_validaciones,
        numero_prestamos=prestamos_pendientes
    )

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def vehiculos():
# Inicializando listas de espacios fisicos y dependencias
    
    # PENDIENTE: Cableando la variable de es_espacio 
    if not request.vars.acceso_direccion:
        request.vars.es_espacio = 'False'
        request.vars.acceso_direccion = False

    # OJO: Espacios debe ser [] siempre que no se este visitando un espacio fisico
    espacios = []
    dependencias = []
    dep_nombre = ""
    dep_padre_id = ""
    dep_padre_nombre = ""

    # Lista de BM en el inventario de un espacio fisico o que componen
    # el inventario agregado de una dependencia
    inventario = []

    # Obtenemos otros datos de SUDEBIP
    cod_localizacion = {
        'Sartenejas': 150301,
        'Litoral': 240107
    }

    localizacion = {
        'Sartenejas': 'Edo Miranda, Municipio Baruta, Parroquia Baruta',
        'Litoral': 'Edo Vargas, Municipio Vargas, Parroquia Macuto'
    }

    # Elementos que deben ser mostrados como una lista en el modal
    # de agregar vehículo
    uso = []
    nombre_cat = []
    nombre_espaciof = []
    unidad_adscripcion = []
    unidad_cap = []

    # Esta variable es enviada a la vista para que cuando el usuario seleccione
    # un espacio fisico, se pase por GET es_espacio = "True". No quiere decir
    # que la dependencia seleccionada sea un espacio, sino que la siguiente
    # dependencia visitada sera un espacio fisico
    es_espacio = False

    # Permite saber si actualmente se esta visitando un espacio fisico (True)
    # o una dependencia (False)
    espacio_visitado = False

    # Indica si se debe seguir mostrando la flecha para seguir retrocediendo
    retroceder = True

    es_tecnico = auth.has_membership("PERSONAL INTERNO") or auth.has_membership("TÉCNICO")
    direccion_id = __find_dep_id('DIRECCIÓN')

    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    user_dep_id = user.f_dependencia

    # Si se esta agregando un nuevo vehiculo, se registra en la DB
    if request.vars.modelo: # Verifico si me pasan como argumento el modelo del vehículo.
        try:
            id_dep_real = int(request.vars.dependencia)
        except:
            id_dep_real = user_dep_id

        dependencia_escogida = db(db.dependencias.id == id_dep_real).select()[0]

        if dependencia_escogida.id_sede == 1:
            sede_verbosa = "Sartenejas"
        else:
            sede_verbosa = "Litoral"

        __agregar_vh(
            num=request.vars.num,
            marca=request.vars.marca if request.vars.marca != "Otro" else "Otro: " + request.vars.marca2,
            modelo=request.vars.modelo,
            ano=int(request.vars.ano),
            serial_motor=request.vars.serialM,
            serial_carroceria=request.vars.serialC,
            serial_chasis=request.vars.serialCh,
            placa=request.vars.placa,
            intt=request.vars.intt,
            observaciones=request.vars.observaciones,
            lugar_pernocta=request.vars.pernocta,
            color=request.vars.color,
            clase=request.vars.clase,
            tipo=request.vars.tipo if request.vars.tipo != "Otros aparatos para circular" else "Otros aparatos para circular: " + request.vars.tipo2,
            clasificacion=request.vars.clasificacion if request.vars.clasificacion != "Emergencia" else "Emergencia: " + requesr.vars.clasificacion2,
            uso=request.vars.uso,
            servicio=request.vars.servicio,
            tara=float(request.vars.tara),
            tara_md=request.vars.tara_md,
            nro_puestos=int(request.vars.nro_puestos),
            nro_ejes=0 if not request.vars.nro_ejes else int(request.vars.nro_ejes),
            capacidad_carga=float(request.vars.capacidad),
            capacidad_carga_md=request.vars.capacidad_carga_md,
            rines=request.vars.rines if request.vars.rines != "Otro" else "Otro: " + request.vars.rines2,
            ubicacion_custodio=request.vars.ubicacion_custodio,
            propietario=request.vars.propietario,
            responsable=int(request.vars.responsable),
            telf_responsable=request.vars.telf_responsable,
            extension_responsable=request.vars.extension_responsable,
            custodio=int(request.vars.custodio),
            telf_custodio=request.vars.telf_custodio,
            extension_custodio=request.vars.extension_custodio,
            sudebip_localizacion=localizacion[sede_verbosa],
            sudebip_codigo_localizacion=cod_localizacion[sede_verbosa],
            sudebip_categoria="15000-0000 - Equipos de transporte, tracción y elevación",
            sudebip_subcategoria=request.vars.sudebip_subcategoria,
            sudebip_categoria_especifica=request.vars.sudebip_categoria_especifica,
            fecha_adquisicion=request.vars.fecha_factura if request.vars.origen == "Compra" else request.vars.fecha_oficio,
            origen=request.vars.origen,
            nro_adquisicion=request.vars.nro_factura if request.vars.origen == "Compra" else request.vars.nro_oficio,
            proveedor=request.vars.proveedor,
            proveedor_rif=request.vars.proveedor_rif,
            donante=request.vars.donante,
            contacto_donante=request.vars.contacto_donante,
            dependencia=id_dep_real,
            oculto=0
        )
        session.flash = "El vehículo de placa %s ha sido agregado." % request.vars.placa

    if auth.has_membership("PERSONAL INTERNO") or auth.has_membership("TÉCNICO"):
        # Si el tecnico ha seleccionado un espacio fisico
        if request.vars.dependencia:
            if request.vars.es_espacio == "True":
                # Evaluando la correctitud de los parametros del GET
                if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('vehiculos'))

                # Determinando si el usuario tiene privilegios suficientes para
                # consultar la dependencia en request.vars.dependencia
                if not __acceso_permitido(user,
                                          int(request.vars.dependencia),
                                          request.vars.es_espacio,
                                          request.vars.acceso_direccion):
                    redirect(URL('vehiculos'))

                try: 
                    # Se muestra el inventario del espacio
                    espacio_id = request.vars.dependencia
                    espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                    dep_nombre = espacio.codigo
                    dep_padre_id = espacio.dependencia

                    # Busca el inventario del espacio
                    inventario = __get_vh_dep(dep_padre_id)
                except IndexError:
                    dep_nombre = "DIRECCIÓN"
                    dep_padre_id = 1
                    inventario = __get_vh_dep(1)

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_id = espacio.dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre
                # Guardando la unidad de adscripcion
                dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                    ).select().first().unidad_de_adscripcion

                espacio_visitado = True

            else:
                # Espacios a cargo del usuario user_id que pertenecen a la seccion
                # en request.vars.dependencia
                espacios = [row.espacios_fisicos for row in db(
                    (db.es_encargado.espacio_fisico == db.espacios_fisicos.id) &
                    (db.espacios_fisicos.dependencia == int(request.vars.dependencia)) &
                    (db.es_encargado.tecnico == user_id)).select()]

                espacios_ids = [e.id for e in espacios]

                dep_id = int(request.vars.dependencia)
                dep_nombre = db(db.dependencias.id == dep_id).select()[0].nombre

                dep_padre_nombre = "Secciones"

                # Se muestran los vehiculos de la dependencia que tiene a cargo el usuario en la
                # seccion actual
                inventario = __get_vh_dep(dep_id)

                es_espacio = True

        # Si el tecnico o jefe no ha seleccionado un espacio sino que acaba de
        # entrar a la opcion de vehiculos
        else:
            # Se buscan las secciones a las que pertenecen los espacios que
            # tiene a cargo el usuario
            espacios_a_cargo = db(
                (db.es_encargado.tecnico == user_id) &
                (db.espacios_fisicos.id == db.es_encargado.espacio_fisico)
                                 ).select()

            secciones_ids = {e.espacios_fisicos.dependencia for e in espacios_a_cargo}

            dependencias = map(lambda x: db(db.dependencias.id == x).select(db.dependencias.ALL, orderby=db.dependencias.id)[0],
                               secciones_ids)

            dep_nombre = "Secciones"

            espacios_ids = [e.espacios_fisicos.id for e in espacios_a_cargo]

            inventario = __get_vh_dep(user_dep_id)

    elif auth.has_membership("JEFE DE SECCIÓN") or auth.has_membership("COORDINADOR"):
        # Si el jefe de seccion ha seleccionado un espacio fisico
        if request.vars.es_espacio == 'True':
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not request.vars.dependencia == user_dep_id and not __acceso_permitido(user,
                                int(request.vars.dependencia),
                                    request.vars.es_espacio,
                                    request.vars.acceso_direccion):
                redirect(URL('vehiculos'))

            # Evaluando la correctitud de los parametros del GET
            if not request.vars.dependencia == user_dep_id and not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('vehiculos'))

            try: 
                # Se muestra el inventario del espacio
                espacio_id = request.vars.dependencia
                espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                dep_nombre = espacio.codigo
                dep_padre_id = espacio.dependencia

                # Busca el inventario del espacio
                inventario = __get_vh_dep(dep_padre_id)
            except IndexError:
                dep_nombre = "DIRECCIÓN"
                dep_padre_id = 1
                inventario = __get_vh_dep(1)

            # Guardando el ID y nombre de la dependencia padre para el link
            # de navegacion de retorno
            dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                ).select().first().nombre
            # Guardando la unidad de adscripcion
            dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                ).select().first().unidad_de_adscripcion

            espacio_visitado = True

        # Si el jefe de seccion no ha seleccionado un espacio sino que acaba de
        # regresar a la vista inicial de inventarios
        elif request.vars.es_espacio == 'False':
            espacios = list(db(
                              db.espacios_fisicos.dependencia == user_dep_id
                              ).select(db.espacios_fisicos.ALL))
            dep_nombre = db(db.dependencias.id == user_dep_id
                           ).select().first().nombre

            es_espacio = True
        # Si el jefe de seccion no ha seleccionado un espacio sino que acaba de
        # entrar a la vista inicial de inventarios
        else:
            espacios = list(db(
                              db.espacios_fisicos.dependencia == user_dep_id
                              ).select(db.espacios_fisicos.ALL))
            dep_nombre = db(db.dependencias.id == user_dep_id
                           ).select().first().nombre

            es_espacio = True

            # Se muestra como inventario el egregado de los inventarios que
            # pertenecen a la seccion del jefe
            inventario = __get_vh_dep(user_dep_id)

    # Si el usuario no es tecnico, para la base de datos es indiferente su ROL
    # pues la jerarquia de dependencias esta almacenada en la misma tabla
    # con una lista de adyacencias
    else:
        # Si el usuario ha seleccionado una dependencia o un espacio fisico
        if request.vars.dependencia:

            # Evaluando la correctitud de los parametros del GET

            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user,
                                int(request.vars.dependencia),
                                    request.vars.es_espacio,
                                    request.vars.acceso_direccion):
                redirect(URL('vehiculos'))

            if request.vars.es_espacio == "True":

                if not request.vars.acceso_direccion and not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos)  and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('vehiculos'))

                try:
                    # Se muestra el inventario del espacio
                    espacio_id = request.vars.dependencia
                    espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                    dep_nombre = espacio.codigo
                    dep_padre_id = espacio.dependencia

                    # Busca el inventario del espacio
                    inventario = __get_inventario_espacio(espacio_id)
                except IndexError:
                    dep_nombre = "DIRECCIÓN"
                    dep_padre_id = 1
                    inventario = __get_vh_dep(1)

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre
                # Guardando la unidad de adscripcion
                dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                    ).select().first().unidad_de_adscripcion

                espacio_visitado = True


            else:
                if not (__is_valid_id(request.vars.dependencia, db.dependencias)  and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('vehiculos'))

                # Se muestran las dependencias que componen a esta dependencia padre
                # y se lista el inventario agregado
                dep_id = request.vars.dependencia
                dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre
                dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                      ).select(db.dependencias.ALL, orderby=db.dependencias.id))
                # Si la lista de dependencias es vacia, entonces la dependencia no
                # tiene otras dependencias por debajo (podria tener espacios fisicos
                # o estar vacia)
                if dependencias:
                    # Buscando espacios fisicos que apunten a la dependencia escogida
                    espacios = list(db(db.espacios_fisicos.dependencia == dep_id
                                      ).select(db.espacios_fisicos.ALL))
                    es_espacio = True

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_id = db(db.dependencias.id == request.vars.dependencia
                                 ).select().first().unidad_de_adscripcion
                # Si dep_padre_id es None, se ha llegado al tope de la jerarquia
                # y no hay un padre de este nodo
                if dep_padre_id:
                    dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                         ).select().first().nombre
                # Se muestra como inventario el egregado de los inventarios que
                # pertenecen a la dependencia del usuario
                inventario = __get_vh_dep(dep_id)

        else:
            # Dependencia a la que pertenece el usuario o que tiene a cargo
            dep_id = user.f_dependencia
            dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre

            # Se muestran las dependencias que componen a la dependencia que
            # tiene a cargo el usuario y el inventario agregado de esta
            dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                  ).select(db.dependencias.ALL, orderby=db.dependencias.id))

            # Se muestra como inventario el egregado de los inventarios que
            # pertenecen a la dependencia del usuario
            inventario = __get_vh_dep(dep_id)

    acceso_direccion = False

    # PENDIENTE: Super refactoizar
    if request.vars.acceso_direccion:
        # Si accedemos a la Dirección cableada, entonces
        # mostramos solo los vehículos de la Dirección
        acceso_direccion = True
        inventario = __get_vh_dep(1)
        dep_padre_id = 1
        dep_padre_nombre = "ULAB"
        dep_nombre = "DIRECCIÓN"
    elif request.vars.dependencia:
        # Si accedemos a cualquier dependencia, entonces mostramos
        # los vehículos de esa dependencia
        inventario = __get_vh_dep(int(request.vars.dependencia))
    else:
        # En la vista general, nos traemos todos los vehículos que
        # no hayan sido eliminados
        inventario = db(db.vehiculo.vh_eliminar != 1).select()

    # Devolvemos las categorias de vehiculos
    dict_categorias = __obtener_categorias()
    dict_clasificaciones = __obtener_clasificaciones()

    if request.vars.dependencia:
        id_actual = int(request.vars.dependencia)
    elif dep_padre_id:
        id_actual = int(dep_padre_id)
    else:
        id_actual = 1

    sede_id = db(db.dependencias.id == id_actual).select()[0].id_sede
    if request.vars.dependencia:
        dep_id = int(request.vars.dependencia)
    else:
        dep_id = 1

    # Ocultamos inventario acorde a lo requerido
    inventario_visible = []
    id_usuario = auth.user.id
    for vh in inventario:
        if __puede_ver_vehiculo(id_usuario, vh['id']):
            inventario_visible.append(vh)

    try:
        dep_id = db(db.dependencias.nombre == dep_nombre).select().first().id
    except:
        pass

    return dict(dep_nombre=dep_nombre,
                dependencias=dependencias,
                espacios=espacios,
                es_espacio=es_espacio,
                espacio_visitado=espacio_visitado,
                dep_padre_id=dep_padre_id,
                dep_padre_nombre=dep_padre_nombre,
                direccion_id=direccion_id,
                es_tecnico=es_tecnico,
                inventario=inventario_visible,
                retroceder=retroceder,
                categorias=dict_categorias,
                clasificaciones=dict_clasificaciones,
                cod_localizacion=cod_localizacion,
                localizacion=localizacion,
                sede_id=sede_id,
                dep_id=dep_id,
                acceso_direccion=acceso_direccion
               )

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles_mod_herramientas():
    #Recuperamos el espacio
    espacio = request.vars['espacio']
    #El nombre de la herramienta
    name = request.vars['nombreHer']
    #La ubicacion interna
    ubicacion = request.vars['ubicacion']

    # El usuario que está editando
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    espacio_nombre = db(db.espacios_fisicos.id == espacio).select().first().codigo
    # Busco la herramienta
    bien = db((db.modificacion_herramienta.mhr_nombre == name) & (db.modificacion_herramienta.mhr_espacio_fisico==espacio) & (db.modificacion_herramienta.mhr_ubicacion==ubicacion)).select()[0]

    #Inicializo variables
    material_pred = []
    unidad_med = []
    presentacion=[]

    # Si se modifica
    if request.vars.si:
        db((db.herramienta.hr_nombre == name) & (db.herramienta.hr_espacio_fisico==espacio) & (db.herramienta.hr_ubicacion==ubicacion)).update(
            hr_nombre = bien['mhr_nombre'],
            hr_num= bien['mhr_num'],  
            hr_marca = bien['mhr_marca'],
            hr_modelo = bien['mhr_modelo'],
            hr_serial = bien['mhr_serial'],
            hr_presentacion = bien['mhr_presentacion'],
            hr_numpiezas= bien['mhr_numpiezas'],
            hr_contenido = bien['mhr_contenido'],
            hr_descripcion = bien['mhr_descripcion'],
            hr_material = bien['mhr_material'],
            hr_unidad = bien['mhr_unidad'],
            hr_ancho = bien['mhr_ancho'],
            hr_largo = bien['mhr_largo'],
            hr_alto = bien['mhr_alto'],
            hr_diametro = bien['mhr_diametro'],
            hr_espacio_fisico = bien['mhr_espacio_fisico'],
            hr_ubicacion = bien['mhr_ubicacion'],
            hr_observacion= bien['mhr_observacion'],
            hr_unidad_de_adscripcion = bien['mhr_unidad_de_adscripcion'],
            hr_depedencia = bien['mhr_depedencia']
        )
        db.bitacora_general.insert(
        f_accion="[inventarios] Modificada la información de la herramienta {} del espacio físico {}".format( bien['mhr_nombre'], espacio_nombre)
        )
        db((db.modificacion_herramienta.mhr_nombre == name) & (db.modificacion_herramienta.mhr_espacio_fisico==espacio) & (db.modificacion_herramienta.mhr_ubicacion==ubicacion)).delete()
        session.flash = "La información de la herramienta ha sido actualizada"
        redirect(URL('validaciones'))

    # Si no se modifica
    if request.vars.no:
        db.bitacora_general.insert(
        f_accion="[inventarios] Rechazada modificación de la información de la herramienta {} del espacio físico {}".format( bien['mhr_nombre'], espacio_nombre)
        )
        db((db.modificacion_herramienta.mhr_nombre == name) & (db.modificacion_herramienta.mhr_espacio_fisico==espacio) & (db.modificacion_herramienta.mhr_ubicacion==ubicacion)).delete()
        session.flash = "La información de la herramienta no ha sido modificada"
        redirect(URL('validaciones'))

    material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
    unidad_med = ['cm', 'm']
    presentacion=["Unidad", "Conjunto"]
    if bien['mhr_presentacion'] == "Unidad":
        caracteristicas_list = [ 'Número de Bien Nacional:', 'Marca:', 'Modelo:', 'Serial:', 'Presentación:',
        'Material predominante:', 'Ubicación interna:']
        caracteristicas_dict = {
            'Número de Bien Nacional:': bien['mhr_num'],
            'Marca:': bien['mhr_marca'],
            'Modelo:': bien['mhr_modelo'],
            'Serial:': bien['mhr_serial'],
            'Presentación:': bien['mhr_presentacion'],
            'Material predominante:': bien['mhr_material'],
            'Ubicación interna:' : bien['mhr_ubicacion']
        }
    else:
        caracteristicas_list = [ 'Número de Bien Nacional:', 'Marca:', 'Modelo:', 'Serial:', 'Presentación:',
        'Número de Piezas:', 'Contenido:', 'Descripción:', 'Material predominante:', 'Ubicación interna:']
        caracteristicas_dict = {
            'Número de Bien Nacional::': bien['mhr_num'],
            'Marca:': bien['mhr_marca'],
            'Modelo:': bien['mhr_modelo'],
            'Serial:': bien['mhr_serial'],
            'Presentación:': bien['mhr_presentacion'],
            'Número de Piezas:': bien['mhr_numpiezas'],
            'Contenido:': bien['mhr_contenido'],
            'Descripción:': bien['mhr_descripcion'],
            'Material predominante:': bien['mhr_material'],
            'Ubicación interna:' : bien['mhr_ubicacion']
        }

    if not caracteristicas_dict['Marca:']:
        del caracteristicas_dict['Marca:']
        caracteristicas_list.remove('Marca:')

    if not caracteristicas_dict['Modelo:']:
        del caracteristicas_dict['Modelo:']
        caracteristicas_list.remove('Modelo:')

    if not caracteristicas_dict['Serial:']:
        del caracteristicas_dict['Serial:']
        caracteristicas_list.remove('Serial:')

    return dict(bien=bien,
                material_pred=material_pred,
                caracteristicas_list=caracteristicas_list,
                caracteristicas_dict=caracteristicas_dict,
                unidad_med=unidad_med,
                presentacion=presentacion
                )

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles_mod_mat():
    #Recuperamos el espacio
    espacio = request.vars['espacio']
    #El nombre del material/consumible
    name = request.vars['nombreMat']
    espacio_nombre = db(db.espacios_fisicos.id == espacio).select().first().codigo
    # El usuario que está editando
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id

    # Busco el material/consumible que ha sido modificado
    bien = db( (db.modificacion_sin_bn.msb_espacio == espacio) & (db.modificacion_sin_bn.msb_nombre == name) ).select()[0]
    bien_original = db( (db.sin_bn.sb_espacio == espacio) & (db.sin_bn.sb_nombre == name) ).select()[0]

    #Si se edita
    if request.vars.si:
        db( (db.sin_bn.sb_espacio == espacio) & (db.sin_bn.sb_nombre == name) ).update(
            sb_cantidad = bien['msb_cantidad'],
            sb_nombre = bien['msb_nombre'],  
            sb_marca = bien['msb_marca'],
            sb_modelo = bien['msb_modelo'],
            sb_descripcion = bien['msb_descripcion'],
            sb_material = bien['msb_material'],
            sb_material_sec = bien['msb_material_sec'],
            sb_calibrar =  bien['msb_calibrar'],
            sb_unidad = bien['msb_unidad'],
            sb_ancho = bien['msb_ancho'],
            sb_largo = bien['msb_largo'],
            sb_alto = bien['msb_alto'],
            sb_diametro = bien['msb_diametro'],
            sb_espacio = bien['msb_espacio'],
            sb_presentacion = bien['msb_presentacion'],
            sb_unidades = bien['msb_unidades'],
            sb_total = bien['msb_total'],
            sb_aforado = bien['msb_aforado'],
            sb_ubicacion = bien['msb_ubicacion'],
            sb_capacidad = bien['msb_capacidad'],
            sb_unidad_dim = bien['msb_unidad_dim']
        )
        db.bitacora_general.insert(
            f_accion="[inventarios] Modificada la información del material de laboratorio {} del espacio físico {}".format( bien['msb_nombre'], espacio_nombre)
        )
        db( (db.modificacion_sin_bn.msb_espacio == espacio) & (db.modificacion_sin_bn.msb_nombre == name) ).delete()
        session.flash = "La información del material de laboratorio ha sido modificada"
        redirect(URL('validaciones'))
    if request.vars.no:
        db.bitacora_general.insert(
            f_accion="[inventarios] Rechazada modificación de la información del material de laboratorio {} del espacio físico {}".format( bien['msb_nombre'], espacio_nombre)
        )
        db( (db.modificacion_sin_bn.msb_espacio == espacio) & (db.modificacion_sin_bn.msb_nombre == name) ).delete()
        session.flash = "La información del material de laboratorio no ha sido modificada"
        redirect(URL('validaciones'))

    if bien_original['sb_clasificacion'] == "Material de Laboratorio":
        caracteristicas_list = ['Cantidad:', 'Marca:', 'Modelo:', 'Aforado:', 'Requiere calibración:',
        'Capacidad:', 'Unidad de medida:', 'Material predominante:', 'Material secundario:', 'Descripción:', 'Tipo:', 'Ubicación interna:']
        caracteristicas_dict = {
            'Cantidad:': bien['msb_cantidad'],
            'Marca:': bien['msb_marca'],
            'Modelo:': bien['msb_modelo'],
            'Descripción:': bien['msb_descripcion'],
            'Material predominante:': bien['msb_material'],
            'Material secundario:': bien['msb_material_sec'],
            'Aforado:': bien['msb_aforado'],
            'Tipo:': bien_original['sb_clasificacion'],
            'Requiere calibración:': bien['msb_calibrar'],
            'Ubicación interna:' : bien['msb_ubicacion'],
            'Capacidad:': bien['msb_capacidad'],
            'Unidad de medida:' : bien['msb_unidad'],
        }
    else:
        caracteristicas_list = ["Marca:", "Modelo:", "Presentación:", "Unidades por presentación:", "Cantidad:",
        "Total(U.):", "Descripción:", "Ubicación interna:"]
        caracteristicas_dict = {
            'Presentación:': bien['msb_presentacion'],
            'Unidades por presentación:': bien['msb_unidades'],
            'Cantidad:': bien['msb_cantidad'],
            'Total(U.):': bien['msb_total'],
            'Marca:': bien['msb_marca'],
            'Modelo:': bien['msb_modelo'],
            'Descripción:': bien['msb_descripcion'],
            'Ubicación interna:' : bien['msb_ubicacion'],
            'Tipo:': bien_original['sb_clasificacion']
        }
    return dict(bien=bien,
                bien_original=bien_original,
                caracteristicas_list=caracteristicas_list,
                caracteristicas_dict=caracteristicas_dict
                )

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles_mod():
    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    bm = request.vars['bm']
    bien = db(db.modificacion_bien_mueble.mbn_num == bm).select()[0] #bien que sera modificado
    bien_original = db(db.bien_mueble.bm_num == bm).select()[0]

    if request.vars.si:
        db(db.bien_mueble.bm_num == bm).update(
            bm_nombre = bien['mbn_nombre'],
            bm_num = bien['mbn_num'],
            bm_placa = bien['mbn_placa'],
            bm_marca = bien['mbn_marca'],
            bm_modelo = bien['mbn_modelo'],
            bm_serial = bien['mbn_serial'],
            bm_descripcion = bien['mbn_descripcion'],
            bm_material = bien['mbn_material'],
            bm_color = bien['mbn_color'],
            bm_calibrar =  bien['mbn_calibrar'],
            bm_fecha_calibracion = bien['mbn_fecha_calibracion'],
            bm_unidad = bien['mbn_unidad'],
            bm_ancho = bien['mbn_ancho'],
            bm_largo = bien['mbn_largo'],
            bm_alto = bien['mbn_alto'],
            bm_diametro = bien['mbn_diametro'],
            bm_movilidad = bien['mbn_movilidad'],
            bm_uso = bien['mbn_uso'],
            bm_estatus = bien['mbn_estatus'],
            bm_categoria = bien['mbn_categoria'],
            bm_subcategoria = bien['mbn_subcategoria'],
            bm_codigo_localizacion = bien['mbn_codigo_localizacion'],
            bm_localizacion = bien['mbn_localizacion']
        )
        db.bitacora_general.insert(
            f_accion="[inventarios] Modificada la información del bien mueble num {}".format(bien['mbn_num'])
        )       
        db(db.modificacion_bien_mueble.mbn_num == bm).delete()
        session.flash = "La información sobre el bien mueble ha sido modificada"
        redirect(URL('validaciones'))

    if request.vars.no:
        db.bitacora_general.insert(
            f_accion="[inventarios] Rechazada modificación de la información del bien mueble num {}".format( bien['mbn_num'])
        ) 
        db(db.modificacion_bien_mueble.mbn_num == bm).delete()
        session.flash = "la información sobre el bien mueble no ha sido modificada"
        redirect(URL('validaciones'))

    if bien_original['bm_clasificacion']=="Equipo":

        caracteristicas_list = ['Marca:', 'Modelo:', 'Serial:',
        'Material predominante:', 'Color:', 'Movilidad:', 'Uso:', 'Estatus:' 'Descripción:']


        caracteristicas_dict = {
            'Marca:': bien['mbn_marca'],
            'Modelo:': bien['mbn_modelo'],
            'Serial:': bien['mbn_serial'],
            'Descripción:': bien['mbn_descripcion'],
            'Material predominante:': bien['mbn_material'],
            'Color:': bien['mbn_color'],
            'Movilidad:': bien['mbn_movilidad'],
            'Uso:': bien['mbn_uso'],
            'Estatus:': bien['mbn_estatus']
        }
    elif bien_original['bm_clasificacion']=="Mobiliario":

        caracteristicas_list = ['Material predominante:', 'Color:', 'Movilidad:', 'Uso:', 'Estatus:', 'Descripción:']

        caracteristicas_dict = {
            'Descripción:': bien['mbn_descripcion'],
            'Material predominante:': bien['mbn_material'],
            'Color:': bien['mbn_color'],
            'Movilidad:': bien['mbn_movilidad'],
            'Uso:': bien['mbn_uso'],
            'Estatus:': bien['mbn_estatus']
        }

    sudebid_list = ['Localización:', 'Código Localización:', 'Categoría:', 'Subcategoría:']
    sudebid_dict = {
        'Localización:': bien['mbn_localizacion'],
        'Código Localización:': bien['mbn_codigo_localizacion'],
        'Categoría:': bien['mbn_categoria'],
        'Subcategoría:': bien['mbn_subcategoria']
    }

    return dict(bien=bien,
                bien_original=bien_original,
                caracteristicas_list=caracteristicas_list,
                caracteristicas_dict=caracteristicas_dict,
                sudebid_list=sudebid_list,
                sudebid_dict=sudebid_dict)

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles_mod_vehiculo():
    vh_id = request.vars['vh']
    vehiculo = db(db.modificacion_vehiculo.mvh_id_vehiculo == vh_id).select()[0] # vh que sera modificado
    vehiculo_original = db(db.vehiculo.id == vh_id).select()[0]

    cod_localizacion = {
        'Sartenejas': 150301,
        'Litoral': 240107
    }

    localizacion = {
        'Sartenejas': 'Edo Miranda, Municipio Baruta, Parroquia Baruta',
        'Litoral': 'Edo Vargas, Municipio Vargas, Parroquia Macuto'
    }

    mantenimiento = __get_mantenimiento_vh(vehiculo_original['id'])
    prestamos = __get_prestamos_vh(vehiculo_original['id'])

    if request.vars.si:
        db(db.vehiculo.id == vh_id).select().first().update_record(
            vh_num=vehiculo['mvh_num'],
            vh_marca=vehiculo['mvh_marca'],
            vh_modelo=vehiculo['mvh_modelo'],
            vh_ano=vehiculo['mvh_ano'],
            vh_extension_custodio=vehiculo['mvh_extension_custodio'],
            vh_ubicacion_custodio=vehiculo['mvh_ubicacion_custodio'],
            vh_serial_motor=vehiculo['mvh_serial_motor'],
            vh_serial_carroceria=vehiculo['mvh_serial_carroceria'],
            vh_serial_chasis=vehiculo['mvh_serial_chasis'],
            vh_placa=vehiculo['mvh_placa'],
            vh_rines=vehiculo['mvh_rines'],
            vh_capacidad_carga_md=vehiculo['mvh_capacidad_carga_md'],
            vh_intt=vehiculo['mvh_intt'],
            vh_tipo=vehiculo['mvh_tipo'],
            vh_clasificacion=vehiculo['mvh_clasificacion'],
            vh_observaciones=vehiculo['mvh_observaciones'],
            vh_lugar_pernocta=vehiculo['mvh_lugar_pernocta'],
            vh_color=vehiculo['mvh_color'],
            vh_clase=vehiculo['mvh_clase'],
            vh_uso=vehiculo['mvh_uso'],
            vh_servicio=vehiculo['mvh_servicio'],
            vh_tara=vehiculo['mvh_tara'],
            vh_tara_md=vehiculo['mvh_tara_md'],
            vh_nro_puestos=vehiculo['mvh_nro_puestos'],
            vh_nro_ejes=vehiculo['mvh_nro_ejes'],
            vh_capacidad_carga=vehiculo['mvh_capacidad_carga'],
            vh_propietario=vehiculo['mvh_propietario'],
            vh_responsable=vehiculo['mvh_responsable'],
            vh_telf_responsable=vehiculo['mvh_telf_responsable'],
            vh_extension_responsable=vehiculo['mvh_extension_responsable'],
            vh_custodio=vehiculo['mvh_custodio'],
            vh_telf_custodio=vehiculo['mvh_telf_custodio'],
            vh_sudebip_subcategoria=vehiculo['mvh_sudebip_subcategoria'],
            vh_sudebip_categoria_especifica=vehiculo['mvh_sudebip_categoria_especifica'],
            vh_fecha_adquisicion=vehiculo['mvh_fecha_adquisicion'],
            vh_origen=vehiculo['mvh_origen'],
            vh_nro_adquisicion=vehiculo['mvh_nro_adquisicion'],
            vh_proveedor=vehiculo['mvh_proveedor'],
            vh_proveedor_rif=vehiculo['mvh_proveedor_rif'],
            vh_donante=vehiculo['mvh_donante'],
            vh_contacto_donante=vehiculo['mvh_contacto_donante'],
            vh_oculto=vehiculo['mvh_oculto'],
        )

        db.bitacora_general.insert(
            f_accion="[inventarios] Modificada la información del vehículo num {}".format(vehiculo['mvh_num'])
        )
        db(db.modificacion_vehiculo.mvh_id_vehiculo == vh_id).delete()
        session.flash = "La información sobre el vehículo ha sido modificada"
        redirect(URL('validaciones'))

    if request.vars.no:
        db.bitacora_general.insert(
            f_accion="[inventarios] Rechazada modificación de la información del vehículo num {}".format(vehiculo['mvh_num'])
        )
        db(db.modificacion_vehiculo.mvh_id_vehiculo == vh_id).delete()
        session.flash = "La información sobre el vehículo no ha sido modificada"
        redirect(URL('validaciones'))

    caracteristicas_list = [
        'Nº Bien Mueble',
        'Marca',
        'Modelo / Código',
        'Año',
        'Color',
        'Placa',
        'Propietario',
        'Serial de carroceria',
        'Serial de motor',
        'Serial de chasis',
        'Clase',
        'Tipo',
        'Clasificación',
        'Uso',
        'Servicio',
        'Nº de Puestos',
        'Nº de Ejes',
        'Tara',
        'Capacidad de carga',
        'Nº de Autorización INTT',
        'Rines',
        'Visibilidad',
        'Observaciones',
    ]

    caracteristicas_dict = {
        'Nº Bien Mueble': vehiculo['mvh_num'],
        'Marca': vehiculo['mvh_marca'],
        'Modelo / Código': vehiculo['mvh_modelo'],
        'Año': vehiculo['mvh_ano'],
        'Color': vehiculo['mvh_color'],
        'Placa': vehiculo['mvh_placa'].upper(),
        'Propietario': vehiculo['mvh_propietario'],
        'Serial de carroceria': vehiculo['mvh_serial_carroceria'],
        'Serial de motor': vehiculo['mvh_serial_motor'],
        'Serial de chasis': vehiculo['mvh_serial_chasis'],
        'Clase': vehiculo['mvh_clase'],
        'Tipo': vehiculo['mvh_tipo'],
        'Clasificación': vehiculo['mvh_clasificacion'],
        'Uso': vehiculo['mvh_uso'],
        'Servicio': vehiculo['mvh_servicio'],
        'Nº de Puestos': vehiculo['mvh_nro_puestos'],
        'Nº de Ejes': vehiculo['mvh_nro_ejes'],
        'Tara': str(vehiculo['mvh_tara']) + " " + vehiculo['mvh_tara_md'],
        'Capacidad de carga': str(vehiculo['mvh_capacidad_carga']) + " " + vehiculo['mvh_capacidad_carga_md'],
        'Nº de Autorización INTT': vehiculo['mvh_intt'],
        'Rines': vehiculo['mvh_rines'],
        'Visibilidad': None if vehiculo['mvh_oculto'] == 0 else "Oculto",
        'Observaciones': vehiculo['mvh_observaciones'],
    }

    caracteristicas_originales_dict = {
        'Nº Bien Mueble': vehiculo_original['vh_num'],
        'Propietario': vehiculo_original['vh_propietario'],
        'Placa': vehiculo_original['vh_placa'].upper(),
        'Marca': vehiculo_original['vh_marca'],
        'Modelo / Código': vehiculo_original['vh_modelo'],
        'Año': vehiculo_original['vh_ano'],
        'Serial de carroceria': vehiculo_original['vh_serial_carroceria'],
        'Serial de motor': vehiculo_original['vh_serial_motor'],
        'Serial de chasis': vehiculo_original['vh_serial_chasis'],
        'Color': vehiculo_original['vh_color'],
        'Clase': vehiculo_original['vh_clase'],
        'Tipo': vehiculo_original['vh_tipo'],
        'Clasificación': vehiculo_original['vh_clasificacion'],
        'Uso': vehiculo_original['vh_uso'],
        'Servicio': vehiculo_original['vh_servicio'],
        'Nº de Puestos': vehiculo_original['vh_nro_puestos'],
        'Nº de Ejes': vehiculo_original['vh_nro_ejes'],
        'Tara': str(vehiculo_original['vh_tara']) + " " + vehiculo_original['vh_tara_md'],
        'Capacidad de carga': str(vehiculo_original['vh_capacidad_carga']) + " " + vehiculo_original['vh_capacidad_carga_md'],
        'Nº de Autorización INTT': vehiculo_original['vh_intt'],
        'Rines': vehiculo_original['vh_rines'],
        'Visibilidad': None if vehiculo_original['vh_oculto'] == 0 else "Oculto",
        'Observaciones': vehiculo_original['vh_observaciones'],
    }

    depend = db(db.dependencias.id == vehiculo['mvh_dependencia']).select().first()
    sede_id = int(depend.id_sede)

    return dict(
        vehiculo=vehiculo,
        vehiculo_original=vehiculo_original,
        mantenimiento=mantenimiento,
        caracteristicas_list=caracteristicas_list,
        caracteristicas_originales_dict=caracteristicas_originales_dict,
        caracteristicas_dict=caracteristicas_dict,
        cod_localizacion=cod_localizacion,
        localizacion=localizacion,
        sede_id=sede_id,
        historial_prestamos=prestamos
    )

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles():
    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    bm = request.vars['bm']
    bien = db(db.bien_mueble.bm_num == bm).select()[0]
    espacio_nombre = db(db.espacios_fisicos.id == bien['bm_espacio_fisico']).select().first().codigo
    mantenimiento=__get_mantenimiento_bm(bm)

    # Si se elimina
    if request.vars.si:
        db(db.historial_mantenimiento_bm.hmbm_nro == bm).delete()
        db(db.bien_mueble.bm_num == bm).delete()
        db(db.modificacion_bien_mueble.mbn_num == bm).delete()
        db.bitacora_general.insert(
            f_accion="[inventarios] Eliminado el bien mueble num {} del espacio físico {}".format(bien['bm_num'], espacio_nombre)
        )
        session.flash = "El bien mueble ha sido eliminado"
        redirect(URL('validaciones'))
    # Si no se elimina
    if request.vars.no:
        db.bitacora_general.insert(
            f_accion="[inventarios] Rechazada eliminación del bien mueble num {} del espacio físico {}".format(bien['bm_num'], espacio_nombre)
        )
        db(db.bien_mueble.bm_num == bien['bm_num']).select().first().update_record(bm_eliminar=2)
        session.flash = "El bien mueble no ha sido eliminado"
        redirect(URL('validaciones'))

    if request.vars.modificacion:
        __agregar_modificar_bm(
            request.vars.nombre, bien['bm_num'], request.vars.no_placa,
            request.vars.marca, request.vars.modelo, request.vars.serial,
            request.vars.descripcion, request.vars.material, request.vars.color,
            request.vars.calibrar, request.vars.fecha_calibracion, request.vars.unidad,
            request.vars.ancho, request.vars.largo, request.vars.alto,
            request.vars.diametro, request.vars.movilidad, request.vars.tipo_uso, request.vars.estatus,
            request.vars.nombre_cat, request.vars.subcategoria, request.vars.cod_loc, request.vars.localizacion,
            request.vars.descripcion_modificacion, user_id)
        request.vars.modificacion = None

    if request.vars.mantenimiento_nuevo:
        __agregar_mantenimiento_bm(
            bien['bm_num'], request.vars.fecha_sol,
            request.vars.codigo, request.vars.tipo, request.vars.servicio,
            request.vars.accion, request.vars.descripcion_man, request.vars.proveedor,
            request.vars.fecha_inicio, request.vars.fecha_fin, request.vars.tiempo_ejec,
            request.vars.fecha_cert, request.vars.observacion_man)
        request.vars.mantenimiento_nuevo=None

    if request.vars.eliminacion:
        if bien['bm_eliminar'] == 2:
            db.bitacora_general.insert(
                f_accion="[inventarios] Añadida solicitud de eliminación del bien mueble num {} del espacio físico {}".format(bien['bm_num'], espacio_nombre)
            )
            db(db.bien_mueble.bm_num == bien['bm_num']).select().first().update_record(bm_eliminar = 0, bm_desc_eliminar = request.vars.descripcion_eliminacion)
            response.flash = "La solicitud de eliminación ha sido realizada exitosamente"
        else:
            response.flash = "El  \"{0}\" tiene una eliminación pendiente. \
                                Por los momentos no se enviarán solicitudes de eliminación.".format(bien['bm_nombre'])
        request.vars.eliminacion = None

    if request.vars.ocultar:
        if bien['bm_oculto'] == 0:
            db(db.bien_mueble.id == bien['id']).select().first().update_record(bm_oculto = 1)
            response.flash = "Ahora " + str(bien['bm_nombre']) + " se encuentra oculto en las consultas."
        else:
            response.flash = bien['bm_nombre'] + " ya se encuentra oculto en las consultas."
        request.vars.ocultar = None

    # Elementos que deben ser mostrados como una lista en el modal
    # de modificar BM
    material_pred = []
    color = []
    unidad_med = []
    movilidad = []
    uso = []
    nombre_cat = []
    cod_localizacion = []
    localizacion = []
    nombre_espaciof = []
    unidad_adscripcion = []

    material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
    color = ['Amarillo', 'Azul', 'Beige', 'Blanco', 'Dorado', 'Gris', 'Madera', 'Marrón', 'Mostaza', 'Naranja',
    'Negro', 'Plateado', 'Rojo', 'Rosado', 'Verde', 'Vinotinto', 'Otro color']
    unidad_med = ['cm', 'm']
    movilidad = ['Fijo', 'Portátil']
    uso = ['Docencia', 'Investigación', 'Extensión', 'Apoyo administrativo']
    nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento',
    'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
    cod_localizacion = ['150301', '240107']
    localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
    'Edo Vargas, Municipio Vargas, Parroquia Macuto']

    if bien['bm_clasificacion']=="Equipo":
       
        caracteristicas_list = ['Marca:', 'Modelo:', 'Serial:',
        'Material predominante:', 'Color:', 'Movilidad:', 'Uso:']

        if bien['bm_descripcion']!="" and bien['bm_descripcion']!=None:
            caracteristicas_list.append('Observaciones:')

        caracteristicas_dict = {
            'Marca:': bien['bm_marca'],
            'Modelo:': bien['bm_modelo'],
            'Serial:': bien['bm_serial'],
            'Observaciones:': bien['bm_descripcion'],
            'Material predominante:': bien['bm_material'],
            'Color:': bien['bm_color'],
            'Movilidad:': bien['bm_movilidad'],
            'Uso:': bien['bm_uso']
        }
    elif bien['bm_clasificacion']=="Mobiliario":

        caracteristicas_list = ['Material predominante:', 'Color:', 'Movilidad:', 'Uso:']

        if bien['bm_descripcion']!="" and bien['bm_descripcion']!=None:
            caracteristicas_list.append('Observaciones:')

        caracteristicas_dict = {
            'Observaciones:': bien['bm_descripcion'],
            'Material predominante:': bien['bm_material'],
            'Color:': bien['bm_color'],
            'Movilidad:': bien['bm_movilidad'],
            'Uso:': bien['bm_uso']
        }

    sudebid_list = ['Localización:', 'Código Localización:', 'Categoría:', 'Subcategoría:']
    sudebid_dict = {
        'Localización:': bien['bm_localizacion'],
        'Código Localización:': bien['bm_codigo_localizacion'],
        'Categoría:': bien['bm_categoria'],
        'Subcategoría:': bien['bm_subcategoria']
    }

    return dict(bien=bien,
                material_pred=material_pred,
                color_list=color,
                unidad_med=unidad_med,
                movilidad_list=movilidad,
                uso_list=uso,
                nombre_cat=nombre_cat,
                cod_localizacion=cod_localizacion,
                localizacion=localizacion,
                caracteristicas_list=caracteristicas_list,
                caracteristicas_dict=caracteristicas_dict,
                sudebid_list=sudebid_list,
                sudebid_dict=sudebid_dict,
                mantenimiento=mantenimiento)


@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles_mat():
    #Recuperamos el espacio
    espacio = request.vars['espacio']
    #El nombre del material/consumible
    name = request.vars['nombreMat']
    espacio_nombre = db(db.espacios_fisicos.id == espacio).select().first().codigo

    # El usuario que está editando
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id

    # Busco el material/consumible
    bien = db( (db.sin_bn.sb_espacio == espacio) & (db.sin_bn.sb_nombre == name) ).select()[0]

    #Inicializo variables
    material_pred = []
    color = []
    unidad_med = []
    movilidad = []
    uso = []
    nombre_cat = []
    cod_localizacion = []
    localizacion = []
    nombre_espaciof = []
    unidad_adscripcion = []
    unidad_cap = []
    presentacion=[]

    # Si se elimina
    if request.vars.si:
        db.bitacora_general.insert(
            f_accion="[inventarios] Eliminado el material de laboratorio {} del espacio físico {}".format(name, espacio_nombre)
        )
        db( (db.sin_bn.sb_espacio == espacio) & (db.sin_bn.sb_nombre == name) ).delete()
        db( (db.modificacion_sin_bn.msb_espacio == espacio) & (db.modificacion_sin_bn.msb_nombre == name) ).delete()
        session.flash = "El material de laboratorio ha sido eliminado"
        redirect(URL('validaciones'))
    # Si no se elimina
    if request.vars.no:
        db.bitacora_general.insert(
            f_accion="[inventarios] Rechazada eliminación del material de laboratorio {} del espacio físico {}".format(name, espacio_nombre)
        )
        db(db.sin_bn.id == bien['id']).select().first().update_record(sb_eliminar = 2)
        session.flash = "El material de laboratorio no ha sido eliminado"
        redirect(URL('validaciones'))

    #Si se edita
    if request.vars.nombre_mat:
        __agregar_material_modificar(
            request.vars.nombre_mat,
            request.vars.marca_mat, request.vars.modelo_mat, request.vars.cantidad_mat, espacio, request.vars.ubicacion_int ,
            request.vars.descripcion_mat, request.vars.aforado, request.vars.calibracion_mat,
            request.vars.capacidad, request.vars.unidad_cap,
                request.vars.unidad_mat, 
            request.vars.ancho_mat, request.vars.largo_mat, request.vars.alto_mat,
            request.vars.diametro_mat, request.vars.material_mat, request.vars.material_sec, request.vars.presentacion,
            request.vars.unidades, request.vars.total_mat, user_id, request.vars.clasificacion, request.vars.descripcion_modificacion)

    if request.vars.eliminacion:
        if bien['sb_eliminar'] == 2:
            db.bitacora_general.insert(
                f_accion="[inventarios] Añadida solicitud de eliminación del material de laboratorio {} del espacio físico {}".format(name, espacio_nombre)
            )
            db(db.sin_bn.id == bien['id']).select().first().update_record(sb_eliminar = 0, sb_desc_eliminar = request.vars.descripcion_eliminacion)
            response.flash = "La solicitud de eliminación ha sido realizada exitosamente"
        else:
            response.flash = "El  \"{0}\" tiene una eliminación pendiente. \
                                Por los momentos no se enviarán solicitudes de eliminación.".format(bien['sb_nombre'])
        request.vars.eliminacion = None

    if request.vars.ocultar:
        if bien['sb_oculto'] == 0:
            db(db.sin_bn.id == bien['id']).select().first().update_record(sb_oculto = 1)
            response.flash = "Ahora " + str(bien['sb_nombre']) + " se encuentra oculto en las consultas."
        else:
            response.flash = bien['sb_nombre'] + " ya se encuentra oculto en las consultas."
        request.vars.ocultar = None

    aforado_options = ['Si', 'No', 'N/A']
    material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
    color = ['Amarillo', 'Azul', 'Beige', 'Blanco', 'Dorado', 'Gris', 'Madera', 'Marrón', 'Mostaza', 'Naranja',
    'Negro', 'Plateado', 'Rojo', 'Rosado', 'Verde', 'Vinotinto', 'Otro color']
    unidad_med = ['cm', 'm']
    movilidad = ['Fijo', 'Portátil']
    uso = ['Docencia', 'Investigación', 'Extensión', 'Apoyo administrativo']
    nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento',
                'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
    cod_localizacion = ['150301', '240107']
    localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
    'Edo Vargas, Municipio Vargas, Parroquia Macuto']
    unidad_cap = ['m³', 'l', 'ml', 'μl', 'kg', 'g', 'mg', 'μg', 'galón', 'oz', 'cup', 'lb']
    presentacion=["Caja", "Paquete", "Unidad", "Otro"]
    if bien['sb_clasificacion'] == "Material de Laboratorio":
        caracteristicas_list = ['Cantidad:', 'Descripción:', 'Marca:', 'Modelo:', 'Aforado:', 'Requiere calibración:',
        'Capacidad:', 'Unidad de medida:', 'Material predominante:', 'Material secundario:', 'Tipo:', 'Ubicación interna:']
        caracteristicas_dict = {
            'Cantidad:': bien['sb_cantidad'],
            'Marca:': bien['sb_marca'],
            'Modelo:': bien['sb_modelo'],
            'Descripción:': bien['sb_descripcion'],
            'Material predominante:': bien['sb_material'],
            'Material secundario:': bien['sb_material_sec'],
            'Aforado:': bien['sb_aforado'],
            'Tipo:': bien['sb_clasificacion'],
            'Requiere calibración:': bien['sb_calibrar'],
            'Ubicación interna:' : bien['sb_ubicacion'],
            'Capacidad:': bien['sb_capacidad'],
            'Unidad de medida:' : bien['sb_unidad'],
        }
    else:
        caracteristicas_list = ["Marca:", "Modelo:", "Presentación:", "Unidades por presentación:", "Cantidad:",
        "Total(U.):", "Descripción:", "Ubicación interna:"]
        caracteristicas_dict = {
            'Presentación:': bien['sb_presentacion'],
            'Unidades por presentación:': bien['sb_unidades'],
            'Cantidad:': bien['sb_cantidad'],
            'Total(U.):': bien['sb_total'],
            'Marca:': bien['sb_marca'],
            'Modelo:': bien['sb_modelo'],
            'Descripción:': bien['sb_descripcion'],
            'Ubicación interna:' : bien['sb_ubicacion'],
            'Tipo:': bien['sb_clasificacion']
        }
    return dict(bien=bien,
                material_pred=material_pred,
                color_list=color,
                unidad_med=unidad_med,
                movilidad_list=movilidad,
                uso_list=uso,
                nombre_cat=nombre_cat,
                cod_localizacion=cod_localizacion,
                localizacion=localizacion,
                caracteristicas_list=caracteristicas_list,
                caracteristicas_dict=caracteristicas_dict,
                aforado_options=aforado_options,
                unidad_cap=unidad_cap,
                presentacion=presentacion
                )

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles_consumibles():
    #Recuperamos el espacio
    espacio = request.vars['espacio']
    #El nombre del material/consumible
    name = request.vars['nombreMat']
    espacio_nombre = db(db.espacios_fisicos.id == espacio).select().first().codigo

    # El usuario que está editando
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id

    # Busco el material/consumible
    bien = db( (db.sin_bn.sb_espacio == espacio) & (db.sin_bn.sb_nombre == name) ).select()[0]

    #Inicializo variables
    material_pred = []
    color = []
    unidad_med = []
    movilidad = []
    uso = []
    nombre_cat = []
    cod_localizacion = []
    localizacion = []
    nombre_espaciof = []
    unidad_adscripcion = []
    unidad_cap = []
    presentacion=[]

    # Si se elimina
    if request.vars.si:
        db.bitacora_general.insert(
            f_accion="[inventarios] Eliminado el consumible {} del espacio físico {}".format(name, espacio_nombre)
        )
        db( (db.sin_bn.sb_espacio == espacio) & (db.sin_bn.sb_nombre == name) ).delete()
        db( (db.modificacion_sin_bn.msb_espacio == espacio) & (db.modificacion_sin_bn.msb_nombre == name) ).delete()
        session.flash = "El consumible ha sido eliminado"
        redirect(URL('validaciones'))
    # Si no se elimina
    if request.vars.no:
        db.bitacora_general.insert(
            f_accion="[inventarios] Rechazada eliminación del consumible {} del espacio físico {}".format(name, espacio_nombre)
        )
        db(db.sin_bn.id == bien['id']).select().first().update_record(sb_eliminar = 2)
        db( (db.modificacion_sin_bn.msb_espacio == espacio) & (db.modificacion_sin_bn.msb_nombre == name) ).delete()
        session.flash = "El consumible no ha sido eliminado"
        redirect(URL('validaciones'))

    #Si se edita
    if request.vars.nombre_mat:
        __agregar_material_modificar(
            request.vars.nombre_mat,
            request.vars.marca_mat, request.vars.modelo_mat, request.vars.cantidad_mat, espacio, request.vars.ubicacion_int ,
            request.vars.descripcion_mat, request.vars.aforado, request.vars.calibracion_mat,
            request.vars.capacidad, request.vars.unidad_cap,
                request.vars.unidad_mat, 
            request.vars.ancho_mat, request.vars.largo_mat, request.vars.alto_mat,
            request.vars.diametro_mat, request.vars.material_mat, request.vars.material_sec, request.vars.presentacion,
            request.vars.unidades, request.vars.total_mat, user_id, request.vars.clasificacion, request.vars.descripcion_modificacion)

    if request.vars.eliminacion:
        if bien['sb_eliminar'] == 2:
            db.bitacora_general.insert(
                f_accion="[inventarios] Añadida solicitud de eliminación del consumible {} del espacio físico {}".format(name, espacio_nombre)
            )
            db(db.sin_bn.id == bien['id']).select().first().update_record(sb_eliminar = 0, sb_desc_eliminar = request.vars.descripcion_eliminacion)
            response.flash = "La solicitud de eliminación ha sido realizada exitosamente"
        else:
            response.flash = "El  \"{0}\" tiene una eliminación pendiente. \
                                Por los momentos no se enviarán solicitudes de eliminación.".format(bien['sb_nombre'])
        request.vars.eliminacion = None

    if request.vars.ocultar:
        if bien['sb_oculto'] == 0:
            db(db.sin_bn.id == bien['id']).select().first().update_record(sb_oculto = 1)
            response.flash = "Ahora " + str(bien['sb_nombre']) + " se encuentra oculto en las consultas."
        else:
            response.flash = bien['sb_nombre'] + " ya se encuentra oculto en las consultas."
        request.vars.ocultar = None

    aforado_options = ['Si', 'No', 'N/A']
    material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
    color = ['Amarillo', 'Azul', 'Beige', 'Blanco', 'Dorado', 'Gris', 'Madera', 'Marrón', 'Mostaza', 'Naranja',
    'Negro', 'Plateado', 'Rojo', 'Rosado', 'Verde', 'Vinotinto', 'Otro color']
    unidad_med = ['cm', 'm']
    movilidad = ['Fijo', 'Portátil']
    uso = ['Docencia', 'Investigación', 'Extensión', 'Apoyo administrativo']
    nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento',
                'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
    cod_localizacion = ['150301', '240107']
    localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
    'Edo Vargas, Municipio Vargas, Parroquia Macuto']
    unidad_cap = ['m³', 'l', 'ml', 'μl', 'kg', 'g', 'mg', 'μg', 'galón', 'oz', 'cup', 'lb']
    presentacion=["Caja", "Paquete", "Unidad", "Otro"]
    if bien['sb_clasificacion'] == "Material de Laboratorio":
        caracteristicas_list = ['Cantidad:', 'Descripción:', 'Marca:', 'Modelo:', 'Aforado:', 'Requiere calibración:',
        'Capacidad:', 'Unidad de medida:', 'Material predominante:', 'Material secundario:', 'Tipo:', 'Ubicación interna:']
        caracteristicas_dict = {
            'Cantidad:': bien['sb_cantidad'],
            'Marca:': bien['sb_marca'],
            'Modelo:': bien['sb_modelo'],
            'Descripción:': bien['sb_descripcion'],
            'Material predominante:': bien['sb_material'],
            'Material secundario:': bien['sb_material_sec'],
            'Aforado:': bien['sb_aforado'],
            'Tipo:': bien['sb_clasificacion'],
            'Requiere calibración:': bien['sb_calibrar'],
            'Ubicación interna:' : bien['sb_ubicacion'],
            'Capacidad:': bien['sb_capacidad'],
            'Unidad de medida:' : bien['sb_unidad'],
        }
    else:
        caracteristicas_list = ["Marca:", "Modelo:", "Presentación:", "Unidades por presentación:", "Cantidad:",
        "Total(U.):", "Descripción:", "Ubicación interna:"]
        caracteristicas_dict = {
            'Presentación:': bien['sb_presentacion'],
            'Unidades por presentación:': bien['sb_unidades'],
            'Cantidad:': bien['sb_cantidad'],
            'Total(U.):': bien['sb_total'],
            'Marca:': bien['sb_marca'],
            'Modelo:': bien['sb_modelo'],
            'Descripción:': bien['sb_descripcion'],
            'Ubicación interna:' : bien['sb_ubicacion'],
            'Tipo:': bien['sb_clasificacion']
        }
    return dict(bien=bien,
                material_pred=material_pred,
                color_list=color,
                unidad_med=unidad_med,
                movilidad_list=movilidad,
                uso_list=uso,
                nombre_cat=nombre_cat,
                cod_localizacion=cod_localizacion,
                localizacion=localizacion,
                caracteristicas_list=caracteristicas_list,
                caracteristicas_dict=caracteristicas_dict,
                aforado_options=aforado_options,
                unidad_cap=unidad_cap,
                presentacion=presentacion
                )

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles_herramientas():
    #Recuperamos el espacio
    espacio = request.vars['espacio']
    #El nombre de la herramienta
    name = request.vars['nombreHer']
    #La ubicacion interna
    ubicacion = request.vars['ubicacion']
    espacio_nombre = db(db.espacios_fisicos.id == espacio).select().first().codigo


    # El usuario que está editando
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id

    # Busco la herramienta
    bien = db((db.herramienta.hr_nombre == name) & (db.herramienta.hr_espacio_fisico==espacio) & (db.herramienta.hr_ubicacion==ubicacion)).select()[0]

    #Inicializo variables
    material_pred = []
    unidad_med = []
    presentacion=[]

    # Si se elimina
    if request.vars.si:
        db.bitacora_general.insert(
            f_accion="[inventarios] Eliminado la herramienta {} del espacio físico {}".format(name, espacio_nombre)
        )
        db((db.herramienta.hr_nombre == name) & (db.herramienta.hr_espacio_fisico==espacio) & (db.herramienta.hr_ubicacion==ubicacion)).delete()
        db((db.modificacion_herramienta.mhr_nombre == name) & (db.modificacion_herramienta.mhr_espacio_fisico==espacio) & (db.modificacion_herramienta.mhr_ubicacion==ubicacion)).delete()
        session.flash = "La herramienta ha sido eliminada"
        redirect(URL('validaciones'))
    # Si no se elimina
    if request.vars.no:
        db.bitacora_general.insert(
            f_accion="[inventarios] Rechazada la eliminación de la herramienta {} del espacio físico {}".format(name, espacio_nombre)
        )
        db(db.herramienta.id == bien['id']).select().first().update_record(hr_eliminar = 2)
        db((db.modificacion_herramienta.mhr_nombre == name) & (db.modificacion_herramienta.mhr_espacio_fisico==espacio) & (db.modificacion_herramienta.mhr_ubicacion==ubicacion)).delete()
        session.flash = "La herramienta no ha sido eliminada"
        redirect(URL('validaciones'))

    #Si se edita
    if request.vars.nombre_her:
        __agregar_herramienta_modificar(
            request.vars.nombre_her, request.vars.num_her,request.vars.marca_her, request.vars.modelo_her,
            request.vars.serial_her, request.vars.presentacion, request.vars.numpiezas_her, request.vars.contenido_her,
            request.vars.descripcion_her,  request.vars.material_mat,request.vars.unidad, request.vars.ancho_her,
            request.vars.largo_her, request.vars.alto_her, request.vars.diametro_her, request.vars.ubicacion_int,
            request.vars.descripcion_herramientas, request.vars.descripcion_modificacion_her, espacio,
            bien['hr_unidad_de_adscripcion'], bien['hr_depedencia'], bien['hr_crea_ficha'] ,user_id)

    if request.vars.eliminacion:
        if bien['hr_eliminar'] == 2:
            db.bitacora_general.insert(
                f_accion="[inventarios] Añadida solicitud de eliminación de la herramienta {} del espacio físico {}".format(name, espacio_nombre)
            )
            db(db.herramienta.id == bien['id']).select().first().update_record(hr_eliminar = 0, hr_desc_eliminar = request.vars.descripcion_eliminacion)
            response.flash = "La solicitud de eliminación ha sido realizada exitosamente"
        else:
            response.flash = "El  \"{0}\" tiene una eliminación pendiente. \
                                Por los momentos no se enviarán solicitudes de eliminación.".format(bien['hr_nombre'])
        request.vars.eliminacion = None

    if request.vars.ocultar:
        if bien['hr_oculto'] == 0:
            db(db.herramienta.id == bien['id']).select().first().update_record(hr_oculto = 1)
            response.flash = "Ahora " + str(bien['hr_nombre']) + " se encuentra oculto en las consultas."
        else:
            response.flash = bien['hr_nombre'] + " ya se encuentra oculto en las consultas."
        request.vars.ocultar = None

    material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
    unidad_med = ['cm', 'm']
    presentacion=["Unidad", "Conjunto"]
    if bien['hr_presentacion'] == "Unidad":
        caracteristicas_list = [ 'Número de Bien Nacional:', 'Marca:', 'Modelo:', 'Serial:', 'Presentación:',
        'Material predominante:', 'Ubicación interna:']
        caracteristicas_dict = {
            'Número de Bien Nacional:': bien['hr_num'],
            'Marca:': bien['hr_marca'],
            'Modelo:': bien['hr_modelo'],
            'Serial:': bien['hr_serial'],
            'Presentación:': bien['hr_presentacion'],
            'Material predominante:': bien['hr_material'],
            'Ubicación interna:' : bien['hr_ubicacion']
        }
    else:
        caracteristicas_list = [ 'Número de Bien Nacional:', 'Marca:', 'Modelo:', 'Serial:', 'Presentación:',
        'Número de Piezas:', 'Contenido:', 'Descripción:', 'Material predominante:', 'Ubicación interna:']
        caracteristicas_dict = {
            'Número de Bien Nacional::': bien['hr_num'],
            'Marca:': bien['hr_marca'],
            'Modelo:': bien['hr_modelo'],
            'Serial:': bien['hr_serial'],
            'Presentación:': bien['hr_presentacion'],
            'Número de Piezas:': bien['hr_numpiezas'],
            'Contenido:': bien['hr_contenido'],
            'Descripción:': bien['hr_descripcion'],
            'Material predominante:': bien['hr_material'],
            'Ubicación interna:' : bien['hr_ubicacion']
        }

    if not caracteristicas_dict['Marca:']:
        del caracteristicas_dict['Marca:']
        caracteristicas_list.remove('Marca:')

    if not caracteristicas_dict['Modelo:']:
        del caracteristicas_dict['Modelo:']
        caracteristicas_list.remove('Modelo:')

    if not caracteristicas_dict['Serial:']:
        del caracteristicas_dict['Serial:']
        caracteristicas_list.remove('Serial:')

    return dict(bien = bien,
                material_pred = material_pred,
                caracteristicas_list = caracteristicas_list,
                caracteristicas_dict = caracteristicas_dict,
                unidad_med = unidad_med,
                presentacion = presentacion
                )

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles_prestamo():
    """
    GET: Muestra en pantalla los detalles de un préstamo o un error
    si un préstamo no existe.

    POST: Permite al custodio o responsable aprobar o rechazar una solicitud de
    préstamo.
    """

    prestamo_id = request.vars['prestamo']

    try:
        prestamo = db(db.historial_prestamo_vh.id == prestamo_id).select().first()
    except:
        return "Préstamo inválido."

    try:
        vehiculo = db(db.vehiculo.id == prestamo['hpvh_vh_id']).select().first()
    except:
        return "Vehículo inválido."

    try:
        solicitante = db(db.auth_user.id == prestamo['hpvh_solicitante']).select().first()
    except:
        return "Solicitante inválido."

    esta_autorizado = (auth.user.id == vehiculo['vh_responsable']) or (auth.user.id == vehiculo['vh_custodio']) or (auth.user.id == 1)

    # Si el usuario autorizado marcó que quería registrar la salida del vehículo
    if esta_autorizado and request.vars.salida:
        # Actualizamos la entrada en la base de datos
        db(db.historial_prestamo_vh.id == prestamo_id).update(
            hpvh_estatus="Vehículo en uso",
            hpvh_autoriza_salida=auth.user.id,
            hpvh_fecha_salida=datetime.now(),
            hpvh_km_salida=request.vars.km_salida,
            hpvh_gasolina_salida=request.vars.gasolina_salida,
            hpvh_aceite_motor_salida=request.vars.aceite_motor_salida,
            hpvh_aceite_caja_salida=request.vars.aceite_caja_salida,
            hpvh_agua_ref_salida=request.vars.agua_ref_salida,
            hpvh_bateria_salida=request.vars.bateria_salida,
            hpvh_cauchos_salida=request.vars.cauchos_salida,
            hpvh_caucho_repuesto_salida=request.vars.caucho_repuesto_salida,
            hpvh_herramientas_seguridad_salida=request.vars.herramientas_seguridad_salida,
            hpvh_latoneria_salida=request.vars.latoneria_salida,
            hpvh_pintura_salida=request.vars.pintura_salida,
            hpvh_accesorios_salida=request.vars.accesorios_salida,
            hpvh_cartel_uso_oficial_salida=request.vars.cartel_uso_oficial_salida,
            hpvh_listado_fluidos_salida=request.vars.listado_fluidos_salida,
            hpvh_carnet_circulacion=int(request.vars.carnet_circulacion_salida),
            hpvh_poliza_seguridad=int(request.vars.poliza_seguridad_salida),
            hpvh_lista_telf_emerg=int(request.vars.lista_telf_emerg_salida),
            hpvh_manual_uso_vehic=int(request.vars.manual_uso_vehic_salida)
        )

        # Colocamos un estatus especial al vehículo
        db(db.vehiculo.id == vehiculo.id).update(
            vh_estatus = "En uso"
        )

        # Guardamos información en bitácora
        db.bitacora_general.insert(
            f_accion="[préstamos] Registrada la salida en préstamo del vehículo de placa {}.".format(prestamo_id, vehiculo['vh_placa'])
        )

        # Enviamos notificación al responsable
        asunto_correo = "[SIGULAB] Salida de Vehículo en Solicitud de Preéstamo #{}".format(vehiculo.vh_placa)
        email_responsable = db(db.auth_user.id == vehiculo.vh_responsable).select().first().email
        mensaje_aprobacion_responsable = ("Estimado usuario, por medio de la presente le notificamos que el usuario {} {} ha REGISTRADO " + \
                                      "LA SALIDA del vehículo {} {} {} en la ficha del Préstamo #{} realizado por {} {}, del cual usted es Responsable Patrimonial, " + \
                                      "en fecha {}.").format(
                                      auth.user.first_name,
                                      auth.user.last_name,
                                      vehiculo.vh_marca,
                                      vehiculo.vh_modelo,
                                      vehiculo.vh_placa,
                                      prestamo_id,
                                      solicitante.first_name,
                                      solicitante.last_name,
                                      datetime.now()
        )

        # Manda correo de aprobación al responsable
        __enviar_correo(
            email_responsable,
            asunto_correo,
            mensaje_aprobacion_responsable
        )

        session.flash = "Se ha registrado la salida del vehículo en la Solicitud de Préstamo #%s." % prestamo_id
        return redirect(URL('prestamos'))

    # Si el usuario autorizado marcó que quería registrar la devolución del vehículo
    if esta_autorizado and request.vars.devolucion:

        # Actualizamos la entrada en la base de datos
        db(db.historial_prestamo_vh.id == prestamo_id).update(
            hpvh_estatus="Vehículo devuelto",
            hpvh_autoriza_devolucion=auth.user.id,
            hpvh_fecha_devolucion=datetime.now(),
            hpvh_km_devolucion=request.vars.km_devolucion,
            hpvh_gasolina_devolucion=request.vars.gasolina_devolucion,
            hpvh_aceite_motor_devolucion=request.vars.aceite_motor_devolucion,
            hpvh_aceite_caja_devolucion=request.vars.aceite_caja_devolucion,
            hpvh_agua_ref_devolucion=request.vars.agua_ref_devolucion,
            hpvh_bateria_devolucion=request.vars.bateria_devolucion,
            hpvh_cauchos_devolucion=request.vars.cauchos_devolucion,
            hpvh_caucho_repuesto_devolucion=request.vars.caucho_repuesto_devolucion,
            hpvh_herramientas_seguridad_devolucion=request.vars.herramientas_seguridad_devolucion,
            hpvh_latoneria_devolucion=request.vars.latoneria_devolucion,
            hpvh_pintura_devolucion=request.vars.pintura_devolucion,
            hpvh_accesorios_devolucion=request.vars.accesorios_devolucion,
            hpvh_cartel_uso_oficial_devolucion=request.vars.cartel_uso_oficial_devolucion,
            hpvh_listado_fluidos_devolucion=request.vars.listado_fluidos_devolucion,
            hpvh_carnet_circulacion= prestamo['hpvh_carnet_circulacion'] if request.vars.carnet_circulacion_devolucion is None else __safe_int(request.vars.carnet_circulacion_devolucion),
            hpvh_poliza_seguridad=prestamo['hpvh_poliza_seguridad'] if request.vars.poliza_seguridad_devolucion is None else __safe_int(request.vars.poliza_seguridad_devolucion),
            hpvh_lista_telf_emerg=prestamo['hpvh_lista_telf_emerg'] if request.vars.lista_telf_emerg_devolucion is None else __safe_int(request.vars.lista_telf_emerg_devolucion),
            hpvh_manual_uso_vehic=prestamo['hpvh_manual_uso_vehic'] if request.vars.manual_uso_vehic_devolucion is None else __safe_int(request.vars.manual_uso_vehic_devolucion)
        )

        # Retornamos el vehículo a su estatus por defecto
        db(db.vehiculo.id == vehiculo.id).update(
            vh_estatus = "Disponible"
        )

        # Guardamos información en bitácora
        db.bitacora_general.insert(
            f_accion="[préstamos] Registrada la devolución del vehículo en préstamo de placa {}.".format(prestamo_id, vehiculo['vh_placa'])
        )

        # Enviamos notificación al responsable
        asunto_correo = "[SIGULAB] Devolución de Vehículo en Solicitud de Preéstamo #{}".format(vehiculo.vh_placa)
        email_responsable = db(db.auth_user.id == vehiculo.vh_responsable).select().first().email
        mensaje_aprobacion_responsable = ("Estimado usuario, por medio de la presente le notificamos que el usuario {} {} ha REGISTRADO " + \
                                      "LA DEVOLUCIÓN del vehículo {} {} {} en la ficha del Préstamo #{} realizado por {} {}, del cual usted es Responsable Patrimonial, " + \
                                      "en fecha {}.").format(
                                      auth.user.first_name,
                                      auth.user.last_name,
                                      vehiculo.vh_marca,
                                      vehiculo.vh_modelo,
                                      vehiculo.vh_placa,
                                      prestamo_id,
                                      solicitante.first_name,
                                      solicitante.last_name,
                                      datetime.now()
        )

        # Manda correo de aprobación al responsable
        __enviar_correo(
            email_responsable,
            asunto_correo,
            mensaje_aprobacion_responsable
        )

        session.flash = "Se ha registrado la devolución del vehículo en la Solicitud de Préstamo #%s." % prestamo_id
        return redirect(URL('prestamos'))


    # Si el usuario autorizado marcó que quería aprobar la solicitud
    if esta_autorizado and request.vars.aprobado:
        # Actualizamos la entrada en la base de datos
        db(db.historial_prestamo_vh.id == prestamo_id).update(
            hpvh_autorizado_por=auth.user.id,
            hpvh_fecha_autorizacion=datetime.now(),
            hpvh_estatus="Aprobada"
        )

        # Colocamos un estatus especial al vehículo
        db(db.vehiculo.id == vehiculo.id).update(
            vh_estatus = "En préstamo"
        )

        # Guardamos información en bitácora
        db.bitacora_general.insert(
            f_accion="[préstamos] Aceptada solicitud de préstamo #{} del vehículo de placa {}.".format(prestamo_id, vehiculo['vh_placa'])
        )

        asunto_correo = "[SIGULAB] Solicitud de Préstamo #%s Aprobada" % prestamo_id

        # Enviamos notificación al responsable
        email_responsable = db(db.auth_user.id == vehiculo.vh_responsable).select().first().email
        mensaje_aprobacion_responsable = ("Estimado usuario, por medio de la presente le notificamos que el usuario {} {} ha APROBADO " + \
                                      "la Solicitud de Préstamo #{} realizada por {} {} al vehículo {} {} {}, del cual usted es Responsable Patrimonial, " + \
                                      "en fecha {}.").format(
                                      auth.user.first_name,
                                      auth.user.last_name,
                                      prestamo_id,
                                      solicitante.first_name,
                                      solicitante.last_name,
                                      vehiculo.vh_marca,
                                      vehiculo.vh_modelo,
                                      vehiculo.vh_placa,
                                      datetime.now()
        )

        # Manda correo de aprobación al responsable
        __enviar_correo(
            email_responsable,
            asunto_correo,
            mensaje_aprobacion_responsable
        )

        # Enviamos notificación al solicitante
        email_solicitante = solicitante.email
        mensaje_aprobacion_solicitante = ("Estimado usuario, por medio de la presente le notificamos que el usuario {} {} ha APROBADO " + \
                                      "la Solicitud de Préstamo #{} realizada por usted al vehículo {} {} {} " + \
                                      "en fecha {}. Puede proceder a contactar al responsable del vehículo para retirar las llaves otros documentos.").format(
                                      auth.user.first_name,
                                      auth.user.last_name,
                                      prestamo_id,
                                      vehiculo.vh_marca,
                                      vehiculo.vh_modelo,
                                      vehiculo.vh_placa,
                                      datetime.now()
        )

        # Manda correo aprobación a solicitante
        __enviar_correo(
            email_solicitante,
            asunto_correo,
            mensaje_aprobacion_solicitante
        )

        session.flash = "Se ha aprobado la Solicitud de Préstamo #%s." % prestamo_id
        return redirect(URL('prestamos'))

    # Si el usuario autorizado ha rechazado la solicitud
    if esta_autorizado and request.vars.rechazo:
        motivo = request.vars.motivo_rechazo

        # Actualizamos la entrada en la base de datos
        db(db.historial_prestamo_vh.id == prestamo_id).update(
            hpvh_autorizado_por=auth.user.id,
            hpvh_razon_rechazo=motivo,
            hpvh_fecha_autorizacion=datetime.now(),
            hpvh_estatus="Denegada"
        )

        # Guardamos información en bitácora
        db.bitacora_general.insert(
            f_accion="[préstamos] Rechazada solicitud de préstamo #{} del vehículo de placa {}.".format(prestamo_id, vehiculo['vh_placa'])
        )

        asunto_rechazo = "[SIGULAB] Rechazo a la Solicitud de Préstamo #%s" % prestamo_id

        # Enviamos notificación al responsable patrimonial
        email_responsable = db(db.auth_user.id == vehiculo.vh_responsable).select().first().email
        mensaje_rechazo_responsable = ("Estimado usuario, por medio de la presente le notificamos que el usuario {} {} ha RECHAZADO " + \
                                      "la Solicitud de Préstamo #{} realizada por {} {} al vehículo {} {} {}, del cual usted es Responsable Patrimonial, " + \
                                      "en fecha {}. Como razón de rechazo, se especificó: {}").format(
                                      auth.user.first_name,
                                      auth.user.last_name,
                                      prestamo_id,
                                      solicitante.first_name,
                                      solicitante.last_name,
                                      vehiculo.vh_marca,
                                      vehiculo.vh_modelo,
                                      vehiculo.vh_placa,
                                      datetime.now(),
                                      motivo
        )

        __enviar_correo(
            email_responsable,
            asunto_rechazo,
            mensaje_rechazo_responsable
        )

        # Enviamos notificación al solicitante
        email_solicitante = solicitante.email
        mensaje_rechazo_solicitante = ("Estimado usuario, por medio de la presente le notificamos que el usuario {} {} ha RECHAZADO " + \
                                      "la Solicitud de Préstamo #{} realizada por usted al vehículo {} {} {} " + \
                                      "en fecha {}. Como razón de rechazo, se especificó: {}").format(
                                      auth.user.first_name,
                                      auth.user.last_name,
                                      prestamo_id,
                                      vehiculo.vh_marca,
                                      vehiculo.vh_modelo,
                                      vehiculo.vh_placa,
                                      datetime.now(),
                                      motivo
        )

        # Manda correo rechazo a solicitante
        __enviar_correo(
            email_solicitante,
            asunto_rechazo,
            mensaje_rechazo_solicitante
        )

        session.flash = "Se ha rechazado la Solicitud de Préstamo #%s." % prestamo_id
        return redirect(URL('prestamos'))

    try:
        autorizado_por = db(db.auth_user.id == prestamo['hpvh_autorizado_por']).select().first()
        nombre_autorizado = "%s %s" % (autorizado_por.first_name, autorizado_por.last_name)
    except Exception as e:
        autorizado_por = -1
        nombre_autorizado = ""

    informacion_dict = {
        "Vehículo Solicitado": "%s %s" % (
            vehiculo['vh_marca'],
            vehiculo['vh_modelo']
        ),
        "Placa": vehiculo['vh_placa'],
        "Solicitante": "%s %s" % (
            solicitante.first_name,
            solicitante.last_name
        ),
        "Fecha de Solicitud": prestamo['hpvh_fecha_solicitud'].strftime("%d/%m/%y %I:%M %p"),
        "Fecha Prevista de Salida": prestamo['hpvh_fecha_prevista_salida'].strftime("%d/%m/%y"),
        "Fecha Prevista de Devolución": prestamo['hpvh_fecha_prevista_devolucion'].strftime("%d/%m/%y"),
        "Motivo de Solicitud": prestamo['hpvh_motivo'],
        "Ruta Prevista": prestamo['hpvh_ruta'],
        "Tiempo Estimado de Uso": "%s %s" % (prestamo['hpvh_tiempo_estimado_uso'], prestamo['hpvh_tiempo_estimado_uso_md']),
        "Estatus": prestamo['hpvh_estatus'],
        "Razón de Rechazo": prestamo['hpvh_razon_rechazo'],
        "Rechazada por": nombre_autorizado if "rechazada" in prestamo['hpvh_estatus'] else None,
        "Aprobada por": nombre_autorizado if "aprobada" in prestamo['hpvh_estatus'] else None,
        "Fecha de Aprobación": prestamo['hpvh_fecha_autorizacion'] if "rechazada" in prestamo['hpvh_estatus'] else None,
        "Fecha de Rechazo": prestamo['hpvh_fecha_autorizacion'] if "aprobada" in prestamo['hpvh_estatus'] else None
    }

    informacion_list = [
        "Vehículo Solicitado",
        "Placa",
        "Solicitante",
        "Fecha de Solicitud",
        "Fecha Prevista de Salida",
        "Fecha Prevista de Devolución",
        "Motivo de Solicitud",
        "Ruta Prevista",
        "Tiempo Estimado de Uso",
        "Estatus",
        "Razón de Rechazo",
        "Rechazada por",
        "Aprobada por",
        "Fecha de Aprobación",
        "Fecha de Rechazo"
    ]

    conductor_dict = {
        "Nombre": prestamo['hpvh_conductor'],
        "C.I.": prestamo['hpvh_ci_conductor'],
        "Nº Celular": prestamo['hpvh_nro_celular_conductor'],
        "Nº Licencia de Conducir": prestamo['hpvh_nro_licencia_conductor'],
        "Certificado Médico": prestamo['hpvh_certificado_medico'],
        "Certificado Psicológico": prestamo['hpvh_certificado_psicologico']
    }

    conductor_list = [
        "Nombre",
        "C.I.",
        "Nº Celular",
        "Nº Licencia de Conducir",
        "Certificado Médico",
        "Certificado Psicológico"
    ]

    usuario_dict = {
        "Nombre": prestamo['hpvh_usuario'],
        "C.I.": prestamo['hpvh_ci_usuario'],
        "Nº Celular": prestamo['hpvh_nro_celular_usuario']
    }

    usuario_list = [
        "Nombre",
        "C.I.",
        "Nº Celular"
    ]

    try:
        usuario_salida = db(db.auth_user.id == prestamo['hpvh_autoriza_salida']).select().first()
        nombre_salida = "%s %s" % (usuario_salida.first_name, usuario_salida.last_name)
    except:
        nombre_salida = None

    info_salida_dict = {
        "Autorizado por": nombre_salida,
        "Kilometraje": prestamo['hpvh_km_salida'],
        "Nivel de gasolina": prestamo['hpvh_gasolina_salida'],
        "Nivel de aceite de motor": prestamo['hpvh_aceite_motor_salida'],
        "Nivel de aceite de caja": prestamo['hpvh_aceite_caja_salida'],
        "Nivel de agua/refrigerante": prestamo['hpvh_agua_ref_salida'],
        "Batería": prestamo['hpvh_bateria_salida'],
        "Estado de los Cauchos": prestamo['hpvh_cauchos_salida'],
        "Caucho de Repuesto": prestamo['hpvh_caucho_repuesto_salida'],
        "Herramientas de Seguridad": prestamo['hpvh_herramientas_seguridad_salida'],
        "Estado de la Latonería": prestamo['hpvh_latoneria_salida'],
        "Estado de la Pintura": prestamo['hpvh_pintura_salida'],
        "Estado de los Accesorios": prestamo['hpvh_accesorios_salida'],
        "Cartel de Uso Oficial": prestamo['hpvh_cartel_uso_oficial_salida'],
        "Listado de fluidos y especificaciones de repuestos frecuentes utilizados": prestamo['hpvh_listado_fluidos_salida'],
        "Carnet de Circulación del Vehículo": __get_estado_documento_vh(prestamo['hpvh_carnet_circulacion'], "salida"),
        "Póliza de Seguridad del Vehículo": __get_estado_documento_vh(prestamo['hpvh_poliza_seguridad'], "salida"),
        "Lista de Teléfonos de Emerg.": __get_estado_documento_vh(prestamo['hpvh_lista_telf_emerg'], "salida"),
        "Manual de Uso del Vehículo": __get_estado_documento_vh(prestamo['hpvh_manual_uso_vehic'], "salida")
    }

    try:
        usuario_devolucion = db(db.auth_user.id == prestamo['hpvh_autoriza_devolucion']).select().first()
        nombre_devolucion = "%s %s" % (usuario_devolucion.first_name, usuario_devolucion.last_name)
    except:
        nombre_devolucion = None

    info_devolucion_dict = {
        "Autorizado por": nombre_devolucion,
        "Kilometraje": prestamo['hpvh_km_devolucion'],
        "Nivel de gasolina": prestamo['hpvh_gasolina_devolucion'],
        "Nivel de aceite de motor": prestamo['hpvh_aceite_motor_devolucion'],
        "Nivel de aceite de caja": prestamo['hpvh_aceite_caja_devolucion'],
        "Nivel de agua/refrigerante": prestamo['hpvh_agua_ref_devolucion'],
        "Batería": prestamo['hpvh_bateria_devolucion'],
        "Estado de los Cauchos": prestamo['hpvh_cauchos_devolucion'],
        "Caucho de Repuesto": prestamo['hpvh_caucho_repuesto_devolucion'],
        "Herramientas de Seguridad": prestamo['hpvh_herramientas_seguridad_devolucion'],
        "Estado de la Latonería": prestamo['hpvh_latoneria_devolucion'],
        "Estado de la Pintura": prestamo['hpvh_pintura_devolucion'],
        "Estado de los Accesorios": prestamo['hpvh_accesorios_devolucion'],
        "Cartel de Uso Oficial": prestamo['hpvh_cartel_uso_oficial_devolucion'],
        "Listado de fluidos y especificaciones de repuestos frecuentes utilizados": prestamo['hpvh_listado_fluidos_devolucion'],
        "Carnet de Circulación del Vehículo": __get_estado_documento_vh(prestamo['hpvh_carnet_circulacion'], "devolucion"),
        "Póliza de Seguridad del Vehículo": __get_estado_documento_vh(prestamo['hpvh_poliza_seguridad'], "devolucion"),
        "Lista de Teléfonos de Emerg.": __get_estado_documento_vh(prestamo['hpvh_lista_telf_emerg'], "devolucion"),
        "Manual de Uso del Vehículo": __get_estado_documento_vh(prestamo['hpvh_manual_uso_vehic'], "devolucion")
    }

    info_transito_list = [
        "Autorizado por",
        "Kilometraje",
        "Nivel de gasolina",
        "Nivel de aceite de motor",
        "Nivel de aceite de caja",
        "Nivel de agua/refrigerante",
        "Batería",
        "Estado de los Cauchos",
        "Caucho de Repuesto",
        "Herramientas de Seguridad",
        "Estado de la Latonería",
        "Estado de la Pintura",
        "Estado de los Accesorios",
        "Cartel de Uso Oficial",
        "Listado de fluidos y especificaciones de repuestos frecuentes utilizados",
        "Carnet de Circulación del Vehículo",
        "Póliza de Seguridad del Vehículo",
        "Lista de Teléfonos de Emerg.",
        "Manual de Uso del Vehículo"
    ]

    return dict(
        vehiculo=vehiculo,
        prestamo=prestamo,
        informacion_dict=informacion_dict,
        informacion_list=informacion_list,
        conductor_dict=conductor_dict,
        conductor_list=conductor_list,
        usuario_dict=usuario_dict,
        usuario_list=usuario_list,
        info_transito_list=info_transito_list,
        info_salida_dict=info_salida_dict,
        info_devolucion_dict=info_devolucion_dict,
        esta_autorizado=esta_autorizado
    )

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles_mantenimiento_vh():
    mant_id = int(request.vars['mantenimiento'])

    # Obtenemos datos de mantenimiento
    try:
        mantenimiento = db(db.historial_mantenimiento_vh.id == mant_id).select()[0]
    except IndexError:
        return "ID de mantenimiento erróneo"
    
    # Obtenemos datos de vehículo asociado
    try:
        vehiculo = db(db.vehiculo.id == mantenimiento.hmvh_vh_id).select()[0]
    except IndexError:
        return "El vehiculo asociado al mantenimiento no existe."
    
    if request.vars.edicion:
        resultado = __registrar_mantenimiento_vh(
            vehiculo=vehiculo['id'],
            fecha_solicitud=request.vars.fecha_solicitud_mant,
            nro_registro=request.vars.nro_registro,
            proveedor=request.vars.proveedor,
            contacto=request.vars.persona_contacto,
            telf_contacto=request.vars.telf_contacto,
            motivo=request.vars.motivo,
            tipo=request.vars.tipo_mant,
            descripcion=request.vars.descripcion,
            fecha_inicio=request.vars.fecha_inicio_mant,
            fecha_fin=request.vars.fecha_culminacion_mant,
            piezas_reparadas=request.vars.piezas_reparadas,
            piezas_sustituidas=request.vars.piezas_sustituidas,
            accion=request.vars.accion,
            observaciones=request.vars.observaciones,
            modificacion=True,
            mant_id=mant_id
        )

        request.vars.mantenimiento = None
        mantenimiento = db(db.historial_mantenimiento_vh.id == mant_id).select()[0]

        if resultado:
            session.flash = "Se ha editado el registro de mantenimiento de O/S %s para el vehiculo." % request.vars.nro_registro
            return redirect(URL('detalles_mantenimiento_vh', vars=dict(mantenimiento=mant_id)))

    # Obtenemos nivel de autorización del usuario
    esta_autorizado = (auth.user.id == vehiculo['vh_responsable']) or (auth.user.id == vehiculo['vh_custodio']) or (auth.user.id == 1)

    # Obtenemos datos de la solicitud
    datos_solicitud_list = [
        "Fecha de Solicitud",
        "Nº Registro (O/S)",
        "Proveedor",
        "Persona de Contacto",
        "Telf. de Contacto",
        "Tipo de Servicio",
        "Motivo"
    ]

    datos_solicitud_dict = {
        "Fecha de Solicitud": mantenimiento['hmvh_fecha_solicitud'].strftime("%d/%m/%y"),
        "Nº Registro (O/S)": mantenimiento['hmvh_nro_registro'],
        "Proveedor": mantenimiento['hmvh_proveedor'],
        "Persona de Contacto": mantenimiento['hmvh_contacto'],
        "Telf. de Contacto": mantenimiento['hmvh_telf_contacto'],
        "Tipo de Servicio": mantenimiento['hmvh_tipo'],
        "Motivo": mantenimiento['hmvh_motivo']
    }

    # Obtenemos datos del servicio
    datos_servicio_list = [
        "Iniciado",
        "Culminado",
        "Fecha de Inicio",
        "Fecha de Culminación",
        "Descripción",
        "Acción",
        "Piezas o partes reparadas",
        "Piezas o partes sustituidas",
        "Observaciones"
    ]

    datos_servicio_dict = {
        "Iniciado": "Sí" if mantenimiento['hmvh_fecha_inicio'] is not None else "No",
        "Culminado": ("Sí" if mantenimiento['hmvh_fecha_fin'] is not None else "No") if mantenimiento['hmvh_fecha_inicio'] is not None else None,
        "Fecha de Inicio": None if mantenimiento['hmvh_fecha_inicio'] is None else mantenimiento['hmvh_fecha_inicio'].strftime("%d/%m/%y"),
        "Fecha de Culminación": None if mantenimiento['hmvh_fecha_fin'] is None else mantenimiento['hmvh_fecha_fin'].strftime("%d/%m/%y"),
        "Descripción": mantenimiento['hmvh_descripcion'],
        "Acción": mantenimiento['hmvh_accion'],
        "Piezas o partes reparadas": mantenimiento['hmvh_piezas_reparadas'],
        "Piezas o partes sustituidas": mantenimiento['hmvh_piezas_sustituidas'],
        "Observaciones del Servicio": mantenimiento['hmvh_observaciones']
    }

    return dict(
        vehiculo=vehiculo,
        mantenimiento=mantenimiento,
        esta_autorizado=esta_autorizado,
        datos_solicitud_list=datos_solicitud_list,
        datos_solicitud_dict=datos_solicitud_dict,
        datos_servicio_list=datos_servicio_list,
        datos_servicio_dict=datos_servicio_dict
    )

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles_vehiculo():
    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    vh = request.vars['vh']

    cod_localizacion = {
        'Sartenejas': 150301,
        'Litoral': 240107
    }

    localizacion = {
        'Sartenejas': 'Edo Miranda, Municipio Baruta, Parroquia Baruta',
        'Litoral': 'Edo Vargas, Municipio Vargas, Parroquia Macuto'
    }

    try:
        vehi = db(db.vehiculo.vh_placa == vh).select()[0]
    except IndexError:
        # PENDIENTE: Transformar esto en una vista de control
        # de errores
        return "El vehiculo solicitado no existe."

    nombre_dependencia = db(db.dependencias.id == vehi['vh_dependencia']).select().first().nombre
    mantenimiento = __get_mantenimiento_vh(vehi['id'])
    prestamos = __get_prestamos_vh(vehi['id'])

    # Si recibimos un registro de mantenimiento
    if request.vars.mantenimiento:
        resultado = __registrar_mantenimiento_vh(
            vehiculo=vehi['id'],
            fecha_solicitud=request.vars.fecha_solicitud_mant,
            nro_registro=request.vars.nro_registro,
            proveedor=request.vars.proveedor,
            contacto=request.vars.persona_contacto,
            telf_contacto=request.vars.telf_contacto,
            motivo=request.vars.motivo,
            tipo=request.vars.tipo_mant,
            descripcion=request.vars.descripcion,
            fecha_inicio=request.vars.fecha_inicio_mant,
            fecha_fin=request.vars.fecha_culminacion_mant,
            piezas_reparadas=request.vars.piezas_reparadas,
            piezas_sustituidas=request.vars.piezas_sustituidas,
            accion=request.vars.accion,
            observaciones=request.vars.observaciones
        )

        request.vars.mantenimiento = None

        if resultado:
            session.flash = "Se ha agregado un registro de mantenimiento de O/S %s para el vehiculo." % request.vars.nro_registro
            return redirect(URL('detalles_vehiculo', vars=dict(vh=vh)))

    # Si recibimos una solicitud de préstamo
    if request.vars.prestamo:
        resultado = __solicitar_prestamo_vh(
           solicitante=auth.user.id,
            vehiculo=vehi['id'],
            fecha_solicitud=datetime.now(),
            fecha_prevista_salida=request.vars.fecha_prevista_salida,
            fecha_prevista_devolucion=request.vars.fecha_prevista_devolucion,
            tiempo_previsto=int(request.vars.tiempo_previsto),
            tiempo_previsto_md=request.vars.tiempo_previsto_md,
            ruta=request.vars.ruta,
            motivo_prestamo=request.vars.motivo_prestamo,
            nombre_conductor=request.vars.nombre_conductor,
            ci_conductor=request.vars.ci_conductor,
            nro_conductor=request.vars.nro_conductor,
            licencia_conducir=request.vars.licencia_conducir,
            certificado_medico=request.vars.certificado_medico,
            certificado_psicologico=request.vars.certificado_psicologico,
            nombre_usuario=request.vars.nombre_usuario,
            ci_usuario=request.vars.ci_usuario,
            nro_usuario=request.vars.nro_usuario
        )

        request.vars.modificacion = None
        if resultado:
            session.flash = "Se ha agregado una solicitud de préstamo para el vehiculo."
        return redirect(URL('prestamos'))

    # Si mandamos eliminación
    if request.vars.eliminacion:
        # Si ya hay una eliminación pendiente, la rechazamos
        if vehi['vh_eliminar'] == 0:
            session.flash = "Ya se está esperando respuesta para la eliminación del vehículo de placa %s por motivo: %s." % (vh, vehi['vh_desc_eliminar'])
        # Si no hay eliminaciones pendientes, la ponemos en cola
        else:
            db(db.vehiculo.vh_placa == vh).update(
                vh_eliminar=0,
                vh_desc_eliminar=request.vars.descripcion_eliminacion
            )

            db.bitacora_general.insert(
                f_accion="[inventarios] Solicitada eliminación del vehiculo de placa {} de la dependencia {}.".format(vehi['vh_placa'], nombre_dependencia)
            )
            session.flash = "Se ha solicitado la eliminación del vehículo de placa %s." % vh
        redirect(URL('detalles_vehiculo', vars=dict(vh=vh)))

    # Si se elimina
    if request.vars.si:
        db.bitacora_general.insert(
            f_accion="[inventarios] Eliminado el vehiculo de placa {} de la dependencia {}".format(vehi['vh_placa'], nombre_dependencia)
        )
        db(db.vehiculo.vh_placa == vehi['vh_placa']).select().first().update_record(vh_eliminar=1)
        session.flash = "El vehiculo ha sido eliminado"
        redirect(URL('validaciones'))

    # Si no se elimina
    if request.vars.no:
        db.bitacora_general.insert(
            f_accion="[inventarios] Rechazada eliminación del vehiculo de placa {} de la dependencia {}".format(vehi['vh_placa'], nombre_dependencia)
        )
        db(db.vehiculo.vh_placa == vehi['vh_placa']).select().first().update_record(vh_eliminar=2)
        session.flash = "El vehiculo no ha sido eliminado."
        redirect(URL('validaciones'))

    # Si se solicita la modificación
    if request.vars.modificacion:
        dependencia_escogida = db(db.dependencias.id == vehi['vh_dependencia']).select()[0]

        if dependencia_escogida.id_sede == 1:
            sede_verbosa = "Sartenejas"
        else:
            sede_verbosa = "Litoral"

        resultado = __agregar_modificar_vehiculo(
            id_vh=vehi['id'],
            marca=request.vars.marca if request.vars.marca != "Otro" else "Otro: " + request.vars.marca2,
            modelo=request.vars.modelo,
            ano=int(request.vars.ano),
            serial_motor=request.vars.serialM,
            serial_carroceria=request.vars.serialC,
            serial_chasis=request.vars.serialCh,
            placa=request.vars.placa,
            intt=request.vars.intt,
            observaciones=request.vars.observaciones,
            lugar_pernocta=request.vars.pernocta,
            color=request.vars.color,
            clase=request.vars.clase,
            tipo=request.vars.tipo if request.vars.tipo != "Otros aparatos para circular" else "Otros aparatos para circular: " + request.vars.tipo2,
            clasificacion=request.vars.clasificacion if request.vars.clasificacion != "Emergencia" else "Emergencia: " + requesr.vars.clasificacion2,
            uso=request.vars.uso,
            servicio=request.vars.servicio,
            dependencia=vehi['vh_dependencia'],
            tara=float(request.vars.tara),
            tara_md=request.vars.tara_md,
            nro_puestos=int(request.vars.nro_puestos),
            nro_ejes=0 if not request.vars.nro_ejes else int(request.vars.nro_ejes),
            capacidad_carga=float(request.vars.capacidad),
            capacidad_carga_md=request.vars.capacidad_carga_md,
            rines=request.vars.rines if request.vars.rines != "Otro" else "Otro: " + request.vars.rines2,
            propietario=request.vars.propietario,
            responsable=int(request.vars.responsable),
            telf_responsable=request.vars.telf_responsable,
            extension_responsable=request.vars.extension_responsable,
            custodio=int(request.vars.custodio),
            telf_custodio=request.vars.telf_custodio,
            extension_custodio=request.vars.extension_custodio,
            sudebip_localizacion=localizacion[sede_verbosa],
            sudebip_codigo_localizacion=cod_localizacion[sede_verbosa],
            sudebip_categoria="15000-0000 - Equipos de transporte, tracción y elevación",
            sudebip_subcategoria=request.vars.sudebip_subcategoria,
            sudebip_categoria_especifica=request.vars.sudebip_categoria_especifica,
            fecha_adquisicion=request.vars.fecha_factura if request.vars.origen == "Compra" else request.vars.fecha_oficio,
            origen=request.vars.origen,
            nro_adquisicion=request.vars.nro_factura if request.vars.origen == "Compra" else request.vars.nro_oficio,
            proveedor=request.vars.proveedor,
            proveedor_rif=request.vars.proveedor_rif,
            num=request.vars.num,
            user=user,
            ubicacion_custodio=request.vars.ubicacion_custodio,
            donante=request.vars.donante,
            contacto_donante=request.vars.contacto_donante,
            motivo=request.vars.motivo,
            oculto=0
        )

        request.vars.modificacion = None
        if resultado:
            session.flash = "Se ha agregado una solicitud de modificacion para el vehiculo."
        redirect(URL('validaciones'))

    if request.vars.ocultar:
        if vehi['vh_oculto'] == 1:
            db(db.vehiculo.id == vehi['id']).select().first().update_record(vh_oculto=0)
            response.flash = "Ahora el vehiculo de placa " + str(vehi['vh_placa']) + " se encuentra visible en las consultas."
        else:
            db(db.vehiculo.id == vehi['id']).select().first().update_record(vh_oculto=1)
            response.flash = "Ahora el vehiculo de placa " + str(vehi['vh_placa']) + " se encuentra oculto en las consultas."
        request.vars.ocultar = None
        vehi = db(db.vehiculo.vh_placa == vh).select()[0]

    caracteristicas_list = [
        'Nº Bien Mueble',
        'Marca',
        'Modelo / Código',
        'Año',
        'Color',
        'Placa',
        'Propietario',
        'Serial de carroceria',
        'Serial de motor',
        'Serial de chasis',
        'Clase',
        'Tipo',
        'Clasificación',
        'Uso',
        'Servicio',
        'Nº de Puestos',
        'Nº de Ejes',
        'Tara',
        'Capacidad de carga',
        'Nº de Autorización INTT',
        'Rines',
        'Estatus',
        'Visibilidad',
        'Observaciones',
    ]

    caracteristicas_dict = {
        'Nº Bien Mueble': vehi['vh_num'],
        'Marca': vehi['vh_marca'],
        'Modelo / Código': vehi['vh_modelo'],
        'Año': vehi['vh_ano'],
        'Color': vehi['vh_color'],
        'Placa': vehi['vh_placa'].upper(),
        'Propietario': vehi['vh_propietario'],
        'Serial de carroceria': vehi['vh_serial_carroceria'],
        'Serial de motor': vehi['vh_serial_motor'],
        'Serial de chasis': vehi['vh_serial_chasis'],
        'Clase': vehi['vh_clase'],
        'Tipo': vehi['vh_tipo'],
        'Clasificación': vehi['vh_clasificacion'],
        'Uso': vehi['vh_uso'],
        'Servicio': vehi['vh_servicio'],
        'Nº de Puestos': vehi['vh_nro_puestos'],
        'Nº de Ejes': vehi['vh_nro_ejes'],
        'Tara': str(vehi['vh_tara']) + " " + vehi['vh_tara_md'],
        'Capacidad de carga': str(vehi['vh_capacidad_carga']) + " " + vehi['vh_capacidad_carga_md'],
        'Nº de Autorización INTT': vehi['vh_intt'],
        'Rines': vehi['vh_rines'],
        'Estatus': vehi['vh_estatus'],
        'Visibilidad': None if vehi['vh_oculto'] == 0 else "Oculto",
        'Observaciones': vehi['vh_observaciones'],
    }

    dict_categorias = __obtener_categorias()
    dict_clasificaciones = __obtener_clasificaciones()
    depend = db(db.dependencias.id == vehi['vh_dependencia']).select().first()
    sede_id = int(depend.id_sede)

    esta_autorizado = (auth.user.id == vehi['vh_responsable']) or (auth.user.id == vehi['vh_custodio']) or (auth.user.id == 1)
    puede_ver_historial_mantenimiento = esta_autorizado or __es_jefe_dep_vh(auth.user.id, vehi['id'])

    # Si solo estoy cargando la vista
    return dict(
        vehiculo=vehi,
        mantenimiento=mantenimiento,
        caracteristicas_list=caracteristicas_list,
        caracteristicas_dict=caracteristicas_dict,
        categorias=dict_categorias,
        cod_localizacion=cod_localizacion,
        localizacion=localizacion,
        clasificaciones=dict_clasificaciones,
        sede_id=sede_id,
        historial_prestamos=prestamos,
        esta_autorizado=esta_autorizado,
        puede_ver_historial_mantenimiento=puede_ver_historial_mantenimiento
    )

# Muestra el inventario de acuerdo al cargo del usuario y la dependencia que tiene
# a cargo
@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def bienes_muebles():
# Inicializando listas de espacios fisicos y dependencias

    # OJO: Espacios debe ser [] siempre que no se este visitando un espacio fisico
    espacios = []
    dependencias = []
    dep_nombre = ""
    dep_padre_id = ""
    dep_padre_nombre = ""

    # Lista de BM en el inventario de un espacio fisico o que componen
    # el inventario agregado de una dependencia
    inventario = []

    # Elementos que deben ser mostrados como una lista en el modal
    # de agregar BM
    material_pred = []
    color = []
    unidad_med = []
    movilidad = []
    uso = []
    nombre_cat = []
    cod_localizacion = []
    localizacion = []
    nombre_espaciof = []
    unidad_adscripcion = []
    unidad_cap = []

    # Esta variable es enviada a la vista para que cuando el usuario seleccione
    # un espacio fisico, se pase por GET es_espacio = "True". No quiere decir
    # que la dependencia seleccionada sea un espacio, sino que la siguiente
    # dependencia visitada sera un espacio fisico
    es_espacio = False

    # Permite saber si actualmente se esta visitando un espacio fisico (True)
    # o una dependencia (False)
    espacio_visitado = False

    # Indica si se debe seguir mostrando la flecha para seguir retrocediendo
    retroceder = True

    es_tecnico = auth.has_membership("PERSONAL INTERNO") or auth.has_membership("TÉCNICO")
    direccion_id = __find_dep_id('DIRECCIÓN')

    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    user_dep_id = user.f_dependencia

    if auth.has_membership("PERSONAL INTERNO") or auth.has_membership("TÉCNICO"):
        # Si el tecnico ha seleccionado un espacio fisico
        if request.vars.dependencia:
            if request.vars.es_espacio == "True":
                # Evaluando la correctitud de los parametros del GET
                if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('bienes_muebles'))

                # Determinando si el usuario tiene privilegios suficientes para
                # consultar la dependencia en request.vars.dependencia
                if not __acceso_permitido(user,
                                    int(request.vars.dependencia),
                                        request.vars.es_espacio):
                    redirect(URL('bienes_muebles'))

                espacio_id = request.vars.dependencia
                espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                dep_nombre = espacio.codigo

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_id = espacio.dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre
                # Guardando la unidad de adscripcion
                dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                    ).select().first().unidad_de_adscripcion

                espacio_visitado = True

                # Busca el inventario del espacio
                inventario = __get_inventario_espacio(espacio_id)

                material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
                color = ['Amarillo', 'Azul', 'Beige', 'Blanco', 'Dorado', 'Gris', 'Madera', 'Marrón', 'Mostaza', 'Naranja',
                'Negro', 'Plateado', 'Rojo', 'Rosado', 'Verde', 'Vinotinto', 'Otro color']
                unidad_med = ['cm', 'm']
                movilidad = ['Fijo', 'Portátil']
                uso = ['Docencia', 'Investigación', 'Extensión', 'Apoyo administrativo']
                nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento',
                'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
                cod_localizacion = ['150301', '240107']
                localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
                'Edo Vargas, Municipio Vargas, Parroquia Macuto']


                # Si se esta agregando un nuevo BM, se registra en la DB
                if request.vars.nombre: # Verifico si me pasan como argumento el nombre del BM.
                    __agregar_bm(
                        request.vars.nombre,request.vars.no_bien,request.vars.no_placa,
                        request.vars.marca, request.vars.modelo, request.vars.serial,
                        request.vars.descripcion, request.vars.material, request.vars.color,
                        request.vars.calibrar, request.vars.fecha_calibracion, request.vars.unidad,
                        request.vars.ancho, request.vars.largo, request.vars.alto,
                        request.vars.diametro, request.vars.movilidad, request.vars.tipo_uso, request.vars.estatus,
                        request.vars.nombre_cat, request.vars.subcategoria, request.vars.cod_loc, request.vars.localizacion, espacio, dep_padre_unid_ads,
                        dep_padre_id, user_id, request.vars.clasificacion)
            else:
                # Espacios a cargo del usuario user_id que pertenecen a la seccion
                # en request.vars.dependencia
                espacios = [row.espacios_fisicos for row in db(
                    (db.es_encargado.espacio_fisico == db.espacios_fisicos.id) &
                    (db.espacios_fisicos.dependencia == int(request.vars.dependencia)) &
                    (db.es_encargado.tecnico == user_id)).select()]

                espacios_ids = [e.id for e in espacios]

                dep_id = int(request.vars.dependencia)
                dep_nombre = db(db.dependencias.id == dep_id).select()[0].nombre

                dep_padre_nombre = "Secciones"

                # Se muestra el inventarios de los espacios que tiene a cargo el usuario en la
                # seccion actual
                inventario = __sumar_inventarios(espacios_ids)

                es_espacio = True

        # Si el tecnico o jefe no ha seleccionado un espacio sino que acaba de
        # entrar a la opcion de inventarios
        else:
            # Se buscan las secciones a las que pertenecen los espacios que
            # tiene a cargo el usuario
            espacios_a_cargo = db(
                (db.es_encargado.tecnico == user_id) &
                (db.espacios_fisicos.id == db.es_encargado.espacio_fisico)
                                 ).select()

            secciones_ids = {e.espacios_fisicos.dependencia for e in espacios_a_cargo}

            dependencias = map(lambda x: db(db.dependencias.id == x).select()[0],
                               secciones_ids)

            dep_nombre = "Secciones"

            espacios_ids = [e.espacios_fisicos.id for e in espacios_a_cargo]

            inventario = __sumar_inventarios(espacios_ids)

    elif auth.has_membership("JEFE DE SECCIÓN") or auth.has_membership("COORDINADOR"):
        # Si el jefe de seccion ha seleccionado un espacio fisico
        if request.vars.es_espacio == 'True':
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user,
                                int(request.vars.dependencia),
                                    request.vars.es_espacio):
                redirect(URL('bienes_muebles'))

            # Evaluando la correctitud de los parametros del GET
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('bienes_muebles'))


            espacio_id = request.vars.dependencia
            espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
            dep_nombre = espacio.codigo

            # Guardando el ID y nombre de la dependencia padre para el link
            # de navegacion de retorno
            dep_padre_id = espacio.dependencia
            dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                ).select().first().nombre
            # Guardando la unidad de adscripcion
            dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                ).select().first().unidad_de_adscripcion

            espacio_visitado = True

            # Busca el inventario del espacio
            inventario = __get_inventario_espacio(espacio_id)

            material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
            color = ['Amarillo', 'Azul', 'Beige', 'Blanco', 'Dorado', 'Gris', 'Madera', 'Marrón', 'Mostaza', 'Naranja',
            'Negro', 'Plateado', 'Rojo', 'Rosado', 'Verde', 'Vinotinto', 'Otro color']
            unidad_med = ['cm', 'm']
            movilidad = ['Fijo', 'Portátil']
            uso = ['Docencia', 'Investigación', 'Extensión', 'Apoyo administrativo']
            nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento',
            'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
            cod_localizacion = ['150301', '240107']
            localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
            'Edo Vargas, Municipio Vargas, Parroquia Macuto']

            # Si se esta agregando un nuevo BM, se registra en la DB
            if request.vars.nombre: # Verifico si me pasan como argumento el nombre del BM.
                __agregar_bm(
                    request.vars.nombre,request.vars.no_bien,request.vars.no_placa,
                    request.vars.marca, request.vars.modelo, request.vars.serial,
                    request.vars.descripcion, request.vars.material, request.vars.color,
                    request.vars.calibrar, request.vars.fecha_calibracion, request.vars.unidad,
                    request.vars.ancho, request.vars.largo, request.vars.alto,
                    request.vars.diametro, request.vars.movilidad, request.vars.tipo_uso, request.vars.estatus,
                    request.vars.nombre_cat, request.vars.subcategoria, request.vars.cod_loc, request.vars.localizacion, espacio, dep_padre_unid_ads,
                    dep_padre_id, user_id, request.vars.clasificacion)


        # Si el jefe de seccion no ha seleccionado un espacio sino que acaba de
        # regresar a la vista inicial de inventarios
        elif request.vars.es_espacio == 'False':
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                    redirect(URL('bienes_muebles'))
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user,
                                int(request.vars.dependencia),
                                    request.vars.es_espacio):
                redirect(URL('bienes_muebles'))
            espacios = list(db(
                              db.espacios_fisicos.dependencia == user_dep_id
                              ).select(db.espacios_fisicos.ALL))
            dep_nombre = db(db.dependencias.id == user_dep_id
                           ).select().first().nombre

            es_espacio = True                       
        # Si el jefe de seccion no ha seleccionado un espacio sino que acaba de
        # entrar a la vista inicial de inventarios
        else:
            espacios = list(db(
                              db.espacios_fisicos.dependencia == user_dep_id
                              ).select(db.espacios_fisicos.ALL))
            dep_nombre = db(db.dependencias.id == user_dep_id
                           ).select().first().nombre

            es_espacio = True

            # Se muestra como inventario el egregado de los inventarios que
            # pertenecen a la seccion del jefe
            inventario = __get_inventario_dep(user_dep_id)

    # Si el usuario no es tecnico, para la base de datos es indiferente su ROL
    # pues la jerarquia de dependencias esta almacenada en la misma tabla
    # con una lista de adyacencias
    else:
        # Si el usuario ha seleccionado una dependencia o un espacio fisico
        if request.vars.dependencia:

            # Evaluando la correctitud de los parametros del GET

            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user,
                                int(request.vars.dependencia),
                                    request.vars.es_espacio):
                redirect(URL('bienes_muebles'))

            if request.vars.es_espacio == "True":

                if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos)  and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('bienes_muebles'))

                # Se muestra el inventario del espacio
                espacio_id = request.vars.dependencia
                espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                dep_nombre = espacio.codigo

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_id = espacio.dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre
                # Guardando la unidad de adscripcion
                dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                    ).select().first().unidad_de_adscripcion

                espacio_visitado = True

                # Busca el inventario del espacio
                inventario = __get_inventario_espacio(espacio_id)

                material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
                color = ['Amarillo', 'Azul', 'Beige', 'Blanco', 'Dorado', 'Gris', 'Madera', 'Marrón', 'Mostaza', 'Naranja',
                'Negro', 'Plateado', 'Rojo', 'Rosado', 'Verde', 'Vinotinto', 'Otro color']
                unidad_med = ['cm', 'm']
                movilidad = ['Fijo', 'Portátil']
                uso = ['Docencia', 'Investigación', 'Extensión', 'Apoyo administrativo']
                nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento',
                'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
                cod_localizacion = ['150301', '240107']
                localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
                'Edo Vargas, Municipio Vargas, Parroquia Macuto']

                # Si se esta agregando un nuevo BM, se registra en la DB
                if request.vars.nombre: # Verifico si me pasan como argumento el nombre del BM.
                    __agregar_bm(
                        request.vars.nombre,request.vars.no_bien,request.vars.no_placa,
                        request.vars.marca, request.vars.modelo, request.vars.serial,
                        request.vars.descripcion, request.vars.material, request.vars.color,
                        request.vars.calibrar, request.vars.fecha_calibracion, request.vars.unidad,
                        request.vars.ancho, request.vars.largo, request.vars.alto,
                        request.vars.diametro, request.vars.movilidad, request.vars.tipo_uso, request.vars.estatus,
                        request.vars.nombre_cat, request.vars.subcategoria, request.vars.cod_loc, request.vars.localizacion, espacio, dep_padre_unid_ads,
                        dep_padre_id, user_id, request.vars.clasificacion)

            else:

                if not (__is_valid_id(request.vars.dependencia, db.dependencias)  and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('bienes_muebles'))

                # Se muestran las dependencias que componen a esta dependencia padre
                # y se lista el inventario agregado
                dep_id = request.vars.dependencia
                dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre
                dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                      ).select(db.dependencias.ALL))
                # Si la lista de dependencias es vacia, entonces la dependencia no
                # tiene otras dependencias por debajo (podria tener espacios fisicos
                # o estar vacia)
                if dependencias:
                    # Buscando espacios fisicos que apunten a la dependencia escogida
                    espacios = list(db(db.espacios_fisicos.dependencia == dep_id
                                      ).select(db.espacios_fisicos.ALL))
                    es_espacio = True

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_id = db(db.dependencias.id == request.vars.dependencia
                                 ).select().first().unidad_de_adscripcion
                # Si dep_padre_id es None, se ha llegado al tope de la jerarquia
                # y no hay un padre de este nodo
                if dep_padre_id:
                    dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                         ).select().first().nombre
                # Se muestra como inventario el egregado de los inventarios que
                # pertenecen a la dependencia del usuario
                inventario = __get_inventario_dep(dep_id)

        else:
            # Dependencia a la que pertenece el usuario o que tiene a cargo
            dep_id = user.f_dependencia
            dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre

            # Se muestran las dependencias que componen a la dependencia que
            # tiene a cargo el usuario y el inventario agregado de esta
            dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                  ).select(db.dependencias.ALL))

            # Se muestra como inventario el egregado de los inventarios que
            # pertenecen a la dependencia del usuario
            inventario = __get_inventario_dep(dep_id)

    return dict(dep_nombre=dep_nombre,
                dependencias=dependencias,
                espacios=espacios,
                es_espacio=es_espacio,
                espacio_visitado=espacio_visitado,
                dep_padre_id=dep_padre_id,
                dep_padre_nombre=dep_padre_nombre,
                direccion_id=direccion_id,
                es_tecnico=es_tecnico,
                inventario=inventario,
                retroceder=retroceder,
                material_pred = material_pred,
                color_list = color,
                unidad_med = unidad_med,
                movilidad_list = movilidad,
                uso_list = uso,
                nombre_cat = nombre_cat,
                cod_localizacion = cod_localizacion,
                localizacion = localizacion,
                )

# Muestra el inventario de acuerdo al cargo del usuario y la dependencia que tiene
# a cargo
@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def material_lab():
# Inicializando listas de espacios fisicos y dependencias

    # OJO: Espacios debe ser [] siempre que no se este visitando un espacio fisico
    espacios = []
    dependencias = []
    dep_nombre = ""
    dep_padre_id = ""
    dep_padre_nombre = ""

    # Lista de BM en el inventario de un espacio fisico o que componen
    # el inventario agregado de una dependencia
    inventario = []

    # Elementos que deben ser mostrados como una lista en el modal
    # de agregar BM
    material_pred = []
    color = []
    unidad_med = []
    movilidad = []
    uso = []
    nombre_cat = []
    cod_localizacion = []
    localizacion = []
    nombre_espaciof = []
    unidad_adscripcion = []
    unidad_cap = []
    presentacion = []

    # Esta variable es enviada a la vista para que cuando el usuario seleccione
    # un espacio fisico, se pase por GET es_espacio = "True". No quiere decir
    # que la dependencia seleccionada sea un espacio, sino que la siguiente
    # dependencia visitada sera un espacio fisico
    es_espacio = False

    # Permite saber si actualmente se esta visitando un espacio fisico (True)
    # o una dependencia (False)
    espacio_visitado = False

    # Indica si se debe seguir mostrando la flecha para seguir retrocediendo
    retroceder = True

    es_tecnico = auth.has_membership("PERSONAL INTERNO") or auth.has_membership("TÉCNICO")
    direccion_id = __find_dep_id('DIRECCIÓN')

    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    user_dep_id = user.f_dependencia

    if auth.has_membership("PERSONAL INTERNO") or auth.has_membership("TÉCNICO"):
        # Si el tecnico ha seleccionado un espacio fisico
        if request.vars.dependencia:
            if request.vars.es_espacio == "True":
                # Evaluando la correctitud de los parametros del GET
                if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('material_lab'))

                # Determinando si el usuario tiene privilegios suficientes para
                # consultar la dependencia en request.vars.dependencia
                if not __acceso_permitido(user,
                                    int(request.vars.dependencia),
                                        request.vars.es_espacio):
                    redirect(URL('material_lab'))

                espacio_id = request.vars.dependencia
                espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                dep_nombre = espacio.codigo

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_id = espacio.dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre
                # Guardando la unidad de adscripcion
                dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                    ).select().first().unidad_de_adscripcion

                espacio_visitado = True

                # Busca el inventario del espacio
                inventario = __get_inventario_materiales_espacio(espacio_id)

                material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
                color = ['Amarillo', 'Azul', 'Beige', 'Blanco', 'Dorado', 'Gris', 'Madera', 'Marrón', 'Mostaza', 'Naranja',
                'Negro', 'Plateado', 'Rojo', 'Rosado', 'Verde', 'Vinotinto', 'Otro color']
                unidad_med = ['cm', 'm']
                movilidad = ['Fijo', 'Portátil']
                uso = ['Docencia', 'Investigación', 'Extensión', 'Apoyo administrativo']
                nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento',
                'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
                cod_localizacion = ['150301', '240107']
                localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
                'Edo Vargas, Municipio Vargas, Parroquia Macuto']
                unidad_cap = ['m³', 'l', 'ml', 'μl', 'kg', 'g', 'mg', 'μg', 'galón', 'oz', 'cup', 'lb']
                presentacion=["Caja", "Paquete", "Unidad", "Otro"]

                # Si se esta agregando un nuevo BM, se registra en la DB
                if request.vars.nombre_mat: # Verifico si me pasan como argumento el nombre del BM.
                    __agregar_material(
                        request.vars.nombre_mat,
                        request.vars.marca_mat, request.vars.modelo_mat, request.vars.cantidad_mat, espacio, request.vars.ubicacion_int ,
                        request.vars.descripcion_mat, request.vars.aforado, request.vars.calibracion_mat,
                        request.vars.capacidad, request.vars.unidad_cap,
                         request.vars.unidad_mat, 
                        request.vars.ancho_mat, request.vars.largo_mat, request.vars.alto_mat,
                        request.vars.diametro_mat, request.vars.material_mat, request.vars.material_sec, request.vars.presentacion,
                        request.vars.unidades, request.vars.total_mat, dep_padre_unid_ads,
                        dep_padre_id, user_id, request.vars.clasificacion)
            else:
                # Espacios a cargo del usuario user_id que pertenecen a la seccion
                # en request.vars.dependencia
                espacios = [row.espacios_fisicos for row in db(
                    (db.es_encargado.espacio_fisico == db.espacios_fisicos.id) &
                    (db.espacios_fisicos.dependencia == int(request.vars.dependencia)) &
                    (db.es_encargado.tecnico == user_id)).select()]

                espacios_ids = [e.id for e in espacios]

                dep_id = int(request.vars.dependencia)
                dep_nombre = db(db.dependencias.id == dep_id).select()[0].nombre

                dep_padre_nombre = "Secciones"

                # Se muestra el inventarios de los espacios que tiene a cargo el usuario en la
                # seccion actual
                inventario = __sumar_inventarios_materiales(espacios_ids)

                es_espacio = True

        # Si el tecnico o jefe no ha seleccionado un espacio sino que acaba de
        # entrar a la opcion de inventarios
        else:
            # Se buscan las secciones a las que pertenecen los espacios que
            # tiene a cargo el usuario
            espacios_a_cargo = db(
                (db.es_encargado.tecnico == user_id) &
                (db.espacios_fisicos.id == db.es_encargado.espacio_fisico)
                                 ).select()

            secciones_ids = {e.espacios_fisicos.dependencia for e in espacios_a_cargo}

            dependencias = map(lambda x: db(db.dependencias.id == x).select()[0],
                               secciones_ids)

            dep_nombre = "Secciones"

            espacios_ids = [e.espacios_fisicos.id for e in espacios_a_cargo]

            inventario = __sumar_inventarios_materiales(espacios_ids)

    elif auth.has_membership("JEFE DE SECCIÓN") or auth.has_membership("COORDINADOR"):
        # Si el jefe de seccion ha seleccionado un espacio fisico
        if request.vars.es_espacio == 'True':
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user,
                                int(request.vars.dependencia),
                                    request.vars.es_espacio):
                redirect(URL('bienes_muebles'))

            # Evaluando la correctitud de los parametros del GET
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('bienes_muebles'))


            espacio_id = request.vars.dependencia
            espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
            dep_nombre = espacio.codigo

            # Guardando el ID y nombre de la dependencia padre para el link
            # de navegacion de retorno
            dep_padre_id = espacio.dependencia
            dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                ).select().first().nombre
            # Guardando la unidad de adscripcion
            dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                ).select().first().unidad_de_adscripcion

            espacio_visitado = True

            # Busca el inventario del espacio
            inventario = __get_inventario_materiales_espacio(espacio_id)

            material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
            color = ['Amarillo', 'Azul', 'Beige', 'Blanco', 'Dorado', 'Gris', 'Madera', 'Marrón', 'Mostaza', 'Naranja',
            'Negro', 'Plateado', 'Rojo', 'Rosado', 'Verde', 'Vinotinto', 'Otro color']
            unidad_med = ['cm', 'm']
            movilidad = ['Fijo', 'Portátil']
            uso = ['Docencia', 'Investigación', 'Extensión', 'Apoyo administrativo']
            nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento',
            'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
            cod_localizacion = ['150301', '240107']
            localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
            'Edo Vargas, Municipio Vargas, Parroquia Macuto']
            unidad_cap = ['m³', 'l', 'ml', 'μl', 'kg', 'g', 'mg', 'μg', 'galón', 'oz', 'cup', 'lb']
            presentacion=["Caja", "Paquete", "Unidad", "Otro"]

            # Si se esta agregando un nuevo BM, se registra en la DB
            if request.vars.nombre_mat: # Verifico si me pasan como argumento el nombre del BM.
                __agregar_material(
                    request.vars.nombre_mat,
                    request.vars.marca_mat, request.vars.modelo_mat, request.vars.cantidad_mat, espacio, request.vars.ubicacion_int ,
                    request.vars.descripcion_mat, request.vars.aforado, request.vars.calibracion_mat,
                    request.vars.capacidad, request.vars.unidad_cap,
                        request.vars.unidad_mat, 
                    request.vars.ancho_mat, request.vars.largo_mat, request.vars.alto_mat,
                    request.vars.diametro_mat, request.vars.material_mat, request.vars.material_sec, request.vars.presentacion,
                    request.vars.unidades, request.vars.total_mat, dep_padre_unid_ads,
                    dep_padre_id, user_id, request.vars.clasificacion)


        # Si el jefe de seccion no ha seleccionado un espacio sino que acaba de
        # regresar a la vista inicial de inventarios
        elif request.vars.es_espacio == 'False':
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                    redirect(URL('material_lab'))
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user,
                                int(request.vars.dependencia),
                                    request.vars.es_espacio):
                redirect(URL('material_lab'))
            espacios = list(db(
                              db.espacios_fisicos.dependencia == user_dep_id
                              ).select(db.espacios_fisicos.ALL))
            dep_nombre = db(db.dependencias.id == user_dep_id
                           ).select().first().nombre

            es_espacio = True                       
        # Si el jefe de seccion no ha seleccionado un espacio sino que acaba de
        # entrar a la vista inicial de inventarios
        else:
            espacios = list(db(
                              db.espacios_fisicos.dependencia == user_dep_id
                              ).select(db.espacios_fisicos.ALL))
            dep_nombre = db(db.dependencias.id == user_dep_id
                           ).select().first().nombre

            es_espacio = True

            # Se muestra como inventario el egregado de los inventarios que
            # pertenecen a la seccion del jefe
            inventario = __get_inventario_materiales_dep(user_dep_id)

    # Si el usuario no es tecnico, para la base de datos es indiferente su ROL
    # pues la jerarquia de dependencias esta almacenada en la misma tabla
    # con una lista de adyacencias
    else:
        # Si el usuario ha seleccionado una dependencia o un espacio fisico
        if request.vars.dependencia:

            # Evaluando la correctitud de los parametros del GET


            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user,
                                int(request.vars.dependencia),
                                    request.vars.es_espacio):
                redirect(URL('material_lab'))

            if request.vars.es_espacio == "True":
                if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('material_lab'))
       
                # Se muestra el inventario del espacio
                espacio_id = request.vars.dependencia
                espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                dep_nombre = espacio.codigo

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_id = espacio.dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre
                # Guardando la unidad de adscripcion
                dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                    ).select().first().unidad_de_adscripcion

                espacio_visitado = True

                # Busca el inventario del espacio
                inventario = __get_inventario_materiales_espacio(espacio_id)

                material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
                color = ['Amarillo', 'Azul', 'Beige', 'Blanco', 'Dorado', 'Gris', 'Madera', 'Marrón', 'Mostaza', 'Naranja',
                'Negro', 'Plateado', 'Rojo', 'Rosado', 'Verde', 'Vinotinto', 'Otro color']
                unidad_med = ['cm', 'm']
                movilidad = ['Fijo', 'Portátil']
                uso = ['Docencia', 'Investigación', 'Extensión', 'Apoyo administrativo']
                nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento',
                'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
                cod_localizacion = ['150301', '240107']
                localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
                'Edo Vargas, Municipio Vargas, Parroquia Macuto']
                unidad_cap = ['m³', 'l', 'ml', 'μl', 'kg', 'g', 'mg', 'μg', 'galón', 'oz', 'cup', 'lb']
                presentacion=["Caja", "Paquete", "Unidad", "Otro"]

                # Si se esta agregando un nuevo BM, se registra en la DB
                if request.vars.nombre_mat: # Verifico si me pasan como argumento el nombre del BM.
                    __agregar_material(
                        request.vars.nombre_mat,
                        request.vars.marca_mat, request.vars.modelo_mat, request.vars.cantidad_mat, espacio, request.vars.ubicacion_int ,
                        request.vars.descripcion_mat, request.vars.aforado, request.vars.calibracion_mat,
                        request.vars.capacidad, request.vars.unidad_cap,
                         request.vars.unidad_mat, 
                        request.vars.ancho_mat, request.vars.largo_mat, request.vars.alto_mat,
                        request.vars.diametro_mat, request.vars.material_mat, request.vars.material_sec, request.vars.presentacion,
                        request.vars.unidades, request.vars.total_mat, dep_padre_unid_ads,
                        dep_padre_id, user_id, request.vars.clasificacion)

            else:

                if not (__is_valid_id(request.vars.dependencia, db.dependencias) and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('material_lab'))
                # Se muestran las dependencias que componen a esta dependencia padre
                # y se lista el inventario agregado
                dep_id = request.vars.dependencia
                dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre
                dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                      ).select(db.dependencias.ALL))
                # Si la lista de dependencias es vacia, entonces la dependencia no
                # tiene otras dependencias por debajo (podria tener espacios fisicos
                # o estar vacia)
                if dependencias:
                    # Buscando espacios fisicos que apunten a la dependencia escogida
                    espacios = list(db(db.espacios_fisicos.dependencia == dep_id
                                      ).select(db.espacios_fisicos.ALL))
                    es_espacio = True

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_id = db(db.dependencias.id == request.vars.dependencia
                                 ).select().first().unidad_de_adscripcion
                # Si dep_padre_id es None, se ha llegado al tope de la jerarquia
                # y no hay un padre de este nodo
                if dep_padre_id:
                    dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                         ).select().first().nombre
                # Se muestra como inventario el egregado de los inventarios que
                # pertenecen a la dependencia del usuario
                inventario = __get_inventario_materiales_dep(dep_id)

        else:
            # Dependencia a la que pertenece el usuario o que tiene a cargo
            dep_id = user.f_dependencia
            dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre

            # Se muestran las dependencias que componen a la dependencia que
            # tiene a cargo el usuario y el inventario agregado de esta
            dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                  ).select(db.dependencias.ALL))

            # Se muestra como inventario el egregado de los inventarios que
            # pertenecen a la dependencia del usuario
            inventario = __get_inventario_materiales_dep(dep_id)

    return dict(dep_nombre=dep_nombre,
                dependencias=dependencias,
                espacios=espacios,
                es_espacio=es_espacio,
                espacio_visitado=espacio_visitado,
                dep_padre_id=dep_padre_id,
                dep_padre_nombre=dep_padre_nombre,
                direccion_id=direccion_id,
                es_tecnico=es_tecnico,
                inventario=inventario,
                retroceder=retroceder,
                material_pred = material_pred,
                color_list = color,
                unidad_med = unidad_med,
                movilidad_list = movilidad,
                uso_list = uso,
                nombre_cat = nombre_cat,
                cod_localizacion = cod_localizacion,
                localizacion = localizacion,
                unidad_cap = unidad_cap,
                presentacion = presentacion
                )

# Dado el id de una dependencia, retorna una lista con el agregado de las solicitudes
# de modificacion y eliminacion para los bienes muebles que existen en los espacios
# fisicos que pertenecen a esta.
def __get_inventario_dep_validaciones(dep_id, tipo_validacion=None):

    inventario = {}

    # Obteniendo lista de espacios bajo la dependencia con id dep_id
    espacios = __get_espacios(dep_id)

    # Agrega los inventarios de los espacios en la lista "espacios"
    inventario_bm = __sumar_inventarios_bn_validacion(espacios, "_", tipo_validacion)
    inventario_materiales = __sumar_inventarios_bn_validacion(espacios, "_materiales_", tipo_validacion)
    inventario_consumibles = __sumar_inventarios_bn_validacion(espacios, "_consumibles_", tipo_validacion)
    inventario_herramientas = __sumar_inventarios_bn_validacion(espacios, "_herramientas_", tipo_validacion)
    return [inventario_bm, inventario_materiales, inventario_consumibles, inventario_herramientas]

def __sumar_inventarios_bn_validacion(espacios, tipo_material, tipo_validacion):

        inventario_temp = []
        for esp_id in espacios:
            inventario_temp += eval('__get_inventario%sespacio(esp_id)' % tipo_material)

        inventario_total = []
        if ( tipo_validacion == "eliminar" ):
            for element in inventario_temp:
                if ( tipo_material == "_"):
                    inventario_total += __get_inventario_espacio_bn_eliminar(element.bm_num)
                elif ( tipo_material == "_materiales_" or tipo_material == "_consumibles_"):
                    inventario_total += __get_inventario_espacio_materialesandconsumibles_eliminar(element.sb_nombre, element.sb_espacio)
                elif ( tipo_material == "_herramientas_" ):
                    inventario_total += __get_inventario_espacio_herramientas_eliminar(element.hr_nombre, element.hr_espacio_fisico, element.hr_ubicacion)

        else:
            for element in inventario_temp:
                if ( tipo_material == "_"):
                    inventario_total += __get_inventario_espacio_bn_validacion(element.bm_num)
                elif ( tipo_material == "_materiales_" or tipo_material == "_consumibles_"):
                    inventario_total += __get_inventario_espacio_materialesandconsumibles_validacion(element.sb_nombre, element.sb_espacio)
                elif ( tipo_material == "_herramientas_" ):
                    inventario_total += __get_inventario_espacio_herramientas_validacion(element.hr_nombre, element.hr_espacio_fisico, element.hr_ubicacion)

        return inventario_total

## Dada una herramienta la ubica en la tabla de modificaciones
def __get_inventario_espacio_herramientas_validacion(name, espacio, ubicacion):
    return db((db.modificacion_herramienta.mhr_nombre == name) & (db.modificacion_herramienta.mhr_espacio_fisico==espacio) & (db.modificacion_herramienta.mhr_ubicacion==ubicacion)).select()
## Dada una herramienta revisa si se solicito su eliminacion
def __get_inventario_espacio_herramientas_eliminar(name, espacio, ubicacion):
    herramienta = db((db.herramienta.hr_nombre == name) & (db.herramienta.hr_espacio_fisico==espacio) & (db.herramienta.hr_ubicacion==ubicacion)).select()[0]
    if ( herramienta['hr_eliminar'] == 0 ):
        return db((db.herramienta.hr_nombre == name) & (db.herramienta.hr_espacio_fisico==espacio) & (db.herramienta.hr_ubicacion==ubicacion)).select()
    return []

# Dado el id de un espacio fisico, retorna las sustancias que componen el inventario
# de ese espacio.
def __get_inventario_espacio_bn_validacion(num=None):
    return db(db.modificacion_bien_mueble.mbn_num == num).select()

# Dado el id de un espacio fisico retorna los materiales que componen
# el inventario de ese espacio.
def __get_inventario_espacio_materialesandconsumibles_validacion(nombre, espacio):
    return db((db.modificacion_sin_bn.msb_espacio == espacio) and (db.modificacion_sin_bn.msb_nombre == nombre)).select()

# Dado el id de un espacio fisico, retorna las sustancias a eliminar que componen el inventario
# de ese espacio.
def __get_inventario_espacio_bn_eliminar(num=None):
    bien = db(db.bien_mueble.bm_num == num).select()[0]
    if ( bien['bm_eliminar'] == 0 ):
        return db(db.bien_mueble.bm_num == num).select()
    return []

""" Dado el id de un espacio fisico retorna los materiales a eliminar que componen
el inventario de ese espacio. """
def __get_inventario_espacio_materialesandconsumibles_eliminar(nombre, espacio):
    element = db(db.sin_bn.sb_espacio == espacio and db.sin_bn.sb_nombre == nombre).select()[0]
    if element['sb_eliminar'] == 0:
        return db(db.sin_bn.sb_espacio == espacio and db.sin_bn.sb_nombre == nombre).select()
    return []


# Muestra las solicitudes de préstamo pendientes por dar respuesta de acuerdo
# al cargo del usuario y la dependencia que tiene a cargo, así como los vehículos
# de los cuales es responsable
@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def prestamos():

    # Pequeña función booleana para saber si un vehículo ha acabado
    # su flujo útil en préstamos
    def __flujo_listo(x):
        return "Vehículo devuelto" == x['hpvh_estatus'] or "Denegada" == x['hpvh_estatus']

    # Hallamos información del usuario
    user_id = auth.user.id

    # Hallamos las solicitudes realizadas pendientes
    solicitudes_realizadas = list(db(db.historial_prestamo_vh.hpvh_solicitante == user_id).select())
    solicitudes_realizadas.reverse()
    solicitudes_realizadas = [x for x in solicitudes_realizadas if not __flujo_listo(x)]

    # Hallamos en principio las solicitudes recibidas pendientes
    solicitudes_recibidas_aux = list(db(db.historial_prestamo_vh.id).select())
    solicitudes_recibidas_aux.reverse()

    solicitudes_recibidas = []
    for solicitud in solicitudes_recibidas_aux:
        vehiculo = db(db.vehiculo.id == solicitud['hpvh_vh_id']).select().first()
        if vehiculo['vh_responsable'] == user_id or vehiculo['vh_custodio'] == user_id:
            solicitudes_recibidas.append(solicitud)
    solicitudes_recibidas = [x for x in solicitudes_recibidas if not __flujo_listo(x)]

    # Para el superusuario, hallamos TODAS las solicitudes para la tabla especial
    todas = []
    if auth.user.id == 1:
        todas = list(db(db.historial_prestamo_vh.id).select())
        todas.reverse()
        todas = [x for x in todas if not __flujo_listo(x)]

    # Contamos las solicitudes pendientes halladas
    c = len(solicitudes_recibidas) + len(solicitudes_realizadas)
    if auth.user.id == 1:
        c = len(todas)

    return dict(
        cant_prestamos=c,
        solicitudes_recibidas=solicitudes_recibidas,
        solicitudes_realizadas=solicitudes_realizadas,
        todas_las_solicitudes=todas
    )

# Muestra las solicitudes de modificacion y eliminacion de acuerdo al cargo del
# usuario y la dependencia que tiene a cargo
@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def validaciones():
    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = auth.user.id
    try:
        user_dep_id = user.f_dependencia
    except:
        user_dep_id = 0
    inventario = [[], [], []]
    inventario_eliminar = [[], [], []]

    if auth.has_membership("JEFE DE SECCIÓN") or auth.has_membership("JEFE DE LABORATORIO") \
        or auth.has_membership("COORDINADOR") or auth.has_membership("DIRECTOR") or \
            auth.has_membership("WEBMASTER"):
        # Dependencia a la que pertenece el usuario o que tiene a cargo
        dep_id = user.f_dependencia
        dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre

        # Se muestran las dependencias que componen a la dependencia que
        # tiene a cargo el usuario y el inventario agregado de esta
        dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                ).select(db.dependencias.ALL))

        # Se muestra como inventario el egregado de los inventarios que
        # pertenecen a la dependencia del usuario
        inventario = __get_inventario_dep_validaciones(dep_id)
        inventario_eliminar = __get_inventario_dep_validaciones(dep_id, "eliminar")

    # Obtenemos todos los vehículos
    vehiculos_responsable = db(db.vehiculo.vh_responsable == user_id).select()

    vehiculos_superusuario = []
    if auth.user.id == 1:
        vehiculos_superusuario = db(db.vehiculo.id).select()


    vehics = []
    lista_ids = set()
    for vh in vehiculos_responsable:
        if vh['id'] not in lista_ids:
            lista_ids.add(vh['id'])
            vehics.append(vh)
    for vh in vehiculos_superusuario:
        if vh['id'] not in lista_ids:
            lista_ids.add(vh['id'])
            vehics.append(vh)

    vehics = list(set(vehics))

    inventario_vehiculos_aux = []
    inventario_eliminar_vehiculos_aux = []
    for auto in vehics:
        if auto['vh_eliminar'] == 1:
            continue
        if auto['vh_eliminar'] == 0:
            inventario_eliminar_vehiculos_aux.append(auto)
        if not db(
                db.modificacion_vehiculo.mvh_estado == 0 and \
                db.modificacion_vehiculo.mvh_id_vehiculo == auto.id and \
                (db.modificacion_vehiculo.mvh_responsable == user_id)).isempty() \
            or not db(
                db.modificacion_vehiculo.mvh_estado == 0 and \
                db.modificacion_vehiculo.mvh_id_vehiculo == auto.id and \
                (db.modificacion_vehiculo.mvh_custodio == user_id)).isempty():
            inventario_vehiculos_aux.append(auto)

    inventario_vehiculos = []
    inventario_eliminar_vehiculos = []

    lista_ids = set()
    for auto in inventario_vehiculos_aux:
        if auto['id'] not in lista_ids:
            lista_ids.add(auto['id'])
            inventario_vehiculos.append(auto)

    lista_ids = set()
    for auto in inventario_eliminar_vehiculos_aux:
        if auto['id'] not in lista_ids:
            lista_ids.add(auto['id'])
            inventario_eliminar_vehiculos.append(auto)

    return dict(inventario=inventario,
                inventario_eliminar=inventario_eliminar,
                inventario_vehiculos=inventario_vehiculos,
                inventario_eliminar_vehiculos=inventario_eliminar_vehiculos
            )

# Muestra un crud para añadir bienes muebles
def entrega0():
    grid_bm = SQLFORM.grid(db.bien_mueble)
    return locals()



# Muestra el inventario de acuerdo al cargo del usuario y la dependencia que tiene
# a cargo
@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def consumibles():
# Inicializando listas de espacios fisicos y dependencias

    # OJO: Espacios debe ser [] siempre que no se este visitando un espacio fisico
    espacios = []
    dependencias = []
    dep_nombre = ""
    dep_padre_id = ""
    dep_padre_nombre = ""

    # Lista de BM en el inventario de un espacio fisico o que componen
    # el inventario agregado de una dependencia
    inventario = []

    # Elementos que deben ser mostrados como una lista en el modal
    # de agregar BM
    material_pred = []
    color = []
    unidad_med = []
    movilidad = []
    uso = []
    nombre_cat = []
    cod_localizacion = []
    localizacion = []
    nombre_espaciof = []
    unidad_adscripcion = []
    unidad_cap = []
    presentacion = []

    # Esta variable es enviada a la vista para que cuando el usuario seleccione
    # un espacio fisico, se pase por GET es_espacio = "True". No quiere decir
    # que la dependencia seleccionada sea un espacio, sino que la siguiente
    # dependencia visitada sera un espacio fisico
    es_espacio = False

    # Permite saber si actualmente se esta visitando un espacio fisico (True)
    # o una dependencia (False)
    espacio_visitado = False

    # Indica si se debe seguir mostrando la flecha para seguir retrocediendo
    retroceder = True

    es_tecnico = auth.has_membership("PERSONAL INTERNO") or auth.has_membership("TÉCNICO")
    direccion_id = __find_dep_id('DIRECCIÓN')

    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    user_dep_id = user.f_dependencia

    if auth.has_membership("PERSONAL INTERNO") or auth.has_membership("TÉCNICO"):
        # Si el tecnico ha seleccionado un espacio fisico
        if request.vars.dependencia:
            if request.vars.es_espacio == "True":
                # Evaluando la correctitud de los parametros del GET
                if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('consumibles'))

                # Determinando si el usuario tiene privilegios suficientes para
                # consultar la dependencia en request.vars.dependencia
                if not __acceso_permitido(user,
                                    int(request.vars.dependencia),
                                        request.vars.es_espacio):
                    redirect(URL('consumibles'))

                espacio_id = request.vars.dependencia
                espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                dep_nombre = espacio.codigo

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_id = espacio.dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre
                # Guardando la unidad de adscripcion
                dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                    ).select().first().unidad_de_adscripcion

                espacio_visitado = True

                # Busca el inventario del espacio
                inventario = __get_inventario_consumibles_espacio(espacio_id)

                material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
                color = ['Amarillo', 'Azul', 'Beige', 'Blanco', 'Dorado', 'Gris', 'Madera', 'Marrón', 'Mostaza', 'Naranja',
                'Negro', 'Plateado', 'Rojo', 'Rosado', 'Verde', 'Vinotinto', 'Otro color']
                unidad_med = ['cm', 'm']
                movilidad = ['Fijo', 'Portátil']
                uso = ['Docencia', 'Investigación', 'Extensión', 'Apoyo administrativo']
                nombre_cat = ['Maquinaria Construcción', 'Equipo Transporte', 'Equipo Comunicaciones',
                'Equipo Médico', 'Equipo Científico Religioso', 'Equipo Oficina']
                cod_localizacion = ['150301', '240107']
                localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
                'Edo Vargas, Municipio Vargas, Parroquia Macuto']
                unidad_cap = ['m³', 'l', 'ml', 'μl', 'kg', 'g', 'mg', 'μg', 'galón', 'oz', 'cup', 'lb']
                presentacion=["Caja", "Paquete", "Unidad", "Otro"]

                # Si se esta agregando un nuevo BM, se registra en la DB
                if request.vars.nombre_mat: # Verifico si me pasan como argumento el nombre del BM.
                    __agregar_material(
                        request.vars.nombre_mat,
                        request.vars.marca_mat, request.vars.modelo_mat, request.vars.cantidad_mat, espacio, request.vars.ubicacion_int ,
                        request.vars.descripcion_mat, request.vars.aforado, request.vars.calibracion_mat,
                        request.vars.capacidad, request.vars.unidad_cap,
                         request.vars.unidad_mat, 
                        request.vars.ancho_mat, request.vars.largo_mat, request.vars.alto_mat,
                        request.vars.diametro_mat, request.vars.material_mat, request.vars.material_sec, request.vars.presentacion,
                        request.vars.unidades, request.vars.total_mat, dep_padre_unid_ads,
                        dep_padre_id, user_id, request.vars.clasificacion)
            else:
                # Espacios a cargo del usuario user_id que pertenecen a la seccion
                # en request.vars.dependencia
                espacios = [row.espacios_fisicos for row in db(
                    (db.es_encargado.espacio_fisico == db.espacios_fisicos.id) &
                    (db.espacios_fisicos.dependencia == int(request.vars.dependencia)) &
                    (db.es_encargado.tecnico == user_id)).select()]

                espacios_ids = [e.id for e in espacios]

                dep_id = int(request.vars.dependencia)
                dep_nombre = db(db.dependencias.id == dep_id).select()[0].nombre

                dep_padre_nombre = "Secciones"

                # Se muestra el inventarios de los espacios que tiene a cargo el usuario en la
                # seccion actual
                inventario = __sumar_inventarios_consumibles(espacios_ids)

                es_espacio = True

        # Si el tecnico o jefe no ha seleccionado un espacio sino que acaba de
        # entrar a la opcion de inventarios
        else:
            # Se buscan las secciones a las que pertenecen los espacios que
            # tiene a cargo el usuario
            espacios_a_cargo = db(
                (db.es_encargado.tecnico == user_id) &
                (db.espacios_fisicos.id == db.es_encargado.espacio_fisico)
                                 ).select()

            secciones_ids = {e.espacios_fisicos.dependencia for e in espacios_a_cargo}

            dependencias = map(lambda x: db(db.dependencias.id == x).select()[0],
                               secciones_ids)

            dep_nombre = "Secciones"

            espacios_ids = [e.espacios_fisicos.id for e in espacios_a_cargo]

            inventario = __sumar_inventarios_consumibles(espacios_ids)

    elif auth.has_membership("JEFE DE SECCIÓN") or auth.has_membership("COORDINADOR"):
        # Si el jefe de seccion ha seleccionado un espacio fisico
        if request.vars.es_espacio == 'True':
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user,
                                int(request.vars.dependencia),
                                    request.vars.es_espacio):
                redirect(URL('bienes_muebles'))

            # Evaluando la correctitud de los parametros del GET
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('bienes_muebles'))


            espacio_id = request.vars.dependencia
            espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
            dep_nombre = espacio.codigo

            # Guardando el ID y nombre de la dependencia padre para el link
            # de navegacion de retorno
            dep_padre_id = espacio.dependencia
            dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                ).select().first().nombre
            # Guardando la unidad de adscripcion
            dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                ).select().first().unidad_de_adscripcion

            espacio_visitado = True

            # Busca el inventario del espacio
            inventario = __get_inventario_consumibles_espacio(espacio_id)

            material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
            color = ['Amarillo', 'Azul', 'Beige', 'Blanco', 'Dorado', 'Gris', 'Madera', 'Marrón', 'Mostaza', 'Naranja',
            'Negro', 'Plateado', 'Rojo', 'Rosado', 'Verde', 'Vinotinto', 'Otro color']
            unidad_med = ['cm', 'm']
            movilidad = ['Fijo', 'Portátil']
            uso = ['Docencia', 'Investigación', 'Extensión', 'Apoyo administrativo']
            nombre_cat = ['Maquinaria Construcción', 'Equipo Transporte', 'Equipo Comunicaciones',
            'Equipo Médico', 'Equipo Científico Religioso', 'Equipo Oficina']
            cod_localizacion = ['150301', '240107']
            localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
            'Edo Vargas, Municipio Vargas, Parroquia Macuto']
            unidad_cap = ['m³', 'l', 'ml', 'μl', 'kg', 'g', 'mg', 'μg', 'galón', 'oz', 'cup', 'lb']
            presentacion=["Caja", "Paquete", "Unidad", "Otro"]

            # Si se esta agregando un nuevo BM, se registra en la DB
            if request.vars.nombre_mat: # Verifico si me pasan como argumento el nombre del BM.
                __agregar_material(
                    request.vars.nombre_mat,
                    request.vars.marca_mat, request.vars.modelo_mat, request.vars.cantidad_mat, espacio, request.vars.ubicacion_int ,
                    request.vars.descripcion_mat, request.vars.aforado, request.vars.calibracion_mat,
                    request.vars.capacidad, request.vars.unidad_cap,
                        request.vars.unidad_mat,
                    request.vars.ancho_mat, request.vars.largo_mat, request.vars.alto_mat,
                    request.vars.diametro_mat, request.vars.material_mat, request.vars.material_sec, request.vars.presentacion,
                    request.vars.unidades, request.vars.total_mat, dep_padre_unid_ads,
                    dep_padre_id, user_id, request.vars.clasificacion)


        # Si el jefe de seccion no ha seleccionado un espacio sino que acaba de
        # regresar a la vista inicial de inventarios
        elif request.vars.es_espacio == 'False':
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                    redirect(URL('consumibles'))
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user,
                                int(request.vars.dependencia),
                                    request.vars.es_espacio):
                redirect(URL('consumibles'))
            espacios = list(db(
                              db.espacios_fisicos.dependencia == user_dep_id
                              ).select(db.espacios_fisicos.ALL))
            dep_nombre = db(db.dependencias.id == user_dep_id
                           ).select().first().nombre

            es_espacio = True                       
        # Si el jefe de seccion no ha seleccionado un espacio sino que acaba de
        # entrar a la vista inicial de inventarios
        else:
            espacios = list(db(
                              db.espacios_fisicos.dependencia == user_dep_id
                              ).select(db.espacios_fisicos.ALL))
            dep_nombre = db(db.dependencias.id == user_dep_id
                           ).select().first().nombre

            es_espacio = True

            # Se muestra como inventario el egregado de los inventarios que
            # pertenecen a la seccion del jefe
            inventario = __get_inventario_consumibles_dep(user_dep_id)

    # Si el usuario no es tecnico, para la base de datos es indiferente su ROL
    # pues la jerarquia de dependencias esta almacenada en la misma tabla
    # con una lista de adyacencias
    else:
        # Si el usuario ha seleccionado una dependencia o un espacio fisico
        if request.vars.dependencia:



            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user,
                                int(request.vars.dependencia),
                                    request.vars.es_espacio):
                redirect(URL('consumibles'))

            if request.vars.es_espacio == "True":

                # Evaluando la correctitud de los parametros del GET
                if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('consumibles'))
       
                # Se muestra el inventario del espacio
                espacio_id = request.vars.dependencia
                espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                dep_nombre = espacio.codigo

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_id = espacio.dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre
                # Guardando la unidad de adscripcion
                dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                    ).select().first().unidad_de_adscripcion

                espacio_visitado = True

                # Busca el inventario del espacio
                inventario = __get_inventario_consumibles_espacio(espacio_id)

                material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
                color = ['Amarillo', 'Azul', 'Beige', 'Blanco', 'Dorado', 'Gris', 'Madera', 'Marrón', 'Mostaza', 'Naranja',
                'Negro', 'Plateado', 'Rojo', 'Rosado', 'Verde', 'Vinotinto', 'Otro color']
                unidad_med = ['cm', 'm']
                movilidad = ['Fijo', 'Portátil']
                uso = ['Docencia', 'Investigación', 'Extensión', 'Apoyo administrativo']
                nombre_cat = ['Maquinaria Construcción', 'Equipo Transporte', 'Equipo Comunicaciones',
                'Equipo Médico', 'Equipo Científico Religioso', 'Equipo Oficina']
                cod_localizacion = ['150301', '240107']
                localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
                'Edo Vargas, Municipio Vargas, Parroquia Macuto']
                unidad_cap = ['m³', 'l', 'ml', 'μl', 'kg', 'g', 'mg', 'μg', 'galón', 'oz', 'cup', 'lb']
                presentacion=["Caja", "Paquete", "Unidad", "Otro"]

                # Si se esta agregando un nuevo BM, se registra en la DB
                if request.vars.nombre_mat: # Verifico si me pasan como argumento el nombre del BM.
                    __agregar_material(
                        request.vars.nombre_mat,
                        request.vars.marca_mat, request.vars.modelo_mat, request.vars.cantidad_mat, espacio, request.vars.ubicacion_int ,
                        request.vars.descripcion_mat, request.vars.aforado, request.vars.calibracion_mat,
                        request.vars.capacidad, request.vars.unidad_cap,
                         request.vars.unidad_mat, 
                        request.vars.ancho_mat, request.vars.largo_mat, request.vars.alto_mat,
                        request.vars.diametro_mat, request.vars.material_mat, request.vars.material_sec, request.vars.presentacion,
                        request.vars.unidades, request.vars.total_mat, dep_padre_unid_ads,
                        dep_padre_id, user_id, request.vars.clasificacion)

            else:

                # Evaluando la correctitud de los parametros del GET
                if not (__is_valid_id(request.vars.dependencia, db.dependencias) and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('consumibles'))
                # Se muestran las dependencias que componen a esta dependencia padre
                # y se lista el inventario agregado
                dep_id = request.vars.dependencia
                dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre
                dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                      ).select(db.dependencias.ALL))
                # Si la lista de dependencias es vacia, entonces la dependencia no
                # tiene otras dependencias por debajo (podria tener espacios fisicos
                # o estar vacia)
                if dependencias:
                    # Buscando espacios fisicos que apunten a la dependencia escogida
                    espacios = list(db(db.espacios_fisicos.dependencia == dep_id
                                      ).select(db.espacios_fisicos.ALL))
                    es_espacio = True

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_id = db(db.dependencias.id == request.vars.dependencia
                                 ).select().first().unidad_de_adscripcion
                # Si dep_padre_id es None, se ha llegado al tope de la jerarquia
                # y no hay un padre de este nodo
                if dep_padre_id:
                    dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                         ).select().first().nombre
                # Se muestra como inventario el egregado de los inventarios que
                # pertenecen a la dependencia del usuario
                inventario = __get_inventario_consumibles_dep(dep_id)

        else:
            # Dependencia a la que pertenece el usuario o que tiene a cargo
            dep_id = user.f_dependencia
            dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre

            # Se muestran las dependencias que componen a la dependencia que
            # tiene a cargo el usuario y el inventario agregado de esta
            dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                  ).select(db.dependencias.ALL))

            # Se muestra como inventario el egregado de los inventarios que
            # pertenecen a la dependencia del usuario
            inventario = __get_inventario_consumibles_dep(dep_id)

    return dict(dep_nombre=dep_nombre,
                dependencias=dependencias,
                espacios=espacios,
                es_espacio=es_espacio,
                espacio_visitado=espacio_visitado,
                dep_padre_id=dep_padre_id,
                dep_padre_nombre=dep_padre_nombre,
                direccion_id=direccion_id,
                es_tecnico=es_tecnico,
                inventario=inventario,
                retroceder=retroceder,
                material_pred = material_pred,
                color_list = color,
                unidad_med = unidad_med,
                movilidad_list = movilidad,
                uso_list = uso,
                nombre_cat = nombre_cat,
                cod_localizacion = cod_localizacion,
                localizacion = localizacion,
                unidad_cap = unidad_cap,
                presentacion = presentacion
                )

# Muestra el inventario de acuerdo al cargo del usuario y la dependencia que tiene
# a cargo
@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def herramientas():
# Inicializando listas de espacios fisicos y dependencias

    # OJO: Espacios debe ser [] siempre que no se este visitando un espacio fisico
    espacios = []
    dependencias = []
    dep_nombre = ""
    dep_padre_id = ""
    dep_padre_nombre = ""

    # Lista de BM en el inventario de un espacio fisico o que componen
    # el inventario agregado de una dependencia
    inventario = []

    # Elementos que deben ser mostrados como una lista en el modal
    # de agregar BM
    material_pred = []
    color = []
    unidad_med = []
    movilidad = []
    uso = []
    nombre_cat = []
    cod_localizacion = []
    localizacion = []
    nombre_espaciof = []
    unidad_adscripcion = []
    unidad_cap = []
    presentacion = []

    # Esta variable es enviada a la vista para que cuando el usuario seleccione
    # un espacio fisico, se pase por GET es_espacio = "True". No quiere decir
    # que la dependencia seleccionada sea un espacio, sino que la siguiente
    # dependencia visitada sera un espacio fisico
    es_espacio = False

    # Permite saber si actualmente se esta visitando un espacio fisico (True)
    # o una dependencia (False)
    espacio_visitado = False

    # Indica si se debe seguir mostrando la flecha para seguir retrocediendo
    retroceder = True

    es_tecnico = auth.has_membership("TÉCNICO") or auth.has_membership("PERSONAL INTERNO")
    direccion_id = __find_dep_id('DIRECCIÓN')

    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    user_dep_id = user.f_dependencia

    if auth.has_membership("TÉCNICO") or auth.has_membership("PERSONAL INTERNO"):
        # Si el tecnico ha seleccionado un espacio fisico
        if request.vars.dependencia:
            if request.vars.es_espacio == "True":
                # Evaluando la correctitud de los parametros del GET
                if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('herramientas'))

                # Determinando si el usuario tiene privilegios suficientes para
                # consultar la dependencia en request.vars.dependencia
                if not __acceso_permitido(user,
                                    int(request.vars.dependencia),
                                        request.vars.es_espacio):
                    redirect(URL('herramientas'))

                espacio_id = request.vars.dependencia
                espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                dep_nombre = espacio.codigo

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_id = espacio.dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre
                # Guardando la unidad de adscripcion
                dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                    ).select().first().unidad_de_adscripcion

                espacio_visitado = True

                # Busca el inventario del espacio
                inventario = __get_inventario_herramientas_espacio(espacio_id)

                material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
                unidad_med = ['cm', 'm']
                presentacion=["Unidad", "Conjunto"]

                # Si se esta agregando un nuevo BM, se registra en la DB
                if request.vars.nombre_her: # Verifico si me pasan como argumento el nombre del BM.
                    __agregar_herramienta(
                        request.vars.nombre_her, request.vars.num_her,request.vars.marca_her, request.vars.modelo_her,
                        request.vars.serial_her, request.vars.presentacion, request.vars.numpiezas_her, request.vars.contenido_her,
                        request.vars.descripcion_her,  request.vars.material_mat,request.vars.unidad, request.vars.ancho_her,
                        request.vars.largo_her, request.vars.alto_her, request.vars.diametro_her, request.vars.ubicacion_int,
                        request.vars.descripcion_herramientas, espacio, dep_padre_unid_ads, dep_padre_id, user_id)
            else:
                # Espacios a cargo del usuario user_id que pertenecen a la seccion
                # en request.vars.dependencia
                espacios = [row.espacios_fisicos for row in db(
                    (db.es_encargado.espacio_fisico == db.espacios_fisicos.id) &
                    (db.espacios_fisicos.dependencia == int(request.vars.dependencia)) &
                    (db.es_encargado.tecnico == user_id)).select()]

                espacios_ids = [e.id for e in espacios]

                dep_id = int(request.vars.dependencia)
                dep_nombre = db(db.dependencias.id == dep_id).select()[0].nombre

                dep_padre_nombre = "Secciones"

                # Se muestra el inventarios de los espacios que tiene a cargo el usuario en la
                # seccion actual
                inventario = __sumar_inventarios_herramientas(espacios_ids)

                es_espacio = True

        # Si el tecnico o jefe no ha seleccionado un espacio sino que acaba de
        # entrar a la opcion de inventarios
        else:
            # Se buscan las secciones a las que pertenecen los espacios que
            # tiene a cargo el usuario
            espacios_a_cargo = db(
                (db.es_encargado.tecnico == user_id) &
                (db.espacios_fisicos.id == db.es_encargado.espacio_fisico)
                                 ).select()

            secciones_ids = {e.espacios_fisicos.dependencia for e in espacios_a_cargo}

            dependencias = map(lambda x: db(db.dependencias.id == x).select()[0],
                               secciones_ids)

            dep_nombre = "Secciones"

            espacios_ids = [e.espacios_fisicos.id for e in espacios_a_cargo]

            inventario = __sumar_inventarios_herramientas(espacios_ids)

    elif auth.has_membership("JEFE DE SECCIÓN") or auth.has_membership("TÉCNICO") or auth.has_membership("COORDINADOR"):
        # Si el jefe de seccion ha seleccionado un espacio fisico
        if request.vars.es_espacio == 'True':
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user,
                                int(request.vars.dependencia),
                                    request.vars.es_espacio):
                redirect(URL('herramientas'))

            # Evaluando la correctitud de los parametros del GET
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('herramientas'))


            espacio_id = request.vars.dependencia
            espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
            dep_nombre = espacio.codigo

            # Guardando el ID y nombre de la dependencia padre para el link
            # de navegacion de retorno
            dep_padre_id = espacio.dependencia
            dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                ).select().first().nombre
            # Guardando la unidad de adscripcion
            dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                ).select().first().unidad_de_adscripcion

            espacio_visitado = True

            # Busca el inventario del espacio
            inventario = __get_inventario_herramientas_espacio(espacio_id)

            material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
            unidad_med = ['cm', 'm']
            presentacion=["Unidad", "Conjunto"]

            # Si se esta agregando un nuevo BM, se registra en la DB
            if request.vars.nombre_her: # Verifico si me pasan como argumento el nombre del BM.
                __agregar_herramienta(
                    request.vars.nombre_her, request.vars.num_her,request.vars.marca_her, request.vars.modelo_her,
                    request.vars.serial_her, request.vars.presentacion, request.vars.numpiezas_her, request.vars.contenido_her,
                    request.vars.descripcion_her,  request.vars.material_mat,request.vars.unidad, request.vars.ancho_her,
                    request.vars.largo_her, request.vars.alto_her, request.vars.diametro_her, request.vars.ubicacion_int ,
                    request.vars.descripcion_herramientas, espacio, dep_padre_unid_ads, dep_padre_id, user_id)


        # Si el jefe de seccion no ha seleccionado un espacio sino que acaba de
        # regresar a la vista inicial de inventarios
        elif request.vars.es_espacio == 'False':
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                    redirect(URL('herramientas'))
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user,
                                int(request.vars.dependencia),
                                    request.vars.es_espacio):
                redirect(URL('herramientas'))
            espacios = list(db(
                              db.espacios_fisicos.dependencia == user_dep_id
                              ).select(db.espacios_fisicos.ALL))
            dep_nombre = db(db.dependencias.id == user_dep_id
                           ).select().first().nombre

            es_espacio = True                       
        # Si el jefe de seccion no ha seleccionado un espacio sino que acaba de
        # entrar a la vista inicial de inventarios
        else:
            espacios = list(db(
                              db.espacios_fisicos.dependencia == user_dep_id
                              ).select(db.espacios_fisicos.ALL))
            dep_nombre = db(db.dependencias.id == user_dep_id
                           ).select().first().nombre

            es_espacio = True

            # Se muestra como inventario el egregado de los inventarios que
            # pertenecen a la seccion del jefe
            inventario = __get_inventario_herramientas_dep(user_dep_id)

    # Si el usuario no es tecnico, para la base de datos es indiferente su ROL
    # pues la jerarquia de dependencias esta almacenada en la misma tabla
    # con una lista de adyacencias
    else:
        # Si el usuario ha seleccionado una dependencia o un espacio fisico
        if request.vars.dependencia:



            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user,
                                int(request.vars.dependencia),
                                    request.vars.es_espacio):
                redirect(URL('herramientas'))

            if request.vars.es_espacio == "True":
       

            # Evaluando la correctitud de los parametros del GET
                if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('herramientas'))
                # Se muestra el inventario del espacio
                espacio_id = request.vars.dependencia
                espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                dep_nombre = espacio.codigo

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_id = espacio.dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre
                # Guardando la unidad de adscripcion
                dep_padre_unid_ads = db(db.dependencias.id == dep_padre_id
                                    ).select().first().unidad_de_adscripcion

                espacio_visitado = True

                # Busca el inventario del espacio
                inventario = __get_inventario_herramientas_espacio(espacio_id)

                material_pred = ['Acero', 'Acrílico', 'Madera', 'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']
                unidad_med = ['cm', 'm']
                presentacion=["Unidad", "Conjunto"]

                # Si se esta agregando un nuevo BM, se registra en la DB
                if request.vars.nombre_her: # Verifico si me pasan como argumento el nombre del BM.
                    __agregar_herramienta(
                        request.vars.nombre_her, request.vars.num_her, request.vars.marca_her, request.vars.modelo_her,
                        request.vars.serial_her, request.vars.presentacion, request.vars.numpiezas_her, request.vars.contenido_her,
                        request.vars.descripcion_her, request.vars.material_mat, request.vars.unidad, request.vars.ancho_her,
                        request.vars.largo_her, request.vars.alto_her, request.vars.diametro_her, request.vars.ubicacion_int ,
                        request.vars.descripcion_herramientas, espacio, dep_padre_unid_ads, dep_padre_id, user_id)
            else:

            # Evaluando la correctitud de los parametros del GET
                if not (__is_valid_id(request.vars.dependencia, db.dependencias) and
                        __is_bool(request.vars.es_espacio)):
                    redirect(URL('herramientas'))
                # Se muestran las dependencias que componen a esta dependencia padre
                # y se lista el inventario agregado
                dep_id = request.vars.dependencia
                dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre
                dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                      ).select(db.dependencias.ALL))
                # Si la lista de dependencias es vacia, entonces la dependencia no
                # tiene otras dependencias por debajo (podria tener espacios fisicos
                # o estar vacia)
                if dependencias:
                    # Buscando espacios fisicos que apunten a la dependencia escogida
                    espacios = list(db(db.espacios_fisicos.dependencia == dep_id
                                      ).select(db.espacios_fisicos.ALL))
                    es_espacio = True

                # Guardando el ID y nombre de la dependencia padre para el link
                # de navegacion de retorno
                dep_padre_id = db(db.dependencias.id == request.vars.dependencia
                                 ).select().first().unidad_de_adscripcion
                # Si dep_padre_id es None, se ha llegado al tope de la jerarquia
                # y no hay un padre de este nodo
                if dep_padre_id:
                    dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                         ).select().first().nombre
                # Se muestra como inventario el egregado de los inventarios que
                # pertenecen a la dependencia del usuario
                inventario = __get_inventario_herramientas_dep(dep_id)

        else:
            # Dependencia a la que pertenece el usuario o que tiene a cargo
            dep_id = user.f_dependencia
            dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre

            # Se muestran las dependencias que componen a la dependencia que
            # tiene a cargo el usuario y el inventario agregado de esta
            dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                  ).select(db.dependencias.ALL))

            # Se muestra como inventario el egregado de los inventarios que
            # pertenecen a la dependencia del usuario
            inventario = __get_inventario_herramientas_dep(dep_id)

    return dict(dep_nombre=dep_nombre,
                dependencias=dependencias,
                espacios=espacios,
                es_espacio=es_espacio,
                espacio_visitado=espacio_visitado,
                dep_padre_id=dep_padre_id,
                dep_padre_nombre=dep_padre_nombre,
                direccion_id=direccion_id,
                es_tecnico=es_tecnico,
                inventario=inventario,
                retroceder=retroceder,
                material_pred=material_pred,
                unidad_med=unidad_med,
                presentacion=presentacion
            )
