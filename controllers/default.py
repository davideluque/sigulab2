# -------------------------------------------------------------------------
# Controladores Basicos
# - index sera la accion basica de la aplicacion.
#
# - download y call son ejemplos de aplicaciones basicas de web2py.
# -------------------------------------------------------------------------

# Pagina principal (Boton de SMDP y otros modulos)
def index():
    
    message=auth.user
    message2=""
    if request.post_vars.rol:
        message2=request.post_vars.rol
    return dict(message=message, message2=message2)

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