#-----------------------------------#
#                                   #
#  Controlador del Modulo Personal  #
#                                   #
#-----------------------------------#

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
        else: idUsuperior=None
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
             "ubicacion" : elm.f_ubicacion
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

    return (gremio,departamento,estatus,categoria,condiciones)

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
            f_rol= (db(db.auth_group.role == dic['rol']).select(db.auth_group.ALL)).first().id)
        redirect(URL('listado'))

#Funcion que toma las variables de la vista
def edit_form():

    edic = {"nombre" : request.post_vars.nombre_edit,
            "apellido" : request.post_vars.apellido_edit,
            "ci" : request.post_vars.ci_edit,
            "email" : request.post_vars.email_edit,
            "telefono" : request.post_vars.telefono_edit,
            "pagina_web" : request.post_vars.pagina_web_edit,
            "categoria" : request.post_vars.categoria_edit,
            "cargo" : request.post_vars.cargo_edit,
            "fecha_ingreso" : request.post_vars.fecha_ingreso_edit,
            "fecha_salida" : request.post_vars.fecha_salida_edit,
            "estatus" : request.post_vars.estatus_edit,
            "dependencia" : request.post_vars.dependencia_edit,
            "celular" : request.post_vars.celular_edit,
             "contacto_emergencia" : request.post_vars.contacto_emergencia_edit,
             "direccion" : request.post_vars.direccion_edit,
             "gremio" : request.post_vars.gremio_edit,
             "fecha_ingreso_usb" : request.post_vars.fecha_ingreso_usb_edit,
             "fecha_ingreso_ulab" : request.post_vars.fecha_ingreso_ulab_edit,
             "fecha_ingreso_admin_publica" : request.post_vars.fecha_ingreso_admin_publica_edit,
             "condicion" : request.post_vars.condicion_edit,
             "unidad_jerarquica_superior" : request.post_vars.unidad_jerarquica_superior_edit,
             "rol" : request.post_vars.rol_edit,
             "ubicacion" : request.post_vars.ubicacion_edit
            }

    #if str(edic) != "{'categoria': None, 'ci': None, 'estatus': None, 'pagina_web': None, 'cargo': None, 'dependencia': None, 'fecha_ingreso': None, 'fecha_salida': None, 'nombre': None, 'telefono': None, 'email': None}": 
    #Si el diccionario no esta vacio
    if (not(None in edic.values())):

        #Eliminamos la instancia anterior
        db(db.t_Personal.f_ci == edic["ci"]).delete()
        #Insertamos en la base de datos
        db.t_Personal.insert(f_nombre = edic["nombre"],
                                f_ci = edic["ci"],
                                f_apellido = edic["apellido"],
                                f_email = edic["email"],
                                f_telefono = edic["telefono"],
                                f_pagina_web = edic["pagina_web"],
                                f_categoria = edic["categoria"],
                                f_cargo = edic["cargo"],
                                f_fecha_ingreso = edic["fecha_ingreso"],
                                f_fecha_salida = edic["fecha_salida"],
                                f_estatus = edic["estatus"],
                                f_dependencia = edic["dependencia"],
            f_celular= dic["celular"],
            f_contacto_emergencia= dic["contacto_emergencia"],
            f_direccion= dic["direccion"],
            f_gremio= dic["gremio"],
            f_fecha_ingreso_usb= dic["fecha_ingreso_usb"],
            f_fecha_ingreso_ulab= dic["fecha_ingreso_ulab"],
            f_fecha_ingreso_admin_publica= dic["fecha_ingreso_admin_publica"],
            f_condicion= dic["condicion"],
            f_unidad_jerarquica_superior= dic["unidad_jerarquica_superior"],
            f_rol = dic["rol"],
            f_ubicacion= dic["ubicacion"]
                                )
                                
        redirect(URL('listado'))

def index():
    return dict()

def lista():
    form = SQLFORM.smartgrid(db.t_Personal, links_in_grid=False)
    
    return locals()

#Creamos la clase usuario que contiene la informacion del usuario que se entregara a la vista 
class Usuario(object):
    nombre = ""
    apellido = ""
    correo = ""
    rol = ""
    dependencia = ""
    unidad_adscripcion = ""
    ubicacion = ""
    cedula = ""
    extension = ""


