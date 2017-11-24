#------------------------------------------------------------------------------
#
# Clase que permite tomar un record de la tabla servicios y realizar cada 
# accion del CRUD de una manera rapida y ordenada
#
#------------------------------------------------------------------------------


class Servicio(object):


	def __init__(self, db, nombre = None, tipo = None, categoria = None,
				 objetivo = None, alcance = None, metodo = None, rango = None,
				 incertidumbre = None, item_ensayar = None, requisitos = None, 
				 resultados = None, docencia = None, investigacion = None,
				 gestion = None, extension = None, visibilidad = None, 
				 responsable = None, dependencia = None, ubicacion = None, id=None):

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
		self.resultados = resultados
		self.docencia = docencia
		self.investigacion = investigacion
		self.gestion = gestion
		self.extension = extension
		self.visibilidad = visibilidad
		self.responsable = responsable
		self.dependencia = dependencia
		self.ubicacion = ubicacion

		# Categorias de Ordenamiento, disponibles tras instanciacion
		self.nombre_tipo = None
		self.nombre_categoria = None
		self.laboratorio = None
		self.seccion = None
		self.sede = None
		self.id = None	

		self.db = db


	def __str__(self):

		return self.nombre


	def insertar(self):
		
		insercion = self.db.servicios.insert(nombre = self.nombre,
			tipo = self.tipo, categoria = self.categoria, objetivo = self.objetivo, 
			alcance = self.alcance, metodo = self.metodo, rango = self.rango, 
			incertidumbre = self.incertidumbre, item_ensayar = self.item_ensayar, 
			requisitos = self.requisitos, resultados = self.resultados, 
			docencia = self.docencia, investigacion = self.investigacion, 
			gestion = self.gestion, extension = self.extension, 
			visibilidad = self.visibilidad, responsable = self.responsable, 
			dependencia = self.dependencia, ubicacion = self.ubicacion)

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
			self.resultados = instanciacion[0].resultados
			self.docencia = instanciacion[0].docencia
			self.investigacion = instanciacion[0].investigacion
			self.gestion = instanciacion[0].gestion
			self.extension = instanciacion[0].extension
			self.visibilidad = instanciacion[0].visibilidad
			self.responsable = instanciacion[0].responsable
			self.dependencia = instanciacion[0].dependencia
			self.ubicacion = instanciacion[0].ubicacion

			self.conseguir_categorias()

			return True
		
		else:

			return False


	def editar(self, nombre, tipo, categoria, objetivo, alcance, metodo,
			   rango, incertidumbre, item_ensayar, requisitos, resultados,
			   docencia, investigacion, gestion, extension, visibilidad, 
			   responsable, dependencia, ubicacion):

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
		self.resultados = resultados
		self.docencia = docencia
		self.investigacion = investigacion
		self.gestion = gestion
		self.extension = extension
		self.visibilidad = visibilidad
		self.responsable = responsable
		self.dependencia = dependencia
		self.ubicacion = ubicacion


	def actualizar(self, id):
	    
	    actualizacion = self.db(self.db.servicio.id == id).update(
							nombre = self.nombre, 
							tipo = self.tipo,
							categoria = self.categoria, 
							objetivo = self.objetivo,
							alcance = self.alcance,
							metodo = self.metodo,
							rango = self.rango,
							incertidumbre = self.incertidumbre,
							item_ensayar = self.item_ensayar,
							requisitos = self.requisitos,
							resultados = self.resultados,
							docencia = self.docencia,
							investigacion = self.investigacion,
							gestion = self.gestion,
							extension = self.extension,
							visibilidad = self.visibilidad,
							responsable = self.responsable,
							dependencia = self.dependencia,
							ubicacion = self.ubicacion)

	    return actualizacion


	def conseguir_categorias(self):
		self.nombre_tipo = self.db(self.tipo == self.db.tipos_servicios.id).select(self.db.tipos_servicios.ALL)[0].nombre		
		self.nombre_categoria = self.db(self.categoria == self.db.categorias_servicios.id).select(self.db.categorias_servicios.ALL)[0].nombre		
		
		seccion_fila = self.db(self.dependencia == self.db.dependencias.id).select(self.db.dependencias.ALL)[0]

		self.seccion = seccion_fila.nombre
		self.laboratorio = self.db(seccion_fila.unidad_de_adscripcion == self.db.dependencias.id).select(self.db.dependencias.ALL)[0].nombre
		self.sede = self.db(seccion_fila.id_sede == self.db.sedes.id).select(self.db.sedes.ALL)[0].nombre


