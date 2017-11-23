#######################################################################################################################
#
# Tablas de Servicios, involucran cada uno de las entidades que manejan la creacion y edicion de las fichas de servicio
#
#######################################################################################################################

# tipos_servicios: Tabla que engloba todos los tipos posibles de servicios
db.define_table(
	'tipos_servicios',
	Field('nombre',	'string', unique=True, notnull=True, label=T('Nombre')),
)

db.tipos_servicios._plural = 'Tipos'
db.tipos_servicios._singular = 'Tipo'

# categorias_servicios: Tabla que engloba todas las categorias posibles de servicios
db.define_table(
	'categorias_servicios',
	Field('nombre',	'string', unique=True, notnull=True, label=T('Nombre')),
)

db.categorias_servicios._plural = 'Categorías'
db.categorias_servicios._singular = 'Categoría'

# servicios: Catalogo de todos los Servicios agregados al sistema.
db.define_table(
	'servicios', # Nombre de la entidad
	# Atributos; Datos puntuales, Nombre, Objetivo, etc
	Field('nombre', 			'string', notnull=True, label=T('Nombre')),
	Field('objetivo', 			'string', notnull=True, label=T('Objetivo')),
	Field('alcance', 			'string', notnull=True, label=T('Alcance')),
	Field('metodo', 			'string', notnull=True, label=T('Método')),
	Field('rango', 				'string', label=T('Rango')),
	Field('incertidumbre', 		'string', label=T('Incertidumbre')),
	Field('item_ensayar', 		'string', notnull=True, label=T('Item a Ensayar')),
	Field('requisitos', 		'text', notnull=True, label=T('Requisitos')),
	Field('resultados', 		'text', notnull=True, label=T('Resultados')),

	# Fecha de Agregacion.
	Field('fecha_de_agregacion', 'datetime', requires=IS_DATETIME(), default=request.now),

	# Tipo y Categoria
	Field('tipo', 				'reference tipos_servicios',
		  requires=IS_IN_DB(db, db.tipos_servicios, '%(nombre)s'), label=T('Tipo')),

	Field('categoria',			'reference categorias_servicios',
		  requires=IS_IN_DB(db, db.categorias_servicios, '%(nombre)s'), label=T('Categoría')),

	# Funciones
	Field('docencia',			'boolean', default=False, label=T('Docencia')),
	Field('investigacion',		'boolean', default=False, label=T('Investigación')),
	Field('gestion',			'boolean', default=False, label=T('Gestión')),
	Field('extension',			'boolean', default=False, label=T('Extensión')),

	Field('visibilidad',		'boolean', default=True, label=T('Visible')),

	# Prof Encargado
	Field('responsable',		'reference t_Personal',
		  requires=IS_IN_DB(db, db.t_Personal.id, '%(nombre)s'), label=T('Encargado')),

	# Dependencia
	Field('dependencia',		'reference dependencias',
		  requires=IS_IN_DB(db, db.dependencias.id, '%(nombre)s'), label=T('Dependencias')),

	# Ubicacion Fisica
	Field('ubicacion',			'reference espacios_fisicos',
		  requires=IS_IN_DB(db, db.espacios_fisicos.id, '%(nombre)s'), label=T('Ubicación Física')),
)

db.servicios._plural = 'Servicios'
db.servicios._singular = 'Servicio'

##################################################################################################
#															TABLA: SOLICITUDES DE SERVICIOS
#
#	Esta tabla es el primer lugar en donde se encuentra un servicio al llenarse el formulario de
# solicitudes de servicios.
#
#################################################################################################

db.define_table(
	'propositos',
	Field('tipo', 'string', requires=IS_NOT_EMPTY())
)

db.define_table(
	'solicitudes',	

	Field('registro', 'string', requires=IS_NOT_EMPTY(), label=T('Número de Registro')),
	
	Field('dependencia', 'reference dependencias', requires=IS_IN_DB(db, 'dependencias.id', '%(nombre)s'), label=T('Dependencia Solicitante')),

	Field('jefe_pendencia', 'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(nombre)s | %(email)s'), label=T('Jefe de la Dependencia Solicitante')),

	Field('responsable', 'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(nombre)s | %(email)s'), label=T('Responsable de la Solicitud')),

	# TODO: Conectar el email con el responsable
	#
	# ###########################################
	Field('email_responsable', 'string', label=T('Email del Responsable de la Solicitud')),

	Field('telefonos_responsable', 'list:string', label=T('Extensiones')),

	Field('fecha',   'date', 
		  requires=IS_DATE(format=('%d-%m-%Y')), default=request.now, notnull=True, label=T('Fecha de Solicitud')),


	Field('id_servicio_solicitud', 'reference servicios', requires=IS_IN_DB(db, db.servicios.id, '%(nombre)s'), label=T('Servicio Solicitado')),

	Field('proposito', 'reference propositos', requires=IS_IN_DB(db, db.propositos.id, '%(tipo)s'), label=T('Propósito del servicio solicitado')),

	Field('proposito_descripcion', 'string', requires=IS_NOT_EMPTY(), label=T('Descripción del propósito')),

	# Si el propósito es extensión, este campo se llena con el cliente final.
	Field('proposito_cliente_final', 'string', label=T('Cliente final del propósito')),
	
	Field('descripcion', 'string', label=T('Descripción de la Solicitud')),
	
	Field('observaciones', 'string', label=T('Observaciones de la Solicitud')),

	Field('id_dependencia_ejecutora_solicitud', 'reference dependencias', requires=IS_IN_DB(db, db.dependencias.id, '%(nombre)s'), label=T('Dependencia Ejecutora')),

	# TO DO: Conectar el espacio físico con la dependencia
	#
	#######################################################
	Field('lugar_ejecucion', 'reference espacios_fisicos', requires=IS_IN_DB(db, db.espacios_fisicos.id, '%(nombre)s'), label=T('Lugar de Ejecución de Servicio')),
	
	Field('jefede_pendencia_ejecutora', 'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(nombre)s | %(email)s'), label=T('Jefe de la Dependencia Ejecutora')),
	
	# TO DO: Conectar este correo con las validaciones de solicitudes
	#
	# Esto en vez de el email quizá pueda tener el id de la persona que aprobo la solicitud
	#
	# Otra cosa: esta tabla sería entonces una tabla de servicios solicitados "pendientes"
	#######################################################################################
	#Field('pendiente',		'boolean', default=True, label=T('Pendiente')),

	# estado=0 pendiente por aprobar
	# estado=1 pendiente por ejecutar

	Field('estado','string', default='0', label=T('Pendiente por aprobar')),


	Field('email_aprueba', 'string', label=T('Solicitud Aprobada Por')),

	Field('fecha_aprobacion',   'date', 
		  requires=IS_DATE(format=('%d-%m-%Y')), default = request.now, notnull=True, label=T('Fecha de Aprobacion de Solicitud')),

)


##################################################################################################
#															TABLA: CERTIFICACIONES DE SERVICIOS
#
#	Esta tabla en donde se encuentra una solicitud al llenarse el formulario de
# certificaciones de servicios.
#
#################################################################################################

