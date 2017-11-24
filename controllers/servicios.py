from servicios_libreria import *

#------------------------------------------------------------------------------
#
# Controladores de las funcionalidades del modulo de Servicios
#
#------------------------------------------------------------------------------
import re

# Pagina principal del modulo
@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
    return dict()


@auth.requires_login(otherwise=URL('modulos', 'login'))
def usuario():
    return dict(form=auth.profile(), form2=auth.change_password())

# Tabla de servicios agregados
@auth.requires_login(otherwise=URL('modulos', 'login'))
def listado():

    #----- AGREGAR SERVICIO -----#

    if request.post_vars.nombreServicio and request.post_vars.envio != "edicion":

        docencia = False if not request.post_vars.docenciaServicio else True
        investigacion = False if not request.post_vars.investigacionServicio else True
        extension = False if not request.post_vars.extensionServicio else True
        gestion = False if not request.post_vars.gestionServicio else True

        servicio_nuevo = Servicio(db, request.post_vars.nombreServicio, request.post_vars.tipoServicio,
                   request.post_vars.categoriaServicio, request.post_vars.objetivoServicio,
                   request.post_vars.alcanceServicio, request.post_vars.metodoServicio,
                   request.post_vars.rangoServicio, request.post_vars.incertidumbreServicio,
                   request.post_vars.itemServicio, request.post_vars.requisitosServicio,
                   request.post_vars.resultadosServicio, docencia,
                   investigacion, gestion, extension, True,
                   request.post_vars.responsableServicio, request.post_vars.dependenciaServicio, 
                   request.post_vars.ubicacionServicio)

        servicio_nuevo.insertar()

    #----- FIN AGREGAR SERVICIO -----#

    #----- EDITAR SERVICIO -----#

    elif request.post_vars.nombreServicio and request.post_vars.envio == "edicion":
        
        docencia = False if not request.post_vars.docenciaServicio else True
        investigacion = False if not request.post_vars.investigacionServicio else True
        extension = False if not request.post_vars.extensionServicio else True
        gestion = False if not request.post_vars.gestionServicio else True      

        servicio_edicion = Servicio(db)
        servicio_edicion.instanciar(request.vars.idServicioEdit)

        servicio_edicion.editar(request.post_vars.nombreServicio, request.post_vars.tipoServicio,
                   request.post_vars.categoriaServicio, request.post_vars.objetivoServicio,
                   request.post_vars.alcanceServicio, request.post_vars.metodoServicio,
                   request.post_vars.rangoServicio, request.post_vars.incertidumbreServicio,
                   request.post_vars.itemServicio, request.post_vars.requisitosServicio,
                   request.post_vars.resultadosServicio, docencia,
                   investigacion, gestion, extension, True,
                   request.post_vars.responsableServicio, request.post_vars.dependenciaServicio, 
                   request.post_vars.ubicacionServicio)

        servicio_edicion.actualizar(request.vars.idServicioEdit)

        redirect(URL('listado?order=id1&page=1'))
    #----- FIN EDITAR SERVICIO -----#

    #----- COMIENZO EDITAR SERVICIO -----#

    if request.post_vars.edit and (request.post_vars.eliminar is None) and (request.post_vars.visibilidad is None):
        editar = db(db.servicios.id == request.vars.idFicha).select(db.servicios.ALL)
        
    else:
        editar = []

    #----- FIN COMIENZO EDITAR SERVICIO -----#

    #----- EDITAR VISIBILIDAD -----#

    if request.post_vars.visibilidad:
        db(db.servicios.id == request.post_vars.idFicha).update(
            visibilidad=eval(request.post_vars.visibilidad))

    #----- FIN EDITAR VISIBILIDAD -----#

    #----- ELIMINAR SERVICIO -----#
    if request.post_vars.eliminar:
        db(db.servicios.id == request.post_vars.idFicha).delete()

    #----- FIN ELIMINAR SERVICIO -----#


    #----- LISTAR SERVICIOS -----#

    listado_de_servicios = ListaServicios(db)

    if request.vars.pagina:
        listado_de_servicios.cambiar_pagina(int(request.vars.pagina))

    if request.vars.columna:
        listado_de_servicios.cambiar_columna(request.vars.columna)

    listado_de_servicios.orden_y_filtrado()
    firstpage=listado_de_servicios.boton_principio
    lastpage=listado_de_servicios.boton_fin
    nextpage=listado_de_servicios.boton_siguiente
    prevpage=listado_de_servicios.boton_anterior

    #----- FIN LISTAR SERVICIOS -----#

    return dict(grid=listado_de_servicios.servicios_a_mostrar,
                pages=listado_de_servicios.rango_paginas,
                actualpage=listado_de_servicios.pagina_central,
                nextpage=nextpage, prevpage=prevpage,
                firstpage=firstpage, lastpage=lastpage,
                categorias=listar_categorias(db), tipos=listar_tipos(db),
                sedes=listar_sedes(db), editar=editar)

