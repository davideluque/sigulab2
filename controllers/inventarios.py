# -*- coding: utf-8 -*-
# tente algo como


# < -------- Funciones privadas de SMDYP ------------>

import datetime

# Verifica si el usuario que intenta acceder al controlador tiene alguno de los
# roles necesarios
def __check_role():

    roles_permitidos = ['WEBMASTER', 'DIRECTOR', 'ASISTENTE DEL DIRECTOR',
                        'COORDINADOR', 'PERSONAL DE DEPENDENCIA', 
                        'JEFE DE LABORATORIO', 'JEFE DE SECCIÓN', 'PERSONAL INTERNO', 
                        'GESTOR DE SMyDP']
    return True in map(lambda x: auth.has_membership(x), roles_permitidos)

# Determina si el id de la dependencia es valido. Retorna False si el id no existe
# o es de un tipo incorrecto
def __is_valid_id(id_, tabla):
    try:
        int(id_)
    except:
        return False
    # Si el id recibido tiene el tipo correcto pero no existe en la base de datos
    if not db(tabla.id == int(id_)).select():
        return False

    return True

# Determina si una variable "booleana" pasada como parametro con GET es realmente
# 'True' o 'False' (request.vars almacena todo como strings)
def __is_bool(bool_var):
    if not bool_var in ['True', 'False']:
        return False
    else:
        return True

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
def __get_mantenimiento_bm(id=None):
    return db(db.historial_mantenimiento_bm.hmbm_nro == id).select()

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

    if not dep_id in jerarquia:
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

    secciones = []
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


# Registra un nueva bm en el espacio fisico indicado. Si el bm ya
# existe en el inventario, genera un mensaje con flash y no anade de nuevo 
# el bm. 
def __agregar_bm(nombre, no_bien, no_placa, marca, modelo, serial,
                descripcion, material, color, calibrar, fecha_calibracion,
                unidad_med, ancho, largo, alto, diametro, movilidad, uso, 
                estatus, nombre_cat, subcategoria, cod_loc, localizacion, espacio, unidad_ad, 
                dependencia, user, clasificacion):

    # Si ya existe el BM en el inventario
    if (db(db.bien_mueble.bm_num == no_bien).select()):
        bm = db(db.bien_mueble.bm_num == no_bien).select()[0]

        response.flash = "El BM \"{0}\" ya ha sido ingresado anteriormente \
                          al espacio \"{1}\".".format(bm.bm_nombre, bm.bm_espacio_fisico)
        return False
    
    if not unidad_med:
        ancho=None
        largo=None
        alto=None
        diametro=None
    
    # Si no, se agrega al inventario del espacio fisico la nueva sustancia
    inv_id = db.bien_mueble.insert(
            bm_nombre = nombre, 
            bm_num = no_bien, 
            bm_placa = no_placa, 
            bm_marca = marca, 
            bm_modelo = modelo, 
            bm_serial = serial,
            bm_descripcion = descripcion, 
            bm_material = material, 
            bm_color = color,
            bm_calibrar =  calibrar,
            bm_fecha_calibracion = fecha_calibracion,
            bm_unidad = unidad_med, 
            bm_ancho = ancho, 
            bm_largo = largo,
            bm_alto = alto, 
            bm_diametro = diametro, 
            bm_movilidad = movilidad, 
            bm_uso = uso,
            bm_estatus = estatus, 
            bm_categoria = nombre_cat,
            bm_subcategoria = subcategoria, 
            bm_codigo_localizacion = cod_loc,
            bm_localizacion = localizacion, 
            bm_espacio_fisico = espacio,
            bm_unidad_de_adscripcion = unidad_ad, 
            bm_depedencia = dependencia, 
            bm_crea_ficha = user,
            bm_clasificacion = clasificacion
        )
    return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 


# Registra un nuevo mantenimiento a un bm indicado.
def __agregar_mantenimiento_bm(no_bien, fecha_sol, codigo, tipo, servicio, accion,
                descripcion, proveedor, fecha_inicio, fecha_fin, tiempo_ejec,
                fecha_cert, observacion):

    inv_id = db.historial_mantenimiento_bm.insert(
            hmbm_nro = no_bien, 
            hmbm_fecha_sol = fecha_sol, 
            hmbm_codigo = codigo, 
            hmbm_tipo = tipo, 
            hmbm_servicio = servicio, 
            hmbm_accion = accion,
            hmbm_descripcion = descripcion, 
            hmbm_proveedor = proveedor, 
            hmbm_fecha_inicio = fecha_inicio,
            hmbm_fecha_fin =  fecha_fin,
            hmbm_tiempo_ejec = tiempo_ejec,
            hmbm_fecha_cert = fecha_cert, 
            hmbm_observacion = observacion
        )
    return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 


