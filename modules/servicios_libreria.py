# -*- coding: utf-8 -*-
import random

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
	    
	    actualizacion = self.db(self.db.servicios.id == id).update(
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
		
		#### Captura de datos desde la Base de Datos

		self.db = db
		
		# 1. Tomar todos los servicios de la Base de Datos
		self.set = self.db(self.db.servicios.id > 0)

		# Aqui se introducen los servicios instanciados
		self.filas = []
		
		# 2. Instanciar todos los servicios como objetos de la clase Servicio
		self.capturar_objetos()

		# Numero de servicios recuperados desde la base de datos
		self.cuenta = self.set.count()

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


#------------------------------------------------------------------------------
#
# Solicitud y Listado de Solicitudes
#
#------------------------------------------------------------------------------

class Solicitud(object):

	def __init__(self, db, auth, registro = None, id_responsable_solicitud = None,
		fecha_solicitud = None, id_servicio_solicitud = None,  id_proposito_servicio = None,
		proposito_descripcion = None, proposito_cliente_final = None, descripcion_servicio = None,
		observaciones = None, estado_solicitud = None):

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
		
		# Variables disponibles despues de aprobacion
		self.aprobada_por = None
		self.fecha_aprobacion = None

		# Variables disponibles despues de ejecucion
		self.fecha_elaboracion = None
		self.elaborada_por = None

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
			self.aprobada_por = instanciacion[0].aprobada_por
			self.fecha_aprobacion = instanciacion[0].fecha_aprobacion
			self.elaborada_por = instanciacion[0].elaborada_por
			self.fecha_elaboracion = instanciacion[0].fecha_elaboracion

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

	def conseguir_atributos(self):
		


		# Extensiones telefonicas del responsable de la solicitud
		personal = self.db(self.id_responsable_solicitud == self.db.t_Personal.id).select(self.db.t_Personal.ALL)[0]
		self.telef_responsable_solicitud = personal.f_telefono

		responsable_usuario = self.db(personal.f_usuario == self.db.auth_user.id).select(self.db.auth_user.ALL)[0]

		# Correo electronico del responsable de la solicitud
		self.email_responsable_solicitud = responsable_usuario.email

		dependencia = self.db(personal.f_dependencia == self.db.dependencias.id).select(self.db.dependencias.ALL)[0]

		self.id_dependencia_solicitante = dependencia.id

		# Dependencia solicitante		
		self.nombre_dependencia_solicitante = dependencia.nombre

		# Jefe Dependencia Solicitante
		usuario_jefe_dependencia_solicitante = self.db(dependencia.id_jefe_dependencia == self.db.auth_user.id).select(self.db.auth_user.ALL)[0]

		self.nombre_jefe_dependencia_solicitante = usuario_jefe_dependencia_solicitante.first_name + " " + usuario_jefe_dependencia_solicitante.last_name

		self.id_dependencia_ejecutora = self.db(self.id_servicio_solicitud == self.db.servicios.id).select(self.db.servicios.ALL)[0].dependencia

		dependencia_ejecutora_servicio = self.db(self.id_dependencia_ejecutora == self.db.dependencias.id).select(self.db.dependencias.ALL)[0]

		# Dependencia Ejecutora del Servicio
		self.nombre_dependencia_ejecutora = dependencia_ejecutora_servicio.nombre

		# Jefe de la Dependencia Ejecutora del Servicio
		usuario_jefe_dependencia_ejecutora = self.db(dependencia_ejecutora_servicio.id_jefe_dependencia == self.db.auth_user.id).select(self.db.auth_user.ALL)[0]	
		
		self.jefe_dependencia_ejecutora = usuario_jefe_dependencia_ejecutora.first_name + " " + usuario_jefe_dependencia_ejecutora.last_name
		
		# Lugar de Ejecucion de Servicio

		id_ubicacion_ejecucion = self.db(self.id_servicio_solicitud == self.db.servicios.id).select(self.db.servicios.ALL)[0].ubicacion

		self.lugar_ejecucion_servicio = self.db(id_ubicacion_ejecucion == self.db.espacios_fisicos.id).select(self.db.espacios_fisicos.ALL)[0].direccion

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
			self.elaborada_por = self.auth.user.first_name + " " + self.auth.user.last_name

		elif estado == 1:
			# Fecha de elaboracion del servicio
			self.fecha_aprobacion = request.now
			# Persona responsable de la solicitud y Elaborado por
			self.aprobada_por = self.auth.user.first_name + " " + self.auth.user.last_name

		self.estado_solicitud_str = self.estado_string()

	def estado_string(self):

		if self.estado_solicitud == -1:
			return "Negada"
		elif self.estado_solicitud == 0:
			return "Pendiente por Ejecución"
		elif self.estado_solicitud == 1:
			return "En ejecución"
		elif self.estado_solicitud == 2:
			return "Pendiente por Certificación"

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

			if (self.tipo_listado == "Solicitante" and solicitud.id_dependencia_solicitante == self.dependencia_usuario):
				self.filas.append(solicitud)
			elif (self.tipo_listado == "Ejecutante" and solicitud.id_dependencia_ejecutora == self.dependencia_usuario):
				self.filas.append(solicitud)

	def orden_y_filtrado(self):
		self.filas.sort(key=lambda serv: getattr(serv, self.columna), reverse=self.orden)
		self.solicitudes_a_mostrar = self.filas[(self.pagina_central - 1)*10:self.ultimo_elemento]

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
    ubicrow = db(entrada[0].ubicacion == db.espacios_fisicos.id).select(db.espacios_fisicos.ALL)
    ubicacion = ubicrow[0].nombre
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
# Clase certificacion de servicio
#
#------------------------------------------------------------------------------

class Certificacion(object):


	def __init__(self, db, registro=None, proyecto=None, elaborado_por=None,
				 dependencia=None, solicitud=None, fecha_certificacion=None, id=None):

		self.registro = registro
		self.proyecto = proyecto
		self.elaborado_por = elaborado_por
		self.dependencia = dependencia
		self.solicitud = solicitud
		self.fecha_certificacion = fecha_certificacion

		self.db = db
		# viene de la instanciacion
		self.id = id

	def __str__(self):

		return self.registro + " " + self.proyecto

	def insertar(self):

		insercion = self.db.certificaciones.insert(registro=self.registro,
											 proyecto=self.proyecto,
											 elaborado_por=self.elaborado_por,
											 dependencia=self.dependencia,
											 solicitud=self.solicitud,
											 fecha_certificacion=self.fecha_certificacion)

		return insercion

	def instanciar(self, id):

		instanciacion = self.db(self.db.certificaciones.id == id).select(self.db.certificaciones.ALL)

		if (len(instanciacion) == 1):
			self.id = id
			self.registro = instanciacion.registro
			self.proyecto = instanciacion.proyecto
			self.elaborado_por = instanciacion.elaborado_por
			self.dependencia = instanciacion.servicio
			self.solicitud = instanciacion.solicitud
			self.fecha_certificacion = instanciacion.fecha_certificacion

			return True

		else:
			return False

	def editar(self, registro, proyecto, elaborado_por,
				 dependencia, solicitud, fecha_certificacion):

		self.registro = registro
		self.proyecto = proyecto
		self.elaborado_por = elaborado_por
		self.dependencia = dependencia
		self.solicitud = solicitud
		self.fecha_certificacion = fecha_certificacion

	def actualizar(self, id):

		actualizacion = self.db(self.db.certificaciones.id == id).update(
			registro=self.registro,
			proyecto=self.proyecto,
			elaborado_por=self.elaborado_por,
			dependencia=self.dependencia,
			solicitud=self.solicitud,
			fecha_certificacion=self.fecha_certificacion)

		return actualizacion

# Funcion que genera numeros arbitrarios para el registro de certificaciones y solicitudes

def generador_num_registro():
    min = 0
    max = 500
    digit = str(random.randint(min, max))
    digits = (len(str(max))-len(digit))*'0' + digit

    return digits

def validador_registro_solicitudes(request, db):
	anio = str(request.now)[2:4]
	registro = 'UL-' + anio + '/' + generador_num_registro()

	check = db(db.solicitudes.registro == registro).count()

	if check != 0:
		return validador_registro_solicitudes(request, db)
	else:
		return registro

def validador_registro_certificaciones(request, db):
	anio = str(request.now)[2:4]
	registro = 'UL-' + anio + '/' + generador_num_registro()

	check = db(db.certificaciones.registro == registro).count()

	if check != 0:
		return validador_registro_certificaciones(request, db)
	else:
		return registro