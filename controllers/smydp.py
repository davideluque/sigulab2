# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# Controladores provisionales utilizados solo para probar las vistas del modulo de SMyDP
#
# - Samuel Arleo <saar1312@gmail.com>
# 
# - Convenciones:
# * Funciones "privadas" utilizadas por los controladores y decoradores tienen el
# prefijo "__"
# * Controladores no poseen prefijos
#
#-----------------------------------------------------------------------------

import datetime

# Verifica si el usuario que intenta acceder al controlador tiene alguno de los
# roles necesarios
def __check_role():

    roles_permitidos = ['WEBMASTER', 'DIRECTOR', 'ASISTENTE DEL DIRECTOR', 
                        'JEFE DE LABORATORIO', 'JEFE DE SECCIÓN', 'TÉCNICO', 
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
    inventario = []
    inventario = list(db((db.t_Inventario.sustancia == db.t_Sustancia.id) &
                         (db.t_Inventario.f_medida == db.t_Unidad_de_medida.id) & 
                         (db.t_Inventario.espacio == espacio_id)).select())

    return inventario

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


# Transforma una cantidad en la unidad de medida indicada en nueva_unidad
def __transformar_cantidad(cantidad, unidad, nueva_unidad):
    cantidad = float(cantidad)
    if nueva_unidad == unidad:
        return cantidad
    elif unidad in ["Kilogramos", "Litros"]:
        return cantidad * 1000
    elif unidad in ["Mililitros", "Gramos"]:
        return cantidad / 1000

# Permite sumar dos cantidades de sustancia de acuerdo a la unidad en la que
# se esta mostrando la cantidad de sustancia en el inventario. *!* Se asume que
# no se agregaran sustancias a los inventarios en unidades diferentes a las normales
# Si es un liquido, se puede pasar de litros a mililitros, pero no se espera
# que se ingrese en algun inventario en gramos. Siempre se pasa a la unidad de 
# medida que ya estaba
def __sumar_cantidad(nueva_cantidad, cantidad_actual, nueva_unidad, unidad):

    if nueva_unidad == unidad:
        return float(nueva_cantidad) + float(cantidad_actual)
    # Si no son iguales y ademas la nueva sustancia esta en Litros o Kilos
    elif nueva_unidad in ["Kilogramos", "Litros"]:
        return float(nueva_cantidad)*1000 + float(cantidad_actual)
    # Si no son iguales y ademas la nueva sustancia esta en Mililitros o gramos
    elif nueva_unidad in ["Mililitros", "Gramos"]:
        return float(nueva_cantidad)/1000 + float(cantidad_actual)


# Agrega los inventarios de los espacios en la lista "espacios"
def __sumar_inventarios(espacios):

    inventario_total = {}
    for esp_id in espacios:
        # Recorriendo las entradas en el inventario que pertenecen al espacio "esp"
        for row in db((db.t_Inventario.sustancia == db.t_Sustancia.id) &
                      (db.t_Inventario.f_medida == db.t_Unidad_de_medida.id) & 
                      (db.t_Inventario.espacio == esp_id)).select():

            sust = row['t_Sustancia']
            inv = row['t_Inventario']
            unid = row['t_Unidad_de_medida']

            sustancia_id = sust.id

            # Se agrega la sustancia al inventario final si esta no estaba ya
            if not sustancia_id in inventario_total:
                
                inventario_total[sustancia_id] = {
                                        'f_nombre': sust.f_nombre,
                                        'f_cas': sust.f_cas,
                                        'f_pureza': sust.f_pureza,
                                        'f_estado': sust.f_estado,
                                        'f_existencia':inv.f_existencia,
                                        'f_uso_interno': inv.f_uso_interno,
                                        'f_unidad': unid.f_nombre
                                                 }
            # Si ya estaba, se suma la cantidad en existencia y de uso interno
            # de la sustancia con id sustancia_id
            else:
                # Inventario actual de la sustancia sustancia_id
                s = inventario_total[sustancia_id]

                # Cantidades existentes por ahora en el inventario general
                existencia = s['f_existencia']
                uso_interno = s['f_uso_interno']

                # Unidad en que se mostrara el inventario general de la sustancia
                unidad = s['f_unidad']

                # Nuevas cantidades que hay que sumar al inventario general
                nueva_exist = inv.f_existencia
                nuevo_uso_interno = inv.f_uso_interno
                nueva_unidad = unid.f_nombre
                
                s['f_existencia'] = __sumar_cantidad(nueva_exist,
                                                    existencia,
                                                    nueva_unidad,
                                                    unidad)
                s['f_uso_interno'] = __sumar_cantidad(nuevo_uso_interno,
                                                     uso_interno,
                                                     nueva_unidad,
                                                     unidad)
                    
    return inventario_total


# Dado el id de una dependencia, retorna una lista con el agregado de las sutancias
# que existen en los espacios fisicos que pertenecen a esta. 
def __get_inventario_dep(dep_id):

    inventario = {}

    # Obteniendo lista de espacios bajo la dependencia con id dep_id
    espacios = __get_espacios(dep_id)

    # Agrega los inventarios de los espacios en la lista "espacios"
    inventario = __sumar_inventarios(espacios)

    return inventario

# Registra una nueva sustancia en el espacio fisico indicado. Si la sustancia ya
# existe en el inventario, genera un mensaje con flash y no anade de nuevo la
# sustancia. 
def __agregar_sustancia(espacio, sustancia_id, total, uso_interno, unidad_id):

    # Si ya existe la sustancia en el inventario
    if db((db.t_Inventario.espacio == espacio.id) & 
          (db.t_Inventario.sustancia == sustancia_id)).select():
        sust = db(db.t_Sustancia.id == sustancia_id).select()[0]

        response.flash = "La sustancia \"{0}\" ya ha sido ingresada anteriormente \
                          al espacio \"{1}\".".format(sust.f_nombre, espacio.nombre)
        return False
    # Si no, se agrega al inventario del espacio fisico la nueva sustancia
    else:
        cantidad = float(total)
        inv_id = db.t_Inventario.insert(f_existencia=cantidad, 
                                f_uso_interno=float(uso_interno),
                                f_medida=unidad_id,
                                espacio=espacio.id,
                                sustancia=sustancia_id)

        concepto = 'Ingreso'
        tipo_ing = 'Ingreso inicial'

        # Agregando la primera entrada de la sustancia en la bitacora
        db.t_Bitacora.insert(
                                f_cantidad=cantidad,
                                f_cantidad_total=cantidad,
                                f_concepto=concepto,
                                f_tipo_ingreso=tipo_ing,
                                f_medida=unidad_id,
                                f_inventario=inv_id,
                                f_sustancia=sustancia_id)

    return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 

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
    if auth.has_membership("TÉCNICO"):
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

# Muestra los movimientos de la bitacora comenzando por el mas reciente
@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def bitacora():

    # INICIO Datos del modal de agregar un registro
    # Conceptos
    conceptos = ['Ingreso','Consumo']

    # Tipos de consumos
    #tipos_egreso = db.t_Bitacora.f_tipo_egreso.requires.other.theset
    tipos_egreso = ['Docencia','Investigación','Extensión']

    # Tipos de ingresos
    #tipos_ingreso = db.t_Bitacora.f_tipo_ingreso.requires.other.theset
    tipos_ingreso = ['Compra','Almacén']

    # Lista de unidades de medida
    unidades_de_medida = list(db(db.t_Unidad_de_medida.id > 0).select())

    # Lista de almacences
    almacenes = db(db.espacios_fisicos.id > 0).select()

    # Lista de servicios
    servicios = db(db.servicios.id > 0).select()
    # FIN Datos del modal de agregar un registro

    # Obteniendo la entrada en t_Personal del usuario conectado

    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]

    if request.vars.inv is None:
        redirect(URL('inventarios'))

    inventario_id = int(request.vars.inv)

    # Si el id de inventario no es valido, retornar al inventario del
    # espacio fisico que se estaba consultando
    if not __is_valid_id(inventario_id, db.t_Inventario):
        response.flash = "La bitácora consultada no es correcta."
        redirect(URL('inventarios'))

    # Inventario al que pertenecen los registros que se desean consultar
    inventario = db((db.t_Inventario.id == inventario_id) & 
                    (db.t_Inventario.espacio == db.espacios_fisicos.id) & 
                    (db.t_Inventario.sustancia == db.t_Sustancia.id)
                   ).select()[0]

    # Espacio al que pertenece la bitacora consultada
    espacio_id = inventario['t_Inventario'].espacio

    # Unidad de medida en que es expresada la sustancia en el inventario
    unidad_medida = db(db.t_Unidad_de_medida.id == inventario.t_Inventario.f_medida
                      ).select()[0]

    # Se valida que el usuario tenga acceso a la bitacora indicada
    # para consultar la bitacora. 
    if not __acceso_permitido(user, espacio_id, "True"):
        redirect(URL('inventarios'))

    sust_nombre = inventario['t_Sustancia'].f_nombre

    espacio_nombre = inventario['espacios_fisicos'].nombre

    bitacora = db((db.t_Bitacora.f_inventario == inventario_id) &
                  (db.t_Bitacora.created_by == db.auth_user.id) &
                  (db.auth_user.id == db.t_Personal.f_usuario) &
                  (db.t_Bitacora.f_medida == db.t_Unidad_de_medida.id)).select()
    
    # *!* Hacer esto cuando se cree el registro y ponerlo en reg['f_descripcion']
    # Obteniendo la descripcion de cada fila y guardandola como un atributo
    for reg in bitacora:
        descripcion = __get_descripcion(reg['t_Bitacora'])
        reg['t_Bitacora']['descripcion'] = descripcion

    # Si se han enviado datos para agregar un nuevo registro
    concepto = request.vars.concepto
    if concepto:
        __agregar_registro(concepto)


    return dict(bitacora=bitacora,
                unidad_medida=unidad_medida,
                inventario=inventario,
                sust_nombre=sust_nombre,
                espacio_nombre=espacio_nombre,
                espacio_id=espacio_id,
                conceptos=conceptos,
                tipos_egreso=tipos_egreso,
                tipos_ingreso=tipos_ingreso,
                unidades_de_medida=unidades_de_medida,
                almacenes=almacenes,
                servicios=servicios)

