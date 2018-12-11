# -*- coding: utf-8 -*-
import random
from difflib import SequenceMatcher
#from fuzzywuzzy import fuzz

# class Sustancia(object):
#     """ Clase que permite tomar un record de la tabla sustancias y realizar cada 
#     accion del CRUD de una manera rapida y ordenada

#     Inicialización con None es necesaria para que estos atributos 
#     puedan ser cargados con informacióm al momento de instanciar un objeto 
#     sustancia con el método instanciar()
#     """    
#     def __init__(self, db, nombre = None, metodo = None, rango = None, item_ensayar = None, requisitos = None,
#                  entregaResultados=None,ensayoCalibracion=None,certificadoConformidadProducto=None,
#                  certificadoCalibracion=None,otro=None,
#                  docencia = None, investigacion = None,
#                  gestion = None, extension = None, visibilidad = None,
#                  responsable = None, dependencia = None, ubicacion = None, id=None,
#                  ambito_in_situ=None, ambito_en_campo=None, ambito_otro=None, 
#                  ambito_otro_detalle=None, per_tecnico=None, cant_per_tecnico=None, per_supervisor=None, 
#                  cant_per_supervisor=None, per_tesista=None, cant_per_tesista=None,  per_pasante=None,
#                  cant_per_pasante=None, per_preparador=None, cant_per_preparador=None, per_obrero=None, 
#                  cant_per_obrero=None, per_otro=None, per_otro_detalle=None, equipo_presta_sustancia=None, 
#                  esp_fis_sustancia=None, insumos_sustancia=None, condicion_ambiental=None,
#                  condicion_ambiental_detalle=None):

#         self.nombre = nombre
#         self.metodo = metodo
#         self.rango = rango
#         self.item_ensayar = item_ensayar
#         self.requisitos=requisitos

#         #Checklist de la lista de producto 
#         self.entregaResultados=entregaResultados
#         self.ensayoCalibracion=ensayoCalibracion
#         self.certificadoConformidadProducto=certificadoConformidadProducto
#         self.certificadoCalibracion=certificadoCalibracion
#         self.otro=otro

#         self.docencia = docencia
#         self.investigacion = investigacion
#         self.gestion = gestion
#         self.extension = extension

#         self.visibilidad = visibilidad
#         self.responsable = responsable
#         self.dependencia = dependencia
#         self.ubicacion = ubicacion

#         self.inicializar_ambito(ambito_in_situ, ambito_en_campo, ambito_otro,
#             ambito_otro_detalle)
        
#         self.inicializar_per_requerido(per_tecnico, cant_per_tecnico, per_supervisor, cant_per_supervisor,
#         per_tesista, cant_per_tesista, per_pasante, cant_per_pasante, per_preparador, cant_per_preparador, 
#         per_obrero, cant_per_obrero, per_otro, per_otro_detalle)

#         self.equipo_presta_sustancia = equipo_presta_sustancia
#         self.esp_fis_sustancia = esp_fis_sustancia
#         self.insumos_sustancia = insumos_sustancia

#         self.condicion_ambiental = condicion_ambiental
#         self.condicion_ambiental_detalle = condicion_ambiental_detalle

#         self.inicializar_condicion_ambiental(condicion_ambiental, 
#             condicion_ambiental_detalle)

#         # Categorias de Ordenamiento, disponibles tras instanciacion
#         self.laboratorio = None
#         self.seccion = None
#         self.sede = None
#         self.id = None

#         self.db = db

#     def inicializar_ambito(self, ambito_in_situ, ambito_en_campo, ambito_otro,
#         ambito_otro_detalle):
#         self.ambito_in_situ = ambito_in_situ
#         self.ambito_en_campo = ambito_en_campo
#         self.ambito_otro = ambito_otro
#         self.ambito_otro_detalle = ambito_otro_detalle

#         return True

#     def inicializar_condicion_ambiental(self, condicion_ambiental,
#         condicion_ambiental_detalle):
#         self.condicion_ambiental = condicion_ambiental
#         self.condicion_ambiental_detalle = condicion_ambiental_detalle

#         return True

#     def inicializar_per_requerido(self, per_tecnico, cant_per_tecnico, per_supervisor, cant_per_supervisor,
#         per_tesista, cant_per_tesista, per_pasante, cant_per_pasante, per_preparador, cant_per_preparador, 
#         per_obrero, cant_per_obrero, per_otro, per_otro_detalle):
#         self.per_tecnico = per_tecnico
#         self.cant_per_tecnico = cant_per_tecnico
#         self.per_supervisor = per_supervisor
#         self.cant_per_supervisor = cant_per_supervisor
#         self.per_tesista = per_tesista
#         self.cant_per_tesista = cant_per_tesista
#         self.per_pasante = per_pasante
#         self.cant_per_pasante = cant_per_pasante
#         self.per_preparador = per_preparador
#         self.cant_per_preparador = cant_per_preparador
#         self.per_obrero = per_obrero
#         self.cant_per_obrero = cant_per_obrero
#         self.per_otro = per_otro
#         self.per_otro_detalle = per_otro_detalle

#         return True

#     def __str__(self):

#         return self.nombre


#     def insertar(self):

