# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# Controladores provisionales utilizados solo para probar las vistas del modulo de SMyDP
#
# - Samuel Arleo <saar1312@gmail.com>
# 
# - Convenciones:
# * Funciones "privadas" utilizadas por los controladores y decoradores tienen el
# prefijo "__"
# * Controladores no poseen prefijos
#
#-----------------------------------------------------------------------------



# Verifica si el usuario que intenta acceder al controlador tiene alguno de los
# roles necesarios
def __check_role():

    roles_permitidos = ['WEBMASTER', 'DIRECTOR', 'ASISTENTE DEL DIRECTOR', 
                        'JEFE DE LABORATORIO', 'JEFE DE SECCIÓN', 'TÉCNICO', 
                        'GESTOR DE SMyDP']
    return True in map(lambda x: auth.has_membership(x), roles_permitidos)


@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
    return locals()


@auth.requires_login(otherwise=URL('modulos', 'login'))
def sustancias():
    return locals()

# Determina si el id de la dependencia es valido. Retorna False si el id no existe
# o es de un tipo incorrecto
def __is_valid_id(id_, tabla):
    try:
        int(id_)
    except:
        return False
    # Si el id recibido tiene el tipo correcto pero no existe en la base de datos
    if not db(tabla.id == int(id_)).select():
        return False

    return True

# Determina si una variable "booleana" pasada como parametro con GET es realmente
# 'True' o 'False' (request.vars almacena todo como strings)
def __is_bool(bool_var):
    if not bool_var in ['True', 'False']:
        return False
    else:
        return True

# Dado el nombre de una dependencia, retorna el id de esta si la encuentra o
# None si no lo hace
def __find_dep_id(dependencias, nombre):

    dep_id = None
    encontrado = False
    k = 0
    while not encontrado and k < len(dependencias):
        if dependencias[k].nombre == nombre:
            encontrado = True
            dep_id = dependencias[k].id
        k = k+1
    return dep_id


# Dado el id de un espacio fisico, retorna las sustancias que componen el inventario
# de ese espacio. Si ningun id es indicado, pero si el de una dependencia, busca
# todos los espacios fisicos que pertenecen a esta, agrega los inventarios y retorna
# la lista
def __get_inventario(espacio_id=None, dep_id=None):
    inventario = []
    if espacio_id:
        inventario = list(db((db.t_Inventario.sustancia == db.t_Sustancia.id) & 
                             (db.t_Inventario.espacio == espacio_id)).select())

    return inventario

# Dado el id de un espacio fisico, retorna los desechos peligrosos que componen el inventario
# de ese espacio. Si ningun id es indicado, pero si el de una dependencia, busca
# todos los espacios fisicos que pertenecen a esta, agrega los inventarios y retorna
# la lista
def __get_inventario_desechos(espacio_id=None, dep_id=None):
    inventario = []
    if espacio_id:
        inventario = list(db(db.desechos.espacio_fisico == espacio_id).select(db.desechos.ALL))
    
    return inventario


# Registra una nueva sustancia en el espacio fisico indicado. Si la sustancia ya
# existe en el inventario, genera un mensaje con flash y no anade de nuevo la
# sustancia. 
def __agregar_sustancia(espacio, sustancia_id, total, excedente, unidad_id):

    # Si ya existe la sustancia en el inventario
    if db((db.t_Inventario.espacio == espacio.id) & 
          (db.t_Inventario.sustancia == sustancia_id)).select():
        sust = db(db.t_Sustancia.id == sustancia_id).select()[0]

        #response.flash = "La sustancia \"{0}\" ya ha sido ingresada anteriormente \
        #                  en el espacio \"{1}\".".format(sust.f_nombre, espacio.nombre)
        return False

    db.t_Inventario.insert(f_existencia=total, 
                           f_uso_interno=float(total)-float(excedente),
                           f_medida=unidad_id,
                           espacio=espacio.id,
                           sustancia=sustancia_id)

    return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 

