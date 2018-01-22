##############################################################################
# Tablas de Servicios, involucran cada uno de las entidades que manejan la 
# creacion y edicion de las fichas de servicio
#
##############################################################################


##############################################################################
#                     TABLA: TIPOS DE SERVICIOS
#
# Tabla que engloba todos los tipos posibles de servicios 
#
##############################################################################
db.define_table(
    'tipos_servicios',
    Field('nombre', 'string', unique=True, notnull=True, label=T('Nombre')),
)

db.tipos_servicios._plural = 'Tipos'
db.tipos_servicios._singular = 'Tipo'

##############################################################################
#                     TABLA: CATEGORIAS DE SERVICIOS
#
#
##############################################################################

db.define_table(
    'categorias_servicios',
    Field('nombre', 'string', unique=True, notnull=True, label=T('Nombre')),
)

db.categorias_servicios._plural = 'Categorías',
db.categorias_servicios._singular = 'Categoría'

##############################################################################
#                         TABLA: SERVICIOS
#
#
##############################################################################

db.define_table(
    'servicios',
    # Atributos; Datos puntuales, Nombre, Objetivo, etc
    Field('nombre',             'string', notnull=True, label=T('Nombre')),
    Field('objetivo',           'string', notnull=True, label=T('Objetivo')),
    Field('alcance',            'string', notnull=True, label=T('Alcance')),
    Field('metodo',             'string', notnull=True, label=T('Método')),
    Field('rango',              'string', label=T('Rango')),
    Field('incertidumbre',      'string', label=T('Incertidumbre')),
    Field('item_ensayar',       'string', notnull=True, label=T('Item a Ensayar')),
    Field('requisitos',         'text', notnull=True, label=T('Requisitos')),
   
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
          requires=IS_IN_DB(db, db.t_Personal.id, '%(f_nombre)s'), 
          label=T('Encargado')),

    # Dependencia
    Field('dependencia',        'reference dependencias',
          requires=IS_IN_DB(db, db.dependencias.id, '%(nombre)s'), 
          label=T('Dependencias')),

    # Ubicacion Fisica
    Field('ubicacion',          'reference espacios_fisicos',
          requires=IS_IN_DB(db, db.espacios_fisicos.id, '%(codigo)s'), 
          label=T('Ubicación Física')),
    
    # Checklist de Producto. Este campo anteriormente se llamaba Resultado
    # y era un campo de texto largo.
    Field('entregaResultados', 'boolean', default=False, 
        label=T('Entrega de Resultados')),
    Field('ensayoCalibracion', 'boolean', default=False, 
        label=T('Informe de ensayo o calibración')),
    Field('certificadoConformidadProducto', 'boolean', default=False, 
        label=T('Certificado de conformidad del producto (ensayado o calibrado)')),
    Field('certificadoCalibracion', 'boolean', default=False,
        label=T('Certificado de calibración')),
    Field('otro','boolean', default=False, label=T('Otro')),

    # Ámbito de aplicación de un servicio. Checklist.
    Field('ambito_in_situ', 'boolean', default=False, label=T('Ámbito: In Situ')),
    Field('ambito_en_campo', 'boolean', default=False, label=T('Ámbito: En Campo')),
    Field('ambito_otro', 'boolean', default=False, label=T('Ámbito: Otro')),
    Field('ambito_otro_detalle', 'string', label=T('Ámbito es otro, especifique:')),

    # Personal que presta el Servicio
    Field('per_tecnico', 'boolean', default=False, label=T('Técnico')),
    Field('cant_per_tecnico', 'boolean', default=False, label=T('Cantidad Técnico')),
    Field('per_supervisor', 'boolean', default=False, label=T('Supervisor')),
    Field('cant_per_supervisor', 'boolean', default=False, label=T('Cantidad Supervisor')),
    Field('per_tesista', 'boolean', default=False, label=T('Tesista')),
    Field('cant_per_tesista', 'boolean', default=False, label=T('Cantidad Tesista')),
    Field('per_pasante', 'boolean', default=False, label=T('Pasante')),
    Field('cant_per_pasante', 'boolean', default=False, label=T('Cantidad Pasante')),
    Field('per_preparador', 'boolean', label=T('Preparador')),
    Field('cant_per_preparador', 'boolean', label=T('Cantidad Preparador')),
    Field('per_obrero', 'boolean', default=False, label=T('Obrero')),
    Field('cant_per_obrero', 'boolean', default=False, label=T('Cantidad Obrero')),
    Field('per_otro', 'boolean', default=False, label=T('Otro')),
    Field('per_otro_detalle', 'string', label=T('Otro, especifique')),

    # Equipo que presta el Servicio
    Field('equipo_presta_servicio', 'string', notnull=True, label=T('Equipo Presta Servicio')),

    # Espacio Fisico donde se desarrolla el servicio
    Field('esp_fis_servicio', 'reference espacios_fisicos', requires=IS_IN_DB(db, db.espacios_fisicos.id, '%(codigo)s'), 
          label=T('Espacio Físico')),

    # Insumos (requerimientos del servicio)
    Field('insumos_servicio', 'string', notnull=True, label=T('Insumos del Servicio')),

    # Ambiente para la ejecucion del servicio
    Field('condicion_ambiental', 'boolean', default=False, label=T('Requiere?')),
    Field('condicion_ambiental_detalle', 'string', label=T('Si requiere, especifique:'))

)

