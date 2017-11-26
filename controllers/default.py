# -------------------------------------------------------------------------
# Controladores Basicos
# - index sera la accion basica de la aplicacion.
#
# - download y call son ejemplos de aplicaciones basicas de web2py.
# -------------------------------------------------------------------------

def register():
    return redirect(URL('modulos','register'))

# Pagina principal (Boton de SMDP y otros modulos)
def index():
    return dict()

def recoverpassword():
    return dict(form=auth.reset_password())

# Inicio de Sesion
def login():
    return redirect(URL('modulos', 'login', vars=dict(error='1')))

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
