# -*- coding: utf-8 -*-
import random
from difflib import SequenceMatcher
#from fuzzywuzzy import fuzz

class Servicio(object):
    """ Clase que permite tomar un record de la tabla servicios y realizar cada 
    accion del CRUD de una manera rapida y ordenada

    Inicialización con None es necesaria para que estos atributos 
    puedan ser cargados con informacióm al momento de instanciar un objeto 
    servicio con el método instanciar()
    """    
    def __init__(self, db, nombre = None, tipo = None, categoria = None,
                 objetivo = None, alcance = None, metodo = None, rango = None,
                 incertidumbre = None, item_ensayar = None, requisitos = None,
                 entregaResultados=None,ensayoCalibracion=None,certificadoConformidadProducto=None,
                 certificadoCalibracion=None,otro=None,
                 docencia = None, investigacion = None,
                 gestion = None, extension = None, visibilidad = None,
                 responsable = None, dependencia = None, ubicacion = None, id=None,
                 ambito_in_situ=None, ambito_en_campo=None, ambito_otro=None, 
                 ambito_otro_detalle=None, per_tecnico=None, cant_per_tecnico=None, per_supervisor=None, 
                 cant_per_supervisor=None, per_tesista=None, cant_per_tesista=None,  per_pasante=None,
                 cant_per_pasante=None, per_preparador=None, cant_per_preparador=None, per_obrero=None, 
                 cant_per_obrero=None, per_otro=None, per_otro_detalle=None, equipo_presta_servicio=None, 
                 esp_fis_servicio=None, insumos_servicio=None, condicion_ambiental=None,
                 condicion_ambiental_detalle=None):

        self.nombre = nombre
        self.tipo = tipo
        self.categoria = categoria
        self.objetivo = objetivo
        self.alcance = alcance
        self.metodo = metodo
        self.rango = rango
        self.incertidumbre = incertidumbre
        self.item_ensayar = item_ensayar
        self.requisitos=requisitos

        #Checklist de la lista de producto 
        self.entregaResultados=entregaResultados
        self.ensayoCalibracion=ensayoCalibracion
        self.certificadoConformidadProducto=certificadoConformidadProducto
        self.certificadoCalibracion=certificadoCalibracion
        self.otro=otro

        self.docencia = docencia
        self.investigacion = investigacion
        self.gestion = gestion
        self.extension = extension

        self.visibilidad = visibilidad
        self.responsable = responsable
        self.dependencia = dependencia
        self.ubicacion = ubicacion

        self.inicializar_ambito(ambito_in_situ, ambito_en_campo, ambito_otro,
            ambito_otro_detalle)
        
        self.inicializar_per_requerido(per_tecnico, cant_per_tecnico, per_supervisor, cant_per_supervisor,
        per_tesista, cant_per_tesista, per_pasante, cant_per_pasante, per_preparador, cant_per_preparador, 
        per_obrero, cant_per_obrero, per_otro, per_otro_detalle)

        self.equipo_presta_servicio = equipo_presta_servicio
        self.esp_fis_servicio = esp_fis_servicio
        self.insumos_servicio = insumos_servicio

        self.condicion_ambiental = condicion_ambiental
        self.condicion_ambiental_detalle = condicion_ambiental_detalle

        self.inicializar_condicion_ambiental(condicion_ambiental, 
            condicion_ambiental_detalle)

        # Categorias de Ordenamiento, disponibles tras instanciacion
        self.nombre_tipo = None
        self.nombre_categoria = None
        self.laboratorio = None
        self.seccion = None
        self.sede = None
        self.id = None

        self.db = db

        self.obtenerListaPropositos()

    def inicializar_ambito(self, ambito_in_situ, ambito_en_campo, ambito_otro,
        ambito_otro_detalle):
        self.ambito_in_situ = ambito_in_situ
        self.ambito_en_campo = ambito_en_campo
        self.ambito_otro = ambito_otro
        self.ambito_otro_detalle = ambito_otro_detalle

        return True

    def inicializar_condicion_ambiental(self, condicion_ambiental,
        condicion_ambiental_detalle):
        self.condicion_ambiental = condicion_ambiental
        self.condicion_ambiental_detalle = condicion_ambiental_detalle

        return True

    def inicializar_per_requerido(self, per_tecnico, cant_per_tecnico, per_supervisor, cant_per_supervisor,
        per_tesista, cant_per_tesista, per_pasante, cant_per_pasante, per_preparador, cant_per_preparador, 
        per_obrero, cant_per_obrero, per_otro, per_otro_detalle):
        self.per_tecnico = per_tecnico
        self.cant_per_tecnico = cant_per_tecnico
        self.per_supervisor = per_supervisor
        self.cant_per_supervisor = cant_per_supervisor
        self.per_tesista = per_tesista
        self.cant_per_tesista = cant_per_tesista
        self.per_pasante = per_pasante
        self.cant_per_pasante = cant_per_pasante
        self.per_preparador = per_preparador
        self.cant_per_preparador = cant_per_preparador
        self.per_obrero = per_obrero
        self.cant_per_obrero = cant_per_obrero
        self.per_otro = per_otro
        self.per_otro_detalle = per_otro_detalle

        return True

    def __str__(self):

        return self.nombre


    def insertar(self):

        insercion = self.db.servicios.insert(nombre = self.nombre.upper(),
            tipo = self.tipo, categoria = self.categoria, objetivo = self.objetivo.upper(),
            alcance = self.alcance.upper(), metodo = self.metodo.upper(), rango = self.rango.upper(),
            incertidumbre = self.incertidumbre.upper(), item_ensayar = self.item_ensayar.upper(),
            requisitos = self.requisitos.upper(), 
            entregaResultados=self.entregaResultados,ensayoCalibracion=self.ensayoCalibracion,
            certificadoConformidadProducto=self.certificadoConformidadProducto,
            certificadoCalibracion=self.certificadoCalibracion,otro=self.otro,
            docencia = self.docencia, investigacion = self.investigacion,
            gestion = self.gestion, extension = self.extension,
            visibilidad = self.visibilidad, responsable = self.responsable,
            dependencia = self.dependencia, ubicacion = self.ubicacion,
            ambito_in_situ=self.ambito_in_situ, ambito_en_campo=self.ambito_en_campo,
            ambito_otro=self.ambito_otro, ambito_otro_detalle=self.ambito_otro_detalle, 
            per_tecnico=self.per_tecnico, cant_per_tecnico=self.cant_per_tecnico, 
            per_supervisor=self.per_supervisor, cant_per_supervisor=self.cant_per_supervisor,
            per_tesista=self.per_tesista, cant_per_tesista=self.cant_per_tesista,
            per_pasante=self.per_pasante, cant_per_pasante=self.per_pasante,
            per_preparador=self.per_preparador, cant_per_preparador=self.cant_per_preparador,
            per_obrero=self.per_obrero, cant_per_obrero=self.cant_per_obrero, per_otro=self.per_otro, 
            per_otro_detalle=self.per_otro_detalle, equipo_presta_servicio=self.equipo_presta_servicio,
            esp_fis_servicio=self.esp_fis_servicio, insumos_servicio=self.insumos_servicio,
            condicion_ambiental=self.condicion_ambiental, 
            condicion_ambiental_detalle=self.condicion_ambiental_detalle
            )

        return insercion


    def instanciar(self, id):

        instanciacion = self.db(self.db.servicios.id == id).select(self.db.servicios.ALL)

        if (len(instanciacion) == 1):
            self.id = id
            self.nombre = instanciacion[0].nombre
            self.tipo = instanciacion[0].tipo
            self.categoria = instanciacion[0].categoria
            self.objetivo = instanciacion[0].objetivo
            self.alcance = instanciacion[0].alcance
            self.metodo = instanciacion[0].metodo
            self.rango = instanciacion[0].rango
            self.incertidumbre = instanciacion[0].incertidumbre
            self.item_ensayar = instanciacion[0].item_ensayar
            self.requisitos = instanciacion[0].requisitos

            self.entregaResultados=instanciacion[0].entregaResultados
            self.ensayoCalibracion=instanciacion[0].ensayoCalibracion
            self.certificadoConformidadProducto=instanciacion[0].certificadoConformidadProducto
            self.certificadoCalibracion=instanciacion[0].certificadoCalibracion
            self.otro=instanciacion[0].otro

            self.docencia = instanciacion[0].docencia
            self.investigacion = instanciacion[0].investigacion
            self.gestion = instanciacion[0].gestion
            self.extension = instanciacion[0].extension
            self.visibilidad = instanciacion[0].visibilidad
            self.responsable = instanciacion[0].responsable
            self.dependencia = instanciacion[0].dependencia
            self.ubicacion = instanciacion[0].ubicacion

            self.instanciacion_ambito(instanciacion[0])

            self.instanciacion_per_requerido(instanciacion[0])

            self.equipo_presta_servicio = instanciacion[0].equipo_presta_servicio
            self.esp_fis_servicio = instanciacion[0].esp_fis_servicio
            self.insumos_servicio = instanciacion[0].insumos_servicio

            self.instanciacion_condicion_ambiental(instanciacion[0])

            self.conseguir_categorias()

            self.obtenerListaPropositos()

            return True

        else:

            return False

    def instanciacion_ambito(self, instancia):
        self.ambito_in_situ = instancia.ambito_in_situ
        self.ambito_en_campo = instancia.ambito_en_campo
        self.ambito_otro = instancia.ambito_otro
        self.ambito_otro_detalle = instancia.ambito_otro_detalle

    def instanciacion_condicion_ambiental(self, instancia):
        self.condicion_ambiental = instancia.condicion_ambiental
        self.condicion_ambiental_detalle = instancia.condicion_ambiental_detalle

    def instanciacion_per_requerido(self, instancia):
        self.per_tecnico = instancia.per_tecnico
        self.cant_per_tecnico = instancia.cant_per_tecnico
        self.per_supervisor = instancia.per_supervisor
        self.cant_per_supervisor = instancia.cant_per_supervisor
        self.per_tesista = instancia.per_tesista
        self.cant_per_tesista = instancia.cant_per_tesista
        self.per_pasante = instancia.per_pasante
        self.cant_per_pasante = instancia.cant_per_pasante
        self.per_preparador = instancia.per_preparador
        self.cant_per_preparador = instancia.cant_per_preparador
        self.per_obrero = instancia.per_obrero
        self.cant_per_obrero = instancia.cant_per_obrero
        self.per_otro = instancia.per_otro
        self.per_otro_detalle = instancia.per_otro_detalle

    def editar(self, nombre, tipo, categoria, objetivo, alcance, metodo,
               rango, incertidumbre, item_ensayar, requisitos, entregaResultados,
               ensayoCalibracion,certificadoConformidadProducto,
               certificadoCalibracion,otro,
               docencia, investigacion, gestion, extension, visibilidad,
               responsable, dependencia, ubicacion, ambito_in_situ, ambito_en_campo,
               ambito_otro, ambito_otro_detalle, per_tecnico, cant_per_tecnico, per_supervisor, 
               cant_per_supervisor, per_tesista, cant_per_tesista,  per_pasante,
               cant_per_pasante, per_preparador, cant_per_preparador, per_obrero, 
               cant_per_obrero, per_otro, per_otro_detalle, equipo_presta_servicio, 
               esp_fis_servicio, insumos_servicio, condicion_ambiental,
               condicion_ambiental_detalle):

        self.nombre = nombre
        self.tipo = tipo
        self.categoria = categoria
        self.objetivo = objetivo
        self.alcance = alcance
        self.metodo = metodo
        self.rango = rango
        self.incertidumbre = incertidumbre
        self.item_ensayar = item_ensayar
        self.requisitos = requisitos

        self.entregaResultados=entregaResultados
        self.ensayoCalibracion=ensayoCalibracion
        self.certificadoConformidadProducto=certificadoConformidadProducto
        self.certificadoCalibracion=certificadoCalibracion
        self.otro=otro

        self.inicializar_ambito(ambito_in_situ, ambito_en_campo, ambito_otro, 
            ambito_otro_detalle)

        self.inicializar_per_requerido(per_tecnico, cant_per_tecnico, per_supervisor, cant_per_supervisor,
            per_tesista, cant_per_tesista, per_pasante, cant_per_pasante, per_preparador, cant_per_preparador, 
            per_obrero, cant_per_obrero, per_otro, per_otro_detalle)

        self.equipo_presta_servicio = equipo_presta_servicio
        self.esp_fis_servicio = esp_fis_servicio
        self.insumos_servicio = insumos_servicio

        self.inicializar_condicion_ambiental(condicion_ambiental, 
            condicion_ambiental_detalle)

        self.docencia = docencia
        self.investigacion = investigacion
        self.gestion = gestion
        self.extension = extension
        self.visibilidad = visibilidad
        self.responsable = responsable
        self.dependencia = dependencia
        self.ubicacion = ubicacion

        self.obtenerListaPropositos()


    def actualizar(self, id):

        actualizacion = self.db(self.db.servicios.id == id).update(
                            nombre = self.nombre.upper(),
                            tipo = self.tipo,
                            categoria = self.categoria,
                            objetivo = self.objetivo.upper(),
                            alcance = self.alcance.upper(),
                            metodo = self.metodo.upper(),
                            rango = self.rango.upper(),
                            incertidumbre = self.incertidumbre.upper(),
                            item_ensayar = self.item_ensayar.upper(),
                            requisitos = self.requisitos.upper(),

                            entregaResultados=self.entregaResultados,
                            ensayoCalibracion=self.ensayoCalibracion,
                            certificadoConformidadProducto=self.certificadoConformidadProducto,
                            certificadoCalibracion=self.certificadoCalibracion,
                            otro=self.otro,

                            docencia = self.docencia,
                            investigacion = self.investigacion,
                            gestion = self.gestion,
                            extension = self.extension,
                            visibilidad = self.visibilidad,
                            responsable = self.responsable,
                            dependencia = self.dependencia,
                            ubicacion = self.ubicacion,
                            ambito_in_situ=self.ambito_in_situ, 
                            ambito_en_campo=self.ambito_en_campo,
                            ambito_otro=self.ambito_otro,
                            ambito_otro_detalle=self.ambito_otro_detalle,
                            per_tecnico = self.per_tecnico,  
                            cant_per_tecnico = self.cant_per_tecnico,
                            per_supervisor = self.per_supervisor,
                            cant_per_supervisor = self.cant_per_supervisor, 
                            per_tesista = self.per_tesista, 
                            cant_per_tesista = self.cant_per_tesista, 
                            per_pasante = self.per_pasante, 
                            cant_per_pasante = self.cant_per_pasante, 
                            per_preparador = self.per_preparador,
                            cant_per_preparador = self.cant_per_preparador, 
                            per_obrero = self.per_obrero, 
                            cant_per_obrero = self.cant_per_obrero, 
                            per_otro = self.per_otro,  
                            per_otro_detalle = self.per_otro_detalle, 
                            equipo_presta_servicio = self.equipo_presta_servicio,
                            esp_fis_servicio = self.esp_fis_servicio,
                            insumos_servicio = self.insumos_servicio,
                            condicion_ambiental = self.condicion_ambiental,
                            condicion_ambiental_detalle = self.condicion_ambiental_detalle)

        return actualizacion

    def conseguir_categorias(self):
        self.nombre_tipo = self.db(self.tipo == self.db.tipos_servicios.id).select(self.db.tipos_servicios.ALL)[0].nombre.decode('utf-8')
        self.nombre_categoria = self.db(self.categoria == self.db.categorias_servicios.id).select(self.db.categorias_servicios.ALL)[0].nombre.decode('utf-8')

        seccion_fila = self.db(self.dependencia == self.db.dependencias.id).select(self.db.dependencias.ALL)[0]

        self.seccion = seccion_fila.nombre.decode('utf-8')
        self.laboratorio = self.db(seccion_fila.unidad_de_adscripcion == self.db.dependencias.id).select(self.db.dependencias.ALL)[0].nombre.decode('utf-8')
        self.sede = self.db(seccion_fila.id_sede == self.db.sedes.id).select(self.db.sedes.ALL)[0].nombre.decode('utf-8')

        self.id_jefe_dependencia = seccion_fila.id_jefe_dependencia

        usuario_jefe_dependencia = self.db(self.id_jefe_dependencia == self.db.auth_user.id).select(self.db.auth_user.ALL)[0]

        self.jefe_dependencia = usuario_jefe_dependencia.first_name + " " + usuario_jefe_dependencia.last_name

        self.email_jefe_dependencia = usuario_jefe_dependencia.email

    def obtenerListaPropositos(self):
        self.propositos_a_mostrar = []


        if self.docencia == True:
            propositoServicio = self.db("Docencia" == self.db.propositos.tipo).select(self.db.propositos.ALL)[0]
            self.propositos_a_mostrar.append(propositoServicio)

        if self.investigacion == True:
            propositoServicio = self.db("Investigación" == self.db.propositos.tipo).select(self.db.propositos.ALL)[0]
            self.propositos_a_mostrar.append(propositoServicio)

        if self.extension == True:
            propositoServicio = self.db("Extensión" == self.db.propositos.tipo).select(self.db.propositos.ALL)[0]
            self.propositos_a_mostrar.append(propositoServicio)

        if self.gestion == True:
            propositoServicio = self.db("Gestión" == self.db.propositos.tipo).select(self.db.propositos.ALL)[0]
            self.propositos_a_mostrar.append(propositoServicio)


    def checkear_tags(self, tags, string):
        for tag in tags:
            string_compare = getattr(self, tag).decode('utf-8').upper()

            if tag == "laboratorio" and "LABORATORIO" in string_compare:
                ratio_str = fuzz.token_set_ratio(string_compare, string)
                if ratio_str >= 95:
                    print(ratio_str, string, string_compare)
                    return True
            else:
                ratio_str = fuzz.token_set_ratio(string_compare, string)
                if ratio_str >= 80:
                    print(ratio_str, string, string_compare)
                    return True

            print(ratio_str, string, string_compare)

        print("NO MATCH")
        return False   