#         insercion = self.db.sustancias.insert(nombre = self.nombre.upper(), metodo = self.metodo.upper(), rango = self.rango.upper(),
#             item_ensayar = self.item_ensayar.upper(),
#             requisitos = self.requisitos.upper(), 
#             entregaResultados=self.entregaResultados,ensayoCalibracion=self.ensayoCalibracion,
#             certificadoConformidadProducto=self.certificadoConformidadProducto,
#             certificadoCalibracion=self.certificadoCalibracion,otro=self.otro,
#             docencia = self.docencia, investigacion = self.investigacion,
#             gestion = self.gestion, extension = self.extension,
#             visibilidad = self.visibilidad, responsable = self.responsable,
#             dependencia = self.dependencia, ubicacion = self.ubicacion,
#             ambito_in_situ=self.ambito_in_situ, ambito_en_campo=self.ambito_en_campo,
#             ambito_otro=self.ambito_otro, ambito_otro_detalle=self.ambito_otro_detalle, 
#             per_tecnico=self.per_tecnico, cant_per_tecnico=self.cant_per_tecnico, 
#             per_supervisor=self.per_supervisor, cant_per_supervisor=self.cant_per_supervisor,
#             per_tesista=self.per_tesista, cant_per_tesista=self.cant_per_tesista,
#             per_pasante=self.per_pasante, cant_per_pasante=self.per_pasante,
#             per_preparador=self.per_preparador, cant_per_preparador=self.cant_per_preparador,
#             per_obrero=self.per_obrero, cant_per_obrero=self.cant_per_obrero, per_otro=self.per_otro, 
#             per_otro_detalle=self.per_otro_detalle, equipo_presta_sustancia=self.equipo_presta_sustancia,
#             esp_fis_sustancia=self.esp_fis_sustancia, insumos_sustancia=self.insumos_sustancia,
#             condicion_ambiental=self.condicion_ambiental, 
#             condicion_ambiental_detalle=self.condicion_ambiental_detalle
#             )

#         return insercion


#     def instanciar(self, id):

#         instanciacion = self.db(self.db.sustancias.id == id).select(self.db.sustancias.ALL)

#         if (len(instanciacion) == 1):
#             self.id = id
#             self.nombre = instanciacion[0].nombre
#             self.metodo = instanciacion[0].metodo
#             self.rango = instanciacion[0].rango
#             self.item_ensayar = instanciacion[0].item_ensayar
#             self.requisitos = instanciacion[0].requisitos

#             self.entregaResultados=instanciacion[0].entregaResultados
#             self.ensayoCalibracion=instanciacion[0].ensayoCalibracion
#             self.certificadoConformidadProducto=instanciacion[0].certificadoConformidadProducto
#             self.certificadoCalibracion=instanciacion[0].certificadoCalibracion
#             self.otro=instanciacion[0].otro

#             self.docencia = instanciacion[0].docencia
#             self.investigacion = instanciacion[0].investigacion
#             self.gestion = instanciacion[0].gestion
#             self.extension = instanciacion[0].extension
#             self.visibilidad = instanciacion[0].visibilidad
#             self.responsable = instanciacion[0].responsable
#             self.dependencia = instanciacion[0].dependencia
#             self.ubicacion = instanciacion[0].ubicacion

#             self.instanciacion_ambito(instanciacion[0])

#             self.instanciacion_per_requerido(instanciacion[0])

#             self.equipo_presta_sustancia = instanciacion[0].equipo_presta_sustancia
#             self.esp_fis_sustancia = instanciacion[0].esp_fis_sustancia
#             self.insumos_sustancia = instanciacion[0].insumos_sustancia

#             self.instanciacion_condicion_ambiental(instanciacion[0])

#             return True

#         else:

#             return False

#     def instanciacion_ambito(self, instancia):
#         self.ambito_in_situ = instancia.ambito_in_situ
#         self.ambito_en_campo = instancia.ambito_en_campo
#         self.ambito_otro = instancia.ambito_otro
#         self.ambito_otro_detalle = instancia.ambito_otro_detalle

#     def instanciacion_condicion_ambiental(self, instancia):
#         self.condicion_ambiental = instancia.condicion_ambiental
#         self.condicion_ambiental_detalle = instancia.condicion_ambiental_detalle

#     def instanciacion_per_requerido(self, instancia):
#         self.per_tecnico = instancia.per_tecnico
#         self.cant_per_tecnico = instancia.cant_per_tecnico
#         self.per_supervisor = instancia.per_supervisor
#         self.cant_per_supervisor = instancia.cant_per_supervisor
#         self.per_tesista = instancia.per_tesista
#         self.cant_per_tesista = instancia.cant_per_tesista
#         self.per_pasante = instancia.per_pasante
#         self.cant_per_pasante = instancia.cant_per_pasante
#         self.per_preparador = instancia.per_preparador
#         self.cant_per_preparador = instancia.cant_per_preparador
#         self.per_obrero = instancia.per_obrero
#         self.cant_per_obrero = instancia.cant_per_obrero
#         self.per_otro = instancia.per_otro
#         self.per_otro_detalle = instancia.per_otro_detalle

#     def editar(self, nombre, metodo,
#                rango, item_ensayar, requisitos, entregaResultados,
#                ensayoCalibracion,certificadoConformidadProducto,
#                certificadoCalibracion,otro,
#                docencia, investigacion, gestion, extension, visibilidad,
#                responsable, dependencia, ubicacion, ambito_in_situ, ambito_en_campo,
#                ambito_otro, ambito_otro_detalle, per_tecnico, cant_per_tecnico, per_supervisor, 
#                cant_per_supervisor, per_tesista, cant_per_tesista,  per_pasante,
#                cant_per_pasante, per_preparador, cant_per_preparador, per_obrero, 
#                cant_per_obrero, per_otro, per_otro_detalle, equipo_presta_sustancia, 
#                esp_fis_sustancia, insumos_sustancia, condicion_ambiental,
#                condicion_ambiental_detalle):

#         self.nombre = nombre
#         self.metodo = metodo
#         self.rango = rango
#         self.item_ensayar = item_ensayar
#         self.requisitos = requisitos

