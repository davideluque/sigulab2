#------------------------------------ Modulo de Sustancias, materiales y desechos -------------------------------------------


"""
#t_Sustancia: Tabla de sustancias de la cual se obtiene informacion del listado (catalogo de sustancias)
db.define_table(
    #Nombre de la entidad
    't_Sustancia', 
    #Atributos;
    Field('f_nombre', 'string', label=T('Nombre'),requires=IS_NOT_EMPTY(),
    Field('f_cas', 'string', label=T('CAS'),requires=IS_NOT_EMPTY()),
    Field('f_pureza', 'integer',requires=IS_INT_IN_RANGE(0, 101), label=T('Pureza')),
    Field('f_estado', 'integer', requires=IS_IN_DB(db,db.t_estado.id,'%(f_estado)s'), label=T('Estado'),
    Field('f_control', 'integer', label=T('Control'), requires=IS_IN_DB(db,db.t_regimenes.id,'%(f_nombre)s'),
    Field('f_peligrosidad', 'list:string', label=T('Peligrosidad'),requires=IS_IN_SET(['Inflamable','Tóxico','Tóxico para el ambiente','Corrosivo','Comburente','Nocivo','Explosivo','Irritante'],multiple = True),
    widget=SQLFORM.widgets.checkboxes.widget),
    Field('f_reporte','upload',label=T('MSDS'),requires=IS_NULL_OR(IS_UPLOAD_FILENAME(extension='pdf'))),
    format='%(f_nombre)s',
    migrate=settings.migrate)

db.t_sustancias.id.readable=False
db.t_sustancias.id.writable=False
db.t_sustancias.f_reporte.readable=(auth.has_membership('Gestor de Sustancias')or auth.has_membership('WebMaster'))
db.t_sustancias._singular='Listado de Sustancias'
db.t_sustancias._plural='Listado de Sustancias'
"""