#------------------------------------------------------------------------------
#
# Clase que permitira tomar la tabla servicios y crear un listado, incluira 
# funciones de paginado y ordenamiento.
#
#------------------------------------------------------------------------------

class ListaServicios(object):

    def __init__(self, db, dependencia, rol, orden=False, columna='id', central=1):

        #### Captura de datos desde la Base de Datos

        self.db = db

        # 1. Tomar servicios visibles o todos de la base de datos

        self.set = self.capturar_conjunto_por_rol(dependencia, rol)

        # Aqui se introducen los servicios instanciados
        self.filas = []

        # 2. Instanciar todos los servicios como objetos de la clase Servicio
        self.capturar_objetos()

        # Numero de servicios recuperados desde la base de datos
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

        # Lista de cada fila, convertida en el objeto servicio
        self.servicios_a_mostrar = []

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

    # Estas pueden ser nombre, id, nombre_tipo, nombre_columna, laboratorio, seccion, sede
    def cambiar_columna(self, columna):
        self.columna = columna

    def posicionar_ultimo(self):
        self.ultimo_elemento = min(self.pagina_central * 10, self.cuenta)

    def invertir_ordenamiento(self):
        self.orden = not(self.orden)

    def cambiar_ordenamiento(self, orden):
        self.orden = orden

    def capturar_conjunto_por_rol(self, dependencia, rol):
        if rol:
            if rol == 2:
                return self.db(self.db.servicios.id > 0)
            else:
                secciones = []
                dep = self.db(self.db.dependencias.unidad_de_adscripcion == dependencia).select(self.db.dependencias.id)

                for d in dep:
                    secciones.append(int(d.id))

                return self.db((any((self.db.servicios.dependencia == s) for s in secciones)) or (self.db.servicios.visibilidad == True))

        else:
            return self.db(self.db.servicios.visibilidad == True)

    def capturar_objetos(self):
        """
        Toma cada servicio de la base de datos, lo instancia como un objeto
        de la clase "Servicio" y luego lo anade a "filas" que es una lista
        tentativa de servicios. El listado final se encuentra en el arreglo
        "servicios_a_mostrar" pues son los servicios que ya pasaron por el
        filtro de 10 servicios por pagina mas por el ordenamiento.
        """
        for serv in self.set.select(self.db.servicios.id):
            servicio = Servicio(self.db)
            servicio.instanciar(serv.id)
            self.filas.append(servicio)

    def orden_y_filtrado(self):
        self.filas.sort(key=lambda serv: getattr(serv, self.columna), reverse=self.orden)
        self.servicios_a_mostrar = self.filas[(self.pagina_central - 1)*10:self.ultimo_elemento]

    def catalogo(self, categoria):
        lista_de_servicios_catalogo = []
        ensayo = []
        inspeccion = []
        calibracion = []
        desarrollo_prototipo_piezas = []
        consultoria_asesoria = []
        formacion_capacitacion_transferencia = []
        sala_computadoras = []
        sala_videos = []
        verificacion = []

        servicios_por_categoria = self.db(categoria == self.db.servicios.categoria).select(self.db.servicios.ALL)

        for servicio in servicios_por_categoria:
            serv = Servicio(self.db)
            serv.instanciar(servicio.id)
            lista_de_servicios_catalogo.append(serv)

        for servicio in lista_de_servicios_catalogo:
            if servicio.tipo == 1:
                ensayo.append(servicio)
            elif servicio.tipo == 2:
                inspeccion.append(servicio)
            elif servicio.tipo == 3:
                calibracion.append(servicio)
            elif servicio.tipo == 4:
                desarrollo_prototipo_piezas.append(servicio)
            elif servicio.tipo == 5:
                consultoria_asesoria.append(servicio)
            elif servicio.tipo == 6:
                formacion_capacitacion_transferencia.append(servicio)
            elif servicio.tipo == 7:
                sala_computadoras.append(servicio)
            elif servicio.tipo == 8:
                sala_videos.append(servicio)
            elif servicio.tipo == 9:
                verificacion.append(servicio)

        servicios_categoria_tipo = [ensayo, inspeccion, calibracion, desarrollo_prototipo_piezas, consultoria_asesoria, formacion_capacitacion_transferencia, sala_computadoras, sala_videos, verificacion]


        return servicios_categoria_tipo


    # Estas pueden ser nombre, nombre_tipo, nombre_columna, laboratorio, seccion, sede
    def filtrar_por_tags(self, filtro, tags=None):
        filtro = filtro.decode('utf-8').upper()
        if tags is None:
            tags = ["nombre", "nombre_tipo", "nombre_categoria", "laboratorio", "seccion", "sede"]

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
        fecha_solicitud = None, id_servicio_solicitud = None,  id_proposito_servicio = None,
        proposito_descripcion = None, proposito_cliente_final = None, descripcion_servicio = None,
        observaciones = None, estado_solicitud = None, proyecto = None, fecha_certificacion = None):

        self.registro = registro
        self.id_responsable_solicitud = id_responsable_solicitud
        self.fecha_solicitud = fecha_solicitud
        self.id_servicio_solicitud = id_servicio_solicitud
        self.id_proposito_servicio = id_proposito_servicio
        self.proposito_descripcion = proposito_descripcion
        self.proposito_cliente_final = proposito_cliente_final
        self.descripcion_servicio = descripcion_servicio
        self.observaciones = observaciones
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
        self.lugar_ejecucion_servicio = None
        self.nombre_servicio = None
        self.tipo_servicio = None
        self.categoria_servicio = None
        self.nombre_proposito = None
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
        self.proyecto = proyecto
        self.fecha_certificacion = fecha_certificacion

        if registro != None:
            self.conseguir_atributos()

    def __str__(self):

        return self.registro

    def insertar(self):

        insercion = self.db.solicitudes.insert( registro = self.registro,
                                                responsable = self.id_responsable_solicitud,
                                                fecha = self.fecha_solicitud,
                                                id_servicio_solicitud = self.id_servicio_solicitud,
                                                proposito = self.id_proposito_servicio,
                                                proposito_descripcion = self.proposito_descripcion,
                                                proposito_cliente_final = self.proposito_cliente_final,
                                                descripcion = self.descripcion_servicio,
                                                observaciones = self.observaciones,
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
            self.id_servicio_solicitud = instanciacion[0].id_servicio_solicitud
            self.id_proposito_servicio = instanciacion[0].proposito
            self.proposito_descripcion = instanciacion[0].proposito_descripcion
            self.proposito_cliente_final = instanciacion[0].proposito_cliente_final
            self.descripcion_servicio = instanciacion[0].descripcion
            self.observaciones = instanciacion[0].observaciones
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
        id_servicio_solicitud, id_proposito_servicio, proposito_descripcion,
        proposito_cliente_final, descripcion_servicio, observaciones):

        self.registro = registro
        self.id_responsable_solicitud = id_responsable_solicitud
        self.fecha_solicitud = fecha_solicitud
        self.id_servicio_solicitud = id_servicio_solicitud
        self.id_proposito_servicio = id_proposito_servicio
        self.proposito_descripcion = proposito_descripcion
        self.proposito_cliente_final = proposito_cliente_final
        self.descripcion_servicio = descripcion_servicio
        self.observaciones = observaciones

        self.conseguir_atributos()

    def actualizar(self, id):

        actualizacion = self.db(self.db.solicitudes.id == id).update(
                                                registro = self.registro,
                                                responsable = self.id_responsable_solicitud,
                                                fecha = self.fecha_solicitud,
                                                id_servicio_solicitud = self.id_servicio_solicitud,
                                                proposito = self.id_proposito_servicio,
                                                proposito_descripcion = self.proposito_descripcion,
                                                proposito_cliente_final = self.proposito_cliente_final,
                                                descripcion = self.descripcion_servicio,
                                                observaciones = self.observaciones,
                                                estado = self.estado_solicitud,
                                                aprobada_por = self.aprobada_por,
                                                fecha_aprobacion = self.fecha_aprobacion,
                                                elaborada_por = self.elaborada_por,
                                                fecha_elaboracion = self.fecha_elaboracion)

        return actualizacion

    def eliminar(self, id):

        self.db(self.db.solicitudes.id == id).delete()

    def conseguir_atributos(self):
        # Nombre de Proposito del Servicio
        self.nombre_proposito = self.db(self.id_proposito_servicio == self.db.propositos.id).select(self.db.propositos.ALL)[0].tipo


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

        self.id_dependencia_ejecutora = self.db(self.id_servicio_solicitud == self.db.servicios.id).select(self.db.servicios.ALL)[0].dependencia

        dependencia_ejecutora_servicio = self.db(self.id_dependencia_ejecutora == self.db.dependencias.id).select(self.db.dependencias.ALL)[0]

        self.id_adscripcion_dependencia_ejecutora = dependencia_ejecutora_servicio.unidad_de_adscripcion

        if self.id_adscripcion_dependencia_ejecutora != None:
            self.adscripcion_dependencia_ejecutora = self.db(self.id_adscripcion_dependencia_ejecutora == self.db.dependencias.id).select(self.db.dependencias.ALL)[0].nombre

        else:
            self.adscripcion_dependencia_ejecutora = "VICERRECTORADO ACADÉMICO"       

        # Dependencia Ejecutora del Servicio
        self.nombre_dependencia_ejecutora = dependencia_ejecutora_servicio.nombre

        # Jefe de la Dependencia Ejecutora del Servicio
        self.usuario_jefe_dependencia_ejecutora = self.db(dependencia_ejecutora_servicio.id_jefe_dependencia == self.db.auth_user.id).select(self.db.auth_user.ALL)[0]

        self.jefe_dependencia_ejecutora = self.usuario_jefe_dependencia_ejecutora.first_name + " " + self.usuario_jefe_dependencia_ejecutora.last_name

        # Lugar de Ejecucion de Servicio

        id_ubicacion_ejecucion = self.db(self.id_servicio_solicitud == self.db.servicios.id).select(self.db.servicios.ALL)[0].ubicacion

        self.lugar_ejecucion_servicio = self.db(id_ubicacion_ejecucion == self.db.espacios_fisicos.id).select(self.db.espacios_fisicos.ALL)[0].codigo

        # Nombre de Servicio

        self.nombre_servicio = self.db(self.id_servicio_solicitud == self.db.servicios.id).select(self.db.servicios.ALL)[0].nombre

        # Nombre Tipo de Servicio

        id_tipo_servicio = self.db(self.id_servicio_solicitud == self.db.servicios.id).select(self.db.servicios.ALL)[0].tipo
        self.tipo_servicio = self.db(id_tipo_servicio == self.db.tipos_servicios.id).select(self.db.tipos_servicios.ALL)[0].nombre

        id_categoria_servicio = self.db(self.id_servicio_solicitud == self.db.servicios.id).select(self.db.servicios.ALL)[0].categoria
        self.categoria_servicio = self.db(id_categoria_servicio == self.db.categorias_servicios.id).select(self.db.categorias_servicios.ALL)[0].nombre

    def cambiar_estado(self, estado, request):
        self.estado_solicitud = estado
        if estado == 2:
            # Fecha de elaboracion del servicio
            self.fecha_elaboracion = request.now
            # Persona responsable de la solicitud y Elaborado por
            self.elaborada_por = "%s %s" % (self.auth.user.first_name, self.auth.user.last_name)

        elif estado == 1:
            # Fecha de elaboracion del servicio
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

    def certificar(self, request):
        self.estado_solicitud = 3
        self.fecha_certificacion = request.now
        self.estado_solicitud_str = self.estado_string()
        self.actualizar(self.id)

    def guardar_en_historial(self):
        historial = Historial(self.db, self.auth, self)

        historial.insertar()

    def correoHacerSolicitud(self):
        nombre_jefe_dependencia = self.jefe_dependencia_ejecutora
        email_jefe_dependencia = self.usuario_jefe_dependencia_ejecutora.email
        nombre_solicitante = self.nombre_responsable_solicitud
        email_solicitante = self.email_responsable_solicitud
        nombre_servicio = self.nombre_servicio
        nombre_solicitante = self.nombre_responsable_solicitud
        nombre_dependencia = self.nombre_dependencia_ejecutora
        numero_registro = self.registro 

        # Se le manda el email al jefe de la dependencia a la que pertenece el servicio
        correo = '<html><head><meta charset="UTF-8"></head><body><table><tr><td><p>Hola, %s.</p><br><p>Se ha hecho una solicitud del servicio %s. La operación fue realizada por %s, el/la cual pertenece a la dependencia de %s.</p><br><p>Para consultar dicha operación diríjase a la página web <a href="159.90.171.24">SIGULAB</a></p></td></tr></table></body></html>' % (nombre_jefe_dependencia, nombre_servicio, nombre_solicitante, nombre_dependencia)

        asunto = numero_registro + ' [SIGULAB] ' + 'Se ha solicitado un servicio'

        enviar_correo(self.auth, email_jefe_dependencia, asunto, correo)

        # Se le manda el email al responsable de la solicitud
        correo = '<html><head><meta charset="UTF-8"></head><body><table><tr><td><p>Hola, %s.</p><br><p>Se ha hecho su solicitud del servicio %s.</p><br><p>Para consultar dicha operación diríjase a la página web <a href="159.90.171.24">SIGULAB</a></p></td></tr></table></body></html>' % (nombre_solicitante, nombre_servicio)

        asunto =  numero_registro + '[SIGULAB] ' + 'Se ha solicitado un servicio'

        enviar_correo(self.auth, email_solicitante, asunto, correo)

    def correoCambioEstadoSolicitud(self):
        nombre_solicitante = self.nombre_responsable_solicitud
        email_solicitante = self.email_responsable_solicitud
        nombre_servicio = self.nombre_servicio
        estado_solicitud = self.estado_solicitud
        nombre_estado_solicitud = self.estado_solicitud_str
        numero_registro = self.registro 

        if estado_solicitud != 2:
            correo = '<html><head><meta charset="UTF-8"></head><body><table><tr><td><p>Hola, %s.</p><br><p>Su solicitud del servicio %s ha cambiado al estado a %s.</p><br><p>Para consultar dicha operación diríjase a la página web <a href="159.90.171.24">SIGULAB</a></p></td></tr></table></body></html>' % (nombre_solicitante, nombre_servicio, nombre_estado_solicitud)

            asunto = numero_registro + ' [SIGULAB] ' + 'Se ha cambiado el estado de su solicitud'

            enviar_correo(self.auth, email_solicitante, asunto, correo)

    def correoSolicitudFinalizada(self):
        estado_solicitud = self.estado_solicitud
        email_jefe_dependencia = self.usuario_jefe_dependencia_ejecutora.email
        nombre_servicio = self.nombre_servicio
        nombre_dependencia_solicitante = self.nombre_dependencia_solicitante
        nombre_jefe_dependencia_solicitante = self.nombre_jefe_dependencia_solicitante
        nombre_solicitante = self.nombre_responsable_solicitud
        email_solicitante = self.email_responsable_solicitud
        extensiones_solicitante = self.telef_responsable_solicitud
        categoria_servicio = self.categoria_servicio
        tipo_servicio = self.tipo_servicio
        proposito_servicio = self.nombre_proposito
        descripcion_proposito_servicio = self.proposito_descripcion
        descripcion_servicio = self.descripcion_servicio
        nombre_dependencia_ejecutora = self.nombre_dependencia_ejecutora
        nombre_jefe_dependencia_ejecutora = self.jefe_dependencia_ejecutora
        observaciones_solicitud = self.observaciones
        solicitud_elaborada_por = self.elaborada_por
        solicitud_aprobada_por = self.aprobada_por
        fecha_elaboracion_solicitud = self.fecha_elaboracion
        fecha_aprobacion_solicitud = self.fecha_aprobacion
        numero_registro = self.registro 

        if estado_solicitud == 2:
            correo = '<html><head><meta charset="UTF-8"></head><body><table><tr><td><p>A continuación se encuentran los datos del servicio que solicitó:</p><p>Servicio solicitado: %s</p><p>Dependencia del solicitante: %s</p><p>Jefe de la dependencia del solicitante: %s</p><p>Responsable de la solicitud: %s</p><p>Email del respponsable de la solicitud: %s</p><p>Telf. del responsable de la solicitud: %d</p><p>Categoría del servicio: %s</p><p>Tipo del servicio: %s</p><p>Propósito del servicio: %s<p>Descripción del propósito del servicio: %s</p><p>Descripción del servicio: %s</p><p>Dependencia ejecutora del servicio: %s</p><p>Jefe de la dependencia ejecutora del servicio: %s</p><p>Observaciones: %s</p><p>Solicitud elaborada por: %s</p><p>Fecha de elaboración de la solicitud: %s</p><p>Solicitud aprobada por: %s</p><p>Fecha de aprobación de la solicitud: %s</p><br><p>Para imprimir el PDF diríjase a la página web <a href="159.90.171.24">SIGULAB</a></p></td></tr></table></body></html>' % (nombre_servicio, nombre_dependencia_solicitante, nombre_jefe_dependencia_solicitante, nombre_solicitante, email_solicitante, extensiones_solicitante, categoria_servicio, tipo_servicio, proposito_servicio, descripcion_proposito_servicio, descripcion_servicio, nombre_dependencia_ejecutora, nombre_jefe_dependencia_ejecutora, observaciones_solicitud, solicitud_elaborada_por, fecha_elaboracion_solicitud, solicitud_aprobada_por, fecha_aprobacion_solicitud)

            asunto = numero_registro + ' [SIGULAB] ' + 'Solicitud de Servicio'

            enviar_correo(self.auth, email_jefe_dependencia, asunto, correo)


    def correoCertificacionFinalizada(self):
        estado_solicitud = self.estado_solicitud
        email_jefe_dependencia = self.usuario_jefe_dependencia_ejecutora.email
        nombre_solicitante = self.nombre_responsable_solicitud
        email_solicitante = self.email_responsable_solicitud
        nombre_dependencia_solicitante = self.nombre_dependencia_solicitante
        nombre_dependencia_ejecutora = self.nombre_dependencia_ejecutora
        nombre_servicio = self.nombre_servicio
        registro = self.registro
        fecha_solicitud = self.fecha_solicitud
        fecha_certificacion = self.fecha_certificacion
        cargo_solicitante = self.cargo_responsable_solicitud
        numero_registro = self.registro 

        if estado_solicitud == 3:
            correo = '<html><head><meta charset="UTF-8"></head><body><table><tr><td><p>Quien suscribe, %s (%s), como responsable de la %s, certifico la conformidad con el(los) trabajo(s) realizado(s) por el/la %s, correspondiente a la Solicitud/orden de servicio identificado como %s, de fecha %s.</p><br><p>%s</p><br><p>%s</p><br><p>Para imprimir el PDF diríjase a la página web <a href="159.90.171.24">SIGULAB</a></p></td></tr></table></body></html>' % (nombre_solicitante, email_solicitante, nombre_dependencia_solicitante, nombre_dependencia_ejecutora, registro, fecha_solicitud, nombre_solicitante, nombre_dependencia_solicitante)

            asunto = numero_registro + ' [SIGULAB] ' + 'Certificación de Servicio'

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

        # Lista de cada fila, convertida en el objeto servicio
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

    # Estas pueden ser nombre, id, nombre_tipo, nombre_columna, laboratorio, seccion, sede
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
        self.filas.sort(key=lambda serv: getattr(serv, self.columna), reverse=self.orden)
        self.solicitudes_a_mostrar = self.filas[(self.pagina_central - 1)*10:self.ultimo_elemento]

