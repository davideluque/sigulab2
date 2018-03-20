#-----------------------------------------------------------------------------
# Controladores provisionales utilizados solo para probar las vistas del modulo de SMyDP
#
# - Samuel Arleo <saar1312@gmail.com>
#-----------------------------------------------------------------------------


@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
    return locals()


@auth.requires_login(otherwise=URL('modulos', 'login'))
def sustancias():
    return locals()

# Determina si el id de la dependencia es valido. Retorna False si el id no existe
# o es de un tipo incorrecto
def is_valid_id(id_, tabla):
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
def is_bool(bool_var):
    if not bool_var in ['True', 'False']:
        return False
    else:
        return True

# Dado el nombre de una dependencia, retorna el id de esta si la encuentra o
# None si no lo hace
def find_dep_id(dependencias, nombre):

    dep_id = None
    encontrado = False
    k = 0
    while not encontrado and k < len(dependencias):
        if dependencias[k].nombre == nombre:
            encontrado = True
            dep_id = dependencias[k].id
        k = k+1
    return dep_id

# Dado el id de una depencia y conociendo si es un espacio fisico o una dependencia
# comun, determina si el usuario tiene privilegios suficientes para obtener informacion
# de esta
def acceso_permitido(dep_id, es_espacio):
    
    permitido = False

    # dep_actual es un apuntador que permitira recorrer la jerarquia de dependencias
    # desde dep_id hasta usuario_dep. Si dep_actual no encuentra usuario_dep 
    # entonces se esta tratando de acceder a una dependencia sin permisos suficientes
    dep_actual = dep_id

    # Obteniendo la entrada en t_Personal del usuario conectado
    user_id = auth.user.id
    user = db.t_Personal(db.t_Personal.id == user_id)

    # Si el usuario es tecnico se busca en la tabla de es_encargado si el usuario 
    # es encargado del espacio con id dep_id
    if user.f_cargo == 'TÉCNICO':
        pass

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
        direccion_id = find_dep_id(dependencias, 'DIRECCIÓN')

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
@auth.requires_login(otherwise=URL('modulos', 'login'))
def inventarios():
    
    # Inicializando listas de espacios fisicos y dependencias
    espacios = []
    dependencias = []
    dep_nombre = ""
    es_espacio = False

    if auth.has_membership("TÉCNICO"):
        # Si el tecnico ha seleccionado un espacio fisico
        if request.vars.dependencia:

            # Evaluando la correctitud de los parametros del GET 
            if not (is_valid_id(request.vars.dependencia, db.dependencias) and
                    is_bool(request.vars.es_espacio)):
                redirect(URL('inventarios'))

            # Se muestra solo el inventario de ese espacio y no se muestran mas
            # dependencias pues ya se alcanzo el nivel mas bajo de la jerarquia 
            # de dependencias
            pass
        # Si el tecnico no ha seleccionado un espacio sino que acaba de entrar
        # a la opcion de inventarios
        else:
            # Se muestran los espacios fisicos que tiene el tecnico a cargo
            pass
    # Si el usuario no es tecnico, para la base de datos es indiferente su ROL
    # pues la jerarquia de dependencias esta almacenada en la misma tabla
    # con una lista de adyacencias
    else:
        # Si el usuario ha seleccionado una dependencia o un espacio fisico
        if request.vars.dependencia:

            bool2 = is_valid_id(request.vars.dependencia, db.dependencias)
            bool1 = is_bool(request.vars.es_espacio)

            # Evaluando la correctitud de los parametros del GET 
            if not (is_valid_id(request.vars.dependencia, db.dependencias) and
                    is_bool(request.vars.es_espacio)):
                redirect(URL('inventarios'))

            # Determinando si el usuario tiene privilegios suficientes para
            # consultar la dependencia en request.vars.dependencia
            if not acceso_permitido(int(request.vars.dependencia), request.vars.es_espacio):
                redirect(URL('inventarios'))

            if request.vars.es_espacio == "True":
                # Se muestra el inventario del espacio
                espacio_id = request.vars.dependencia
                dep_nombre = db.espacios_fisicos(db.espacios_fisicos.id == espacio_id).nombre

            else:
                # Se muestran las dependencias que componen a esta dependencia padre
                # y se lista el inventario agregado
                dep_id = request.vars.dependencia
                dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre
                dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id).select(
                                                                          db.dependencias.ALL))
                # Si la lista de dependencias es vacia, entonces la dependencia no 
                # tiene otras dependencias por debajo (podria tener espacios fisicos
                # o estar vacia)
                if len(dependencias) == 0:
                    # Buscando espacios fisicos que apunten a la dependencia escogida
                    espacios = list(db(db.espacios_fisicos.dependencia == dep_id).select(
                                                                db.espacios_fisicos.ALL))
                    es_espacio = True

        else:

            # Obteniendo la entrada en t_Personal del usuario conectado
            user_id = auth.user.id
            user = db.t_Personal(db.t_Personal.id == user_id)

            # Dependencia a la que pertenece el usuario o que tiene a cargo
            dep_id = user.f_dependencia
            dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre

            # Se muestran las dependencias que componen a la dependencia que
            # tiene a cargo el usuario y el inventario agregado de esta
            dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id).select(
                                                                      db.dependencias.ALL))

        return dict(dep_nombre=dep_nombre, 
                    dependencias=dependencias, 
                    espacios=espacios, 
                    es_espacio=es_espacio)


@auth.requires_login(otherwise=URL('modulos', 'login'))
def desechos():
    return locals()

#-------------------------------------- Catalogo ---------------------------------------

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

