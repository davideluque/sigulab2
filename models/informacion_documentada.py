################################################################################
##                                                                            ##
##    Modelos del Módulo de Informacion Documentada                           ##
##                                                                            ##
################################################################################




###############################################################################
##                                                                           ##
##    Tabla de los Registros                                                 ##
##                                                                           ##
###############################################################################

db.define_table(

      'registros',

      Field('usuario', 'string', label=T('Usuario creador del registro')),

      Field('codigo', 'string', label=T('Codigo del registro'), requires=IS_NOT_EMPTY()),

      Field('fecha_creacion', 'string', label=T('Fecha')),

      Field('descripcion', 'string', label=T('Descripcion del registro')),

      Field('destinatario', 'string', label=T('Destinatario del registro')),

      Field('remitente', 'string', label=T('Remitente del registro')),

      Field('doc_electronico', 'string', label=T('Doc. Electrónico')),

      Field('archivo_fisico', 'string', label=T('Archivo Fisico')),

      primarykey=['codigo']
)






###############################################################################
##                                                                           ##
##    Tabla de los Documentos                                                ##
##                                                                           ##
###############################################################################

db.define_table(
      
      'documentos',



      ################ Fase de Planificación

      Field('usuario', 'string', label=T('Usuario creador del documento')),
    
      Field('nombre_doc', 'string', label=T('Nombre del Documento'), unique=True, notnull=True),

      Field('tipo_doc', 'string', label=T('Tipo del Documento'), notnull=True, widget=SQLFORM.widgets.options.widget,
            requires=IS_IN_SET(['Referente Estratégico','Reglamento','Manual de Organización', \
            'Manual de Calidad', 'Manual de Proceso de Gestión', 'Manual de Proceso Técnico', \
            'Manual de Uso', 'Otro'])
      ),


      Field('otro_tipo', 'string', label=T('Otro tipo de documento')),


      Field('responsable', 'string', label=T('Dependencia responsable del Documento'),
            requires=IS_IN_SET(['DIRECCIÓN','LABORATORIO A','LABORATORIO B', \
            'LABORATORIO C','LABORATORIO D','LABORATORIO E',\
            'LABORATORIO F','LABORATORIO G','UNIDAD DE ADMINISTRACIÓN',\
            'COORDINACIÓN DE ADQUISICIONES','COORDINACIÓN DE IMPORTACIONES',\
            'COORDINACIÓN DE LA CALIDAD','OFICINA DE PROTECCIÓN RADIOLÓGICA'
            ])
      ),

      Field('codigo', 'string', label=T('Codigo del registro')),


      Field('objetivo', 'string', label=T('Objetivo del documento')),

      Field('periodo_rev', 'string', label=T('Periodo de revision del Documento'),
            widget=SQLFORM.widgets.options.widget,
            requires=IS_IN_SET(['Semestral', 'Anual','Bienal','Trienal','Quinqueanual'])
      ),




      ################ Fase de Elaboración


      Field('fecha_prox_rev', 'date', requires=IS_DATE(format=('%Y-%m-%d')),
            label=T('Fecha de proxima revision del Documento')
      ),


      Field('anexo_code1', 'string',  label=T('Codigo del anexo')),

      Field('anexo_name1', 'string', label=T('Nombre del anexo del Documento')),


      Field('anexo_code2', 'string',  label=T('Codigo del anexo')),

      Field('anexo_name2', 'string', label=T('Nombre del anexo del Documento')),


      Field('anexo_code3', 'string',  label=T('Codigo del anexo')),

      Field('anexo_name3', 'string', label=T('Nombre del anexo del Documento')),


      Field('anexo_code4', 'string',  label=T('Codigo del anexo')),

      Field('anexo_name4', 'string', label=T('Nombre del anexo del Documento')),


      Field('anexo_code5', 'string',  label=T('Codigo del anexo')),

      Field('anexo_name5', 'string', label=T('Nombre del anexo del Documento')),


      Field('elaborador0', 'string', label=T('Nombre de quien elaboro/actualizo el Documento')),

      Field('elaborador1','string', label=T('Nombre de quien elaboro/actualizo el Documento')),

      Field('elaborador2', 'string', label=T('Nombre de quien elaboro/actualizo el Documento')),

      Field('elaborador3', 'string', label=T('Nombre de quien elaboro/actualizo el Documento')),

      Field('elaborador4', 'string', label=T('Nombre de quien elaboro/actualizo el Documento')),







      ################# Fase de Revisión

      Field('rev_contenido_realizado_por', 'string', label=T('Nombre de quien reviso el contenido del Documento')),

      Field('fecha_rev_contenido', 'date', requires=IS_DATE(format=('%Y-%m-%d')),
          label=T('Fecha de revision del contenido del Documento')
      ),

      Field('rev_especficaciones_doc_realizado_por', 'string',
          label=T('Nombre de quien realizo la revision de las especificaciones')
      ),

      Field('fecha_rev_especificaciones_doc', 'date', requires=IS_DATE(format=('%Y-%m-%d')),
          label=T('Fecha de revision de las especificaciones del Documento')
      ),

      Field('fecha_rev_por_consejo_asesor', 'date', requires=IS_DATE(format=('%Y-%m-%d')),
          label=T('Fecha de revision por el Consejo Asesor')
      ),



      ################# Fase de Aprobación

      Field('aprobado_por', 'string', label=T('Nombre de quien aprobo el Documento')),

      Field('fecha_aprob', 'date', requires=IS_DATE(format=('%Y-%m-%d')), 
            label=T('Fecha de aprobacion del Documento')
      ),

      Field('cod_aprob', 'string', label=T('Codigo de registro de aprobacion del Documento')),

      Field('ubicacion_fisica', 'string', label=T('Ubicacion fisica del Documento')),

      Field('ubicacion_electronica', 'string', label=T('Ubicacion Electronica del Documento')),

      Field('cod_control_cambio', 'string', label=T('Codigo de registro de control de cambios del Documento')),

      Field('fecha_control_cambio', 'date', requires=IS_DATE(format=('%Y-%m-%d')),
            label=T('Fecha de registro de control de cambios en el Documento')
      ),

      Field('ccelaborado', 'text', label=T("Elaborador del control de cambios")),

      Field('registro_fisico', 'text', label=T("Ubicación del registro en formato físico")),

      Field('registro_electronico', 'text', label=T("Ubicación del registro en formato electrónico")),

      Field('vinculo', 'text', label=T("Vinculo electrónico")),


      ############### ESTATUS DEL DOCUMENTO

      Field('estatus', 'string', label=T('Estatus del Documento'), widget=SQLFORM.widgets.options.widget,
          requires=IS_IN_SET(['Planificado','Elaborado','Revisado','Aprobado'])
      ),


    primarykey=['codigo']
)