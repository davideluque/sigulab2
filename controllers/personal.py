#-----------------------------------#
#                                   #
#  Controlador del Modulo Personal  #
#                                   #
#-----------------------------------#

def index():
    return dict()

#Enviar info a la tabla del listado
def tabla_categoria():


    #Buscamos la tabla personal
    tb = db().select(db.t_Personal.ALL)

    #Creamos una lista para enviar a la vista
    jsns = []


    #Llenamos la lista con los json
    for elm in tb:

        #Buscamos el nombre de la dependencia con el id que manda la vista
        named = db(db.dependencias.id == elm.f_dependencia).select(db.dependencias.ALL)

        dep= named[0].nombre if len(named) > 0 else None

        if (dep) : idUSuperior = (db(db.dependencias.nombre==dep).select(db.dependencias.ALL)).first().unidad_de_adscripcion
        else: idUSuperior=None
        if (idUSuperior) : Usuperior=(db(db.dependencias.id==idUSuperior).select(db.dependencias.ALL)).first().nombre
        else: Usuperior=None

        jsns.append(
            {"nombre" : elm.f_nombre,
            "apellido" : elm.f_apellido,
            "ci" : elm.f_ci,
            "email" : elm.f_email,
            "telefono" : elm.f_telefono,
            "pagina_web" : elm.f_pagina_web,
            "categoria" : elm.f_categoria,
            "cargo" : elm.f_cargo,
            "fecha_ingreso" : elm.f_fecha_ingreso,
            "fecha_salida" : elm.f_fecha_salida,
            "estatus" : elm.f_estatus,
            "dependencia" : dep,
             "celular" : elm.f_celular,
             "contacto_emergencia" : elm.f_contacto_emergencia,
             "direccion" : elm.f_direccion,
             "gremio" : elm.f_gremio,
             "fecha_ingreso_usb" : elm.f_fecha_ingreso_usb,
             "fecha_ingreso_ulab" : elm.f_fecha_ingreso_ulab,
             "fecha_ingreso_admin_publica" : elm.f_fecha_ingreso_admin_publica,
             "condicion" : elm.f_condicion,
             "unidad_jerarquica_superior" : Usuperior,
             "dependencia" : dep ,
             "rol" : elm.f_rol,
             "ubicacion" : elm.f_ubicacion,
             "es_supervisor": elm.f_es_supervisor
             })

    return jsns

#Mandar informacion a los dropdowns
def dropdowns():

    #Dropdown de gremio
    gremio = ['Docente', 'Administrativo', 'Estudiante']
    #Dropdown de dependencias
    departamento = db(db.dependencias.nombre).select(db.dependencias.ALL)
    #Dropdown de estatus
    estatus = ['Activo', 'Jubilado', 'Retirado']
    #Dropdown de categoria
    categoria = ['Fijo' , 'Contratado', 'Pasantía' , 'Ayudantía']
    #Dropdown de condiciones
    condiciones = ['En funciones', 'Año Sabático', 'Reposo', 'Permiso Pre-Natal', 'Permiso Post-Natal']
    #Dropdown de roles
    roles= list(db(db.auth_group.role).select(db.auth_group.ALL))

    return (gremio,departamento,estatus,categoria,condiciones,roles)