#----- AGREGAR SOLICITUDES -----#

@auth.requires_login(otherwise=URL('modulos', 'login'))
def solicitudes():

    if request.post_vars.numRegistro :
        solicitud_nueva = Solicitudes(db, request.post_vars.numRegistro, request.post_vars.dependenciaSolicitante,
                        request.post_vars.jefeDependenciaSolicitante, request.post_vars.responsableSolicitud,
                        request.post_vars.categoriaServicio, request.post_vars.tipoServicio, request.post_vars.nombreServicio, 
                        request.post_vars.propositoServicio, request.post_vars.descripcionSolicitud, 
                        request.post_vars.dependenciaEjecutoraServicio, request.post_vars.jefeDependenciaEjecutoraServicios, 
                        request.post_vars.servicioElaboradoPor, request.post_vars.fechaElaboracion, request.post_vars.servicioAprobadoPor, 
                        request.post_vars.fechaAprobacion, request.post_vars.observaciones)

        solicitud_nueva.insertar()

    return dict(grid=[], controls=False)


@auth.requires_login(otherwise=URL('modulos', 'login'))
def certificaciones():

    # ---- ACCION DE CERTIFICACION DEL SERVICIO ----
    if request.post_vars.registro:
        registro = request.post_vars.registro
        proyecto = request.post_vars.proyecto
        elaborado_por = request.post_vars.usuarioid
        dependencia = request.post_vars.dependenciaid
        solicitud = request.post_vars.solicitudid
        fecha = request.post_vars.fecha

        certificado = Certificacion(db, registro, proyecto, elaborado_por, dependencia, solicitud, fecha)

        certificado.insertar()
    #-------------------FIN------------------------

    #------ ACCION LISTAR SOLICITUDES DE SERV -----

    listado_de_solicitudes = ListaSolicitudes(db)

    if request.vars.pagina:
        listado_de_solicitudes.cambiar_pagina(int(request.vars.pagina))

    if request.vars.columna:
        listado_de_solicitudes.cambiar_columna(request.vars.columna)

    listado_de_solicitudes.orden_y_filtrado()
    firstpage = listado_de_solicitudes.boton_principio
    lastpage = listado_de_solicitudes.boton_fin
    nextpage = listado_de_solicitudes.boton_siguiente
    prevpage = listado_de_solicitudes.boton_anterior

    # ----- FIN LISTAR SOLICITUDES -----#

    return dict(grid=listado_de_solicitudes.solicitudes_a_mostrar,
                pages=listado_de_solicitudes.rango_paginas,
                actualpage=listado_de_solicitudes.pagina_central,
                nextpage=nextpage, prevpage=prevpage,
                firstpage=firstpage, lastpage=lastpage,
                categorias=listar_categorias(db), tipos=listar_tipos(db),
                sedes=listar_sedes(db))




#------------------------------------------------------------------------------
#
# Controladores de los Ajax del modulo de Servicios
#
#------------------------------------------------------------------------------