# Registra un nueva material/consumible en el espacio fisico indicado. Si el bm ya
# existe en el inventario, genera un mensaje con flash y no anade de nuevo 
# el bm. 
def __agregar_material(nombre, marca, modelo, cantidad, espacio, ubicacion,
                descripcion, aforado, calibrar, capacidad, unidad, unidad_dim, 
                 ancho, largo, alto, diametro, material, material_sec, presentacion,
                 unidades,total, unidad_adscripcion, dependencia, user , clasificacion):

    # Si ya existe el BM en el inventario
    if (db( (db.sin_bn.sb_nombre == nombre) & (db.sin_bn.sb_espacio==espacio) ).select()):
        #bm = db(db.bien_mueble.bm_num == no_bien).select()[0]

        response.flash = "El BM \"{0}\" ya ha sido ingresado anteriormente \
                          en este espacio.".format(nombre)
        return False
    
    if not unidad_dim:
        ancho=None
        largo=None
        alto=None
        diametro=None
    
    # Si no, se agrega al inventario del espacio fisico la nueva sustancia
    inv_id = db.sin_bn.insert(
        sb_cantidad = cantidad,
        sb_nombre = nombre,   
        sb_marca = marca, 
        sb_modelo = modelo, 
        sb_descripcion = descripcion, 
        sb_material = material, 
        sb_material_sec = material_sec,
        sb_calibrar =  calibrar,
        sb_unidad = unidad, 
        sb_ancho = ancho, 
        sb_largo = largo,
        sb_alto = alto, 
        sb_diametro = diametro, 
        sb_espacio = espacio,
        sb_clasificacion = clasificacion,
        sb_presentacion = presentacion,
        sb_unidades = unidades,
        sb_total = total,
        sb_aforado = aforado,
        sb_ubicacion = ubicacion,
        sb_capacidad = capacidad,
        sb_unidad_dim = unidad_dim,
        sb_unidad_de_adscripcion = unidad_adscripcion,
        sb_depedencia = dependencia,
        sb_crea_ficha = user,
    )
    return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 

"""         concepto = 'Ingreso'
        tipo_ing = 'Ingreso inicial'
        # Agregando la primera entrada de la sustancia en la bitacora
        db.t_Bitacora.insert(
                                f_cantidad=cantidad,
                                f_cantidad_total=cantidad,
                                f_concepto=concepto,
                                f_tipo_ingreso=tipo_ing,
                                f_medida=unidad_id,
                                f_inventario=inv_id,
                                f_sustancia=sustancia_id) """



# Registra un nueva material/consumible en la tabla de modiciaciones. Si el bm ya
# existe en el inventario, genera un mensaje con flash y no anade de nuevo 
# el bm. 
def __agregar_material_modificar(nombre, marca, modelo, cantidad, espacio, ubicacion,
                descripcion, aforado, calibrar, capacidad, unidad, unidad_dim, 
                 ancho, largo, alto, diametro, material, material_sec, presentacion,
                 unidades,total, user , clasificacion, descripcion_mod):

    if (db( (db.modificacion_sin_bn.msb_nombre == nombre) & (db.modificacion_sin_bn.msb_espacio==espacio) ).select()):
        #bm = db(db.bien_mueble.bm_num == no_bien).select()[0]

        response.flash = "El  \"{0}\" tiene una modificación pendiente \
                          Por los momentos no se enviarán solicitudes de modificación.".format(clasificacion)
        return False

    response.flash = "Se ha enviado una solicidad de modificación del \"{0}\"  \"{1}\" \
                        .".format(clasificacion,nombre)

    if not unidad_dim:
        ancho=None
        largo=None
        alto=None
        diametro=None

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
    response.flash = "Se ha realizado exitosamente la solicitud de modificación del material de laboratorio " + str(nombre)
    return True
    #return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 


# Registra un nueva material/consumible en el espacio fisico indicado. Si el bm ya
# existe en el inventario, genera un mensaje con flash y no anade de nuevo 
# el bm. 
def __agregar_herramienta(nombre, num, marca, modelo, serial, presentacion, numpiezas,
                contenido, descripcion, material, unidad, ancho, largo, alto, diametro, 
                ubicacion, observacion, espacio,unidad_adscripcion, dependencia, user):

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
        ancho=None
        largo=None
        alto=None
        diametro=None
    
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
    return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 

def __agregar_herramienta_modificar(nombre, num, marca, modelo, serial, presentacion, numpiezas,
                contenido, descripcion, material, unidad, ancho, largo, alto, diametro, 
                ubicacion, observacion, motivo, espacio,unidad_adscripcion, dependencia, user1, user2):

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
        ancho=None
        largo=None
        alto=None
        diametro=None
    
    # Si no, se agrega al inventario del espacio fisico la nueva sustancia
    inv_id = db.modificacion_herramienta.insert(
        mhr_nombre = nombre,
        mhr_num=num,   
        mhr_marca = marca, 
        mhr_modelo = modelo, 
        mhr_serial = serial, 
        mhr_presentacion = presentacion,
        mhr_numpiezas= numpiezas,
        mhr_contenido =contenido,
        mhr_descripcion = descripcion, 
        mhr_material = material, 
        mhr_unidad = unidad, 
        mhr_ancho = ancho, 
        mhr_largo = largo,
        mhr_alto = alto, 
        mhr_diametro = diametro, 
        mhr_espacio_fisico = espacio,
        mhr_ubicacion = ubicacion,
        mhr_observacion= observacion,
        mhr_motivo = motivo,
        mhr_unidad_de_adscripcion = unidad_adscripcion,
        mhr_depedencia = dependencia,
        mhr_crea_ficha = user1,
        mhr_modifica_ficha = user2
    )
    response.flash = "Se ha realizado exitosamente la solicitud de modificación de la herramienta " + str(nombre)
    return True
    #return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 