#         self.entregaResultados=entregaResultados
#         self.ensayoCalibracion=ensayoCalibracion
#         self.certificadoConformidadProducto=certificadoConformidadProducto
#         self.certificadoCalibracion=certificadoCalibracion
#         self.otro=otro

#         self.inicializar_ambito(ambito_in_situ, ambito_en_campo, ambito_otro, 
#             ambito_otro_detalle)

#         self.inicializar_per_requerido(per_tecnico, cant_per_tecnico, per_supervisor, cant_per_supervisor,
#             per_tesista, cant_per_tesista, per_pasante, cant_per_pasante, per_preparador, cant_per_preparador, 
#             per_obrero, cant_per_obrero, per_otro, per_otro_detalle)

#         self.equipo_presta_sustancia = equipo_presta_sustancia
#         self.esp_fis_sustancia = esp_fis_sustancia
#         self.insumos_sustancia = insumos_sustancia

#         self.inicializar_condicion_ambiental(condicion_ambiental, 
#             condicion_ambiental_detalle)

#         self.docencia = docencia
#         self.investigacion = investigacion
#         self.gestion = gestion
#         self.extension = extension
#         self.visibilidad = visibilidad
#         self.responsable = responsable
#         self.dependencia = dependencia
#         self.ubicacion = ubicacion


#     def actualizar(self, id):

#         actualizacion = self.db(self.db.sustancias.id == id).update(
#                             nombre = self.nombre.upper(),
#                             metodo = self.metodo.upper(),
#                             rango = self.rango.upper(),
#                             item_ensayar = self.item_ensayar.upper(),
#                             requisitos = self.requisitos.upper(),

#                             entregaResultados=self.entregaResultados,
#                             ensayoCalibracion=self.ensayoCalibracion,
#                             certificadoConformidadProducto=self.certificadoConformidadProducto,
#                             certificadoCalibracion=self.certificadoCalibracion,
#                             otro=self.otro,

#                             docencia = self.docencia,
#                             investigacion = self.investigacion,
#                             gestion = self.gestion,
#                             extension = self.extension,
#                             visibilidad = self.visibilidad,
#                             responsable = self.responsable,
#                             dependencia = self.dependencia,
#                             ubicacion = self.ubicacion,
#                             ambito_in_situ=self.ambito_in_situ, 
#                             ambito_en_campo=self.ambito_en_campo,
#                             ambito_otro=self.ambito_otro,
#                             ambito_otro_detalle=self.ambito_otro_detalle,
#                             per_tecnico = self.per_tecnico,  
#                             cant_per_tecnico = self.cant_per_tecnico,
#                             per_supervisor = self.per_supervisor,
#                             cant_per_supervisor = self.cant_per_supervisor, 
#                             per_tesista = self.per_tesista, 
#                             cant_per_tesista = self.cant_per_tesista, 
#                             per_pasante = self.per_pasante, 
#                             cant_per_pasante = self.cant_per_pasante, 
#                             per_preparador = self.per_preparador,
#                             cant_per_preparador = self.cant_per_preparador, 
#                             per_obrero = self.per_obrero, 
#                             cant_per_obrero = self.cant_per_obrero, 
#                             per_otro = self.per_otro,  
#                             per_otro_detalle = self.per_otro_detalle, 
#                             equipo_presta_sustancia = self.equipo_presta_sustancia,
#                             esp_fis_sustancia = self.esp_fis_sustancia,
#                             insumos_sustancia = self.insumos_sustancia,
#                             condicion_ambiental = self.condicion_ambiental,
#                             condicion_ambiental_detalle = self.condicion_ambiental_detalle)

#         return actualizacion

#     def checkear_tags(self, tags, string):
#         for tag in tags:
#             string_compare = getattr(self, tag).decode('utf-8').upper()

#             if tag == "laboratorio" and "LABORATORIO" in string_compare:
#                 ratio_str = fuzz.token_set_ratio(string_compare, string)
#                 if ratio_str >= 95:
#                     print(ratio_str, string, string_compare)
#                     return True
#             else:
#                 ratio_str = fuzz.token_set_ratio(string_compare, string)
#                 if ratio_str >= 80:
#                     print(ratio_str, string, string_compare)
#                     return True

#             print(ratio_str, string, string_compare)

#         print("NO MATCH")
#         return False   


#------------------------------------------------------------------------------
#
# Clase que permitira tomar la tabla sustancias y crear un listado, incluira 
# funciones de paginado y ordenamiento.
#
#------------------------------------------------------------------------------

