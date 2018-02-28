#------------------------------------ Modulo de Sustancias, materiales y desechos peligrosos-------------------------------------------


#t_Sustancia: Tabla de sustancias de la cual se obtiene informacion del listado (catalogo de sustancias)
db.define_table(
    #Nombre de la entidad
    't_Sustancia', 
    #Atributos;
    Field('f_nombre', 	'string',	requires=IS_NOT_EMPTY(), label=T('Nombre')),
    Field('f_cas', 		'string',	requires=IS_NOT_EMPTY(), unique=True, label=T('CAS')),
    Field('f_pureza', 	'integer',	requires=IS_INT_IN_RANGE(0, 101), label=T('Pureza')),
    Field('f_estado', 'list:string',requires=IS_IN_SET(['Sólido','Líquido','Gaseoso']), 
    widget=SQLFORM.widgets.checkboxes.widget, label=T('Estado')),
    Field('f_control', 'list:string',requires=IS_IN_SET(['N/A','RL4','RL7', 'RL4 y RL7']), 
    widget=SQLFORM.widgets.checkboxes.widget, label=T('Control')),
    Field('f_peligrosidad', 'list:string',requires=IS_IN_SET(['Inflamable','Tóxico','Tóxico para el ambiente','Corrosivo','Comburente','Nocivo','Explosivo','Irritante'],multiple = True),
    widget=SQLFORM.widgets.checkboxes.widget, label=T('Peligrosidad')),
    # Hoja de seguridad (archivo pdf)
    Field('f_hds','upload',requires=IS_NULL_OR(IS_UPLOAD_FILENAME(extension='pdf')),label=T('Hoja de seguridad'), format='%(f_nombre)s'),
    auth.signature) # Agrega los campos adicionales created_by, created_on, modified_by, modified_on para los logs de la tabla

#db.t_sustancias.id.readable=False #Si se muestra en la forma, descomentar
#db.t_sustancias.id.writable=False
db.t_Sustancia.f_hds.readable=(auth.has_membership('Gestor de SMyDP') or auth.has_membership('WEBMASTER')) #-*-* Chequear permisos aqui
db.t_Sustancia._singular='Catálogo de Sustancias'
db.t_Sustancia._plural='Catálogo de Sustancias'


