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

        dep= named[0] if len(named) > 0 else None

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
            "dependencia" : dep
             })
        
    return jsns

#Mandar informacion a los dropdowns
def dropdowns():

    #Dropdown de categoria
    cat = ['Docente', 'Administrativo', 'Técnico', 'Obrero']
    #Dropdown de dependencias
    dep = db(db.dependencias.nombre).select(db.dependencias.ALL)
    #Dropdown de estatus
    est = ['Activo', 'Jubilado', 'Retirado']

    return (cat,dep,est)

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
            "dependencia" : request.post_vars.dependencia_add
            }

    #if str(dic) != "{'categoria': None, 'ci': None, 'estatus': None, 'pagina_web': None, 'cargo': None, 'dependencia': None, 'fecha_ingreso': None, 'fecha_salida': None, 'nombre': None, 'telefono': None, 'email': None}": 

    #Si el diccionario no esta vacio
    if (not(None in dic.values())):

        #Insertamos en la base de datos
        db.t_Personal.insert(f_nombre = dic["nombre"],
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
                                f_dependencia = dic["dependencia"]
                                )
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
            "dependencia" : request.post_vars.dependencia_edit
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
                                f_dependencia = edic["dependencia"]
                                )
                                
        redirect(URL('listado'))

def index():
    return dict()

#Funcion que envia los datos a la vista
def listado():

    #Obtenemos los datos para el listado
    tabla = tabla_categoria()

    #Obtenemos los elementos de los dropdowns
    temp = dropdowns()
    cat = temp[0]
    dep = temp[1]
    est = temp[2]

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
            "dependencia" : editdata[0].f_dependencia
            }
    else:
        edic = {"nombre" :None,
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
            "dependencia" : None
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


    return dict(gridedit = edic, editar = editar, grid= tabla, categorias = cat,dependencias = dep, estados = est)