class ListaSustancias(object):

    def __init__(self, db, dependencia, rol, orden=False, columna='id', central=1):

        #### Captura de datos desde la Base de Datos

        self.db = db

        # 1. Tomar sustancias visibles o todos de la base de datos

        self.set = self.capturar_conjunto_por_rol(dependencia, rol)

        # Aqui se introducen los sustancias instanciados
        self.filas = []

        # 2. Instanciar todos los sustancias como objetos de la clase Sustancia
        self.capturar_objetos()

        # Numero de sustancias recuperados desde la base de datos
        self.cuenta = len(self.filas)

        #### Variables de Ordenamiento

        # Esta indicara sobre que columna se ordenara
        # Por defecto se ordenan por el ID
        self.columna = columna

        # False: A-Z..1-9..etc, True: Z-A..9-1..etc
        # Por defecto es False
        self.orden = orden

        # Variables de Paginado
        self.pagina_central = central
        self.primera_pagina = 1
        self.ultima_pagina = int((self.cuenta / 10) + (self.cuenta % 10 > 0))

        if self.ultima_pagina == 0:
            self.ultima_pagina = 1

        # Pagina a la que ira cada boton, False si el boton no estara presente
        self.boton_principio = self.primera_pagina
        self.boton_fin = self.ultima_pagina
        self.boton_siguiente = self.pagina_central + 1
        self.boton_anterior = self.pagina_central - 1

        self.rango_paginas = range(max(self.primera_pagina, self.pagina_central - 2), min(self.pagina_central + 2, self.ultima_pagina)+1)
        # Configuraremos estos botones
        self.configurar_botones()

        # Posicion del ultimo elemento segun la pagina actual (Lo posicionamos)
        self.ultimo_elemento = self.cuenta

        self.posicionar_ultimo()

        # Lista de cada fila, convertida en el objeto sustancia
        self.sustancias_a_mostrar = []

    # Configurara la visibilidad y posicion de cada boton

    def configurar_botones(self):
        self.boton_principio = self.primera_pagina
        self.boton_fin = self.ultima_pagina
        self.boton_siguiente = self.pagina_central + 1
        self.boton_anterior = self.pagina_central - 1

        if self.pagina_central - 2 <= self.primera_pagina:
            self.boton_principio = False

        if self.pagina_central + 2 >= self.ultima_pagina:
            self.boton_fin = False

        if self.pagina_central == self.primera_pagina:
            self.boton_anterior = False

        if self.pagina_central == self.ultima_pagina:
            self.boton_siguiente = False

        self.rango_paginas = range(max(self.primera_pagina, self.pagina_central - 2), min(self.pagina_central + 2, self.ultima_pagina)+1)

    def cambiar_pagina(self, nueva_pagina):
        self.pagina_central = nueva_pagina
        self.configurar_botones()
        self.posicionar_ultimo()

    # Estas pueden ser nombre, id, nombre_columna, laboratorio, seccion, sede
    def cambiar_columna(self, columna):
        self.columna = columna

    def posicionar_ultimo(self):
        self.ultimo_elemento = min(self.pagina_central * 10, self.cuenta)

    def invertir_ordenamiento(self):
        self.orden = not(self.orden)

    def cambiar_ordenamiento(self, orden):
        self.orden = orden

    # def capturar_conjunto_por_rol(self, dependencia, rol):
    #     if rol:
    #         if rol == 2:
    #             return self.db(self.db.sustancias.id > 0)
    #         else:
    #             secciones = []
    #             dep = self.db(self.db.dependencias.unidad_de_adscripcion == dependencia).select(self.db.dependencias.id)

    #             for d in dep:
    #                 secciones.append(int(d.id))

    #             return self.db((any((self.db.sustancias.dependencia == s) for s in secciones)) or (self.db.sustancias.visibilidad == True))

    #     else:
    #         return self.db(self.db.sustancias.visibilidad == True)

    def capturar_objetos(self):
        """
        Toma cada sustancia de la base de datos, lo instancia como un objeto
        de la clase "Sustancia" y luego lo anade a "filas" que es una lista
        tentativa de sustancias. El listado final se encuentra en el arreglo
        "sustancias_a_mostrar" pues son los sustancias que ya pasaron por el
        filtro de 10 sustancias por pagina mas por el ordenamiento.
        """
        for sust in self.set.select(self.db.t_Sustancia.id):
            sustancia = Sustancia(self.db)
            sustancia.instanciar(serv.id)
            self.filas.append(sustancia)

    def orden_y_filtrado(self):
        self.filas.sort(key=lambda sust: getattr(serv, self.columna), reverse=self.orden)
        self.sustancias_a_mostrar = self.filas[(self.pagina_central - 1)*10:self.ultimo_elemento]

    # Estas pueden ser nombre, nombre_columna, laboratorio, seccion, sede
    def filtrar_por_tags(self, filtro, tags=None):
        filtro = filtro.decode('utf-8').upper()
        if tags is None:
            tags = ["nombre", "laboratorio", "seccion", "sede"]

        nueva_lista = [fila for fila in self.filas if fila.checkear_tags(tags, filtro)]

        self.filas = nueva_lista
        self.orden_y_filtrado()




#------------------------------------------------------------------------------
#
# Solicitud y Listado de Solicitudes
#
#------------------------------------------------------------------------------

