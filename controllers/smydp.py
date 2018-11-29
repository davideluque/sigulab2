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
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment, Font
import unicodedata
import calendar
import datetime

# Verifica si el usuario que intenta acceder al controlador tiene alguno de los
# roles necesarios
def __check_role():

    roles_permitidos = ['WEBMASTER', 'DIRECTOR', 'ASISTENTE DEL DIRECTOR', 
                        'JEFE DE LABORATORIO', 'JEFE DE SECCIÓN', 'TÉCNICO', 
                        'GESTOR DE SMyDP', 'PERSONAL INTERNO']
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

# Dado el id de un espacio fisico, retorna los desechos peligrosos que componen el inventario
# de ese espacio. Si ningun id es indicado, pero si el de una dependencia, busca
# todos los espacios fisicos que pertenecen a esta, agrega los inventarios y retorna
# la lista
def __get_inventario_desechos(espacio_id=None, dep_id=None):
    inventario = []
    if espacio_id:
        inventario = list(db((db.t_inventario_desechos.grupo == db.t_categoria_desechos.id) &
                         (db.t_inventario_desechos.unidad_medida == db.t_Unidad_de_medida.id) & 
                         (db.t_inventario_desechos.espacio_fisico == espacio_id)).select())
    
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


# consulta los espacios que tienen cierta sustancia
def __consultar_espacios(espacios, sustancia):

    inventario_total = {}
    i = 0
    for esp_id in espacios:
        # Recorriendo las entradas en el inventario que pertenecen al espacio "esp"
        for row in db((db.t_Inventario.sustancia == db.t_Sustancia.id) &
                      (db.t_Inventario.f_medida == db.t_Unidad_de_medida.id) & 
                      (db.t_Inventario.espacio == esp_id)).select():

            esp_actual = db(db.espacios_fisicos.id == esp_id).select().first()

            sust = row['t_Sustancia']
            inv = row['t_Inventario']
            unid = row['t_Unidad_de_medida']

            # Se agrega la sustancia al inventario final
            if sust.f_nombre == sustancia:
                
                i += 1
                inventario_total[int(i)] = {
                                    'f_inv': inv.id,
                                    'f_espacio': esp_actual.codigo,
                                    'f_cas': sust.f_cas,
                                    'f_pureza': sust.f_pureza,
                                    'f_estado': sust.f_estado,
                                    'f_existencia':inv.f_existencia,
                                    'f_uso_interno': inv.f_uso_interno,
                                    'f_unidad': unid.f_nombre
                                             }
                    
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


# Dado el id de una dependencia, retorna una lista con el agregado de las sutancias
# que existen en los espacios fisicos que pertenecen a esta. 
def __solicitar_inventario_dep(dep_id, sustancia):

    inventario = {}

    # Obteniendo lista de espacios bajo la dependencia con id dep_id
    espacios = __get_espacios(dep_id)

    # Agrega los inventarios de los espacios en la lista "espacios"
    inventario = __consultar_espacios(espacios, sustancia)

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
                          al espacio \"{1}\".".format(sust.f_nombre, espacio.codigo)
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
                                f_sustancia=sustancia_id,
                                f_fechaUso=datetime.date.today())

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


        elif registro.f_tipo_ingreso[0] == "Prestamo":
            descripcion = "Ingreso por prestamo "


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


        elif registro.f_tipo_egreso[0] == "Prestamo":
           

            descripcion = "prestamo a .."
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

        fecha_sumi = request.vars.fecha_sumi

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
                f_fechaUso=fecha_sumi,
                f_medida=inv.f_medida,
                f_inventario=inv.id,
                f_sustancia=inv.sustancia,
                f_almacen=almacen)

        elif  tipo_ing == 'Prestamo':
            db.t_Bitacora.insert(
                f_cantidad=cantidad,
                f_cantidad_total=total_nuevo,
                f_concepto=concepto,
                f_tipo_ingreso=tipo_ing,
                f_fechaUso=fecha_sumi,
                f_medida=inv.f_medida,
                f_inventario=inv.id,
                f_sustancia=inv.sustancia)

        elif tipo_ing == 'Cesion':
             db.t_Bitacora.insert(
                f_cantidad=cantidad,
                f_cantidad_total=total_nuevo,
                f_concepto=concepto,
                f_tipo_ingreso=tipo_ing,
                f_fechaUso=fecha_sumi,
                f_medida=inv.f_medida,
                f_inventario=inv.id,
                f_sustancia=inv.sustancia)

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
                f_sustancia=inv.sustancia,
                f_fechaUso=fecha_compra)

    # Si es un tipo Egreso 
    
    else:
        tipo_eg = request.vars.tipo_egreso            
        fecha_uso= request.vars.fecha_uso
       

        
        # Nueva cantidad total luego del consumo
        total_nuevo = total_viejo - cantidad
        if total_nuevo <= 0:
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
            f_fechaUso= fecha_uso,         
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
    tipos_egreso = ['Docencia','Investigación','Extensión','Prestamo','Cesion']

    # Tipos de ingresos
    #tipos_ingreso = db.t_Bitacora.f_tipo_ingreso.requires.other.theset
    tipos_ingreso = ['Compra','Almacén','Prestamo','Cesion']

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

    espacio_nombre = inventario['espacios_fisicos'].codigo

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
def sustancia():

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
    
    sust = request.vars.sust


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
                dep_nombre = espacio.codigo

                # Guardando el ID y nombre de la dependencia padre para el link 
                # de navegacion de retorno
                dep_padre_id = espacio.dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre

                espacio_visitado = True

                # Busca el inventario del espacio
                inventario = __consultar_espacios(espacio_id, sust)

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
                inventario = __consultar_espacios(espacios_ids, sust)

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

            inventario = __consultar_espacios(espacios_ids, sust)

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
                           ).select().first().codigo

            # Guardando el ID y nombre de la dependencia a la que pertenece el 
            # espacio fisico visitado
            dep_padre_id = db(db.espacios_fisicos.id == request.vars.dependencia
                             ).select().first().dependencia
            dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                 ).select().first().nombre

            espacio_visitado = True
                            # Se muestra la lista de sustancias que tiene en inventario
            inventario = __consultar_espacios(espacio_id, sust)

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
            inventario = __consultar_espacios(user_dep_id, sust)

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
                dep_nombre = espacio.codigo

                # Guardando el ID y nombre de la dependencia padre para el link 
                # de navegacion de retorno
                dep_padre_id = db(db.espacios_fisicos.id == request.vars.dependencia
                                    ).select().first().dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre

                espacio_visitado = True

                # Se muestra la lista de sustancias que tiene en inventario
                inventario = __consultar_espacios(espacio_id, sust)

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
                inventario = __solicitar_inventario_dep(dep_id, sust)

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
            inventario = __solicitar_inventario_dep(dep_id, sust)

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
                unidades_de_medida=unidades_de_medida,
                retroceder=retroceder
                )


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
                dep_nombre = espacio.codigo

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
                           ).select().first().codigo

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
                dep_nombre = espacio.codigo

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

