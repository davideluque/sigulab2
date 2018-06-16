##############################################################################
#                                                                            #
# Tablas del Modulo de Informacion Documentada                               #
#                                                                            #
##############################################################################

##############################################################################
#                                                                            #
# Tabla de los Registros                                                     #
#                                                                            #
##############################################################################

db.define_table(

    'registros',

    Field('codigo', 'string', label=T('Codigo del registro'),
          requires=IS_NOT_EMPTY()
          ),

    Field('fecha_creacion', 'string', label=T('Fecha')
          ),

    Field('descripcion', 'string', label=T('Descripcion del registro')
          ),

    Field('destinatario', 'string', label=T('Destinatario del registro')
          ),

    Field('remitente', 'string', label=T('Remitente del registro')
          ),

    Field('doc_electronico', 'string', label=T('Doc. Electrónico')
          ),

    Field('archivo_fisico', 'string', label=T('Archivo Fisico')
          ),

    primarykey=['descripcion']
)

##############################################################################
#                                                                            #
# Tabla de los Documentos                                                    #
#                                                                            #
##############################################################################

db.define_table(

    "documentos",

    Field('codigo', 'string', label=T('Codigo del registro'),
          requires=IS_NOT_EMPTY()
          ),

    Field('objetivo', 'string', label=T('Objetivo del documento')
          ),

    Field('ubicacion_fisica', 'string', label=T('Ubicacion fisica del Documento')
          ),

    Field('ubicacion_electronica', 'string',
          label=T('Ubicacion Electronica del Documento')),

    Field('cod_anexo', 'string', label=T('Codigo del anexo')),

    Field('nombre_anexo', 'string', label=T('Nombre del anexo del Documento'),
          unique=True),

    Field('responsable', 'string',
          label=T('Dependencia responsable del Documento'),
          requires=IS_IN_SET(['DIRECCIÓN','LABORATORIO A','LABORATORIO B', \
                    'LABORATORIO C','LABORATORIO D','LABORATORIO E',\
                    'LABORATORIO F','LABORATORIO G','UNIDAD DE ADMINISTRACIÓN',\
                    'COORDINACIÓN DE ADQUISICIONES','COORDINACIÓN DE IMPORTACIONES',\
                    'COORDINACIÓN DE LA CALIDAD','OFICINA DE PROTECCIÓN RADIOLÓGICA'
                    ])
          ),

    Field('nombre_doc', 'string', label=T('Nombre del Documento'), unique=True,
          notnull=True),

    Field('estatus', 'string', label=T('Estatus del Documento'),
          widget=SQLFORM.widgets.options.widget,
          requires=IS_IN_SET(['Planificado','Elaborado','Revisado','Aprobado'])
          ),

    Field('periodo_rev', 'string', label=T('Periodo de revision del Documento'),
          widget=SQLFORM.widgets.options.widget,
          requires=IS_IN_SET(['Mensual','Quincenal','Trimestral','Semestral',\
                             'Anual','Bienal','Trienal','Quinqueanual'])
          ),

    Field('aprobado_por', 'string', label=T('Nombre de quien aprobo el Documento')
          ),

    Field('elaborado_actualizado_por', 'string',
          label=T('Nombre de quien elaboro/actualizo el Documento')
          ),

    Field('vigencia', 'boolean', label=T('Vigencia del Documento')),

    Field('fecha_aprob', 'date', requires=IS_DATE(format=('%d-%m-%Y')),
          label=T('Fecha de aprobacion del Documento')),

    Field('fecha_prox_rev', 'date', requires=IS_DATE(format=('%d-%m-%Y')),
          label=T('Fecha de proxima revision del Documento')),

    Field('fecha_control_cambio', 'date', requires=IS_DATE(format=('%d-%m-%Y')),
          label=T('Fecha de registro de control de cambios en el Documento')
          ),

    Field('cod_control_cambio', 'string',
          label=T('Codigo de registro de control de cambios del Documento')
          ),

    Field('cod_aprob', 'string',
          label=T('Codigo de registro de aprobacion del Documento')),

    Field('fecha_rev_por_consejo_asesor', 'date',
          requires=IS_DATE(format=('%d-%m-%Y')),
          label=T('Fecha de revision por el Consejo Asesor')),

    Field('rev_por_consejo_asesor', 'string',
          label=T('Revision hecha por el Consejo Asesor')),

    Field('fecha_rev_especificaciones_doc', 'date',
          requires=IS_DATE(format=('%d-%m-%Y')),
          label=T('Fecha de revision de las especificaciones del Documento')),

    Field('rev_especficaciones_doc_realizado_por', 'string',
          label=T('Nombre de quien realizo la revision de las especificaciones')
          ),

    Field('fecha_rev_contenido', 'date',
          requires=IS_DATE(format=('%d-%m-%Y')),
          label=T('Fecha de revision del contenido del Documento')
          ),

    Field('rev_contenido_realizado_por', 'string',
          label=T('Nombre de quien reviso el contenido del Documento')),

    Field('tipo_doc', 'string', label=T('Tipo del Documento'),
          widget=SQLFORM.widgets.options.widget,
          requires=IS_IN_SET(['Referente Estrategico','Reglamento','Manual','Otro'])
          ),

    Field('procedimientos', 'string',
          label=T('Procedimientos del Manual')),

    Field('formularios', 'string',
          label=T('Formularios del Manual')),

    Field('instructivos', 'string',
          label=T('Instructivos del Manual')),

    Field('registro', 'string', unique=True,
          label=T('Identificador del registo del manual')),

    Field('tipo_manual', 'string', label=T('Tipo del manual')),

    primarykey=['codigo']
)