class Solicitud(object):

    def __init__(self, db, auth, registro = None, id_responsable_solicitud = None,
        fecha_solicitud = None, id_sustancia_solicitud = None,
        estado_solicitud = None):

        self.registro = registro
        self.id_responsable_solicitud = id_responsable_solicitud
        self.fecha_solicitud = fecha_solicitud
        self.id_sustancia_solicitud = id_sustancia_solicitud
        self.estado_solicitud = estado_solicitud

        self.estado_solicitud_str = self.estado_string()

        # Fuentes de datos
        self.db = db
        self.auth = auth

        # Variables Disponibles tras conseguir_atributos()
        self.id = None

        self.nombre_responsable_solicitud = None
        self.email_responsable_solicitud = None
        self.telef_responsable_solicitud = None
        self.id_dependencia_solicitante = None
        self.nombre_dependencia_solicitante = None
        self.nombre_jefe_dependencia_solicitante = None
        self.id_dependencia_ejecutora = None
        self.nombre_dependencia_ejecutora = None
        self.jefe_dependencia_ejecutora = None
        self.lugar_ejecucion_sustancia = None
        self.nombre_sustancia = None
        self.adscripcion_dependencia_solicitante = None
        self.adscripcion_dependencia_ejecutora = None

        # Variables disponibles despues de aprobacion
        self.aprobada_por = None
        self.fecha_aprobacion = None

        # Variables disponibles despues de ejecucion
        self.fecha_elaboracion = None
        self.elaborada_por = None
        # Variables para Certificacion
        self.cargo_responsable_solicitud = None
        self.ci_responsable_solicitud = None

        if registro != None:
            self.conseguir_atributos()

    def __str__(self):

        return self.registro

    def insertar(self):

        insercion = self.db.solicitudes.insert( registro = self.registro,
                                                responsable = self.id_responsable_solicitud,
                                                fecha = self.fecha_solicitud,
                                                id_sustancia_solicitud = self.id_sustancia_solicitud,
                                                estado = self.estado_solicitud,
                                                aprobada_por = self.aprobada_por,
                                                fecha_aprobacion = self.fecha_aprobacion,
                                                elaborada_por = self.elaborada_por,
                                                fecha_elaboracion = self.fecha_elaboracion)

        return insercion

    def instanciar(self, id):
        instanciacion = self.db(self.db.solicitudes.id == id).select(self.db.solicitudes.ALL)


        if (len(instanciacion) == 1):
            self.id = id
            self.registro = instanciacion[0].registro
            self.id_responsable_solicitud = instanciacion[0].responsable
            self.fecha_solicitud = instanciacion[0].fecha
            self.id_sustancia_solicitud = instanciacion[0].id_sustancia_solicitud
            self.estado_solicitud = instanciacion[0].estado

            if instanciacion[0].aprobada_por:
                self.aprobada_por = instanciacion[0].aprobada_por
            else:
                self.aprobada_por = ""

            if instanciacion[0].fecha_aprobacion:
                self.fecha_aprobacion = instanciacion[0].fecha_aprobacion
            else:
                self.fecha_aprobacion = ""

            if instanciacion[0].elaborada_por:
                self.elaborada_por = instanciacion[0].elaborada_por
            else:
                self.elaborada_por = ""

            if instanciacion[0].fecha_elaboracion:
                self.fecha_elaboracion = instanciacion[0].fecha_elaboracion
            else:
                self.fecha_elaboracion = ""

            self.estado_solicitud_str = self.estado_string()

            self.conseguir_atributos()

            return True

        else:

            return False

    def editar(self, registro, id_responsable_solicitud, fecha_solicitud,
        id_sustancia_solicitud):

        self.registro = registro
        self.id_responsable_solicitud = id_responsable_solicitud
        self.fecha_solicitud = fecha_solicitud
        self.id_sustancia_solicitud = id_sustancia_solicitud

        self.conseguir_atributos()

    def actualizar(self, id):

        actualizacion = self.db(self.db.solicitudes.id == id).update(
                                                registro = self.registro,
                                                responsable = self.id_responsable_solicitud,
                                                fecha = self.fecha_solicitud,
                                                id_sustancia_solicitud = self.id_sustancia_solicitud,
                                                estado = self.estado_solicitud,
                                                aprobada_por = self.aprobada_por,
                                                fecha_aprobacion = self.fecha_aprobacion,
                                                elaborada_por = self.elaborada_por,
                                                fecha_elaboracion = self.fecha_elaboracion)

        return actualizacion

    def eliminar(self, id):

        self.db(self.db.solicitudes.id == id).delete()

    def conseguir_atributos(self):

        # Extensiones telefonicas del responsable de la solicitud
        personal = self.db(self.id_responsable_solicitud == self.db.t_Personal.id).select(self.db.t_Personal.ALL)[0]
        self.telef_responsable_solicitud = personal.f_telefono
        self.ci_responsable_solicitud = personal.f_ci

        responsable_usuario = self.db(personal.f_usuario == self.db.auth_user.id).select(self.db.auth_user.ALL)[0]

        cargo_id = self.db(personal.f_usuario == self.db.auth_membership.user_id).select(self.db.auth_membership.ALL)[0].group_id

        self.cargo_responsable_solicitud = self.db(cargo_id == self.db.auth_group.id).select(self.db.auth_group.ALL)[0].role

        self.nombre_responsable_solicitud = responsable_usuario.first_name + " " + responsable_usuario.last_name

        # Correo electronico del responsable de la solicitud
        self.email_responsable_solicitud = responsable_usuario.email

        dependencia = self.db(personal.f_dependencia == self.db.dependencias.id).select(self.db.dependencias.ALL)[0]

        self.id_dependencia_solicitante = dependencia.id

        self.id_adscripcion_dependencia_solicitante = dependencia.unidad_de_adscripcion

        if self.id_adscripcion_dependencia_solicitante != None:
            self.adscripcion_dependencia_solicitante = self.db(self.id_adscripcion_dependencia_solicitante == self.db.dependencias.id).select(self.db.dependencias.ALL)[0].nombre

        else:
            self.adscripcion_dependencia_solicitante = "VICERRECTORADO ACADÉMICO"

        # Dependencia solicitante
        self.nombre_dependencia_solicitante = dependencia.nombre

        # Jefe Dependencia Solicitante
        usuario_jefe_dependencia_solicitante = self.db(dependencia.id_jefe_dependencia == self.db.auth_user.id).select(self.db.auth_user.ALL)[0]

        self.nombre_jefe_dependencia_solicitante = usuario_jefe_dependencia_solicitante.first_name + " " + usuario_jefe_dependencia_solicitante.last_name

        self.id_dependencia_ejecutora = self.db(self.id_sustancia_solicitud == self.db.t_Sustancia.id).select(self.db.t_Sustancia.ALL).dependencia

        dependencia_ejecutora_sustancia = self.db(self.id_dependencia_ejecutora == self.db.dependencias.id).select(self.db.dependencias.ALL)[0]

        self.id_adscripcion_dependencia_ejecutora = dependencia_ejecutora_sustancia.unidad_de_adscripcion

        if self.id_adscripcion_dependencia_ejecutora != None:
            self.adscripcion_dependencia_ejecutora = self.db(self.id_adscripcion_dependencia_ejecutora == self.db.dependencias.id).select(self.db.dependencias.ALL)[0].nombre

        else:
            self.adscripcion_dependencia_ejecutora = "VICERRECTORADO ACADÉMICO"       

        # Dependencia Ejecutora del Sustancia
        self.nombre_dependencia_ejecutora = dependencia_ejecutora_sustancia.nombre

        # Jefe de la Dependencia Ejecutora del Sustancia
        self.usuario_jefe_dependencia_ejecutora = self.db(dependencia_ejecutora_sustancia.id_jefe_dependencia == self.db.auth_user.id).select(self.db.auth_user.ALL)[0]

        self.jefe_dependencia_ejecutora = self.usuario_jefe_dependencia_ejecutora.first_name + " " + self.usuario_jefe_dependencia_ejecutora.last_name

        # Lugar de Ejecucion de Sustancia

        id_ubicacion_ejecucion = self.db(self.id_sustancia_solicitud == self.db.t_Sustancia.id).select(self.db.t_Sustancia.ALL)[0].ubicacion

        self.lugar_ejecucion_sustancia = self.db(id_ubicacion_ejecucion == self.db.espacios_fisicos.id).select(self.db.espacios_fisicos.ALL)[0].codigo

        # Nombre de Sustancia

        self.nombre_sustancia = self.db(self.id_sustancia_solicitud == self.db.t_Sustancia.id).select(self.db.t_Sustancia.ALL)[0].nombre

    def cambiar_estado(self, estado, request):
        self.estado_solicitud = estado
        if estado == 2:
            # Fecha de elaboracion del sustancia
            self.fecha_elaboracion = request.now
            # Persona responsable de la solicitud y Elaborado por
            self.elaborada_por = "%s %s" % (self.auth.user.first_name, self.auth.user.last_name)

        elif estado == 1:
            # Fecha de elaboracion del sustancia
            self.fecha_aprobacion = request.now
            # Persona responsable de la solicitud y Elaborado por
            self.aprobada_por = self.auth.user.first_name + " " + self.auth.user.last_name

        self.estado_solicitud_str = self.estado_string()

    def estado_string(self):
        if self.estado_solicitud == -1:
            return "Denegada"
        elif self.estado_solicitud == 0:
            return "Por Aprobación"
        elif self.estado_solicitud == 1:
            return "En ejecución"
        elif self.estado_solicitud == 2:
            return "Por certificación"
        elif self.estado_solicitud == 3:
            return "Ejecutado"

    def guardar_en_historial(self):
        historial = Historial(self.db, self.auth, self)

        historial.insertar()

    def correoHacerSolicitud(self):
        nombre_jefe_dependencia = self.jefe_dependencia_ejecutora
        email_jefe_dependencia = self.usuario_jefe_dependencia_ejecutora.email
        nombre_solicitante = self.nombre_responsable_solicitud
        email_solicitante = self.email_responsable_solicitud
        nombre_sustancia = self.nombre_sustancia
        nombre_dependencia = self.nombre_dependencia_ejecutora
        numero_registro = self.registro 

        # Se le manda el email al jefe de la dependencia a la que pertenece el sustancia
        correo = '<html><head><meta charset="UTF-8"></head><body><table><tr><td><p>Hola, %s.</p><br><p>Se ha hecho una solicitud del sustancia %s. La operación fue realizada por %s, el/la cual pertenece a la dependencia de %s.</p><br><p>Para consultar dicha operación diríjase a la página web <a href="159.90.171.24">SIGULAB</a></p></td></tr></table></body></html>' % (nombre_jefe_dependencia, nombre_sustancia, nombre_solicitante, nombre_dependencia)

        asunto = numero_registro + ' [SIGULAB] ' + 'Se ha solicitado una sustancia'

        enviar_correo(self.auth, email_jefe_dependencia, asunto, correo)

        # Se le manda el email al responsable de la solicitud
        correo = '<html><head><meta charset="UTF-8"></head><body><table><tr><td><p>Hola, %s.</p><br><p>Se ha hecho su solicitud del sustancia %s.</p><br><p>Para consultar dicha operación diríjase a la página web <a href="159.90.171.24">SIGULAB</a></p></td></tr></table></body></html>' % (nombre_solicitante, nombre_sustancia)

        asunto =  numero_registro + '[SIGULAB] ' + 'Se ha solicitado un sustancia'

        enviar_correo(self.auth, email_solicitante, asunto, correo)

    def correoCambioEstadoSolicitud(self):
        nombre_solicitante = self.nombre_responsable_solicitud
        email_solicitante = self.email_responsable_solicitud
        nombre_sustancia = self.nombre_sustancia
        estado_solicitud = self.estado_solicitud
        nombre_estado_solicitud = self.estado_solicitud_str
        numero_registro = self.registro 

        if estado_solicitud != 2:
            correo = '<html><head><meta charset="UTF-8"></head><body><table><tr><td><p>Hola, %s.</p><br><p>Su solicitud del sustancia %s ha cambiado al estado a %s.</p><br><p>Para consultar dicha operación diríjase a la página web <a href="159.90.171.24">SIGULAB</a></p></td></tr></table></body></html>' % (nombre_solicitante, nombre_sustancia, nombre_estado_solicitud)

            asunto = numero_registro + ' [SIGULAB] ' + 'Se ha cambiado el estado de su solicitud'

            enviar_correo(self.auth, email_solicitante, asunto, correo)

    def correoSolicitudFinalizada(self):
        estado_solicitud = self.estado_solicitud
        email_jefe_dependencia = self.usuario_jefe_dependencia_ejecutora.email
        nombre_sustancia = self.nombre_sustancia
        nombre_dependencia_solicitante = self.nombre_dependencia_solicitante
        nombre_jefe_dependencia_solicitante = self.nombre_jefe_dependencia_solicitante
        nombre_solicitante = self.nombre_responsable_solicitud
        email_solicitante = self.email_responsable_solicitud
        extensiones_solicitante = self.telef_responsable_solicitud
        nombre_dependencia_ejecutora = self.nombre_dependencia_ejecutora
        nombre_jefe_dependencia_ejecutora = self.jefe_dependencia_ejecutora
        solicitud_elaborada_por = self.elaborada_por
        solicitud_aprobada_por = self.aprobada_por
        fecha_elaboracion_solicitud = self.fecha_elaboracion
        fecha_aprobacion_solicitud = self.fecha_aprobacion
        numero_registro = self.registro 

        if estado_solicitud == 2:
            correo = '<html><head><meta charset="UTF-8"></head><body><table><tr><td><p>A continuación se encuentran los datos del sustancia que solicitó:</p><p>Sustancia solicitado: %s</p><p>Dependencia del solicitante: %s</p><p>Jefe de la dependencia del solicitante: %s</p><p>Responsable de la solicitud: %s</p><p>Email del respponsable de la solicitud: %s</p><p>Telf. del responsable de la solicitud: %d</p><p>Categoría del sustancia: %s</p><p>Propósito del sustancia: %s<p>Descripción del propósito del sustancia: %s</p><p>Descripción del sustancia: %s</p><p>Dependencia ejecutora del sustancia: %s</p><p>Jefe de la dependencia ejecutora del sustancia: %s</p><p>Solicitud elaborada por: %s</p><p>Fecha de elaboración de la solicitud: %s</p><p>Solicitud aprobada por: %s</p><p>Fecha de aprobación de la solicitud: %s</p><br><p>Para imprimir el PDF diríjase a la página web <a href="159.90.171.24">SIGULAB</a></p></td></tr></table></body></html>' % (nombre_sustancia, nombre_dependencia_solicitante, nombre_jefe_dependencia_solicitante, nombre_solicitante, email_solicitante, extensiones_solicitante, nombre_dependencia_ejecutora, nombre_jefe_dependencia_ejecutora, solicitud_elaborada_por, fecha_elaboracion_solicitud, solicitud_aprobada_por, fecha_aprobacion_solicitud)

            asunto = numero_registro + ' [SIGULAB] ' + 'Solicitud de Sustancia'

            enviar_correo(self.auth, email_jefe_dependencia, asunto, correo)