########################################
#         ENVASES/CONTENEDORES         #
# FUNCIONES AUXILIARES Y CONTROLADORES #
########################################
@auth.requires_login(otherwise=URL('modulos', 'login'))
def envases():
    user_id = auth.user_id

    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_dep_id = user.f_dependencia

    categorias_de_desecho = []
    contenedores = []
    espacios_fisicos_adscritos = []
    unidades_de_medida = []

    formas = ['Cilíndrica', 'Cuadrada', 'Rectangular', 'Otra']
    materiales = ['Plástico', 'Polietileno (HDPE)', 'Polietileno (PE)', 'Vidrio', 'Metal', 'Acero', 'Otro']
    tipos_de_boca = ['Boca ancha', 'Boca angosta', 'Cerrados con abertura de trasvase', 'Otra']

    categorias_de_desecho = list(db(db.t_categoria_desechos).select(db.t_categoria_desechos.ALL))

    # Listas de espacios físicos de los cuáles el usuario logueado es responsable
    # Si el usuario es un gestor o webmaster, puede crear envases en cualquier espacio físico
    if(auth.has_membership('GESTOR DE SMyDP') or  auth.has_membership('WEBMASTER') or auth.has_membership('DIRECTOR') or auth.has_membership('ASISTENTE DEL DIRECTOR') or auth.has_membership("PERSONAL INTERNO")):
        contenedores = list(db(db.t_envases).select(db.t_envases.ALL))
        espacios_fisicos_adscritos = list(db(
            (db.espacios_fisicos)
        ).select(db.espacios_fisicos.id, db.espacios_fisicos.codigo)) 

    elif(auth.has_membership('TÉCNICO') or auth.has_membership('JEFE DE LABORATORIO')):
        #pero si no es un gestor o webmaster, solamente puede crear contenedores en los espacios físicos en donde tiene
        #jurisdicción
        contenedores = list(db(
            (db.t_envases.espacio_fisico == db.espacios_fisicos.id) &
            (db.espacios_fisicos.dependencia == db.dependencias.id ) &
            (db.dependencias.unidad_de_adscripcion == user_dep_id) 
        ).select(db.t_envases.ALL))

        espacios_fisicos_adscritos = list(db(
            (db.espacios_fisicos.dependencia == db.dependencias.id) &
            (db.dependencias.unidad_de_adscripcion == user_dep_id) 
        ).select(db.espacios_fisicos.id, db.espacios_fisicos.codigo)) 

    elif auth.has_membership('JEFE DE SECCIÓN'):
        #pero si no es un gestor o webmaster, solamente puede crear contenedores en los espacios físicos en donde tiene
        #jurisdicción
        contenedores = list(db(
            (db.t_envases.espacio_fisico == db.espacios_fisicos.id) &
            (db.espacios_fisicos.dependencia == user_dep_id)
        ).select(db.t_envases.ALL))

        espacios_fisicos_adscritos = list(db(
            (db.espacios_fisicos.dependencia == user_dep_id)
        ).select(db.espacios_fisicos.id, db.espacios_fisicos.codigo)) 


    unidades_de_medida = list(db(db.t_Unidad_de_medida).select(db.t_Unidad_de_medida.ALL))

    # El formulario de edición/creación de un envase se ha recibido
    if request.vars.capacidad:

        envase = {}

        marcado_para_borrar = False

        if request.vars.borrar_envase == 'True':
            marcado_para_borrar = True

        # Verifica si el elemento fue marcado para ser borrado
        if marcado_para_borrar:
            response.flash = __eliminar_envase(int(request.vars.id_envase))
            session.flash = response.flash
            return redirect(URL(host=True)) 

        else:
            #De lo contrario debe ser creado o actualizado
            id_envase = -1

            if request.vars.id_envase != '':
                id_envase = int(request.vars.id_envase)
            
            response.flash = __agregar_envase(
                request.vars.identificacion,
                float(str(request.vars.capacidad).replace(",", ".")),
                int(request.vars.unidad_medida),
                request.vars.forma,
                request.vars.material,
                request.vars.tipo_boca,
                request.vars.descripcion,
                request.vars.composicion,
                int(request.vars.espacio_fisico),
                int(request.vars.categoria),
                id_envase
            )

            session.flash = response.flash
            return redirect(URL(host=True)) 

    return locals()


def __agregar_envase(identificacion, capacidad, unidad_medida, forma, material, tipo_boca, descripcion, composicion, espacio_fisico, categoria, id_envase):
    # Si el id_envase es distinto de -1, es porque ya existe el envase y se va a actualizar su informacion
    if id_envase != -1:
        if len(list(db((db.t_envases.identificacion == identificacion) & (db.t_envases.id != id_envase)).select())) > 0:
            return T("La identificación que proporcionó para el contenedor ya se encuentra en uso.")
        else:
            db(db.t_envases.id == id_envase).update(
                identificacion = identificacion.upper(),
                capacidad = capacidad, 
                unidad_medida = unidad_medida, 
                forma = forma.upper(), 
                material = material.upper(), 
                tipo_boca = tipo_boca.upper(), 
                descripcion = descripcion.upper(), 
                composicion = composicion, 
                espacio_fisico = espacio_fisico, 
                categoria = categoria
            )

            return T("La información del contenedor se ha modificado exitosamente.")
        
    else:
        # Se verifica si la identificación del envase que se quiere crear fue previamente utilizada
        if len(list(db(db.t_envases.identificacion == identificacion).select())) > 0:
            return T("La identificación que proporcionó para el contenedor ya se encuentra en uso.")
            
        else:
            #De lo contrario, el envase aún no existe y se tiene que crear
            db.t_envases.insert(
                identificacion = identificacion.upper(),
                capacidad = capacidad, 
                unidad_medida = unidad_medida, 
                forma = forma.upper(), 
                material = material.upper(), 
                tipo_boca = tipo_boca.upper(), 
                descripcion = descripcion.upper(), 
                composicion = composicion, 
                espacio_fisico = espacio_fisico, 
                categoria = categoria
            )

            return T("Contenedor creado exitosamente.")

def __eliminar_desecho(id_desecho):
    db(db.t_inventario_desechos.id == id_desecho).delete()
    return T("Desecho eliminado exitosamente.")

def __eliminar_envase(id_envase):
    db(db.t_envases.id == id_envase).delete()
    return T("Contenedor eliminado exitosamente.")

########################################
#         CATEGORIAS DE DESECHOS       #
# FUNCIONES AUXILIARES Y CONTROLADORES #
########################################
@auth.requires_login(otherwise=URL('modulos', 'login'))
def categorias_desechos():
    categorias = []

    if(auth.has_membership('GESTOR DE SMyDP') or  auth.has_membership('WEBMASTER')):
        categorias = list(db(db.t_categoria_desechos
                                  ).select(db.t_categoria_desechos.ALL))
        # El formulario de edición/creación de categoria se ha recibido
        if request.vars.categoria:
            marcado_para_borrar = False

            if request.vars.borrar_categoria == 'True':
                marcado_para_borrar = True

            # Verifica si el elemento fue marcado para ser borrado
            if marcado_para_borrar:
                
                response.flash = __eliminar_categoria(int(request.vars.id_categoria))
                session.flash = response.flash
                return redirect(URL(host=True)) 
            else:
                #De lo contrario debe ser creado o actualizado
                id_categoria = -1

                if request.vars.id_categoria != '':
                    id_categoria = int(request.vars.id_categoria)
                
                response.flash = __agregar_categoria(request.vars.categoria, request.vars.descripcion, id_categoria)
                session.flash = response.flash
                return redirect(URL(host=True)) 

    else:
        categorias = list(db(db.t_categoria_desechos
                                  ).select(db.t_categoria_desechos.ALL))
    return locals()


def __agregar_categoria(nombre_categoria, descripcion_categoria, id_categoria):
    # Si el id_categoria es distinto de -1, es porque ya exista la categoría y se va a actualizar
    if id_categoria != -1:
        db(db.t_categoria_desechos.id == id_categoria).update(categoria = nombre_categoria.upper(), descripcion = descripcion_categoria.upper())
    else:
        # Se verifica que la categoría no exista previamente
        if(len(list(db(db.t_categoria_desechos.categoria == nombre_categoria).select())) > 0):
            return T("La categoría que intenta agregar ya existe")
        else:
            #De lo contrario, la categoría no existe y se tiene que crear
            db.t_categoria_desechos.insert(categoria = nombre_categoria.upper(), descripcion = descripcion_categoria.upper())
            return T("Categoría agregada exitosamente")
            



def __eliminar_categoria(categoria_id):
    db(db.t_categoria_desechos.id == categoria_id).delete()
    return T("Categoría de desecho eliminada exitosamente.")


