# Usemos la siguiente convencion:
#
# Los nombres de cada tabla seran en minusculas, separados con _ y en plural.
#
# Los nombres de los atributos seran en minusculas y singular, a menos de que se trate de una lista, en ese caso
# se intentara tomar un nombre distinto al de una tabla
#
# Si un atributo tiene como referencia a un record de otra tabla, se le agregara el sufijo _<tabla> si es dificil
# identificar que se trata de una referencia, si no es asi, se adoptara la convencion normal de atributos

#######################################################################################################################
#
# Tablas de Autenticacion de Usuarios
#
#######################################################################################################################

# Aqui se crearan las tablas de autenticacion, antes de ser estas definidas por web2py.
# Despues de auth = Auth(db) pero antes de auth.define_tables(username=True)
# (En el archivo 'db.py', la linea auth.define_tables(username=True) fue eliminada para ser usada aqui)

# La tabla de auth_membership funcionara como la tabla de roles, asociaremos a esta una referencia a las dependencias.
auth.settings.extra_fields['auth_membership'] = [
    Field('dependencia_asociada', 'string',
          label=T('Dependencia Asociada al Rol'))
]


# Definimos todas las tablas de web2py por defecto con las modificaciones hechas

auth.define_tables()

######################################################################################################################
#
# Tablas principales de los modulos
# Se definira antes que las tablas de autenticacion porque son necesarias para estas
#
######################################################################################################################

# Tabla de Sedes, necesaria para las Dependencias

db.define_table(
    'sedes',
    Field('nombre', 'string', unique=True, notnull=True, label=T('Nombre de la Sede')),
)

# Tabla de Dependencias, Incluira la Direccion, los laboratorios y sus secciones y las coordinaciones

db.define_table(
    #Nombre de la entidad
    'dependencias',
    #Atributos;
    Field('nombre', 'string', notnull=True, label=T('Nombre')),

    Field('email', 'string', requires=IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com'), label=T('Correo')),
    # Auto-Referencia
    Field('id_jefe_dependencia', 'reference auth_user', requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s | %(email)s'), label=T('Responsable')),
    
    Field('unidad_de_adscripcion', 'reference dependencias', requires=False, label=T('Unidad de Adscripción')),

    Field('id_sede', 'reference sedes', requires=IS_IN_DB(db, db.sedes.id, '%(nombre)s'), label=T('Sede')),

    Field('ext_USB', 'list:integer', label=T('Extension Telefonica USB')),

    Field('ext_interna', 'string', label=T('Extension Telefonica Interna')),

    Field('fax', 'integer', label=T('Fax')),

    Field('pagina_web', 'string', label=T('Pagina Web'))

)

# Auto-Referencia, se definira cual dependencia es la unidad de adscripcion, esta sera una relacion de 0-1 a muchos
# una dependencia tendra adscrita varias, pero cada dependencia tendra o ninguna o una dependencia 'jefe'

# Se define fuera de la tabla para asegurar su existencia antes de ser referenciada

db.dependencias.unidad_de_adscripcion.requires = IS_EMPTY_OR(IS_IN_DB(db, db.dependencias.id, '%(nombre)s', zero=None))

db.dependencias._plural = 'Dependencias'
db.dependencias._singular = 'Dependencia'

db.auth_membership.dependencia_asociada.requires = IS_IN_DB(db, db.dependencias.id, '%(nombre)s', zero=None)
db.auth_membership.dependencia_asociada.type = 'reference dependencias'

# Tabla de Espacios Fisicos, incluira el nombre, la direccion de este y bajo que dependencia esta adscrito
db.define_table(
    'espacios_fisicos',
    #Atributos;
    Field('nombre', 'string', unique=True, notnull=True, label=T('Nombre')),
    Field('direccion', 'string', unique=True, notnull=True, label=T('Direccion')),
    #Referencia (Revisar si el label es asistio o organizo)
    Field('dependencia_adscrita', 'reference dependencias',
          requires=IS_IN_DB(db, db.dependencias.id, '%(nombre)s', zero=None), label=T('Ubicacion')),
    )
db.espacios_fisicos._plural = 'Espacio Fisico'
db.espacios_fisicos._singular = 'Espacio Fisico'
