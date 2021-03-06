#------------------------------------------------Modulo de Personal-----------------------------------------------------------------------------------------------------------------------------------------------------------

# Tablas para formularios adicionales

#####################################################################
#                                                                   #
#                        Competencias                               #
#                                                                   #
#####################################################################

db.define_table(
    't_Competencias',
    # Atributos
    Field('f_nombre', 'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Competencia')),
    Field('f_observaciones', 'string', length=150, label=T('Observaciones')),
    Field('f_categorias', 'list:string', default='', label=T('Categorías')),
    Field('f_numero', 'integer', default=1,label=T('Numero')),
    Field('f_Competencia_Personal', 'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_Personal)s', zero=None) ),
    migrate=True
    )
db.t_Competencias._plural = 'Competencias'
db.t_Competencias._singular = 'Competencia'


#####################################################################
#                                                                   #
#                      Historial Laboral                            #
#                                                                   #
#####################################################################

db.define_table(
    
    #Nombre de la entidad
    't_Historial_trabajo', 
    
    #Atributos;
    Field('f_fecha_inicio_1', 'date', label=T('Desde')),
    Field('f_fecha_final_1', 'date', label=T('Hasta')),
    Field('f_dependencia_hist_1', 'string', label=T('Dependencia')),
    Field('f_organizacion_1',          'string', label=T('Organización')),
    Field('f_cargo_hist_1',          'string', label=T('Cargo')),
    Field('f_rol_hist_1',          'string', label=T('Rol')),
    Field('f_fecha_inicio_2', 'date', label=T('Desde')),
    Field('f_fecha_final_2', 'date', label=T('Hasta')),
    Field('f_dependencia_hist_2', 'string', label=T('Dependencia')),
    Field('f_organizacion_2',          'string',label=T('Organización')),
    Field('f_cargo_hist_2',          'string', label=T('Cargo')),
    Field('f_rol_hist_2',          'string', label=T('Rol')),
    Field('f_fecha_inicio_3', 'date', label=T('Desde')),
    Field('f_fecha_final_3', 'date', label=T('Hasta')),
    Field('f_dependencia_hist_3', 'string', label=T('Dependencia')),
    Field('f_organizacion_3',          'string', label=T('Organización')),
    Field('f_cargo_hist_3',          'string', label=T('Cargo')),
    Field('f_rol_hist_3',          'string', label=T('Rol')),
    Field('f_fecha_inicio_4', 'date', label=T('Desde')),
    Field('f_fecha_final_4', 'date', label=T('Hasta')),
    Field('f_dependencia_hist_4', 'string', label=T('Dependencia')),
    Field('f_organizacion_4',          'string', label=T('Organización')),
    Field('f_cargo_hist_4',          'string', label=T('Cargo')),
    Field('f_rol_hist_4',          'string', label=T('Rol')),
    Field('f_fecha_inicio_5', 'date', label=T('Desde')),
    Field('f_fecha_final_5', 'date', label=T('Hasta')),
    Field('f_dependencia_hist_5', 'string', label=T('Dependencia')),
    Field('f_organizacion_5',          'string', label=T('Organización')),
    Field('f_cargo_hist_5',          'string', label=T('Cargo')),
    Field('f_rol_hist_5',          'string',label=T('Rol')),
    #Referencia (Revisar si el label es asistio o organizo)
    Field('f_Historial_trabajo_Personal',         'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_Personal)s', zero=None), label=T('Posee')),
    )

db.t_Historial_trabajo._plural = 'Historial de trabajo'
db.t_Historial_trabajo._singular = 'Historial de trabajo'

#####################################################################
#                                                                   #
#                  Actividades Administrativas                      #
#                                                                   #
#####################################################################

db.define_table(
    't_Actividades_Administrativas',
    # Atributos
    Field('f_fecha_inicio', 'date', label=T('Fecha de inicio'), requires=IS_NOT_EMPTY()),
    Field('f_fecha_final', 'date', label=T('Fecha de fin'), requires=IS_NOT_EMPTY()),
    Field('f_cargo', 'string', length=150,label=T('Cargo'), requires=IS_NOT_EMPTY()),
    Field('f_institucion', 'string', length=150, label=T('Institución'), requires=IS_NOT_EMPTY()),
    Field('f_numero', 'integer'),
    Field('f_Administrativas_Personal', 'reference t_Personal',
        requires=IS_IN_DB(db, db.t_Personal.id, '%(f_Personal)s', zero=None) ),
    migrate=True
    )
db.t_Actividades_Administrativas._plural = 'Actividades administrativas'
db.t_Actividades_Administrativas._singular = 'Actividad administrativa'

#####################################################################
#                                                                   #
#                              Extension                            #
#                                                                   #
#####################################################################