#------------------------------------------------------------------------------
#
# Clase certificacion de servicio, sera representada por la tabla historial
#
#------------------------------------------------------------------------------

class Certificacion(object):

    def __init__(self, db, registro=None, responsable_solicitud=None, fecha_solicitud=None,
        id_servicio=None, proposito=None, proposito_descripcion=None, proposito_cliente_final=None, descripcion=None,
        observaciones=None, aprobada_por=None, fecha_aprobacion=None, elaborada_por=None,
        fecha_elaboracion=None, fecha_certificacion=None, proyecto=None, estado=None):

        self.db = db

        # Solicitud
        self.id_servicio = id_servicio
        self.registro = registro
        self.responsable_solicitud = responsable_solicitud
        self.fecha_solicitud = fecha_solicitud
        self.proposito = proposito
        self.proposito_descripcion = proposito_descripcion
        self.proposito_cliente_final = proposito_cliente_final
        self.descripcion = descripcion
        self.fecha_aprobacion = fecha_aprobacion
        self.elaborada_por = elaborada_por
        self.observaciones = observaciones
        self.aprobada_por = aprobada_por
        self.fecha_elaboracion = fecha_elaboracion
        self.estado = estado

        # Certificacion
        self.proyecto = proyecto
        self.fecha_certificacion = fecha_certificacion

        # Datos de instanciacion para su categorizacion

        self.id = None

        # En el listado de Certificaciones:
        self.nombre_servicio = None
        self.solicitante = None
        self.dependencia_ejecutora = None
        self.dependencia_ejecutora_id = None

        # En el Historial:
        self.unidad_adscripcion = None

    def instanciar(self, id):
        instanciacion = self.db(self.db.historial_solicitudes.id == id).select(self.db.historial_solicitudes.ALL)

        if (len(instanciacion) == 1):
            # Solicitud
            self.id_servicio = instanciacion[0].id_servicio
            self.registro = instanciacion[0].registro
            self.responsable_solicitud = instanciacion[0].responsable_solicitud
            self.fecha_solicitud = instanciacion[0].fecha_solicitud
            self.proposito = instanciacion[0].proposito
            self.proposito_descripcion = instanciacion[0].proposito_descripcion
            self.proposito_cliente_final = instanciacion[0].proposito_cliente_final
            self.descripcion = instanciacion[0].descripcion
            self.observaciones = instanciacion[0].observaciones
            self.aprobada_por = instanciacion[0].aprobada_por
            self.fecha_aprobacion = instanciacion[0].fecha_aprobacion
            self.elaborada_por = instanciacion[0].elaborada_por
            self.fecha_elaboracion = instanciacion[0].fecha_elaboracion
            self.estado = instanciacion[0].estado

            self.nombre_servicio = self.db(self.db.servicios.id == self.id_servicio).select(self.db.servicios.nombre)[0].nombre
            self.solicitante = self.db(self.db.t_Personal.id == self.responsable_solicitud).select(self.db.t_Personal.f_nombre)[0].f_nombre

            dep = self.db(self.db.servicios.id == self.id_servicio).select(self.db.servicios.dependencia).first().dependencia
            self.dependencia_ejecutora_id = dep
            self.dependencia_ejecutora = self.db(self.db.dependencias.id == dep).select().first()

            if self.estado == 1:
                # Certificacion
                self.proyecto = instanciacion[0].proyecto
                self.fecha_certificacion = instanciacion[0].fecha_certificacion

                # En el Historial:
                self.unidad_adscripcion = self.db(dep.unidad_de_adscripcion == self.db.dependencias.id).select(self.db.dependencias.nombre).first().nombre

            # Datos de instanciacion para su categorizacion
            self.id = id

    def insertar(self):

        insercion = self.db.historial_solicitudes.insert(id_servicio = self.id_servicio,
                                        registro = self.registro,
                                        responsable_solicitud = self.responsable_solicitud,
                                        fecha_solicitud = self.fecha_solicitud,
                                        proposito = self.proposito,
                                        proposito_descripcion = self.proposito_descripcion,
                                        proposito_cliente_final = self.proposito_cliente_final,
                                        descripcion = self.descripcion,
                                        observaciones = self.observaciones,
                                        aprobada_por = self.aprobada_por,
                                        fecha_aprobacion = self.fecha_aprobacion,
                                        elaborada_por = self.elaborada_por,
                                        fecha_elaboracion = self.fecha_elaboracion,
                                        estado = self.estado,
                                        proyecto = self.proyecto,
                                        fecha_certificacion = self.fecha_certificacion,)

        return insercion

    def certificar(self):
        certificar = self.db(self.db.historial_solicitudes.id == self.id).update(
            estado = 1)

        self.instanciar(self.id)

        self.estado = 1

        return certificar

    def __str__(self):
        return self.registro


