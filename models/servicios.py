#######################################################################################################################
#
# Tablas de Servicios, involucran cada uno de las entidades que manejan la creacion y edicion de las fichas de servicio
#
#######################################################################################################################

# tipos_servicios: Tabla que engloba todos los tipos posibles de servicios
db.define_table(
    'tipos_servicios',
    Field('nombre', 'string', unique=True, notnull=True, label=T('Nombre')),
)

db.tipos_servicios._plural = 'Tipos'
db.tipos_servicios._singular = 'Tipo'

# categorias_servicios: Tabla que engloba todas las categorias posibles de servicios
db.define_table(
    'categorias_servicios',
    Field('nombre', 'string', unique=True, notnull=True, label=T('Nombre')),
)

db.categorias_servicios._plural = 'Categorías',
db.categorias_servicios._singular = 'Categoría'

# servicios: Catalogo de todos los Servicios agregados al sistema.
db.define_table(
    'servicios', # Nombre de la entidad
    # Atributos; Datos puntuales, Nombre, Objetivo, etc
    Field('nombre',             'string', notnull=True, label=T('Nombre')),
    Field('objetivo',           'string', notnull=True, label=T('Objetivo')),
    Field('alcance',            'string', notnull=True, label=T('Alcance')),
    Field('metodo',             'string', notnull=True, label=T('Método')),
    Field('rango',              'string', label=T('Rango')),
    Field('incertidumbre',      'string', label=T('Incertidumbre')),
    Field('item_ensayar',       'string', notnull=True, label=T('Item a Ensayar')),
    Field('requisitos',         'text', notnull=True, label=T('Requisitos')),
    Field('resultados',         'text', notnull=True, label=T('Resultados')),

    # Fecha de Agregacion.
    Field('fecha_de_agregacion', 'datetime', requires=IS_DATETIME(), default=request.now),

    # Tipo y Categoria
    Field('tipo',               'reference tipos_servicios',
          requires=IS_IN_DB(db, db.tipos_servicios, '%(nombre)s'), label=T('Tipo')),

    Field('categoria',          'reference categorias_servicios',
          requires=IS_IN_DB(db, db.categorias_servicios, '%(nombre)s'), label=T('Categoría')),

    # Funciones
    Field('docencia',           'boolean', default=False, label=T('Docencia')),
    Field('investigacion',      'boolean', default=False, label=T('Investigación')),
    Field('gestion',            'boolean', default=False, label=T('Gestión')),
    Field('extension',          'boolean', default=False, label=T('Extensión')),

    Field('visibilidad',        'boolean', default=True, label=T('Visible')),

    # Prof Encargado
    Field('responsable',        'reference t_Personal',
          requires=IS_IN_DB(db, db.t_Personal.id, '%(f_nombre)s'), label=T('Encargado')),

    # Dependencia
    Field('dependencia',        'reference dependencias',
          requires=IS_IN_DB(db, db.dependencias.id, '%(nombre)s'), label=T('Dependencias')),

    # Ubicacion Fisica
    Field('ubicacion',          'reference espacios_fisicos',
          requires=IS_IN_DB(db, db.espacios_fisicos.id, '%(nombre)s'), label=T('Ubicación Física')),
)

db.servicios._plural = 'Servicios'
db.servicios._singular = 'Servicio'

##################################################################################################
#                                                           TABLA: SOLICITUDES DE SERVICIOS
#
#   Esta tabla es el primer lugar en donde se encuentra un servicio al llenarse el formulario de
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
    
    #Field('dependencia', 'reference dependencias', requires=IS_IN_DB(db, 'dependencias.id', '%(nombre)s'), label=T('Dependencia Solicitante')),

    #Field('jefe_dependencia', 'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_nombre)s | %(f_email)s'), label=T('Jefe de la Dependencia Solicitante')),

    Field('responsable', 'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_nombre)s | %(f_email)s'), label=T('Responsable de la Solicitud')),

    Field('fecha',   'date',
          requires=IS_DATE(format=('%d-%m-%Y')), default=request.now, notnull=True, label=T('Fecha de Solicitud')),

    Field('id_servicio_solicitud', 'reference servicios', requires=IS_IN_DB(db, db.servicios.id, '%(nombre)s'), label=T('Servicio Solicitado')),

    Field('proposito', 'reference propositos', requires=IS_IN_DB(db, db.propositos.id, '%(tipo)s'), label=T('Propósito del servicio solicitado')),

    Field('proposito_descripcion', 'string', requires=IS_NOT_EMPTY(), label=T('Descripción del propósito')),

    # Si el propósito es extensión, este campo se llena con el cliente final.
    Field('proposito_cliente_final', 'string', label=T('Cliente final del propósito')),
    
    Field('descripcion', 'string', label=T('Descripción de la Solicitud')),
    
    Field('observaciones', 'string', label=T('Observaciones de la Solicitud')),

    #Field('id_dependencia_ejecutora', 'reference dependencias', requires=IS_IN_DB(db, db.dependencias.id, '%(nombre)s'), label=T('Dependencia Ejecutora')),

    
    #
    #######################################################
    #Field('lugar_ejecucion', 'reference espacios_fisicos', requires=IS_IN_DB(db, db.espacios_fisicos.id, '%(nombre)s'), label=T('Lugar de Ejecución de Servicio')),

    #Field('jefe_dependencia_ejecutora', 'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_nombre)s | %(f_email)s'), label=T('Jefe de la Dependencia Ejecutora')),


    #
    # Esto en vez de el email quizá pueda tener el id de la persona que aprobo la solicitud
    #
    # Otra cosa: esta tabla sería entonces una tabla de servicios solicitados "pendientes"
    #######################################################################################
    #Field('pendiente',     'boolean', default=True, label=T('Pendiente')),

    # estado=-1 rechazado
    # estado=0 pendiente por aprobar
    # estado=1 pendiente por ejecutar
    # estado=2 pendiente por certificar
    # estado=3 certificado

    Field('estado','integer', default=0, label=T('Estado de Solicitud')),

    Field('aprobada_por', 'string', label=T('Solicitud Aprobada Por')),

    Field('fecha_aprobacion',   'date',  label=T('Fecha de Aprobacion de Solicitud')),

    Field('elaborada_por', 'string', label=T('Solicitud Elaborada Por')),

    Field('fecha_elaboracion',   'date', label=T('Fecha de Elaboracion de Solicitud')),

)


