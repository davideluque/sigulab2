# Usemos la siguiente convencion:
#
# Los nombres de cada tabla seran en minusculas, separados con _ y en plural.
#
# Los nombres de los atributos seran en minusculas y singular, a menos de que se trate de una lista, en ese caso
# se intentara tomar un nombre distinto al de una tabla
#
# Si un atributo tiene como referencia a un record de otra tabla, se le agregara el sufijo _<tabla> si es dificil
# identificar que se trata de una referencia, si no es asi, se adoptara la convencion normal de atributos


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
    # Auto-Referencia
    Field('unidad_de_adscripcion', 'reference dependencias', requires=False), label=T('Unidad de Adscripción')
)

# Auto-Referencia, se definira cual dependencia es la unidad de adscripcion, esta sera una relacion de 0-1 a muchos
# una dependencia tendra adscrita varias, pero cada dependencia tendra o ninguna o una dependencia 'jefe'

# Se define fuera de la tabla para asegurar su existencia antes de ser referenciada

db.dependencias.unidad_de_adscripcion.requires = IS_EMPTY_OR(IS_IN_DB(db, db.dependencias.id, '%(nombre)s', zero=None))

db.dependencias._plural = 'Dependencias'
db.dependencias._singular = 'Dependencia'