#Funcion que envia los datos a la vista
def listado():
    usuario = Usuario()
    #Obtenemos el usuario loggeado
    infoUsuario=(db(db.auth_user.id==auth.user.id).select(db.auth_user.ALL)).first()
    #infoUsuario=(db(db.auth_user.id==3).select(db.auth_user.ALL)).first()
    
    usuario.correo = infoUsuario.email
    usuario.nombre = infoUsuario.first_name
    usuario.apellido = infoUsuario.last_name
    usuario.cedula = (db(db.t_Personal.f_email==auth.user.email).select(db.t_Personal.ALL)).first().f_ci
    

    GrupoUsuario = (db(db.auth_membership.user_id==auth.user.id).select(db.auth_membership.ALL)).first()
    #GrupoUsuario = (db(db.auth_membership.user_id==3).select(db.auth_membership.ALL)).first()
    idGrupoUsuario = GrupoUsuario.group_id
    usuario.idGrupo=idGrupoUsuario
    usuario.rol= (db(db.auth_group.id == idGrupoUsuario).select(db.auth_group.ALL)).first().role
    
    idDependenciaUsuario= GrupoUsuario.dependencia_asociada
    usuario.dependencia = (db(db.dependencias.id == idDependenciaUsuario).select(db.dependencias.ALL)).first().nombre
    id_unidad_adscripcion = (db(db.t_Personal.f_email==auth.user.email).select(db.t_Personal.ALL)).first().f_unidad_jerarquica_superior
    usuario.unidad_adscripcion = (db(db.dependencias.id == id_unidad_adscripcion).select(db.dependencias.ALL)).first().nombre 
    usuario.ubicacion = (db(db.dependencias.id == idDependenciaUsuario).select(db.dependencias.ALL)).first().codigo_registro
    
    
    #Obtenemos los datos para el listado
    tabla = tabla_categoria()

    #Obtenemos los elementos de los dropdowns
    temp = dropdowns()
    gremios = temp[0]
    dependencias = temp[1]
    estados = temp[2]
    categorias = temp[3]
    condiciones = temp[4]

    editar = []
    cedit = request.vars.cedula_editar
    if (cedit != None):
        editar.append(cedit)
        editdata = db(db.t_Personal.f_ci == cedit).select(db.t_Personal.ALL)
        edic = {"nombre" : editdata[0].f_nombre,
            "apellido" : editdata[0].f_apellido,
            "ci" : editdata[0].f_ci,
            "email" : editdata[0].f_email,
            "telefono" : editdata[0].f_telefono,
            "pagina_web" : editdata[0].f_pagina_web,
            "categoria" : editdata[0].f_categoria,
            "cargo" : editdata[0].f_cargo,
            "fecha_ingreso" : editdata[0].f_fecha_ingreso,
            "fecha_salida" : editdata[0].f_fecha_salida,
            "estatus" : editdata[0].f_estatus,
            "dependencia" : editdata[0].f_dependencia,
            "gremio" : editdata[0].f_gremio
            }
    else:
        edic = {"nombre" :usuario.nombre,
            "apellido" :None,
            "ci" :None,
            "email" :None,
            "telefono" :None,
            "pagina_web" :None,
            "categoria" :None,
            "cargo" :None,
            "fecha_ingreso" :None,
            "fecha_salida" :None,
            "estatus" :None,
            "dependencia" : None,
            "gremio" : None
            }

    #Agregamos los datos del formulario a la base de datos
    add_form()

    #Agregamos los datos del formulario a la base de datos
    edit_form()

    #Obtenemos la cedula del usuario desde el boton de eliminar
    ced = request.vars.cedula_eliminar
    if (ced != None):
        db(db.t_Personal.f_ci == ced).delete()
        redirect(URL('listado'))

    return dict(gridedit = edic, editar = editar, grid= tabla, categorias = categorias,dependencias = dependencias, estados = estados, gremios=gremios, condiciones = condiciones, usuario=usuario)

def reporte():
    tabla=tabla_categoria()
    personas=[]
    for persona in tabla:
        personas.append(persona)
    return dict(personas=personas)

# def reporte(tipo,filtro):
#     tabla=tabla_categoria()
#     personas=[]
#     if (tipo=="categoria"):
#         for persona in tabla:
#             if (persona["categoria"]==filtro):
#                 personas.append(persona)
#     elif (tipo=="dependencia"):
#         named = db(db.dependencias.id == filtro).select(db.dependencias.ALL)
#         dep= named[0] if len(named) > 0 else None
#         for persona in tabla:
#             if (persona["dependencia"]==dep)
#                 personas.append(persona)
#     else:
#         for persona in tabla:
#             personas.append(persona)
#     return dict(personas=personas)