#------------------------------------------------------------------------------
#
# Clase que permitira tomar la tabla servicios y crear un listado, incluira 
# funciones de paginado y ordenamiento.
#
#------------------------------------------------------------------------------


class ListaServicios(object):

	def __init__(self, db, orden=False, columna='id', central=1):
		self.db = db

		# Instanciacion de cada servicio en la bd
		self.set = self.db(self.db.servicios.id > 0)
		self.filas = []
		self.capturar_objetos()

		self.cuenta = self.set.count()

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
		for serv in self.set.select(self.db.servicios.id):
			servicio = Servicio(self.db)
			servicio.instanciar(serv.id)
			self.filas.append(servicio)

	def orden_y_filtrado(self):
		self.filas.sort(key=lambda serv: getattr(serv, self.columna), reverse=self.orden)
		self.servicios_a_mostrar = self.filas[(self.pagina_central - 1)*10:self.ultimo_elemento]


#------------------------------------------------------------------------------
#
# Solicitud y Listado de Solicitudes
#
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#
# Funciones para listar Categorias, Tipos y Sedes
# funciones de paginado y ordenamiento.
#
#------------------------------------------------------------------------------

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
    ubicrow = db(entrada[0].ubicacion == db.espacios_fisicos.id).select(db.espacios_fisicos.ALL)
    ubicacion = ubicrow[0].nombre
    ubicacionid = ubicrow[0].id

    # Responsable
    resprow = db(entrada[0].responsable == db.personal.id).select(db.personal.ALL)
    responsable = resprow[0].nombre
    respid = resprow[0].id

    # Numeros
    telefono = resprow[0].telefono

    # Correo
    email = resprow[0].email

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
# Clase Solicitudes
#
#------------------------------------------------------------------------------

