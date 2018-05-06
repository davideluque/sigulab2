#------------------------------------ Modulo de Sustancias, materiales y desechos peligrosos -------------------------------------------


#t_Unidades_de_medida: Tabla de unidades de medida de las sustancias (ml, l, g, kg, etc.)
db.define_table(
    #Nombre de la entidad
    't_Unidad_de_medida',

    #Atributos;
    Field('f_nombre', 'string', requires=IS_NOT_EMPTY(), label=T('Nombre')),
    Field('f_abreviatura', 'string', requires=IS_NOT_EMPTY(), label=T('Abreviatura'))
    )

#t_Sustancia: Tabla de sustancias de la cual se obtiene informacion del listado (catalogo de sustancias)
db.define_table(
    #Nombre de la entidad
    't_Sustancia',

    #Atributos;
    Field('f_nombre', 'string', requires=IS_NOT_EMPTY(), label=T('Nombre')),

    Field('f_cas', 'string',    requires=[  IS_NOT_EMPTY(),
                                         IS_MATCH('^[0-9]+\-[0-9]+\-[0-9]+$',
                                error_message='El CAS debe contener tres números separados entre sí por guiones. Por ejemplo, 7732-18-5')],
                                unique=True, label=T('CAS')),

    Field('f_pureza', 	'integer',	requires=IS_INT_IN_RANGE(0, 101), label=T('Pureza')),

    Field('f_estado', 'list:string',requires=IS_IN_SET(['Sólido','Líquido','Gaseoso']), widget=SQLFORM.widgets.options.widget, label=T('Estado')),

    Field('f_control', 'list:string',requires=IS_IN_SET(['N/A','RL4','RL7', 'RL4 y RL7']), widget=SQLFORM.widgets.options.widget, label=T('Control')),

    # *!* La unidad no va aqui, porque alguien podria querer solicitar la sustancia en ml porque es muy poca y estaria obligada a usar una unidad 
    #Field('f_unidad', 'list:string',requires=IS_IN_SET(['kg','g','l', 'ml']), widget=SQLFORM.widgets.options.widget, label=T('Unidad')),

    Field('f_peligrosidad', 'list:string',
          requires=IS_IN_SET(['Inflamable','Tóxico','Tóxico para el ambiente','Corrosivo','Comburente','Nocivo','Explosivo','Irritante'],
          multiple = True), widget=SQLFORM.widgets.checkboxes.widget, label=T('Peligrosidad')),
    
    # Hoja de seguridad (archivo pdf)
    Field('f_hds','upload',requires=IS_NULL_OR(IS_UPLOAD_FILENAME(extension='pdf')),label=T('Hoja de seguridad'), format='%(f_nombre)s'),
    # Agrega los campos adicionales created_by, created_on, modified_by, modified_on para los logs de la tabla
    auth.signature
    )

db.t_Sustancia.id.readable=False
db.t_Sustancia.id.writable=False
db.t_Sustancia.f_hds.readable=(auth.has_membership('Gestor de SMyDP') or auth.has_membership('WEBMASTER')) #-*-* Chequear permisos aqui
db.t_Sustancia._singular='Catálogo de Sustancias'
db.t_Sustancia._plural='Catálogo de Sustancias'


#t_Inventario: Tabla de la entidad debil Inventario que contiene la existencia de cada sustancia en cada espacio fisico
db.define_table(
    #Nombre de la entidad
    't_Inventario',

    #Atributos;

    # Cantidades (el excedente es calculado dinamicamente como existencia - uso interno)
    Field('f_existencia', 'double', requires=IS_NOT_EMPTY(), label=T('Existencia')),
    Field('f_uso_interno', 'double', requires=IS_NOT_EMPTY(), label=T('Uso interno')),
    Field('f_medida', 'reference t_Unidad_de_medida',
          requires=IS_IN_DB(db, db.t_Unidad_de_medida.id, '%(f_nombre)s', zero=None), label=T('Unidad de medida'), notnull=True),
    # Referencias a otras tablas
    Field('espacio', 'reference espacios_fisicos',
          requires=IS_IN_DB(db, db.espacios_fisicos.id, '%(nombre)s', zero=None), label=T('Espacio Físico'), notnull=True),
    Field('sustancia', 'reference t_Sustancia',
          requires=IS_IN_DB(db, db.t_Sustancia.id, '%(f_nombre)s', zero=None), label=T('Sustancia'), notnull=True),
    
    # Agrega los campos adicionales created_by, created_on, modified_by, modified_on para los logs de la tabla
    auth.signature
    )

db.t_Inventario._singular='Inventario'
db.t_Inventario._plural='Inventario'


# Tabla de Grupos de Desechos peligrosos. Cada desecho peligroso pertenece a un cierto grupo (tipo), los cuáles
# se definen en esta tabla. Contiene los campos: grupo de desecho, estado, peligrosidad.
db.define_table(
    'grupo_desechos',
    #Atributos;
    Field('grupo', 'string', unique=True, notnull=True, label=T('Grupo')),

    Field('estado', 'string', requires=IS_IN_SET(['Sólido', 'Líquido', 'Gaseoso']), notnull=True, label=T('Estado')),
    
    Field('peligrosidad', 'string', notnull=True, label=T('Peligrosidad'))
)


db.grupo_desechos._plural = 'Grupo de Desecho'
db.grupo_desechos._singular = 'Grupos de Desechos'

# Tabla de Desechos peligrosos. Contiene los campos: espacio_físico, cantidad, sección, responsable, grupo.
db.define_table(
    'desechos',
    #Atributos;
    Field('espacio_fisico', 'reference espacios_fisicos', 
            requires=IS_IN_DB(db, db.espacios_fisicos.id, '%(nombre)s', zero=None), notnull=True, label=T('Espacio físico')), 

    Field('cantidad', 'double', requires=IS_NOT_EMPTY(), label=T('Cantidad'), notnull=True),

    Field('seccion', 'reference dependencias', requires=IS_IN_DB(db, db.dependencias.id, '%(nombre)s', zero=None), label=T('Unidad de Adscripción'), notnull=True),
    
    Field('unidad_medida', 'reference t_Unidad_de_medida',
          requires=IS_IN_DB(db, db.t_Unidad_de_medida.id, '%(f_nombre)s', zero=None), label=T('Unidad de medida'), notnull=True),

    Field('responsable', 'reference t_Personal', 
            requires=IS_IN_DB(db, db.t_Personal.id, '%(f_email)s', zero=None), notnull=True, label=T('Responsable')),

    Field('grupo', 'reference grupo_desechos', 
            requires=IS_IN_DB(db, db.grupo_desechos.id, '%(grupo)s', zero=None), notnull=True, label=T('Grupo de Desecho')),

    
)