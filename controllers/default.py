# -------------------------------------------------------------------------
# Controladores Basicos
# - index sera la accion basica de la aplicacion donde se muestran los modulos de SMyDP, Personal y servicios
#
# - download y call son ejemplos de aplicaciones basicas de web2py.
# -------------------------------------------------------------------------

# Pagina principal 
@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
    val = db(db.t_Personal.f_por_validar == True).count()
    session.validaciones_pendientes = val
    return dict()

def register():
    return redirect(URL('modulos','register'))

def recoverpassword():
    return dict(form=auth.reset_password())

# Inicio de Sesion
def login():
    return redirect(URL('modulos', 'login', vars=dict(error='invalid_data')))

#--------------------------------------
# Otras Funcionalidades Basicas
#--------------------------------------

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