# Dado el id de una depencia y conociendo si es un espacio fisico o una dependencia
# comun, determina si el usuario tiene privilegios suficientes para obtener informacion
# de esta
def __acceso_permitido(user, dep_id, es_espacio):
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
    if auth.has_membership("PERSONAL INTERNO"):
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
        if es_espacio == "True":
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

# Agrega un nuevo registro a la bitacora de una sustancia
def __agregar_registro(concepto):

    cantidad = float(request.vars.cantidad)

    # Operaciones comunes a todos los casos: actualizacion del inventario

    # ID de la unidad en la que el usuario registro la cantidad ingresada
    unidad_id = request.vars.unidad

    # Inventario al cual pertenece la bitacora consultada
    inv = db(db.t_Inventario.id == request.get_vars.inv).select()[0]

    # Unidad indicada por el usuario
    unidad = db(db.t_Unidad_de_medida.id == unidad_id
                   ).select()[0].f_nombre

    # Unidad de medida en la que se encuentra el inventario de la sustancia
    unidad_inventario = db(db.t_Unidad_de_medida.id == inv.f_medida
                          ).select()[0].f_nombre

    # Transformando las cantidades de acuerdo a la unidad utilizada en
    # el inventario de la sustancia
    cantidad = __transformar_cantidad(cantidad, unidad, unidad_inventario)

    # Cantidades total y de uso interno antes del ingreso o consumo
    total_viejo = inv.f_existencia
    uso_interno_viejo = inv.f_uso_interno

    if concepto == 'Ingreso':
        tipo_ing = request.vars.tipo_ingreso

        # Nueva cantidad total y nueva cantidad para uso interno
        total_nuevo = total_viejo + cantidad
        uso_interno_nuevo = uso_interno_viejo + cantidad

        # Actualizando cantidad total con la nueva 
        inv.update_record(
            f_existencia=total_nuevo,
            f_uso_interno=uso_interno_nuevo)

        if tipo_ing == 'Almacén':

            almacen = int(request.vars.almacen)

            db.t_Bitacora.insert(
                f_cantidad=cantidad,
                f_cantidad_total=total_nuevo,
                f_concepto=concepto,
                f_tipo_ingreso=tipo_ing,
                f_medida=inv.f_medida,
                f_inventario=inv.id,
                f_sustancia=inv.sustancia,
                f_almacen=almacen)

        # Tipo ingreso es compra
        else:

            # Datos de la nueva compra
            nro_factura = request.vars.nro_factura
            institucion = request.vars.institucion
            rif = request.vars.rif

            # Fecha de la compra en formato "%m/%d/%Y"
            fecha_compra = request.vars.fecha_compra
            
            # Se registra la nueva compra en la tabla t_Compra
            compra_id = db.t_Compra.insert(
                f_cantidad=cantidad,
                f_nro_factura=nro_factura,
                f_institucion=institucion,
                f_rif=rif,
                f_fecha=fecha_compra,
                f_sustancia=inv.sustancia,
                f_medida=unidad_id)

            db.t_Bitacora.insert(
                f_cantidad=cantidad,
                f_cantidad_total=total_nuevo,
                f_concepto=concepto,
                f_tipo_ingreso=tipo_ing,
                f_medida=inv.f_medida,
                f_compra=compra_id,
                f_inventario=inv.id,
                f_sustancia=inv.sustancia)

    else:
        tipo_eg = request.vars.tipo_egreso            
        
        # Nueva cantidad total luego del consumo
        total_nuevo = total_viejo - cantidad
        if total_nuevo < 0:
            response.flash = "La cantidad total luego del consumo no puede ser "\
                             "negativa"
            redirect(URL(args=request.args, vars=request.get_vars, host=True))
        
        # Nueva cantidad de uso interno nueva puede ser maximo lo que era antes
        # (si hay material suficiente) o el nuevo total
        uso_interno_nuevo = min(uso_interno_viejo, total_nuevo)

        # Actualizando cantidad total con la nueva 
        inv.update_record(
            f_existencia=total_nuevo,
            f_uso_interno=uso_interno_nuevo)

        servicio_id = request.vars.servicio

        db.t_Bitacora.insert(
            f_cantidad=cantidad,
            f_cantidad_total=total_nuevo,
            f_concepto=concepto,
            f_tipo_egreso=tipo_eg,
            f_medida=inv.f_medida,
            f_servicio=servicio_id,
            f_inventario=inv.id,
            f_sustancia=inv.sustancia)

    # Se redirije para evitar mensaje de revisita con metodo POST
    return redirect(URL(args=request.args, vars=request.get_vars, host=True))