db.servicios._plural = 'Servicios'
db.servicios._singular = 'Servicio'

#############################################################################
#                          TABLA: PROPOSITOS
#
#
#
##############################################################################

db.define_table(
    'propositos',
    Field('tipo', 'string', requires=IS_NOT_EMPTY())
)

#############################################################################
#                   TABLA: SOLICITUDES DE SERVICIOS
#
# Esta tabla es el primer lugar en donde se encuentra un servicio al 
# llenarse el formulario de solicitudes de servicios.
#
##############################################################################

db.define_table(
    'solicitudes',  

    Field('registro', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Número de Registro')),

    Field('responsable', 'reference t_Personal', 
        requires=IS_IN_DB(db, db.t_Personal.id, '%(f_nombre)s | %(f_email)s'), 
        label=T('Responsable de la Solicitud')),

    Field('fecha',   'date',
          requires=IS_DATE(format=('%d-%m-%Y')), 
          default=request.now, notnull=True, label=T('Fecha de Solicitud')),

    Field('id_servicio_solicitud', 'reference servicios', 
        requires=IS_IN_DB(db, db.servicios.id, '%(nombre)s'), 
        label=T('Servicio Solicitado')),

    Field('proposito', 'reference propositos', 
        requires=IS_IN_DB(db, db.propositos.id, '%(tipo)s'), 
        label=T('Propósito del servicio solicitado')),

    Field('proposito_descripcion', 'string', 
        requires=IS_NOT_EMPTY(), label=T('Descripción del propósito')),

    # Si el propósito es extensión, este campo se llena con el cliente final.
    Field('proposito_cliente_final', 'string', label=T('Cliente final del propósito')),

    Field('descripcion', 'string', label=T('Descripción de la Solicitud')),
    
    Field('observaciones', 'string', label=T('Observaciones de la Solicitud')),

    # Estado = -1 :Denegado
    # Estado = 0  :Por aprobación
    # Estado = 1  :pendiente por ejecutar
    # Estado = 2  :pendiente por certificar
    # Estado = 3  :certificado

    Field('estado','integer', default=0, label=T('Estado de Solicitud')),

    Field('aprobada_por', 'string', label=T('Solicitud Aprobada Por')),

    Field('fecha_aprobacion',   'date',  label=T('Fecha de Aprobacion de Solicitud')),

    Field('elaborada_por', 'string', label=T('Solicitud Elaborada Por')),

    Field('fecha_elaboracion',   'date', label=T('Fecha de Elaboracion de Solicitud')),

)

##############################################################################
#                     TABLA: HISTORIAL DE SERVICIOS
#
# Tabla de servicios solicitados ya ejecutados y certificados. 
# Tabla final para una solicitud de servicio (Solicitud estado 3).
#
##############################################################################

db.define_table(
    "historial_solicitudes",

    Field('registro_solicitud', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Número de Registro de la Solicitud')),

    Field('nombre_servicio', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Nombre del Servicio')),

    Field('tipo_servicio', 'string', requires=IS_NOT_EMPTY(),
        label=T('Tipo del Servicio')),

    Field('categoria_servicio', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Categoría del Servicio')),

   Field('proposito_solicitud', 'string', requires=IS_NOT_EMPTY(), 
    label=T('Propósito del Servicio Solicitado')),

    Field('proposito_solicitud_descripcion', 'string', 
        requires=IS_NOT_EMPTY(), 
        label=T('Descripción del Propósito del Servicio Solicitado')),

    Field('descripcion_solicitud', 'string', 
        label=T('Descripción de la Solicitud')),

    Field('observaciones_solicitud', 'string', 
        label=T('Observaciones de la Solicitud')),

    Field('responsable_solicitud', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Responsable de la Solicitud')),

    Field('ci_responsable_solicitud', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Cédula del Responsable de la Solicitud')),

    Field('email_responsable_solicitud', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Correo del Responsable de la Solicitud')),

    Field('telefono_responsable_solicitud', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Teléfono del Responsable de la Solicitud')),

    Field('cargo_responsable_solicitud', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Cargo del Responsable de la Solicitud')),

    Field('nombre_dependencia_solicitante', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Nombre de la Dependencia Solicitante')),

    Field('nombre_jefe_dependencia_solicitante', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Nombre del Jefe de la Dependencia Solicitante')),

    Field('adscripcion_dependencia_solicitante', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Unidad de Adscripción de la Dependencia Solicitante')),

    Field('fecha_solicitud', 'date', 
        requires=IS_DATE(format=('%d-%m-%Y')), 
        label=T('Fecha de Solicitud')),

    Field('nombre_dependencia_ejecutora', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Nombre de la Dependencia Ejecutora')),

    Field('nombre_jefe_dependencia_ejecutora', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Nombre del Jefe de la Dependencia Ejecutora')),

    Field('adscripcion_dependencia_ejecutora', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Unidad de Adscripción de la Dependencia Ejecutora')),

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

    Field('fecha_certificacion', 'date', requires=IS_DATE(format=('%d-%m-%Y')), 
        label=T('Fecha de Certificación de la Solicitud')),

    Field('numero_de_proyecto', 'string', requires=IS_NOT_EMPTY(), 
        label=T('Número de Proyecto'))
)