class ListaSolicitudes(object):

    def __init__(self, db, auth, tipo_listado, orden=False, columna='id', central=1):
        self.db = db
        self.auth = auth
        self.tipo_listado = tipo_listado

        # Dependencia del usuario para filtrar la lista
        personal_usuario = db(auth.user_id==self.db.t_Personal.f_usuario).select(self.db.t_Personal.ALL)[0]

        self.dependencia_usuario = personal_usuario.f_dependencia

        # Instanciacion de cada solicitud en la bd
        self.set = self.db(self.db.solicitudes.id > 0)
        self.filas = []
        self.capturar_objetos()

        self.cuenta = len(self.filas)

        # Variables de Ordenamiento
        # Esta indicara sobre que columna se ordenara
        self.columna = columna

        # False sera orden alfabetico, True sera su reverso
        self.orden = orden

        # Variables de Paginado
        self.pagina_central = central
        self.primera_pagina = 1
        self.ultima_pagina = int((self.cuenta / 10) + (self.cuenta % 10 > 0))

        if self.ultima_pagina == 0:
            self.ultima_pagina = 1

        # Pagina a la que ira cada boton, False si el boton no estara presente
        self.boton_principio = self.primera_pagina
        self.boton_fin = self.ultima_pagina
        self.boton_siguiente = self.pagina_central + 1
        self.boton_anterior = self.pagina_central - 1

        self.rango_paginas = range(max(self.primera_pagina, self.pagina_central - 2), min(self.pagina_central + 2, self.ultima_pagina)+1)

        # Configuraremos estos botones
        self.configurar_botones()

        # Posicion del ultimo elemento segun la pagina actual (Lo posicionamos)
        self.ultimo_elemento = self.cuenta

        self.posicionar_ultimo()

        # Lista de cada fila, convertida en el objeto sustancia
        self.solicitudes_a_mostrar = []

    # Configurara la visibilidad y posicion de cada boton

    def configurar_botones(self):
        self.boton_principio = self.primera_pagina
        self.boton_fin = self.ultima_pagina
        self.boton_siguiente = self.pagina_central + 1
        self.boton_anterior = self.pagina_central - 1

        if self.pagina_central - 2 <= self.primera_pagina:
            self.boton_principio = False

        if self.pagina_central + 2 >= self.ultima_pagina:
            self.boton_fin = False

        if self.pagina_central == self.primera_pagina:
            self.boton_anterior = False

        if self.pagina_central == self.ultima_pagina:
            self.boton_siguiente = False

        self.rango_paginas = range(max(self.primera_pagina, self.pagina_central - 2), min(self.pagina_central + 2, self.ultima_pagina)+1)

    def cambiar_pagina(self, nueva_pagina):
        self.pagina_central = nueva_pagina
        self.configurar_botones()
        self.posicionar_ultimo()

    def posicionar_ultimo(self):
        self.ultimo_elemento = min(self.pagina_central * 10, self.cuenta)

    def invertir_ordenamiento(self):
        self.orden = not(self.orden)

    def cambiar_ordenamiento(self, orden):
        self.orden = orden

    # Estas pueden ser nombre, id, nombre_columna, laboratorio, seccion, sede
    def cambiar_columna(self, columna):
        self.columna = columna

    def capturar_objetos(self):
        for solic in self.set.select(self.db.solicitudes.ALL):
            solicitud = Solicitud(self.db, self.auth)
            solicitud.instanciar(solic.id)

            if solicitud.estado_solicitud == 3:
                pass
            elif (self.tipo_listado == "Solicitante" and solicitud.id_dependencia_solicitante == self.dependencia_usuario and
                  solicitud.estado_solicitud <= 2):
                self.filas.append(solicitud)
            elif (self.tipo_listado == "Ejecutante" and solicitud.id_dependencia_ejecutora == self.dependencia_usuario and
                  solicitud.estado_solicitud <= 2 and solicitud.estado_solicitud >= 0):
                self.filas.append(solicitud)
            elif (self.tipo_listado == "Certificante" and solicitud.id_dependencia_solicitante == self.dependencia_usuario and
                  solicitud.estado_solicitud == 2):
                self.filas.append(solicitud)

    def orden_y_filtrado(self):
        self.filas.sort(key=lambda sust: getattr(serv, self.columna), reverse=self.orden)
        self.solicitudes_a_mostrar = self.filas[(self.pagina_central - 1)*10:self.ultimo_elemento]