def __agregar_modificar_bm(nombre, no_bien, no_placa, marca, modelo, serial,
                descripcion, material, color, calibrar, fecha_calibracion,
                unidad_med, ancho, largo, alto, diametro, movilidad, uso, 
                estatus, nombre_cat, subcategoria, cod_loc, localizacion, descripcion_mod, user, confirmacion=None):
    # Si ya existe el BM en el inventario
    if (db(db.modificacion_bien_mueble.mbn_num == no_bien).select()):
        bm = db(db.bien_mueble.bm_num == no_bien).select()[0] #Se busca de la tabla de bm para tener el nombre original
        response.flash = "El  \"{0}\" tiene una modificación pendiente \
                        Por los momentos no se enviarán solicitudes de modificación.".format(nombre)
        return False
    # Si no, se agrega al inventario del espacio fisico la nueva sustancia
    
    if not unidad_med:
        ancho=None
        largo=None
        alto=None
        diametro=None
    
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
    response.flash = "Se ha realizado exitosamente la solicitud de modificación del bien mueble " + str(nombre)
    #return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 
    return True


# < -------- Final Funciones privadas de SMDYP ------------>

# < ------- Vistas del modulo de inventario -------->
def index(): 
    solicitudes_pendientes = validaciones()
    numero_solicitudes = 0
    if(len(solicitudes_pendientes['inventario'][0]) != 0 or \
        len(solicitudes_pendientes['inventario'][1]) != 0 or \
        len(solicitudes_pendientes['inventario'][2]) != 0 or \
        len(solicitudes_pendientes['inventario_eliminar'][0]) != 0 or \
        len(solicitudes_pendientes['inventario_eliminar'][1]) != 0 or \
        len(solicitudes_pendientes['inventario_eliminar'][2]) != 0
        ):
        numero_solicitudes = len(solicitudes_pendientes['inventario'][0]) + \
        len(solicitudes_pendientes['inventario'][1]) + \
        len(solicitudes_pendientes['inventario'][2]) + \
        len(solicitudes_pendientes['inventario_eliminar'][0]) + \
        len(solicitudes_pendientes['inventario_eliminar'][1]) + \
        len(solicitudes_pendientes['inventario_eliminar'][2])
    return dict(numero_solicitudes = numero_solicitudes)

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

    # Busco la herramienta
    bien = db((db.modificacion_herramienta.mhr_nombre == name) & (db.modificacion_herramienta.mhr_espacio_fisico==espacio) & (db.modificacion_herramienta.mhr_ubicacion==ubicacion)).select()[0]

    #Inicializo variables
    material_pred = []
    unidad_med = []
    presentacion=[]

    # Si se elimina
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
        db((db.modificacion_herramienta.mhr_nombre == name) & (db.modificacion_herramienta.mhr_espacio_fisico==espacio) & (db.modificacion_herramienta.mhr_ubicacion==ubicacion)).delete()
        session.flash = "Solicitud de modificación aceptada"
        redirect(URL('validaciones'))
    # Si no se modifica
    if request.vars.no:
        db((db.modificacion_herramienta.mhr_nombre == name) & (db.modificacion_herramienta.mhr_espacio_fisico==espacio) & (db.modificacion_herramienta.mhr_ubicacion==ubicacion)).delete()
        session.flash = "Solicitud de modificación rechazada"
        redirect(URL('validaciones'))

    material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
    unidad_med = ['cm','m']
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

    return dict(bien = bien,
                material_pred = material_pred,
                caracteristicas_list = caracteristicas_list,
                caracteristicas_dict = caracteristicas_dict,
                unidad_med = unidad_med,
                presentacion = presentacion
                )

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles_mod_mat():
    #Recuperamos el espacio
    espacio = request.vars['espacio']
    #El nombre del material/consumible
    name = request.vars['nombreMat']

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
        db( (db.modificacion_sin_bn.msb_espacio == espacio) & (db.modificacion_sin_bn.msb_nombre == name) ).delete()
        session.flash = "Solicitud de modificación aceptada"
        redirect(URL('validaciones'))
    if request.vars.no:
        db( (db.modificacion_sin_bn.msb_espacio == espacio) & (db.modificacion_sin_bn.msb_nombre == name) ).delete()
        session.flash = "Solicitud de modificación rechazada"
        redirect(URL('validaciones'))

    if bien_original['sb_clasificacion'] == "Material de Laboratorio":
        caracteristicas_list = ['Cantidad:','Marca:', 'Modelo:', 'Aforado:', 'Requiere calibración:', 
        'Capacidad:', 'Unidad de medida:', 'Material predominante:', 'Material secundario:', 'Descripción:', 'Tipo:', 'Ubicación interna:']
        caracteristicas_dict = {
            'Cantidad:': bien['msb_cantidad'],
            'Marca:': bien['msb_marca'].upper(),
            'Modelo:': bien['msb_modelo'].upper(),
            'Descripción:': bien['msb_descripcion'].upper(),
            'Material predominante:': bien['msb_material'].upper(),
            'Material secundario:': bien['msb_material_sec'].upper(),
            'Aforado:': bien['msb_aforado'].upper(),
            'Tipo:': bien_original['sb_clasificacion'].upper(),
            'Requiere calibración:': bien['msb_calibrar'].upper(),
            'Ubicación interna:' : bien['msb_ubicacion'].upper(),
            'Capacidad:': bien['msb_capacidad'],
            'Unidad de medida:' : bien['msb_unidad'].upper(),
        }
    else:
        caracteristicas_list = ["Marca:", "Modelo:", "Presentación:", "Unidades por presentación:", "Cantidad:", 
        "Total(U.):", "Descripción:", "Ubicación interna:"]
        caracteristicas_dict = {
            'Presentación:': bien['msb_presentacion'].upper(),
            'Unidades por presentación:': bien['msb_unidades'].upper(),
            'Cantidad:': bien['msb_cantidad'],
            'Total(U.):': bien['msb_total'],
            'Marca:': bien['msb_marca'].upper(),
            'Modelo:': bien['msb_modelo'].upper(),
            'Descripción:': bien['msb_descripcion'].upper(),
            'Ubicación interna:' : bien['msb_ubicacion'].upper(),
            'Tipo:': bien_original['sb_clasificacion'].upper()
        }
    return dict(bien = bien,
                bien_original = bien_original,
                caracteristicas_list = caracteristicas_list,
                caracteristicas_dict = caracteristicas_dict
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
        db(db.modificacion_bien_mueble.mbn_num == bm).delete()
        session.flash = "Solicitud de modificación aceptada"
        redirect(URL('validaciones'))

    if request.vars.no:
        db(db.modificacion_bien_mueble.mbn_num == bm).delete()
        session.flash = "Solicitud de modificación rechazada"
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
    
    return dict(bien = bien,
                bien_original = bien_original,
                caracteristicas_list = caracteristicas_list,
                caracteristicas_dict = caracteristicas_dict,
                sudebid_list = sudebid_list,
                sudebid_dict = sudebid_dict)

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles():
    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    bm = request.vars['bm']
    bien = db(db.bien_mueble.bm_num == bm).select()[0]

    mantenimiento=__get_mantenimiento_bm(bm)

    # Si se elimina
    if request.vars.si:
        db(db.historial_mantenimiento_bm.hmbm_nro == bm).delete()
        db(db.bien_mueble.bm_num == bm).delete()
        db(db.modificacion_bien_mueble.mbn_num == bm).delete()
        session.flash = "Solicitud de eliminación aceptada"
        redirect(URL('validaciones'))
    # Si no se elimina
    if request.vars.no:
        db(db.bien_mueble.bm_num == bien['bm_num']).select().first().update_record(bm_eliminar = 2)
        session.flash = "Solicitud de eliminación rechazada"
        redirect(URL('validaciones'))

    if request.vars.modificacion:
        __agregar_modificar_bm(
            request.vars.nombre, bien['bm_num'],request.vars.no_placa, 
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
            bien['bm_num'],request.vars.fecha_sol, 
            request.vars.codigo, request.vars.tipo, request.vars.servicio,
            request.vars.accion, request.vars.descripcion_man, request.vars.proveedor,
            request.vars.fecha_inicio, request.vars.fecha_fin, request.vars.tiempo_ejec, 
            request.vars.fecha_cert, request.vars.observacion_man)
        request.vars.mantenimiento_nuevo=None

    if request.vars.eliminacion:
        if bien['bm_eliminar'] == 2: 
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

    material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
    color = ['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja',
    'Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color']
    unidad_med = ['cm','m']
    movilidad = ['Fijo','Portátil']
    uso = ['Docencia','Investigación','Extensión','Apoyo administrativo']
    nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento', 
    'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
    cod_localizacion = ['150301','240107']
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

    return dict(bien = bien,
                material_pred = material_pred,
                color_list = color,
                unidad_med = unidad_med,
                movilidad_list = movilidad,
                uso_list = uso,
                nombre_cat = nombre_cat,
                cod_localizacion = cod_localizacion,
                localizacion = localizacion,
                caracteristicas_list = caracteristicas_list,
                caracteristicas_dict = caracteristicas_dict,
                sudebid_list = sudebid_list,
                sudebid_dict = sudebid_dict,
                mantenimiento = mantenimiento)


@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles_mat():
    #Recuperamos el espacio
    espacio = request.vars['espacio']
    #El nombre del material/consumible
    name = request.vars['nombreMat']

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
        db( (db.sin_bn.sb_espacio == espacio) & (db.sin_bn.sb_nombre == name) ).delete()
        db( (db.modificacion_sin_bn.msb_espacio == espacio) & (db.modificacion_sin_bn.msb_nombre == name) ).delete()
        session.flash = "Solicitud de eliminación aceptada"
        redirect(URL('validaciones'))
    # Si no se elimina
    if request.vars.no:
        db(db.sin_bn.id == bien['id']).select().first().update_record(sb_eliminar = 2)
        session.flash = "Solicitud de eliminación rechazada"
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
    material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
    color = ['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja',
    'Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color']
    unidad_med = ['cm','m']
    movilidad = ['Fijo','Portátil']
    uso = ['Docencia','Investigación','Extensión','Apoyo administrativo']
    nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento', 
                'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
    cod_localizacion = ['150301','240107']
    localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
    'Edo Vargas, Municipio Vargas, Parroquia Macuto']
    unidad_cap = ['m³','l','ml','μl','kg','g','mg','μg','galón','oz','cup','lb']
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
    return dict(bien = bien,
                material_pred = material_pred,
                color_list = color,
                unidad_med = unidad_med,
                movilidad_list = movilidad,
                uso_list = uso,
                nombre_cat = nombre_cat,
                cod_localizacion = cod_localizacion,
                localizacion = localizacion,
                caracteristicas_list = caracteristicas_list,
                caracteristicas_dict = caracteristicas_dict,
                aforado_options = aforado_options,
                unidad_cap = unidad_cap,
                presentacion = presentacion
                )

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def detalles_consumibles():
    #Recuperamos el espacio
    espacio = request.vars['espacio']
    #El nombre del material/consumible
    name = request.vars['nombreMat']

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
        db( (db.sin_bn.sb_espacio == espacio) & (db.sin_bn.sb_nombre == name) ).delete()
        db( (db.modificacion_sin_bn.msb_espacio == espacio) & (db.modificacion_sin_bn.msb_nombre == name) ).delete()
        session.flash = "Solicitud de eliminación aceptada"
        redirect(URL('validaciones'))
    # Si no se elimina
    if request.vars.no:
        db(db.sin_bn.id == bien['id']).select().first().update_record(sb_eliminar = 2)
        db( (db.modificacion_sin_bn.msb_espacio == espacio) & (db.modificacion_sin_bn.msb_nombre == name) ).delete()
        session.flash = "Solicitud de eliminación rechazada"
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
    material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
    color = ['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja',
    'Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color']
    unidad_med = ['cm','m']
    movilidad = ['Fijo','Portátil']
    uso = ['Docencia','Investigación','Extensión','Apoyo administrativo']
    nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento', 
                'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
    cod_localizacion = ['150301','240107']
    localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
    'Edo Vargas, Municipio Vargas, Parroquia Macuto']
    unidad_cap = ['m³','l','ml','μl','kg','g','mg','μg','galón','oz','cup','lb']
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
    return dict(bien = bien,
                material_pred = material_pred,
                color_list = color,
                unidad_med = unidad_med,
                movilidad_list = movilidad,
                uso_list = uso,
                nombre_cat = nombre_cat,
                cod_localizacion = cod_localizacion,
                localizacion = localizacion,
                caracteristicas_list = caracteristicas_list,
                caracteristicas_dict = caracteristicas_dict,
                aforado_options = aforado_options,
                unidad_cap = unidad_cap,
                presentacion = presentacion
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
        db((db.herramienta.hr_nombre == name) & (db.herramienta.hr_espacio_fisico==espacio) & (db.herramienta.hr_ubicacion==ubicacion)).delete()
        db((db.modificacion_herramienta.mhr_nombre == name) & (db.modificacion_herramienta.mhr_espacio_fisico==espacio) & (db.modificacion_herramienta.mhr_ubicacion==ubicacion)).delete()
        session.flash = "Solicitud de eliminación aceptada"
        redirect(URL('validaciones'))
    # Si no se elimina
    if request.vars.no:
        db(db.herramienta.id == bien['id']).select().first().update_record(hr_eliminar = 2)
        db((db.modificacion_herramienta.mhr_nombre == name) & (db.modificacion_herramienta.mhr_espacio_fisico==espacio) & (db.modificacion_herramienta.mhr_ubicacion==ubicacion)).delete()
        session.flash = "Solicitud de eliminación rechazada"
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

    material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
    unidad_med = ['cm','m']
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

    es_tecnico = auth.has_membership("PERSONAL INTERNO")
    direccion_id = __find_dep_id('DIRECCIÓN')

    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    user_dep_id = user.f_dependencia

    if auth.has_membership("PERSONAL INTERNO"):
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

                material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
                color = ['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja',
                'Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color']
                unidad_med = ['cm','m']
                movilidad = ['Fijo','Portátil']
                uso = ['Docencia','Investigación','Extensión','Apoyo administrativo']
                nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento', 
                'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
                cod_localizacion = ['150301','240107']
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

                material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
                color = ['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja',
                'Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color']
                unidad_med = ['cm','m']
                movilidad = ['Fijo','Portátil']
                uso = ['Docencia','Investigación','Extensión','Apoyo administrativo']
                nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento', 
                'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
                cod_localizacion = ['150301','240107']
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
            if not (__is_valid_id(request.vars.dependencia, db.dependencias) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('bienes_muebles'))

            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('bienes_muebles'))

            if request.vars.es_espacio == "True":
        
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

                material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
                color = ['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja',
                'Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color']
                unidad_med = ['cm','m']
                movilidad = ['Fijo','Portátil']
                uso = ['Docencia','Investigación','Extensión','Apoyo administrativo']
                nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento', 
                'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
                cod_localizacion = ['150301','240107']
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
                # Se muestran las dependencias que componen a esta dependencia padre
                # y se lista el inventario agregado
                dep_id = request.vars.dependencia
                dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre
                dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                      ).select(db.dependencias.ALL))
                # Si la lista de dependencias es vacia, entonces la dependencia no 
                # tiene otras dependencias por debajo (podria tener espacios fisicos
                # o estar vacia)
                if len(dependencias) == 0:
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

    es_tecnico = auth.has_membership("PERSONAL INTERNO")
    direccion_id = __find_dep_id('DIRECCIÓN')

    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    user_dep_id = user.f_dependencia

    if auth.has_membership("PERSONAL INTERNO"):
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

                material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
                color = ['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja',
                'Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color']
                unidad_med = ['cm','m']
                movilidad = ['Fijo','Portátil']
                uso = ['Docencia','Investigación','Extensión','Apoyo administrativo']
                nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento', 
                'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
                cod_localizacion = ['150301','240107']
                localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
                'Edo Vargas, Municipio Vargas, Parroquia Macuto']
                unidad_cap = ['m³','l','ml','μl','kg','g','mg','μg','galón','oz','cup','lb']
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

                material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
                color = ['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja',
                'Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color']
                unidad_med = ['cm','m']
                movilidad = ['Fijo','Portátil']
                uso = ['Docencia','Investigación','Extensión','Apoyo administrativo']
                nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento', 
                'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
                cod_localizacion = ['150301','240107']
                localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
                'Edo Vargas, Municipio Vargas, Parroquia Macuto']
                unidad_cap = ['m³','l','ml','μl','kg','g','mg','μg','galón','oz','cup','lb']
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
            if not (__is_valid_id(request.vars.dependencia, db.dependencias) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('material_lab'))

            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('material_lab'))

            if request.vars.es_espacio == "True":
        
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

                material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
                color = ['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja',
                'Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color']
                unidad_med = ['cm','m']
                movilidad = ['Fijo','Portátil']
                uso = ['Docencia','Investigación','Extensión','Apoyo administrativo']
                nombre_cat = ['Maquinaria y demás equipos de construcción, campo, industria y taller', 'Equipos de transporte, tracción y elevación', 'Equipos de comunicaciones y de señalamiento', 
                'Equipos médicos - quirúrgicos, dentales y veterinarios', 'Equipos científicos, religiosos, de enseñanza y recreación', 'Máquinas, muebles y demás equipos de oficina y de alojamiento']
                cod_localizacion = ['150301','240107']
                localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
                'Edo Vargas, Municipio Vargas, Parroquia Macuto']
                unidad_cap = ['m³','l','ml','μl','kg','g','mg','μg','galón','oz','cup','lb']
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
                # Se muestran las dependencias que componen a esta dependencia padre
                # y se lista el inventario agregado
                dep_id = request.vars.dependencia
                dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre
                dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                      ).select(db.dependencias.ALL))
                # Si la lista de dependencias es vacia, entonces la dependencia no 
                # tiene otras dependencias por debajo (podria tener espacios fisicos
                # o estar vacia)
                if len(dependencias) == 0:
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