db.define_table(
    't_Extension',
    # Atributos
    Field('f_categoria', 'list:string', default='', label=T('Categorías')),
    Field('f_fecha_inicio', 'date', label=T('Fecha de inicio'), requires=IS_NOT_EMPTY()),
    Field('f_fecha_final', 'date', label=T('Fecha de fin'), requires=IS_NOT_EMPTY()),
    Field('f_nombre', 'string', label=T('Nombre'), requires=IS_NOT_EMPTY()),
    Field('f_descripcion', 'string', label=T('Descripción'), requires=IS_NOT_EMPTY()),
    Field('f_institucion', 'string', label=T('Institución'), requires=IS_NOT_EMPTY()),
    Field('f_numero', 'integer'),
    Field('f_Extension_Personal', 'reference t_Personal',
        requires=IS_IN_DB(db, db.t_Personal.id, '%(f_Personal)s', zero=None) ),
    migrate=True
    )
db.t_Extension._plural = 'Actividades de extensión'
db.t_Extension._singular = 'Actividad de extensión'

#####################################################################
#                                                                   #
#                 Proyectos de Investigacion                        #
#                                                                   #
#####################################################################

db.define_table(
    #Nombre de la entidad
    't_Proyecto', 
    #Atributos;
    Field('f_categoria', 'list:string', default='', label=T('Categoría')),
    Field('f_fecha_inicio', 'date',label=T('Desde')),
    Field('f_fecha_fin', 'date',label=T('Hasta')),
    Field('f_titulo', 'string', label=T('Título')),
    Field('f_responsabilidad', 'string', label=T('Responsabilidad')),
    Field('f_resultados', 'string', label=T('Resultados')),
    Field('f_institucion', 'string', label=T('Institución')),
    Field('f_numero', 'integer'),
    #Referencia
    Field('f_proyecto_Personal', 'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_Personal)s', zero=None), label=T('Participante')),
    )

db.t_Proyecto._plural = 'Proyectos'
db.t_Proyecto._singular = 'Proyecto'

#####################################################################
#                                                                   #
#                     Trabajos Dirigidos                            #
#                                                                   #
#####################################################################

#t_Personal: Tabla de Trabajos dirigidos
db.define_table(
    #Nombre de la entidad
    't_Trabajos_dirigidos', 
    #Atributos;
    Field('f_anio',          'integer', requires=IS_INT_IN_RANGE(minimum=1900,maximum=2100, error_message='Introduzca un año válido'), notnull=True, label=T('Año')),
    Field('f_estudiantes', 'string', default='', label=T('Estudiantes')),
    Field('f_titulo_trabajo',          'string', label=T('Titulo')),
    Field('f_nivel',  'list:string', default='', label=T('Nivel')),
    Field('f_institucion',          'string', label=T('Institución')),
    Field('f_numero', 'integer', default=1,label=T('Numero')),
    Field('f_Trabajo_Personal', 'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_Personal)s', zero=None) ),
    migrate=True
    )

db.t_Trabajos_dirigidos._plural = 'Trabajos'
db.t_Trabajos_dirigidos._singular = 'Trabajo'

#####################################################################
#                                                                   #
#                              Cursos                               #
#                                                                   #
#####################################################################

db.define_table(
    #Nombre de la entidad
    't_Cursos', 
    #Atributos;
    Field('f_anio',          'integer', requires=IS_INT_IN_RANGE(minimum=1900,maximum=2100, error_message='Introduzca un año válido'), notnull=True, label=T('Año')),
    Field('f_horas',          'integer', requires=IS_INT_IN_RANGE(minimum=1, error_message='Las horas no pueden ser negativas'), notnull=True, label=T('Horas')),
    Field('f_categorias', 'list:string', default='', label=T('Categorías')),
    Field('f_formacion',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Formacion')),
    Field('f_dictadoPor',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('DictadoPor')),
    Field('f_numero', 'integer', default=1,label=T('Numero')),
    Field('f_Cursos_Personal', 'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_Personal)s', zero=None) ),
    migrate=True 
    )

db.t_Cursos._plural = 'Cursos'
db.t_Cursos._singular = 'Curso'

#####################################################################
#                                                                   #
#                              Materias                             #
#                                                                   #
#####################################################################

#t_Personal: Tabla de Materias.
db.define_table(
    #Nombre de la entidad
    't_Materia', 
    #Atributos;
	Field('f_area', 'list:string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Área')),
    Field('f_codigo','string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Código')),
    Field('f_nombre_materia',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Materia')),
    Field('f_fecha_inicio_materia', 'date', label=T('Desde')),
    Field('f_fecha_final_materia', 'date', label=T('Hasta')),
    Field('f_numero', 'integer', default=1,label=T('Numero')),
    Field('f_Materia_Personal',         'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_Personal)s', zero=None), label=T('Dirigió')),
    migrate=True
    )

db.t_Materia._plural = 'Materias'
db.t_Materia._singular = 'Materia'

