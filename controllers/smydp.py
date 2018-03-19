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

# Muestra el inventario de acuerdo al cargo del usuario y la dependencia que tiene
# a cargo
@auth.requires_login(otherwise=URL('modulos', 'login'))
def inventarios():

    # Obteniendo la fila del usuario conectado en t_Personal
    user_id = auth.user.id
    user = db.t_Personal(db.t_Personal.id == user_id)

    # Dependencia a la que pertenece el usuario o que tiene a cargo
    dep_id = user.f_dependencia
    dep_nombre = db.dependencias(db.dependencias.id == dep_id).nombre

    if auth.has_membership("TÉCNICO"):
        # Si el tecnico ha seleccionado un espacio fisico
        if request.post_vars.dependencia:
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
        # Si el usuario ha seleccionado una dependencia
        if request.post_vars.dependencia:
            # Se muestran las dependencias que componen a esta dependencia padre
            # y se lista el inventario agregado de estas
            pass
        else:
            # Se muestran las dependencias que componen a la dependencia que
            # tiene a cargo el usuario y el inventario agregado de esta
            dependencias = list(db(db.dependencias.unidad_de_adscripcion == dep_id).select(
                                                                      db.dependencias.ALL))

    return dict(dep_nombre=dep_nombre, dependencias=dependencias)


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