""" Dado el id de un espacio fisico retorna los materiales que componen
el inventario de ese espacio. """
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


# Muestra las solicitudes de modificacion y eliminacion de acuerdo al cargo del
# usuario y la dependencia que tiene a cargo
@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def validaciones():
# Inicializando listas de espacios fisicos y dependencias

    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    user_dep_id = user.f_dependencia

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

    return dict(inventario=inventario,
                inventario_eliminar = inventario_eliminar) 

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

    es_tecnico = auth.has_membership("TÉCNICO")
    direccion_id = __find_dep_id('DIRECCIÓN')

    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    user_dep_id = user.f_dependencia

    if auth.has_membership("TÉCNICO"):
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
                inventario = __get_inventario_consumibles_espacio(espacio_id)

                material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
                color = ['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja',
                'Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color']
                unidad_med = ['cm','m']
                movilidad = ['Fijo','Portátil']
                uso = ['Docencia','Investigación','Extensión','Apoyo administrativo']
                nombre_cat = ['Maquinaria Construcción', 'Equipo Transporte', 'Equipo Comunicaciones', 
                'Equipo Médico', 'Equipo Científico Religioso', 'Equipo Oficina']
                cod_localizacion = ['150301','240107']
                localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
                'Edo Vargas, Municipio Vargas, Parroquia Macuto']
                unidad_cap = ['m³','l','ml','μl','kg','g','mg','μg','galón','oz','cup','lb']
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

    elif auth.has_membership("JEFE DE SECCIÓN"):
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

                material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
                color = ['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja',
                'Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color']
                unidad_med = ['cm','m']
                movilidad = ['Fijo','Portátil']
                uso = ['Docencia','Investigación','Extensión','Apoyo administrativo']
                nombre_cat = ['Maquinaria Construcción', 'Equipo Transporte', 'Equipo Comunicaciones', 
                'Equipo Médico', 'Equipo Científico Religioso', 'Equipo Oficina']
                cod_localizacion = ['150301','240107']
                localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
                'Edo Vargas, Municipio Vargas, Parroquia Macuto']
                unidad_cap = ['m³','l','ml','μl','kg','g','mg','μg','galón','oz','cup','lb']
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
            inventario = __get_inventario_consumibles_dep(user_dep_id)

    # Si el usuario no es tecnico, para la base de datos es indiferente su ROL
    # pues la jerarquia de dependencias esta almacenada en la misma tabla
    # con una lista de adyacencias
    else:
        # Si el usuario ha seleccionado una dependencia o un espacio fisico
        if request.vars.dependencia:

            # Evaluando la correctitud de los parametros del GET 
            if not (__is_valid_id(request.vars.dependencia, db.dependencias) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('material_lab'))

            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('material_lab'))

            if request.vars.es_espacio == "True":
        
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

                material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
                color = ['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja',
                'Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color']
                unidad_med = ['cm','m']
                movilidad = ['Fijo','Portátil']
                uso = ['Docencia','Investigación','Extensión','Apoyo administrativo']
                nombre_cat = ['Maquinaria Construcción', 'Equipo Transporte', 'Equipo Comunicaciones', 
                'Equipo Médico', 'Equipo Científico Religioso', 'Equipo Oficina']
                cod_localizacion = ['150301','240107']
                localizacion = ['Edo Miranda, Municipio Baruta, Parroquia Baruta',
                'Edo Vargas, Municipio Vargas, Parroquia Macuto']
                unidad_cap = ['m³','l','ml','μl','kg','g','mg','μg','galón','oz','cup','lb']
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
                # Se muestran las dependencias que componen a esta dependencia padre
                # y se lista el inventario agregado
                dep_id = request.vars.dependencia
                dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre
                dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                      ).select(db.dependencias.ALL))
                # Si la lista de dependencias es vacia, entonces la dependencia no 
                # tiene otras dependencias por debajo (podria tener espacios fisicos
                # o estar vacia)
                if len(dependencias) == 0:
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

    es_tecnico = auth.has_membership("TÉCNICO")
    direccion_id = __find_dep_id('DIRECCIÓN')

    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    user_dep_id = user.f_dependencia

    if auth.has_membership("TÉCNICO"):
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

                material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
                unidad_med = ['cm','m']
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

    elif auth.has_membership("JEFE DE SECCIÓN"):
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

                material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
                unidad_med = ['cm','m']
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

            # Evaluando la correctitud de los parametros del GET 
            if not (__is_valid_id(request.vars.dependencia, db.dependencias) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('herramientas'))

            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('herramientas'))

            if request.vars.es_espacio == "True":
        
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

                material_pred = ['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro']
                unidad_med = ['cm','m']
                presentacion=["Unidad", "Conjunto"]

                # Si se esta agregando un nuevo BM, se registra en la DB
                if request.vars.nombre_her: # Verifico si me pasan como argumento el nombre del BM.
                    __agregar_herramienta(
                        request.vars.nombre_her, request.vars.num_her,request.vars.marca_her, request.vars.modelo_her, 
                        request.vars.serial_her, request.vars.presentacion, request.vars.numpiezas_her, request.vars.contenido_her,
                        request.vars.descripcion_her,  request.vars.material_mat,request.vars.unidad, request.vars.ancho_her,
                        request.vars.largo_her, request.vars.alto_her, request.vars.diametro_her, request.vars.ubicacion_int ,
                        request.vars.descripcion_herramientas, espacio, dep_padre_unid_ads, dep_padre_id, user_id)
            else:
                # Se muestran las dependencias que componen a esta dependencia padre
                # y se lista el inventario agregado
                dep_id = request.vars.dependencia
                dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre
                dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                      ).select(db.dependencias.ALL))
                # Si la lista de dependencias es vacia, entonces la dependencia no 
                # tiene otras dependencias por debajo (podria tener espacios fisicos
                # o estar vacia)
                if len(dependencias) == 0:
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
                material_pred = material_pred,
                unidad_med = unidad_med,
                presentacion = presentacion
                ) 