#------------------------------------------------------------------------------
#
# Funciones para listar Tipos y Sedes
# funciones de paginado y ordenamiento.
#
#--------------------------x----------------------------------------------------


def listar_sedes(db):
    query = db().select(db.sedes.ALL)

    return query

#------------------------------------------------------------------------------
#
# Funcion para hacer query de Ficha de Sustancia
#
#------------------------------------------------------------------------------

def query_ficha(db, idv):
    entrada = db(db.t_Sustancia.id == idv).select(db.t_Sustancia.ALL)

    # Dependencia
    dependrow = db(entrada[0].dependencia == db.dependencias.id).select(db.dependencias.ALL)
    dependencia = dependrow[0].nombre
    dependenciaid = dependrow[0].id

    # Unidad de Adscripcion
    adscripcionid = dependrow[0].unidad_de_adscripcion

    adsrow = db(adscripcionid == db.dependencias.id).select(db.dependencias.ALL)
    adscripcion = adsrow[0].nombre

    # Sede
    sederow = db(adsrow[0].id_sede == db.sedes.id).select(db.sedes.ALL)
    sede = sederow[0].nombre
    sedeid = sederow[0].id

    # Ubicacion Fisica
    """
    *!* ERROR? si no fue seleccionado un espacio fisico, explota
    """
    ubicrow = ''
    ubicacion = ''
    ubicacionid = ''
    if entrada[0].ubicacion:
        ubicrow = db(entrada[0].ubicacion == db.espacios_fisicos.id).select(db.espacios_fisicos.ALL)
        ubicacion = ubicrow[0].codigo
        ubicacionid = ubicrow[0].id

    # Responsable
    resprow = db(entrada[0].responsable == db.t_Personal.id).select(db.t_Personal.ALL)

    responsable = resprow[0].f_nombre
    respid = resprow[0].id

    # Numeros
    telefono = resprow[0].f_telefono

    # Correo
    email = resprow[0].f_email

    ficha_con_queries = {"entrada": entrada,
                         "dependencia": dependencia,
                         "dependenciaid": dependenciaid,
                         "adscripcion": adscripcion,
                         "adscripcionid": adscripcionid,
                         "sede": sede,
                         "sedeid": sedeid,
                         "ubicacion": ubicacion,
                         "ubicacionid": ubicacionid,
                         "responsable": responsable,
                         "respid": respid,
                         "telefono": telefono,
                         "email": email
                         }

    return ficha_con_queries