# Muestra el inventario de acuerdo al cargo del usuario y la dependencia que tiene
# a cargo
@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def inventarios():

    # Inicializando listas de espacios fisicos y dependencias

    # OJO: Espacios debe ser [] siempre que no se este visitando un espacio fisico
    espacios = []
    dependencias = []
    dep_nombre = ""
    dep_padre_id = ""
    dep_padre_nombre = ""

    # Lista de sustancias en el inventario de un espacio fisico o que componen 
    # el inventario agregado de una dependencia
    inventario = []
    
    # Lista de sustancias en el catalogo para el modal de agregar sustancia
    # al alcanzar el nivel de espacios fisicos
    sustancias = []

    # Lista de unidades de medida
    unidades_de_medida = list(db(db.t_Unidad_de_medida.id > 0).select())

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
                    redirect(URL('inventarios'))

                # Determinando si el usuario tiene privilegios suficientes para
                # consultar la dependencia en request.vars.dependencia
                if not __acceso_permitido(user, 
                                    int(request.vars.dependencia), 
                                        request.vars.es_espacio):
                    redirect(URL('inventarios'))

                espacio_id = request.vars.dependencia
                espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                dep_nombre = espacio.nombre

                # Guardando el ID y nombre de la dependencia padre para el link 
                # de navegacion de retorno
                dep_padre_id = espacio.dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre

                espacio_visitado = True

                # Busca el inventario del espacio
                inventario = __get_inventario_espacio(espacio_id)

                sustancias = list(db(db.t_Sustancia.id > 0).select(db.t_Sustancia.ALL))

                # Si se esta agregando una nueva sustancia, se registra en la DB
                if request.vars.sustancia:
                    __agregar_sustancia(espacio,
                                        request.vars.sustancia, 
                                        request.vars.total,
                                        request.vars.uso_interno,
                                        request.vars.unidad)
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

                # Se suman los inventarios de los espacios que tiene a cargo el usuario en la
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

    elif auth.has_membership("JEFE DE SECCIÓN"):
        # Si el jefe de seccion ha seleccionado un espacio fisico
        if request.vars.es_espacio == 'True':
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('inventarios'))

            # Evaluando la correctitud de los parametros del GET 
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('inventarios'))


            espacio_id = request.vars.dependencia
            espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
            dep_nombre = db(db.espacios_fisicos.id == request.vars.dependencia
                           ).select().first().nombre

            # Guardando el ID y nombre de la dependencia a la que pertenece el 
            # espacio fisico visitado
            dep_padre_id = db(db.espacios_fisicos.id == request.vars.dependencia
                             ).select().first().dependencia
            dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                 ).select().first().nombre

            espacio_visitado = True
                            # Se muestra la lista de sustancias que tiene en inventario
            inventario = __get_inventario_espacio(espacio_id)

            sustancias = list(db(db.t_Sustancia.id > 0).select(db.t_Sustancia.ALL))

            # Si se esta agregando una nueva sustancia, se registra en la DB
            if request.vars.sustancia:
                __agregar_sustancia(espacio,
                                    request.vars.sustancia, 
                                    request.vars.total,
                                    request.vars.uso_interno,
                                    request.vars.unidad)


        # Si el jefe de seccion no ha seleccionado un espacio sino que acaba de 
        # regresar a la vista inicial de inventarios
        elif request.vars.es_espacio == 'False':
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                    redirect(URL('inventarios'))
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('inventarios'))
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
                redirect(URL('inventarios'))

            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('inventarios'))

            if request.vars.es_espacio == "True":
        
                # Se muestra el inventario del espacio
                espacio_id = request.vars.dependencia
                espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                dep_nombre = espacio.nombre

                # Guardando el ID y nombre de la dependencia padre para el link 
                # de navegacion de retorno
                dep_padre_id = db(db.espacios_fisicos.id == request.vars.dependencia
                                    ).select().first().dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre

                espacio_visitado = True

                # Se muestra la lista de sustancias que tiene en inventario
                inventario = __get_inventario_espacio(espacio_id)

                sustancias = list(db(db.t_Sustancia.id > 0).select(db.t_Sustancia.ALL))

                # Si se esta agregando una nueva sustancia, se registra en la DB
                if request.vars.sustancia:
                    __agregar_sustancia(espacio,
                                        request.vars.sustancia, 
                                        request.vars.total,
                                        request.vars.uso_interno,
                                        request.vars.unidad)

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
                sustancias=sustancias,
                unidades_de_medida=unidades_de_medida,
                retroceder=retroceder)


@auth.requires_login(otherwise=URL('modulos', 'login'))
def desechos():
    return locals()

#-------------------------------------- Catalogo ---------------------------------------

@auth.requires_login(otherwise=URL('modulos', 'login'))
def catalogo():

    if(auth.has_membership('GESTOR DE SMyDP') or  auth.has_membership('WEBMASTER')):
        table = SQLFORM.smartgrid(  db.t_Sustancia, 
                                    onupdate=auth.archive,
                                    links_in_grid=False,
                                    csv=False,
                                    user_signature=True,
                                    paginate=10)

    else:
        table = SQLFORM.smartgrid(  db.t_Sustancia, 
                                    editable=False,
                                    deletable=False,
                                    csv=False,
                                    links_in_grid=False,
                                    create=False,
                                    paginate=10)
    return locals()


@auth.requires_login(otherwise=URL('modulos', 'login'))
def solicitudes():
    return locals()


@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
    return locals()


@auth.requires_login(otherwise=URL('modulos', 'login'))
def sustancias():
    return locals()

