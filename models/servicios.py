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
	Field('responsable',		'reference personal',
		  requires=IS_IN_DB(db, db.personal.id, '%(nombre)s'), label=T('Encargado')),

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