# Dado el id de una depencia y conociendo si es un espacio fisico o una dependencia
# comun, determina si el usuario tiene privilegios suficientes para obtener informacion
# de esta
def __acceso_permitido(user, dep_id, es_espacio):
    """
    Args:
        * user_id (str): id del usuario en la tabla t_Personal (diferente de auth.user.id)
        * dep_id (str): id de la dependencia a la cual pertenece el recurso que se 
            desea acceder
        * es_espacio (str): 'True' si el usuario viene de seleccionar un espacio 
            fisico
    """
    # Valor a retornar que determina si el usuario tiene o no acceso al recurso
    permitido = False

    # dep_actual es un apuntador que permitira recorrer la jerarquia de dependencias
    # desde dep_id hasta usuario_dep. Si dep_actual no encuentra usuario_dep 
    # entonces se esta tratando de acceder a una dependencia sin permisos suficientes
    dep_actual = dep_id

    # Si el usuario es tecnico se busca en la tabla de es_encargado si el usuario 
    # es encargado del espacio con id dep_id
    if auth.has_membership("TÉCNICO"):
        encargado = db(db.es_encargado.espacio_fisico == dep_id).select().first()
        if encargado:
            permitido = encargado.tecnico == user.id

    else:
        # Dependencia a la que pertenece el usuario o que tiene a cargo
        usuario_dep = user.f_dependencia

        # Buscando todas las dependencias para conocer la lista de adyacencias con
        # la jerarquia de la ULAB
        dependencias = db(db.dependencias.id > 0).select(
                                db.dependencias.nombre,
                                db.dependencias.id,
                                db.dependencias.unidad_de_adscripcion)

        # Creando lista de adyacencias
        lista_adyacencias = {row.id: row.unidad_de_adscripcion for row in dependencias}

        # Buscando el id de la direccion para saber si ya se llego a la raiz
        direccion_id = __find_dep_id(dependencias, 'DIRECCIÓN')

        # Si dep_id es un espacio fisico, se sube un nivel en la jerarquia (hasta
        # las secciones) ya que los espacios fisicos no aparecen en la lista de 
        # adyacencias pero si las secciones a las que pertenecen
        if es_espacio == "True":
            dep_actual = db(db.espacios_fisicos.id == dep_id).select().first().dependencia

        while dep_actual is not None:

            # Si en el camino hacia la raiz se encontro la dependencia a la que
            # pertenece el usuario, entonces si hay privilegios suficientes
            if dep_actual == usuario_dep:
                permitido = True
                break
            # Si ya se llego a la raiz, terminar el while
            if dep_actual == direccion_id:
                break
            else:
                dep_actual = lista_adyacencias[dep_actual] 

    return permitido