# @auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def inventarios_desechos():
    # Inicializando listas de espacios fisicos y dependencias

    # OJO: Espacios debe ser [] siempre que no se este visitando un espacio fisico
    espacios = []
    dependencias = []
    dep_nombre = ""
    dep_padre_id = ""
    dep_padre_nombre = ""
    envases = []
    envases_totales = []
    inventario_total = []
    # Este valor indica si se muestra el campo "Dependencia" en la tabla del inventario 
    # si se esta visitando el menu principal del inventario, o si se está visitando una sección
    mostrar_campo_dependencia = False 

    # Lista de sustancias en el inventario de un espacio fisico o que componen 
    # el inventario agregado de una dependencia
    inventario = []
    
    # Lista de sustancias en el catalogo para el modal de agregar sustancia
    # al alcanzar el nivel de espacios fisicos
    desechos = []

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

    if(auth.has_membership('GESTOR DE SMyDP') or  auth.has_membership('WEBMASTER') or auth.has_membership('DIRECTOR') or auth.has_membership('ASISTENTE DEL DIRECTOR')):
        # Si el usuario ha seleccionado una dependencia o un espacio fisico
        if request.vars.dependencia:
            if request.vars.es_espacio == "True":
                # Se muestra el inventario del espacio
                espacio_id = request.vars.dependencia
                espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                dep_nombre = espacio.codigo

                # Guardando el ID y nombre de la dependencia padre para el link 
                # de navegacion de retorno
                dep_padre_id = db(db.espacios_fisicos.id == request.vars.dependencia
                                    ).select().first().dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre

                espacio_visitado = True

                # Se muestra la lista de sustancias que tiene en inventario

                inventario = list(db(
                    (db.espacios_fisicos.id == espacio_id) &
                    (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                    (db.espacios_fisicos.id == db.t_inventario_desechos.espacio_fisico)
                    ).select(
                    db.t_inventario_desechos.categoria,
                    db.t_inventario_desechos.id,
                    db.t_inventario_desechos.composicion, 
                    db.t_inventario_desechos.cantidad.sum(),
                    db.t_inventario_desechos.responsable,
                    db.t_inventario_desechos.envase,
                    db.t_inventario_desechos.unidad_medida,
                    db.t_inventario_desechos.peligrosidad,
                    db.t_inventario_desechos.tratamiento,
                    groupby = 
                     db.t_inventario_desechos.categoria |  
                    db.t_inventario_desechos.id | 
                     db.t_inventario_desechos.composicion | 
                     db.t_inventario_desechos.responsable |
                     db.t_inventario_desechos.unidad_medida |
                     db.t_inventario_desechos.peligrosidad |
                     db.t_inventario_desechos.tratamiento |
                     db.t_inventario_desechos.envase
                ))

                inventario_total = list(db(
                    (db.espacios_fisicos.id == espacio_id) &
                    (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                    (db.espacios_fisicos.id == db.t_inventario_desechos.espacio_fisico)
                    ).select())

                ####################
                # A T E N C I Ó N  #
                ####################
                # Cuando se va a subir el sistema a produccion, descomentar la linea que dice "t_bitacora_desecho" y comentar la que dice "t_Bitacora_desecho"
                # Analogamente, comentar la línea correcta cuando se está en ambiente de desarrollo
                envases = list(db.executesql('SELECT * from t_envases e where e.espacio_fisico = ' + espacio_id + ' and e.id not in (select entrada.envase from "t_Bitacora_desechos" entrada);', as_dict = True))
                #envases = list(db.executesql('SELECT * from t_envases e where e.espacio_fisico = ' + espacio_id + ' and e.id not in (select entrada.envase from "t_bitacora_desechos" entrada);', as_dict = True))

                envases_totales = list(db.executesql('SELECT * from t_envases e where e.espacio_fisico = ' + espacio_id + ';', as_dict = True))
                
                # Se quiere eliminar un desecho
                print request.vars
                if request.vars.view and request.vars.borrar_desecho:
                    marcado_para_borrar = False
                    print request.vars
                    if request.vars.borrar_desecho == 'True':
                        print "marcado para borrar = true"
                        marcado_para_borrar = True

                    # Verifica si el elemento fue marcado para ser borrado
                    if marcado_para_borrar:
                        print "se va a borrar"
                        response.flash = __eliminar_desecho(int(request.vars.view))
                        print "ya se tuvo que haber borrado"
                        session.flash = response.flash
                        return redirect(URL('..', 'sigulab2', 'smydp/inventarios_desechos', vars=dict(dependencia=request.vars.dependencia, es_espacio="True"))) 


                # Se esta editando el detalle de un desecho
                if request.vars.view and request.vars.envase:
                    envase = db(db.t_envases.id == int(request.vars.envase)).select().first()
                    
                    response.flash = __actualizar_desecho(request.vars.view, envase, request.vars.peligrosidad, request.vars.tratamiento, request.vars.concentracion)
                    session.flash = response.flash
                    return redirect(URL('..', 'sigulab2', 'smydp/inventarios_desechos', vars=dict(dependencia=request.var.dependencia, es_espacio="True", view=request.vars.view))) 
                
                else:
                    # Si se esta agregando un nuevo desecho, se registra en la DB
                    if request.vars.envase:

                        #Se busca la información del envase en la DB
                        envase = list(db(db.t_envases.id == request.vars.envase).select())

                        response.flash =__agregar_desecho(envase[0],
                                            request.vars.peligrosidad,
                                            request.vars.tratamiento,
                                            request.vars.cantidad,
                                            request.vars.concentracion
                        )

                        session.flash = response.flash
                        return redirect(URL(host=True)) 

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
                    
                    inventario = list(db(
                        (db.t_inventario_desechos.seccion == request.vars.dependencia)).select())

                    inventario = list(db(
                    (db.dependencias.id == dep_id) & 
                    (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                    (db.espacios_fisicos.id == db.t_inventario_desechos.espacio_fisico)
                    ).select(
                    db.t_inventario_desechos.categoria,
                    db.t_inventario_desechos.espacio_fisico,
                    db.t_inventario_desechos.seccion,
                    db.t_inventario_desechos.id,
                    db.t_inventario_desechos.cantidad.sum(),
                    db.t_inventario_desechos.unidad_medida,
                    db.t_inventario_desechos.responsable,
                    groupby = 
                     db.t_inventario_desechos.categoria |
                     db.t_inventario_desechos.espacio_fisico |
                        db.t_inventario_desechos.id | 
                    db.t_inventario_desechos.seccion |
                    db.t_inventario_desechos.unidad_medida | 
                    db.t_inventario_desechos.responsable
                    ))

                    es_espacio = True
                
                else:
                    inventario = list(db(
                    (db.t_inventario_desechos.espacio_fisico == db.espacios_fisicos.id) &
                        (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                        (db.dependencias.unidad_de_adscripcion == request.vars.dependencia)
                    ).select(
                    db.t_inventario_desechos.categoria,
                    db.t_inventario_desechos.id,
                    db.t_inventario_desechos.espacio_fisico,
                    db.t_inventario_desechos.seccion,
                    db.t_inventario_desechos.cantidad.sum(),
                    db.t_inventario_desechos.unidad_medida,
                    db.t_inventario_desechos.responsable,
                    groupby = 
                     db.t_inventario_desechos.categoria |
                        db.t_inventario_desechos.id | 
                     db.t_inventario_desechos.espacio_fisico |
                     db.t_inventario_desechos.seccion |
                    db.t_inventario_desechos.unidad_medida | 
                    db.t_inventario_desechos.responsable
                    ))

                    mostrar_campo_dependencia = True

                # Guardando el ID y nombre de la dependencia padre para el link 
                # de navegacion de retorno
                dep_padre_id = db(db.dependencias.id == request.vars.dependencia
                                 ).select().first().unidad_de_adscripcion
                # Si dep_padre_id es None, se ha llegado al tope de la jerarquia
                # y no hay un padre de este nodo
                if dep_padre_id:
                    dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                         ).select().first().nombre


        else:
            # Dependencia a la que pertenece el usuario o que tiene a cargo
            dep_id = user.f_dependencia
            dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre

            # Se muestran las dependencias que componen a la dependencia que
            # tiene a cargo el usuario y el inventario agregado de esta
            dependencias = list(db(db.dependencias.nombre.startswith('LAB')).select(db.dependencias.ALL))

            # Se muestra como inventario el egregado de los inventarios que
            # pertenecen a la dependencia del usuario
            inventario = list(db(
                (db.t_inventario_desechos.espacio_fisico == db.espacios_fisicos.id) &
                (db.espacios_fisicos.dependencia == db.dependencias.id)
                ).select(
                db.t_inventario_desechos.categoria,
                db.t_inventario_desechos.espacio_fisico,
                db.t_inventario_desechos.id,
                db.t_inventario_desechos.seccion,
                db.t_inventario_desechos.cantidad.sum(),
                db.t_inventario_desechos.unidad_medida,
                db.t_inventario_desechos.responsable,
                groupby = 
                    db.t_inventario_desechos.categoria |
                    db.t_inventario_desechos.espacio_fisico |
                    db.t_inventario_desechos.id | 
                    db.t_inventario_desechos.seccion |
                db.t_inventario_desechos.unidad_medida | 
                db.t_inventario_desechos.responsable
                ))

            mostrar_campo_dependencia = True

    elif(auth.has_membership("TÉCNICO") or auth.has_membership("JEFE DE LABORATORIO")):
        # Si el usuario ha seleccionado una dependencia o un espacio fisico
        if request.vars.dependencia:
            if request.vars.es_espacio == "True":
                # Si se está editando un desecho, se actualiza la informacion
                if request.vars.es_espacio == "True":
                    # Se muestra el inventario del espacio
                    espacio_id = request.vars.dependencia
                    espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                    dep_nombre = espacio.codigo

                    # Guardando el ID y nombre de la dependencia padre para el link 
                    # de navegacion de retorno
                    dep_padre_id = db(db.espacios_fisicos.id == request.vars.dependencia
                                        ).select().first().dependencia
                    dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                        ).select().first().nombre

                    espacio_visitado = True

                    # Se muestra la lista de sustancias que tiene en inventario

                    inventario = list(db(
                        (db.espacios_fisicos.id == espacio_id) &
                        (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                        (db.espacios_fisicos.id == db.t_inventario_desechos.espacio_fisico)
                        ).select(
                        db.t_inventario_desechos.categoria,
                        db.t_inventario_desechos.id,
                        db.t_inventario_desechos.composicion, 
                        db.t_inventario_desechos.cantidad.sum(),
                        db.t_inventario_desechos.responsable,
                        db.t_inventario_desechos.envase,
                        db.t_inventario_desechos.unidad_medida,
                        db.t_inventario_desechos.peligrosidad,
                        db.t_inventario_desechos.tratamiento,
                        groupby = 
                        db.t_inventario_desechos.categoria |  
                        db.t_inventario_desechos.id | 
                        db.t_inventario_desechos.composicion | 
                        db.t_inventario_desechos.responsable |
                        db.t_inventario_desechos.unidad_medida |
                        db.t_inventario_desechos.peligrosidad |
                        db.t_inventario_desechos.tratamiento |
                        db.t_inventario_desechos.envase
                    ))

                    inventario_total = list(db(
                        (db.espacios_fisicos.id == espacio_id) &
                        (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                        (db.espacios_fisicos.id == db.t_inventario_desechos.espacio_fisico)
                        ).select())

                    ####################
                    # A T E N C I Ó N  #
                    ####################
                    # Cuando se va a subir el sistema a produccion, descomentar la linea que dice "t_bitacora_desecho" y comentar la que dice "t_Bitacora_desecho"
                    # Analogamente, comentar la línea correcta cuando se está en ambiente de desarrollo
                    envases = list(db.executesql('SELECT * from t_envases e where e.espacio_fisico = ' + espacio_id + ' and e.id not in (select entrada.envase from "t_Bitacora_desechos" entrada);', as_dict = True))
                    #envases = list(db.executesql('SELECT * from t_envases e where e.espacio_fisico = ' + espacio_id + ' and e.id not in (select entrada.envase from "t_bitacora_desechos" entrada);', as_dict = True))

                    envases_totales = list(db.executesql('SELECT * from t_envases e where e.espacio_fisico = ' + espacio_id + ';', as_dict = True))
                    
                    # Se esta editando el detalle de un desecho
                    if request.vars.view and request.vars.envase:
                        envase = db(db.t_envases.id == int(request.vars.envase)).select().first()
                        
                        response.flash = __actualizar_desecho(request.vars.view, envase, request.vars.peligrosidad, request.vars.tratamiento, request.vars.concentracion)
                        session.flash = response.flash
                        return redirect(URL(host=True)) 
                    else:
                        # Si se esta agregando un nuevo desecho, se registra en la DB
                        if request.vars.envase:

                            #Se busca la información del envase en la DB
                            envase = list(db(db.t_envases.id == request.vars.envase).select())

                            response.flash = __agregar_desecho(envase[0],
                                                request.vars.peligrosidad,
                                                request.vars.tratamiento,
                                                request.vars.cantidad,
                                                request.vars.concentracion
                            )

                            session.flash = response.flash
                            return redirect(URL(host=True)) 

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
                        
                        inventario = list(db(
                            (db.t_inventario_desechos.seccion == request.vars.dependencia)).select())

                        inventario = list(db(
                        (db.dependencias.id == dep_id) & 
                        (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                        (db.espacios_fisicos.id == db.t_inventario_desechos.espacio_fisico)
                        ).select(
                        db.t_inventario_desechos.categoria,
                        db.t_inventario_desechos.espacio_fisico,
                        db.t_inventario_desechos.seccion,
                        db.t_inventario_desechos.id,
                        db.t_inventario_desechos.cantidad.sum(),
                        db.t_inventario_desechos.unidad_medida,
                        db.t_inventario_desechos.responsable,
                        groupby = 
                        db.t_inventario_desechos.categoria |
                        db.t_inventario_desechos.espacio_fisico |
                            db.t_inventario_desechos.id | 
                        db.t_inventario_desechos.seccion |
                        db.t_inventario_desechos.unidad_medida | 
                        db.t_inventario_desechos.responsable
                        ))

                        es_espacio = True
                    
                    else:
                        inventario = list(db(
                        (db.t_inventario_desechos.espacio_fisico == db.espacios_fisicos.id) &
                            (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                            (db.dependencias.unidad_de_adscripcion == request.vars.dependencia)
                        ).select(
                        db.t_inventario_desechos.categoria,
                        db.t_inventario_desechos.id,
                        db.t_inventario_desechos.espacio_fisico,
                        db.t_inventario_desechos.seccion,
                        db.t_inventario_desechos.cantidad.sum(),
                        db.t_inventario_desechos.unidad_medida,
                        db.t_inventario_desechos.responsable,
                        groupby = 
                        db.t_inventario_desechos.categoria |
                            db.t_inventario_desechos.id | 
                        db.t_inventario_desechos.espacio_fisico |
                        db.t_inventario_desechos.seccion |
                        db.t_inventario_desechos.unidad_medida | 
                        db.t_inventario_desechos.responsable
                        ))

                        mostrar_campo_dependencia = True

                    # Guardando el ID y nombre de la dependencia padre para el link 
                    # de navegacion de retorno
                    dep_padre_id = db(db.dependencias.id == request.vars.dependencia
                                    ).select().first().unidad_de_adscripcion
                    # Si dep_padre_id es None, se ha llegado al tope de la jerarquia
                    # y no hay un padre de este nodo
                    if dep_padre_id:
                        dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                            ).select().first().nombre

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
                    
                    inventario = list(db(
                        (db.t_inventario_desechos.seccion == request.vars.dependencia)).select())

                    inventario = list(db(
                    (db.dependencias.id == dep_id) & 
                    (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                    (db.espacios_fisicos.id == db.t_inventario_desechos.espacio_fisico)
                    ).select(
                    db.t_inventario_desechos.categoria,
                    db.t_inventario_desechos.espacio_fisico,
                    db.t_inventario_desechos.seccion,
                    db.t_inventario_desechos.id,
                    db.t_inventario_desechos.cantidad.sum(),
                    db.t_inventario_desechos.unidad_medida,
                    db.t_inventario_desechos.responsable,
                    groupby = 
                     db.t_inventario_desechos.categoria |
                     db.t_inventario_desechos.espacio_fisico |
                        db.t_inventario_desechos.id | 
                    db.t_inventario_desechos.seccion |
                    db.t_inventario_desechos.unidad_medida | 
                    db.t_inventario_desechos.responsable
                    ))


                    es_espacio = True
                
                else:
                    inventario = list(db(
                    (db.t_inventario_desechos.espacio_fisico == db.espacios_fisicos.id) &
                        (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                        (db.dependencias.unidad_de_adscripcion == request.vars.dependencia)
                    ).select(
                    db.t_inventario_desechos.categoria,
                    db.t_inventario_desechos.id,
                    db.t_inventario_desechos.espacio_fisico,
                    db.t_inventario_desechos.seccion,
                    db.t_inventario_desechos.cantidad.sum(),
                    db.t_inventario_desechos.unidad_medida,
                    db.t_inventario_desechos.responsable,
                    groupby = 
                     db.t_inventario_desechos.categoria |
                        db.t_inventario_desechos.id | 
                     db.t_inventario_desechos.espacio_fisico |
                     db.t_inventario_desechos.seccion |
                    db.t_inventario_desechos.unidad_medida | 
                    db.t_inventario_desechos.responsable
                    ))

                    mostrar_campo_dependencia = True

                # Guardando el ID y nombre de la dependencia padre para el link 
                # de navegacion de retorno
                dep_padre_id = db(db.dependencias.id == request.vars.dependencia
                                 ).select().first().unidad_de_adscripcion
                # Si dep_padre_id es None, se ha llegado al tope de la jerarquia
                # y no hay un padre de este nodo
                if dep_padre_id:
                    dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                         ).select().first().nombre


        else:
            # Dependencia a la que pertenece el usuario o que tiene a cargo
            dep_id = user.f_dependencia
            dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre

            # Se muestran las dependencias que componen a la dependencia que
            # tiene a cargo el usuario y el inventario agregado de esta
            dependencias = list(db(
                (db.dependencias.unidad_de_adscripcion == dep_id)
            ).select(db.dependencias.ALL))

            # Se muestra como inventario el egregado de los inventarios que
            # pertenecen a la dependencia del usuario

            inventario = list(db(
                (db.t_inventario_desechos.espacio_fisico == db.espacios_fisicos.id) &
                (db.espacios_fisicos.dependencia == db.dependencias.id) &
                (db.dependencias.unidad_de_adscripcion == dep_id)
                ).select(
                db.t_inventario_desechos.categoria,
                db.t_inventario_desechos.espacio_fisico,
                db.t_inventario_desechos.id,
                db.t_inventario_desechos.seccion,
                db.t_inventario_desechos.cantidad.sum(),
                db.t_inventario_desechos.unidad_medida,
                db.t_inventario_desechos.responsable,
                groupby = 
                    db.t_inventario_desechos.categoria |
                    db.t_inventario_desechos.espacio_fisico |
                    db.t_inventario_desechos.id | 
                    db.t_inventario_desechos.seccion |
                db.t_inventario_desechos.unidad_medida | 
                db.t_inventario_desechos.responsable
                ))

            mostrar_campo_dependencia = True
            espacio_visitado = False

    elif auth.has_membership("JEFE DE SECCIÓN") or auth.has_membership("PERSONAL INTERNO") :
        # Si el usuario ha seleccionado una dependencia o un espacio fisico
        if request.vars.dependencia:
            if request.vars.es_espacio == "True":
                # Si se está editando un desecho, se actualiza la informacion
                if request.vars.es_espacio == "True":
                    # Se muestra el inventario del espacio
                    espacio_id = request.vars.dependencia
                    espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                    dep_nombre = espacio.codigo

                    # Guardando el ID y nombre de la dependencia padre para el link 
                    # de navegacion de retorno
                    dep_padre_id = db(db.espacios_fisicos.id == request.vars.dependencia
                                        ).select().first().dependencia
                    dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                        ).select().first().nombre

                    espacio_visitado = True

                    # Se muestra la lista de sustancias que tiene en inventario

                    inventario = list(db(
                        (db.espacios_fisicos.id == espacio_id) &
                        (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                        (db.espacios_fisicos.id == db.t_inventario_desechos.espacio_fisico)
                        ).select(
                        db.t_inventario_desechos.categoria,
                        db.t_inventario_desechos.id,
                        db.t_inventario_desechos.composicion, 
                        db.t_inventario_desechos.cantidad.sum(),
                        db.t_inventario_desechos.responsable,
                        db.t_inventario_desechos.envase,
                        db.t_inventario_desechos.unidad_medida,
                        db.t_inventario_desechos.peligrosidad,
                        db.t_inventario_desechos.tratamiento,
                        groupby = 
                        db.t_inventario_desechos.categoria |  
                        db.t_inventario_desechos.id | 
                        db.t_inventario_desechos.composicion | 
                        db.t_inventario_desechos.responsable |
                        db.t_inventario_desechos.unidad_medida |
                        db.t_inventario_desechos.peligrosidad |
                        db.t_inventario_desechos.tratamiento |
                        db.t_inventario_desechos.envase
                    ))

                    inventario_total = list(db(
                        (db.espacios_fisicos.id == espacio_id) &
                        (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                        (db.espacios_fisicos.id == db.t_inventario_desechos.espacio_fisico)
                        ).select())

                    ####################
                    # A T E N C I Ó N  #
                    ####################
                    # Cuando se va a subir el sistema a produccion, descomentar la linea que dice "t_bitacora_desecho" y comentar la que dice "t_Bitacora_desecho"
                    # Analogamente, comentar la línea correcta cuando se está en ambiente de desarrollo
                    envases = list(db.executesql('SELECT * from t_envases e where e.espacio_fisico = ' + espacio_id + ' and e.id not in (select entrada.envase from "t_Bitacora_desechos" entrada);', as_dict = True))
                    #envases = list(db.executesql('SELECT * from t_envases e where e.espacio_fisico = ' + espacio_id + ' and e.id not in (select entrada.envase from "t_bitacora_desechos" entrada);', as_dict = True))

                    envases_totales = list(db.executesql('SELECT * from t_envases e where e.espacio_fisico = ' + espacio_id + ';', as_dict = True))
                    
                    # Se esta editando el detalle de un desecho
                    if request.vars.view and request.vars.envase:
                        envase = db(db.t_envases.id == int(request.vars.envase)).select().first()
                        
                        response.flash = __actualizar_desecho(request.vars.view, envase, request.vars.peligrosidad, request.vars.tratamiento, request.vars.concentracion)
                        session.flash = response.flash
                        return redirect(URL(host=True)) 
                    else:
                        # Si se esta agregando un nuevo desecho, se registra en la DB
                        if request.vars.envase:

                            #Se busca la información del envase en la DB
                            envase = list(db(db.t_envases.id == request.vars.envase).select())

                            response.flash = __agregar_desecho(envase[0],
                                                request.vars.peligrosidad,
                                                request.vars.tratamiento,
                                                request.vars.cantidad,
                                                request.vars.concentracion
                            )

                            session.flash = response.flash
                            return redirect(URL(host=True)) 

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
                        
                        inventario = list(db(
                            (db.t_inventario_desechos.seccion == request.vars.dependencia)).select())

                        inventario = list(db(
                        (db.dependencias.id == dep_id) & 
                        (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                        (db.espacios_fisicos.id == db.t_inventario_desechos.espacio_fisico)
                        ).select(
                        db.t_inventario_desechos.categoria,
                        db.t_inventario_desechos.espacio_fisico,
                        db.t_inventario_desechos.seccion,
                        db.t_inventario_desechos.id,
                        db.t_inventario_desechos.cantidad.sum(),
                        db.t_inventario_desechos.unidad_medida,
                        db.t_inventario_desechos.responsable,
                        groupby = 
                        db.t_inventario_desechos.categoria |
                        db.t_inventario_desechos.espacio_fisico |
                            db.t_inventario_desechos.id | 
                        db.t_inventario_desechos.seccion |
                        db.t_inventario_desechos.unidad_medida | 
                        db.t_inventario_desechos.responsable
                        ))

                        es_espacio = True
                    
                    else:
                        inventario = list(db(
                        (db.t_inventario_desechos.espacio_fisico == db.espacios_fisicos.id) &
                            (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                            (db.dependencias.unidad_de_adscripcion == request.vars.dependencia)
                        ).select(
                        db.t_inventario_desechos.categoria,
                        db.t_inventario_desechos.id,
                        db.t_inventario_desechos.espacio_fisico,
                        db.t_inventario_desechos.seccion,
                        db.t_inventario_desechos.cantidad.sum(),
                        db.t_inventario_desechos.unidad_medida,
                        db.t_inventario_desechos.responsable,
                        groupby = 
                        db.t_inventario_desechos.categoria |
                            db.t_inventario_desechos.id | 
                        db.t_inventario_desechos.espacio_fisico |
                        db.t_inventario_desechos.seccion |
                        db.t_inventario_desechos.unidad_medida | 
                        db.t_inventario_desechos.responsable
                        ))

                        mostrar_campo_dependencia = True

                    # Guardando el ID y nombre de la dependencia padre para el link 
                    # de navegacion de retorno
                    dep_padre_id = db(db.dependencias.id == request.vars.dependencia
                                    ).select().first().unidad_de_adscripcion
                    # Si dep_padre_id es None, se ha llegado al tope de la jerarquia
                    # y no hay un padre de este nodo
                    if dep_padre_id:
                        dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                            ).select().first().nombre

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
                    
                    inventario = list(db(
                        (db.t_inventario_desechos.seccion == request.vars.dependencia)).select())

                    inventario = list(db(
                    (db.dependencias.id == dep_id) & 
                    (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                    (db.espacios_fisicos.id == db.t_inventario_desechos.espacio_fisico)
                    ).select(
                    db.t_inventario_desechos.categoria,
                    db.t_inventario_desechos.espacio_fisico,
                    db.t_inventario_desechos.seccion,
                    db.t_inventario_desechos.id,
                    db.t_inventario_desechos.cantidad.sum(),
                    db.t_inventario_desechos.unidad_medida,
                    db.t_inventario_desechos.responsable,
                    groupby = 
                     db.t_inventario_desechos.categoria |
                     db.t_inventario_desechos.espacio_fisico |
                        db.t_inventario_desechos.id | 
                    db.t_inventario_desechos.seccion |
                    db.t_inventario_desechos.unidad_medida | 
                    db.t_inventario_desechos.responsable
                    ))


                    es_espacio = True
                
                else:
                    inventario = list(db(
                    (db.t_inventario_desechos.espacio_fisico == db.espacios_fisicos.id) &
                        (db.espacios_fisicos.dependencia == db.dependencias.id) & 
                        (db.dependencias.unidad_de_adscripcion == request.vars.dependencia)
                    ).select(
                    db.t_inventario_desechos.categoria,
                    db.t_inventario_desechos.id,
                    db.t_inventario_desechos.espacio_fisico,
                    db.t_inventario_desechos.seccion,
                    db.t_inventario_desechos.cantidad.sum(),
                    db.t_inventario_desechos.unidad_medida,
                    db.t_inventario_desechos.responsable,
                    groupby = 
                     db.t_inventario_desechos.categoria |
                        db.t_inventario_desechos.id | 
                     db.t_inventario_desechos.espacio_fisico |
                     db.t_inventario_desechos.seccion |
                    db.t_inventario_desechos.unidad_medida | 
                    db.t_inventario_desechos.responsable
                    ))

                    mostrar_campo_dependencia = True

                # Guardando el ID y nombre de la dependencia padre para el link 
                # de navegacion de retorno
                dep_padre_id = db(db.dependencias.id == request.vars.dependencia
                                 ).select().first().unidad_de_adscripcion
                # Si dep_padre_id es None, se ha llegado al tope de la jerarquia
                # y no hay un padre de este nodo
                if dep_padre_id:
                    dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                         ).select().first().nombre


        else:
            # Dependencia a la que pertenece el usuario o que tiene a cargo
            dep_id = user.f_dependencia
            dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre

            # Se muestran las dependencias que componen a la dependencia que
            # tiene a cargo el usuario y el inventario agregado de esta
            dependencias = list(db(
                (db.dependencias.id == dep_id)
            ).select(db.dependencias.ALL))

            # Se muestra como inventario el egregado de los inventarios que
            # pertenecen a la dependencia del usuario

            inventario = list(db(
                (db.t_inventario_desechos.espacio_fisico == db.espacios_fisicos.id) &
                (db.espacios_fisicos.dependencia == db.dependencias.id) &
                (db.dependencias.id == dep_id)
                ).select(
                db.t_inventario_desechos.categoria,
                db.t_inventario_desechos.espacio_fisico,
                db.t_inventario_desechos.id,
                db.t_inventario_desechos.seccion,
                db.t_inventario_desechos.cantidad.sum(),
                db.t_inventario_desechos.unidad_medida,
                db.t_inventario_desechos.responsable,
                groupby = 
                    db.t_inventario_desechos.categoria |
                    db.t_inventario_desechos.espacio_fisico |
                    db.t_inventario_desechos.id | 
                    db.t_inventario_desechos.seccion |
                db.t_inventario_desechos.unidad_medida | 
                db.t_inventario_desechos.responsable
                ))

            mostrar_campo_dependencia = True
            espacio_visitado = False


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
                desechos=desechos,
                envases=envases,
                envases_totales=envases_totales,
                inventario_total=inventario_total,
                unidades_de_medida=unidades_de_medida,
                retroceder=retroceder,
                mostrar_campo_dependencia = mostrar_campo_dependencia)


########################################
#          BITÁCORA DESECHOS           #
# FUNCIONES AUXILIARES Y CONTROLADORES #
########################################
def __agregar_entrada_bitacora_desechos(fecha, descripcion, cantidad_generada, cantidad_retirada, saldo_anterior, envase, inventario):
    fecha_parseada = datetime.datetime.strptime(fecha, "%Y-%m-%d")

    saldo_actual = float(cantidad_generada) + float(saldo_anterior) - float(cantidad_retirada)
    
    # Se actualiza la cantidad del desecho peligroso en la entrada del inventario
    row = db(db.t_inventario_desechos.id == int(inventario)).select().first()

    row.update_record(
        cantidad = saldo_actual
    )
    
    # Se agrega la entrada en la bitácora
    id = db.t_Bitacora_desechos.insert(
                fecha = fecha_parseada,
                descripcion = descripcion.upper(),
                cantidad_generada = cantidad_generada,
                cantidad_retirada = cantidad_retirada,
                saldo = saldo_actual,
                unidad_medida_bitacora = envase.unidad_medida,
                envase = envase.id,
                inventario = inventario
    )

    return T("Entrada agregada exitósamente.")

# Actualiza la información de un desecho peligroso
def __actualizar_desecho(id, envase, peligrosidad, tratamiento, concentracion):
    # Verifica que no existe en el inventario una entrada repetida 
    # se considera que una entrada es una única cuando una determinada composición
    # con una determinada unidad de medida ya se encuentra en un determinado especifico
    busqueda = 0

    busqueda = len(list(db(
        (db.t_inventario_desechos.composicion == envase.composicion) &
        (db.t_inventario_desechos.espacio_fisico == envase.espacio_fisico) &
        (db.t_inventario_desechos.unidad_medida == envase.unidad_medida) &
        (db.t_inventario_desechos.envase != envase.id) 
    ).select()))

    if busqueda == 0:
        row = db(db.t_inventario_desechos.id == int(id)).select().first()
        
        peligrosidad_mayusculas = []
        
        if type(peligrosidad) is list:
            peligrosidad_mayusculas = [x.upper() for x in peligrosidad]
        else:
            peligrosidad_mayusculas = peligrosidad.upper()
            
        row.update_record(
            categoria = envase.categoria,
            composicion = envase.composicion,
            envase = envase.id,
            concentracion = concentracion,
            espacio_fisico = envase.espacio_fisico,
            seccion = envase.espacio_fisico.dependencia,
            tratamiento = tratamiento.upper(),
            peligrosidad = peligrosidad_mayusculas
        )

        return T("Desecho actualizado correctamente.")

    else:
        return T("El desecho que usted está intentando ingresar ya se encuentra registrado. Por favor edite su entrada en la bitácora.")


# Agrega un nuevo desecho peligroso al inventario de un espacio físico
def __agregar_desecho(envase, peligrosidad, tratamiento, cantidad, concentracion):
    
    # Verifica que no existe en el inventario una entrada repetida 
    # se considera que una entrada es una única cuando una determinada composición
    # con una determinada unidad de medida ya se encuentra en un determinado especifico
    busqueda = 0
    busqueda = len(list(db(
        (db.t_inventario_desechos.composicion == envase.composicion) &
        (db.t_inventario_desechos.espacio_fisico == envase.espacio_fisico) &
        (db.t_inventario_desechos.unidad_medida == envase.unidad_medida) 
    ).select()))

    if busqueda == 0:
        # Verifica que la cantidad de desecho que se quiere registrar quepa dentro de la capacidad
        # del envase seleccionado
        if int(cantidad) <= int(envase.capacidad): 
            peligrosidad_mayusculas = []

            if type(peligrosidad) is list:
                peligrosidad_mayusculas = [x.upper() for x in peligrosidad]
            else:
                peligrosidad_mayusculas = peligrosidad.upper()

            #Agrega el desecho al inventario
            nueva_entrada_id = db.t_inventario_desechos.insert(categoria = envase.categoria,
                                            cantidad = cantidad,
                                            unidad_medida = envase.unidad_medida,
                                            composicion = envase.composicion,
                                            concentracion = concentracion,
                                            espacio_fisico = envase.espacio_fisico,
                                            seccion = envase.espacio_fisico.dependencia,
                                            responsable = auth.user_id,
                                            envase = envase.id,
                                            tratamiento = tratamiento.upper(),
                                            peligrosidad = peligrosidad_mayusculas)
            
            # Crea la entrada inicial en la bitácora de desechos
            db.t_Bitacora_desechos.insert(
                fecha = str(datetime.datetime.now()),
                descripcion = "ENTRADA INICIAL",
                cantidad_generada = cantidad,
                cantidad_retirada = 0,
                saldo = cantidad,
                unidad_medida_bitacora = envase.unidad_medida,
                envase = envase.id,
                inventario = nueva_entrada_id
            )

            return T("Desecho creado exitósamente.")


        else:
            return T("El contenedor que usted eligió no tiene la capacidad suficiente para almacenar la cantidad de desecho indicada.")
    else:
        return T("El desecho que usted está intentando ingresar ya se encuentra registrado. Por favor edite su entrada en la bitácora.")



# Muestra los movimientos de la bitacora comenzando por el mas reciente
@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def bitacora_desechos():
    # INICIO Datos del modal de agregar un registro
    # Conceptos
    conceptos = ['Generación','Retiro']

    # Tipos de consumos

    # Tipos de ingresos

    # Lista de unidades de medida
    unidades_de_medida = list(db(db.t_Unidad_de_medida.id > 0).select())

    # Obteniendo la entrada en t_Personal del usuario conectado

    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]

    if request.vars.inv is None:
        redirect(URL('inventarios_desechos'))

    inventario_id = int(request.vars.inv)

    # Inventario al que pertenecen los registros que se desean consultar
    inventario = db((db.t_inventario_desechos.id == inventario_id) & 
                    (db.t_inventario_desechos.espacio_fisico == db.espacios_fisicos.id)
                   ).select()[0]
    
    # Espacio al que pertenece la bitacora consultada
    espacio_id = inventario['t_inventario_desechos']['espacio_fisico']['id']

    # Unidad de medida en que es expresada la sustancia en el inventario
    unidad_medida = inventario['t_inventario_desechos']['unidad_medida']['f_abreviatura']

    espacio_nombre = inventario['t_inventario_desechos']['espacio_fisico']['codigo']

    envases = list(db((db.t_envases.espacio_fisico == espacio_id)).select())

    bitacora = list(db(
        (db.t_Bitacora_desechos.inventario == inventario_id) & 
        (db.t_Bitacora_desechos.created_by == db.auth_user.id)
    ).select(orderby=~db.t_Bitacora_desechos.id))

    ultima_entrada = db(
        (db.t_Bitacora_desechos.inventario == inventario_id) &
        (db.t_Bitacora_desechos.created_by == db.auth_user.id)
    ).select(orderby=~db.t_Bitacora_desechos.id).first()

    #Se está agregando una nueva entrada a la bitácora
    if request.vars.fecha_entrada:
        cantidad_retirada = 0
        cantidad_generada = 0

        envase = db((db.t_envases.id == request.vars.envase)).select().first()

        if(request.vars.cantidad_retirada != ''):
            cantidad_retirada = request.vars.cantidad_retirada

        if(request.vars.cantidad_generada != ''):
            cantidad_generada = request.vars.cantidad_generada
        
        response.flash = __agregar_entrada_bitacora_desechos(
            request.vars.fecha_entrada,
            request.vars.descripcion,
            cantidad_generada,
            cantidad_retirada,
            ultima_entrada['t_Bitacora_desechos']['saldo'],
            envase,
            bitacora[0]['t_Bitacora_desechos']['inventario'].id
        )
        session.flash = response.flash
        
        return redirect(URL('..', 'sigulab2', 'smydp/bitacora_desechos', vars=dict(inv=inventario_id))) 


    return dict(bitacora=bitacora,
                unidad_medida=unidad_medida,
                inventario=inventario,
                composicion=inventario['t_inventario_desechos']['composicion'],
                espacio_nombre=espacio_nombre,
                espacio_id=espacio_id,
                conceptos=conceptos,
                unidades_de_medida=unidades_de_medida,
                envases = envases,
                fecha_actual = str(datetime.datetime.now()).split(" ")[0]
                )

@auth.requires_login(otherwise=URL('modulos', 'login'))
def desechos():
    return locals()



#--------------------- Catalogo de Sustancias y Materiales ----------

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

############################################################################
############################################################################
#       GENERACION DE REPORTES
#############################################################################
############################################################################

def select_fecha():
    now = datetime.datetime.now()
    tablemes = SQLFORM.factory(Field('mes',requires=IS_IN_SET(['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']),
            label=T('Seleccione mes')),
        Field('year','integer',requires=IS_INT_IN_RANGE(1969,now.year+1,error_message='Debe introducir un año menor o igual al actual'),
            label=T('Introduzca año'))
        )
    if tablemes.process().accepted:
        if tablemes.vars.mes=="Enero":
            x=1
        elif tablemes.vars.mes=="Febrero":
            x=2
        elif tablemes.vars.mes=="Marzo":
            x=3
        elif tablemes.vars.mes=="Abril":
            x=4
        elif tablemes.vars.mes=="Mayo":
            x=5
        elif tablemes.vars.mes=="Junio":
            x=6
        elif tablemes.vars.mes=="Julio":
            x=7
        elif tablemes.vars.mes=="Agosto":
            x=8
        elif tablemes.vars.mes=="Septiembre":
            x=9
        elif tablemes.vars.mes=="Octubre":
            x=10
        elif tablemes.vars.mes=="Noviembre":
            x=11
        elif tablemes.vars.mes=="Diciembre":
            x=12
        redirect(URL('reportes','select_rl4',vars=dict(m=x,y=tablemes.vars.year)))
    return locals()


def generar_reporte():
    wb = Workbook()
    ws = wb.active
    cen = Alignment(horizontal='center', vertical='distributed')
    rig = Alignment(horizontal='right')
    lef = Alignment(horizontal='left')
    ft1 = Font(name='Arial', size=10, bold=True)
    ft2 = Font(name='Arial', size=10, bold=False)
    ft3 = Font(name='Arial', size=8)
    ws.font = ft2
    now = datetime.datetime.now()

    ws1 = wb.create_sheet("Informe mensual")

    #Encabezado
    ws.title = "Informe mensual"
    ws1.title = "Informe mensual"


    #tamaño de las columnas
    for i in ['A', 'D', 'E','F','G','J','K']:
       ws.column_dimensions[i].width = 10
       ws1.column_dimensions[i].width = 10
    ws.column_dimensions['B'].width = 17
    ws.column_dimensions['C'].width = 11
    ws.column_dimensions['H'].width = 9
    ws.column_dimensions['I'].width = 10
    ws1.column_dimensions['B'].width = 17
    ws1.column_dimensions['C'].width = 11
    ws1.column_dimensions['H'].width = 9
    ws1.column_dimensions['I'].width = 10

        #tamaño de las filas
    ws.row_dimensions[13].height = 40
    ws1.row_dimensions[13].height = 40
    for i in range(1,13):
        ws.row_dimensions[i].height = 13
        ws1.row_dimensions[i].height = 13
    for i in range(14,29):
        ws.row_dimensions[i].height = 12
        ws1.row_dimensions[i].height = 12

    #All Merges
    ws.merge_cells(start_row=5,start_column=3,end_row=5,end_column=10)
    ws.merge_cells(start_row=7,start_column=3,end_row=7,end_column=5)
    ws1.merge_cells(start_row=5,start_column=3,end_row=5,end_column=10)
    ws1.merge_cells(start_row=7,start_column=3,end_row=7,end_column=5)
    for i in range(13,28):
        ws.merge_cells(start_row=i,start_column=2,end_row=i,end_column=3)
        ws.merge_cells(start_row=i,start_column=10,end_row=i,end_column=11)
        ws1.merge_cells(start_row=i,start_column=2,end_row=i,end_column=3)
        ws1.merge_cells(start_row=i,start_column=10,end_row=i,end_column=11)

    for i in range(29,33):
        ws.merge_cells(start_row=i,start_column=1,end_row=i,end_column=10)
        ws1.merge_cells(start_row=i,start_column=1,end_row=i,end_column=10)

    #titulos y datos
    z = ['C5', 'J7', 'I9', 'J9', 'K9','B7','B8','B9','B10','B11','I10','J10','K10']
    ws['C5'] = 'INFORME MENSUAL DE SUSTANCIAS QUIMICAS CONTROLADAS'
    ws['J7'] = 'FECHA'
    ws['I9'] = 'DIA'
    ws['J9'] = 'MES'
    ws['K9'] = 'AÑO'
    ws1['C5'] = 'INFORME MENSUAL DE SUSTANCIAS QUIMICAS CONTROLADAS'
    ws1['J7'] = 'FECHA'
    ws1['I9'] = 'DIA'
    ws1['J9'] = 'MES'
    ws1['K9'] = 'AÑO'


    for i in range(5):
        ws[z[i]].font = ft1
        ws[z[i]].alignment = cen
        ws1[z[i]].font = ft1
        ws1[z[i]].alignment = cen

    ws['B7'] = 'OPERADOR:'
    ws['B8'] = 'LICENCIA:'
    ws['B9'] = 'PERMISO DEL CICPC:'
    ws['B10'] = 'RIF:'
    ws['B11'] = 'MES-AÑO:'
    ws1['B7'] = 'OPERADOR:'
    ws1['B8'] = 'LICENCIA:'
    ws1['B9'] = 'PERMISO DEL CICPC:'
    ws1['B10'] = 'RIF:'
    ws1['B11'] = 'MES-AÑO:'

    for i in range(5,10):
        ws[z[i]].font = ft1
        ws[z[i]].alignment = rig
        ws1[z[i]].font = ft1
        ws1[z[i]].alignment = rig

    ws['I10'] = now.day
    ws['J10'] = now.month
    ws['K10'] = now.year
    ws1['I10'] = now.day
    ws1['J10'] = now.month
    ws1['K10'] = now.year

    for i in range(10,13):
        ws[z[i]].font = ft2
        ws[z[i]].alignment = cen
        ws1[z[i]].font = ft2
        ws1[z[i]].alignment = cen

    ws['A28'] = 'Nota:'
    ws['A28'].font = ft1
    ws['A28'].alignment = lef
    ws1['A28'] = 'Nota:'
    ws1['A28'].font = ft1
    ws1['A28'].alignment = lef

    w = ['C7', 'C8', 'C9', 'C10', 'C11','A13','B13','D13','E13','F13','G13','H13','I13','J13']

    for i in range(5):
        ws[w[i]].font = ft2
        ws1[w[i]].font = ft2

    ws['C7'] = 'UNIVERSIDAD SIMON BOLIVAR'
    ws['C8'] = '2014LIC0256'
    ws['C9'] = 'No. 1311'
    ws['C10'] = 'G-20000063-5'
    ws['C11'] = str(now.month)+'/'+str(now.year)
    ws['A13'] = 'N°'

    ws['B13'] = 'Sustancia Química Controlada'

    ws['D13'] = 'Código Arancelario'

    ws['E13'] = 'Saldo Físico Inicial'

    ws['F13'] = 'Total Entradas'

    ws['G13'] = 'Total Salidas'

    ws['H13'] = 'Saldo Físico Final'

    ws['I13'] = 'Unidad de Medida'

    ws['J13'] = 'Observaciones'

    ws1['C7'] = 'UNIVERSIDAD SIMON BOLIVAR'
    ws1['C8'] = '2014LIC0256'
    ws1['C9'] = 'No. 1311'
    ws1['C10'] = 'G-20000063-5'
    ws1['C11'] = str(now.month)+'/'+str(now.year)
    ws1['A13'] = 'N°'

    ws1['B13'] = 'Sustancia Química Controlada'

    ws1['D13'] = 'Código Arancelario'

    ws1['E13'] = 'Saldo Físico Inicial'

    ws1['F13'] = 'Total Entradas'

    ws1['G13'] = 'Total Salidas'

    ws1['H13'] = 'Saldo Físico Final'

    ws1['I13'] = 'Unidad de Medida'

    ws1['J13'] = 'Observaciones'


    for i in range(5,14):
        ws[w[i]].font = ft1
        ws[w[i]].alignment = cen
        ws1[w[i]].font = ft1
        ws1[w[i]].alignment = cen


    x = ['A14','A15','A16','A17','A18','A19','A20','A21','A22','A23','A24','A25','A26']
    y = ['01','02','03','04','05','06','07','08','09','10','11','12','13']
    for i in range(0,13):
        ws[x[i]] = y[i]
        ws[x[i]].font = ft3
        ws[x[i]].alignment = cen
        ws1[x[i]] = y[i]
        ws1[x[i]].font = ft3
        ws1[x[i]].alignment = cen
    x = ['B14','B15','B16','B17','B18','B19','B20','B21','B22','B23','B24','B25','B26']
    wb.save('Reporte Universidad Simon Bolivar.xlsx')
    response.stream('Reporte Universidad Simon Bolivar.xlsx',attachment=True, filename='Reporte Universidad Simon Bolivar.xlsx')
    return locals()