class Historial(object):

    def __init__(self, db, auth, solicitud = None):

        
        if solicitud:
            # VARIABLES PARA SOLICITUD

            self.registro_solicitud = solicitud.registro
            self.proposito_solicitud = solicitud.nombre_proposito
            self.proposito_solicitud_descripcion = solicitud.proposito_descripcion
            self.descripcion_solicitud = solicitud.descripcion_servicio
            self.observaciones_solicitud = solicitud.observaciones
            self.responsable_solicitud = solicitud.nombre_responsable_solicitud
            self.email_responsable_solicitud = solicitud.email_responsable_solicitud
            self.telefono_responsable_solicitud = solicitud.telef_responsable_solicitud
            self.nombre_dependencia_solicitante = solicitud.nombre_dependencia_solicitante
            self.nombre_jefe_dependencia_solicitante = solicitud.nombre_jefe_dependencia_solicitante
            self.nombre_dependencia_ejecutora = solicitud.nombre_dependencia_ejecutora
            self.nombre_jefe_dependencia_ejecutora = solicitud.jefe_dependencia_ejecutora
            self.lugar_ejecucion_servicio = solicitud.lugar_ejecucion_servicio
            self.nombre_servicio = solicitud.nombre_servicio
            self.tipo_servicio = solicitud.tipo_servicio
            self.categoria_servicio = solicitud.categoria_servicio
            self.solicitud_aprobada_por = solicitud.aprobada_por
            self.fecha_aprobacion_solicitud = solicitud.fecha_aprobacion
            self.fecha_elaboracion_solicitud = solicitud.fecha_elaboracion
            self.solicitud_elaborada_por = solicitud.elaborada_por
            self.adscripcion_dependencia_solicitante = solicitud.adscripcion_dependencia_solicitante
            self.adscripcion_dependencia_ejecutora = solicitud.adscripcion_dependencia_ejecutora      


            # VARIABLES PARA CERTIFICACION
            self.fecha_solicitud = solicitud.fecha_solicitud
            self.cargo_responsable_solicitud = solicitud.cargo_responsable_solicitud
            self.ci_responsable_solicitud = solicitud.ci_responsable_solicitud

            self.fecha_certificacion = solicitud.fecha_certificacion
            self.numero_de_proyecto = solicitud.proyecto
            

        # VARIABLES DE INSTANCIACION
        self.id = None
        self.db = db
        self.auth = auth
    
    def __str__(self):
       
        return self.registro 

    def insertar(self):

        insercion = self.db.historial_solicitudes.insert(registro_solicitud = self.registro_solicitud,
                                                       nombre_servicio = self.nombre_servicio,
                                                       tipo_servicio = self.tipo_servicio,
                                                       categoria_servicio = self.categoria_servicio,
                                                       proposito_solicitud = self.proposito_solicitud,
                                                       proposito_solicitud_descripcion = self.proposito_solicitud_descripcion,
                                                       descripcion_solicitud = self.descripcion_solicitud,
                                                       observaciones_solicitud = self.observaciones_solicitud,
                                                       responsable_solicitud = self.responsable_solicitud,
                                                       ci_responsable_solicitud = self.ci_responsable_solicitud,
                                                       email_responsable_solicitud = self.email_responsable_solicitud,
                                                       telefono_responsable_solicitud = self.telefono_responsable_solicitud,
                                                       cargo_responsable_solicitud = self.cargo_responsable_solicitud,
                                                       nombre_dependencia_solicitante = self.nombre_dependencia_solicitante,
                                                       nombre_jefe_dependencia_solicitante = self.nombre_jefe_dependencia_solicitante,
                                                       fecha_solicitud = self.fecha_solicitud,
                                                       nombre_dependencia_ejecutora = self.nombre_dependencia_ejecutora,
                                                       nombre_jefe_dependencia_ejecutora = self.nombre_jefe_dependencia_ejecutora,
                                                       lugar_ejecucion_servicio = self.lugar_ejecucion_servicio,
                                                       solicitud_aprobada_por = self.solicitud_aprobada_por,
                                                       fecha_aprobacion_solicitud = self.fecha_aprobacion_solicitud,
                                                       fecha_elaboracion_solicitud = self.fecha_elaboracion_solicitud,
                                                       solicitud_elaborada_por = self.solicitud_elaborada_por,
                                                       fecha_certificacion = self.fecha_certificacion,
                                                       numero_de_proyecto = self.numero_de_proyecto,
                                                       adscripcion_dependencia_solicitante = self.adscripcion_dependencia_solicitante,
                                                       adscripcion_dependencia_ejecutora = self.adscripcion_dependencia_ejecutora )

                                    

        return insercion

    def instanciar(self, id):
        instanciacion = self.db(self.db.historial_solicitudes.id == id).select(self.db.historial_solicitudes.ALL)


        if (len(instanciacion) == 1):

            self.id = instanciacion[0].id

            self.registro_solicitud = instanciacion[0].registro_solicitud
            self.nombre_servicio = instanciacion[0].nombre_servicio
            self.tipo_servicio = instanciacion[0].tipo_servicio
            self.categoria_servicio = instanciacion[0].categoria_servicio
            self.proposito_solicitud = instanciacion[0].proposito_solicitud
            self.proposito_solicitud_descripcion = instanciacion[0].proposito_solicitud_descripcion
            self.descripcion_solicitud = instanciacion[0].descripcion_solicitud
            self.observaciones_solicitud = instanciacion[0].observaciones_solicitud
            self.responsable_solicitud = instanciacion[0].responsable_solicitud
            self.ci_responsable_solicitud = instanciacion[0].ci_responsable_solicitud
            self.email_responsable_solicitud = instanciacion[0].email_responsable_solicitud
            self.telefono_responsable_solicitud = instanciacion[0].telefono_responsable_solicitud
            self.cargo_responsable_solicitud = instanciacion[0].cargo_responsable_solicitud
            self.nombre_dependencia_solicitante = instanciacion[0].nombre_dependencia_solicitante
            self.nombre_jefe_dependencia_solicitante = instanciacion[0].nombre_jefe_dependencia_solicitante
            self.fecha_solicitud = instanciacion[0].fecha_solicitud
            self.nombre_dependencia_ejecutora = instanciacion[0].nombre_dependencia_ejecutora
            self.nombre_jefe_dependencia_ejecutora = instanciacion[0].nombre_jefe_dependencia_ejecutora
            self.lugar_ejecucion_servicio = instanciacion[0].lugar_ejecucion_servicio
            self.solicitud_aprobada_por = instanciacion[0].solicitud_aprobada_por
            self.fecha_aprobacion_solicitud = instanciacion[0].fecha_aprobacion_solicitud
            self.fecha_elaboracion_solicitud = instanciacion[0].fecha_elaboracion_solicitud
            self.solicitud_elaborada_por = instanciacion[0].solicitud_elaborada_por
            self.fecha_certificacion = instanciacion[0].fecha_certificacion
            self.numero_de_proyecto = instanciacion[0].numero_de_proyecto
            self.adscripcion_dependencia_solicitante = instanciacion[0].adscripcion_dependencia_solicitante
            self.adscripcion_dependencia_ejecutora = instanciacion[0].adscripcion_dependencia_ejecutora   

            return True
        else:
            return False

    def eliminar(self, id):
        
        self.db(self.db.historial_solicitudes.id == id).delete()

    def generacion_pdf(self):
        self.registro = self.registro_solicitud
        self.nombre_proposito = self.proposito_solicitud
        self.proposito_descripcion = self.proposito_solicitud_descripcion
        self.descripcion_servicio = self.descripcion_solicitud
        self.observaciones = self.observaciones_solicitud
        self.nombre_responsable_solicitud = self.responsable_solicitud
        self.email_responsable_solicitud = self.email_responsable_solicitud
        self.telef_responsable_solicitud = self.telefono_responsable_solicitud
        self.nombre_dependencia_solicitante = self.nombre_dependencia_solicitante
        self.nombre_jefe_dependencia_solicitante = self.nombre_jefe_dependencia_solicitante
        self.nombre_dependencia_ejecutora = self.nombre_dependencia_ejecutora
        self.jefe_dependencia_ejecutora = self.nombre_jefe_dependencia_ejecutora
        self.lugar_ejecucion_servicio = self.lugar_ejecucion_servicio
        self.nombre_servicio = self.nombre_servicio
        self.tipo_servicio = self.tipo_servicio
        self.categoria_servicio = self.categoria_servicio
        self.aprobada_por = self.solicitud_aprobada_por
        self.fecha_aprobacion = self.fecha_aprobacion_solicitud
        self.fecha_elaboracion = self.fecha_elaboracion_solicitud
        self.elaborada_por = self.solicitud_elaborada_por
        self.ci_responsable_solicitud = self.ci_responsable_solicitud
        self.fecha_certificacion = self.fecha_certificacion
        self.proyecto = self.numero_de_proyecto


