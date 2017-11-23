#!/usr/bin/ python
# encoding=utf8  
#import sys  
  
#sys.setdefaultencoding('utf8')

#-------------------------------------
#
# Controladores integrados/en conjunto
#
#-------------------------------------

# Pagina, botones de eleccion entre nuestros modulos
# o SMDP

@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
    return dict()

@auth.requires_login(otherwise=URL('modulos', 'login'))
def sigulab2():
    return dict()

#-------------------------------------
# Autenticacion y manejo de cuenta
#-------------------------------------

# Inicio de Sesion
def login():
    if auth.user:
        return redirect(URL('index'))
    form=auth.login()
    return dict(form=form)

# Perfil de Usuario
@auth.requires_login(otherwise=URL('modulos', 'login'))
def editprofile():
    return dict(form=auth.profile(), form2=auth.change_password())

# Registro de usuarios- Incluye la creacion del rol
def register():
    if auth.user:
        return redirect(URL('index'))
    form=auth.register()
    roles=list(db(db.auth_group.role != 'WebMaster').select(db.auth_group.ALL))
    return dict(form=form, roles=roles)

# Ajax helper para crear una membership para el usuario recien registrado
def ajax_membership():
    depid = int(request.post_vars.laboratorio)
    rolid = int(request.post_vars.rol)


    if request.post_vars.seccion:
        depid = int(request.post_vars.seccion)

    user = db(db.auth_user.id > 0).select(db.auth_user.ALL)[-1]

    print(rolid, depid)
    print(user.id)
    db.auth_membership(user_id=user.id, group_id=rolid, dependencia_asociada=depid)
    return dict()

# Ajax Helper para la dependencia de acuerdo a su unidad de adscripcion
def ajax_unidad_rol():
    rolid = request.post_vars.dependenciahidden
    
    roltype = db(db.auth_group.id == int(rolid)).select(db.auth_group.ALL)[0].role
    direccion=db(db.dependencias.nombre == "Dirección").select(db.dependencias.ALL)
    labs_y_coordinaciones=list(db(db.dependencias.unidad_de_adscripcion == direccion[0].id).select(db.dependencias.ALL))
    labs = []
    coordinaciones = []
    for i in labs_y_coordinaciones:
        if "Laboratorio" in i.nombre:
            labs.append(i)
        else:
            coordinaciones.append(i)
    if roltype == "Director" or roltype == "Asistente del Director" or roltype == "Gestor de SMyDP":
        lista = direccion
    elif roltype == "Coordinador" or roltype == "Personal de Coordinación":
        lista = coordinaciones
    elif roltype == "WebMaster" or roltype == "Cliente Interno":
        lista = False
    else:
        lista = labs

    return(dict(lista=lista))

def ajax_registro_seccion():
    rolid = request.post_vars.dependenciahidden
    labid = request.post_vars.seccionhidden
    roltype = db(db.auth_group.id == int(rolid)).select(db.auth_group.ALL)[0].role
    secciones=False
    if roltype == "Técnico" or roltype == "Jefe de Sección":
        secciones=list(db(db.dependencias.unidad_de_adscripcion == int(labid)).select(db.dependencias.ALL))

    return dict(lista=secciones)


# Recuperacion de Contraseña (pedido) 
def resetpassword():
    site_url = URL(request.application, 'modulos', 'recoverpassword', host=True)
    # pagina indicada en el email
    auth.messages.reset_password = 'Por favor clickee el siguiente link ' + site_url + '/?key=' + '%(key)s para resetear su contraseña'
    form = auth.request_reset_password()
    return dict(form=form)

# Recuperacion de Contraseña (reinicio) 
def recoverpassword():
    return dict(form=auth.reset_password())

def logout():
    auth.logout()
    return redirect(URL('login'))