#####################################################################
#                                                                   #
#                      Estudios Formales                            #
#                                                                   #
#####################################################################

#t_Personal: Tabla de Materias.
db.define_table(
    #Nombre de la entidad
    't_Estudios',
    Field('f_numero', 'integer', default=1,label=T('Numero')),
    Field('f_anio', 'integer', requires=IS_INT_IN_RANGE(minimum=1900,maximum=2100, error_message='Introduzca un año válido'), notnull=True, label=T('Año')),
    Field('f_nivel', 'list:string', default='', label=T('Nivel')),
    Field('f_titulo', 'string', label=T('Titulo')),
    Field('f_area', 'string', label=T('Area de Especializacion')),
    Field('f_institucion',          'string', label=T('Institución')),
    Field('f_ubicacion', 'string', default='', label=T('Estudiantes')),
    Field('f_categorias', 'list:string', default='', label=T('Categorías')),
    Field('f_Estudios_Personal', 'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_Personal)s', zero=None) ),
    migrate=True
    )

'''

TABLAS PARA FORMULARIOS NO IMPLEMENTADOS (REVISAR)

#t_Personal: Tabla de publicaciones.
db.define_table(
    #Nombre de la entidad
    't_Publicacion', 
    #Atributos;
    Field('f_anio',          'integer', requires=IS_INT_IN_RANGE(minimum=1900,maximum=2100, error_message='Introduzca un año válido'), notnull=True, label=T('Año de Publicación')),
    Field('f_arbitrada',          'boolean', requires=IS_NOT_EMPTY(), notnull=True, label=T('Arbitrada')),
    Field('f_titulo',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Título')),
    Field('f_autores',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Autores')),
    Field('f_referencia',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Referencia')),
    #Referencia
    Field('f_publicacion_Personal',         'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_Personal)s', zero=None), label=T('Autor')),
    )

db.t_Publicacion._plural = 'Publicaciones'
db.t_Publicacion._singular = 'Publicacion'

#t_Personal: Tabla de eventos.
db.define_table(
    #Nombre de la entidad
    't_Evento', 
    #Atributos;
    Field('f_anio',          'integer', requires=IS_INT_IN_RANGE(minimum=1900,maximum=2100, error_message='Introduzca un año válido'), notnull=True, label=T('Año')),
    Field('f_lugar',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Lugar')),
    Field('f_titulo',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Título')),
    Field('f_coactores',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Coactores')),
    Field('f_nombre',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Nombre')),
    #Referencia (Revisar si el label es asistio o organizo)
    Field('f_evento_Personal',         'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_Personal)s', zero=None), label=T('Asistió')),
    )

db.t_Evento._plural = 'Eventos'
db.t_Evento._singular = 'Evento'


#t_Personal: Tabla de Reconocimientos.
db.define_table(
    #Nombre de la entidad
    't_Reconocimiento', 
    #Atributos;
    Field('f_anio',          'integer', requires=IS_INT_IN_RANGE(minimum=1900,maximum=2100, error_message='Introduzca un año válido'), notnull=True, label=T('Año')),
    Field('f_referencia',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Referencia')),
    Field('f_otorgado_por',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Otorgado por')),
    #Referencia (Revisar si el label es asistio o organizo)
    Field('f_Reconocimiento_Personal',         'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_Personal)s', zero=None), label=T('Obtuvo')),
    )

db.t_Reconocimiento._plural = 'Reconocimientos'
db.t_Reconocimiento._singular = 'Reconocimiento'


#t_Personal: Tabla de Comisiones.
db.define_table(
    #Nombre de la entidad
    't_Comision', 
    #Atributos;
    Field('f_fecha',          'string', requires=IS_DATE(format=T('%d/%m/%Y'), error_message='Debe tener el siguiente formato: dd/mm/yyyy'), notnull=True, label=T('Fecha')),
    Field('f_rol',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Rol')),
    Field('f_nombre',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Nombre')),
    #Referencia (Revisar si el label es asistio o organizo)
    Field('f_Comision_Personal',         'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_Personal)s', zero=None), label=T('Participó')),
    )

db.t_Comision._plural = 'Comisiones'
db.t_Comision._singular = 'Comision'


#t_Personal: Tabla de Tesis.
db.define_table(
    #Nombre de la entidad
    't_Tesis', 
    #Atributos;
    Field('f_anio',          'integer', requires=IS_INT_IN_RANGE(minimum=1900,maximum=2100, error_message='Introduzca un año válido'), notnull=True, label=T('Año')),
    Field('f_nivel',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Nivel')),
    Field('f_trabajo',          'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Trabajo')),
    #Referencia (Revisar si el label es asistio o organizo)
    Field('f_Tesis_Personal',         'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_Personal)s', zero=None), label=T('Publicó')),
    )

db.t_Tesis._plural = 'Tesis'
db.t_Tesis._singular = 'Tesis'

'''