class ListaHistorial(object):

    def __init__(self, db, auth, tipo_listado, orden=False, columna='id', central=1):
        self.db = db
        self.auth = auth
        self.tipo_listado = tipo_listado

        # Dependencia del usuario para filtrar la lista
        personal_del_usuario = db(db.t_Personal.f_usuario == auth.user.id).select().first()

        self.id_personal = personal_del_usuario.id
        self.id_dependencia_usuario = personal_del_usuario.f_dependencia

        # Instanciacion de cada solicitud en la bd
        self.set = self.db(self.db.historial_solicitudes.id > 0)
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

        self.rango_paginas = range(max(self.primera_pagina, self.pagina_central - 2),
                                   min(self.pagina_central + 2, self.ultima_pagina) + 1)

        # Configuraremos estos botones
        self.configurar_botones()

        # Posicion del ultimo elemento segun la pagina actual (Lo posicionamos)
        self.ultimo_elemento = self.cuenta

        self.posicionar_ultimo()

        # Lista de cada fila, convertida en el objeto servicio
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

        self.rango_paginas = range(max(self.primera_pagina, self.pagina_central - 2),
                                   min(self.pagina_central + 2, self.ultima_pagina) + 1)

    def cambiar_pagina(self, nueva_pagina):
        self.pagina_central = nueva_pagina
        self.configurar_botones()
        self.posicionar_ultimo()

    def posicionar_ultimo(self):
        self.ultimo_elemento = min(self.pagina_central * 10, self.cuenta)

    def invertir_ordenamiento(self):
        self.orden = not (self.orden)

    def cambiar_ordenamiento(self, orden):
        self.orden = orden

    # Estas pueden ser:
    def cambiar_columna(self, columna):
        self.columna = columna

    def capturar_objetos(self):
        for hist in self.set.select(self.db.historial_solicitudes.ALL):
            historial = Historial(self.db, self.auth)
            historial.instanciar(hist.id)

            self.filas.append(historial)

    def orden_y_filtrado(self):
        self.filas.sort(key=lambda serv: getattr(serv, self.columna), reverse=self.orden)
        self.solicitudes_a_mostrar = self.filas[(self.pagina_central - 1) * 10:self.ultimo_elemento]

#------------------------------------------------------------------------------
#
# Funciones para listar Categorias, Tipos y Sedes
# funciones de paginado y ordenamiento.
#
#--------------------------x----------------------------------------------------

def listar_categorias(db):
    query = db().select(db.categorias_servicios.ALL)

    return query

def listar_tipos(db):
    query = db().select(db.tipos_servicios.ALL)

    return query

def listar_sedes(db):
    query = db().select(db.sedes.ALL)

    return query

#------------------------------------------------------------------------------
#
# Funcion para hacer query de Ficha de Servicio
#
#------------------------------------------------------------------------------

def query_ficha(db, idv):
    entrada = db(db.servicios.id == idv).select(db.servicios.ALL)


    # Categoria
    categrow = db(entrada[0].categoria == db.categorias_servicios.id).select(db.categorias_servicios.ALL)
    categoria = categrow[0].nombre

    # Tipo
    tiporow = db(entrada[0].tipo == db.tipos_servicios.id).select(db.tipos_servicios.ALL)
    tipo = tiporow[0].nombre

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
                         "categoria": categoria,
                         "tipo": tipo,
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