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
        jsns.append(
            {"nombre" : elm.f_nombre,
            "ci" : elm.f_ci,
            "email" : elm.f_email,
            "telefono" : elm.f_telefono,
            "pagina_web" : elm.f_pagina_web,
            "categoria" : elm.f_categoria,
            "cargo" : elm.f_cargo,
            "fecha_ingreso" : elm.f_fecha_ingreso,
            "fecha_salida" : elm.f_fecha_salida,
            "estatus" : elm.f_estatus,
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
            "ci" : request.post_vars.ci_add,
            "email" : request.post_vars.email_add,
            "telefono" : request.post_vars.telefono_add,
            "pagina_web" : request.post_vars.pagina_web_add,
            "categoria" : request.post_vars.categoria_add,
            "cargo" : request.post_vars.cargo_add,
            "fecha_ingreso" : request.post_vars.fecha_ingreso_add,
            "fecha_salida" : request.post_vars.fecha_salida_add,
            "estatus" : request.post_vars.estatus_add,
            #"dependencia" : request.post_vars.dependencia_add
            }

    #if str(dic) != "{'categoria': None, 'ci': None, 'estatus': None, 'pagina_web': None, 'cargo': None, 'dependencia': None, 'fecha_ingreso': None, 'fecha_salida': None, 'nombre': None, 'telefono': None, 'email': None}": 

    #Si el diccionario no esta vacio
    if (not(None in dic.values())):

        #Insertamos en la base de datos
        db.t_Personal.insert(f_nombre = dic["nombre"],
                                f_ci = dic["ci"],
                                f_email = dic["email"],
                                f_telefono = dic["telefono"],
                                f_pagina_web = dic["pagina_web"],
                                f_categoria = dic["categoria"],
                                f_cargo = dic["cargo"],
                                f_fecha_ingreso = dic["fecha_ingreso"],
                                f_fecha_salida = dic["fecha_salida"],
                                f_estatus = dic["estatus"]
                                #f_dependencia = dic["dependencia"]
                                )
        redirect(URL('index'))

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
    #Agregamos los datos del formulario a la base de datos
    add_form()

    datos_basicos = {}

    #Obtenemos la cedula del usuario
    ced = request.vars.cedula_modal
    if (ced != None):
        #Buscamos la tabla personal que posee esta cedula
        pers = db(db.t_Personal.f_ci == ced).select(db.t_Personal.ALL)
        print(ced)
        #Creamos una instancia con los valores para enviar a la ficha
        datos_basicos = {"nombre" : pers[0].f_nombre,
                        "ci" : ced,
                        "email" : pers[0].f_email,
                        "telefono" : pers[0].f_telefono,
                        "pagina_web" : pers[0].f_pagina_web,
                        "categoria" : pers[0].f_categoria,
                        "cargo" : pers[0].f_cargo,
                        "fecha_ingreso" : pers[0].f_fecha_ingreso,
                        "fecha_salida" : pers[0].f_fecha_salida,
                        "estatus" : pers[0].f_estatus
                        #"dependencia" : pers[0].f_dependencia_add
                        }
    else:
        datos_basicos = {"nombre" : None,
                "ci" : ced,
                "email" : None,
                "telefono" : None,
                "pagina_web" : None,
                "categoria" : None,
                "cargo" : None,
                "fecha_ingreso" : None,
                "fecha_salida" : None,
                "estatus" : None
                #"dependencia" : None
                }

    return dict(basicos = datos_basicos, grid= tabla, categorias = cat,dependencias = dep, estados = est)