#UNIDAD DE ADSCRIPCION:
#A PARTIR DE SEDE: DEPENDENCIA1 QUE TENGA COMO UNIDAD DE unidad_de_adscripcion A "Direccion" Y A DIRECCION

#DEPENDENCIA:
#A PARTIR DE DEPENDENCIA1: DEPENDENCIA2 QUE TENGA COMO UNIDAD DE ADSCRIPCION A DEPENDENCIA1

#ESPACIO FISICO:
#A PARTIR DE DEPENDENCIA2: ESPACIOS FISICOS QUE TENGA COMO DEPENDENCIA ADSCRITA A DEPENDENCIA2

#RESPONSABLE:
#A PARTIR DE DEPENDENCIA2: PERSONAL QUE TENGA COMO DEPENDENCIA A DEPENDENCIA2


#------------------------------------------------------------------------------
#
# Funciones para generar numeros para el registro de certificaciones y solicitudes
#
#------------------------------------------------------------------------------

def generador_num_registro():
    min = 0
    max = 999
    digit = str(random.randint(min, max))
    digits = (len(str(max))-len(digit))*'0' + digit

    return digits

def validador_registro_solicitudes(request, db, registro, contador=0):
    anio = str(request.now)[2:4]
    contador = 1 + contador
    digits = (3 - len(str(contador))) * '0' + str(contador)

    registronum = 'SIG-' + registro + "-" + anio + '/' + digits

    check = db(db.solicitudes.registro == registronum).count()

    check2 = db(db.historial_solicitudes.registro_solicitud == registronum).count()

    if check + check2 != 0:
        return validador_registro_solicitudes(request, db, registro, contador)
    else:
        return registronum

#------------------------------------------------------------------------------
#
# Funcion para enviar correo
#
#------------------------------------------------------------------------------


def enviar_correo(auth, destinatario, asunto, cuerpo):
    mail = auth.settings.mailer

    mail.send(destinatario, asunto, cuerpo)
    # reply_to = "yari.luciani95@gmail.com")


# Funcion para encontrar un radio de similitud entre 2 strings

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()