class Solicitudes(object):

	def __init__(self, db, id=None, registro=None, dependencia_solicitante=None, 
		jefe_dependencia_solicitante=None, responsable_solicitud=None, 
		email_responsable_solicitud=None, telef_responsable_solicitud=None, 
		categoria_servicio=None, tipo_servicio=None, nombre_servicio=None, 
		proposito_servicio=None, proposito_descripcion=None, 
		extension_cliente_final=None, descripcion_servicio=None, 
		dependencia_ejecutora=None, jefe_dependencia_ejecutora=None, 
		observaciones=None, elaborada_por=None,fecha_elaboracion=None, 
		aprobada_por=None, email_aprueba=None,fecha_aprobacion=None, 
		lugar_ejecucion_servicio=None, estado_solicitud=None):

		self.id = id
		self.registro = registro
		self.dependencia_solicitante = dependencia_solicitante
		self.jefe_dependencia_solicitante = jefe_dependencia_solicitante
		self.responsable_solicitud = responsable_solicitud
		self.email_responsable_solicitud = email_responsable_solicitud
		self.telef_responsable_solicitud = telef_responsable_solicitud
		self.categoria_servicio = categoria_servicio
		self.tipo_servicio = tipo_servicio
		self.nombre_servicio = nombre_servicio
		self.proposito_servicio = proposito_servicio
		self.proposito_descripcion = proposito_descripcion
		self.descripcion_servicio = descripcion_servicio
		self.dependencia_ejecutora = dependencia_ejecutora
		self.jefe_dependencia_ejecutora = jefe_dependencia_ejecutora
		self.observaciones = observaciones
		self.elaborada_por = elaborada_por
		self.fecha_elaboracion = fecha_elaboracion
		self.aprobada_por = aprobada_por
		self.email_aprueba = email_aprueba
		self.fecha_aprobacion = fecha_aprobacion
		self.lugar_ejecucion_servicio = lugar_ejecucion_servicio
		self.estado_solicitud = estado_solicitud
		self.db = db
		
	def __str__(self):

		return self.registro 

	def insertar(self):
		
		insercion = self.db.solicitudes.insert(registro = self.registro,
			dependencia = self.dependencia_solicitante, jefedependencia = self.jefe_dependencia_solicitante, 
			responsable = self.responsable_solicitud, emailresponsable = self.email_responsable_solicitud,
			telefonosresponsable = self.telef_responsable_solicitud, fechasolicitud = self.fecha_elaboracion, 
			servicio = self.categoria_servicio, proposito = self.proposito_servicio, 
			propositodescripcion = self.proposito_descripcion, propositoclientefinal = self.extension_cliente_final,
			descripcion = self.descripcion_servicio, observaciones = self.observaciones, 
			id_dependenciaejecutora = self.dependencia_ejecutora, lugarejecucion = self.lugar_ejecucion_servicio, 
			jefedependenciaejecutora = self.jefe_dependencia_ejecutora, pendiente = self.estado_solicitud, 
			emailaprueba = self.dependencia, fechaaprobacion = self.fecha_aprobacion)

		return insercion


	def instanciar(self, id):
		
		instanciacion = self.db(self.db.solicitudes.id == id).select(self.db.solicitudes.ALL)

		if (len(instanciacion) == 1):
			self.id = id
			self.registro = instanciacion[0].registro
			self.dependencia_solicitante = instanciacion[0].dependencia_solicitante
			self.jefe_dependencia_solicitante = instanciacion[0].jefe_dependencia_solicitante
			self.responsable_solicitud = instanciacion[0].responsable_solicitud
			self.email_responsable_solicitud = instanciacion[0].email_responsable_solicitud
			self.telef_responsable_solicitud = instanciacion[0].telef_responsable_solicitud
			self.categoria_servicio = instanciacion[0].categoria_servicio
			self.tipo_servicio = instanciacion[0].tipo_servicio
			self.nombre_servicio = instanciacion[0].nombre_servicio
			self.proposito_servicio = instanciacion[0].proposito_servicio
			self.proposito_descripcion = instanciacion[0].proposito_descripcion
			self.descripcion_servicio = instanciacion[0].descripcion_servicio
			self.dependencia_ejecutora = instanciacion[0].dependencia_ejecutora
			self.jefe_dependencia_ejecutora = instanciacion[0].jefe_dependencia_ejecutora
			self.observaciones = instanciacion[0].observaciones
			self.elaborada_por = instanciacion[0].elaborada_por
			self.fecha_elaboracion = instanciacion[0].fecha_elaboracion
			self.aprobada_por = instanciacion[0].aprobada_por
			self.email_aprueba = instanciacion[0].email_aprueba
			self.fecha_aprobacion = instanciacion[0].fecha_aprobacion
			self.lugar_ejecucion_servicio = instanciacion[0].lugar_ejecucion_servicio
			self.estado_solicitud = instanciacion[0].estado_solicitud

			return True
		
		else:

			return False

	def actualizar(self, id):
	    
	    actualizacion = self.db(self.db.solicitudes.id == id).update(
	    	
	    	registro = self.registro,
	    	dependencia_solicitante = self.dependencia_solicitante,
	    	jefe_dependencia_solicitante = self.jefe_dependencia_solicitante,
	    	responsable_solicitud = self.responsable_solicitud,
	    	email_responsable_solicitud = self.email_responsable_solicitud,
	    	telef_responsable_solicitud = self.telef_responsable_solicitud,
	    	categoria_servicio = self.categoria_servicio,
			tipo_servicio = self.tipo_servicio, 
			nombre_servicio = self.nombre_servicio,
			proposito_servicio = self.proposito_servicio, 
			proposito_descripcion = self.proposito_descripcion,
			descripcion_servicio = self.descripcion_servicio, 
			dependencia_ejecutora = self.dependencia_ejecutora, 
			jefe_dependencia_ejecutora = self.jefe_dependencia_ejecutora, 
			observaciones = self.observaciones, 
			fecha_elaboracion = self.fecha_elaboracion,
			email_aprueba = self.email_aprueba, 
			fecha_aprobacion = self.fecha_aprobacion, 
			lugar_ejecucion_servicio = self.lugar_ejecucion_servicio,
			estado_solicitud = self.estado_solicitud 
	    	)

	    return actualizacion