# -------------------------------------------------------------------------
# Controladores Basicos
# - index sera la accion basica de la aplicacion donde se muestran los modulos de SMyDP, Personal y servicios
#
# - download y call son ejemplos de aplicaciones basicas de web2py.
# -------------------------------------------------------------------------

# Pagina principal
@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
    val = contar_validaciones()
    session.validaciones_pendientes = val
    try:
        session.ficha_negada = db(db.t_Personal.f_email == auth.user.email).select(db.t_Personal.f_comentario).first().f_comentario
    except:
        pass
    session.prestamo_rechazado = _obtener_prestamo_rechazado()
    return dict()

def register():
    return redirect(URL('modulos','register'))

def recoverpassword():
    return dict(form=auth.reset_password())

# Inicio de Sesion
def login():
    return redirect(URL('modulos', 'login', vars=dict(error='invalid_data')))

# Devuelve el primer préstamo rechazado no notificado
def _obtener_prestamo_rechazado():

    def _obtener_registro_de_prestamo(id_prestamo):

        # El formato dado es:
        # SIG-DDDD/AA-NNN
        #
        # Donde:
        #   DDDD:   Código de dependencia
        #   AA:     Últimos dos dígitos del año de la solicitud
        #   NNN:    Identificador único numérico de la solicitud (3 dígitos)

        prestamo = db(db.historial_prestamo_vh.id == id_prestamo).select().first()
        vehiculo = db(db.vehiculo.id == prestamo['hpvh_vh_id']).select().first()
        dependencia = db(db.dependencias.id == vehiculo['vh_dependencia']).select().first()

        registro = "SIG"
        registro += "-"

        registro += str(dependencia['codigo_registro'])
        registro += "/"
        registro += str(prestamo['hpvh_fecha_solicitud'].year)[2:]
        registro += "-"
        registro += str(prestamo['id']).zfill(3)

        return registro

    user_id = auth.user.id

    prestamos_rechazados = db((db.historial_prestamo_vh.hpvh_estatus == "Denegada") & (db.historial_prestamo_vh.hpvh_solicitante == user_id) & (db.historial_prestamo_vh.hpvh_rechazo_notificado == False)).select()
    if len(prestamos_rechazados) == 0:
        return None
    else:
        prestamo = prestamos_rechazados.first()
        registro = _obtener_registro_de_prestamo(prestamo.id)
        session.registro_prestamo = registro

        db(db.historial_prestamo_vh.id == prestamo.id).update(
            hpvh_rechazo_notificado = True
        )

        session.flash = "La solicitud de préstamo {{= session.registro_prestamo }} ha sido denegada."
        return prestamo


def contar_validaciones():
    usuario =db(db.t_Personal.f_email == auth.user.email).select(db.t_Personal.ALL)
    if(len(usuario)>1): usuario = usuario[1]
    else: usuario = usuario.first()
    try:
        es_supervisor = usuario.f_es_supervisor
    except:
        es_supervisor = False
    dependencia = None
    if es_supervisor:
        if(auth.user.email == "sigulabusb@gmail.com") or (auth.user.email == "asis-ulab@usb.ve"):
            notif = db(db.t_Personal.f_por_validar == True).count()
        else:
            dependencia = usuario.f_dependencia
            notif = db((db.t_Personal.f_dependencia == dependencia)&(db.t_Personal.f_es_supervisor == False)&(db.t_Personal.f_por_validar == True)).count()
    else: notif = 0
    return notif

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