# Muestra el inventario de acuerdo al cargo del usuario y la dependencia que tiene
# a cargo

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def inventarios():

    # Inicializando listas de espacios fisicos y dependencias
    espacios = []
    dependencias = []
    dep_nombre = ""
    dep_padre_id = ""
    dep_padre_nombre = ""

    # Lista de sustancias en el inventario de un espacio fisico o que componen 
    # el inventario agregado de una dependencia
    inventario = []
    
    # Lista de sustancias en el catalogo
    sustancias = []

    # Lista de unidades de medida
    unidades_de_medida = list(db(db.t_Unidad_de_medida.id > 0).select())

    # Esta variable es enviada a la vista para que cuando el usuario seleccione 
    # un espacio fisico, se pase por GET es_espacio = "True". No quiere decir
    # que la dependencia seleccionada sea un espacio, sino que la siguiente
    # dependencia visitada sera un espacio fisico
    es_espacio = False

    # Permite saber si actualmente se esta visitando un espacio fisico (True)
    # o una dependencia (False)
    espacio_visitado = False
    
    es_tecnico = auth.has_membership("TÉCNICO")
    direccion_id = __find_dep_id(dependencias, 'DIRECCIÓN')

    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    user_dep_id = user.f_dependencia

    if auth.has_membership("TÉCNICO"):
        # Si el tecnico o jefe de seccion ha seleccionado un espacio fisico
        if request.vars.dependencia:

            # Evaluando la correctitud de los parametros del GET 
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('inventarios'))

            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('inventarios'))

            dep_nombre = db(db.espacios_fisicos.id == request.vars.dependencia
                           ).select().first().nombre

            espacio_visitado = True
            # Se muestra solo el inventario de ese espacio y no se muestran mas
            # dependencias pues ya se alcanzo el nivel mas bajo de la jerarquia 
            # de dependencias

        # Si el tecnico o jefe no ha seleccionado un espacio sino que acaba de 
        # entrar a la opcion de inventarios
        else:
            # Buscando espacios fisicos que tengan a user_id como encargado en 
            # la tabla 'es_encargado'
            espacios = list(db(
                    (db.es_encargado.tecnico == user_id) & 
                    (db.es_encargado.espacio_fisico == db.espacios_fisicos.id)
                              ).select(db.espacios_fisicos.ALL))
            es_espacio = True

    elif auth.has_membership("JEFE DE SECCIÓN"):
                # Si el tecnico o jefe de seccion ha seleccionado un espacio fisico
        if request.vars.es_espacio == 'True':
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('inventarios'))

            # Evaluando la correctitud de los parametros del GET 
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('inventarios'))

            dep_nombre = db(db.espacios_fisicos.id == request.vars.dependencia
                           ).select().first().nombre

            # Guardando el ID y nombre de la dependencia a la que pertenece el 
            # espacio fisico visitado
            dep_padre_id = db(db.espacios_fisicos.id == request.vars.dependencia
                             ).select().first().dependencia
            dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                 ).select().first().nombre

            espacio_visitado = True
            # Se muestra solo el inventario de ese espacio y no se muestran mas
            # dependencias pues ya se alcanzo el nivel mas bajo de la jerarquia 
            # de dependencias

        # Si el tecnico o jefe no ha seleccionado un espacio sino que acaba de 
        # entrar a la opcion de inventarios
        elif request.vars.es_espacio == 'False':
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                    redirect(URL('inventarios'))
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('inventarios'))
            espacios = list(db(
                              db.espacios_fisicos.dependencia == user_dep_id
                              ).select(db.espacios_fisicos.ALL))
            dep_nombre = db(db.dependencias.id == user_dep_id
                           ).select().first().nombre

            es_espacio = True                        

        else:
            espacios = list(db(
                              db.espacios_fisicos.dependencia == user_dep_id
                              ).select(db.espacios_fisicos.ALL))
            dep_nombre = db(db.dependencias.id == user_dep_id
                           ).select().first().nombre

            es_espacio = True

    # Si el usuario no es tecnico, para la base de datos es indiferente su ROL
    # pues la jerarquia de dependencias esta almacenada en la misma tabla
    # con una lista de adyacencias
    else:
        # Si el usuario ha seleccionado una dependencia o un espacio fisico
        if request.vars.dependencia:

            # Evaluando la correctitud de los parametros del GET 
            if not (__is_valid_id(request.vars.dependencia, db.dependencias) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('inventarios'))

            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('inventarios'))

            if request.vars.es_espacio == "True":
        
                # Se muestra el inventario del espacio
                espacio_id = request.vars.dependencia
                espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                dep_nombre = espacio.nombre

                # Guardando el ID y nombre de la dependencia padre para el link 
                # de navegacion de retorno
                dep_padre_id = db(db.espacios_fisicos.id == request.vars.dependencia
                                    ).select().first().dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre

                espacio_visitado = True

                # Se muestra la lista de sustancias que tiene en inventario
                inventario = __get_inventario(espacio_id)

                sustancias = list(db(db.t_Sustancia.id > 0).select(db.t_Sustancia.ALL))

                # Si se esta agregando una nueva sustancia, se registra en la DB
                if request.vars.sustancia:
                    __agregar_sustancia(espacio,
                                        request.vars.sustancia, 
                                        request.vars.total,
                                        request.vars.excedente,
                                        request.vars.unidad)

            else:
                # Se muestran las dependencias que componen a esta dependencia padre
                # y se lista el inventario agregado
                dep_id = request.vars.dependencia
                dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre
                dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                      ).select(db.dependencias.ALL))
                # Si la lista de dependencias es vacia, entonces la dependencia no 
                # tiene otras dependencias por debajo (podria tener espacios fisicos
                # o estar vacia)
                if len(dependencias) == 0:
                    # Buscando espacios fisicos que apunten a la dependencia escogida
                    espacios = list(db(db.espacios_fisicos.dependencia == dep_id
                                      ).select(db.espacios_fisicos.ALL))
                    es_espacio = True

                # Guardando el ID y nombre de la dependencia padre para el link 
                # de navegacion de retorno
                dep_padre_id = db(db.dependencias.id == request.vars.dependencia
                                 ).select().first().unidad_de_adscripcion
                # Si dep_padre_id es None, se ha llegado al tope de la jerarquia
                # y no hay un padre de este nodo
                if dep_padre_id:
                    dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                         ).select().first().nombre

        else:
            # Dependencia a la que pertenece el usuario o que tiene a cargo
            dep_id = user.f_dependencia
            dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre

            # Se muestran las dependencias que componen a la dependencia que
            # tiene a cargo el usuario y el inventario agregado de esta
            dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                  ).select(db.dependencias.ALL))

    return dict(dep_nombre=dep_nombre, 
                dependencias=dependencias, 
                espacios=espacios, 
                es_espacio=es_espacio,
                espacio_visitado=espacio_visitado,
                dep_padre_id=dep_padre_id,
                dep_padre_nombre=dep_padre_nombre,
                direccion_id=direccion_id,
                es_tecnico=es_tecnico,
                inventario=inventario,
                sustancias=sustancias,
                unidades_de_medida=unidades_de_medida)

