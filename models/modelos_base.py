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
    Field('nombre', 'string', requires=IS_NOT_EMPTY(), notnull=True, label=T('Nombre')),
    # Auto-Referencia
    Field('unidad_de_adscripcion', 'reference dependencias', requires=False, label=T('Unidad de Adscripción')),

    Field('id_sede', 'reference sedes', requires=IS_IN_DB(db, db.sedes.id, '%(nombre)s'), label=T('Sede'))
)

# Auto-Referencia, se definira cual dependencia es la unidad de adscripcion, esta sera una relacion de 0-1 a muchos
# una dependencia tendra adscrita varias, pero cada dependencia tendra o ninguna o una dependencia 'jefe'

# Se define fuera de la tabla para asegurar su existencia antes de ser referenciada

db.dependencias.unidad_de_adscripcion.requires = IS_IN_DB(db, db.dependencias.id, '%(nombre)s', zero=None)

db.dependencias._plural = 'Dependencias'
db.dependencias._singular = 'Dependencia'

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
    Field('dependencia_asociada', 'reference dependencias',
          requires=IS_EMPTY_OR(IS_IN_DB(db, db.dependencias.id, '%(nombre)s', zero=None)),
          label=T('Dependencia Asociada al Rol'))
]

# Definimos todas las tablas de web2py por defecto con las modificaciones hechas

auth.define_tables()

#######################################################################################################################
#
# Tabla principal del modulo de personal. Englobara la info de cada persona en la unidad de laboratorios. Es necesaria
# para el funcionamiento de cualquier otro modulo
#
#######################################################################################################################

db.define_table(
    #Nombre de la entidad
    'personal',
    #Atributos;
    Field('nombre',         'string',
          requires=IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]([a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+[\s-]?[a-zA-ZñÑáéíóúÁÉÍÓÚ\s][a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+)*$',
                            error_message='Debe ser no vacío y contener sólo letras, guiones o espacios.'),

          notnull=True, label=T('Nombre')),

    Field('categoria',      'string',
          requires=IS_IN_SET(['Docente', 'Administrativo', 'Técnico', 'Obrero']), notnull=True, label=T('Categoría')),

    Field('cargo',          'string',
          requires=IS_NOT_EMPTY(), notnull=True, label=T('Cargo')),

    Field('ci',             'integer',
          requires=IS_INT_IN_RANGE(minimum=1,maximum=100000000, error_message='Número de cedula no válido.'),
          notnull=True, label=T('Cédula')),

    Field('email',          'string',
          requires=IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com'),
          notnull=True, label=T('Correo Electrónico')),

    Field('telefono',       'integer',  default = '00', label=T('Teléfono')),
    Field('pagina_web',     'string', default = 'N/A', label=T('Página web')),

    Field('estatus',        'string', requires=IS_IN_SET(['Activo', 'Jubilado', 'Retirado']),
          default='Activo', notnull=True, label=T('Estatus')),

    Field('fecha_ingreso',  'string', default='N/A', label=T('Fecha de Ingreso')),
    Field('fecha_salida',   'string', default='N/A', label=T('Fecha de Salida')),

    #Referencias
    Field('usuario', 'reference auth_user',
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s | %(email)s'), label=T('Usuario Asociado')),

    Field('dependencia', 'reference dependencias',
          requires=IS_IN_DB(db, db.dependencias, '%(nombre)s'), label=T('Pertenece A'))
    )

db.personal._plural = 'Personal'
db.personal._singular = 'Personal'


#######################################################################################################################
#
# Tablas Generales
#
#######################################################################################################################

# Tabla de Espacios Fisicos, incluira el nombre, la direccion de este y bajo que dependencia esta adscrito
db.define_table(
    'espacios_fisicos',
    #Atributos;
    Field('nombre', 'string', unique=True, notnull=True, label=T('Nombre')),
    Field('direccion', 'string', unique=True, notnull=True, label=T('Direccion')),
    #Referencia (Revisar si el label es asistio o organizo)
    Field('dependencia_adscrita', 'reference dependencias',
          requires=IS_IN_DB(db, db.dependencias.id, '%(nombre)s', zero=None), label=T('Dependencia Adscrita')),
    )
db.espacios_fisicos._plural = 'Espacio Fisico'
db.espacios_fisicos._singular = 'Espacio Fisico'