@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_ficha_servicio():
    session.forget(response)

    # Servicio
    entrada = db(db.servicios.id == int(request.vars.serv)).select(db.servicios.ALL)


    # Funciones
    funcion = []
    if entrada[0].gestion:
        funcion.append("Gestión  ")
    else:
        funcion.append("")

    if entrada[0].docencia:
        funcion.append("Docencia  ")
    else:
        funcion.append("")

    if entrada[0].investigacion:
        funcion.append("Investigación  ")
    else:
        funcion.append("")

    if entrada[0].extension:
        funcion.append("Extensión  ")
    else:
        funcion.append("")

    valores_de_ficha = query_ficha(db, int(request.vars.serv))
    valores_de_ficha['funcion'] = funcion

    return dict(ficha=valores_de_ficha)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_adscripcion():
    session.forget(response)
    adscripcion_query = db((db.dependencias.id_sede == int(request.vars.sede))).select(db.dependencias.ALL)
    dependencias_a_mostrar = []

    for l in adscripcion_query:
        if re.match( r'Laboratorio\s[A-G]', l.nombre) or (l.id == 1):
            dependencias_a_mostrar.append(l)
    return dict(dependencias=dependencias_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_dependencia():
    session.forget(response)
    dependencia_query = db((db.dependencias.unidad_de_adscripcion == int(request.vars.adscripcion))).select(db.dependencias.ALL)
    dependencias_a_mostrar = []

    for l in dependencia_query:
        if (re.match( r'Laboratorio\s[A-G]', l.nombre)) == None:
            dependencias_a_mostrar.append(l)
    return dict(dependencias=dependencias_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_ubicacion():
    session.forget(response)
    ubicacion_query = db((db.espacios_fisicos.dependencia_adscrita == int(request.vars.dependencia))).select(db.espacios_fisicos.ALL)
    ubicaciones_a_mostrar = []

    for l in ubicacion_query:
        ubicaciones_a_mostrar.append(l)
    return dict(ubicaciones=ubicaciones_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_responsable():
    session.forget(response)
    responsable_query = db((db.t_Personal.f_dependencia == int(request.vars.dependencia))).select(db.t_Personal.ALL)
    responsables_a_mostrar = []

    for l in responsable_query:
        responsables_a_mostrar.append(l)
    return dict(responsables=responsables_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_adscripcion_editar():
    session.forget(response)
    adscripcion_query = db((db.dependencias.id_sede == int(request.vars.sede))).select(db.dependencias.ALL)
    dependencias_a_mostrar = []

    for l in adscripcion_query:
        if re.match( r'Laboratorio\s[A-G]', l.nombre) or (l.id == 1):
            dependencias_a_mostrar.append(l)
    return dict(dependencias=dependencias_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_dependencia_editar():
    session.forget(response)
    dependencia_query = db((db.dependencias.unidad_de_adscripcion == int(request.vars.adscripcion))).select(db.dependencias.ALL)
    dependencias_a_mostrar = []

    for l in dependencia_query:
        if (re.match( r'Laboratorio\s[A-G]', l.nombre)) == None:
            dependencias_a_mostrar.append(l)
    return dict(dependencias=dependencias_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_ubicacion_editar():
    session.forget(response)
    ubicacion_query = db((db.espacios_fisicos.dependencia_adscrita == int(request.vars.dependencia))).select(db.espacios_fisicos.ALL)
    ubicaciones_a_mostrar = []

    for l in ubicacion_query:
        ubicaciones_a_mostrar.append(l)
    return dict(ubicaciones=ubicaciones_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_responsable_editar():
    session.forget(response)
    responsable_query = db((db.t_Personal.f_dependencia == int(request.vars.dependencia))).select(db.t_Personal.ALL)
    responsables_a_mostrar = []

    for l in responsable_query:
        responsables_a_mostrar.append(l)
    return dict(responsables=responsables_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_certificar_servicio():
    solicitudesid = request.post_vars.solicitud
    solicitud_info = db(db.solicitudes.id == solicitudesid).select()[0]
    usuario = db(db.t_Personal.f_usuario == auth.user_id).select()[0]
    servicio = db(db.servicios.id == solicitud_info.id_servicio_solicitud).select()[0]
    responsable = db(db.t_Personal.id == servicio.responsable).select()[0]
    fecha = request.now
    dependencia = db(auth.user_id == db.auth_membership.user_id).select()[0].dependencia_asociada
    if not(dependencia is None):
        dependencianombre = db(db.dependencias.id == dependencia).select()[0].nombre
    else:
        dependencianombre = "Laboratorio A"
        dependencia = db(db.dependencias.id > 0).select()[0].id

    registro = validador_registro_certificaciones(request, db)

    return dict(solicitud=solicitud_info,
                usuario=usuario,
                servicio=servicio,
                responsable=responsable,
                fecha=fecha,
                registro=registro,
                dependenciaid=dependencia,
                dependencia=dependencianombre,
                proyecto='Proyecto ' + registro)