@auth.requires(lambda: __check_role())
@auth.requires_login(otherwise=URL('modulos', 'login'))
def inventarios_desechos():

    # Inicializando listas de espacios fisicos y dependencias
    espacios = []
    dependencias = []
    dep_nombre = ""
    dep_padre_id = ""
    dep_padre_nombre = ""

    # Lista de desechos en el inventario de un espacio fisico o que componen 
    # el inventario agregado de una dependencia
    inventario = []
    
    # Lista de sustancias en el catalogo
    desechos = []

    # Lista de unidades de medida
    unidades_de_medida = list(db(db.t_Unidad_de_medida.id > 0).select())

    # Esta variable es enviada a la vista para que cuando el usuario seleccione 
    # un espacio fisico, se pase por GET es_espacio = "True". No quiere decir
    # que la dependencia seleccionada sea un espacio, sino que la siguiente
    # dependencia visitada sera un espacio fisico
    es_espacio = False

    # Permite saber si actualmente se esta visitando un espacio fisico (True)
    # o una dependencia (False)
    espacio_visitado = False
    
    es_tecnico = auth.has_membership("TÉCNICO")
    direccion_id = __find_dep_id(dependencias, 'DIRECCIÓN')

    # Obteniendo la entrada en t_Personal del usuario conectado
    user = db(db.t_Personal.f_usuario == auth.user.id).select()[0]
    user_id = user.id
    user_dep_id = user.f_dependencia

    if auth.has_membership("TÉCNICO"):
        # Si el tecnico o jefe de seccion ha seleccionado un espacio fisico
        if request.vars.dependencia:

            # Evaluando la correctitud de los parametros del GET 
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('inventarios'))

            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('inventarios'))

            dep_nombre = db(db.espacios_fisicos.id == request.vars.dependencia
                           ).select().first().nombre

            espacio_visitado = True
            # Se muestra solo el inventario de ese espacio y no se muestran mas
            # dependencias pues ya se alcanzo el nivel mas bajo de la jerarquia 
            # de dependencias

        # Si el tecnico o jefe no ha seleccionado un espacio sino que acaba de 
        # entrar a la opcion de inventarios
        else:
            # Buscando espacios fisicos que tengan a user_id como encargado en 
            # la tabla 'es_encargado'
            espacios = list(db(
                    (db.es_encargado.tecnico == user_id) & 
                    (db.es_encargado.espacio_fisico == db.espacios_fisicos.id)
                              ).select(db.espacios_fisicos.ALL))
            es_espacio = True

    elif auth.has_membership("JEFE DE SECCIÓN"):
                # Si el tecnico o jefe de seccion ha seleccionado un espacio fisico
        if request.vars.es_espacio == 'True':
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('inventarios'))

            # Evaluando la correctitud de los parametros del GET 
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('inventarios'))

            dep_nombre = db(db.espacios_fisicos.id == request.vars.dependencia
                           ).select().first().nombre

            # Guardando el ID y nombre de la dependencia a la que pertenece el 
            # espacio fisico visitado
            dep_padre_id = db(db.espacios_fisicos.id == request.vars.dependencia
                             ).select().first().dependencia
            dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                 ).select().first().nombre

            espacio_visitado = True
            # Se muestra solo el inventario de ese espacio y no se muestran mas
            # dependencias pues ya se alcanzo el nivel mas bajo de la jerarquia 
            # de dependencias

        # Si el tecnico o jefe no ha seleccionado un espacio sino que acaba de 
        # entrar a la opcion de inventarios
        elif request.vars.es_espacio == 'False':
            if not (__is_valid_id(request.vars.dependencia, db.espacios_fisicos) and
                    __is_bool(request.vars.es_espacio)):
                    redirect(URL('inventarios'))
            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('inventarios'))
            espacios = list(db(
                              db.espacios_fisicos.dependencia == user_dep_id
                              ).select(db.espacios_fisicos.ALL))
            dep_nombre = db(db.dependencias.id == user_dep_id
                           ).select().first().nombre

            es_espacio = True                        

        else:
            espacios = list(db(
                              db.espacios_fisicos.dependencia == user_dep_id
                              ).select(db.espacios_fisicos.ALL))
            dep_nombre = db(db.dependencias.id == user_dep_id
                           ).select().first().nombre

            es_espacio = True

    # Si el usuario no es tecnico, para la base de datos es indiferente su ROL
    # pues la jerarquia de dependencias esta almacenada en la misma tabla
    # con una lista de adyacencias
    else:
        # Si el usuario ha seleccionado una dependencia o un espacio fisico
        if request.vars.dependencia:

            # Evaluando la correctitud de los parametros del GET 
            if not (__is_valid_id(request.vars.dependencia, db.dependencias) and
                    __is_bool(request.vars.es_espacio)):
                redirect(URL('inventarios'))

            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not __acceso_permitido(user, 
                                int(request.vars.dependencia), 
                                    request.vars.es_espacio):
                redirect(URL('inventarios'))

            if request.vars.es_espacio == "True":
        
                # Se muestra el inventario del espacio
                espacio_id = request.vars.dependencia
                espacio = db(db.espacios_fisicos.id == espacio_id).select()[0]
                dep_nombre = espacio.nombre

                # Guardando el ID y nombre de la dependencia padre para el link 
                # de navegacion de retorno
                dep_padre_id = db(db.espacios_fisicos.id == request.vars.dependencia
                                    ).select().first().dependencia
                dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                    ).select().first().nombre

                espacio_visitado = True

                # Se muestra la lista de sustancias que tiene en inventario
                inventario = __get_inventario_desechos(espacio_id)

                desechos = list(db(db.desechos.id > 0).select(db.desechos.ALL))

                # Si se esta agregando una nueva sustancia, se registra en la DB
                if request.vars.sustancia:
                    __agregar_sustancia(espacio,
                                        request.vars.sustancia, 
                                        request.vars.total,
                                        request.vars.excedente,
                                        request.vars.unidad)

            else:
                # Se muestran las dependencias que componen a esta dependencia padre
                # y se lista el inventario agregado
                dep_id = request.vars.dependencia
                dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre
                dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                      ).select(db.dependencias.ALL))
                # Si la lista de dependencias es vacia, entonces la dependencia no 
                # tiene otras dependencias por debajo (podria tener espacios fisicos
                # o estar vacia)
                if len(dependencias) == 0:
                    # Buscando espacios fisicos que apunten a la dependencia escogida
                    espacios = list(db(db.espacios_fisicos.dependencia == dep_id
                                      ).select(db.espacios_fisicos.ALL))
                    es_espacio = True

                # Guardando el ID y nombre de la dependencia padre para el link 
                # de navegacion de retorno
                dep_padre_id = db(db.dependencias.id == request.vars.dependencia
                                 ).select().first().unidad_de_adscripcion
                # Si dep_padre_id es None, se ha llegado al tope de la jerarquia
                # y no hay un padre de este nodo
                if dep_padre_id:
                    dep_padre_nombre = db(db.dependencias.id == dep_padre_id
                                         ).select().first().nombre

        else:
            # Dependencia a la que pertenece el usuario o que tiene a cargo
            dep_id = user.f_dependencia
            dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre

            # Se muestran las dependencias que componen a la dependencia que
            # tiene a cargo el usuario y el inventario agregado de esta
            dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id
                                  ).select(db.dependencias.ALL))

    return dict(dep_nombre=dep_nombre, 
                dependencias=dependencias, 
                espacios=espacios, 
                es_espacio=es_espacio,
                espacio_visitado=espacio_visitado,
                dep_padre_id=dep_padre_id,
                dep_padre_nombre=dep_padre_nombre,
                direccion_id=direccion_id,
                es_tecnico=es_tecnico,
                inventario=inventario,
                desechos=desechos,
                unidades_de_medida=unidades_de_medida)



@auth.requires_login(otherwise=URL('modulos', 'login'))
def desechos():
    return locals()

#--------------------- Catalogo de Sustancias y Materiales ----------

@auth.requires_login(otherwise=URL('modulos', 'login'))
def catalogo():

    if(auth.has_membership('Gestor de SMyDP') or  auth.has_membership('WEBMASTER')):
        table = SQLFORM.smartgrid(  db.t_Sustancia, 
                                    onupdate=auth.archive,
                                    links_in_grid=False,
                                    csv=False,
                                    user_signature=True,
                                    paginate=10)

    else:
        table = SQLFORM.smartgrid(  db.t_Sustancia, 
                                    editable=False,
                                    deletable=False,
                                    csv=False,
                                    links_in_grid=False,
                                    create=False,
                                    paginate=10,
                                    showid=False)
    return locals()