#Funcion que toma las variables de la vista
def add_form():

    dic = {"nombre" : request.post_vars.nombre_add,
            "apellido" : request.post_vars.apellido_add,
            "ci" : request.post_vars.ci_add,
            "email" : request.post_vars.email_add,
            "telefono" : request.post_vars.telefono_add,
            "pagina_web" : request.post_vars.pagina_web_add,
            "categoria" : request.post_vars.categoria_add,
            "cargo" : request.post_vars.cargo_add,
            "fecha_ingreso" : request.post_vars.fecha_ingreso_add,
            "fecha_salida" : request.post_vars.fecha_salida_add,
            "estatus" : request.post_vars.estatus_add,
             "celular" : request.post_vars.celular_add,
             "contacto_emergencia" : request.post_vars.contacto_emergencia_add,
             "direccion" : request.post_vars.direccion_add,
             "gremio" : request.post_vars.gremio_add,
             "fecha_ingreso_usb" : request.post_vars.fecha_ingreso_usb_add,
             "fecha_ingreso_ulab" : request.post_vars.fecha_ingreso_ulab_add,
             "fecha_ingreso_admin_publica" : request.post_vars.fecha_ingreso_admin_publica_add,
             "condicion" : request.post_vars.condicion_add,
             "ubicacion" : request.post_vars.ubicacion_add,
             "dependencia" : request.post_vars.dependencia_add,
             "rol" : request.post_vars.rol_add
            }

    #if str(dic) != "{'categoria': None, 'ci': None, 'estatus': None, 'pagina_web': None, 'cargo': None, 'dependencia': None, 'fecha_ingreso': None, 'fecha_salida': None, 'nombre': None, 'telefono': None, 'email': None}":

    #Si el diccionario no esta vacio
    if (not(None in dic.values())):
        #Insertamos en la base de datos
        db(db.t_Personal.f_email == dic['email'] ).update(f_nombre = dic["nombre"],
                                f_apellido = dic["apellido"],
                                f_ci = dic["ci"],
                                f_email = dic["email"],
                                f_telefono = dic["telefono"],
                                f_pagina_web = dic["pagina_web"],
                                f_categoria = dic["categoria"],
                                f_cargo = dic["cargo"],
                                f_fecha_ingreso = dic["fecha_ingreso"],
                                f_fecha_salida = dic["fecha_salida"],
                                f_estatus = dic["estatus"],
                              f_celular= dic["celular"],
            f_contacto_emergencia= dic["contacto_emergencia"],
            f_direccion= dic["direccion"],
            f_gremio= dic["gremio"],
            f_fecha_ingreso_usb= dic["fecha_ingreso_usb"],
            f_fecha_ingreso_ulab= dic["fecha_ingreso_ulab"],
            f_fecha_ingreso_admin_publica= dic["fecha_ingreso_admin_publica"],
            f_condicion= dic["condicion"],
            f_ubicacion= dic["ubicacion"],
            f_rol= dic["rol"])
        redirect(URL('listado'))


#Creamos la clase usuario que contiene la informacion del usuario que se entregara a la vista
class Usuario(object):
    """
    Esta clase usuario no tiene ninguna relacion con la base de datos, solamente
    es para facilitar la presentacion en el template.
    """
    def __init__(self, usuario):
        # pagina 1
        self.f_nombre = usuario.f_nombre
        self.f_apellido = usuario.f_apellido
        self.f_ci = usuario.f_ci
        self.f_email = usuario.f_email
        dependencia = usuario.f_dependencia
        dependencia = db(db.dependencias.id == dependencia).select().first()
        self.f_dependencia = dependencia.nombre
        self.f_extension = usuario.f_telefono
        self.f_celular = usuario.f_celular
        self.f_direccion = usuario.f_direccion
        self.f_contacto_emergencia = usuario.f_contacto_emergencia
        self.f_pagina_web = usuario.f_pagina_web

        # pagina 2
        self.f_estatus = usuario.f_estatus
        self.f_categoria = usuario.f_categoria
        self.f_condicion = usuario.f_condicion
        self.f_fecha_ingreso = usuario.f_fecha_ingreso
        self.f_fecha_salida = usuario.f_fecha_salida
        self.f_fecha_ingreso_usb = usuario.f_fecha_ingreso_usb
        self.f_fecha_ingreso_ulab = usuario.f_fecha_ingreso_ulab
        self.f_fecha_ingreso_admin_publica = usuario.f_fecha_ingreso_admin_publica

        # pagina 3
        self.f_cargo = usuario.f_cargo
        self.f_gremio = usuario.f_gremio
        self.f_ubicacion = usuario.f_ubicacion
        self.f_rol = usuario.f_rol
        # dependencia ya dada arriba
        self.f_es_supervisor = usuario.f_es_supervisor
        
#Funcion que envia los datos a la vista
@auth.requires_login(otherwise=URL('modulos', 'login'))
def listado():
    #Obtenemos el usuario loggeado
    infoUsuario=(db(db.auth_user.id==auth.user.id).select(db.auth_user.ALL)).first()
    usuario = Usuario(infoUsuario.t_Personal.select().first())
    #Obtenemos los datos para el listado
    tabla = tabla_categoria()

    #Obtenemos los elementos de los dropdowns
    gremios, dependencias, estados, categorias, condiciones, roles = dropdowns()

    return dict(
        grid=tabla,
        categorias=categorias,
        dependencias=dependencias,
        estados=estados,
        gremios=gremios,
        condiciones=condiciones,
        roles=roles,
        usuario=usuario
        
        )

def reporte():
    tabla=tabla_categoria()
    personas=[]
    for persona in tabla:
        personas.append(persona)
    return dict(personas=personas)