##################################################################################################
#                                                           TABLA: CERTIFICACIONES DE SERVICIOS
#
#   Esta tabla en donde se encuentra una solicitud al llenarse el formulario de
# certificaciones de servicios.
#
#################################################################################################

db.define_table(
    'certificaciones',

    Field('registro', 'string', requires=IS_NOT_EMPTY(), label=T('Número de Registro')),
    Field('proyecto', 'string', requires=IS_NOT_EMPTY(), label=T('Número de Poyecto')),
    Field('elaborado_por', 'reference t_Personal',
          requires=IS_IN_DB(db, db.t_Personal.id, '%(f_nombre)s | %(f_email)s'), label=T('Elaborado Por')),
    Field('servicio', 'reference servicios',
          requires=IS_IN_DB(db, db.servicios.id, '%(nombre)s'), label=T('Servicio Solicitado')),
    Field('solicitud', 'reference solicitudes',
          requires=IS_IN_DB(db, db.solicitudes.id, '%(registro))s'), label=T('Solicitud a Certificar')),
    Field('fecha_certificacion',   'date',
          requires=IS_DATE(format=('%d-%m-%Y')), default = request.now, notnull=True, label=T('Fecha de Certificacion de Solicitud')),
)

##############################################################################
#                     TABLA: HISTORIAL DE SERVICIOS
#
# Tabla de servicios solicitados ya ejecutados y certificados. 
# Tabla final para una solicitud de servicio (Solicitud estado 3). 
# Combinacion de las tablas de certificacion y solicitud.
#
##############################################################################

db.define_table(
    "historial_solicitudes",

    Field('registro_solicitud', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Número de Registro de la Solicitud')),

    Field('nombre_servicio', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Nombre del Servicio'))

    Field('tipo_servicio', 'string', requires=IS_NOT_EMPTY(),
        label=T('Tipo del Servicio')),

    Field('categoria_servicio', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Categoría del Servicio')),

   Field('proposito_solicitud', 'string', requires=IS_NOT_EMPTY(), 
    label=T('Propósito del Servicio Solicitado')),

    Field('proposito_solicitud_descripcion', 'string', requires=IS_NOT_EMPTY(), label=T('Descripción del Propósito del Servicio Solicitado')),

    Field('descripcion_solicitud', 'string', 
        label=T('Descripción de la Solicitud')),

    Field('observaciones_solicitud', 'string', 
        label=T('Observaciones de la Solicitud')),

    Field('responsable_solicitud', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Responsable de la Solicitud')),

    Field('ci_responsable_solicitud', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Cédula del Responsable de la Solicitud')),

    Field('email_responsable_solicitud', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Cédula del Responsable de la Solicitud')),

    Field('telefono_responsable_solicitud', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Teléfono del Responsable de la Solicitud')),

    Field('nombre_dependencia_solicitante', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Nombre de la Dependencia Solicitante')),

    Field('nombre_jefe_dependencia_solicitante', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Nombre del Jefe de la Dependencia Solicitante')),

    Field('nombre_dependencia_ejecutora', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Nombre de la Dependencia Ejecutora')),

    Field('nombre_jefe_dependencia_ejecutora', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Nombre del Jefe de la Dependencia Ejecutora')),

    Field('lugar_ejecucion_servicio', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Lugar de Ejecución del Servicio')),

    Field('solicitud_aprobada_por', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Solicitud Aprobada Por')),

    Field('fecha_aprobacion_solicitud', 'date', 
        requires=IS_DATE(format=('%d-%m-%Y')), 
        label=T('Fecha de Aprobación de la Solicitud')),

    Field('fecha_elaboracion_solicitud', 'date', 
        requires=IS_DATE(format=('%d-%m-%Y')), 
        label=T('Fecha de Elaboración de la Solicitud')),

    Field('solicitud_elaborada_por', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Solicitud Elaborada por')),

    Field('fecha_certificacion', 'date', requires=IS_DATE(format=('%d-%m-%Y')), label=T('Fecha de Certificación de la Solicitud')),

    Field('numero_de_proyecto', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Número de Proyecto'))
)
